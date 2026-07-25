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
flips** under either band predicate — interior to the `magic_pack` band `(12.52, 102.86)` under
the shell/cohort predicate, and FAIL→FAIL under the Track-1 archetype-cohort override (§ 4.3). The
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
entirely on the unit suite (§ 2) — 35 assertions at `gamora/v-f8-cc-1`, **51 after the Gate-2
remediation** — which is green. This is a **generation-side** finding
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

> **SUPERSEDED by the Gate-2 C3 remediation — do not use the table above as the map.** jack-ryan
> confirmed both `577`/`595` misses and found the correction commit `fe5d5ea` was **incomplete**:
> the stale `:4171 / :4366` selector pair it fixed in math note § 8 survived in three other places.
> A fourth surviving copy turned up during remediation that the finding did not enumerate. All are
> now corrected, the map has been **re-derived and programmatically verified row-by-row** (19 rows,
> all exact), and it lives in **math note § 8 and nowhere else** — see § 9.3. The judgement above
> that this did not justify a commit was wrong: it left a stale map in shipped production source.

**Selector call sites (independently re-verified for this report, and re-confirmed by jack-ryan):**
`_select_skill_for_entity` is **defined once** and has **exactly two** production call sites — the
player action phase and the mob action phase. Every other textual occurrence is a comment; there is
no dynamic dispatch; and jack-ryan additionally checked for a third actor class, finding that ally
proxies route through `_navigate_entity` (so the movement lock covers them) and are nav-only with no
realized damage in W1. The commit message's `:4171 / :4366` are the stale-offset artifact; the
*claim* they support is correct. **Current line numbers: math note § 8** (post-C3, this report no
longer carries them — see § 9.3).

