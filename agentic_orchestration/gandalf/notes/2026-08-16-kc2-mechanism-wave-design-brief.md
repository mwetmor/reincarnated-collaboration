# KC2 MECHANISM WAVE — DESIGN BRIEF

## The bundled interaction loop: post-displacement re-engagement · movement-while-channeling · pack-seek targeting

**Author:** gandalf (`SPEC-AUTHOR`) · **Date:** 2026-08-16
**Authority:** Matt rulings D1 = (A), D2 = (i), D3 = (a), D5, banked 2026-08-16 at the KC2-PM4 commitment boundary (ledger row **L-68**)
**Fires per:** `R-PM4-78 part 4` — *"the conductor authors the bundled-mechanism design brief (SPEC-AUTHOR seam) and hands to knight-rider for sequencing."*
**Lineage:** `R-CPB-4` (SB-1 ledger — motion wire-blocked scene-side, ROUTED to the engine as movement-while-channeling + pack-seek targeting policy) · `R-PM4-77 part 5` (the mechanism HALT) · `D-I12-5` (the targeting/locomotion surface, first named at I-12)
**Sealed run this hands off from:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (rows L-1..L-68, R-PM4-1..R-PM4-78; SEALED)
**Grading run this hands off to:** KC2-PM5 (chartered separately, *after* this wave ships — `R-PM4-78 part 3`, the wall between the runs)

---

## 0 — Authority chain, in one paragraph

