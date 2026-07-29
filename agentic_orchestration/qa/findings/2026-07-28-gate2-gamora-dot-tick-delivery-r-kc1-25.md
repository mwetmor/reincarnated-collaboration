# Finding — 2026-07-28 — gamora DoT tick-delivery ledger (R-KC1-25)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **BLOCK**
**Target:** engine commit `3aa4a55`, tag `gamora/v-dot-delivery-1`
**Developer:** gamora (simulation seam)
**Run:** KIT-CAL-1 / KC1-2026-07-27, ratified repair R-KC1-25 (charter §14.31 footer)
**Review mandate:** MANDATORY per the ratification text — first operand-class fix on the
production-shared kernel path. Not self-clearing.
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity)
**Disciplines cited:** #1, #2, #9, #10, #11, #12

---

## §0 — Verdict in one line

The single-application repair is **correct, complete, and independently reproduced**. The
**refresh path is a regression**: under sustained re-application — the dominant production mode
for DoTs — the repaired kernel delivers **0.55–1.00** of the declared rate where the pre-fix
kernel delivered a uniform **0.992**. The `_fix2` battery is structurally blind to it (the
fixture applies its bleed exactly once per fight, 30/30). **BLOCK.**

---

## §1 — Root-cause adjudication: hers supersedes mine, plainly

I corrected her this morning; symmetric honesty requires I say this without hedging.

**Her mechanism is right and mine was incomplete.** My addendum §6 explained the shipped
3.0 s/0.1 bleed via a race between two drifting float accumulators. That explains the
*integral-duration* cells only. Her M-1 (remainder discard) is the deeper root: the ticker paid a
**continuous declaration in indivisible 1.0 s lumps**, and the sub-interval tail was never paid at
all — with **zero float error involved**. Her M-3 (over-delivery at coarse tick) is genuinely new,
opposite-signed, and not predicted by anything I wrote.

Reproduced independently against the pre-fix tree (`7483a21`, git worktree, my own harness — not
her tests):

| cell | pre-fix delivered/declared | pulses | status |
|---|---|---|---|
| **D=1.5, ts=0.25** (exact binary fraction, zero drift) | **66.7%** | 1 | **her M-1 cell — CONFIRMED** |
| D=0.5, ts=1.00 | **200.0%** | 1 | **her M-3 over-delivery — CONFIRMED** |
| D=0.3, ts=1.00 | **333.3%** | 1 | worse than her matrix records; not in her §1.1 |
| D=0.05, ts=0.1 / D=0.10, ts=0.5 | 0.0% | 0 | total loss — CONFIRMED |
| D=3.0, ts=0.1 (shipped bleed) | 66.7% | 2 | my §6 number — CONFIRMED |
| D=2.0, ts=0.1 | 50.0% | 1 | her matrix — CONFIRMED |
| D=6.37, ts=0.1 / ts=1.0 | 94.2% / 109.9% | 6 / 7 | `control_duration_bonus` band — CONFIRMED |

Her full 52-cell matrix reproduces cell-for-cell on my replication. **Her root-cause extension
supersedes my derivation.** Her two consequences also hold: the smoke arm (ts=0.5) and the full
arm (ts=0.1) were measuring different DoT totals, so the Discipline-#2 smoke gate structurally
could not catch this class; and non-integral durations are ordinary production via the
`control_duration_bonus` affix (`gear_generation.py:740`, continuous 0.5–2.0 s).

---

## §2 — The invariant: INV-1/2/3 hold for a single binding. Verified.

Post-fix, my harness (independent of `tests/test_dot_tick_delivery.py`):

- **Full 12 × 4 (duration × tick_size) matrix: 100.0% in every cell**, including all pre-fix
  0% and 200% cells.
- **Adversarial `D < tick_size`:** (0.05, 0.1), (0.10, 0.5), (0.30, 1.0), (0.50, 1.0) → all
  ratio `1.000000`, 1 pulse. Pre-fix: 0%, 0%, 333%, 200%.
