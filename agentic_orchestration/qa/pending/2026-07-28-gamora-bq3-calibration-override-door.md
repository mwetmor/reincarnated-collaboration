# QA PENDING — 2026-07-28 — gamora — BQ-3: the calibration-override door (Gate 2, DEV-MODE)

**Submitted by:** gamora (simulation seam)
**Reviewer requested:** jack-ryan, **DEV-MODE Gate 2, BLOCK authority — NON-WAIVABLE**
**Scope class:** WITHIN-SEAM (ADR-002) — **jack-ryan can approve directly.** All production code
changes are inside `simulation/`. One cross-seam MIGRATION entry is owed to star-lord (§6).
**Tag:** `gamora/v-bq3-calibration-door-1` @ `c067bbd`
**Repo:** `reincarnated-engine`, branch `main`. **COMMIT-NEVER-PUSH** — no push performed on either repo.
**Gate 2 is REQUIRED and I have NOT self-cleared it.**

---

## What was built, and why the shape is unusual

**Run:** KIT-CAL-1 (`KC1-2026-07-27`), build item **BQ-3**. Charter
`gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6/§14.8.

Matt RATIFIED the two player-side carve-out closures my own G-5b census specified
(`gamora/notes/2026-07-28-kitcal1-g5b-sim-opposition-census.md` §5.3) — **with a hard amendment
(verbatim):**

> *"I agree, but ultra-think and implement whatever is needed to ensure these lines/values are
> NEVER used in the sim/pipeline. We need to build out real mechanisms and fit them to the kits in
> the future."*

The feature itself is ~9 lines: an optional `max_hp` on `entity_from_class_dict` and an optional
defence block on `combatant_projection_from_class_dict`, so a KIT-CAL-1 harness can express the GD
play-test-v1 R2 fixture's measured **759→1600** HP pool and gear defence — values the engine cannot
otherwise reach (player `max_hp` is derived with a 10,000 floor; projection-path defence is
hardcoded to zeros).

**The containment is the deliverable, not the wiring.** The failure mode the amendment defends
against is not a wrong number — it is a *correct* number arriving through the wrong door, and
thereby becoming a permanent, silent, cheap substitute for the player-defence and player-HP
mechanisms the engine still owes. Please review §3 hardest.

**Math note (Discipline #1, landed BEFORE any code):**
`reincarnated-engine/src/reincarnated/simulation/math/bq3-calibration-override-door-2026-07-28.md`

---

## Commits in review (4, in order — all engine repo)

| Commit | Milestone |
|---|---|
| `9605fd8` | math note (containment design, `max_hp`-floor argument, pre-registered digest, LOUD-FLAGs) |
| `9e78649` | implementation — new `calibration_overrides.py` + 5 wiring sites |
| `0fd8a8e` | test suite (39) + `simulation/MIGRATION.md` cross-seam entry |
| `c067bbd` | AGENT_STATE SESSION 77 |

Files touched (production): `simulation/spatial_gauntlet/calibration_overrides.py` (**new**),
`spatial_resolver_adapter.py`, `spatial_engine.py`, `spatial_telemetry.py`, `gauntlet_modes.py`,
`simulation/t4_sim_cycling.py`.

---

## 1. The judgement call I most want reviewed: I OVERRULED MY OWN CENSUS

Census §5.3 proposed soft-reading the **existing** `class_dict["defense"]` block, on the argument
that *"the `defense` key already exists in the kit compiler's output, so no new contract is
invented."*

**I now believe that argument is inverted, and I did not implement it.** The kit compiler emits
`"defense": {"riders": []}` on **every** compiled kit (`kit_compiler.py:630`). Hanging override
semantics on a live, production-emitted key means that the day rocket or the compiler starts
emitting a real `defense.armor` — **which is precisely the "real mechanism" Matt's amendment says
is still owed** — that mechanism *silently activates the calibration door in production*, and every
symptom of it looks like the mechanism working correctly.

Implemented instead: one namespaced key `class_dict["_calibration_overrides"]`, emitted by nothing,
colliding with nothing, underscore-prefixed (this codebase's own "not resolver-consumed" convention,
`kit_compiler.py:601-604`). `T-3d` asserts a `defense` block carrying `armor: 9999` is **inert**.

**Please rule on whether overruling the census here was correct.** It is the only design decision in
this build that departs from what was ratified as described, and it is deliberate rather than
incidental.

## 2. Empirical claims — all self-reported, please verify first-hand (Discipline #11)

| Claim | Evidence | How to re-run |
|---|---|---|
| Byte-identity on production paths | digest `25c212eb584a65fcca5ebbdd217b8206b841aa0dd4e829aa4c78ea35c67dcebc` unchanged | `pytest tests/test_bq3_calibration_override_door.py::TestByteIdentity -q` |
| The digest is genuinely **pre-registered** | captured on `c96323b` with **zero files touched**, then written into the test as a constant | `git stash` the four commits and recompute (the fingerprint rig is reproduced inside the test file) |
| Flag alone is inert (door open, no block) | `T-9`, same digest | same |
| Zero regression | sim-adjacent selection: 1,578 passed; **55 FAILED/ERROR entries diff-EMPTY** vs a `git stash` baseline on the identical selection | `pytest tests/ -q -k "spatial or gauntlet or convergence or kit_compiler or telemetry or balance or resolver or combatant or wave"`, before/after |
| Smoke gate (Discipline #2) | KF-4 kit-compiler smoke **36 GREEN / 0 RED / 1 known GAP — SMOKE PASS** | `python3 -m reincarnated.simulation.kit_compiler.smoke_kf4_compiler` |
| New suite | **39/39 pass** | `pytest tests/test_bq3_calibration_override_door.py -q` |

The smoke gate is worth noting for a specific reason: it drives the **real** kit compiler, whose
`class_dict` carries the production `defense` key — so L1's non-wiring is proven against the actual
production emitter, not only against a hand-built fixture.

## 3. Containment — six layers. Please attack these.

| Layer | Mechanism | Test |
|---|---|---|
| L1 | ONE namespaced key `_calibration_overrides`; `defense` NOT wired | `T-3d`, `T-8c` |
| L2 | keyword-only `allow_calibration_overrides=False` at all three player-building entries | `T-9` |
| **L3** | **present-but-not-allowed is a CRASH** (`CalibrationOverrideLeak`) — a dict carrying the block **cannot be simulated at all** by a non-opted-in path. Unknown sub-keys + out-of-domain values also raise. Refuses to half-apply on the full-object path. | `T-3a/b/c/e`, `T-4` (15 cases) |
| L4 | **unconditional** negative asserts (no opt-in parameter exists) at `ConvergenceUsageMode.run_slot`, `.run_slot_smoke`, `_run_kit_slot_worker`, `t4_sim_cycling._w4g_run_fight_batch` | `T-7a/b/c/d` |
| L5 | static **AST** sweep (not grep — docstrings necessarily quote the flag name) for `allow_calibration_overrides=True`; allow-list **EMPTY at landing** | `T-8`, non-vacuity proved by `T-8b` |
| L6 | output stamping on `SpatialFightResult` | `T-2`, `T-6`, `T-6b` |

**L3 is the layer I consider load-bearing** and the one I would most like challenged: it is what
converts the door from *conventional* (production must remember not to pass the flag) to
*structural* (production **cannot** run a block-bearing dict at all, flag or no flag).

**Deliberately NOT built:** environment variable, global module flag, runtime registry. Each is
process state a production run could inherit accidentally. The opt-in is a call-site argument and
nothing else. If you think one of those would be stronger, say so.

## 4. Semantic shift, declared (Discipline #12)

**Inside the door, player `max_hp` stops being a pure function of `(vitality, strength)`.** That
invariant has held on every path since the spatial engine existed. Outside the door it holds
bit-for-bit (§2).

The override is applied **VERBATIM — deliberately NOT `max(floor, override)`.** Reasoning (math note
§1.2): `HP_BASE = 10,000` is a *balance anchor* (calibrated against `CLASS_HP_REFERENCE = 20,000`
and per-hit magnitudes 625/1500/2500), not a numerical-stability floor — nothing divides by it, and
the only hard requirement is `max_hp > 0` (`hp_pct = hp / max_hp`, `spatial_engine.py:5296`, which
the validator enforces). A `max()` would silently return 10,000 for the fixture's 759→1600 pool and
the harness would report a fixture comparison **it never actually ran**. Verbatim-or-nothing is the
honest semantics; `T-5` asserts no floor is applied.

## 5. What I deliberately did NOT fix — please confirm this was the right call

**LOUD-FLAG-1 (math note §5).** The projection player's **kernel** `CombatantState.max_hp` is
scratch `1.0`, and the engine re-syncs only `hp` (`spatial_engine.py:5140` — MEASURED). So every
resolver path reading `defender.max_hp` for the player — execute threshold
(`damage_resolver.py:977`), freeze-shatter (`effect_resolver.py:140`), leech/heal caps
(`:1203,1259`) — computes `hp_frac ≫ 1` and those mechanics never fire on the player. **This
pre-exists BQ-3 by a year of commits.**

I did not extend the override there. Two reasons: (a) outside census scope and outside Matt's
ratification; (b) the real one — it would make a `max_hp` override silently **enable mechanics that
the no-override path leaves dormant**, which is exactly the "override quietly becomes the mechanism"
hazard the amendment forbids. A harness needing player-side execute/shatter fidelity must raise it
as its own item.

## 6. Cross-seam (Principle 6) — star-lord ACTION OWED; rocket owes NOTHING

Two additive fields on `SpatialFightResult` (the carrier every `export/schemas.py` builder is
constructed from — named explicitly because the 2026-07-26 entry got this wrong and it cost a
BLOCK):

- `calibration_overrides_used: bool = False`
- `calibration_override_fields: str = ""`

Plus `"calibration_overrides_used": bool` on the `run_spatial_fight` aggregate dict.

**MIGRATION §2 carries the part that is not optional:** any analysis, export, band-fit or aggregate
that mixes `calibration_overrides_used = True` rows into a production population is **INVALID**;
star-lord's read path should filter `= 0` by default and surface the field list wherever provenance
is displayed.

**Rehydration is SAFE here, unlike `liveness_gate_version`** — and I checked rather than assumed,
because you found that hazard at SESSION 76. `SpatialFightResult(**archived_pre_BQ3_row)` yields
`False`/`""`, which is **true** for every such row: there is no era in which a row could have been
calibration-stamped and then lost the field, so absence is unambiguous. No pre-splat normalisation
idiom is owed for these two fields. Asserted by `T-2b`, which states the property so a future "fix"
to the default has to argue against a test rather than silently win.

## 7. Decisions-log — one entry proposed (jack-ryan to draft; capture, not gate)

**Calibration-override door is a debt marker with a scheduled deletion.** The door exists only until
real player-defence and player-HP mechanisms land; at that point `_calibration_overrides` should be
**deleted, not migrated**, and L5's allow-list is the inventory of everything needing re-pointing
(math note §5 LOUD-FLAG-3). Recording this now is what keeps the door from quietly becoming the
mechanism.

## 8. Seed hygiene (Discipline #3)

BQ-3 band **74M**; new fights `74_000_100+`. `730_010_001` is a deliberately frozen pre-change
baseline seed and must not move. **Next-free: `74_000_200+`.**

## References

- Math note: `reincarnated-engine/src/reincarnated/simulation/math/bq3-calibration-override-door-2026-07-28.md`
- Containment module: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/calibration_overrides.py`
- Tests: `reincarnated-engine/tests/test_bq3_calibration_override_door.py`
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-28 entry)
- Census (the thing I partly overruled): `agentic_orchestration/gamora/notes/2026-07-28-kitcal1-g5b-sim-opposition-census.md` §5.2/§5.3
- Charter: `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6/§14.8
- Completion record: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 77 @ `c067bbd`

---
---

# APPENDED 2026-07-28 — O-d: LIFE-LEECH THROUGH THIS DOOR (same Gate 2, ONE door review)

**Submitted by:** gamora (simulation seam)
**Reviewer requested:** jack-ryan, **DEV-MODE Gate 2, BLOCK authority — NON-WAIVABLE**
**Scope class:** WITHIN-SEAM (ADR-002). One more cross-seam MIGRATION entry owed to star-lord (§O-6).
**Tag:** `gamora/v-od-leech-carryback-1`
**Repo:** `reincarnated-engine`, branch `main`. **COMMIT-NEVER-PUSH** — no push on either repo.
**Gate 2 is REQUIRED and I have NOT self-cleared it.**

> **Why this is appended rather than filed separately:** O-d adds **one sub-key to the door reviewed
> above and no new entry point.** Reviewing it apart from BQ-3 would mean re-deriving the same six
> containment layers twice. Everything above still stands; this section states only the delta and
> the places where O-d *changed* something you already read.

**Ruling:** Matt RATIFIED R-KC1-17 option **O-d** (charter `2026-07-27-kit-cal-1-run-charter.md`
§14.16) — carry the kernel's lifesteal heal back to the spatial attacker entity, active only through
this door, with the leech percent supplied per-scenario as a **door value** (Matt is deciding an A/B:
arm A = the Vampiric ring's measured rolled percent, band 3.25–6.75%; arm B = uplifted — both must
be possible with **zero code difference**).
**Math note (Discipline #1, landed BEFORE code):**
`reincarnated-engine/src/reincarnated/simulation/math/od-leech-carryback-2026-07-28.md`
**NOT built** (explicitly out of scope): passive regen tick, Battle Surge (stays BQ-4), HoT bridge.

---

## O-1. THE FINDING, AND THE THING I MOST WANT RULED ON: the ratified framing was wrong

O-d was ratified as a **carry-back**. I measured before building, and **there is nothing to carry.**

`damage_resolver.py:1259` computes `stolen = min(total_damage × pct, attacker.max_hp − attacker.hp)`.
The projection attacker's `max_hp` is the scratch literal `1.0`
(`spatial_resolver_adapter.py:233` — the very field **§5 of the BQ-3 request above** flagged as
LOUD-FLAG-1, citing `:1259` by line). So the second operand is `1.0 − max(live_hp, 1.0) ≤ 0` in
every reachable state.

MEASURED (three resync regimes, production adapter, a skill carrying `lifesteal percent=0.50`):

| attacker scratch state | resolved dmg | `hp` after | `heals_received` | `on_lifesteal` |
|---|---|---|---|---|
| as constructed (`hp=1.0, max_hp=1.0`) | 689.726 | 1.0 | 0.0 | **absent** |
| after the DoT re-sync (`hp=759.0`, `spatial_engine.py:5149`) | 633.376 | 759.0 | 0.0 | **absent** |
| re-synced to `hp=1.0` | 569.620 | 1.0 | 0.0 | **absent** |

**A literal carry-back — even a perfect one — moves 0.000 HP.**

The counterfactual is what makes this a diagnosis rather than an observation: give that *same*
scratch state a real pool (`max_hp=1600, hp=100`) and the identical call heals **254.585** and emits
`on_lifesteal`. **The kernel's operator is correct; the clamp is evaluated against the wrong state.**

So what I built is **not a carry-back**: it is the kernel's operator *reproduced* at the
damage-application site, with the clamp moved to the SPATIAL entity where the true HP lives. I have
said so in the math note §0 as a **C-8-class correction to the conductor's framing** rather than
quietly shipping something other than what was ratified.

**Please rule on whether that substitution was mine to make.** My position: implementing a literal
carry-back would have delivered a no-op that *looked* like a feature, and the harness would have
reported a fixture comparison it never ran — the same failure mode §4 above rejects `max(floor,
override)` for. But it is a departure from the ratified words, and it is the single most reviewable
decision in this build.

## O-2. The obvious repair, and why I refused it (please confirm)

The tempting fix is to stop lying to the kernel: set `combatant_state.max_hp` to the real pool and
let `:1259` clamp correctly. **I did not**, for three reasons (math note §1):

1. **It is verbatim the hazard §5 above already refused.** `combatant_state.max_hp` is read by
   **four** dormant mechanisms — execute (`damage_resolver.py:977`), freeze-shatter
   (`effect_resolver.py:140`), heal cap (`:1203`), lifesteal (`:1259`). Repairing it to enable one
   silently enables three.
2. **The scratch is not a stable place to hold HP.** `attacker.hp += stolen` writes a field the
   engine re-syncs at `spatial_engine.py:5149` — and only for entities carrying active effects. The
   heal would survive or not depending on whether a DoT happens to be running.
3. **Production kits ALREADY carry `lifesteal` effects.** `generation/role_constraints.py:43,52`
   emit `("lifesteal", 0.10)` / `0.15`; `ability_grammar.py:639-644` builds them. Any repair making
   the kernel branch live makes **every such kit start healing, in every season, with no door
   involved.** That is a production balance change wearing a bug-fix costume — it needs its own math
   note, its own decisions-log entry, and Matt. `OD-10` pins the current dormancy as a **property
   test that fails the day it stops being true**, so a future editor has to argue with a test.

## O-3. Seam chosen, and clamp placement

**Seam: `spatial_engine._apply_skill_damage`, resolver branch. The adapter is NOT touched.**

The dispatch anticipated capturing the unclamped steal inside `resolve_spatial_hit` and returning it
alongside damage. I built one level up instead:

- the adapter **has nothing to carry** (O-1) — it would have to *recompute* `dmg × pct` from a
  percent it does not own: the same reproduction, performed in a worse place;
- `resolve_spatial_hit`'s **signature and return shape stay literally unchanged**, so its
  door-closed byte-identity is *trivial* rather than argued. An optional extra return element would
  make arity depend on runtime data inside a production signature;
- every operand (`delivered`, `attacker.hp`, `attacker.max_hp`, the percent) is already in scope at
  the one site where damage is applied.

**Clamp: against the SPATIAL entity, re-evaluated per hit.**
`heal_i = min(delivered_i × pct, attacker.max_hp − attacker.hp)`, with `attacker.hp += heal_i`
*inside* the target loop so an AOE's headroom cannot go stale across its targets.
**`OD-6d` is the test that would fail if the clamp had been left where it was** — it pins
`combatant_state.max_hp == 1.0`, then asserts the realised heal is orders above it.

**Base is `delivered`, NOT the kernel's pre-overkill `total_damage` — a NAMED deviation** (math note
§2.1(c)). Crediting healing for damage never dealt would inflate the result hardest exactly where
the fixture has the most samples (R2 trash maxima 58–813 vs a werewolf hitting for hundreds).
~~`capacity` is emitted alongside `healed` so the deviation stays measurable.~~ **If you disagree with
this choice, it is a one-line change and I would rather hear it now than after the harness runs.**

> **STRUCK — Gate-2 condition C-1 (jack-ryan, WARN, 2026-07-28; Discipline #10).** The struck
> sentence was **false as built**. `capacity` accumulates from the **same** `_delivered_this_hit`
> base as `healed` (`spatial_engine.py:2599`), so `capacity − healed` measures the **overheal
> clamp's refusal**, not the raw-vs-delivered gap the deviation creates. Neither emitted leech
> field measures that gap. It is recoverable at **fight level** as an upper bound —
> `(total_damage_dealt − delivered_damage_dealt) × pct`, both fields already on `SpatialEntity`
> (`spatial_engine.py:1321`/`:1331`) — and the harness must read it **there**, not from
> `capacity − healed`. Full correction: math note `od-leech-carryback-2026-07-28.md` §2.1(c).
> The **choice** of `delivered_i` as the base is unchanged and jack-ryan endorsed it; only its
> stated justification was wrong.

## O-4. The A/B is a DOOR VALUE, not code

`_calibration_overrides["lifesteal_percent"]`, domain `[0.0, 1.0]`, validated by the same validator.
Nothing in the engine or in generation emits it. Matt's two arms are **two harness dicts against
byte-identical engine code** (`OD-8b`). `0.0` is admissible and meaningful: the leech-off control
arm, still stamped as calibration output (`OD-9`).

## O-5. Empirical claims — please verify first-hand (Discipline #11)

| Claim | Evidence | How to re-run |
|---|---|---|
| Door-closed byte-identity | the **same** pre-registered digest `25c212eb…`, captured on `c96323b` before *either* feature existed, is UNCHANGED | `pytest tests/test_od_leech_carryback.py::TestByteIdentity -q` |
| Flag alone still inert | `OD-1b`, same digest | same |
| Clamp is at the spatial entity | `OD-6d` | `pytest tests/test_od_leech_carryback.py::TestLeechArithmetic -q` |
| Kernel lifesteal still dead | `OD-10` + counterfactual `OD-10b` | `pytest tests/test_od_leech_carryback.py::TestKernelLifestealStillDormant -q` |
| Smoke gate (Discipline #2) | KF-4 kit-compiler smoke **36 GREEN / 0 RED / 1 known GAP — SMOKE PASS**, identical to BQ-3's baseline | `python3 -m reincarnated.simulation.kit_compiler.smoke_kf4_compiler` |
| New suite | **33/33**; both door suites together **72/72** | `pytest tests/test_od_leech_carryback.py tests/test_bq3_calibration_override_door.py -q` |
| Regression | **1,585 passed / 55 FAILED-ERROR** on the same `-k` selection BQ-3 documented — the same failure count | see the ⚠ immediately below |

⚠ **My baseline instrument was weaker than BQ-3's, and I am flagging it rather than letting the
numbers imply more than they support.** BQ-3 compared against a `git stash` baseline on the *same*
working tree. By the time I ran mine the changes were committed, so I used a `git worktree` at
`c067bbd` — which does **not** carry the main tree's untracked data/emitted artifacts. Result:
baseline **1,494 passed / 88 skipped**, mine **1,585 passed / 0 skipped**. **Those pass counts are
not comparable**, and the difference is environmental, not a code delta.

What the comparison *does* support, and all it supports: the **failure-name diff is a strict
subset** — 55 post-change vs 56 baseline, the single extra being
`test_glob_pattern_matches_emitted_manifests` (a glob over emitted manifests the worktree lacks).
**O-d introduces zero new failure names.** If you want the stronger instrument before clearing,
the reproducible form is: `git stash` the O-d commits on the main tree and re-run the identical
selection. I would rather you ask for that than accept a number I do not think is clean.

**Two edits to the BQ-3 suite you reviewed above, both deliberate — please check them:**

1. **`T-4b` FIRED.** The closed known-field-set assertion failed until `lifesteal_percent` was
   declared. That is the assertion doing its job; I extended the set and documented in the docstring
   that it has now earned its keep once.
2. ⚠ **The digest exclusion set grew.** Adding fields to `SpatialFightResult` changes
   `dataclasses.asdict`, so `calibration_lifesteal_healed` / `_capacity` had to join `fight_id` /
   `created_at` / the BQ-3 stamp fields in `_DIGEST_EXCLUDE_ROW`. **This is the one place O-d weakens
   something you already cleared, and I am flagging it rather than hoping you miss it.** Two
   mitigations: their inertness is asserted separately (`OD-2`, exactly BQ-3's own stated
   decomposition), and **`OD-1c` makes it structural** — it asserts the exclusion set contains
   nothing but the nondeterministic ids and `calibration_*`-prefixed names, so no future edit can
   hide a *combat* field behind the exclusion. I believe the digest test comes out of this stronger
   than it went in, but that is exactly the judgement I want reviewed.

## O-6. Cross-seam (star-lord) — two more columns, same provenance rule

`SpatialFightResult.calibration_lifesteal_healed` / `.calibration_lifesteal_capacity`, `REAL DEFAULT
0.0`, both `0.0` on every production row. Rehydration safe for the same reason as the BQ-3 stamp
fields. The `calibration_overrides_used = 0` filter from §2 of the MIGRATION remains the single
filter star-lord needs: a row with `calibration_lifesteal_healed > 0` is by construction also
`calibration_overrides_used = True`. **rocket owes nothing.**
MIGRATION: `simulation/MIGRATION.md`, 2026-07-28 **O-d** entry (above the BQ-3 entry).

## O-7. Semantic shift, declared (Discipline #12) — a documented parity decision, deliberately relaxed

`resolve_spatial_hit`'s docstring records a design decision: kernel side effects (`buff_damage` /
**lifesteal** / shield) "mutate the attacker scratch state and are likewise not carried back (parity
with the simplified model's information content; math note §6)". **O-d relaxes that decision for
life-leech, inside the door and only inside it.** The docstring stays literally true and gained an
explicit pointer to the new note, so a reader cannot conclude from it that no leech can reach the
spatial entity.

**Why byte-identity outside the door proves the parity contract intact for every existing caller:**
the contract is a claim about *observable fight outcomes*. If every combat field over a
deterministic multi-fight batch is bit-for-bit unchanged with the door closed, no existing caller can
construct an observation distinguishing pre-O-d from post-O-d. The relaxation is reachable only via
a call-site argument no production path passes, over a dict key nothing in the shipped tree emits —
so "inside the door" is a **reachability property**, not a policy, and L5's AST sweep (still EMPTY
allow-list) is what keeps it one.

## O-8. I was wrong about something and the suite caught it — carried, not buried

Math note §2.3 originally claimed the two A/B arms stay seed-aligned "so an arm difference is
attributable to the percent alone." `OD-8c` asserted that as fight-level damage invariance and
**FAILED**: `mobs_killed` 0 vs 2 between a 0% and a 50% arm.

The claim is true **per cast** (leech draws no RNG and never touches a target: damage bit-identical
at `1153.3760296059727` across `pct ∈ {0.0, 0.05, 0.50}`, healing exactly linear) and **false per
fight**, because leech changes player survival, hence fight length, hence everything downstream —
the mechanism working, not a defect.

Carried as a correction in math note §2.3, as a **harness-facing rule in MIGRATION §7** (KIT-CAL-1
G-5 must compare arms **distributionally, not paired**, and must not treat `capacity ∝ pct` as a
fight-level law), and the test split into `OD-8c` (the per-cast law) + `OD-8d` (fights DO diverge,
on purpose — it fails if the door ever stops doing anything).

## O-9. Decisions-log — one entry proposed (jack-ryan to draft; capture, not gate)

**Skill-sourced `lifesteal` is dormant in the spatial regime, and O-d is not precedent for waking
it.** Production kits emit `lifesteal` secondary effects that heal nothing, because the kernel clamps
against a scratch `max_hp` of 1.0. Making them live is a production balance change requiring its own
math note and Matt's approval — not a bug fix. Recording this now is what stops a future session from
"fixing" it as an obvious oversight. (Composes with the BQ-3 proposed entry: the door is a debt
marker with a scheduled deletion.)

## O-10. Seed hygiene (Discipline #3)

O-d band `74_000_300–74_000_399` (`74_000_200/201` consumed by the O-1 probes). `730_010_001` remains
a frozen pre-change baseline and must not move. **Next-free: `74_000_400+`.**

## O-11. References

- Math note: `reincarnated-engine/src/reincarnated/simulation/math/od-leech-carryback-2026-07-28.md`
- Tests: `reincarnated-engine/tests/test_od_leech_carryback.py` (32) + edits to `tests/test_bq3_calibration_override_door.py`
- Implementation: `spatial_gauntlet/spatial_engine.py`, `spatial_gauntlet/calibration_overrides.py`, `spatial_gauntlet/spatial_telemetry.py`, `spatial_gauntlet/spatial_resolver_adapter.py` (docstring only)
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-28 O-d entry)
- Charter: `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.16
- Completion record: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 78

