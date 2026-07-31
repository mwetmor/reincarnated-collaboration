# WR3-KITE-COMMIT — run charter v0 (grill-open)

> **STATUS:** v1 — GRILL CLOSED 2026-07-30. All four §5 forks resolved (R-WR3-7 ratified the
> K-1/C2-1/CAL-1 leans; R-WR3-8 ruled POOL-1 = BOTH). Mechanism-spec freeze pends two
> commissioned reads: gamora in-fight form-swap feasibility (R-WR3-8(c)) + legolas policy-package
> survey (R-WR3-9).
> **Conductor:** gandalf (`RUN-CONDUCTOR`). **Lineage:** direct sequel to WR2-ENCGEO-2026-07-29
> (charter closed §8.42 on the held watch predicate; verdict F-WR2-5). Desirable-run pattern
> (`operating-procedures/desirable-run-pattern.md`) governs; fit test passes F1–F4 for stage 1
> (stage 2 carries one Matt commitment-boundary, declared below).

---

## §0 — Intent (the owner's sentence is the target)

**R-WR3-2 (MATT-SIGNED, verbatim, 2026-07-30):** *"If the player kit plays as I did in the GD
game, and if the player and monster(s) stats and calculations are approximately similar to the GD
game that I played at level 13, then the player should win the majority of encounters."*

The run makes the sim's boss fight EARN that sentence: a player policy that plays the kit the way
Matt played it (kite, answer telegraphs, spend the speed surplus) against a boss that fights the
way the referent boss fought (commits to attacks, pays ground for them) — measured against the GD
L13 reference envelope, gated on competent-play majority win rate.

**R-WR3-1 (MATT-SIGNED mandate, from the two watch-verdict messages):** build kite + commit
against the frozen WR2 baseline immediately.

## §1 — Bounded substrate (countable, listable, diffable — frozen at launch)

1. **The WR2 battery of record** — 450 AFTER traces at
   `reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after/`
   (frozen §8.42; becomes this run's BEFORE arm — no regeneration, no reinterpretation).
2. **The F-WR2-5 pursuit diagnostic** (gamora `66c0e5f3`) — the measured decomposition this run
   builds against: ratio 0.70 graded; boss moves 100% of ticks, `commit_state` idle 76,714/76,714
   (no commit mechanism exists); player intents {reposition/advance/hold}, NO evade; median
   separation exactly 2.000 m in 180/180 boss fights; 132/132 novas eaten in production.
3. **The GD L13 reference envelope** (legolas `e34e6e7e`,
   `legolas/research/2026-07-30-gd-l13-reference-envelope.md`) — the R-WR3-2 referent, with
   per-row confidence grades CARRIED (HIGH/measured rows are decision-grade; LOW rows are not).
4. **WR2's finding cluster** — F-WR2-1 (subsumed into the envelope diff), F-WR2-2 (knife-edge
   `pre_endpoint` losses), F-WR2-4 (telegraph texture unverified in-ring; M-3 instrumented re-run
   owed), the 3-ticks-late ring-delivery incidental (§8.41), the WR2 wave-tail ledger.

## §2 — Conductor rulings at founding (veto-open, R-WR3-3 onward)

- **R-WR3-3 — the G-5a correction is ADOPTED.** Legolas falsified his own banked G-5a life rule
  (difficulty `characterLifeModifier` summed additively) against the one MEASURED monster pool we
  hold: Primordian 15,822 from the `.gdc`; multiplicative lands 15,891 (0.4%), additive
  overshoots 1.82×. All G-5a HP figures were high by 1.45× (trash) / 1.81× (champion+).
  Errata banners owed on the G-5a artifact itself (routed to legolas follow-on).
- **R-WR3-4 — the werewolf form-swap fact is ADOPTED; the G-7 U-1 hypothesis is CLOSED-FALSE.**
  `werewolf1.dbr` carries no `characterLife` at any rank — pure form-swap; the 759→1600 pool step
  is NOT the werewolf. Human-form 759 reconstructs to +6.6% (454 + 135 mastery + 220 weapon).
  Consequence: pool-fraction envelope rows must state WHICH pool (759 human / 1600 played-form)
  they divide by — an unlabeled fraction is the ninth family exhibit waiting to happen.
- **R-WR3-5 — attack-commit is the LOAD-BEARING mechanism; speed ratio 0.70 STANDS.** The
  envelope's sharpest fact: **the GD referent boss was FASTER than the player**
  (player:boss 0.99/0.81) **and Matt still kited it** — the kite windows came entirely from
  attack-commit and telegraph dodges, never from outrunning. Our boss is already 30% slower than
  the referent's relative speed. No gap-closer question remains for stage 1: the referent ran
  faster than the player and the fight still worked; commit is what we owe. (This also retires
  the WR2-era Mechanism-E "pursuit-speed law" sketch — measured moot before built, twice.)
- **R-WR3-6 — U-5 stands OPEN; 260.498 is the envelope datum.** `lastHitBy` 273.704 >
  `greatestDamageReceived` 260.498 is impossible for one hit; prefer the measured 260.498 (34.3%
  of 759) until legolas closes the anomaly. No decision may lean on the 273.704 figure.

- **R-WR3-7 (MATT-SIGNED, 2026-07-30): K-1, C2-1, CAL-1 leans RATIFIED as decision rules.**
  Kite fires on telegraphs + sustained-pressure rhythm; boss commit = wind-up + recovery lock;
  nova calibrates to scripted-heavy norm per projectile with 2× reaching ~the measured worst-hit
  fraction.
- **R-WR3-8 (MATT-SIGNED, 2026-07-30): POOL-1 = BOTH.** Matt, near-verbatim: the player-kit AI in
  the battle sim should replicate the choices a real player would make — including the form
  choice. Consequences: (a) all pool-fraction gates are computed against the CURRENT form's pool,
  never a fixed 759; (b) the policy owes a FORM-SWAP verb alongside kite — noting the battery's
  own legs already carry both pools (`pre` 759 human-form / `post` 1607 ≈ the played-form 1600),
  so what's missing is the IN-FIGHT choice; (c) whether in-fight form-swap exists as an engine
  mechanism is a stage-1 feasibility question routed to gamora before the mechanism-spec freeze —
  if absent, form-swap is staged as its own mechanism (K2) rather than silently folded into K.
- **R-WR3-9 (conductor, veto-open): the policy architecture ruling.** Stage 1's policy core is a
  DETERMINISTIC utility policy built in-seam (extending the existing intent system + the M-3
  piloted-competence heuristics into production), NOT a learned policy — battery determinism and
  gate reproducibility are non-negotiable, and adding verbs does not need learning. BUT the
  policy is built behind a **Gymnasium-compatible env interface from day 1** (observation/action
  contract), so scripted and learned policies are interchangeable: that adapter is what makes the
  entire off-the-shelf ecosystem (Stable-Baselines3 et al.) available later at near-zero
  marginal cost — as a competence probe and exploit-finder, not as the policy of record — without
  betting the run on it. Package-landscape verification commissioned (legolas, post-cutoff
  survey); ruling revisits if the survey surfaces a materially better path.

- **R-WR3-10 (conductor, veto-open): the form-swap feasibility verdict is IN — K2 STAGES
  SEPARATELY, and it SHRINKS.** Gamora's R-WR3-8(c) read (`gamora/notes/2026-07-30-wr3-formswap-feasibility.md`,
  engine HEAD `54536c30`): **ABSENT-CHEAP at the engine seam** (no mid-fight stat/pool/kit change
  mechanism exists anywhere in `simulation/`; `class_dict` bound once at `spatial_engine.py:6990`;
  a swap is a two-body atomic rebind reusing the existing factory functions, NOT a new intent —
  the movement enum must not carry a non-movement verb) — **ABSENT-STRUCTURAL at the fixture**
  (exactly ONE compiled kit exists, the transformed form; human-form Onslaught deliberately
  excluded at `kitcal_g5_scenarios.py:183`; a swap verb today swaps the werewolf for itself).
  The conditional fires: **form-swap = Mechanism K2, own lane, NOT folded into K.** Rulings:
  (a) **K2 is scoped CONSTANT-POOL** — per R-WR3-4 + the fixture provenance (`:57-59`), the
  referent's 759→1607 step is a GEAR event at the R2/R3 boundary, not a form event; the referent's
  form-swap changed kit/stats at constant pool, so HP-carry semantics (all three options
  UNDEFINED-by-representation, incl. a proportional-carry that would manufacture ~443 HP of free
  healing into a fixture whose A/B arms exist because healing is absent) are MOOT for this run and
  stay unruled. (b) **The R-WR3-8(a) schema amendment is K2-prep, sequenced FIRST in the K2 lane**
  — pool moves from the replica-frame HEADER (emitted once, `replica_frame_emitter.py:151-173`)
  onto the per-frame block, making every pool-fraction grader + S-7's `movement_speed_ms` join key
  form-aware BEFORE any form exists (MIGRATION owed; star-lord + drax downstream). Stage 1's
  mechanism scope stays frozen at K + C2. (c) **The compiled human-form kit is K2's owed input** —
  kit-spec extraction routed to legolas before K2's math note; math-before-code cannot start
  without knowing what the other form IS. (d) The four K2 pre-code decisions (swap trigger, swap
  cost/lockout, cooldown carry, and — only if a pool-changing form ever lands — HP carry) are
  ledgered as a future ELICITOR grill, not ruled here.

- **R-WR3-11 (conductor, veto-open): the package survey is IN — R-WR3-9 CONFIRMED, and the
  MECHANISM-SPEC FREEZE IS UNBLOCKED** (both commissioned pre-freeze reads have landed). Legolas
  (`legolas/research/2026-07-30-player-policy-package-survey.md`, all-primary-source, graded):
  no player-behavior package exists at any maturity — the behavior layer is empty *by
  construction* (a policy cannot be packaged without packaging its game); what IS packaged is the
  interface (Gymnasium — central API **frozen by maintainer commitment** since v1.0.0, seven
  releases honoring it, SB3 pinning `<2.0` on the bet) and the training stacks (SB3's own docs
  disclaim cross-platform/cross-torch reproducibility "even when using identical seeds"). BC path
  confirmed closed: `imitation`/`d3rlpy`/Minari all mandate action-aligned arrays; the `.gdc`
  holds aggregates. Adopted amendments: (a) **duck-typed Gymnasium compatibility, zero
  dependency** — the sim core exposes `reset(*, seed, options)`/`step(action)` with exact
  signatures in plain numpy/dataclasses; a thin `GymEnvAdapter` + `gymnasium` land only behind an
  optional `[rl]` extra; the 450-trace battery hot path never imports an RL package (auditability:
  the gate chain stays pure-Python and diffable — no non-diffable weights artifact ever enters a
  gate). (b) **Preference-comparison reward learning banked as the NAMED STAGE-3 candidate** —
  the one surveyed route from "no action traces" to "learned policy": Matt labels pairwise "which
  clip plays more like I did" and his *judgment* becomes the training signal in place of the
  inputs we don't have. Presupposes stage-1 geometry + the adapter; does not touch stage 1/2.
  (c) The 0.30 s reaction delay stands as **fast-competent-human by validated precedent**
  (DeepMind FTW: agents 258 ms vs humans 559 ms; injected-delay handicapping is the established
  human-likeness lever) — defended by precedent, not by an ARPG-telegraph measurement, which the
  survey confirms does not exist in the literature (ledgered: if stage 2 wants it numerically, it
  gets measured from Matt himself). (d) Follow-on probe candidate ledgered, not fired: Lin's
  playstyle-similarity metric (arXiv 2508.19152, no tooling located) if stage 2 wants a
  quantitative "plays-like-the-referent" column.