- **`control_duration_bonus`-shaped non-integral durations:** 5.50, 6.37, 3.73, 5.99, 2.51 →
  all ratio `1.000000`. Pre-fix: 0.909, 0.942, 0.804, 1.002, 0.797.
- **Degenerate `D ≤ 0`:** 0.0 and −1.0 → 0 pulses, 0.0 delivered, culled on sub-tick 1. No raise.
- **INV-2 determinism:** identical pulse sub-tick indices on repeat, and **identical when three
  other effects (freeze, stun) share the combatant** — delivery does not depend on list contents.
- **INV-3 cadence:** 3.0 s bleed = 3 pulses, not 30. Battery-confirmed (§4): pulse rows went
  60→90, not 600→900, and magnitude stayed pinned at 186.3.
- **Control-layer byte-neutrality:** freeze / stun / chill / root / silence / shock / sunder /
  curse / fear / taunt / shield / buff_damage / mark:* all cull at sub-tick 24 with
  `duration_remaining` trajectory identical to pre-fix. The 8-name pin is real and the scope
  line at `_SCHEDULED_TICK_NAMES` is drawn correctly.
- **HoT:** D = 3.0 / 6.37 / 0.5-at-ts-1.0 all conserve to `1.000000`.

**Nothing to fault here.** The math note (Discipline #1, written first, `simulation/math/
dot-tick-delivery-2026-07-28.md`) is one of the better ones in the tree: it names the semantic
shifts rather than burying them, it argues INV-3 against the dispatch's literal form and is
right to, and it measured non-vacuity by stash (212 fail pre-fix) rather than asserting it
(Discipline #11).

---

## §3 — **BLOCK: the refresh phase-carry under-credits by a factor of `n_pulses`**

### §3.1 — What I measured

`_add_or_refresh` was correctly identified as the trap. The mitigation is directionally right and
**quantitatively insufficient**. Sustained re-application, 120 s fight at `ts = 0.1`,
`tick_damage = 10.0/s`, ratio = delivered / (10.0 × 120.0):

| ailment | D | reapply 0.2 s | 0.5 s | 0.8 s | 1.0 s | 1.2 s | 1.5 s |
|---|---|---|---|---|---|---|---|
| bleed | 2.0 | **0.550** | 0.667 | 0.625 | 1.000 | 0.833 | 0.667 |
| bleed / burn | 3.0 | 0.708 | 0.725 | 0.833 | 1.000 | 0.833 | **0.667** |
| burn (default) | 5.0 | 0.833 | 0.800 | 0.833 | 1.000 | 0.833 | 0.883 |
| burn + affix | 6.37 | 0.814 | 0.849 | 0.885 | 0.885 | 0.885 | 0.885 |
| drain | 4.0 | 0.767 | 0.800 | 0.833 | 1.000 | 0.833 | 0.833 |

**The same grid on the pre-fix kernel reads `0.992` in every one of the 54 cells.**

So the post-fix kernel is worse than the pre-fix kernel in 34/54 cells of the sustained-refresh
grid, by 11 to 44 percentage points, and it is worse *non-uniformly* — delivery again depends on
`(duration, reapply cadence)` in a way a designer cannot predict. **That is the same class of
defect R-KC1-25 was chartered to remove, relocated from the single-application axis to the
refresh axis, with the sign inverted.**

Worst reachable case measured (single-effect probe, not in the table above): D = 1.0 s
re-applied every 0.3 s → pre-fix 0.893, **post-fix 0.182**. Not reachable from `ailments.yaml`
minimums (lowest DoT `duration_seconds` min is 2.0), but reachable by any future DoT declaring
`D < 1.5`, and it is the limiting behaviour the mechanism below produces.

### §3.2 — Mechanism (derived, then confirmed by measurement)

At refresh, with `S` = old `sched_subticks`, `P` = old `sched_pulses`, `N = round(D'/Δ)`,
`P' = round(D'/1.0)`:

```
boundary = ceil(pulses_delivered · S / P)
phase    = subticks_elapsed − boundary        # sub-ticks accrued but unpaid
S'       = N + phase ;  e' = phase ;  pulses_delivered' = 0
next pulse at  e ≥ ceil(1 · S' / P')
⇒ time-to-next-pulse from the refresh instant
       = ceil((N + phase)/P') − phase  ≈  N/P' − phase·(P' − 1)/P'
```

An unrefreshed effect's first pulse is at `N/P'`. **The carry therefore credits only
`phase / P'` of the accrued phase and forfeits `phase · (P'−1)/P'` at every refresh.** For
`P' = 1` the credit is *exactly zero* and the pulse boundary is pushed out by the full duration
on every re-apply — total starvation while re-application continues.

Gamora's own math note §3.4 names this exact approximation in a parenthesis — *"the carry is
spread across the new schedule rather than applied only to the first interval"* — and then
concludes *"non-starving."* The parenthesis is the bug and the conclusion is falsified by
measurement. **The repair is to do what the parenthesis says: credit the phase to the FIRST
post-refresh interval only, not spread it across the schedule.**

### §3.3 — Why neither the test battery nor the `_fix2` batteries caught it

- `test_refresh_does_not_starve_the_pulse_cadence` runs **9.0 s with 6 refreshes** and asserts
  `pulses >= 8`. I measured that exact cell on both kernels: **pre-fix 8, post-fix 8.** The test
  is in the 181 that pass either way — it is **non-discriminating** for the property it names.
  Extending the same cell: 20 s → 0.950 vs 0.850; 40 s → 0.975 vs 0.875; 120 s → **0.992 vs
  0.883**. A 9-second window is a smoke-scale probe for a defect that accrues over a 120-second
  fight (Disciplines #2, #11).
- The `_fix2` batteries cannot see it **by construction**. Per-fight DoT trace-row counts on the
  W-c arm: `_fix` = `{2: 30}`, `_fix2` = `{3: 30}` — **exactly one bleed application per fight,
  never refreshed, in all 30 fights.** R3 poison routes through `_add_poison_stack` and never
  re-binds. **Refresh is exercised zero times in the entire evidence set.**

This is the same structural blindness gamora correctly diagnosed for the smoke gate, one layer
down: the fixture chosen to validate the repair is the one fixture that cannot exercise the
repaired code path.

### §3.4 — Production reachability (this is not a corner case)

`ROLE_CONSTRAINTS["primary_attack"]` (`generation/role_constraints.py:38-46`) carries
`cooldown_range=(0.0, 1.5)` and `ailment_chance=0.25`. So ~1 in 4 generated primary attacks
carries the element's signature ailment and re-applies it every 0.0–1.5 s — **precisely the band
in the §3.1 table**. `_DOT_AILMENT_NAMES = {bleed, burn, drain, poison}`; the first three route
through `_add_or_refresh`. Sustained re-application is the dominant, not the exotic, production
mode for a DoT.

---

## §4 — `_fix2` battery spot-verification: every headline number reproduces

Recomputed from the committed traces, independently of her report aggregation:

| instrument | `_fix` | `_fix2` | her claim | verdict |
|---|---|---|---|---|
| W-c bleed rows / damage | 60 / 11,178.00 | 90 / 16,767.00 | ×1.5000 | **✓ exact** |
| S-1 bleed rows / damage | 180 / 33,534.00 | 270 / 50,301.00 | ×1.5000 | **✓ exact** |
| boss mean elapsed W-c | 28.4500 | 28.4500 | "did not move at all" | **✓ exact** |
| boss mean elapsed R3 | 26.4833 | 26.0600 | — | ✓ |
| R3/W-c kill-time ratio | 0.93088 | 0.91600 | 0.9309 → 0.9160 | **✓** |
| player DoT share W-c / R3 | 0.863% / 4.770% | 1.295% / 6.215% | same | **✓ exact** |
| S-1 DoT share | 2.593% | 3.887% | ×1.5000 on damage | **✓** |
| S-1 boss win rate | 56/60 | 56/60 | unchanged | **✓** |
| total player `delivered` W-c / R3 | 1,295,220.00 | 1,295,220.00 | identical to last decimal | **✓ exact** |
| kills | 720 / 720 / 716 | 720 / 720 / 716 | — | ✓ |
| R3 poison alone (DoT − bleed) | 50,604.69 | 63,725.31 | +25.8% | **✓ (+25.93%)** |

Her §8.2a conservation finding is correct and important: `delivered` clips at remaining HP and
every mob dies, so total damage is pinned at the opposition HP pool and **can never read a DoT
lever**. Same trap as `A·B·C ≡ kills` through a second door. Kill-time and damage share are the
only live instruments. Agreed and endorsed.

**Matched seeds/flags confirmed** on all three arms: `seed_base = 74000800`, `seeds = 30`,
`run_id = KC1-2026-07-27`, `harness_version = harness-v1`, `window_id = W-c`,
`kit_id = gd-werewolf-kitcal-1` — identical `_fix` → `_fix2`. All ten `static_assertions_passed`,
plus `named_absent`, `not_recut_flags`, `insensitivity`, `grain`, `s1_control_a_summary`,
`s1_control_design`, `boss_dmg_per_hit`, `boss_dmg_sweep_declared`, `arm_a_jitter`,
`coverage_note`, `r3_arm` — **byte-identical** by JSON canonical compare. Runs sequential
(Discipline #3). 393/393 new tests pass; 263/263 kernel-adjacent regression passes.

### §4.1 — Two evidence-integrity defects found while verifying

**(a) `_fix2` is stamped with a pre-fix engine hash.** Every `_fix2` report and trace header
carries `engine_git_hash: 7483a21` — the **parent** commit. `_fix` carries `9f6805a`. Nothing in
the tree stamps `3aa4a55`. The only calibrated battery in the project is therefore
indistinguishable, by hash, from an uncalibrated one. Discipline #9 (attribution clarity).

**(b) The quarantined `kitcal_g5/` directory WAS written to.** This commit modifies
`src/reincarnated/simulation/output/kitcal_g5/smoke/kitcal_g5_smoke_report.json`
(`engine_git_hash` 9218238 → 7483a21; `elapsed_s` 27.300 → 28.800; `n_received_hits` 23 → 24;
`total_intake_pct_maxhp` 146.030 → 161.517; three `trace_path` values nulled). The commit message
states *"kitcal_g5/ and kitcal_g5_fix/ UNTOUCHED — evidence"* and the math note §8 states
`kitcal_g5/` is *"permanently quarantined … not touched."* Both are **false as committed**: a
post-fix smoke result now sits inside the directory declared to be pre-fix evidence, and it is
not labelled as post-fix. Prior content is recoverable from git, so nothing is lost — but the
directory's declared meaning is violated and the note asserts otherwise.

---

## §5 — Leech interaction (O-d door + R-KC1-20 scratch clamp): asked and answered

**Direct answer: per-pulse re-lumping does NOT change leech accounting. There is no leech on the
DoT path at all.**

- The O-d door leech block lives inside `_apply_skill_damage`'s per-hit loop
  (`spatial_engine.py:2627-2634`) and is keyed off `_delivered_this_hit` from **direct hits**.
- The DoT tick site (`spatial_engine.py:~5299`) calls `effect_resolver.tick_effects` and bridges
  only the returned damage float onto spatial HP. It makes **no** `_leech_fn` call, touches no
  `calibration_lifesteal_*` field, and adds/removes no RNG draw on that path.
- The kernel's own lifesteal (`damage_resolver.py:1253-1263`) is on the skill-resolution path,
  not the tick path, and its heal is written to the attacker scratch and discarded (census F-4).
  Unchanged here.

**But there is an indirect coupling gamora did not name, and it matters for the A/B.** Because
`delivered` is pinned at the opposition HP pool on a battery where everything dies, the DoT gain
is *exactly* offset by a direct-hit loss (W-c: DoT +5,589.0, non-DoT −5,589.0; R3: ±18,709.6).
Leech capacity and healed accumulate from direct-hit `_delivered_this_hit` **only**, so on any
arm with the O-d door open, `calibration_lifesteal_capacity` falls by `Δ_DoT × door_pct`.
**`leech_capacity_total` / `leech_healed_total` are therefore non-poolable across `_fix` and
`_fix2`, in addition to the DoT magnitudes SS-1 already names.** SS-1 should say so.

**R-KC1-20 scratch clamp interaction — one under-statement.** The repaired real `max_hp` on the
projection `CombatantState` is read by the **HoT** branch: `min(tick_heal, max_hp − hp)`.
Re-lumping changes the per-pulse *magnitude* for non-integral HoT durations, so the overheal
clamp now bites at different points. SS-2 names only the timing shift ("~1 extra pulse per
fight"); the magnitude change is a second, independent perturbation of
`bc_signals.hot_recovered` → telemetry column `a_hot_recovered` (v2.17) → **BC Axis-4 eHP regen**.
Under-stated, not wrong. HoT heals reach only scratch HP and are discarded at the seam, so no
spatial-HP exposure.

**Scope pin verified:** `_SCHEDULED_TICK_NAMES = {bleed, burn, drain, poison, heal_over_time}` —
nothing else re-lumped, confirmed empirically across 13 control/buff names in §2.

---

## §6 — Production blast radius: telemetry and season-generation consumers

- **No schema field added or changed.** No `MIGRATION.md` owed. Agreed with her call.
- **`replica_frame_emitter._ailments()` emits `remaining_s` from `duration_remaining`**, which is
  now *derived* for scheduled effects. Value trajectory changes (exact multiples of Δ; hits
  exactly 0.0 rather than a drifted residue). Emitted-field distributional shift even where
  totals match. SS-4 covers the write-invalidation contract but not the emission consequence.
- **`ReplicaFrameSink.dot()` per-pulse rows shift in both count and magnitude.** Confirmed: W-c
  60→90 rows; R3 3,150→3,182 rows with the dominant magnitude bucket moving 20.7→27.6 because
  deterministic scheduling makes co-applied poison stacks pulse on the *same* sub-tick and sum
  into one row. **Any consumer that histograms per-tick DoT magnitude reads a different
  distribution even where the sum is conserved.** She named this for R3; it should be generalised
  as a consumer notice to galadriel (replica-1 frame work) and drax (analytics).
- **Season generation:** `generation/` is untouched and no generated artifact consumes per-tick
  DoT values. Exposure is confined to simulation output.
- **SS-3 (`rng_dmgvar` stream shifts with pulse count)** is correctly named and correctly used —
  she reads the deltas as "post-repair stack vs pre-repair stack," not as DoT attribution. That
  is the honest read and I endorse it.

---

## §7 — Severity and conditions

**BLOCK.** Not because the fix is wrong — the single-application repair is right and well
evidenced — but because it ships an **opposite-signed regression on the dominant production
path**, the guard test that names that property does not discriminate, and the evidence set
cannot exercise it. Per Review Principle 5, a repair that trades a known 66.7% under-delivery for
an unknown 55–100% band on the refresh axis is not a net improvement to the production kernel and
must not be read as calibrated.

### Conditions

- **C-1 (BLOCK) — repair the phase credit.** Apply the carried intra-pulse phase to the **first
  post-refresh interval only**, not spread across the new schedule (math note §3.4's own
  parenthesis). Re-derive in the note before coding (Discipline #1).
- **C-2 (BLOCK) — a discriminating refresh test.** Replace
  `test_refresh_does_not_starve_the_pulse_cadence`. Required shape: sustained re-application over
  **≥ 120 s**, swept over `D ∈ {2.0, 3.0, 5.0, 6.37}` × `reapply ∈ {0.2, 0.5, 0.8, 1.0, 1.2,
  1.5}` s, asserting delivered / (tick_damage × window) ≈ 1.0. Measure non-vacuity by stash as
  she did for the main battery (Discipline #11) — the current test scores identically on both
  kernels and proves nothing.
- **C-3 (BLOCK) — `_fix2` is NOT final.** Re-run all three batteries after C-1 into `_fix3`.
  **Predicted (must be verified, not assumed): the G-5 headline numbers are invariant under C-1**,
  because the W-c bleed is applied exactly once per fight and R3 poison never re-binds. If that
  prediction holds, `_fix3` should reproduce §4's table cell-for-cell — which is itself the
  cleanest confirmation that C-1's blast radius is confined to the refresh path.
- **C-4 (WARN) — stamp the post-repair hash.** Battery reports and trace headers must carry the
  commit that produced them. `_fix2` currently reads `7483a21` (pre-fix).
- **C-5 (WARN) — resolve the `kitcal_g5/smoke/` overwrite.** Either restore the `9218238` content
  from git and re-point the smoke run elsewhere, or amend both the commit-message and math-note
  §8 "UNTOUCHED" claims to state what actually happened.
- **C-6 (WARN) — extend the semantic shifts.** SS-1: add O-d `leech_capacity_total` /
  `leech_healed_total` to the non-poolable list. SS-2: add the HoT per-pulse *magnitude* change
  (R-KC1-20 clamp interaction), not only the timing shift. New SS: per-tick DoT trace-row
  distribution shifts even where sums are conserved — notice to galadriel and drax.
- **C-7 (INFO) — banker's rounding.** `round()` is round-half-to-even: `round(2.5) == 2`, so a
  2.5 s DoT pays 2 pulses of 1.25 × `tick_damage`. Conserving and deterministic, so no invariant
  is violated, but the *cadence* is not what a reader of INV-3 would predict at half-integral
  durations. Worth one line in the note.

### Approval routing (ADR-002)

C-1 through C-3 are within-seam kernel changes with no consumer API change — **gamora's to
implement, mine to re-review; no Matt decision needed** unless she disputes the finding. C-5
touches banked evidence and is also in-seam. **Escalate to Matt only if:** (a) gamora argues the
refresh regression is acceptable and should ship as a named semantic shift rather than be
repaired, or (b) the C-1 repair turns out to move the G-5 headline numbers, which would make
`_fix2` non-final in substance and not merely in provenance.

---

## §8 — What I am NOT faulting

Stated explicitly so the record is not read as broader than it is:

- The integer-ledger design itself. It is the right shape and it is correct for a single binding.
- The rejection of the dispatch's literal `n_ticks = round(duration/tick_size)` form. Her INV-3
  argument is right; that form would have 10×'d trace volume and broken like-for-like.
- The `_SCHEDULED_TICK_NAMES` scope line and the 8-name control-layer pin. Verified byte-neutral
  across 13 names.
- The zero-diff cull site via derived `duration_remaining`. Verified — hits exactly 0.0.
- The single pinned-number change (DW-5, 900→1000) and her reasoning for why 251/251 held. Both
  verified: the ailment-layer DoT pins run at `ts=1.0` with integral durations, the one cell
  where the ledger and the old accumulator are arithmetically identical.
- Discipline #1, #3, #11 and #12 compliance. The math note preceded the code, runs were
  sequential, non-vacuity was measured by stash, and four semantic shifts were framed rather than
  buried. This is good practice and it is why the one gap is worth naming precisely rather than
  generally.

---

## References

**Reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py`
  (`_bind_tick_schedule`, `_pulse_due`, `_per_pulse`, `tick_effects`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py`
  (`_add_or_refresh` ledger invalidation, `_try_apply_ailment`, `_add_poison_stack`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (`ActiveEffect`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/dot-tick-delivery-2026-07-28.md`
- `/Users/admin/Games/reincarnated-engine/tests/test_dot_tick_delivery.py`
- `/Users/admin/Games/reincarnated-engine/tests/test_kitcal_g5_dot_wake.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
  (leech block ~2570-2640; tick_effects call site ~5299)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/role_constraints.py` (cooldown bands)
- `/Users/admin/Games/reincarnated-engine/config/ailments.yaml` (DoT duration ranges)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5_fix2/**`
  and `…/kitcal_g5_fix/**` (traces + reports, recomputed independently)

**Upstream:**
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-g5-dotfix-addendum.md` (my §6, now
  superseded on root cause by her M-1/M-3)
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-g5-s1control.md`

**Method note:** all pre-fix numbers in this finding were produced by running my own harness
against a detached `git worktree` at `7483a21`, then the identical harness against `3aa4a55`.
No engine file was modified; the worktree was removed after measurement (Discipline #10 —
empirical inspection over assumption).

---

# APPENDED 2026-07-28 — CORRECTION NOTE (not a silent edit)

## A-1 — §3.2's prose transposes the credit/forfeit split. Gamora is right; I concede.

Raised by gamora in `simulation/math/dot-tick-delivery-2026-07-28.md` §10.1 and re-derived by me
during the `gamora/v-dot-delivery-2` re-review.

**§3.2 as written says:** *"the carry therefore credits only `phase / P'` of the accrued phase and
forfeits `phase · (P'−1)/P'` at every refresh."* **That is backwards.**

**Re-derivation.** §3.2's own formula gives time-to-next-pulse from the refresh instant as
`⌈(N + phase)/P'⌉ − phase ≈ N/P' − phase·(P'−1)/P'`. An *unrefreshed* effect's first pulse is at
`N/P'`. The refresh therefore **advances** the pulse by `phase·(P'−1)/P'` — that quantity is the
**credit**. The **forfeit**, relative to a full `phase` credit, is `phase − phase·(P'−1)/P' = phase/P'`.

**The decisive check is §3.2's own limiting case.** At `P' = 1`:
- `credit = phase·(P'−1)/P' = 0` — matches the sentence immediately following in §3.2 ("*For `P' = 1`
  the credit is **exactly zero***") and matches the measured total starvation (0.0000 on my harness);
- `credit = phase/P' = phase` — a *full* credit, which contradicts both.

So the formula, the `P' = 1` conclusion, and every measured cell in §3.1 are all consistent with
**credit = `phase·(P'−1)/P'`, forfeit = `phase/P'`**. The labels in that one sentence are transposed.

**Scope of the error.** Prose only. §3.1's 54 measured cells, the mechanism, the production
reachability argument in §3.4, and the BLOCK itself are unaffected — all were measured, not inferred
from this sentence. Its only substantive effect is that the transposed reading **overstates**
severity at large `P'` (implying near-total forfeiture where the truth is near-full credit) and
**understates** it at `P' = 1`, which is the worst case. The finding was directionally right; that
sentence was not.

**Discipline #9 note on myself.** I shipped a derivation and a prose gloss of it that disagreed, and
did not check the gloss against the formula's own limiting case. That is the same failure mode I
BLOCKed her for — a sentence asserted past the arithmetic immediately preceding it. Recorded here
rather than corrected in place so the record shows what was claimed alongside what is true, which is
the standard she was held to under C-5.

**Verdict on this finding is superseded by:**
`agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-dot-delivery-2-rereview.md`
(BLOCK lifted → CONDITIONAL PASS at `gamora/v-dot-delivery-2`). Note in particular that **C-1's
letter was rejected by gamora with measurement, and the rejection is upheld**: the literal repair
prescribed above still reads 0.964 at Δ=0.1 and 0.708 at Δ=0.5 for D=6.37 — independently
reproduced — i.e. it reproduces this finding's own defect class one order down. C-1's *intent* is
satisfied by the shipped absolute-time carry.