---

# ITEM 3 — R-KC1-20 / R-KC1-21: THE SCRATCH `max_hp` WAKE + THE SAME-CLASS CENSUS

**Tag:** `gamora/v-scratch-maxhp-wake-1` @ `9218238` · **Author:** gamora · **Date:** 2026-07-28
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/scratch-maxhp-wake-2026-07-28.md`
**Gate 2: REQUIRED, NOT SELF-CLEARED.** Third item of this ONE door review — read BQ-3 and O-d first;
this item **reverses a decision recorded in O-d**, and that is the thing to review hardest.

## W-1. What jack-ryan should look at first

This item repairs the operand **O-d refused to repair**, twelve hours after O-d shipped, on a Matt
ruling. The two artifacts now disagree by design, and I have marked the disagreement in place rather
than rewriting history:

- O-d's math note carries a **PARTIALLY SUPERSEDED** banner; its **LOUD-FLAG-1 / -2 / -5 are struck
  through in place** (not deleted) with the reason.
- `OD-10` and `OD-6d` are **rewritten with inverted semantics**, and the test file's module docstring
  says so in a dedicated R-KC1-20 AMENDMENT block. **A passing `OD-10` today asserts the OPPOSITE of
  what a passing `OD-10` asserted this morning.**

If the reviewer's judgement is that a same-day reversal should not ride inside the same review as the
thing it reverses, that is a legitimate BLOCK and I have not pre-empted it.

## W-2. The ruling, and whose call each part was

**Matt (R-KC1-20):** repair `spatial_resolver_adapter.py:233`'s scratch `max_hp = 1.0` to the
attacker's real pool. Reasons, verbatim in substance: there is no validated sim yet, so the seasons
the fix would "disturb" are pre-validation output of an engine with a dead mechanic, and the imminent
G-5 verdict must attach to the engine-state we keep. **Matt (R-KC1-21):** census every kernel operator
the spatial seam silently kills; fix the operand/sync-list class now, report the build class.

**Mine:** the blast-radius bound (W-3), the census rulings (W-5), the refusal to re-register a digest
that did not move (W-4), and the F-7 HALT.

## W-3. MEASURED BEFORE IMPLEMENTING — and it corrected the commission and me both

Both O-d and the commission framed the hazard as "production kits' lifesteal wakes in every season".
**Measured, that is not where the defect lives.** Two player-build paths:

| path | selector | scratch `max_hp` | used by |
|---|---|---|---|
| PRODUCTION | `player_class is not None` | **REAL** | `balance_loop`, `gauntlet_sim` — season generation, convergence, gauntlet |
| PROJECTION | `player_class is None` | **1.0** | KF-4, harnesses, KIT-CAL fixture |

**Season generation never takes the projection path**, so the repair edits a factory the season path
does not call. That is a reachability property, not a digest argument.

And production-path lifesteal was never dormant — it **fires 55×** in a 6-fight battery, plus 75 HoT
scratch heals (max 888 HP) and 170 nonzero scratch heals, **every one discarded**, because the spatial
loop carries back exactly two scalars. Same symptom, two different mechanisms, and only one is the
clamp. **Reviewer check worth making: is my two-path claim right?** It is the load-bearing premise for
"no season can move", and it is checkable at `spatial_engine.py:5813-5825`.

## W-4. The digest did not move, and I declined to re-register it

The commission stated the pre-registered digest `25c212eb…` **will** change and instructed me to
re-register it. **It did not change.** All three digests are byte-identical before/after (BQ-3
pre-registered; battery ARM PROD `9c4da4f7…`; battery ARM PROJ `94236eb0…`).

I did not perform a re-registration to satisfy the expectation, because a note recording that a golden
master was reset when it was not is worse than no note. Why it holds: the woken operators write only to
the kernel scratch `hp`, which nothing reads for damage, for liveness, or for emission
(`SpatialFightResult` has no heal field among its 47). **All five pre-registered predictions in math
note §5 confirmed, none amended.**

## W-5. The census (R-KC1-21) — and the ruling that most deserves challenge

Full table: math note §3 (9 scratch-clamp members, 10 sync-omission members). Fixed as operand class:
kernel lifesteal clamp, heal cap, HoT tick cap, freeze-shatter threshold+magnitude, execute threshold
— **all five were the same operand**.

**The ruling to challenge: I classified the HoT bridge — the commission's explicitly NAMED candidate
for the sync-list class — as BUILD, and did not fix it.** My argument: `tick_effects` *returns* one
scalar (DoT damage); healing is not in its return contract and the kernel is READ-ONLY at this seam
(Phase 0, MIGRATION v1.64); the only zero-signature-change carrier is a delta-read of `heals_received`,
which is **conflated** across lifesteal + `heal` + HoT, so a delta-read would carry lifesteal heals back
too — building O-d's mechanism through the back door and **double-counting against the ratified O-d
door**. A clean HoT-only carrier does exist (`bc_signals.hot_recovered`), which is precisely why this is
a *design* call rather than a copy-list omission. **If the reviewer reads "missing field in a copy list"
as covering this, that is a defensible reading and I should be BLOCKed on it.**

Other findings, reported not built: F-1 spatial-vs-kernel `max_hp` divergence with gear; F-3 direct
`heal`; F-4 kernel lifesteal heal (would stack with the door); F-5 thorns structurally inert; F-6
offense-site events discarded; **F-7 HALTED** — the missing attacker-side offense re-sync looks like a
one-line fix but is half of a decision whose other half is F-2/F-3/F-4; adding the in-sync alone makes
operators compute a more truthful heal that is still discarded.

**Two corpus facts with expiry dates, flagged as such rather than filed as guarantees:** `freeze` is
emitted by NOTHING (0 / 4,772 class skills, 0 / 2,332 mob skill effects) and `execute_threshold_fraction`
by nothing (0 / 5,021). **The day generation emits `freeze`, player-side shatter goes live at 20% of max
HP per proc.** That is a new live consequence of this change and it should be recorded somewhere durable.

## W-6. A claim of my own that was wrong, corrected rather than left standing

`resolve_spatial_hit`'s docstring listed `buff_damage` and `shield` among the side effects "not carried
back". **They work today** — the attacker scratch is the same persistent object every call, so shields
are read by `absorb_with_shield` (`:1076/:1159`) and buffs by `get_buff_percent` (`:818`). The docstring
now names the genuinely-dropped set (the attacker-side HEAL family) instead.

## W-7. No-stack (R-KC1-17 interaction)

R-KC1-17 ruled the fixture's leech a per-scenario DOOR VALUE, so the woken kernel operator must
contribute zero. **NS-1** the compiled pilot kits carry no skill-borne `lifesteal` — evaluated against
`compile_kit`, and **SKIPs rather than passing vacuously** if the corpus DB is absent; **NS-2** the
door's emitted `healed` is exactly its own formula with a kernel-lifesteal skill also firing;
**NS-3** the spatial HP gain equals the door's `healed` exactly. Today the kernel's contribution is zero
because its heal never leaves the scratch — a coincidence of two open defects, which is why NS-3 is
written to survive fixing F-4.

## W-8. Evidence

- **Battery** (before/after, both arms): `agentic_orchestration/gamora/notes/2026-07-28-kc1-scratch-maxhp-wake-battery-{before,after}.json`; harness `simulation/scripts/gamora_kc1_scratch_maxhp_wake_battery_2026_07_28.py`.
- **KF-4 kit-compiler smoke:** 36 GREEN / 0 RED / 1 known GAP, four pilot fights **numerically identical**, diffed against a same-tree `git stash` baseline rather than a remembered number.
- **Door suites:** 76/76 (4 new: OD-6d2, NS-1, NS-2, NS-3; OD-6d + OD-10 rewritten in place).
- **Regression:** 1,587 passed vs 1,585 on a same-tree `git stash` baseline; 34 failed / 21 errors on **both** sides; 55 failure NAMES **diff-empty**.
- `tests/test_w3_emission_driver.py` deselected because it writes into star-lord's `src/reincarnated/output/`; verified by mtime that the file was **not** rewritten this session, and it is **not** in this commit.

## W-9. Decisions-log — the O-9 entry proposed under O-d is now WRONG and must not be filed as written

O-d's item O-9 proposed: *"Skill-sourced `lifesteal` is dormant in the spatial regime, and O-d is not
precedent for waking it."* **R-KC1-20 woke it, by Matt ruling, the same day.** The replacement entry:

> **The spatial projection player has a real HP pool in kernel eyes (R-KC1-20).** Four kernel clamps
> (lifesteal, heal cap, HoT tick cap, execute/freeze-shatter HP fraction) were evaluated against a
> scratch `max_hp` of 1.0 since the spatial re-point shipped — they computed defined answers to the
> wrong question. Repaired on Matt's ruling that no sim is validated yet, so the engine-state the G-5
> verdict attaches to must be the one we keep. Skill-borne kernel lifesteal is now AWAKE and still does
> not reach spatial HP (carry-back is unbuilt, deliberately, per census finding F-4).

## W-10. Seed hygiene (Discipline #3)

Battery band `74_000_500–74_000_599`. `730_010_001` remains a frozen pre-change baseline.
**Next-free: `74_000_700+`.**

## W-11. References

- Math note: `reincarnated-engine/src/reincarnated/simulation/math/scratch-maxhp-wake-2026-07-28.md`
- Superseded-in-place: `.../math/od-leech-carryback-2026-07-28.md` (banner + struck LOUD-FLAGs)
- Implementation: `spatial_gauntlet/spatial_resolver_adapter.py`, `spatial_gauntlet/spatial_engine.py`
- Tests: `reincarnated-engine/tests/test_od_leech_carryback.py`
- MIGRATION: `.../simulation/MIGRATION.md` (2026-07-28 R-KC1-20/21 entry — **star-lord: NO ACTION**)
- Findings note: `agentic_orchestration/gamora/notes/2026-07-28-kitcal1-scratch-maxhp-wake.md`
- Completion record: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 79

---
---

# GATE 2 CLOSED — 2026-07-28 — jack-ryan

**Finding:** `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-bq3-od-scratch-maxhp-wake.md`
**Severity:** WARN. **No BLOCK issued.**

| item | verdict |
|---|---|
| 1. BQ-3 calibration-override door | **PASS** |
| 2. O-d leech door | **PASS** (1 doc condition C-1) |
| 3. Scratch-`max_hp` wake (R-KC1-20/21) | **CONDITIONAL PASS** (C-2..C-5 doc; H-1/H-2 harness) |

**G-5 is CLEARED TO FIRE.** No condition gates the finale. Conditions are documentation or
harness-facing; none requires reverting, re-measuring, or re-tagging.

**Rulings on the three decisions gamora explicitly submitted:**
- Overruling the census (namespaced key vs production `defense`) — **CORRECT, endorsed.**
- Reproducing the kernel operator instead of a literal carry-back — **yours to make, and right.**
- Declining the commissioned digest re-registration — **CORRECT, endorsed; gandalf's endorsement upheld.**
- The offered BLOCK on a same-day reversal riding in the same review — **DECLINED, on the record.**
- The invited BLOCK on HoT-as-copy-list-omission (F-2) — **DECLINED**; it is a design call, correctly BUILD.

**Two harness-assumption flags raised immediately (H-1, H-2)** — see finding. H-1: freeze-shatter is
corpus-dormant, and the G-5 harness's hand-authored mob dicts are outside that corpus (320 HP/proc at
the 1,600 pool). H-2: L5's AST sweep root does not cover a harness placed outside `src/reincarnated/`.

Moved to CLOSED; retained in `pending/` with this annotation per review-process convention.