RUN KC2-PM4 replicated Matt's real Grim Dawn Crucible fight (EoR Warlord, waves 150–160, death at
160) in the KC2 sim on frozen substrate `E-s09-cp150`, and closed its account: waves 151–160
replicate **faithfully in structure** (contact geometry, kill ring, wave cadence, body decode —
`GATE_S` EXACT ×7) and **unfaithfully in exactly one dimension — RING RESIDENCE.** The deficit is
located (per-body residence), bounded (2.1–11.5× at the referent's lower bound), and decomposed
(Q-leg ~85% of log-magnitude on every evaluable row, median `s_Q` 0.8478; body-count leg
insufficient even at saturation `f := 1`, reaching the referent lower bound on 0 of 10 waves;
wave-duration T-leg 0.384–1.863, **not one-signed**). Closing that distance is not a grading
question and not a tuning question. It is a **mechanism** question — and mechanism is production
code, outside RUN-CONDUCTOR authority. The conductor HALTed. **Matt ruled:** D1 = (A) the mechanism
work is authorized; D2 = (i) it ships as **ONE BUNDLED gamora wave** carrying three components as a
single interaction loop; D3 = (a) the build runs **outside any run** as ordinary engine work
(knight-rider sequences, jack-ryan Gate 2, decisions-log entry fires); D5 a **new** frozen
checkpoint is cut at the wave's close for PM5's cells, and `E-s09-cp150` is retained **immutable,
permanently.** This brief is the design hand-off. It is a **design spec, not an implementation
spec** — it names the decisions and the acceptance shape; the algorithms are gamora's.

**One further thing this brief does that no artifact in PM4 was permitted to do.** Across the run,
*attribution* was forbidden to every grading instrument by construction — instruments measure,
they do not explain. Five independent measurements converged on the same seam and each was
required to state magnitude without naming cause. **This brief is where attribution becomes
design.** What follows in § 2 is the mechanism claim, made in the open, by the party whose seam it
is, and made falsifiable by § 4's acceptance shape rather than protected by it.

---

## 1 — The convergent measurement (why this wave, and only this wave)

Five measurements, taken by different instruments under different definitions, point at one seam:

| # | measurement | what it says |
|---|---|---|
| **I-27** ring-residence census | sim residence is **terminated by displacement, not death** — `M_disp > M_death` on every cell ≥19 intervals, and displacement-terminated intervals are *longer*, not shorter | the ring empties because bodies **leave**, not because bodies **die** |
| **D-I12-5** | 51.2% of wave 154 elapses *after the player's last kill*; the remaining bodies die to `pet_ttl_expired` | bodies exist that neither engage nor die for half a wave — nothing re-converges them |
| **GL-12 / R-CPB-4** | the SB-1 record wire pins the player at 0.000000000 m across all **3,732 ticks** | the player model the replication ran is a **pivot**, not a fighter |
| **Lap AC fork (c)** | 235 decidable referent ring exits: **99 explicable by player motion alone** (share_player 0.4213, robust 0.344–0.456); **all 309 observed exits are EXIT_ALIVE** | the referent's bodies leave the ring **alive** — and the ring stays occupied anyway (bracket 3.24–3.43) |
| **I-28 / I-29** | arrival cannot close the residual even at saturation; window-duration cannot and is not one-signed; **residence carries ~85%** | the open question is not *getting there*. It is **staying** |

The divergence, stated at its narrowest (`R-PM4-74 part 3`): **displacement is real on both sides of
the seam. What differs is what a displaced body does next.** The referent's displaced bodies
*re-engage*. The sim's displaced bodies *are gone* — and the ring, movers-only, reads 0.19–0.49
against a referent bracket of 3.24–3.43.

That is the whole design problem, and it is a small one to state and a large one to feel.

---

## 2 — Design intent, in player-experience terms

### 2.1 The Crucible pressure fantasy

Matt did not play a shooting gallery. He played **Grim Dawn's Crucible of the Dead**, waves 150–160,
tier-16 rosters, in an arena roughly eleven metres across, channelling **Eye of Reckoning** —
a spin the character sustains *while walking* — into a press of nineteen to thirty-six living
bodies. He has described his own play in his own words twice on this project's record: *"the
direction of movement always be towards the largest group of enemies or most bosses"* and
*"I kited multiple packs into a single area to max leech/tick."* Those two sentences are not
colour. They are a **survival loop**, and every limb of it depends on one thing: **the ring stays
occupied.** Attack-Damage-converted-to-Health is a *rate over bodies in the disc*. Bodies in the
disc are simultaneously the threat and the health bar. Take the bodies away and you have not made
the fight easier — you have made it **a different fight**, one with no pressure and no sustain and
no reason to move at all.

That is precisely the fight the sim is currently running. In a threat-free clear-pacing sim,
KC2-PM1 measured the consequence and reported it honestly against its own pre-registered
prediction: **movement made the run LONGER** (3,732 → 3,817 ticks, +2.3%) — because when monsters
deliver themselves to a stationary disc and never need to be re-collected, **camping is optimal.**
That finding is not an argument against movement. It is the cleanest possible diagnosis of a world
whose monsters do not re-swarm.

### 2.2 What the genre knows about this

The re-swarm is not an exotic behaviour. It is the **melee ARPG's oldest load-bearing contract**,
and every game in the lineage pays it:

- **Grim Dawn, Crucible mode.** The arena is small and the spawn emitters ring it; the entire mode
  is built on packs that converge, get scattered by knockback and by your own movement, and
  **converge again**. Nemesis-class bodies re-path relentlessly. An EoR Warlord's whole gameplan —
  walk the spin through the press — only works because the press *follows the walk.*
- **Diablo II: Lord of Destruction, Whirlwind Barbarian.** Whirlwind is a *travelling* channel: you
  select a destination and carve through. The build has been played for twenty-five years on one
  assumption — **the pack re-forms behind you and you turn around and do it again.** D2's melee AI
  re-targets on the player's new position essentially continuously; that is why Baal-run and
  cow-level pulls read as a *tide* rather than a queue. Take away re-engagement and Whirlwind
  becomes a single-pass mower with nothing on the return trip.
- **Diablo III.** The genre's canonical failure case sits here too, and it is worth naming because
  it is the anti-pattern this wave must not build: vanilla D3's ranged-monster AI produced the
  much-complained "monsters that will not stand in your melee range," and the design answer was
  explicit re-collection tooling — **Ground Stomp, Threatening Shout, the pull affixes, Wrath of the
  Berserker.** D3 shipped whirlwind-with-full-movement and then had to *give the player a way to
  make the pack come back.* The lesson: if displacement is one-way, the fantasy dies, and you end
  up bolting pull mechanics onto it after launch.
- **Diablo IV.** Whirlwind is a full-speed movement channel by default — the modern reconciliation
  of the D2 contract.
- **Path of Exile, Cyclone; Last Epoch, Warpath.** Both are channels whose *entire identity is
  locomotion during channel*, and both live in worlds where a monster's re-target latency is
  effectively a frame. The skills are not interesting because they spin. They are interesting
  because **the spinner moves and the world chases.**

The counter-example — the shape to avoid — is the **orbiting vacuum**: a player who stops at the
edge of a pack, and a pack that mills at a fixed radius, producing a static pinwheel. It was named
and pre-empted once already on this project, at `R-PM1-2` (drive-through with rolling re-target;
no stop-at-edge). It is named again here because a badly-shaped re-engagement rule reintroduces it
from the *monster* side.

### 2.3 The intent in one sentence

**When the player moves — or when the crush of bodies shoves a monster out of its own attack
range — the displaced body's next act is to come back.** The ring travels with the player, the
pack re-forms around it, and the pressure the Crucible is built on becomes a property of the
simulation rather than an accident of a stationary pivot.

---

## 3 — Per-component design intent

Three components, one loop. They are bundled by Matt's D2 = (i) because **they are not separable:**
a moving player without monster re-engagement is a player who runs away from the fight (PM-1
measured exactly this — the player at 5.4 m/s outruns 339 of 344 bodies); monster re-engagement
without a moving player is a mechanism with almost nothing to do; and both are meaningless unless
the pack knows *which* player position to converge on and *which* pack the player is converging on.

> **A design law that governs all three components, adopted from the run's own practice:**
> **decode before declaring.** Grim Dawn's AI state machine is decodable substrate and this project
> has decoded it repeatedly (`ControllerAIState::ShouldFindEnemy` · `ControllerMonsterStatePatrol`
> → `DefaultEnemyFoundResponse` → `SetState("Pursue")` · `ViewDistance` 80.0 m on 169/169 tier-16
> rolls · `MaxPursuitDistance` 125 m · `meleeTargetDistance` 2.4). Where the referent engine's own
> transition rule for **"target is outside attack range"** can be decoded, it is decoded and folded.
> Where it cannot, the mechanism is **DECLARED, with its bound stated, its alternative left
> runnable, and its cost reported** — the `D-PURSUIT-TIME` pattern, which is this project's
> established honest form for a named-absent rule. What is forbidden is the third path: a
> plausible-looking invented rule with no provenance. If gamora judges a decode lap is needed,
> that is a **sequencing** item for knight-rider (a legolas fork), not a licence for this wave to
> improvise.

### 3.1 Component (1) — post-displacement re-engagement · **NEW**

**The decision to design:** *what does a displaced monster do next?*

The sim currently answers this implicitly, and the implicit answer is "nothing in particular." A
body whose ring interval terminated by displacement is not obviously wrong anywhere in the code —
it simply has no rule that notices its situation has changed. I-27 measured the consequence and
named it precisely: **displacement-terminated intervals are not merely more numerous than
death-terminated ones, they are LONGER.** The bodies are out there, alive, for a long time.

Design intent for the new behaviour:

- **A body that is out of its own attack range and has a live acquired target is in a LOCOMOTIVE
  state, not a waiting state.** This is the design's spine. The failure mode to eliminate is a
  monster burning its attack/cooldown clock at a position where its attack cannot land. Whether the
  engine expresses this as an explicit state transition, a per-tick range predicate, or a re-issued
  path is gamora's call — but *the condition must be noticed.*
- **Displacement has (at least) two channels and the rule must cover both.** (i) The player's own
  motion carries the engage ring away from a stationary attacker; (ii) crowd pressure — the
  non-penetration solver — shoves a body out of a ring it had reached, without either party
  intending it. The referent's own exit census shows both are real there and its bodies come back
  from both. A rule that only handles player-motion displacement leaves the crowding channel
  unaddressed, and crowding is *maximal* precisely in the dense late waves this replication cares
  about.
- **Re-engagement is a re-approach, not a teleport and not a leash-snap.** The body re-paths at its
  own `characterRunSpeed` (there is no global monster speed in this sim and this wave must not
  introduce one), obeys the same non-penetration geometry, and re-enters the ring the same way it
  entered the first time. Its re-entry should be *indistinguishable in kind* from its first entry —
  that is what makes the emitted residence ledger interpretable to PM5.
- **The behaviour must have an exit.** A rule with no terminal condition manufactures immortal
  pursuit. The referent supplies leash vocabulary already (`MaxPursuitDistance` 125 m; the
  `PursuitTime`-as-memory-timer declaration of record). Whatever terminal conditions exist must be
  **named and enumerable in the exit-cause partition** — "the body stopped coming back" is only a
  legitimate outcome if the reason has a name.
- **Design tension to resolve deliberately, not by default: re-engagement latency.** An
  *instantaneous* re-path is the D2/PoE reading and produces the tightest swarm. A *deliberate*
  re-path — a beat of reorientation before the body commits — is the Grim Dawn reading, and the
  project already has an open item pointing at it (`UNREACHED-AA-3`, the `AlertBeforePursue`
  animation length, animation `0x21`). This is a **decode-first** question by the law above. If it
  is declared instead, it is declared as one named constant with its bound stated, and the
  alternative stays runnable. **It is never solved against occupancy** (§ 4.3).

### 3.2 Component (2) — player movement-while-channeling · *previously routed by `R-CPB-4`*

**Status, verified in the tree, so the wave scopes against what exists rather than rebuilding it:**
`src/reincarnated/simulation/kc2/locomotion.py :: PlayerPolicy` already carries
**`DRIVE_TO_PACK`** (KC2-PM1 — channels while moving at full base speed toward the boss-weighted
densest live cluster, drives *through*, re-targets on cadence under hysteresis) and
**`CLUSTER_SEEK`** (KC2-PM3 — seeks the density centroid at the sim's own 3.0 m disc scale, arrives
and dwells, a declared departure from `R-PM1-2` scoped to that limb only). The policy machinery,
its declared constants, and its math notes exist and are pushed. **What does not exist is these
limbs being the model of record on the replication path** — the PM4 cells ran a camp limb, and the
consequence is the pinned player the whole run was measured against.

Design intent:

- **The replication path's player is a fighter, not a pivot.** The record cell for the mechanism
  wave runs a channelling-while-moving limb. `CAMP` / `CAMP_THEN_COLLECT` remain runnable —
  refuted-or-superseded limbs are *kept and made falsifiable* on this project, never deleted
  (`NodeAssignment.GROUP_CENTROID` is the precedent).
- **Full speed while channelling stands** (`R-PM1-1`), on the ground it was ruled: the reference
  scene was played at full speed, and the player model mirrors the play it models. The genre split
  is real and was named honestly at the time (D3's whirlwind baseline is reduced-speed, restored by
  the Hurricane rune; D4 and PoE Cyclone are full-speed) — but this is a *replication* of a
  specific fight, not a balance choice, and the referent's own play is the authority.
- **Drive-through with rolling re-target, not stop-at-edge** (`R-PM1-2`). The orbiting-vacuum
  anti-pattern is out of bounds from the player side as well as the monster side.
- **The pre-named consequence is the point, not a defect.** `R-PM1-2` said it before any code ran:
  *a moving player drags the 2.400 m engage ring; baseline dwells become chases.* Under component
  (1), chases resolve into re-engagements instead of into empty ring — **that interaction IS the
  wave.** Neither component demonstrates it alone.
- **Hysteresis is load-bearing, not tuning** (`R-PM1-3(b)`). Target-flapping between near-equal
  clusters is drunk-walk jitter in any scene that ever renders this trace. Its margin and cooldown
  are declared, seeded, deterministic constants, and their justification is *behavioural
  coherence*, not outcome.

### 3.3 Component (3) — pack-seek targeting policy · *previously routed by `R-CPB-4`*

**The decision to design:** *how does a pack re-acquire a moving player, and how does the player
choose which pack?* Two halves of one hand-shake; they are one component because a mismatch
between them is what produces the pinwheel.

- **Player-side objective expresses Matt's stated intent verbatim** (`R-PM1-3(a)`): score ≈ pack
  size + β·boss-weight, β declared. *"Towards the largest group of enemies or most bosses."* This
  is not a heuristic someone liked — it is the recorded intent of the player being replicated.
- **Monster-side acquisition is already decode-resolved and must not be re-litigated by this wave.**
  `ControllerMonsterStatePatrol::ShouldFindEnemy` returns TRUE; `EnemyFound` tail-jumps to
  `DefaultEnemyFoundResponse` → `SetState("Pursue")`; `FindEnemiesInSight` reads `ViewDistance`
  = 80.0 m on 169/169 rolled tier-16 monsters, over an arena whose worst-case spawn→player is
  ≲76 m. **Every Crucible monster acquires the player from the moment it is placed.** The sim's
  `MotionLimb.GATE_FIRST` is that semantics term-for-term and is the decoded reading of record.
  Acquisition is therefore *not* the open question.
- **The open question is TRACKING, and its shape is a cadence.** A pack that re-acquires a moving
  player *continuously* is D2/PoE-tight. A pack that re-evaluates on a coarse tick lags, and lag
  reads to a player as sluggishness or as exploitable pathing. The re-target cadence is a
  **declared constant with a stated bound** if it cannot be decoded — and the sim already has a
  precedent for a poll interval decoded rather than assumed (the 1000 ms advance-gate poll folded
  at I-19).
- **Pack coherence is a named design fork, and this brief takes a position without closing it.**
  Do bodies converge *individually* on the player's current position, or does a pack maintain a
  formation/centroid that converges as a unit? The Grim Dawn substrate carries a per-actor state
  machine with no obvious formation layer, and `distressCall` — an actual pull mechanic that would
  couple arrivals across actors — sits on this project's own out-of-model list, graded *unsigned*
  at first and **measured as signed** at I-27's lap (without it, low-`ViewDistance` actors beside
  dying neighbours never acquire). **My lean: individual convergence, decoded semantics, no
  invented formation layer** — with `distressCall` named as the coupling mechanism the model omits
  and left as a named open rather than improvised. If gamora's decode finds a coupling term, fold
  the decoded one. Matt rules if this becomes a commitment question.