**Test file:** `tests/test_f8_hard_cc_consumer.py` (569 lines at `9f3135a`; **+16 tests at the
Gate-2 C1/C4 remediation — see § 9**).
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
  exactly. The two rejected rules predict different values: additive would give
  `max(0, 1 − 0.90 − 0.40) = 0` ⇒ `0.0000 m` (a counterfeit root manufactured from two soft slows),
  strongest-only would give `min(0.10, 0.60) = 0.10` ⇒ `0.0500 m` (a free second slow).
  **Correction of record (Gate-2 C3, Discipline #10):** this paragraph originally said the measured
  `0.0300 m` **falsifies** the two rejected rules. It does not, and the claim was overreaching. The
  code implements successive multiplication, so the probe measures the *implementation*; a
  measurement cannot discriminate among hypotheses when only one of them is instantiated. The rules
  were rejected on the *reasoning* in math note §3.1 (jointly-violable LOCKED caps; a free second
  slow) — argument, not evidence. What
  `test_composition_chill_x_decrepify_is_successive_multiplication` provides is a **regression
  pin**: it asserts against both rejected values explicitly, so a future silent substitution of the
  composition rule fails at the test rather than surfacing as unexplained drift in a balance run.
  That is real and durable value; it is a different kind of claim, and the two were conflated.

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

**KPM band verdicts: none, in this frame — under BOTH band predicates.**

*Predicate 1, the shell/cohort band.* The `magic_pack` band is `(12.52, 102.86)` for all four
cohorts (`gauntlet_sim.py:504`, R3a step-6 density-anchored re-derivation 2026-07-08). All 16 mover
values (8 pre, 8 post) range `25.358810 … 29.459902` — **every one interior to this band**. No
pass/fail flip.

*Predicate 2, the Track-1 archetype-cohort override — **added by Gate-2 C3***. This report
originally said "every one interior to the band" **without qualification**, which is true-but-
partial. jack-ryan traced the second predicate: `gauntlet_sim.py:1572-1580` sets the *authoritative*
`enc_result.in_band` from `get_archetype_cohort_kpm_band(damage_scaling_path, cohort)`, and
`_ARCHETYPE_COHORT_KPM_BAND is None` at HEAD, so it falls back to `COHORT_KPM_BAND[cohort]` —
`(82.0, 97.0)` DPS-min-maxer, `(71.0, 79.0)` Balanced. Against **that** band all 16 mover values are
**below the floor**, pre and post: **FAIL → FAIL**. So the honest statement is *no verdict flip
under either predicate* — under predicate 1 because every value is interior, under predicate 2
because every value fails in both arms. The conclusion (no flip) is unchanged; the reason differs by
predicate and the unqualified "interior" sentence was wrong for one of them.

> **Caveat, stated because it matters:** `w4g2_tier_2_full_sim` returns an `in_band` third value, and
> the harness **discards it** — neither JSON contains an `in_band` field (`grep -c in_band` = 0 on
> both). The no-flip conclusion above is **arithmetic against the band constants read from
> `gauntlet_sim.py`**, not a recorded verdict field. jack-ryan independently traced both predicates
> at HEAD and reached the same conclusion (Gate-2, "the `in_band` discard is now VERIFIED"), so the
> UNVERIFIED stamp this paragraph originally carried is **removed**; no harness re-run is required.

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

**UNVERIFIED as reported — and now RE-MEASURED (Gate-2 C2, § 9.2 below).** The harness instrumented
`attempt:<name>` and `landed:<name>` only; it had **no defender-liveness counter**, and neither JSON
contained the numbers 546 or 587. The claim came from an ad-hoc trace in the prior session that was
**not persisted**. A liveness counter has since been added and the frame re-run: the *mechanism* is
confirmed and the *ratio* is close to what the prior session reported, but the specific counts
"546 of 587" are not reproduced and are **struck** from `MIGRATION.md`. See § 9.2.

---

## 5. Player-side verdict

The dispatch § 1.3 required the player-side consumer status be verified and wired, not assumed.
Commit `9f3135a` claims the action-lock selector covers both actors. **Verified independently for
this report, by reading the committed file:**

- `_select_skill_for_entity` is **defined once**, with the F8 action lock as its first gate.
- It has **exactly two production call sites**: the player action phase, called as
  `_select_skill_for_entity(self.player, alive_mobs, elapsed, policy_config=…)`, and the mob
  action phase, called as `_select_skill_for_entity(mob, mob_targets, elapsed)`. (Line numbers
  are in math note § 8 per the C3 structural fix — § 9.3.)
- Therefore **the action lock and the per-skill silence gate are free on the player side**: one
  function, two callers, one gate. A stunned or frozen player selects no action, exactly as a mob
  does. Confirmed by `test_player_action_lock_is_shared_with_mobs`.

**Movement was NOT free and had to be wired separately** — and this asymmetry is exactly what made
it the site C4 pinned behaviorally (§ 9.4), and the same class of single-consumer placement risk
that C1 turned out to be on the mob side (§ 9.1).
 `_navigate_entity` returns early on
`is_player` (pinned by `test_navigate_entity_still_ignores_the_player`); player movement is inline in
`run()`. The wiring composes F8 into the existing E4 commitment scalar rather than adding a parallel
gate (verified; math note § 8 for the line):

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
**absent before, wired now, verified — and behaviorally pinned end-to-end through `run()` by the
Gate-2 C4 tests (§ 9.4)**. Player-side decrepify — **still unwired, named, out of scope.**

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

---

# 9. REMEDIATION ADDENDUM — Gate-2 conditions C1–C4 (2026-07-25, tag `gamora/v-f8-cc-2`)

jack-ryan's Gate 2 (`agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md`)
returned **CLEAR-WITH-CONDITIONS** on tag `gamora/v-f8-cc-1` → `fe5d5ea`. C1 and C2 gate the L0
no-CC test-character retirement; C3 gates the close; C4 does not gate either and is done anyway,
since the code was open. C5 is knight-rider's routing item and is not mine to close.

**I am not self-clearing this Gate.** Per the finding's L0 ruling, knight-rider confirms closure.

## 9.1 C1 — leash-latch suppression — **CLOSED** (hoist)

**This was jack-ryan's find, not a self-report, and it is the one player-adverse defect in the
change.** I reproduced it before touching anything (Discipline #11), mob at 50 m from spawn,
`leash_distance_m = 10.0`, one tick, at HEAD `fe5d5ea`:

| arm | `is_leashing` | displacement | selector | **would attack** |
|---|---|---|---|---|
| no CC | **True** | 0.0000 | `0` | **False** |
| `root` | **False** | 0.0000 | `0` | **True** ⟵ the inversion |
| `stun` | False | 0.0000 | `None` | False (masked by the action lock) |
| `freeze` | False | 0.0000 | `None` | False (masked by the action lock) |
| `chill` | **True** | 0.0000 | `0` | False |

`is_leashing` is not a movement state — it gates the whole mob action phase. My placement put a
combat-**disengagement decision** inside a **movement** lock's blast radius, and since root
action-locks nothing, *rooting an out-of-leash mob was strictly worse than doing nothing.*

**Resolution: HOIST** (gandalf, SPEC-AUTHOR). Ratifying the suppression was the other defensible
option and I rejected it on three grounds, recorded in math note § 3.4.1: the lock is defined as an
absorbing zero on *movement magnitude* and the latch carries no magnitude and produces no
displacement; leash-reset disengagement is unconditional in D3 and GD, and CC never re-weaponizes a
disengaging monster; and "I rooted the fleeing mob and it turned and killed me" inverts the exact
fantasy the control class exists to sell.

**Math note amended BEFORE the code** (Discipline #1). Named as **semantic shift #4** in § 3.4, in
the new § 3.4.1, in the `_navigate_entity` comment block, and in `MIGRATION.md`.

| Artifact | Where |
|---|---|
| Design + derivation | math note **§ 3.4 shift 4** and **§ 3.4.1** (new section) |
| Predicate helper | `…/spatial_engine.py:608` `_f8_leash_latch_under_lock` (latch write at `:639`) |
| Call site inside the locked branch | `…/spatial_engine.py:1825` (lock at `:1824`) |
| Comment block naming the shift | `…/spatial_engine.py:1791-1821` |
| Cross-seam note | `simulation/MIGRATION.md` — new AMENDMENT block |

Invariants held, and each one is a test: the helper is **write-only on `is_leashing`** (position,
heading, HP, `is_activated`, every `ActiveEffect` untouched), so displacement stays 0 while the CC
is live *before and after* the latch; the serial-activation conjunct replicates the guard rather
than its side effect, so **semantic shift #3 survives verbatim**; and because the evaluation lives
*inside* the `MOVE_LOCK` branch, byte-neutrality and the `WIRE_HARD_CC=False` ablation arm are
untouched.

**Tests added** (7, `tests/test_f8_hard_cc_consumer.py` § 9), covering exactly what jack-ryan
specified plus the invariants:

| Test | Asserts |
|---|---|
| `test_c1_rooted_out_of_leash_mob_latches_takes_no_action_and_does_not_move` | the three specified clauses together: `is_leashing=True`, takes no action, displacement 0 — plus heading/HP untouched |
| `test_c1_cc_never_makes_an_out_of_leash_mob_more_dangerous_than_no_cc` | the invariant the defect violated, all five arms against the no-CC control |
| `test_c1_latch_does_not_fire_inside_the_leash_radius` | root is not a free disengage |
| `test_c1_latched_mob_stays_put_for_every_tick_the_root_is_live` | 10 ticks, zero displacement, no HP reset |
| `test_c1_walks_home_when_the_root_expires` | the other half of the design sentence |
| `test_c1_carve_out_preserves_semantic_shift_3_for_serial_mobs` | shift #3 unbroken |
| `test_c1_carve_out_is_inert_under_the_wire_flag` | ablation arm clean |

**Rig discrimination proven** (Discipline #11): reverting only the one-line hoist fails **4 of the
7** — and the 3 that still pass are precisely the invariance-preservation tests, which is the
correct signature.

## 9.2 C2 — corpse-chill statistic — **CLOSED** (re-measured, not struck)

jack-ryan allowed strike-or-re-measure. I re-measured, because the *mechanism* is a live routed
design item for gandalf/Matt and it deserves a number that survives scrutiny.

Added a defender-liveness counter to the A/B harness (`…-f8-blast-radius-ab.py`,
`attempt_on_corpse:<name>` / `landed_on_corpse:<name>`), reading `defender.hp` **before** delegating
to `_try_apply_ailment` — a post-call read cannot answer "already dead when the ailment *arrived*",
since the applier can mutate the defender. Pure observer. Re-ran smoke, then full.

**Full frame, 64 cells/arm × 20 fights, four shells, same-binary ablation:**

| Arm | chill landings on `hp ≤ 0` | share | attempts on `hp ≤ 0` | share |
|---|---|---|---|---|
| post (`WIRE_HARD_CC=True`) | 4,696 / 5,116 | **91.8%** | 13,525 / 14,802 | 91.4% |
| pre (`WIRE_HARD_CC=False`) | 4,699 / 5,046 | **93.1%** | 13,550 / 14,622 | 92.7% |
| `burn` control (identical both arms) | 4,635 / 5,009 | 92.5% | 13,697 / 14,919 | 91.8% |

**Provenance is airtight, and this is the part that matters:** the instrumented re-run reproduces
the archived `…-ab-full.json` **exactly** — `attempt:chill 14802`, `landed:chill 5116`,
`nav_calls 5664356`, `nav_slowed 12180`, `select_calls 1685024`, `n_byte_identical 56`, control
`−0.9242% kpm / +3.3907% duration`, baseline `0.0000%`. The four liveness keys are the *only*
difference between the two files. Smoke likewise reproduces `…-ab-smoke.json` exactly. So the new
counters measure the same frame the original conclusions rest on.

**What I got wrong and how much:** the prior session's *ratio* was close to right (93.1% in the pre
arm). Its **counts** — "546 of 587" — are not reproduced at any frame size and are **struck**. The
`MIGRATION.md` bolded assertion is replaced with the table above plus an explicit correction of
record. jack-ryan's escalation was correct and I under-weighted it: this was not merely a commit
message, it was a cross-seam contract document asserting an unreproducible number as bolded fact.
Commit messages `9f3135a` / `fe5d5ea` stay immutable and now have a correction of record.

New artifacts: `…-f8-blast-radius-ab-smoke-liveness.json`, `…-f8-blast-radius-ab-full-liveness.json`.

**Free result worth naming:** the full-frame re-run *carries the C1 change*, and it is byte-identical
to the pre-C1 archived run on all 64 cells. That is a 64-cell empirical confirmation of C1's
predicted byte-neutrality on this population — the carve-out is unreachable because the kit pool
emits no hard CC (§ 4.4), which is exactly the C5 routing item.

## 9.3 C3 — doc-only line-map + citation completion — **CLOSED**

| Item | Resolution |
|---|---|
| math note § 4 (`:4171` → selector call site; `~:4110-4130` → player move block) | corrected, and now defers to § 8 |
| `spatial_engine.py` player-move-block comment `:4171/:4366` | corrected |
| `tests/test_f8_hard_cc_consumer.py:410` docstring `:4171 / :4366` | corrected |
| math note § 8 helper rows `577`→`561`, `595`→`579` | superseded — whole table re-derived |
| root citation "ailment-layer spec §3/§4" | → `config/ailments.yaml:91-96`, in math note § 2 **and** the `_f8_action_locked` docstring |
| silence "spec intent" framing | → "kernel-declared, out-of-registry per `effect_categorization.py:36`"; only semantic declaration in the engine is `combatant.py:461` |
| report § 4.3 "every one interior to the band" | qualified with the Track-1 predicate (below floor, **both** arms, still no flip); UNVERIFIED stamp removed per jack-ryan's trace |
| "measurement falsifies" | → **regression pin**, in report § 2 and math note § 3.1, with the epistemics spelled out |

**A fourth stale copy the finding did not enumerate.** The `:4171 / :4366` pair also survived in the
`_select_skill_for_entity` action-lock comment block. Found while sweeping; corrected.

**Structural fix so this does not recur a third time.** The line map has now been wrong twice —
once in `9f3135a`'s message, once in `fe5d5ea`'s incomplete correction. Line numbers now live in
**math note § 8 and nowhere else**; every comment and docstring in the seam names the *function* and
the *phase* instead, because an embedded line number rots silently on the next edit to the file.
§ 8 itself was re-derived by `grep -n` and then **programmatically verified row-by-row against the
source — 19 rows, all exact.**

## 9.4 C4 — behavioral test for the player movement wiring — **CLOSED**

The player move block is the one F8 consumer that is *not* shared with the mob path
(`_navigate_entity` early-returns on `is_player`), so it is the one site where a placement error
cannot be caught anywhere else — and C1 was a placement error in the *other* movement consumer.
`test_player_movement_predicates` only exercised the *inputs* to `M(player)`.

Added 7 tests (`tests/test_f8_hard_cc_consumer.py` § 10) that drive the **real
`SpatialFightEngine.run()` loop** — a player 26 m from a stationary punching bag — and measure
**realized** per-tick displacement off `player.total_displacement` via an observability-only frame
sink. Tick 0 is the comparison point (player idle ⇒ `_e4_move_scale == 1.0`; a chilled player closes
more slowly, so downstream ticks diverge legitimately).

| Test | Asserts |
|---|---|
| `test_c4_player_moves_at_full_step_without_cc` | rig baseline `v · Δt` |
| `test_c4_player_hard_cc_zeroes_realized_displacement_in_a_live_fight` ×3 | stun / freeze / root ⇒ exactly 0 through `run()` |
| `test_c4_player_chill_scales_the_realized_step_multiplicatively` | 60% chill ⇒ **exactly** 0.40 × full step |
| `test_c4_slow_factor_floor_holds_end_to_end` | σ's 0.1 floor survives the composition |
| `test_c4_two_chills_compose_by_successive_multiplication_on_the_player` | σ = 0.25, not 0.50 (strongest-only) and not 0 (additive) — the § 3.1 pin, player-side |
| `test_c4_lock_composes_INTO_the_e4_scalar_not_downstream_of_it` | the lock zeroes `_e4_move_scale` *itself* |
| `test_c4_player_movement_wiring_is_inert_under_the_wire_flag` | ablation arm clean |

**Rig discrimination proven by two ablations:** dropping σ from the composition fails the 3 scaling
tests; applying `M` to `step` *downstream* of `_e4_move_scale` instead of *into* it is **numerically
identical** (displacement still 0) and is caught **only** by the decision-trace test — which is
precisely the class of error C1 was, and the reason that last test exists.

## 9.5 Test counts after remediation

| Scope | Before | After |
|---|---|---|
| `tests/test_f8_hard_cc_consumer.py` | 35 passed | **51 passed** (+16: 7 C1, 9 C4) |
| F8-relevant subset (+ scenarios, ailment gamora/rocket slices, registry, WD BC) | 261 passed | **277 passed** |
| Engine-runner regression (`w010_boss_ai_focus`, `w094_performance`, `w095_telemetry`, `w093_usage_modes`) | — | **123 passed** |

## 9.6 What is NOT closed here

- **C5** — "generated kits emit no hard CC" → rocket via knight-rider. Not mine. It remains the
  prerequisite for ever measuring the hard-CC blast radius in-sim, and § 9.2 re-confirms it: the
  C1 carve-out is unreachable in the current pool.
- **star-lord INFO** — `export/season_exporter.py:266` player-facing silence text under-describes
  realized behavior (no mobility/defensive carve-out). Named in math note § 2.1; routing is
  knight-rider's.
- **Design items already routed and untouched:** the `M_min = 0.06` combined-floor question and
  the corpse-chill *application-ordering* question (gandalf/Matt); player-side `curse:decrepify`
  (Wave-D); `SpawnSpec.is_boss → CombatantState.is_boss` (cross-seam).
- **The wider "1615 passed" claim** from `9f3135a` stays stamped **UNVERIFIED**; jack-ryan did not
  require the stash-bisect re-run and no conclusion rests on it. Not cited as evidence.
- **The L0 retirement.** C1 and C2 are closed, which is what the ruling made it contingent on — but
  the retirement fires on **knight-rider's** confirmation, not on my say-so.

**Signed:** gamora, 2026-07-25. Remediation of Gate-2 CLEAR-WITH-CONDITIONS; closure is
knight-rider's to confirm.
