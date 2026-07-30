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

## §3 — The envelope diff (what stage 2 calibrates, pending grill)

| metric | GD L13 referent | our fixture | verdict |
|---|---|---|---|
| boss:player HP | 22.8× (vs 1600 pool) · Warden ph.1 15,569 | 19.5× · clear 16,235 | **IN BAND** (~15%) |
| boss fight duration | 59–118 s | ~65 s | **IN BAND** |
| player DPS | 310–620 HP/s (width = open cadence U-2) | ~250 HP/s | **BELOW BAND** — F-WR2-1's number |
| boss heavy hit ÷ pool | worst MEASURED hit taken all run: 34.3% · scripted heavy 10.4% | nova up to 55% (2×414.80/759) | **1.6–3.4× OVER** — the outlier |
| player:boss speed | 0.99/0.81 (boss FASTER) | 1.43 (boss slower) | we are GENEROUS vs referent |
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