- **Summons ride the same rule set.** The referent bracket carries **no summon term** (measured
  three independent ways at Lap AC; `NAMED-I27-1` resolved — movers-only is the definition of
  record). The sim's pets remain in the sim as measured fact and stay out of the graded numerator.
  Whatever pursuit rule lands, pets are not a special case invented for this wave.

---

## 4 — ACCEPTANCE SHAPE

### 4.1 ⛔ THE PROHIBITION — read this before the criteria

> **THIS WAVE MUST NOT TUNE TOWARD THE REFERENT'S NUMBERS. NOT ONE KNOB, NOT ONCE, NOT "JUST TO
> SEE."**
>
> The following figures are **the exam, and gamora is not permitted to hold the answer key as a
> target**:
> referent occupancy bracket **3.24–3.43** · sim movers-only occupancy **0.19–0.49** · the residual
> **2.1–11.5×** at the lower bound · `s_Q` median **0.8478** · ratio-to-rung-A **0.033–0.405** ·
> ρ **2.83–14.83** · any per-wave `T_ref`, `B_A`, or rung-A/rung-C value.
>
> **No constant introduced or modified by this wave may be selected, swept, fitted, or
> "sanity-checked" against any of them.** A re-engagement latency chosen because it moved occupancy
> toward 3.24 is a fitted parameter wearing a mechanism's clothes, and it would silently convert
> KC2-PM5 from an independent grading run into a validation of its own training target. That is
> the exact failure this project's **Law 3** exists to prevent, and it held across **twenty-nine
> iterations and every decode lap of PM4 with witnesses** — including on iterations that graded
> *worse* after a true fold was adopted (I-19, I-20). It does not get bent at the finish line.
>
> **The wall between the runs is structural** (`R-PM4-78 part 3`): the build happens *between* the
> runs, inside neither ledger; PM5 grades this mechanism **from a clean seat**, exactly as PM4
> graded the original sim. `E-s09-cp150` is untouched and immutable, permanently.
>
> **Therefore this wave's acceptance is MECHANISM-EXISTENCE ONLY. There are no numeric occupancy
> targets in this brief, and any that appear in the build's own criteria are a Gate-2 finding.**
> If the mechanism is right and occupancy still misses, that is a *finding* and PM5 will name it.
> If the mechanism is wrong and occupancy hits, we have learned nothing and corrupted the
> instrument.

