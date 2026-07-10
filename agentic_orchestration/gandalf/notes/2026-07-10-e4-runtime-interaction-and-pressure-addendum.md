# E4 Addendum — Runtime Interaction Systems + Interruption Pressure + Scope-Exemption Audit

**Author:** gandalf, 2026-07-10. **Trigger:** Matt directive (same-day, on the landed E4 design note):
*"we need to build the runtime interaction systems either in parallel or push them upstream so that
they also work in the battle sim … [ultrathink] how the battle simulation will need to model
interruption pressure … The 68,040 × 3 = 204,120 math is not true due to these scope exemptions."*
**Standing:** this addendum EXTENDS `2026-07-10-e4-commitment-axis-design-note.md` — the rocket+gamora
dispatch pair builds against note + addendum as one authority. §F forks await Matt; everything else
is design-note-level intent (Matt curates; objection reopens).
**Source-verified this session:** `endgame_encounter_catalog.py:130-134` (5 coords, 324 lattice) ·
`qd-engine-bc-axes-lock-2026-05-20.md §2` (8 axes, 68,040) · `per_skill_emitter.py:159-190, :282,
:326, :360-373, :524-551` (role vocabulary + E2 exemption machinery) · `spatial_engine.py:365,
:1052-1173, :1265-1337, :2002-2014` (behavior branches, kite logic, kills-only timeout semantics,
HP<50%-timeout loss).

---

## A. Parallel vs upstream — the architectural answer: ONE contract, upstream mechanics, parallel presentation

Matt's either/or dissolves under the already-ruled **versioned packet contract** law (business-platform
strategy, NOW-obligation #1). The commitment runtime fields are emitted ONCE (rocket), then consumed by
THREE surfaces:

| Consumer | Reads | Ignores |
|---|---|---|
| **Battle sim** (gamora) | mechanical fields: cast/tick/drain/move-policy/break rules | animation/UX fields |
| **Godot** (drax) | mechanical + presentation fields (same numbers the sim certified) | — |
| **Loadout** (drax) | descriptive projection (cast bar stats, drain readout) | runtime state |

