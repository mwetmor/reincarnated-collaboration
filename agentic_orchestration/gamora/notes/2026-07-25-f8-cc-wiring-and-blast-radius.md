# F8 hard-CC consumer wiring — wiring summary, acceptance probe, blast radius

**Agent:** gamora (simulation seam)
**Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-gamora-f8-cc-consumer-wiring.md`
(gandalf SPEC-AUTHOR, under Matt ruling 2026-07-25: *"We ARE building all mechanics needed into our
engine. If we don't yet have CC in the sim, then we build it in — we don't work around it."*)
**This is the dispatch § 4 report.** Gate 2 request filed at
`agentic_orchestration/qa/pending/2026-07-25-gamora-f8-cc-wiring-gate2.md`.

**Provenance note:** the build and the A/B were executed in a prior gamora session that died on a
stream timeout before this report was filed. This document is a **closeout synthesis**: every number
below was re-read from the committed artifacts on disk, and the acceptance probe was **re-executed
read-only against current HEAD** for this report. Anything not verifiable from disk is marked
**UNVERIFIED** and named as such.

---

## 0. Headline

Two findings lead, in this order.

**(1) The measured control-kit delta is moderate and concentrated, not verdict-flipping.**
Across the full 64-cell frame the CC-bearing kit moves **−0.9242% observed_kpm / +3.3907% mean
duration** in aggregate. All movement is confined to **one shell (`magic_pack`)**, where it is
**−9.7379% kpm / +10.8510% duration**, worst single cell **−13.6392%**. **Zero KPM band verdict
flips** — every pre and post value sits interior to the magic_pack band `(12.52, 102.86)`. The
zero-CC control arm is **32/32 cells byte-identical, 0.0000% on every metric**. No historical
verdict class in this frame needs an asterisk on band membership; the asterisk that IS owed is on
comparability, § 4.3.

**(2) The frame never exercised hard CC at all — and that is the finding that routes.**
Across all 66 kit configs in the census the **only** CC effect type present anywhere is `chill`, at a
single magnitude (`slow_percent 0.35`, `duration_seconds 3.0`). The instrumentation counters confirm
it at runtime: the post arm records `nav_slowed = 12180` and **no `select_action_locked` key and no
`nav_move_locked` key at all** (the harness's `bump()` creates a key only when it fires — absence is
a hard zero). So the entire measured blast radius above is the **soft-CC / chill** arm. The
stun / freeze / root / silence action-and-movement locks — the actual F8 subject — landed **zero
times in 64 cells** and their in-sim blast radius is **UNMEASURED**. Their correctness rests
entirely on the 35-assertion unit suite (§ 2), which is green. This is a **generation-side** finding
(the kit pool emits no hard CC), not a wiring defect, and it is routed, not patched.

---

## 1. Wiring summary (file:line — the VERIFIED map)

All sites in `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`. Source of truth is
math note § 8 (commit `fe5d5ea`), **not** commit `9f3135a`'s message, whose line numbers are
pre-implementation estimates (every SITE it names is correct; the offsets are 4–100 lines off).

Re-verified line-by-line against the committed file for this report:

| Math note § 8 line | Site | Role | Re-verified |
|---|---|---|---|
| `542` | `def _f8_action_locked(entity)` | § 2 predicate — freeze ∨ stun | **exact** |
| `577` | `_f8_move_locked` | § 3 predicate — freeze ∨ stun ∨ root | **site correct, line off** — `def` is at **`561`**; `577` is inside the body |
| `595` | `_f8_slow_factor` | § 3 σ — chill product, 0.1 floor | **site correct, line off** — `def` is at **`579`**; `595` is inside the body |
| `700` | `WIRE_HARD_CC: bool = True` | § 6 flag | **exact** |
| `1770` | `_navigate_entity` | § 3.4 MOB movement lock, ahead of every branch | **exact** (`if _f8_move_locked(entity):`) |
| `1877` | `_navigate_entity` fear-flee | § 3.5 σ on the flee vector magnitude | **exact** |
| `1978` | `_navigate_entity` move block | § 3.1 σ × (1−δ), successive multiplication | **exact** |
| `2109` | `_select_skill_for_entity` | § 2 action lock — covers player AND mobs | **exact** (`if _f8_action_locked(entity):`) |
| `2135` | `_select_skill_for_entity` | § 2.1 silence scan, hoisted once per call | **exact** (`_f8_silenced = False`) |
| `4291` | `run()` player move block | § 4.1 player lock into `_e4_move_scale` | **exact** (`if _f8_move_locked(self.player):`) |

**8 of 10 rows land on the exact line; 2 rows point ~16 lines into the correct function body.** Both
misses are the two helper-definition rows, and both still land inside the function they name — the
map is navigable, but § 8's "verified" claim is stronger than the two rows support. Recorded here so
the Gate-2 reviewer is not surprised. Not amended in the engine repo (no code change to justify a
third commit on this).

**Selector call sites (independently re-verified for this report):** `_select_skill_for_entity` is
defined once at `:2066` and has exactly two production call sites — `:4369` (player action phase,
`_select_skill_for_entity(self.player, alive_mobs, …)`) and `:4564` (mob action phase,
`_select_skill_for_entity(mob, mob_targets, …)`). The commit message's `:4171 / :4366` are the same
stale-offset artifact; the *claim* they support is correct.

**Test file:** `tests/test_f8_hard_cc_consumer.py` (569 lines, added in `9f3135a`).
**Math note:** `src/reincarnated/simulation/math/f8-hard-cc-consumer-wiring-2026-07-25.md`.
**MIGRATION.md:** entry `[2026-07-25] F8 HARD-CC CONSUMER WIRING — NO SCHEMA CHANGE, VALUE-LEVEL SHIFT`.
**Commits:** `9f3135a` (wiring + tests + math note + MIGRATION + AGENT_STATE), `fe5d5ea` (math note
§ 8 verified line map). **Tag `gamora/v-f8-cc-1` → `fe5d5ea`** (confirmed by `git rev-list -n1`).
**Not pushed.**

---

## 2. Acceptance-probe table — before / after

The dispatch § 3 criterion is the audit § 6 probe. **Re-executed read-only against current HEAD for
this report** (`/tmp/gamora_f8_probe_ab.py`, an extension of the audit's `/tmp/gamora_cc_probe.py`
that adds the flag ablation and the math-note § 7 rows). No engine file touched, nothing written.
BEFORE = `WIRE_HARD_CC = False`, AFTER = `WIRE_HARD_CC = True` — same binary, per Discipline #3.

Baseline displacement is `5.0 m/s × 0.1 s = 0.5000 m`.

| Arm | BEFORE action | BEFORE disp | AFTER action | AFTER disp | Matches § 7 |
|---|---|---|---|---|---|
| clean (control) | `0` | `0.5000 m` | `0` | `0.5000 m` | yes |
| **stun** | `0` | `0.5000 m` | **`None`** | **`0.0000 m`** | yes |
| **freeze** | `0` | `0.5000 m` | **`None`** | **`0.0000 m`** | yes |
| **root** | `0` | `0.5000 m` | `0` *(movement-only, by design)* | **`0.0000 m`** | yes |
| **chill only (90%)** | `0` | `0.5000 m` | `0` | **`0.0500 m`** | yes |
| **chill + decrepify(0.40)** | `0` | `0.3000 m` | `0` | **`0.0300 m`** | yes |
| **all four** | `0` | `0.5000 m` | **`None`** | **`0.0000 m`** | yes |
| **silence + offensive-only kit** | `0` | `0.5000 m` | **`None`** | `0.5000 m` | yes |
| **silence + mobility skill** | `0` | `0.5000 m` | **`1`** (the mobility index) | `0.5000 m` | yes |
| POS-CTL fear | `0`, dx `−0.6000` | `0.6000 m` | `0`, dx `−0.6000` | `0.6000 m` | **unchanged** |
| POS-CTL decrepify(0.40) | `0` | `0.3000 m` | `0` | `0.3000 m` | **unchanged** |

**Every arm matches math note § 7 exactly.** Positive controls are bit-for-bit unchanged across the
flag flip — the rig discriminates.

**Two rows deserve explicit reading, because the dispatch § 3 summary sentence
("all five CC arms must flip from `0 / 0.5000 m` to `None / 0.0000 m`") is not literally satisfiable
and should not be:**

- **`root` does not flip its action to `None`.** Root is a movement lock only, per ailment-layer
  spec § 3/§ 4 and per the kernel predicate `combatant.py:459-462` this wiring transcribes. A root
  that silenced its target would be a freeze. This divergence is declared in math note § 7 and § 2,
  pinned by `test_acceptance_root_locks_movement_but_NOT_action`, and is a **documented reading of
  the existing spec, not a wiring miss**. Its *movement* half does flip to `0.0000 m` as required.
- **`chill` lands at `0.0500 m`, not `0.05 m` "pending the composition rule".** The dispatch
  anticipated this. Per the composition rule ratified in math note § 3.1 — **successive
  multiplication, `M = σ · (1 − δ)`** — the chill-only arm is `0.5 × σ` with `σ = max(0.1, 1 − 0.90)
  = 0.10` ⇒ `0.0500 m`, and the composed arm is `0.5 × 0.10 × 0.60 = 0.0300 m`. Both measured
  exactly. The two rejected rules are falsified by the same measurement: additive would give
  `max(0, 1 − 0.90 − 0.40) = 0` ⇒ `0.0000 m` (a counterfeit root manufactured from two soft slows),
  strongest-only would give `min(0.10, 0.60) = 0.10` ⇒ `0.0500 m` (a free second slow). The measured
  `0.0300 m` discriminates all three.

---

## 3. Test status

Re-run for this report against current HEAD (`fe5d5ea`), interpreter `python3` (no venv in the repo;
`python` is not on PATH):

| Scope | Result |
|---|---|
| `tests/test_f8_hard_cc_consumer.py` (the touched test file) | **35 passed** in 0.06s |
| F8-relevant subset — the above + `test_spatial_gauntlet_scenarios.py`, `test_ailment_layer_gamora_slice.py`, `test_ailment_layer_rocket_slice.py`, `test_ailment_registry.py`, `test_wd_spatial_bc_measurement.py` | **261 passed** in 4.01s |

Green. The `9f3135a` smoke-line's broader claim (1615 passed across the spatial/fight/resolver/
combat/aura/economy/ailment/wave/commitment subset, with one pre-existing failure and 21 pre-existing
errors in `test_cycle13_wave5_season_generation.py` confirmed by stash-bisect) is **carried from the
commit message and NOT re-run in this closeout session** — treat that wider count as **UNVERIFIED
in this session**; the F8-scoped subset above is verified.

---

## 4. Blast-radius A/B

**Method:** same-binary flag ablation (`WIRE_HARD_CC` False → True) in one sequential process, per
math note § 6.1 and Discipline #3 — not a git checkout, so checkout drift is removed as a confound.
Harness: `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab.py`. Instrument is
`w4g2_tier_2_full_sim` (the blessed tier-2 direct call). Two kits: **control** (config idx 27,
4 CC effects) and **baseline** (config idx 24, 0 CC effects) — note both resolve to the same
`legendary_id` string `endgame_bc_ranged_medium_variable_int_none_t4_chain_1`, so the kits are
distinguished by config index and CC census, **not** by that label.

**Frames.** Smoke: 2 kits × 2 encounters × 2 cohorts × 2 seeds = **16 cells/arm**, 20 fights/cell.
Full: 2 kits × 4 encounters × 2 cohorts × 4 seeds = **64 cells/arm**, 20 fights/cell.
Cohorts `DPS-min-maxer`, `Balanced`. `seed_base = 8100000`.
Encounter→shell (full): `…melee_high_flat_dex_none`→`open_arena`,
`…ranged_high_flat_dex_none`→`chokepoint_corridor`, `…mid_low_spiky_int_none`→`magic_pack`,
`…melee_high_flat_int_none`→`elite_pack`.

**Provenance nit:** both JSONs record `engine_head = 70c1d4d089b49fd2de83b08904ee31877a272d27` — the
commit *preceding* `9f3135a`. The A/B was run from the working tree before the wiring was committed.
Both arms share that binary, so the ablation is internally valid; the recorded head simply does not
equal the tagged commit. Stated, not glossed.

### 4.1 Full frame (`2026-07-25-f8-blast-radius-ab-full.json`) — numbers verbatim

`n_cells 64`, `n_byte_identical 56`.

| Kit | cells | byte-identical | observed_kpm pre → post | Δ% | mean_duration_s pre → post | Δ% | mean_player_damage_dealt Δ% | survival_rate Δ |
|---|---|---|---|---|---|---|---|---|
| **baseline** (0 CC) | 32 | **32** | 75.817887 → 75.817887 | **0.0000%** | 40.484063 → 40.484063 | **0.0000%** | **0.0000%** | 0.0 |
| **control** (4 CC) | 32 | **24** | 77.160808 → 76.447679 | **−0.9242%** | 39.331094 → 40.664687 | **+3.3907%** | **0.0000%** | 0.0 |

Per-shell, control kit:

| Shell | cells | identical | kpm pre → post | Δ% | duration pre → post | Δ% |
|---|---|---|---|---|---|---|
| `open_arena` | 8 | 8 | 27.350217 → 27.350217 | 0.0000% | 87.7644 → 87.7644 | 0.0000% |
| `chokepoint_corridor` | 8 | 8 | 72.000000 → 72.000000 | 0.0000% | 20.0000 → 20.0000 | 0.0000% |
| `elite_pack` | 8 | 8 | 180.000000 → 180.000000 | 0.0000% | 0.4000 → 0.4000 | 0.0000% |
| **`magic_pack`** | 8 | **0** | **29.293016 → 26.440500** | **−9.7379%** | **49.1600 → 54.4944** | **+10.8510%** |

Baseline kit per shell: `open_arena` 8/8, `chokepoint_corridor` 8/8, `elite_pack` 8/8,
`magic_pack` **8/8** identical — all `0.0000%`.

The 8 moving cells, all `control` × `endgame_bc_mid_low_spiky_int_none` × `magic_pack`:

| cohort | seed | kpm pre → post | Δ% | duration pre → post |
|---|---|---|---|---|
| Balanced | 8121000 | 29.268293 → 26.167545 | −10.5942% | 49.200 → 55.030 |
| Balanced | 8121001 | 29.459902 → 27.673681 | −6.0632% | 48.880 → 52.035 |
| Balanced | 8121002 | 29.459902 → 26.808154 | −9.0012% | 48.880 → 53.715 |
| Balanced | 8121003 | 29.459902 → 25.955299 | −11.8962% | 48.880 → 55.480 |
| DPS-min-maxer | 8120000 | 29.173420 → 26.858155 | −7.9362% | 49.360 → 53.615 |
| DPS-min-maxer | 8120001 | 28.985507 → 26.463291 | −8.7016% | 49.680 → 54.415 |
| DPS-min-maxer | 8120002 | 29.363785 → 25.358810 | **−13.6392%** (worst) | 49.040 → 56.785 |
| DPS-min-maxer | 8120003 | 29.173420 → 26.239067 | −10.0583% | 49.360 → 54.880 |

**Direction is uniform:** all 8 movers are slower (kpm down, duration up). No cell moved the other
way. `mean_player_damage_dealt` is `0.0000%` for both kits — **the player's damage output did not
change; only the pacing did.** `survival_rate` is 1.0 pre and post everywhere, and every cell
terminates `b_dead: 20` in both arms — **no termination-reason class flipped**.

### 4.2 Smoke frame (`…-smoke.json`) — corroborates

`n_cells 16`, `n_byte_identical 12`. Baseline 8/8 identical, `0.0000%` on every metric. Control
4/8 identical, aggregate kpm `28.309043 → 26.855873` (**−5.1332%**), duration `68.5775 → 71.281875`
(**+3.9435%**), `mean_player_damage_dealt` `0.0000%`. All 4 movers in `magic_pack`: shell aggregate
**−9.8883% kpm / +11.0383% duration**, worst cell −12.2952% (Balanced, seed 8111001). The smoke
per-shell magnitude (−9.89% / +11.04%) reproduces the full frame's (−9.74% / +10.85%) to within
0.2 pp — the effect is stable across frame size.

### 4.3 Which historical verdict classes need an asterisk

**KPM band verdicts: none, in this frame.** The `magic_pack` band is `(12.52, 102.86)` for all four
cohorts (`gauntlet_sim.py:504`, R3a step-6 density-anchored re-derivation 2026-07-08). All 16 mover
values (8 pre, 8 post) range `25.358810 … 29.459902` — **every one interior to the band**. No
pass/fail flip.

> **Caveat, stated because it matters:** `w4g2_tier_2_full_sim` returns an `in_band` third value, and
> the harness **discards it** — neither JSON contains an `in_band` field (`grep -c in_band` = 0 on
> both). The no-flip conclusion above is **my arithmetic against the band constant read from
> `gauntlet_sim.py:504`**, not a recorded verdict field. It is a sound derivation for band membership;
> it is **not** a re-run of the full verdict function, so any verdict predicate that consults
> something other than the KPM band is **UNVERIFIED** here.

**Asterisks that ARE owed:**

1. **Comparability across 2026-07-25, for CC-bearing kits only.** Telemetry rows for kits that land
   CC are not directly comparable pre/post this change. Zero-CC kits are byte-identical (32/32
   measured) and need no asterisk. Filed in `simulation/MIGRATION.md` for star-lord; no schema
   migration to author (no column moved).
2. **The BC `control density` axis.** Pre-2026-07-25 that axis measured an emitted *property* with
   no realized *effect* — control effects moved nothing in the live loop. Any BC coordinate derived
   from control density before this change was measuring intent, not consequence. Flagged in
   MIGRATION.md; **not re-derived here** (cross-seam, and out of this dispatch's scope).
3. **Hard-CC-bearing kits: no verdict class can be asterisked or cleared, because none was
   measured.** See § 4.4.

### 4.4 What the A/B did NOT measure — the census finding

The harness took a CC census over the kit pool before running. Across **66 configs**: **61 have
`cc_effects = 0`**, **5 have `cc_effects = 4`**, and the census `magnitudes` dict has exactly **one
key — `chill`** — with exactly one distinct magnitude: `{"duration_seconds": 3.0, "slow_percent":
0.35}`.

Runtime instrumentation agrees. Full-frame post arm exercise counters, verbatim:

```
nav_calls 5664356 · select_calls 1685024 · attempt:chill 14802 · landed:chill 5116
nav_slowed 12180 · attempt:burn 14919 · landed:burn 5009
```

There is **no `select_action_locked` key and no `nav_move_locked` key**. The harness's `bump()`
creates a key only on first increment, so their absence is a hard zero: across 5.66 M navigate calls
and 1.69 M selector calls, **the action lock fired zero times and the movement lock fired zero
times.** The only F8 consumer that fired is the chill slow (`nav_slowed = 12180`). Smoke frame
matches: `nav_slowed = 7424`, same two keys absent.

Consequences, stated plainly:

- The **entire measured blast radius in § 4.1 is the soft-CC (chill) arm** — a 35%-slow, 3-second
  chill composing multiplicatively on mob movement. That is what −9.74% kpm in `magic_pack` buys.
- The **hard-CC blast radius (stun / freeze / root / silence) is UNMEASURED in-sim.** Not "small" —
  unmeasured. No stun, freeze, root or silence was ever attempted in 64 cells.
- The cause is **generation-side, not simulation-side**: the endgame kit pool sampled here emits no
  hard-CC effects. This is not a wiring defect and it is not patched here. It is the natural
  successor question to the dispatch's own routing instruction, and it belongs to rocket's seam via
  knight-rider — *do generated kits emit hard CC at all, and if not, should they?*
- **Correctness of the hard-CC path therefore rests entirely on the unit suite** (§ 2 probe + the 35
  assertions in `test_f8_hard_cc_consumer.py`), which is green and which does exercise the DR
  immunity window end-to-end through the applier and the boss resist tier. That is real evidence.
  It is not in-sim evidence.

### 4.5 A prior-session claim I could not verify

Commit `9f3135a` and the MIGRATION entry both state: *"546 of 587 chill landings (93%) hit a defender
already at hp ≤ 0"* — i.e. `_try_apply_ailment` is called post-damage with no liveness gate, so an
overkilling hit stamps the ailment onto a corpse, which is offered as the explanation for why three
of four shells show a zero delta.

**UNVERIFIED.** The harness instruments `attempt:<name>` and `landed:<name>` only
(`2026-07-25-f8-blast-radius-ab.py:137-141`); it has **no defender-liveness counter**, and neither
JSON contains the numbers 546 or 587. The claim came from an ad-hoc trace in the prior session that
was **not persisted**. The mechanism is plausible and the *shape* is consistent with the census (both
JSONs record `landed:chill` well below `attempt:chill` — full: 5116 of 14802), but the specific
93% figure cannot be reproduced from disk. It should be **re-measured before it is cited as fact**,
and it should not be treated as ratified by Gate 2 on the strength of the commit message alone.

---

## 5. Player-side verdict

The dispatch § 1.3 required the player-side consumer status be verified and wired, not assumed.
Commit `9f3135a` claims the action-lock selector covers both actors. **Verified independently for
this report, by reading the committed file:**

- `_select_skill_for_entity` is **defined once**, at `:2066`, with the F8 action lock at `:2109`.
- It has **exactly two production call sites**: `:4369` — the player action phase, called as
  `_select_skill_for_entity(self.player, alive_mobs, elapsed, policy_config=…)` — and `:4564`, the
  mob action phase, called as `_select_skill_for_entity(mob, mob_targets, elapsed)`.
- Therefore **the action lock and the per-skill silence gate are free on the player side**: one
  function, two callers, one gate. A stunned or frozen player selects no action, exactly as a mob
  does. Confirmed by `test_player_action_lock_is_shared_with_mobs`.

**Movement was NOT free and had to be wired separately.** `_navigate_entity` returns early on
`is_player` (pinned by `test_navigate_entity_still_ignores_the_player`); player movement is inline in
`run()`. The wiring composes F8 into the existing E4 commitment scalar rather than adding a parallel
gate (`:4291`, verified):

```
if _f8_move_locked(self.player):  _e4_move_scale = 0.0
else:                             _e4_move_scale *= _f8_slow_factor(self.player)   # when < 1.0
```

so `step = v · Δt · _e4_move_scale · M(player)` on a single multiplicative chain. The E4 `"rooted"`
move-policy (`0.0`) and an F8 `root` compose as `0.0 × 0 = 0` — trivially consistent.
`total_displacement` (W-D Axis-1) accrues realized post-clamp motion, so a locked player accrues zero
with no separate accounting change.

**Named scope boundary, not a silent gap:** `curse:decrepify` (δ) is **deliberately not wired
player-side**. It is Wave-D scope, not F8, and wiring it would move the W-D Axis-1 mobility
measurement outside the blast radius this dispatch was chartered to measure. Math note § 4.2 holds
the slot in the formula; when δ is wired player-side it drops into the same `M` with no
re-derivation. Reported as a follow-on, not closed.

**Player-side verdict in one line:** action lock — **shared, verified, free**. Movement lock —
**absent before, wired now, verified at `:4291`**. Player-side decrepify — **still unwired, named,
out of scope.**

---

## 6. Ladder consequence

**The L0 no-CC character constraint retires when this clears Gate 2.**

That constraint existed because the ladder could not place a CC-bearing character honestly: the
engine emitted control effects that consumed nothing, so an L0 character carrying stun or chill was
scored as though those effects were free flavor. With the consumption half wired, hard CC gates
action and movement and soft CC scales it, and a CC-bearing character can be laddered on its realized
behavior rather than its declared one.

Two conditions on that retirement, both stated rather than assumed:

1. It is **contingent on Gate 2**, not on this report.
2. The empirical support underneath it is **asymmetric** (§ 4.4). The soft-CC arm is measured in-sim
   across 64 cells. The hard-CC arm is unit-tested but has **zero in-sim exercise**, because the kit
   pool emits no hard CC. A ladder that places hard-CC characters will be the first thing to exercise
   that path in production. That is not a reason to hold the retirement; it is a reason to watch the
   first hard-CC ladder run closely, and a reason the generation-side question in § 4.4 should route.

---

## 7. Open items routed out of this dispatch

| Item | Where it goes | Why not here |
|---|---|---|
| Kit pool emits no hard CC (§ 4.4) | rocket, via knight-rider | Generation-side; simulation cannot fix what is never emitted |
| Corpse-chill / applier liveness gate (§ 4.5) | gandalf → Matt, **after re-measurement** | Application-ordering, pre-dates this dispatch, semantic shift needing design authority; and the 93% figure is currently UNVERIFIED |
| Whether a combined slow floor should exist (math note § 3.3) | gandalf / Matt | Introducing one is a balance decision without design authority; `M_min = 0.06` is stated as a derived consequence, not clamped |
| Player-side `curse:decrepify` (§ 5, math note § 4.2) | Wave-D follow-on | Not F8 scope |
| `SpawnSpec.is_boss → CombatantState.is_boss` (math note § 5) | cross-seam pass | Pre-existing; the boss resist tier is inert until the flag is populated. Consumer is correct either way |
| `Paralyze` / `Trapped` / `KnockedDown` / `Confused`; F9 mid-commitment interruption; F7 feared-mob action suppression | gandalf owes design specs; F6 displacement prerequisite for knockback | ABSENT mechanisms — dispatch explicitly excludes green-fielding them |
| BC `control density` axis re-derivation | elrond / star-lord, cross-seam | Flagged in MIGRATION.md; out of scope |

---

## 8. Artifact index

| Artifact | Path |
|---|---|
| Dispatch (charter) | `agentic_orchestration/dispatches/2026-07-25-gamora-f8-cc-consumer-wiring.md` |
| Math note (composition rule + § 8 line map) | `reincarnated-engine/src/reincarnated/simulation/math/f8-hard-cc-consumer-wiring-2026-07-25.md` |
| Wiring | `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` |
| Tests | `reincarnated-engine/tests/test_f8_hard_cc_consumer.py` |
| MIGRATION entry | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` |
| A/B harness | `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab.py` |
| A/B smoke result | `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab-smoke.json` |
| A/B full result | `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab-full.json` |
| Audit that seeded the spec | `agentic_orchestration/gamora/notes/2026-07-25-gd-40-state-coverage-audit.md` |
| Acceptance probe (re-run, read-only, ephemeral) | `/tmp/gamora_f8_probe_ab.py` (extends `/tmp/gamora_cc_probe.py`) |
| Gate 2 request | `agentic_orchestration/qa/pending/2026-07-25-gamora-f8-cc-wiring-gate2.md` |

**Signed:** gamora, 2026-07-25. Closeout of a session that died before it could file.