- **R-WR3-12 (conductor, veto-open): the stage-1 mechanism spec is ADOPTED**
  (`gandalf/notes/2026-07-30-wr3-stage1-mechanism-spec.md`, SPEC-AUTHOR draft verified under
  `⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC`) **with dispositions on its six §8 flags:**
  - **(8.1 — the §7.2 canon reconciliation. THE MATERIAL RULING; Matt's veto expressly invited.**)
    Canon (`telegraph-dodge-temporal-decoupling-2026-06-15.md` §7.2, Matt-ratified): *"do not let
    anyone try to make the sim 'model' the dodge."* Ruling: **§7.2 and Mechanism K do not
    collide.** §7.2's protected object is the DODGE SKILL — a timing-based ability the autobattle
    cannot honestly time, whose statistical credit would let the balance loop stop walling
    glass-close-ST coordinates. K is POSITIONAL MOVEMENT: no skill, no i-frames, no avoidance
    stat, no chance term (M-3's own header draws the line: "POSITIONAL, not statistical"). And
    the newer Matt-signed authority is explicit that the sim MUST model competent positioning:
    F-WR2-5 verbatim ("the kiting is worthless… the boss is pinned") + R-WR3-1's build mandate +
    R-WR3-2's competent-play target. Adopted fence: `kite_policy_v1` **default OFF**, armed by
    the WR3 battery-of-record ONLY — never the balance loop, generation, or production content
    paths; §7.2's actual protection (the balance loop keeps walling dodge-gated coordinates)
    is untouched. One word from Matt reverts this and stage 1 re-scopes. The spec's
    third-default-off-flag combinatorics observation is LEDGERED as a wave-tail finding.
  - **(8.2)** G3 stands as charter law; the `escape_rate` diagnostic column is adopted REPORTED
    beside it, ungraded. The two-sided band question (total escape would make the nova inert and
    collide with stage-2 CAL-1) is DEFERRED to the stage boundary, where it lands in the stage-2
    grill alongside the nova calibration it constrains.
  - **(8.3)** Reading CONFIRMED: stage-1 boss win rate is predicted to FALL or hold at 0.00 —
    K costs uptime and the DPS row is stage-2's. Stage-1 gates are geometry gates. **The
    owner-eye checkpoint brief carries this sentence ABOVE the render link**, so the watch is
    read against the right question (geometry verbs first, then numbers — charter §4).
  - **(8.4)** Obs idx 11 (`focus_commit_t_remaining_s`) is EXPOSED, through the delayed buffer.
    R-WR3-2's own words answer the fidelity fork: "plays as I did" — Matt at L13 had fought the
    referent repeatedly and knew the animations. The replicated player is the experienced one;
    the delayed buffer keeps him human.
  - **(8.5)** `Commitment.recovery_s` cross-seam routing: builder proceeds with the additive,
    default-inert field per the E4 as-emitted contract; the emitter-side MIGRATION question is
    ROUTED TO KNIGHT-RIDER and must be dispositioned before jack-ryan's Gate 2 on the build.
  - **(8.6)** ADOPTED AS A PRE-BUILD GATE: gamora duty-cycle measurement over the frozen
    `wr2_battery_after/` traces (realized inter-swing intervals; implied duty cycle at
    `T_lock ∈ {0.40, 0.60, 0.90}`) fires NOW, read-only, before any build line is written —
    math-before-code points at exactly this number, in both failure directions (G2-fails-on-
    arithmetic vs broken-easy fixture that stage 2 would calibrate against).
  - **Build sequencing:** the build commission to gamora fires after the duty-cycle read returns
    and grounds CAL-C1/CAL-C2 — which also holds a natural veto window open on (8.1).

- **R-WR3-13 (conductor, veto-open): the duty-cycle pre-build gate PASSES — T_lock 0.60 GROUNDED;
  build RELEASED.** Gamora's measurement (`gamora/notes/2026-07-30-wr3-duty-cycle-prebuild.md`,
  identity-asserted vs the frozen root, digest `b5ce25e6…`): boss realized inter-swing cadence is
  a METRONOME — median 1.500 s, exactly two values {1.5 s: 89.7%, 1.6 s: 10.3%} (tick-grid
  rounding of the U(1.411,1.511) draw; closed-form mean recovered to 0.00067 s over 4,432 draws),
  zero pursuit-gapped intervals — "the boss is pinned" restated at the cadence layer. T_lock 0.60
  → duty 28.6% (spec-literal) / 40.0% (cooldown-absorbing), fight-locked median 34.8%: neither
  §8.6 failure fires; safe ceiling on this fixture T_lock ≲ 0.75; bracket neighbours DISQUALIFIED
  (0.40 = one-tick window, a rounding artifact not a mechanism; 0.90 = degenerate on two
  independent measures, the broken-easy corner). **Flag rulings:**
  - **(F1+F2, ruled together — TICK REALIZATION):** T_lock realizes as **exactly 6 locked
    ticks** with the strike INSIDE it: windup 3 ticks (0.30 s), strike 1 tick (0.10 s, resolves
    per C2-L1), recovery 2 ticks (0.20 s). CAL register amended: **CAL-C1 := 0.30** (stays
    M-anchored — the lower bound of the measured 0.30–0.40 dead-time quantum) and
    **CAL-C2 := 0.20**; nominal T_lock 0.60 and the §3.4 daylight arithmetic (1.725 m) are
    UNMOVED, and the heavy-vs-basic hierarchy IMPROVES to 0.750/0.30 = 2.5×. This is the
    state-machine-pure realization of gamora's 3/3 recommendation (his windup=0.30 + 6-tick
    total are both honored; the spec's idle→windup→strike→recovery states stay distinct).
  - **(F3 — ADOPT the packet write):** the C2 fixture packet writes `wind_up_s = 0.30` onto the
    boss melee skill alongside `commitment_bin`/`cast_time`, so the minted telegraph advertises
    the REAL lead — the advertised-vs-real disagreement (cosmetic 0.5 today) does not survive
    into a world where the wind-up is mechanical ("Godot would render a lie" law, melee side).
  - **(F4 — ADOPT, one line of scope law):** C2 arms on the boss MELEE packet only; the nova
    cast remains UNCOMMITTED in stage 1. (The nova already has its own telegraph mechanism;
    committing the cast would move every §4 number and is a stage-2+ question.)
  - **(F5 — ADOPT as a free falsifiable check in the cell):** post-build, engaged swing cadence
    must stay on {1.5, 1.6}; if it moves, C2 changed the attack cadence — a BUILD DEFECT under
    the spec's own §3.4 law, not a balance outcome.
  - **(WARN-N1 — LEDGERED, emission-truth family):** the nova telegraph stream counts RESOLVED
    novas (132), not CAST novas (180) — a refused cast consumes the 6.0 s action budget and
    emits nothing; consumers reading cast frequency off the stream under-count 26.7% on this
    fixture. Routed to sequel space beside the 3-ticks-late ring delivery.
  - Evidentiary bonus banked: the first 6.8 s of every boss fight is DETERMINISTIC (nova cast
    t=0.700, first swing t=6.800, σ=0 across 180) — all fight variance enters after t=6.8 s;
    G2's onset>1.5 s exclusion is untouched but instruments should know the opening is constant.

- **R-WR3-14 (MATT-SIGNED 2026-07-30 — "agreed on both"): the GD AI state-machine question
  resolves as TWO chartered sequels, W-1 + W-2.** Matt's ask: witness aggro/spawn/attack/chase
  states for monsters/bosses inside the battle simulator. Ground truth from the substrate read:
  chase EXISTS (100% of ticks — the battery pins engagement), attack EXISTS (the metronome),
  attack-commit is IN FLIGHT (C2 adds windup/strike/recovery — the first real per-monster state
  machine), cast EXISTS (nova), leash-reset EXISTS dormant (R2 territory-guard full-heal return,
  `spatial_engine.py:1957`); idle/wander/spawn/proximity-aggro are ABSENT BY DESIGN in the
  battery, which forces engagement at t=0. Rulings:
  - **(W-1 — witness labels; emission truth, post-stage-1):** add a per-frame `ai_state` label
    to the replica-frame emission — vocabulary {approach, engage, windup, strike, recover,
    leash-return} — so any watch/render shows the monster's state explicitly rather than
    inferring it from geometry. NO behavior change; label-only. Rides with the K2-prep
    replica-frame schema amendment (R-WR3-10) or fires as its own micro-cell, whichever lands
    first. Godot-would-render-a-lie law applies: the label must derive from the SAME state
    variables C2 executes, never a parallel reimplementation (one-implementation, R-M3-1 family).
  - **(W-2 — encounter-AI lap; chartered between stage 2 and the full-mix acceptance gate):**
    proximity aggro (radius-triggered engagement instead of forced t=0 pinning), pack social
    aggro (aggroing one member pulls the pack per GD's social-aggro convention), and
    leash-in-combat (the dormant R2 return armed under battery conditions). SEQUENCING REASON,
    load-bearing: R-WR3-2's "majority of encounters" is measured on the FULL MIX including pack
    fights; an always-pinned pack is strictly HARDER than the GD referent (real packs stagger
    engagement via aggro radii and body-blocking approach) — measuring the acceptance gate
    without W-2 would bias the win rate DOWN vs the intent sentence. So: stage-1 gates → owner-eye
    → stage-2 calibration → W-2 lap → R-WR3-2 acceptance measurement (boss + full mix).
  - Per the conductor's commitment at ratification: **nothing in W-1/W-2 fires until the
    in-flight stage-1 build lands its G1–G5 gates.** Spawn/wander remain out of scope for the
    simulator (full-gameplay-loop functions — Matt's own suspicion, confirmed).

- **R-WR3-15 (conductor, veto-open): STAGE-1 GATES STAND — the build report
  (`gamora/notes/2026-07-30-wr3-stage1-build-report.md`, engine `6de80aab`+`a6c6bcf9`, verified:
  3,523/3,523 unit tests re-run by the conductor at 1.27 s, zero new regression failures against
  the 81-name baseline) is ACCEPTED, with five finding dispositions:**
  - **(F-1 — the HALT ruling; disposition (c) with a chartered debt):** the **11-seed diagnostic
    arm is ACCEPTED as the stage-1 mechanism-existence evidence** — explicitly NOT a battery of
    record, G2 at-threshold (+0.0091) noted. Option (a) — suspending A-DMG-1 for the WR3 arm —
    is REFUSED as pin-silencing: the pin fired TRUTHFULLY (the HELD boss-damage regime IS
    falsified at r≈11 m, per-projectile 290.36 > measured ceiling 260.5); buying 19 more seeds
    by disarming a falsification pin is grading against a known-broken ruler. Option (b) is
    fenced by spec §7 (no nova number moves in stage 1) — gamora was right to take nothing.
    **Chartered debt:** the battery of record (full 30-seed) RE-FIRES after stage-2's CAL-1 nova
    calibration re-establishes a holdable damage regime — where R-WR3-2's acceptance measurement
    required a fresh full battery anyway. Stage 1's question — does the geometry exist — is
    answered decisively on the diagnostic arm: separation unpinned (+0.471 m), degenerate
    signature 66/66 → 0/66, escapes exist (0 → 60/114), whiffs exist (95.55 %), and the
    duty-cycle prediction survived contact to four figures (0.400 predicted / 0.3992 realized).
  - **(F-1+F-2 held together — stage-2's first-order input):** the nova's outer-band payload
    step (207.40 → 290.36 at r ≈ 10 m) is now indicted from BOTH directions on one battery —
    over-lethal on seed 74000811, fully INERT (0/114 crossings) on the other eleven. §8.2's
    two-sided worry is live. **CAL-1 nova calibration and the escape-rate band are ONE stage-2
    grill item, not two** — both facts are the same number. WARN-N1 (resolved-vs-cast
    undercount) joins that grill as the emission companion.
  - **(F-4 — §8.3's prediction FALSIFIED; owner-eye brief REWRITTEN):** boss win rate went
    0.33/0.36 → **1.00/1.00**, not down — the boss lands 4.45 % of swings and 0 % of novas;
    K's uptime cost is real and simply dominated. This is §8.6's broken-easy direction,
    announcing itself. NOT a stage-1 gate failure (stage-1 gates are geometry gates, correctly)
    and NOT a build defect: `bout_max`/`release_m`/`pressure_threshold` are stage-2-owned [CAL]
    rows chosen for defensibility, not correctness. **The owner-eye brief's headline sentence is
    REPLACED** — Matt watches a mechanism-existence proof, not a balance state, and the brief
    says so ABOVE the render link (the R-WR3-12(8.3) slot, corrected content). Mean boss fight
    duration 82.2 s landing inside the GD 59–118 s band is banked as the one envelope row the
    mechanism moved INTO band by itself.
  - **(F-5 — deviations ratified):** **SC-K-1 RATIFIED as spec completion** — the spec's §2.6
    field list could not implement its own §2.4 yield condition 3; the omission was the spec
    author's (conductor's own DRIFT-CRITIC finding against his own spec, on record). **BS-1
    RATIFIED as declared stage-1 scope** — replay-backed `step` with exact contract; steering is
    stage-2's named prerequisite. **The S-2 predicate/cell conflict resolves in the cell's
    favor** (grade the predicate, report the wall-share beside it; wall-share improved
    0.0223 → 0.0158 — K un-cornered the player, an unasked-for good).
  - Banked with approval: the Discipline #11 smoke-catch (`is_boss` lives on `SpawnSpec`, not
    `SpatialEntity` — a mechanism that would have armed and measured NOTHING with every counter
    a clean zero, caught by the first ablation smoke). SS-C2-1's emitter-side MIGRATION remains
    OPEN with knight-rider per R-WR3-12(8.5) — must disposition before jack-ryan Gate 2.
  - **Sequence now:** owner-eye render commission (drax) → Matt watches → stage-2 boundary
    grill (nova/escape-band + player-DPS + K-calibration rows) → W-2 lap → battery of record →
    R-WR3-2 acceptance.

- **R-WR3-16 (conductor, veto-open; Matt's eye recorded): OWNER-EYE #3 LANDED AND PASSED on the
  geometry verbs.** Drax's render (`drax/notes/2026-07-30-wr3-stage1-owner-eye-render.md`, godot
  `72723ca` pushed; fight `pre`/boss/B/74000802 — chosen so the BEFORE clip is byte-identically
  the WR2 owner-eye AFTER clip: one seed, three geometries, one lineage). **Matt watched the
  side-by-side and signed the geometry: "looking REALLY good"** — with the sequel asks (AI-state
  labels, then full scene baking) noted. Conductor confession banked: the commission's fallback
  pick (74000800) fires NO nova in any arm/leg — drax's measured selection caught it; absence is
  data, and the default was wrong. Finding dispositions:
  - **(D-F1 — the 7-vs-6 tick disagreement; ROUTED to gamora, blocking the baked watch's label
    layer):** emitted `commit_state` reads windup 4 / strike 1 / recovery 2 = **7 ticks**
    (3,096/3,098 episodes, zero variance; telegraph mint-to-fire lead agrees at 4), while the
    build report declares 6 and the duty arithmetic sides with 6 (measured committed-tick share
    0.3992 ≈ 6/15 = 0.400; 7 ticks would read ≈0.467). Most probable: the initiation tick emits
    `windup` but is not movement-locked — an inclusive/exclusive sampling fencepost, prose vs
    emission. **Gamora verifies which variable each reader reads and DOCUMENTS the convention;
    if the movement lock is actually 7 ticks, that is a build defect against R-WR3-13 and
    re-opens F1.** W-1's `ai_state` field must DECLARE its sampling edge so label and lock agree
    by contract, not coincidence.
  - **(D-F2 — the metronome, quantified):** from median onset 18.8 s the (windup, strike)
    separation pair freezes — median fight spends **69 % of commit episodes inside one frozen
    bit-identical pair** ((2.000, 2.7584) on 46/66). The legible surface of F-4: the swing is
    clockwork and the deterministic policy solves it exactly. **Stage-2 grill gains a row:**
    frozen-pair share becomes a REPORTED (ungraded) battery column, and drax's §7 question goes
    to Matt verbatim at the grill — is "the player has solved the boss's swing" the thing to
    calibrate away from, or the geometry he wanted proven first?
  - **(D-F3 — C_reach custody; ADOPTED):** C_reach (2.5 m) lives only in a cell's grading
    artifact; drax verified it against all 3,096 strikes (0.091 m of clean air between LANDED
    max 2.4837 and WHIFFED min 2.5750) before drawing. **Emit it beside `presentation_units`**
    in the leg report/g5_header — same custody argument that closed the nova unit payload
    (R-WR2-15(2)), one layer out. Rides the schema amendment below.
  - **(D-F4 — routed to jack-ryan as a consumer-discipline candidate):** third value-set growth
    in three runs (`reposition`, `evade:*`, `commit_state` non-idle); drax's stated rule — *on
    this schema, an exhaustive match without a default arm is a latent silent-wrong-render* —
    is discipline-shaped and belongs in his stack, not this ledger.
  - **(D-F5/GAP-1 — ledgered):** the telegraph channel is per-attacker-per-skill, NOT per-swing
    (`commit_state`/W-1 is the only per-swing source — consumers warned); the tracking-camera
    rule change folds into the presentation baton, not this run.
  - **Cross-reference:** the parallel LR/presentation session banked cell **AMB-REFIT**
    (`gandalf/notes/2026-07-30-ambient-refit-fold-in.md`, Matt-directed: ambient extents refit +
    overhead AI-state tags on enemy NPCs, trace-driven instrument-overlay). Zero WR3 rulings
    consumed there; this run's W-1 emission is the AUTHORITATIVE source those tags upgrade to
    when it lands.
  - **NOW FIRING (post-stage-1 unlocked, per R-WR3-14):** the **K2-prep schema amendment as one
    bundle** — (i) D-F1 verification + convention doc, (ii) W-1 per-frame `ai_state` with a
    declared sampling edge, (iii) C_reach into the header (D-F3), (iv) the R-WR3-10 pool-header→
    per-frame move. Cross-seam schema change → **MIGRATION.md owed** (ADR-004; drax + galadriel
    consume). Gamora's seam; battery re-emission NOT required for the amendment itself.

- **R-WR3-17 (MATT-SIGNED 2026-07-30 — the stage-2 grill OPENED by Matt directly): the target
  band and three adjustments.** Matt, verbatim intent: *"another few adjustments to get back to
  the 40%-60% win rate band"* — sequenced AFTER the baton pass (W-1 → baked watch). Rulings:
  - **(a — TARGET BAND):** stage-2 calibration target is **boss-encounter win rate in the
    40–60 % band**. Conductor's reading, veto-open: the band governs BOSS fights; R-WR3-2's
    full-mix "majority of encounters" (>50 %) is unchanged and is still the acceptance sentence.
    Current state: 100 % (66/66) — the band is the calibration distance.
  - **(b — SPEED PARITY, Matt-directed):** re-run with player speed = boss speed (today 1.43×
    player-favored; the GD referent measured the boss FASTER, 0.99/0.81). Adopted as a stage-2
    CAL row. Design note banked: K's escape windows derive from the LOCK, not the speed delta —
    parity kills free inter-commit kiting (K-T2b pressure regime), which is the knob working.
    Gate note: G1–G3 thresholds were registered against 1.43×; stage-2 re-registers its own
    gates before any battery is graded (no silent threshold reuse).
  - **(c — DODGE SKILL, Matt-directed, fence-preserving):** add the GD Evade dodge (cooldown +
    range from the referent) to the player toolkit — **behind the same battery-only fence as
    `kite_policy_v1`** (flag, default OFF, never the balance loop / generation). Canon §7.2
    walling is PRESERVED: the grading sim still never models the dodge; the fidelity battery
    models it because the referent player HAD it. Parameters are OWED FROM THE REFERENT
    (legolas commission below) — no number enters from memory. Design pairing banked in Matt's
    framing: boss-you-cannot-outwalk + cooldown-gated-escape = GD's commit-window resource
    grammar; (b) and (c) are ONE mechanism pair, calibrated together.
  - **(d — REFERENT CONFIRMATION, Matt-demanded; promoted to MANDATORY):** today's windup
    0.30 s / recovery 0.20 s are OUR-SIM-anchored (the duty-cycle dead-time quantum,
    R-WR3-13) — NOT GD-confirmed. The ledgered legolas .anm attack-cadence question is promoted:
    **the boss's actual GD wind-up/cast/recovery values must be extracted and reconciled before
    stage 2 locks CAL-C1/CAL-C2.** If GD disagrees with 0.30/0.20, the referent governs.
  - **(e — envelope honesty restated for the record, answering Matt's last question):** stats
    are "approximately similar" (his R-WR3-2 wording), NOT exact — kit compiled from his L13
    save; four named deltas stand in §3 (DPS below band, nova 1.6–3.4× over, speeds generous,
    HP ratio ~15 % in-band). Stage 2 closes them.
  - **COMMISSIONED (legolas, referent-extraction):** GD Evade parameters (cooldown, distance,
    i-frame/immunity behavior, availability at L13 in Matt's session) + boss attack animation
    timings (wind-up/contact-frame/recovery; nova cast time) + exact speed values for (b).

- **R-WR3-18 (conductor, veto-open): the W-1/K2-prep amendment LANDS — D-F1 resolves NO-HALT,
  and the conductor's own arithmetic is CORRECTED on the record.** Gamora's cell
  (`gamora/notes/2026-07-30-wr3-w1-schema-amendment.md`, engine `2a33881e`, verified; evidence
  roots banked at `883c0a49`):
  - **(D-F1 VERDICT — the lock is SIX ticks; R-WR3-13 F1 STANDS):** `N_emit = N_lock + 1` by
    loop-phase order — the frame is written AFTER the action phase that enters `windup`, the
    lock is read at navigation BEFORE it. Inclusive-on-emit, exclusive-on-lock; convention now
    DOCUMENTED in the schema. Proven by the falsifier, not the prose: with all move scales
    zeroed, the first emitted `windup` tick still navigates a full 0.4025 m step on
    3,098/3,098 episodes — the initiation tick is not locked. **Conductor correction banked:**
    R-WR3-16's "duty arithmetic sides with 6" was WRONG twice — the share counter reads the
    EMITTED state (it cannot see the lock), and 0.3992 ≈ 6/15 was a coincidence of two wrong
    inputs (realized period 16.18 ticks + a 68-tick commit-free opening; the true identity is
    46.94 × 7 / 821.5 = 0.400; a 6-tick emission would read 0.3427). Right verdict, wrong
    proof — the falsifier is the proof. INFO banked: the lock is a NAVIGATION lock (boid
    push-apart drifts ≤ 0.148 m, median 0.000); HEADING is bit-exact frozen (C2-L2 intact).
  - **(Named decisions RATIFIED, all five):** AI-D1 (contact discriminator = the selector's own
    extracted range predicate, cooldown excluded, ∃-MAX reach not C_reach's MIN — label and
    swing-legality are one expression); AI-D2 (commit outranks leash-return, movement-path
    precedence — **with the dormant action-vs-movement precedence DISAGREEMENT ledgered to
    W-2**: when leash-in-combat arms, the two mechanical paths conflict and W-2 must resolve
    the MECHANICS, not just the label); AI-D3 (three-valued presence; corpse = `null`);
    K2P-D1 (additive MIRROR not literal move — the ruling's wording was imprecise, the
    additive law governs); K2P-D2 (per-frame speed unconditional; **two fields, same name,
    different meanings** — MIGRATION §4 carries the consumer warning).
  - **(Custody landed):** `commit_reach` in g5_header AND leg report — boss 2.5 m reproducing
    drax's verified value, shaman 18.5 m proving a leg-wide scalar would have been wrong.
  - **(Evidence):** re-emitted smoke fight = the RENDER fight (`pre`/boss/B/74000802) —
    2,445/2,445 records byte-identical with new keys stripped; 3,553 tests pass; extractions
    differentially proven (1,470 grid cells + 40k rosters, 0 mismatches). **THE BAKED-WATCH
    INPUT EXISTS:** `output/kitcal_g5/wr3_w1_smoke/` carries 74000802 with `ai_state` live —
    the presentation session's AMB-REFIT tags upgrade from derived to authoritative HERE.
  - **(Owed):** full `tests/` re-run verdict at jack-ryan Gate 2 (in flight >18 min at cell
    close; corroboration, not the proof). `s11_det` replicate deliberately NOT banked (G5
    byte-identity + digests protect it). MIGRATION.md landed at
    `simulation/MIGRATION.md` (ADR-004; drax + galadriel consumers).

- **R-WR3-19 (conductor, veto-open; one fork HELD FOR MATT): the referent extraction is IN —
  R-WR3-17(d)'s answer, and R-WR3-17(b)'s premise is FALSIFIED.** Legolas
  (`legolas/research/2026-07-30-wr3-stage2-referent-extraction.md`, verified; the `.anm` format
  documented first-of-kind, closing the ledgered question):
  - **(EVADE — parameters DETERMINATE, all MEASURED):** cooldown 3.0 s, 1 charge, max range
    10.0 u, 11 u root motion in 0.282 s inside a 0.333 s lock, **NO i-frames** (absent from the
    record, its template, and all nine GDX3 runes). Present + ENABLED in Matt's L13 save,
    unmodified. Purely positional → the §7.2 walling survives on the mechanism's own nature,
    not just our fence. R-WR3-17(c) builds to THESE numbers. (In-form werewolf dodge CLIP is
    U-1-blocked — see matt_to_do T10; the skill parameters above are not.)
  - **(BOSS TIMINGS — GD DISAGREES with 0.30/0.20, and per R-WR3-17(d) THE REFERENT GOVERNS):**
    Primordian melee wind-up **0.489 s** / recovery **0.879 s** / T_lock **1.369 s** rooted
    (0.000 u root motion — the lock model itself CONFIRMED), cycle 1.719 s; nova telegraph
    0.80–0.89 s (vs our 0.30 written). Cycle length is in band (~15 %); **the duty cycle is
    INVERTED** — GD's boss is rooted 79.6 % of its cycle, ours 28.6–40 %. Their boss buys
    cadence with commitment; ours buys it with free idle. **Tension named, not silently
    adopted:** referent T_lock 1.37 s sits far above gamora's measured safe ceiling
    (T_lock ≲ 0.75 s at OUR 1.5 s cadence) — adopting referent durations forces the cadence
    toward the referent's 1.72 s too. This is the stage-2 grill's first agenda item, with
    gamora feasibility at the table (CAL-C1/C2 re-anchor + cadence draw + §3.4 daylight
    arithmetic all move together). U-3 (which pak modifier hits the nova telegraph, 0.80 vs
    0.89) and U-4 (recovery = upper bound) are the spec's to name.
  - **(SPEED — R-WR3-17(b)'s premise MOVED; fork HELD FOR MATT, commitment boundary):** the
    charter's 0.99/0.81 "boss faster" row measured **Warden Krieg** — the WRONG boss. Against
    Primordian (the fixture's boss), Matt was **1.29–1.33× faster** under both open composition
    models; our 1.43× is IN BAND, 7–11 % over. **Parity (1.00×) would over-correct PAST the
    referent** — boss-favored beyond anything Matt actually fought — while stage 2 is
    simultaneously landing a 2.3× longer lock. §3 speed row corrected in place. Fork to Matt
    (legolas's three options, conductor lean appended): (1) parity as deliberate
    over-correction; (2) referent-matched 1.30×; **(3) spend the correction on the COMMIT duty
    cycle instead — the measured fidelity gap — and trim speed only to 1.30× (lean: 3, which
    subsumes 2; both boss-favoring levers at full strength risks overshooting the 40–60 % band
    from above).**
  - **(ROUTED):** matt_to_do **T10** filed (GDX3 `Creatures.arc` pull — werewolf-form player
    timings, the sole blocking UNKNOWN; boss + speed rows complete without it). Legolas's §6
    corrections to his own prior artifacts noted (envelope U-1 closed; wr1-extraction G-1/G-3
    closed for base-game creatures). U-5 carried unchanged.

- **R-WR3-20 (Matt-signed, 2026-07-30) — the stage-2 calibration package: Option 3 +
  Primordian parity.** Matt verbatim: *"Option 3 — fix the duty cycle, trim speed to 1.30x.
  Let's bring parity to the dodge and cast/wind up and any other GD Primordian boss behaviors."*
  - **Ruled by signature:** (a) player:boss speed **1.43× → 1.30×** (referent-matched); (b) boss
    commit durations go REFERENT — melee wind-up **0.489 s** / recovery **0.879 s** / rooted
    **1.369 s**, cycle **1.719 s**. Cadence moves WITH the lock (the R-WR3-19 tension resolves
    referent-ward: 1.5 s cadence dies, 1.719 s replaces it — they are one package). Nova
    telegraph goes referent-range 0.80–0.89 s (build takes **0.85** midpoint; U-3 pak-modifier
    flag stays open, veto-open). (c) **Evade enters the player kit at GD parameters** — 3.0 s
    cooldown, 1 charge, 10.0 u range, 0.333 s lock, NO i-frames — behind the same battery-only
    fence as `kite_policy_v1` (canon §7.2 untouched; unit conversion derives from the
    extraction's own §3 composition models, never asserted fresh). (d) *"any other GD Primordian
    boss behaviors"* = **referent-parity as standing rule for the boss's behavior surface**:
    where the extraction measured, the measurement governs; unmeasured surfaces get spec-named
    leans, ledgered here.
  - **Conductor rulings under the signature (veto-open):** CAL-1 fires in the SAME build as
    ratified (R-WR3-7 lean) — nova per-projectile to scripted-heavy norm (~10–15 % of pool) with
    the 2× quantum reaching ≈ the 34.3 % measured worst. This is also the **A-DMG-1 unblock**:
    the 30-seed battery of record re-fires under stage-2 params (R-WR3-15's deferral discharges).
    Player DPS calibrates toward the 310–620 band interior (lower-mid ≈ 400) pending T10
    werewolf-cadence refinement. **Gates RE-REGISTER before the battery** — stage-1 gates were
    tuned at 1.43×/0.30 s; carrying them forward unexamined would be gate-shopping in reverse.
    **Feasibility pre-pass MANDATORY** (Discipline #1, math-before-code): daylight arithmetic at
    referent durations + 1.30× BEFORE code — gamora's T_lock ≲ 0.75 s safe ceiling was measured
    at 1.5 s cadence and must be re-derived at 1.719 s; if the arithmetic shows a degenerate
    regime (boss permanently outranged or kite trivially safe), HALT and route back to Matt
    before build.
  - **(COMMISSIONED):** gamora stage-2 build, background. Deliverable:
    `agentic_orchestration/gamora/notes/2026-07-30-wr3-stage2-build-report.md`.

- **R-WR3-21 (Matt referent observation → DBR-VERIFIED, 2026-07-30) — the nova is a STAR, not a
  ring.** Matt verbatim: *"Primordian's ice nova is actually not a full circle radius. It seems
  more like a multi-pronged star ice-shot which can be avoided by moving between prongs of the
  star (which is what I did)."*
  - **Conduct:** the in-flight stage-2 build was STOPPED (killed during read-only pre-pass, no
    code written) rather than let it register gates against a ring the referent doesn't have.
    Targeted legolas extraction fired first; recording = claim, DBR = verification.
  - **CONFIRMED** (`legolas/research/2026-07-30-wr3-nova-star-geometry.md`, commit `52bddc33`):
    `primordian_frigidring` = **16 prongs / 22.5° / 360° even, no randomization**; prong collision
    radius 0.10 u (threat corridor 0.84 u vs player 0.32); speed **14.0 u/s**, range 12.0 u in
    0.857 s, despawns without end-blast. Gaps close below **r ≈ 2.15 u** (at melee-hug the star
    IS our uniform ring); at r = 10 the clear gap is 3.06 u = 4.8× player diameter. **Radial
    outrun is arithmetically impossible below r ≈ 7.9 u — the referent's escape verb is ANGULAR**
    (constant 0.42 u lateral clearance ≈ 0.053 s, ~7 % of the 0.80 s telegraph). Payload is full
    per prong, no piercing, **distance-banded 50/100/140 % at 2.5/9.0 u**; double-hit confined to
    r ∈ [0.77, 2.15] u and priced to ≈1× by the 50 % close band. Rider our model lacks entirely:
    **1.3–1.8 s hard freeze + 77 cold over 2 s** at rank 5 — the freeze OUTLASTS the boss's whole
    1.369 s melee lock. Legolas's one-liner, adopted as the design statement: *the referent's
    nova is not a test of distance, it is a test of bearing — cheap to pass, expensive to fail.
    Our sim inverts both halves.* Telegraph attribution confirmed (same skill, same `Roar` anim);
    Matt's description matches frigidring and nothing else in the kit.
  - **Conductor rulings under R-WR3-20(d) referent-parity (veto-open):** (1) star geometry
    ADOPTED, data-driven (prong count / spread / corridor / speed / range as packet fields).
    (2) The kite policy gains the **angular-dodge verb**; radial escape retained only where the
    arithmetic permits it (r ≳ 7.9 u). (3) **CAL-1's ratified lean is SUPERSEDED by measurement**:
    the 2× close quantum RETIRES (the referent prices overlap to ≈1×); per-prong payload takes
    the measured rank-5 block (148 phys + 247 cold + riders) under the 50/100/140 bands —
    far-band worst ≈ 34.6 % of the 1600 pool, landing ON the 34.3 % measured-worst ceiling the
    old lean was aiming at by construction. **A-DMG-1's 260.5 ceiling RE-DERIVES under this
    model** — the pin discharges by re-derivation, not silencing. (4) Freeze + cold-DoT riders
    enter (battery-only, as all of stage 2). (5) U-1 ring phase: **hostile assumption** —
    prong-0 on target — flag carried. (6) **Full-kit parity per Matt's signature** ("any other
    GD Primordian boss behaviors"): `primordian_wave` (directional cone 3→6 u over 16 u),
    `chillbane_blizzard` (aerial bombardment, 8 s), `primordian_icearmor` (25 % absorb, 12 s/32 s)
    enter the spec. Phase-A feasibility RANKS them; the star correction is the non-negotiable
    core, the other three phase in behind it — phasing is reported, never silently dropped.
  - **(RE-COMMISSIONED):** gamora stage-2 relaunched with the star baked in; same deliverable
    path. Pin-path correction noted for the record: the true asset pins are
    `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (+ legacy `…/vendor/grim-dawn/`),
    not the engine-vendor path the first commission named.

- **R-WR3-22 (Matt session-recall corroboration, 2026-07-30) — the full kit FIRED in the
  referent fight.** Matt verbatim: *"aren't there also some other moves with different geometries
  which we haven't yet represented such as conical or wide lane or a circle which is cast away
  from the boss, maybe towards the character? I thought I saw Primordian also have some or all of
  these."* — matches the DBR enumeration (star extraction §9) one-for-one: conical/wide lane =
  `primordian_wave` (3→6 u widening front over 16 u); remote circle at the character =
  `chillbane_blizzard` (aerial bombardment targeted at the player, 8 u target radius / 15 u
  scatter, 8 s). **Significance ruled (veto-open):** Matt's recall is session evidence that wave
  + blizzard fired in the fight he won — so the 40–60 % band (R-WR3-17) describes a fight that
  INCLUDES them. Full-kit modeling priority firms from "parity by directive" to
  "referent-session-observed." Phase-A ranking latitude stands, but any phasing that defers wave
  or blizzard must state what the deferral does to band comparability — a boss missing the moves
  Matt dodged is an easier boss, and a win rate measured against it is not Matt's number. Design
  note for the record: the referent kit is a complete movement-verb curriculum — bearing (star),
  lane (wave), area (blizzard), rhythm (melee commit) — four distinct dodge verbs, one per
  geometry class. That is the boss-design grammar the fixture inherits.

- **R-WR3-23 (conductor rulings on the stage-2 landing, 2026-07-30) — the band FAIL is the
  priced deferral, and the run buys the load-bearing pair.** Report verified
  (`gamora/notes/2026-07-30-wr3-stage2-build-report.md`; engine `92381a23`, collab `39cd441f`,
  conductor pushes). Headline: boss win **1.00** (FAIL, above 0.40–0.60) · full-mix **1.00**
  (R-WR3-2 majority PASS) · duration 36–39 s (FAIL, below 59–118) · **duty cycle 79.1 % vs
  referent 79.6 %** — the R-WR3-19 fidelity gap CLOSED to half a point · melee whiff 100 % ·
  nova crossings 0.733 → 2.20–2.33 (the inert-nova finding discharged). Both FAILs were
  pre-registered by the math note in direction and cause: **the loss mechanism lives in the
  phased skills.** Rulings on the report's §10:
  1. **Phase-A RE-RANKING RATIFIED** — `primordian_wave` + `chillbane_blizzard` are
     LOAD-BEARING; the band is unreachable without them by any [CAL] setting. This is
     R-WR3-22's comparability clause landing as arithmetic. **STAGE-2b commissioned:** wave
     (widening-RECTANGLE resolver, NOT the arc primitive — the arc inverts the r ≈ 9.5 m
     crossover that makes the wave price the kite), blizzard (drop scheduler + own RNG
     sub-stream), icearmor (timed absorb), + F-2's in-flight steering half of the angular verb.
  2. **A-DMG-1 narrowing + A-NOVA-2 RATIFIED** — *"worst-taken is a lower bound; an absence
     produced by competence cannot ceiling a measured payload"* is the correct discharge shape,
     and A-NOVA-2 bites (it is the pin that catches the h = 0.60 counterfactual).
  3. **U-BODY-1 RATIFIED** — the corridor composes from the referent's two bodies; the h = 0.60
     hybrid (513.6 spike = 67.7 % of pool, manufactured by our 1.56×-fatter body wearing Crate's
     bands) had no referent behind it. Carried open: `ENTITY_RADIUS_STANDARD` 0.5 vs referent
     0.32 is a fixture-wide delta with a named consequence — a future Matt fork, not this run's.
  4. **SS-S2-2 RATIFIED** — Mechanism D disarmed; its Matt-signed premise ("damage cannot be
     avoided") is discharged by the star's measured 0.42 m escape. Consequence accepted: the A/B
     is a PACKAGE comparison; no stage-2 column attributes to a single mechanism.
  5. **F-3 refusal RATIFIED WITH EMPHASIS** — CAL-K2 = 4.00 lands in the band and was REFUSED as
     a noise fit on a chaotic, non-monotone sweep. A number that will not reproduce is not a
     calibration. Derived anchors stand. The sweep's chaos itself (kite bout phase-locking
     against the boss's 1.769 s metronome) is BANKED as a grill/design observation.
  6. **SCHEMA — lean amendment ADOPTED:** `spoke_offset_rad` + `t_launch` + projectile velocity
     ride the TELEGRAPH record (additive; consumers reconstruct prong fronts procedurally).
     Per-frame per-prong positions REFUSED — emission weight in the serial pipeline for a
     derivable quantity. Built in stage-2b; MIGRATION + replica-frame spec note owed; drax
     consumes at bake.
  7. **F-2 in-flight steering** → stage-2b scope (item 1).
  - **Sequencing ruling:** wave/blizzard payloads are CARRIED-EXT, not M — and stage-2b's
    headline verdict WILL lean on them, so per the report's own §8 rule a **legolas commission
    fires FIRST**: measured payload blocks + riders + cadence for `primordian_wave` and
    `chillbane_blizzard` (+ icearmor confirmation) at boss-level-16 ranks. Stage-2b builds on
    returned numbers, never on carried-ext.
  - **EV note:** `ev_dashes = 0` across the whole battery — the walk sufficed under the
    telegraph limb, as the math note predicted. Evade's marginal moment is expected to arrive
    WITH the wave (the r ≳ 9.5 m no-walk-escape zone); stage-2b re-measures.
  - **Owner-eye:** the next watch is the stage-2b render — rendering the current arm would show
    Matt a boss missing the moves he dodged.

- **R-WR3-24 (payload extraction lands, 2026-07-30) — carried-ext FALSIFIED, a missing damage
  stage, and the boss-level correction.** Artifact verified
  (`legolas/research/2026-07-30-wr3-wave-blizzard-payloads.md`, rides this push). Rulings:
  1. **Carried-ext 122/210 and 58/111 are DEAD** — they are the records' rank-4 arrays exactly,
     produced by binding `skillLevel = charLevel/4+1` to the PLAYER's 13 instead of the
     monster's own level. Correct rank **5**, invariant across the whole boss-level band
     (retroactively securing the star note's rank-5 frigidring block).
  2. **Boss level 16 → 18–19 ADOPTED** — proxy chain (`p_wightmire_slitha01` → `lv6_hero`) +
     the envelope note's measured `lifeAndMana` anchor (0.4 %). The commission's "16" treated
     player level as spawn level. Moves only the charLevel-keyed passives (melee base, damper).
  3. **THE DAMAGE STAGE:** every Primordian outgoing number passes **×0.2625** at Normal/1p
     (`armorbase05` −73 pool + `damage_totaladjuster` +8, then pak −25 % multiplicative) —
     system-wide (93.4 % of 1,307 Monster records), operator adjudicated against a measured HP
     anchor, corrects the star note's own "nothing projectile-side" claim (§7 correction
     logged). **ADJUDICATION MANDATE, stage-2b Phase A, BLOCKING:** reconcile GD's outgoing
     composition with the fixture's delivery chain (M-1 mitigation replica + Matt's gear vector)
     into ONE named stage map — which GD stage maps to which fixture stage, no double-count, no
     silent omission. Stage-2's nova delivered 256.82 vs referent worst-taken 260.5 under RAW
     payload: **convergence or coincidence is exactly what the stage map decides.** A-NOVA-2
     re-derives under the adopted map; HALT to conductor if the map moves the nova's delivered
     regime materially (>15 %).
  4. **Wave adopted M:** rank-5 153 phys / 272 cold (point values, no roll), cold DoT 91/3.0 s,
     + an UNDOCUMENTED rider — 30 %/3.0 s damage-reduction debuff. Hits ONCE (no tick field
     exists); geometry 3/6/16/1/1.4 and cadence 100 %/5.0 s confirmed.
  5. **Blizzard adopted M — and gamora's rank-2 premise WEAKENS:** 76 phys / 137 cold per drop,
     30 %/5.0 s slow, warning window 0.833 s (no telegraph field — the falling orb IS the
     warning, lean adopted), hit test = **SPLASH 1.32 u** (fresh class adjudication: 64/64
     records carry the field, ground-targeting removes the contact event — Reading A correctly
     did NOT transfer; ratified). **Centre is FIXED at cast** (`targetingMode 'Point'`;
     `skillTargetInterval` is volley cadence, not re-aim) — so position CAN answer it by leaving
     the circle. Phase A re-derives the load-bearing ranking under the true mechanics.
  6. **Icearmor is twice the described ability:** + 35 % attack speed, TOTAL slow immunity,
     +28 % cold, cold retaliation — up 37.5 % of the fight. Its "zero lethality of its own"
     rank-3 status revises: it multiplies the boss's other channels.
  7. **Melee gains a referent:** `damagebase_physical04` at cl 18–19 composes to **43–61
     effective**, inside the envelope's independently measured 35–85 band (the operator's
     cross-check). The HELD melee channel now has an M target; whether A-DMG-1's HELD scope
     graduates is stage-2b's to propose.
  - **(COMMISSIONED):** gamora stage-2b, background — wave (widening-rectangle resolver) +
    blizzard (drop scheduler, own RNG sub-stream) + icearmor (full rider set) + F-2 in-flight
    steering + the R-WR3-23(6) telegraph-record schema fields, ALL on measured numbers, stage
    map first. Deliverable: `gamora/notes/2026-07-30-wr3-stage2b-build-report.md`.

- **R-WR3-25 (conductor rulings on the stage-2b landing, 2026-07-30) — the band is REACHABLE,
  the stage-map HALT is SUSTAINED, and F-2 is unmasked as the run's largest balance
  intervention.** Landing verified against the artifact (engine `97d51798`, collab `3b4d5cc7`;
  38 new tests; WR suites 3,907 pass; the full-`tests/` verdict owed from stage 2 now banked —
  the 82nd failing name was the W-1 guard-the-guard test firing on its own refactor (`2a33881e`
  extracted the predicate it inspected), re-pointed at the extraction site, **baseline back to
  81**; flag-OFF byte identity `a0c6b5c8f6c8795f` PROVEN vs `92381a23`). Decision-grade
  findings: (a) seed-matched ablation at leech 0 puts kit-only at **0.433** and the stage-2 arm
  at **0.567** — BOTH inside Matt's 40–60 band (R-WR3-17); (b) what LEAVES the band is F-2
  in-flight steering (0.433→0.933; intake −54 %; nova crossings −94 %) and lifesteal (H1 on the
  battery of record is a BQ-3-door reading, not a boss-difficulty reading); (c) the stage arm
  moves intake 2.3× and the win rate not at all — convergence-or-coincidence answered:
  **coincidence** at the outcome layer, which is exactly why the HALT stands at the evidence
  layer.
  - **(1) HALT SUSTAINED (the pre-registered >15 % predicate fired):** `S0_NONE` / `S1_PAK` /
    `S2_FULL` re-bases the evidence chain and re-points a Matt-signed gate's input —
    COMMITMENT BOUNDARY, HELD FOR MATT. The discriminator gamora cannot settle: **whether the
    referent's `greatestDamageReceived` 260.498 / `lastHitBy` 273.704 was a Primordian event at
    all** (if Primordian: S2_FULL — no prong over 107 — is falsified and S1_PAK's far-band
    prong 269.66 sits 3.5 % over it, consistent with dodged-far-band lower-bound logic; if
    Warden Krieg: the constraint dissolves and gamora's mechanical case for S2_FULL stands).
  - **(2) legolas COMMISSIONED (evidence, read-only, background):** settle the discriminator
    from the referent session's save/stats artifacts + prior extraction chains, so the fork
    reaches Matt DECIDABLE. Deliverable:
    `legolas/research/2026-07-30-wr3-damage-discriminator.md`.
  - **(3) F-2 SEPARATION — RULED (conductor scope per §11.2):** F-2 gets its OWN flag; the
    stage-2b arm's H1 is not attributable while kit and steering share one. Whether the
    competent policy SHIPS with perfect in-flight bearing-tracking is a POOL-1
    "replicates-a-real-player" fidelity question — HELD FOR MATT.
  - **(4) LEECH — H1 re-read RULED:** H1 on the battery of record is NOT a boss-difficulty
    number while both arms carry leech 0.05/0.08; the leech-0 ablation is the decision-grade
    H1. The BQ-3 calibration door itself — HELD FOR MATT.
  - **(5) RE-RANKING AMENDED (ratified on measurement):** wave to rank 1 on the compound-loss
    warrant (freeze → unescapable wave → 30 %/3 s outgoing-damage debuff; predicted hit rate
    0.10, measured 0.098–0.100), icearmor to rank 2 (twice-the-ability, up 37.5 % of the
    fight), blizzard DEMOTED to tempo channel. Amends R-WR3-23(1). gamora's self-corrections
    accepted (§2.1 blizzard re-aim premise, §2.2 r≈9.5 crossover) — a rank ratified on a wrong
    premise and corrected on measurement is the veto-open ledger working as designed.
  - **(6) PINS RATIFIED:** A-WAVE-1 (345.32 / 258.99 / 91.37) and A-BLIZ-1 (173.61 / 130.21 /
    45.93) join the set, per-arm, icearmor's +28 % cold included; A-NOVA-2 per-arm stands;
    A-DMG-1 fired TRUTHFULLY on the wave at S0 (279.82 > 260.5) — banked as an independent
    stage-map datum, reported-not-used, which is exactly the narrowed pin's job.
  - **(7) RANK-BINDING ERROR CLASS — third instance:** our own
    `NovaParams.tdm_additive_multiplier` was built at charLevel 13 (−78) where the boss's own
    18 gives −73 — the same shape as carried-ext's rank-4 wave/blizzard arrays. SS-S2B-4
    supersession ratified. Three instances make a NAMED CLASS; a grep-audit for
    `char_level`-crossed bindings rides the next gamora commission.
  - **(8) SMOKE DEFECTS RATIFIED flag-scoped (Discipline #11):** SS-S2B-8 (re-use timer ≠
    action-slot occupancy — the blizzard's 10 s Delay was starving the entire kit, nova
    crossings 3→0) and SS-S2B-9 (least-recently-used tiebreak among specials; the melee keeps
    strict priority). Both are arguably fixture-wide truths; graduation off-flag is Gate-2
    territory — routed to jack-ryan, not widened here. Also banked: icearmor cooldown-init
    (the R-WR3-15 `is_boss`-on-the-wrong-object shape, SECOND occurrence this run) and the
    `range_m == 0.0` dead carve-out (repaired at the packet; the dead branch stays a named
    follow-on).
  - **(9) MELEE GRADUATION — DEFERRED to stage-2c:** `BOSS_DMG_SWEEP` → (43.1, 52.0, 60.8) +
    HELD-SWEPT→M-BAND is the right shape, but it re-points gate inputs and the sweep's meaning
    depends on the arm — folds into the stage-2c calibration ratification AFTER the arm ruling.
  - **(10) PRONG COUNT — RULED:** emit `prong_count` as one more additive telegraph-record key.
    R-WR3-23(6) refused per-frame prong positions as DERIVABLE; the count is not derivable from
    a single record and the renderer needs it. Rides the F-2 flag-separation commission.
  - **(COMMISSIONED):** legolas discriminator probe (background, read-only, per (2)); gamora
    micro-commission (F-2 own flag + `prong_count` emission + the binding-class grep-audit,
    flag-OFF byte identity must hold) — orthogonal plumbing the HALT does not block, and
    prerequisite to ANY attributable battery after the arm ruling. Stage-2c calibration and the
    owner-eye render QUEUED behind the arm + leech + F-2 rulings.

- **R-WR3-26 (discriminator lands, 2026-07-30) — the fork's premise FALLS, the ceiling sweep
  stands: S1_PAK favoured, S2_FULL disfavoured-not-falsified; the arm fork goes to Matt
  DECIDABLE.** Landing verified against the artifact
  (`legolas/research/2026-07-30-wr3-damage-discriminator.md`, commit `21b18db7`; ten read-only
  harnesses in scratch; no canonical docs touched; no web sources — corpus + save + `Game.dll`
  symbol table only).
  - **(1) V1 BANKED:** `lastHitBy` 273.704 is **NOT-PRIMORDIAN, firm** — the save stores the
    entity (`lastMonsterHitBy` = Plague Walker, a trash zombie; save written mid-trash-pack).
    AND it is **not a single impact**: Plague Walker's entire instantaneous kit is 68–85 raw
    physical, failing the single-impact reading 8–16× under EVERY regime → the field
    AGGREGATES. **Envelope U-5 closed, by the negative.**
  - **(2) V2 BANKED:** `greatestDamageReceived` 260.498 is **lifetime-of-character** (7,096 s,
    882 kills, 500 hits received), carries no attribution field, and is structurally
    unresolvable from a single save.
  - **(3) CONDUCTOR ERROR BANKED — the commission's premise was FALSIFIED:** I wrote "if not
    Primordian, the constraint dissolves and S2_FULL stands unopposed." Wrong: the outgoing
    damper is ROSTER-WIDE (93.4 % of 1,307 Monster records, trash tier included at
    `−56 + rank`) — re-attribution relocates the constraint into another damped bucket. The
    envelope note had only ever read trash records' *life* modifier, never their *offensive*
    one. Legolas's single most important line, and the finding that reshapes the fork.
  - **(4) THE DECISION SUBSTRATE is the ceiling sweep, not the datum:** best-case
    post-mitigation single-event ceilings over the full reachable roster — **S0 894.6 / S1
    670.9 / S2 252.9** (deliberately generous to S2: fabricated +80 weapon, 8 %-proc granted
    everywhere, implausible cl-21 spawns admitted; excluding those → 240.3) vs the measured
    260.498 / 273.704. **S2 short by 2.9–7.6 % from ANY source the character could have met.**
    Regime arithmetic over the corpus, independent of save-field semantics.
  - **(5) CROSS-ARTIFACT CORRECTIONS ABSORBED:** stage-2b's "S2 entire-kit ceiling ~283.14"
    does NOT reproduce — Primordian's S2 kit ceiling is **94.4** (frigidring far band), and if
    283 summed simultaneous events it is not comparable to a per-event maximum; the "~107
    worst prong" was the 100 %-band figure — the FAR band governs. Routed to gamora at next
    landing.
  - **(6) LIVE THREATS NAMED, NOT CLOSED:** U-1 — the two field labels are community
    convention, not engine truth (`Game.dll` has no such symbols), and the invariant
    `greatest ≥ last` is VIOLATED as labelled; under the swap reading, 260.498 becomes the
    Plague-Walker-attributed number — a direct NOT-PRIMORDIAN on the headline datum. U-2 —
    if `greatestDamageReceived` aggregates like its neighbour, it constrains nothing. U-3 —
    trap damage may bypass the monster damper (`trap_floorspikes` 449 raw pierce vs zero
    player pierce resist; regime-neutral if so). **Cheapest closure for U-1+U-2: a second
    `.gdc` diffed — filed as matt_to_do T11.**
  - **(7) CONDUCTOR LEAN (veto-open; the RULING stays HELD FOR MATT per R-WR3-25(1)):**
    **S1_PAK**, resting on the ceiling sweep; S2_FULL disfavoured, NOT falsified (2.9 % is
    not a landslide); S0_NONE remains the regime of record until Matt rules.
  - **(8) INDEPENDENT CONFIRMATION BANKED:** legolas reproduced the 269.66 far-band figure to
    the decimal from record payloads + measured gear (armor 337 → 70 % physical absorb, cold
    resist 14) — validating the mitigation model, the rank-5 payload, and that all these are
    post-mitigation comparisons. Side datum: Warden Krieg ph.2 was never killed by this
    character (`greatestMonsterKilled` = Primordian at 15,822).
  - **(9) GATE-2 ROUTING:** envelope U-5 closure + envelope §2 correction (the missed
    trash-tier offensive modifier) → jack-ryan on ratification.

- **R-WR3-27 (F-2 flag-split micro-commission lands, 2026-07-30) — the switch exists, the
  count is emitted, the binding class is a PATTERN — and stage-2b's F-2 attribution was an
  UPPER BOUND.** Landing verified (engine `127ba505`, collab `26922ead`; 18 new tests; WR
  suites 4,000/0; MIGRATION §1a/§3a/§6a; byte-identity proven over 30 fights **including 6
  stage-2b-ARMED** — mech `6e20f784…` / trace `14b08bfa…` identical, sole delta the additive
  keys).
  - **(1) FLAG DESIGN RATIFIED:** `wr3_f2_inflight_v1` tri-state with load-bearing `None` =
    inherit `wr3_stage2b_v1` — every pre-existing call site reproduces WITHOUT edits (a plain
    bool would fail silently on one missed caller). 2×2 smoke-verified non-vacuous (72/72/0
    steering with kit; 0/139/0 without). Default UNTOUCHED — the F-2 ruling stays Matt's.
  - **(2) `prong_count` RATIFIED**, additive, v1 stays v1. Trap banked for the renderer:
    the existing `n_realized` counter reads **1.000 at every radius against a launched 16** —
    a renderer reaching for the wrong field draws ONE prong. Rides the schema handoff to drax.
  - **(3) ⚑ ARM-B CONFOUND — R-WR3-25's headline AMENDED:** stage-2b's ablation built arm B by
    disarming the ENGINE flag with packets still armed, which disarmed **F-2 and the icearmor
    tick together**. So "kit-only 0.433" was *kit minus F-2 minus icearmor*, and **the +0.500
    attributed to F-2 is an UPPER BOUND**. Gamora declined to present the 6-seed smoke as a
    rate — correct. **AUTHORIZED (conductor scope — measurement serving the HELD Fork 3, not
    calibration; HALT untouched):** 30-seed seed-matched re-run of the clean arms
    (`_s2bv1_f2off`, `_f2on`), leech 0 + leech default, same seeds as stage-2b §5; PLUS the
    R-WR3-26(5) cross-artifact reconciliation owed (the ~283.14 S2 kit ceiling that does not
    reproduce vs legolas's 94.4; the ~107 prong that was the 100 %-band figure).
  - **(4) §1.4 `--help` REPAIR RATIFIED as in-commission:** the deliverable IS a switch, and an
    undiscoverable switch is not delivered; `%`→`%%`, pre-existence proven at `97d51798`, live
    since WR2-B, now pinned by a test. Meta-finding banked: the harness had never once been
    driven by its own help — pinned-flag scripts only.
  - **(5) THE BINDING CLASS IS A PATTERN — five instances, two seams, three ours.** Gamora's
    standing-check proposal ("any `charLevel`-keyed operand names its owning entity at the
    composition site") ROUTED to jack-ryan as an engineering-discipline candidate. Instance 4
    (gd_nova derives boss level 16, gd_boss_kit says 18; inert only via the UNDECLARED
    rank-5 invariance over 16..19): repair AUTHORIZED to ride the (3) commission — declare the
    invariance, unify on the named constant, byte-identity proof required. Instance 5
    (`OppositionRow.char_level = 13` emitted as the boss's into every artifact): **HELD to
    stage-2c** — artifact-visible, and R-WR3-24 deliberately kept it; gamora's §6.6 honesty
    accepted (his stated justification was wrong; the banked-artifact argument survives).
  - **(6) GATE SEMANTICS BANKED:** `G-F2` grades steering > 0 and reads FAIL on an `_f2off`
    run BY DESIGN — label such runs so the FAIL is read as the mechanism working.
  - **(7) HONESTY RATIFIED on the pre-registered digest:** `a0c6b5c8…` was not reproduced
    (instrument unrecoverable); the substitute stash-and-rerun digest pair is the operative
    proof and the math note says so rather than substituting quietly. Full `tests/` sweep was
    in flight at commit — verdict OWED at next landing.

- **R-WR3-28 (Matt-signed, 2026-07-30) — THE THREE FORKS RULED: S1_PAK provisional with routes
  open · leech is the RING's 5 %, not a dial · F-2 capped.**
  - **(1) FORK 1 — Matt verbatim: "we will continue with S1_PAK for now, but leave the option
    of either route later as open."** `S1_PAK` is the REGIME OF RECORD, PROVISIONAL. All
    per-arm pins re-base to their S1 columns (A-NOVA-2 269.66/305.97 · A-WAVE-1 258.99 ·
    A-BLIZ-1 130.21); stage-2c calibrates under S1. **The three-arm stage map is retained
    LIVE, not collapsed** — S0/S2 stay built and switchable; the arm object IS the
    open-route mechanism Matt asked for. The R-WR3-24/25 HALT is RESOLVED by this ruling.
  - **(2) FORK 2 — Matt: "I had a leech ring, remember?… ok with removing or quite low."
    CONDUCTOR ELICITATION FAILURE BANKED FIRST:** I presented as a Matt-question what was a
    substrate lookup — the referent gear was never lost; the G-7 save parse carries all 12
    pieces with affix records. Extracted this turn: **exactly ONE leech source in the whole
    kit — equipment slot 6, "Vampiric Silver Band," prefix `ao008a_lifeleech_01.dbr`,
    `offensiveLifeLeechMin = 5.0` (5 % of ATTACK damage converted to health); full 12-piece
    sweep found no other leech field anywhere.** RULING under R-WR3-2 referent-parity: the
    battery of record carries **leech 0.05 scoped to attack damage per GD ADCtH semantics**
    (scope-mapping into our sim's leech channel = a named stage-2c gamora task — if our leech
    applies to ALL damage dealt it overstates the ring); **the 0.08 value has NO gear warrant
    and is RETIRED**. Matt's remove-or-low latitude noted; parity governs: the ring is real,
    it stays, at its measured value and measured scope.
  - **(3) FORK 3 — Matt: "agreed on (c)."** F-2 in-flight steering is CAPPED-IMPERFECT: the
    shape is ruled; the cap's numbers (reaction latency + miss rate, tuned so telegraph-escape
    rates match referent behavior) are stage-2c calibration, informed by the clean ablation
    in flight.
  - **(4) SEQUENCED:** stage-2c calibration lap fires when the clean ablation lands —
    S1_PAK regime + ring-scoped leech 0.05 + F-2 cap tuning + melee graduation
    (R-WR3-25(9)) + instance-5 char_level repair (R-WR3-27(5)) + battery of record →
    owner-eye render.

- **R-WR3-29 (Matt's difficulty hypothesis lands, 2026-07-30) — CONFIRMED where asked, and the
  unasked half INVERTS Fork 1's basis: the referent save reads VETERAN.** Landing verified
  (`legolas/research/2026-07-30-wr3-damper-difficulty-probe.md`, commit `886d81d1`; M/C grades
  carried throughout; parse alignment corroborated by money/texture decode AND third-party
  parser field order; slot-index scheme validated against the wiki-corroborated asymmetric
  resist penalty).
  - **(1) HYPOTHESIS CONFIRMED (the asked half):** the pak −25 % is literally a difficulty-table
    cell — `balancingadjustment_mp+difficulty_enemies01.dbr`, 12-slot array (3 difficulties ×
    4 player counts), `offensiveTotalDamageModifier = [−25 Normal, +25 Elite, +40 Ultimate]`.
    The pool stage is NOT difficulty-keyed — it is a **level-normalising ramp** (−91+rank,
    crossing ZERO at monster level 88): early-game forgiveness that fully releases by cap. No
    other difficulty-keyed damage multiplier exists in `gameengine.dbr`; the chain is closed.
  - **(2) THE UNASKED FINDING (grade C, high confidence):** the referent save's difficulty byte
    is **128 = Normal with bit 7 set = the VETERAN mutator** (third-party saves read plain 0
    and 2; `GetGamePlusChallengeDifficulty` packs game+challenge into one int; no other
    candidate flag). Veteran: monster damage +40 %, life +140 %.
  - **(3) WHAT IT DOES TO THE ARMS:** S2_FULL + Veteran ceiling 354.1–541.9 — **both measured
    numbers REACHABLE under either mutator-composition reading**; the 2.9 % shortfall that was
    S1_PAK's sole mechanical basis does not survive; and S1's signature 269.66-to-the-decimal
    fit BREAKS under Veteran (377.5 = 38 % overshoot). Q4 answered flatly: ×0.75 is not the
    Normal composition of anything (composite reaches 0.75 only at monster level 75);
    **×0.2625 IS the Normal composition, now with a design rationale** (ramp × difficulty
    cell, unwinding monotonically to ×2.09 at Ultimate/100).
  - **(4) CONDUCT — R-WR3-28(1) is Matt-signed; the inversion is HELD FOR MATT, not enacted.**
    S1_PAK REMAINS the regime of record until Matt re-rules — the routes-open clause doing
    exactly its job. Two evidence asks put to Matt: (a) MEMORY — was Veteran toggled at
    character creation?; (b) U-2, the cheapest decisive test in the run — one ~2-minute save
    known-by-provenance to be Veteran-on, read the byte. **T11 UPDATED** to fold this in (the
    same pull closes the field-semantics questions).
  - **(5) CASCADE NAMED, not resolved:** the HP anchor is DEGENERATE — "cl 18 plain" and
    "cl 13 Veteran" predict Primordian's 15,822 within 0.4 % of each other, and the save's own
    `greatestMonsterKilledLevel = 13` (U-4 semantics open). If cl-13-Veteran confirms, skill
    rank re-derives 5 → 4 and R-WR3-24(1)'s carried-ext falsification PARTIALLY RE-OPENS (the
    rank-4 arrays were right under that reading); the payload pin set would re-base. Queued
    behind U-2; also noted: Veteran is mid-playthrough-toggleable, so per-field mutator states
    need not agree.
  - **(6) CONDUCTOR LEAN, regardless of which regime Matt re-rules:** adopt the
    **difficulty-parameterised OPERATOR, not a scalar** — `outgoing = base ×
    (1 + Σpool(charLevel)/100) × (1 + pak[difficulty]/100) × mutators` — and NEVER port
    ×0.2625 into engine work as "GD's damper": it is one cell. **The transferable design fact
    is the SHAPE** — per-level damage normalisation that releases by cap, crossed with a small
    difficulty layer — and it is a mechanism our own difficulty system wants. The three-arm
    stage map graduates from evidence-hedge to design object.
  - **(7) SEQUENCING:** stage-2c now waits on BOTH the clean ablation (in flight) and Matt's
    Fork-1 re-ruling; calibrating under an arm whose basis just inverted would burn the lap.

- **R-WR3-30 (Matt corroboration + Veteran characterization commissioned, 2026-07-30) — Matt
  verbatim: "I looked it up, and Veteran setting is an optional modifier for normal mode which
  increases monster stats, density, hero spawns, and grants +10% experience. I must have been
  playing on veteran. Can you research this?"**
  - **(1) EVIDENCE UPGRADED:** player testimony (independent lookup matching GD's Veteran
    exactly, plus self-attribution) now corroborates the byte-128 read. R-WR3-29(2)'s grade-C
    call is effectively confirmed for conduct purposes; the T11 provenance save remains the
    formal M-grade closure and stays open (it also closes U-4 boss-level and the field
    semantics).
  - **(2) REFERENT REDEFINED (consequence):** the referent world is **Normal + Veteran** —
    which touches not just the damage stage but potentially DENSITY and HERO-SPAWN rates,
    i.e. R-WR3-2's "majority of encounters" mix, not only the boss fight. A Veteran-blind
    encounter mix under-prices the trash the referent player actually fought.
  - **(3) COMMISSIONED — legolas Mode A, full Veteran characterization (background):**
    (a) complete corpus enumeration of the Veteran mutator's effects (every nonzero field,
    stats/life/damage/XP/density/champion-hero spawn mechanics, where each lives);
    (b) U-3 composition adjudication attempt (own ×1.40 stage vs pooled ×2.14);
    (c) the four-cell Primordian payload grid — {cl 13 rank 4, cl 18 rank 5} × {both
    composition readings} under S2_FULL + Veteran — so stage-2c commissions the moment Matt
    re-rules Fork 1, with pin re-basing pre-computed;
    (d) what Veteran density/hero spawns imply for the encounter-mix fixture and the
    R-WR3-2 majority measurement. Deliverable:
    `legolas/research/2026-07-30-wr3-veteran-characterization.md`.
  - **(4) FORK-1 RE-RULING still open at Matt's hand** — the characterization lands first so
    the re-ruling arrives with the full price tag, not just the damage multiplier.

- **R-WR3-31 (clean ablation lands, 2026-07-30) — ΔF2 = +0.467 measured clean, the banked
  "kit-only" arm was PERMANENT icearmor, and the fourth BQ-3 door caught its own author.**
  Landing verified (PREDICATE R PASS — banked arms reproduce to the last digit; 30 seeds
  seed-matched; decomposition telescopes exactly: Δkit −0.133 · Δicearmor(permanent→cycling)
  +0.033 · **ΔF2 +0.467** · interaction +0.100).
  - **(1) CHARTER CORRECTION (gamora §8.1):** R-WR3-27(3) recorded the confound as "disarmed
    F-2 and the icearmor tick together"; MEASURED, disarming the engine flag made icearmor
    **PERMANENT** (tick_calls = 0, buff up 95.0 % of reads vs clean 33.2 %). Every R-WR3-25/27
    sentence reading arm B as "kit only" carries this correction. **The headline SURVIVES on
    better ground:** the shippable clean arm (kit + cycling icearmor, F-2 OFF) reads **0.467
    at leech 0 — IN BAND, nearer centre** than the unshippable 0.433.
  - **(2) R-WR3-25(5) AMENDED — icearmor's rank-2 promotion is UNMEASURED, was believed
    measured:** no arm removes the packet-driven cast; the only contrast available is
    permanent-vs-cycling (+0.033). Not challenged — unmeasured. **AUTHORIZED: packet-level
    icearmor kill-switch, riding the stage-2c build** (with it, icearmor-alone and the true
    Δkit both become measurable). Stage-2b's Δkit likewise re-labelled.
  - **(3) 283.14 STRUCK from the charter (gamora: "legolas is right"):** it was
    `nova_delivered(9.5, count=3)` — three simultaneous far-band crossings where
    `n_bounds = (0,1)`; not a per-event maximum. **The charter carries 95.36** (rider-inclusive
    far-band single prong; legolas's 94.4 is the same number rider-free). Legolas's diagnosis
    of the "~107" was wrong (it is the `resists_low`-leg far band, not the 100 %-band) but his
    conclusion stands. NOTE: gamora's "this strengthens the S1_PAK lean, against the arm I
    argued for" was written blind to R-WR3-29/30 — the S-arm question now runs through
    VETERAN, where S2+Veteran is favoured; the number correction banks either way.
  - **(4) F-3 CALIBRATION INPUT BANKED:** F-2's true effect is +0.467 (the cap target prices
    against this, not +0.500). Under Matt's ruled ring-leech 0.05 the clean arm reads 0.733 —
    ABOVE band — which makes the R-WR3-28(2) leech SCOPE-MAPPING (attack-only per the ring vs
    all-damage in the sim) load-bearing for stage-2c, exactly as named.
  - **(5) INSTANCE-4 LANDED byte-inert** (stash-and-rerun incl. armed fights, digests
    identical); instance 5 still HELD, now resting on the banked-artifact argument ALONE
    (its stated justification corrected in source).
  - **(6) SECOND NAMED CLASS — state-object degeneracy, three occurrences this run:**
    `is_boss`-on-wrong-object (R-WR3-15), icearmor cooldown-init, and now the tick/cast split.
    Two made mechanisms measuring NOTHING; one made a mechanism measuring EVERYTHING, forever
    — the dangerous variant, because its counters all look plausible. Routed with the
    residual-key discipline question to jack-ryan.
  - **(7) RESIDUAL-KEY WIDENING AUTHORIZED to ride stage-2c** (eight counters absent-not-zero
    on flag-OFF arms; one `if`, schema-visible so gamora rightly did not land it unruled). The
    discipline companion — "any conditionally-emitted counter block declares its own absence"
    — routes to jack-ryan alongside R-WR3-27(5)'s charLevel standing check.
  - **(8) THE FOURTH BQ-3 DOOR:** gamora's own byte-identity harness opened the door
    undeclared at `127ba505` — his labelled expectation ("sweep should be unmoved at 81") was
    wrong, the full-regression name-diff caught it, three declared allow-list entries fixed
    it, confirming sweep **81 exact, name-diff 0/0**. All four occurrences of this class were
    measurement drivers; three of four were caught only by the full sweep. **R-WR3-27(7)'s
    standing full-sweep requirement is hereby RATIFIED as run law: a labelled expectation is
    not a substitute for the sweep.**

- **R-WR3-32 (Veteran characterization lands, 2026-07-30) — Matt's lookup corroborated
  field-by-field, and THE DEGENERACY reorders the run's unknowns: U-3 gates stage-2c, U-4
  does not.** Landing verified (`legolas/research/2026-07-30-wr3-veteran-characterization.md`,
  659 lines, commit `8fe88a07`; §0 verdict, §4.4 degeneracy, §4.5–4.6 grid + pins, §5 mix,
  §6 corrections read against the ledger).
  - **(1) Q1 CLOSED (M):** R-WR3-30's commission answered at the record. Veteran =
    `records/game/balancingadjustment_challengemode_enemies01.dbr` (`Class=GameAdjustment`,
    a THIRD class distinct from AttributePak and Mutator), reached
    `gameengine.dbr → challengeAdjustment`, template-described **"GameAdjustment for
    Normal"** — the corpus itself calls Veteran a Normal-mode overlay. **14 nonzero fields,
    complete:** dmg +40 total/+10 phys · life +140 (×2.40) · OA +25/+5 % · DA +15/+5 % ·
    speeds +5 % · str +5 % · retaliation +15 (negligible: composes with pak −66 to ≈3.4–7.4)
    · **`spawnMaxAdj +1` · `spawnChampionMaxAdj +2`**. XP +10 % is a literal `*1.1` in
    `experienceformulas.dbr`. Every channel of Matt's lookup confirmed. **Deliberate
    asymmetry banked:** `spawnMinAdj`/`spawnChampionMinAdj` ABSENT — **Veteran raises pack
    ceilings, not floors** (widens the right tail without moving the smallest pack).
  - **(2) U-3 OPEN and now THE gate — own-stage ×1.40 lean (grade C) sustained on better
    ground:** `GameEngine::GetChallengeAdjustment()` has NO exported consumer (application
    site inlined), so composition is unproven from binary. The difficulty probe's
    `ContributeMutator*` citation is SUPERSEDED (§6.3 — those symbols are Crucible/SR
    mutators, not Veteran); the lean now rests on the structural argument plus a soft
    play-consistency read: **own-stage cells land ON CAL-1's 10–15 % norm; pooled cells run
    2.2× over with the worst hit at 98 % of the 759 pool** — pricing a fight the save says
    was won comfortably at level 13 with 2 deaths in 7,096 s.
  - **(3) THE DEGENERACY (headline):** cl-13/rank-4 + Veteran-own-stage vs the charter's
    existing cl-18/rank-5 no-Veteran column = **mean ratio 0.951, spread 0.909–0.971,
    dispersion ≤4.4 % across all eight channels** — the SAME FIXTURE within 5 %. The
    rank-step (≈0.79×) and the `armorbase05` level-step (≈0.86×) near-cancel Veteran's
    ×1.40; the probe's 0.4 % HP coincidence is a property of the whole kit. **SEQUENCING
    AMENDED (inverts R-WR3-29(5)):** if U-3 = own-stage, closing U-4 is worth ≤5 % and the
    feared rank-5→4 pin re-basing DOES NOT MOVE the fixture; if pooled, every cell is
    1.58–2.19× and pins re-base. **U-3 gates; U-4 does not; both close on the same T11 pull**
    (T11 amended to carry U-3 as its decisive item).
  - **(4) FOUR-CELL PIN TABLE BANKED** (artifact §4.6, post-mitigation rider-ON, ratified
    units): a Fork-1 re-ruling to S2_FULL+Veteran **halves the pins under own-stage (×0.50)
    and cuts ~23 % under pooled (×0.77)** vs the S1_PAK values in force. No cell reproduces
    S1_PAK (30–200 % apart everywhere) — **the arm ruling is genuinely load-bearing.**
  - **(5) U-4 ADVANCED, one branch dead, a third surfaced:** `greatestMonsterKilledLevel`
    is **engine-truth** (`PlayStats::{Get,Set}GreatestMonsterKilledLevel` + co-named
    monster-side triple) — the "player level at kill" reading is **DEAD**. New branch:
    proxy-SPAWN-level = 13 ⇒ **cl 16 / rank 5**, more plausible on world-level grounds
    (aPL 10–11 clearing Act-1 Wightmire) and reconciling `gd_nova`'s charLevel-16 derivation
    (R-WR3-27(5) instance 4). Three readings priced; degeneracy caps the stakes at ≤5 %
    under own-stage. ALSO banked: `play_stats.maxLevel = 12` vs `character_bio.level = 13`
    — a lagging high-water mark; **any argument leaning on play_stats currency at save time
    is on notice.**
  - **(6) ENCOUNTER MIX — measured answer was in the save all along:** `championKills 7` ·
    `heroKills 3` / 882 kills = **1.13 % elite (M)**, the R-WR3-2 mix, measured and
    Veteran-inclusive. **PRESCRIPTION RATIFIED:** pin ABSOLUTES to the save; use modelled
    uplift ratios (+73 % champ / +56 % hero / +16 % bodies) for counterfactuals ONLY; price
    the pack-size RIGHT TAIL (ceilings-not-floors); acceptance denominator ≈141–164
    pack-equivalents. **U-V1 registered:** champion model over-predicts 10× (hero rate
    matches — soft corroboration of the Veteran read); not laundered, causes named.
  - **(7) CORRECTIONS ROUTED TO JACK-RYAN (Gate-2 packet filed):** (a) **R-WR3-26(6) U-1's
    premise FALSIFIED** — `greatestDamageReceived`/`greatestDamageInflicted` ARE literal
    `Game.dll` strings (engine-truth labels); swap hypothesis stays dead (`lastHitBy`
    unattested) but the ledger's stated basis was wrong; (b) **melee-band unit mismatch** —
    charter's 43.1–60.8 is PRE-mitigation (post-mit equivalent 17.13–27.90 at cl 18 no-Vet)
    vs post-mitigation pins; `BOSS_DMG_SWEEP` (R-WR3-25(9), deferred) would compare against
    pins in different units — routes WITH the melee graduation.
  - **(8) NEW UNKNOWNS REGISTERED:** U-V1 (championChance semantics) · U-V2 (Adj add vs
    clamp; lean add) · U-V3 (Ascendant = Veteran-on-Ultimate; not needed) · **U-V4 (monster
    base life/OA/DA NOT in the `.arz`** — envelope HP figures are back-solved, not
    forward-computed; why the HP-anchor route to U-4 cannot close from corpus, and why the
    OA/DA/speed/str Veteran terms are unpriceable pre-fixture).
  - **(9) FORK-1 RE-RULING PACKAGE — HELD FOR MATT (commitment boundary):** conductor lean =
    difficulty-parameterised operator with **S2_FULL × Veteran own-stage** (the cell within
    5 % of the fixture already in force). T11 (~5 min) closes U-3 + U-4 + field semantics
    and is the run's critical path. Stage-2c waits on the re-ruling.

- **R-WR3-33 (MATT-SIGNED 2026-07-30 — Fork-1 RE-RULED, plan (a): S2_FULL × Veteran
  own-stage; stage-2c COMMISSIONED).** Matt verbatim: *"go ahead with plan (a). We will
  later check T11 and confirm/deny."*
  - **(1) REGIME OF RECORD:** `S2_FULL × Veteran own-stage (×1.40)` via the
    difficulty-parameterised operator (R-WR3-29 lean, now ruled):
    `outgoing = base × (1 + Σpool(charLevel)/100) × (1 + pak[difficulty]/100) × (1 + veteran/100)`
    with veteran applied at its OWN stage. **Supersedes R-WR3-28(1)'s provisional S1_PAK.**
    The three-arm stage map is RETAINED as flags (R-WR3-28's routes-open clause carries
    forward); a T11 "pooled" result is a PARAMETER flip, not a rebuild — gamora builds it so.
  - **(2) THE ≤5 % CAVEAT IS THE RULING'S WHOLE RISK:** boss cell of record = **cl 13 /
    rank 4 + Veteran own-stage**, which by the degeneracy (R-WR3-32(3)) is within 5 % of
    the existing cl-18/rank-5 no-Veteran fixture — so the existing fixture STANDS as the
    approximation and pins re-base per the characterization §4.6 (A-NOVA-2 far 113.78 /
    mid 81.27 · A-WAVE-1 85.12 · A-BLIZ-1 44.28, rider-ON post-mitigation units).
  - **(3) CONFIRM/DENY PROTOCOL (Matt's clause):** T11 remains queued. **Confirm**
    (own-stage) → caveat dissolves, pins stand. **Deny** (pooled) → cells re-base ×1.58–2.19
    vs the no-Vet column; battery re-fires under flipped parameter; gates re-register.
    Either way the stage-2c BUILD survives untouched — only calibration constants move.
  - **(4) STAGE-2c COMMISSIONED (gamora, background, commit-never-push).** Scope, all
    previously authorized items now firing together: (i) arm-of-record wiring per (1);
    (ii) ring-scoped leech 0.05 with the ATTACK-ONLY scope-mapping task (R-WR3-28(2) /
    R-WR3-31(4) — load-bearing: clean arm reads 0.733 at all-damage 0.05); (iii) F-2
    capped-imperfect tuning, cap priced against ΔF2 = +0.467 (R-WR3-28(3), R-WR3-31(4));
    (iv) melee graduation `BOSS_DMG_SWEEP (43.1, 52.0, 60.8)` WITH the pre/post-mitigation
    unit fix (R-WR3-32(7b)); (v) icearmor packet-level kill-switch (R-WR3-31(2)) + the
    icearmor-alone and true-Δkit measurements it unlocks; (vi) residual-key widening
    (R-WR3-31(7)); (vii) instance-5 repair — `OppositionRow.char_level` binding declared
    at call site (R-WR3-27(5), HELD → now authorized within this build); (viii) gates
    RE-REGISTER under stage-2c params, then the **30-seed battery of record** fires
    (discharges R-WR3-15's chartered debt); full-regression name-diff sweep MANDATORY per
    run law R-WR3-31(8). Target: boss win rate **40–60 %** (R-WR3-17). HALT-and-route on
    any degenerate regime or unruled decision.
  - **(5) SEQUENCE TO STAGE-2 COMPLETION:** 2c build + battery → Gate-2 (jack-ryan, joins
    the consolidated packet) → owner-eye render (drax baton) → Matt watches → stage 2
    CLOSES. W-2 encounter-AI lap remains chartered between stage-2 close and the R-WR3-2
    full-mix acceptance measurement.

- **R-WR3-34 (conductor, veto-open, 2026-07-30) — godot-session trace findings land on the
  in-flight 2c commission: STOP + RELAUNCH with three scope additions.** Source: drax-seam
  playback-consumer read of the WR3 trace, relayed by Matt. The commission was minutes old;
  a corrupted battery of record would cost far more than the relaunch.
  - **(1) ICEARMOR IS STRUCTURALLY INVISIBLE TO EMISSION — FOURTH occurrence of the
    state-object degeneracy class (R-WR3-31(6)):** its state is a plain Python attribute
    (`mob._wr3_icearmor`), not in `active_effects` — the only surface the emitter's ailment
    path reads. A 25 % absorb + 28 % outgoing-cold buff runs with NO emission channel. The
    class's new variant: state visible to its author only. **2c scope item (ix): route
    icearmor state through `active_effects` (or a declared `buffs:[]` block) BEFORE any
    baton emits** — rides the icearmor kill-switch item, same code region. Without it every
    baton needs re-emitting regardless of what else is right. Class count 4 → the Gate-2
    packet's item B.6 gains this instance.
  - **(2) BLIZZARD MASQUERADES AS THE NOVA — MEASUREMENT-INTEGRITY THREAT, the reason for
    the stop:** `chillbane_blizzard` telegraphs `shape:"circle"`; an unqualified circle-test
    scores it into `_nova_verdicts`, silently corrupting the escape-rate statistic the run
    is graded on. **2c scope item (x): add a `family` discriminator string to telegraph
    events (`nova|blizzard|wave|melee`)** — additive key, prong_count precedent
    (R-WR3-25(10)) — AND, BLOCKING before the battery of record: **audit whether the
    ENGINE-side verdict/escape-rate scorer keys on unqualified circle-shape.** If yes, every
    stage-2b escape figure taken since blizzard entered is suspect and the fix precedes the
    battery; if the defect is playback-only, the family key still lands for the baton.
  - **(3) 2c scope item (xi): `attack_id` join key on damage/dot events** (today the nova's
    own hit carries `skill_idx:-1` — a hit cannot be joined to its telegraph). Cheapest of
    the three; unlocks impact-flavor rendering downstream.
  - **(4) FIDELITY BANKED (the good news is evidence, not just cheer):** telegraph geometry
    CARRIES — 19 fields; the real nova reads circle / radius 12.0 m / windup 2.32 s /
    damage 218; TELL-DRESS can draw the honest death-2 ring from the trace AS IT STANDS.
    And the CC arrives as `action_lock`, not `freeze` — the Gate-2 ruling (model the GD
    mechanic, don't reuse RDR freeze-shatter) is honored in the schema itself.
  - **(5) CONDUCT:** in-flight commission STOPPED (stop+relaunch pattern; no landings had
    committed) and RELAUNCHED with scope (i)–(xi). Schema additions are additive keys —
    MIGRATION note owed with the report (star-lord emission seam + drax consumer downstream).

## §3 — The envelope diff (what stage 2 calibrates, pending grill)

| metric | GD L13 referent | our fixture | verdict |
|---|---|---|---|
| boss:player HP | 22.8× (vs 1600 pool) · Warden ph.1 15,569 | 19.5× · clear 16,235 | **IN BAND** (~15%) |
| boss fight duration | 59–118 s | ~65 s | **IN BAND** |
| player DPS | 310–620 HP/s (width = open cadence U-2) | ~250 HP/s | **BELOW BAND** — F-WR2-1's number |
| boss heavy hit ÷ pool | worst MEASURED hit taken all run: 34.3% · scripted heavy 10.4% | nova up to 55% (2×414.80/759) | **1.6–3.4× OVER** — the outlier |
| player:boss speed | ~~0.99/0.81 (boss FASTER)~~ **CORRECTED R-WR3-19: that ratio was WARDEN KRIEG. vs Primordian (the fixture's boss): player 1.29–1.33× FASTER** | 1.43× player-faster | **IN BAND, 7–11 % over** |
| commit/telegraph rhythm | commit windows + telegraphed heavies = the kite | none (76,714/76,714 idle) | **THE MISSING MECHANISM** |

## §4 — Run shape (two stages; stage boundary is a Matt checkpoint)

- **STAGE 1 (mechanism build; F1–F4 all YES):** Mechanism K (player evade/kite intent — trigger
  rules grill-open below) + Mechanism C2 (boss attack-commit wind-ups — durations grill-open).
  Full battery vs frozen baseline. Pre-registered gates incl.: separation distribution UNPINS
  from the 2.000 m floor; ≥1 conceded kite window per boss fight beyond the opening charge;
  production telegraph-escape rate > 0 (F-WR2-4's regime finally sampled); no S-1/S-2 regression.
  **Every pre-registered column NAMES its computing cell** (the §8.38 lesson, now law here).
- **OWNER-EYE CHECKPOINT (desirable-pattern §6.2):** Matt watches a stage-1 render BEFORE
  calibration — geometry verbs first, then numbers.
- **STAGE 2 (envelope calibration; Matt commitment-boundary):** calibrate the out-of-band rows
  (player DPS ↑ toward band; nova pool-fraction ↓ toward the ≤34.3% measured worst) under pinned
  decision rules elicited at the stage boundary. **Acceptance gate: R-WR3-2 majority win rate
  under the competent policy — measured separately on boss encounters and the full encounter
  mix** (Matt's "majority of encounters" includes the trash the player shreds).

## §5 — Grill forks (ALL RESOLVED 2026-07-30 — kept verbatim as the decision record)

> K-1, C2-1, CAL-1: leans RATIFIED as decision rules (R-WR3-7). POOL-1: ruled BOTH (R-WR3-8) —
> Matt's intent sentence: the player-kit AI replicates the choices a real player would make,
> including the form choice.

- **K-1 evade trigger:** does the kite intent fire on (a) telegraph events only, or (b) telegraph
  + a health/pressure heuristic (sustained-contact timer)? Lean: (b) — the referent play kited
  rhythmically, not only on telegraphs.
- **C2-1 commit texture:** flat wind-up stops only, or wind-up + recovery (GD-style animation
  lock both sides of the swing)? Lean: wind-up + short recovery — the recovery is where the
  referent's kite windows lived.
- **CAL-1 nova target:** calibrate the nova's pool-fraction to the measured worst-hit (≤34.3%)
  or to the scripted-heavy norm (~10–15%) with the 2× quantum kept as the punishment case? Lean:
  scripted-heavy norm per projectile with 2× reaching ~ the measured worst — punishment stays
  possible, one-shot pressure stops.
- **POOL-1:** which pool does R-WR3-2 mean — human 759 or played-form 1600? (R-WR3-4: the 1600
  is not the werewolf's; the referent experience was mostly played at which pool?) This halves or
  doubles every fraction in §3.

## §6 — Matt interface

Declared: grill answers to §5 (or "defaults stand" — the leans fire as decision rules); the
stage-boundary checkpoint watch; stage-2 calibration ratification; final watch = exit predicate.
Red-flag pings mid-run only. All conductor rulings veto-open in this ledger, one word reverts.

*Charter v1 — grill closed; mechanism-spec freeze pends the gamora form-swap feasibility read
(R-WR3-8(c)) and the legolas policy-package survey (R-WR3-9). — gandalf, RUN-CONDUCTOR*