**Consequence:** the runtime-interaction fields enter the SAME rocket+gamora dispatch pair — a scope
amendment to the pair, not a separate later build. Mechanics are upstream (sim-certified); presentation
rides in parallel on identical data. The sim and the game can never disagree about what a channel IS,
because there is only one description of it. This kills the classic failure where cert models a
different skill than the player casts (D3's tooltip-vs-actual coefficient drift, years of it).

**Honest cost statement:** "cheapest of the four" is now doubly dead. The pair is a mid-size cross-seam
build: rocket (coordinate + runtime fields + pricing) + gamora (cast-state machine, ticks, break rule,
pilot policy, regime matrix, perf guard). Still ONE math-note conversation at the pricing loop.

## B. Runtime interaction systems — field-level design

### B.1 Cast-state machine (the new sim primitive)
One actor-level state machine, two configurations:
- **wind-up:** `idle → committing(cast_time) → resolve-at-completion` — damage resolves against world
  positions AT completion (motion-whiff law, already ruled).
- **channel:** `idle → channeling(tick loop) → released | broken | exhausted` — per-tick resolution.
- **snap:** degenerate case (no state, current behavior).
Integration points: the readiness gate (`action_available_at`, `spatial_engine.py:1281`) gains a
busy-state; the behavior branch (kite/reposition logic `:1052-1173`) SUSPENDS while committed under
`rooted` policy — this is what makes lock-opportunity-cost mechanically real instead of a phrase: a
rooted channeler stops kiting, and the sim's kiting is real, so the exposure is real.

### B.2 Tick system (channel)
- Damage applies per tick; **each tick resolves against positions at tick time** (extends the
  motion-honesty law from completion-instant to the tick train — a beam tracks, a ground-tether
  doesn't; the frame declares which).
- `tick_interval_seconds` guidance band **[0.25, 0.5]s**: ≤0.5 so channel feels continuous (genre floor:
  D3 channel breakpoints ~4-6 ticks/s scaled; we don't need that density in a cert sim), ≥0.25 so the
  36 fights/s instrument doesn't degrade (perf criterion §E).
- Per-tick damage share derives from the k-aware period model (math note) — total channel throughput
  in-band, ticks are the delivery texture.

### B.3 Drain economics + cost timing
- **Channel pays per tick** (`drain_rate` per second, resource per the kit's economy model). Sustain
  window = pool ÷ net drain — a NATURAL channel duration bound; no artificial max-duration needed.
- **Wind-up and snap pay on commit** (cost deducted at initiation). A whiffed wind-up forfeits the
  resource — the economic leg of the risk the pricing loop measures. Genre: D2 mana paid at cast start;
  the refund-on-whiff alternative makes whiffs free-ish and dishonors the premium.
- **Economy-coupling guard (Axis 5):** drain must be sized against the kit's resource model so it
  BINDS — an `overflow`-economy kit whose drain never approaches its regen has a free channel (lock
  premium unpriceable). `starved` × channel = double-starve: legal, flagged, expect low sustain uptime
  as the identity. Math note derives drain per (economy bin, k).

### B.4 Move-while-channeling policy
`move_policy ∈ { rooted | walk(pct) | full_move }` — emitted per channel skill:
- **rooted** — default for beams/tethers (PoE Flameblast-class stakes; the lock IS the identity).
- **walk(pct)** — curated exceptions (D3 walk-while-channeling item affix precedent; ~40-60% speed).
- **full_move** — the spin class (B12 Whirlwind re-cert; PoE Cyclone). Required for spin-channel; also
  the resolution of the **dodger × channel** coupling (§D.3): a dodger-defensive-profile kit may only
  take channel with non-rooted policy, or it accepts windowed-vulnerability as identity.
Sim consumption: `rooted` suspends the behavior branch; `walk` scales `movement_speed`; `full_move`
leaves it untouched.

### B.5 Break rules
- **Voluntary release:** free, any tick boundary (player agency — D3 got this right; a channel you
  can't exit is a coffin). Remaining sustain is simply unspent.
- **Wind-up move-cancel:** legal, forfeits the cast AND the committed cost (no refund). Gives the pilot
  (and later the player) an out; makes whiff-avoidance an active skill instead of pure dice.
- **Forced break (the v1 sim rule — §C.2):** ramp/stage reset (if F-2b adopted) + short recovery
  lockout (guidance 0.3–0.5s, math-note-derived) + no refund of the broken tick.

### B.6 Channel reward structure — fork F-2 (§F)
Flat-ticks+drain vs ramp+break-reset vs staged-release. My lean is (b) ramp — argued at the fork.

### B.7 Animation / UX packet fields — bounded per weapon-manifestation-class
Presentation-only fields (sim ignores): `charge_pose_id`, `channel_loop_id`, `release_anim_id`,
`cast_bar {duration, interruptible}`, `channel_meter {drain_rate, sustain_s}`.
**Matt's parenthetical ratified as the lean:** the pose/loop vocabulary is a CLOSED ENUM declared per
**weapon-manifestation-class** (the E7 identity layer) — 2H overhead wind-up, bow draw-hold, staff
gather, tether stance. Kits inherit their weapon class's set; generators pick from it, never invent.
This keeps drax's Synty animation library finite, star-lord's packet enum closed, and the D7 line
intact (no LLM inventing animation names). UI/UX surface design itself = drax seam + galadriel rubric
downstream; this note only fixes the field contract.

## C. Interruption pressure — instrument honesty

### C.1 The diagnosis, both failure signs
Matt's statement, sharpened: **the pricing loop calibrates premiums against MEASURED risk; if the
instrument's risks are fake, the premium is fiction.** Two directions:
- **Channel:** if the gauntlet has no lock cost and no break pressure, channel measures as safe
  sustained throughput → priced flat → in live play (where lock and breaks are real) it's strictly
  dominated → dead bin. OR, with drain but no premium: dominated inside the sim itself and mis-banded
  low. Either sign, same disease.
- **Wind-up:** if regimes are static, completion rate measures ~100% → the premium (big hits) is paid
  without the whiff risk ever expressing → over-banded → GGG-style nerf-after-ship. The D3-Inferno
  graveyard, manufactured by our own instrument.

### C.2 The split ruling (proposed — fork F-0): RULE upstream at v1, PRESENTATION at v1.1
- **v1 (sim, this pair):** a minimal **forced-break threshold rule** on channels — cumulative incoming
  damage ≥ Y% max-HP within window W forces a break (form at fork F-1). ONE rule, math-note-derived,
  Discipline #17 empirically calibrated. NOT a poise/stagger system.
- **v1.1 (unchanged re-entry):** the player-facing interrupt design — stagger bars, poise, wind-up
  interruption, CC-vs-channel interactions — consumes the SAME rule as its floor and designs the
  presentation + the wind-up-interrupt extension on top.
- **Wind-up stays un-interruptible at v1:** its priced risks (whiff + truncation + move-cancel
  forfeit) are already real once regimes are honest; adding damage-interrupt to wind-ups without the
  full stagger design would double-charge the bin.
This is Matt's "push upstream" made precise: the RULE lives upstream where certification needs it; the
FEEL lives downstream where the player meets it.

### C.3 The three-honesty-axes law (guard-2 extended)
Each commitment cost maps to the regime property that makes it measurable. The cert regime matrix MUST
contain at least one regime per axis, or the corresponding premium is uncalibrated:

| Honesty axis | Regime property | What it prices |
|---|---|---|
| **Mobility** | targets that reposition (kite/hit-and-run branches exist: `spatial_engine.py:1134-1173`) | wind-up whiff rate |
| **Lethality** | incoming damage that genuinely threatens (deaths + HP<50%-timeout losses are already fitness-visible: `:321`, `:1597`) | channel lock exposure + forced-break rate |
| **Attrition** | fights long enough that sustain windows bind (60–240s scenarios exist: `:70-86`) | drain economics |

The substrate for all three ALREADY EXISTS in the sim — this law is a regime-matrix composition
requirement on the gauntlet, not new machinery.

### C.4 Pilot-competence baseline (the counter-direction threat)
The action policy currently optimizes fastest-cycling under kills-only timeout semantics
(`spatial_engine.py:1265-1337`) — it is commitment-blind. A dumb pilot mis-prices the OTHER way:
initiating wind-ups against departing targets → pessimistic completion rates → inflated premium →
over-banded in live play the moment a competent player pilots the kit. v1 pilot floor (gamora):
- initiate wind-up only when the target's projected position at completion is inside the template
  (the sim has positions and velocities; this is one extrapolation);
- hold channel until drain exhaustion, threat threshold, or target death; no frivolous release.
Cert measures the kit at a COMPETENT baseline, not an idiot one. Genre: every serious balance sim
(GGG's internal, Blizzard's THUD-era community sims) learned this — bot competence is part of the
instrument's calibration, not a nicety.

### C.5 Telemetry additions (star-lord, downstream of gamora measurement)
Per (kit, commitment_bin, regime): `completion_rate`, `whiff_rate`, `damage_taken_while_committed`,
`forced_break_count`, `move_cancel_count`, `drain_exhaustion_events`, `sustain_uptime`. These ARE the
pricing loop's inputs — guard 1 is unimplementable without them.

## D. Scope-exemption audit — "is 204,120 true?" No, and here is exactly why

### D.1 The two-space conflation (my arithmetic error, corrected)
The E4 note's "68,040 × 3 = 204,120" grafted the new coordinate onto the WRONG space:
- **68,040** = the 8-axis QD MAP-Elites archive (`qd-engine-bc-axes-lock-2026-05-20.md §2`:
  6×5×3×3×3×3×4×7). Form of record: **"68,040 full lattice / 12,960 live"** (motion-frame amendment
  corrections-of-record).
- **The catalog `bc_commitment` actually joins** (per the Q-E4-4 ruling: "sixth coordinate") =
  `endgame_encounter_catalog.py:130-134`: range(3) × tempo(3) × amplitude(3) × attribute(4) ×
  proxy_density(3) = **324 lattice → 972 with commitment**; live = the 25 roster CellDefs, each
  taking one commitment value (pinned or rolled).
- **QD-archive admission of commitment as a NINTH axis** (which WOULD produce 204,120 lattice) is a
  separate decision requiring the same arity stress-test the 5→8 lock session ran — especially since
  Axis 5 already contains commitment-adjacent bins (below). Deferred to fork F-3.
**Corrected statements of record:** catalog **324 → 972 lattice / 25-31 live (roster)**; QD archive
unchanged at 68,040/12,960 pending ninth-axis stress-test. All prior "204,120" cites corrected to
point here.

### D.2 Skill-scope ≠ cell-scope
The support/control/T4 exemptions cut which SKILLS inside a kit express the bin — they never cut
CELLS, because support is not a cell dimension in either space (verified: no support bin among the 5
catalog coordinates or the 8 archive axes; the emitter's `support` is a chain-role,
`per_skill_emitter.py:524-551`). So "we removed support" was never what broke the ×3. What breaks it
is COUPLINGS:

### D.3 The coupling table (the nonsense-cell audit Matt asked for)

| Coupling | Verdict | Reasoning |
|---|---|---|
| amplitude **flat × wind-up** | **INFEASIBLE-BY-PRICING — hard cut** | the premium must express as per-hit size (k-model: lower rate × lower completion ⇒ higher per-hit to hold band) — which IS spiky/variable; flat wind-up cannot exist inside tolerance |
| amplitude **spiky × channel** | **INFEASIBLE at v1** | a pure tick train is flat by construction; unlocks via staged-release (F-2c: PoE Blade Flurry) if later admitted |
| economy **overflow × channel** | LEGAL-GUARDED | drain must be sized to bind (§B.3) or the lock premium is unpriceable |
| economy **charge-stack × wind-up** | **BOUNDARY LAW** | charge-stack (accumulate-N-then-spend, Axis 5 bin) ≠ wind-up (cast-time commitment); generators and cert must never conflate them — the archive already reserves charge-up-skill as a cross-axis mechanic |
| defensive **dodger × channel** | CONDITIONAL | legal only with `move_policy ≠ rooted` (spin class) or accepted vulnerability-window identity (§B.4) |
| **proxy ≥ light × channel** | CONDITIONAL | legal ONLY as `while_channeling` tether (F-substrate persistence — the lock is the proxies' lifeline, so it costs something); fire-and-forget proxies + channel = nonsense (output decoupled from the lock ⇒ risk-free premium) |
| **control-pure (Axis 2B) × commitment** | DILUTED — fork F-5 | the coordinate would hang on the kit's minority attack complement |
| engagement ***-fast × wind-up** | SOFT TENSION — no pre-prune | sparse occupancy expected; MAP-Elites self-resolves (empty cells are the mechanism, ~1.5% occupancy is design-normal) |

**Enforcement point:** couplings bind the SAMPLER and the PRICING law (the things that actively try to
fill cells) — the archive itself needs no pruning; emptiness is its native answer.

### D.4 The genuinely uncovered class: summon-act skills
The four-way scope table (attacks FULL / control cast-only / support exempt / T4 per-capstone) does
NOT cover the **13th summon skill** appended to proxy-dominant cells
(`season_generation_pipeline.py:1140+`) — it is none of those roles. Proposed fifth scope row (fork
F-4): **summon-act skills carry commitment** — conjure defaults **wind-up** (matches the ruled
conjure-summon T4 pin; the summoning-ritual fantasy), snap-summon legal (D2 Revive spam), and
channel-summon ONLY as `while_channeling` tether per D.3. This closes the last skill-role hole.

## E. Amended acceptance criteria (additions 13–19 to the design note's twelve)

13. **Cast-state machine** lands in the sim with per-tick position resolution (B.1/B.2); readiness
    gate + behavior-branch suspension integrated.
14. **Drain + pay-on-commit economics** (B.3) derived k-aware AND economy-aware in the math note;
    overflow-binding guard demonstrated.
15. **Move-policy enum** (B.4) emitted + honored by the behavior branches; spin class certifies under
    `full_move`.
16. **v1 forced-break rule** (C.2) implemented + calibrated (Disc #17); telemetry fields (C.5) land
    with it.
17. **Three-honesty-axes regime matrix** (C.3): the cert gauntlet demonstrably contains ≥1 mobility,
    ≥1 lethality, ≥1 attrition regime, and the pricing loop consumes rates measured across them.
18. **Pilot-competence floor** (C.4): wind-up initiation gating + channel hold logic; report the
    delta in measured completion rates vs the blind pilot (the calibration honesty receipt).
19. **Perf bound:** instrument throughput ≥30 fights/s with the state machine + ticks live (baseline
    36; regression >17% blocks).
Packet-contract version bump (B.7 fields) rides criterion 10 (provenance) — one version, all fields.

## F. Forks for Matt (ELICITOR — decision-shaped, with leans)

| # | Fork | Options | gandalf lean |
|---|---|---|---|
| **F-0** | Ratify the split: interruption RULE v1 (sim) / interruption PRESENTATION v1.1 (player-facing stagger) | yes / no / all-v1.1 | **YES** — this is your "push upstream" made precise; all-v1.1 leaves channel pricing dishonest for the entire axis run |
| **F-1** | Forced-break threshold form | (a) single hit ≥X% maxHP · (b) cumulative ≥Y% in window W · (c) both | **(b)** — cumulative reads "sustained pressure breaks concentration"; single-hit makes break a stat-check one big mob auto-wins (PoE stun-threshold lineage) |
| **F-2** | Channel reward structure v1 | (a) flat ticks + drain · (b) ramp + break-reset · (c) staged-release | **(b)** — without ramp, a forced break costs a fraction of a tick and the break rule prices at ~0; ramp-reset gives pressure TEETH (D3 Ray of Frost, PoE Incinerate). (c) is the later spiky×channel unlock, not v1 |
| **F-3** | Space bookkeeping of record | adopt catalog 324→972/25-31-live + defer QD ninth-axis to arity stress-test · vs. admit ninth axis now | **ADOPT + DEFER** — ninth-axis admission needs the 5→8 session's discipline, and Axis 5 overlap (charge-stack) must be boundary-drawn first |
| **F-4** | Summon-act fifth scope row (D.4) | as proposed / summon-acts exempt | **AS PROPOSED** — exempting them re-opens the free-premium hole for the proxy octet |
| **F-5** | Control-pure kits' commitment expression | (a) attack-complement carries the bin · (b) snap-pin default | **(a)** — even a controller's attacks have rhythm identity; (b) wastes the texture dimension on a whole Axis-2B bin |

**Signed:** gandalf, 2026-07-10. A commitment the instrument can't hurt is a commitment the game can't
price. Build the pressure where the pricing lives — the player only ever feels what the sim already
paid for.

---

## RULINGS RECEIVED (Matt, 2026-07-10 — same-day)

> *"I Ratify all except space bookkeeping as I need more information on this topic."*

| Fork | Ruling |
|---|---|
| **F-0** | **RATIFIED** — interruption RULE v1 (sim-side forced break) / PRESENTATION v1.1 (stagger UX). The split is LAW for the pair. |
| **F-1** | **RATIFIED (b)** — cumulative ≥Y% max-HP within window W forces channel break; Y/W math-note-derived, Disc #17 calibrated. |
| **F-2** | **RATIFIED (b)** — ramp + break-reset is the v1 channel reward structure; staged-release (c) stays the named spiky×channel unlock, not v1. |
| **F-3** | **HELD** — Matt needs the two-space distinction re-explained (8-axis QD archive vs `endgame_encounter_catalog.py`) before ruling. Explainer delivered same-turn; also answered: the archive-vs-catalog gap is the blocker for exactly the Axis-5 bench trio (B1/B2/B3), not the whole bench. |
| **F-4** | **RATIFIED** — summon-act fifth scope row: summon-acts carry commitment; conjure defaults wind-up; channel-summon tether-only (`while_channeling`). |
| **F-5** | **RATIFIED (a)** — control-pure kits' commitment expressed via attack-complement. |

**Same-message riders (Matt):** (1) **B12 admission-in-principle** — *"D2 Barb spin-to-win is moved to unblocked"*: the E4 pair's channel machinery + `full_move` policy is the re-cert TARGET; promote-path = pair lands → G3 zero-behavioral-diff migration audit → re-cert at channel bin. (2) **Bench-promotion intent declared** — *"bring all kits into the pilot if we can, so that we only have experimental/research left open"*: a bench-promotion elicitation pass over the remaining 12 is queued post-E3-design (see serial tracker fourth entry 2026-07-10).