### 4.2 Mechanism-existence criteria

The wave is complete when each of the following is **demonstrated from emitted artifacts**, not
asserted in prose. Every one is a *does-the-behaviour-exist* question. None has a magnitude.

| # | criterion | shape of the evidence |
|---|---|---|
| **A-1** | **A displaced body's disposition is total and enumerated.** Every ring interval that terminates by displacement resolves into a named outcome: re-entry · death en route · a named terminal cause (leash / despawn / wave end). **No unassigned residue** — an unclassifiable body HALTs the instrument. | exit-cause partition closing exhaustively, in the operational partition form adopted at `R-PM4-75 part 3` (assembled from the artifact's own construction; an unassigned key HALTs, never defaults) |
| **A-2** | **Re-entry events exist and are individually observable.** The residence ledger distinguishes first entry from re-entry and carries per-body re-entry latency. | ledger schema + non-empty re-entry population on the record cell |
| **A-3** | **No body burns its attack cycle out of attack range.** An actor with a live acquired target beyond its own attack reach is in a locomotive state. | a guard/assert on the state predicate, armed and demonstrably reachable (a guard that can never fire is `D-I27-2`'s green-by-absence, four laps running) |
| **A-4** | **The player path is a trajectory, not a constant, on the record cell.** | `tracks.player_path` non-degenerate; policy limb declared in the emission receipt; camp limbs still runnable |
| **A-5** | **The pack tracks a moving player.** Monster target positions update on the declared cadence; the engage ring travels with the player rather than persisting at a stale location. | a positional-lag census, published *as a census* — no target value |
| **A-6** | **Every constant this wave introduces is DECODED-with-citation or DECLARED-with-bound, and none is fitted.** Declared constants name their alternative and leave it runnable. | `Cited(...)`-form provenance, and a Law-3 witness set showing no constant moved toward an outcome |
| **A-7** | **Determinism preserved.** Same seed ⇒ byte-identical emission, ×2, layer declared. | digest ×2 per `FG-10` |
| **A-8** | **The instrument PM5 needs exists and emits.** Per-body ring residence intervals, exit-cause partition including re-entry, re-entry latency, per-wave movers-only occupancy — emitted, whatever they say. | artifacts on disk, digests published, re-hashed from bytes (`DO-NOT 8`) |
| **A-9** | **The new frozen checkpoint is cut, digested, and sibling-safe** (D5). | new file, own digest, `E-s09-cp150` byte-unchanged and verified so |
| **A-10** | **A pre-registered falsifier existed and was graded as written.** Whatever the wave predicted about its own behaviour, it says so *before* running and reports the result unedited. | prereg committed **alone, before code**, per the run's standing practice |

### 4.3 What a failure looks like (so it is recognisable)

- Occupancy appearing in *any* acceptance criterion, sweep, or commit message of this wave.
- A constant whose stated justification is an outcome ("0.35 s worked best").
- A guard that cannot fire.
- Re-engagement that only handles player-motion displacement and silently ignores crowd-shove.
- A pack that mills at a fixed radius — the orbiting vacuum, from the monster side.
- An invented rule where the substrate could have been decoded (§ 3 design law).
- Deleting a superseded limb instead of keeping it runnable.

---

## 5 — Constraints

1. **NO BALANCE TUNING.** Not in this wave, not "while we're in there." Comparative behaviour
   against the pinned baseline is the deliverable — the same discipline KC2-PM1 ran under.
2. **NO THRESHOLD CHASING.** § 4.1 governs. Law 3 stands in its strongest form.
3. **`E-s09-cp150` IS FROZEN, PERMANENTLY** (Matt D5; `GL-6`). Never overwritten, never amended,
   never "regenerated for convenience." Retained for lineage forever. Any new baton or checkpoint
   is a **SIBLING file with its own digest.**
4. **NEW CHECKPOINT FREEZE RIDES THE WAVE'S CLOSE** (Matt D5) — cut post-mechanism, digested,
   handed to PM5's charter as its cells' substrate. Naming is gamora/star-lord's; the constraint is
   sibling-not-successor.
5. **No global monster speed.** Per-actor `characterRunSpeed × v_ref` stays the model; a single
   `v_mob` constant is the exact class of uncited bare float `F-12a` caught.
6. **Superseded limbs stay runnable**, so their refutations stay reproducible.
7. **The two-functional referent carve-out does not travel.** PM4 licensed exactly two referent
   functionals for grading; **this wave grades nothing against the referent at all.** Referent
   values are not inputs, not comparators, and not sanity checks here.
8. **The run's law stack binds this build by reference** (`R-PM4-78 part 2`): `DO-NOT 8`
   (truncated pin is a locator, not a digest — re-hash from bytes at the moment of writing) ·
   the partition operational form · `D-CON-9` (a grade names its quantity, population, and clock) ·
   math-note-first, committed ALONE before code (Discipline #1) · defect addenda committed ALONE
   *before* their repairs.
9. **Ordinary engine work, ordinary governance** (Matt D3 = (a)) — this is not a run, has no
   conductor, and no ledger. Knight-rider sequences it; jack-ryan gates it; the decisions-log
   records it.

---

## 6 — Hand-off table

| party | role on this wave |
|---|---|
| **gamora** | **Implements.** All three components as one bundled wave. Owns every algorithmic and parameter decision inside the design intent above. Math note first, alone, before code. Pre-registers its own falsifier. Emits the instrument A-8 names. Cuts the D5 checkpoint at close. |
| **knight-rider** | **Sequences.** Slots the wave; resolves cross-seam ordering (star-lord export/emission surfaces — PM-1 already carried two `MIGRATION` deltas and an emitter volatile-field finding; drax/SB-1 scene consumption is a *later* beat and is not gated on this). Routes the § 3 decode-vs-declare fork to legolas if gamora calls for it. Carries the decisions-log entry to jack-ryan. |
| **jack-ryan** | **Gate 2**, with BLOCK authority. Two findings this brief specifically asks him to look for: (i) any acceptance criterion, sweep, or constant selected against a referent number (§ 4.1 — the single highest-value catch on this wave); (ii) any guard that cannot fire (`D-I27-2`'s green-by-absence class, which ran green for four laps). |
| **decisions-log** | **Entry fires** (Matt D3 = (a)). Architectural commitment: the sim's player model on the replication path changes from pivot to fighter, and monsters gain post-displacement re-engagement. jack-ryan writes; gandalf/knight-rider propose; Matt approves. |
| **gandalf (`DRIFT-CRITIC`)** | **Reviews the build against this brief** — design intent honoured, § 4.1 prohibition honoured, decode-before-declare honoured, genre anti-patterns absent. Verdict on the wave *as design*, separate from jack-ryan's process gate. `⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC` fires at that review. |
| **Matt** | Rules any commitment-boundary question that surfaces mid-build (scope, substrate, a fork this brief left open). Approves the decisions-log entry and the checkpoint freeze. |
| **gandalf (`RUN-CONDUCTOR`)** | **Not on this wave.** Charters KC2-PM5 *after* the mechanism ships and the checkpoint freezes — the wall between the runs (`R-PM4-78 part 3`). |

---

## 7 — What KC2-PM5 will grade

> **Read this section for INSTRUMENT DESIGN ONLY.** It exists so gamora emits what PM5 will need to
> measure. **Nothing in it is a target.** § 4.1 governs this section with full force — knowing the
> exam's *shape* is legitimate; aiming at its *answers* is the one failure this whole architecture
> is built to prevent.

- **The pass criterion PRE-REGISTERS at PM5's charter, before any cell runs** (Matt D4). The
  conductor's lean — recorded as a lean, **not a lock** — is per-wave sim movers-only occupancy
  inside `[rung-A, rung-C]` on evaluable waves, with the aggregate inside the pinned band. It may
  change at prereg, and gamora has no standing to build toward it.
- **PM5 inherits the referent BY DIGEST, never by re-derivation** — exactly the I-29 `pinned_inputs`
  block (eight full-64 digests: AD1/AD2/AD3, R1, S1/S2/S3, MATH_NOTE) plus the artifact digests
  banked in ledger rows L-64..L-67. It inherits PM4's law stack by reference and may re-rule the
  two-functional carve-out for itself at prereg.
- **The decomposition re-runs.** `L = Q·N/T`, each side its own T, referent values as **grades never
  inputs**. The question PM5 asks is whether the **Q-leg** — per-body residence, which carried ~85%
  of the log-magnitude on every evaluable row — moved, and whether the N- and T-legs stayed honest.
- **`GATE_S`-class sim-fidelity checks travel.** PM5 will verify that limbs this wave did *not*
  touch still reproduce their pinned values exactly. **Practical consequence for the build:** keep
  the mechanism's blast radius nameable. A change that perturbs contact geometry, the kill ring,
  wave cadence, or body decode as a side effect makes PM5's fidelity gate unpassable and the
  finding uninterpretable.
- **The new checkpoint opens coverage that PM4 could not reach.** `UNREACHED-I28-4`'s **54 rows**
  — the wave-157–160 cells no PM4 board could fight past — become closable for the first time under
  D5's checkpoint. This is the largest single gain the freeze buys.
- **`NAMED-CON-AD-1` transfers as a gated open**: two referent per-wave duration vectors exist and
  disagree beyond tolerance on three waves; T3 provenance must be reconciled before any T3 span-MAE
  grading fires. Not this wave's problem; named so nobody trips it.
- **All other `UNREACHED` items transfer as named opens with their obstacles**, per the seal.

---

## 8 — Closing note from the SPEC-AUTHOR seat

PM4 did the hard and unglamorous thing: it ran twenty-nine iterations, renamed its residual
fourteen times as each carrier was decoded and folded, graded itself *worse* on iterations where a
true fold cost it a number, and never once moved a constant toward an outcome. What it bought with
that discipline is the right to say the following sentence and be believed:

**The sim's fight is unfaithful in exactly one dimension, and the dimension is that its monsters do
not come back.**

Every ARPG worth its lineage pays that contract — D2's Whirlwind Barbarian, PoE's Cyclone, Last
Epoch's Warpath, and the Grim Dawn Crucible run this project is replicating. Nobody notices it
while it works. It is the substrate the whole melee power fantasy stands on, and its absence does
not read to a player as "wrong pathing" — it reads as **a fight with no weight.** The bodies arrive,
they die, nothing presses. There is no reason to move because moving costs you the fight, and no
reason to hold ground because ground was never contested.

Build the contract. Do not build the number. If the contract is right and the number still misses,
PM5 will tell us — honestly, from a clean seat — and *that* is a finding worth having. A number
reached by aiming at it is worth nothing at all.

---

*Authored by gandalf (`SPEC-AUTHOR`), 2026-08-16, per `R-PM4-78 part 4` on Matt's D1/D2/D3/D5
rulings. Hands to knight-rider for sequencing. The build runs outside any run; the grading run
comes after.*
