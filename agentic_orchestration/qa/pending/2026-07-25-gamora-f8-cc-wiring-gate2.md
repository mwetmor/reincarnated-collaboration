# GATE 2 REQUEST — gamora: F8 hard-CC consumer wiring

**From:** gamora (simulation seam)
**To:** jack-ryan (Gate 2, DEV-MODE, BLOCK authority)
**Date filed:** 2026-07-25
**Status:** **REVIEWED 2026-07-25 — CLEAR-WITH-CONDITIONS (jack-ryan).** Finding:
`agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md`.
Conditions C1 (leash-latch suppression under root — NEW, not self-reported) and C2 (strike the
unverifiable 546/587 statistic from `MIGRATION.md:50`) **gate the L0 no-CC retirement**; C3 (complete
the line-map correction) gates close; C4/C5 are follow-ons. Composition rule, silence hoist,
shared-selector coverage, and root's movement-only semantics all CLEAR. The `in_band` discard is
**closed as VERIFIED** — no verdict flip under either band predicate. Tests reproduced (35 / 261).
**Gate 2 was pre-registered in the dispatch** — this is not an after-the-fact request.

**Dispatch (charter):** `agentic_orchestration/dispatches/2026-07-25-gamora-f8-cc-consumer-wiring.md`
(gandalf SPEC-AUTHOR), under Matt ruling 2026-07-25:
> *"We ARE building all mechanics needed into our engine. If we don't yet have CC in the sim, then we
> build it in — we don't work around it."*

**Full report (the evidence this request summarizes):**
`agentic_orchestration/gamora/notes/2026-07-25-f8-cc-wiring-and-blast-radius.md`

**Filing note:** the build and the A/B ran in a prior gamora session that died on a stream timeout
before it could file. This request is a closeout. Every claim below was re-verified from disk or
re-executed in the closeout session; claims that could not be are marked **UNVERIFIED** in-line.

---

## 1. What was built

The **consumption half** of the hard-CC stack, wired into the live loop (`run_spatial_fight` path).

The application half has been complete since Wave-C/Wave-D — effect registry (`damage_resolver.py:62`),
DR immunity windows (`effect_resolver.py:158-164`), boss resist tier (`damage_resolver.py:1650`),
refresh law, state predicates (`combatant.py:395-424`). The consumption half existed **only** on
`CombatantState.can_use_skill` (`combatant.py:459`) — a code path with **zero production callers**.
Before this change, a mob in the live loop carrying live `stun + freeze + root + 90% chill` selected
skill index 0 and moved its full per-tick distance.

Three gates were added, all in
`src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`:

1. **Action lock** — `freeze ∨ stun ⇒ no action selected`, in `_select_skill_for_entity` (`:2109`).
2. **Silence** — per-skill role gate (`mobility` / `defensive` still selectable), hoisted once per
   selector call (`:2135`).
3. **Movement lock + slow composition** — `freeze ∨ stun ∨ root ⇒ zero displacement`; `chill ⇒ σ`
   applied multiplicatively; in `_navigate_entity` (`:1770`, `:1877`, `:1978`) for mobs and in the
   inline `run()` player move block (`:4291`) for the player.

Gated by `WIRE_HARD_CC: bool = True` (`:700`) — **default ON, which is what "build it in" means**.
The flag exists for the same-binary A/B ablation and for forced-off regression tests, precedent
`WIRE_WAVEC_*` / `WIRE_COMMITMENT_AXIS`.

**Explicitly NOT built** (dispatch § 1 excludes them): `Paralyze` / `Trapped` / `KnockedDown` /
`Confused` as new mechanisms; knockback (needs the F6 shared-displacement prerequisite); F9
mid-commitment interruption (v1-locked OFF); F7 feared-mob action suppression. No green-fielding.

---

## 2. Commits, tag, and paths

| Item | Value |
|---|---|
| Repo | `~/Games/reincarnated-engine`, branch `main` |
| Commit 1 | `9f3135a` — *"F8 hard-CC consumer wiring — the mechanism was built and unwired; now it is wired"* (spatial_engine.py +198, tests +569, math note +299, MIGRATION.md +51, AGENT_STATE.md) |
| Commit 2 | `fe5d5ea` — *"F8 math note §8 — verified wiring line map, correcting my own commit message"* (docs only, +27/−1) |
| Tag | `gamora/v-f8-cc-1` → **`fe5d5ea`** (verified via `git rev-list -n1`) |
| Pushed? | **No.** Push awaits Matt per ADR-006. |
| Math note | `src/reincarnated/simulation/math/f8-hard-cc-consumer-wiring-2026-07-25.md` |
| Tests | `tests/test_f8_hard_cc_consumer.py` |
| MIGRATION | `src/reincarnated/simulation/MIGRATION.md` — entry `[2026-07-25] F8 HARD-CC CONSUMER WIRING — NO SCHEMA CHANGE, VALUE-LEVEL SHIFT` |
| Report | `agentic_orchestration/gamora/notes/2026-07-25-f8-cc-wiring-and-blast-radius.md` |
| A/B harness + results | `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab{.py,-smoke.json,-full.json}` |

**Read `fe5d5ea` before `9f3135a`.** Commit `9f3135a`'s message cites the wiring sites with
**pre-implementation estimated line numbers** (`:626`, `:531`, `:2035`, `:1736`, `:1794`, `:1897`,
`:4295`, and call sites `:4171`/`:4366`). Every **site** it names is correct; the offsets are 4–100
lines off because they were written against the file as read rather than as written. Math note § 8 is
the corrected map. Recorded as a new commit rather than an amend, per new-commit-over-amend.

---

## 3. Test status (re-run in the closeout session, against HEAD `fe5d5ea`)

Interpreter is `python3` — there is no venv in the repo and `python` is not on PATH.

```
python3 -m pytest tests/test_f8_hard_cc_consumer.py -q
  → 35 passed in 0.06s

python3 -m pytest tests/test_f8_hard_cc_consumer.py tests/test_spatial_gauntlet_scenarios.py \
    tests/test_ailment_layer_gamora_slice.py tests/test_ailment_layer_rocket_slice.py \
    tests/test_ailment_registry.py tests/test_wd_spatial_bc_measurement.py -q
  → 261 passed in 4.01s
```

**Green.** `tests/test_f8_hard_cc_consumer.py` is the only test file the change touched; the second
command widens to the ailment + spatial suites that exercise the touched code file.

**UNVERIFIED in this session:** commit `9f3135a`'s broader smoke-line claim — *1615 passed* across
the spatial/fight/resolver/combat/aura/economy/ailment/wave/commitment subset, with one failure
(`test_wave5_swift_closure_path_x_phase4_feeds_phase5`) and 21 errors in
`test_cycle13_wave5_season_generation.py` asserted **pre-existing** via stash-bisect. That wider run
was not repeated here. If Gate 2 wants the pre-existing classification independently confirmed, say
so and I will re-run the stash-bisect.

---

## 4. Acceptance evidence

### 4.1 The dispatch § 3 probe, re-executed read-only against HEAD, both flag arms

Same binary, `WIRE_HARD_CC` False → True (Discipline #3: no parallel regens). Baseline displacement
`5.0 m/s × 0.1 s = 0.5000 m`.

| Arm | BEFORE (flag off) | AFTER (flag on) |
|---|---|---|
| clean (control) | `0` / `0.5000 m` | `0` / `0.5000 m` |
| **stun** | `0` / `0.5000 m` | **`None` / `0.0000 m`** |
| **freeze** | `0` / `0.5000 m` | **`None` / `0.0000 m`** |
| **root** | `0` / `0.5000 m` | `0` / **`0.0000 m`** — movement-only, see § 5.1 |
| **chill (90%)** | `0` / `0.5000 m` | `0` / **`0.0500 m`** |
| **chill + decrepify(0.40)** | `0` / `0.3000 m` | `0` / **`0.0300 m`** |
| **all four** | `0` / `0.5000 m` | **`None` / `0.0000 m`** |
| **silence, offensive-only kit** | `0` / `0.5000 m` | **`None`** / `0.5000 m` |
| **silence, kit with a mobility skill** | `0` / `0.5000 m` | **`1`** (the mobility index) / `0.5000 m` |
| POS-CTL fear | `0`, dx `−0.6000` | `0`, dx `−0.6000` — **unchanged** |
| POS-CTL decrepify(0.40) | `0` / `0.3000 m` | `0` / `0.3000 m` — **unchanged** |

Every arm matches math note § 7 exactly. Positive controls bit-identical across the flip — the rig
discriminates. `test_wire_flag_off_reproduces_the_pre_wiring_audit_row` pins the BEFORE column so the
ablation cannot silently rot.

### 4.2 Blast-radius A/B — the dispatch § 2 question, answered empirically

Same-binary flag ablation via `w4g2_tier_2_full_sim`. Full frame 2 kits × 4 encounters × 2 cohorts ×
4 seeds = 64 cells/arm, 20 fights/cell.

| Kit | cells | byte-identical | observed_kpm Δ | duration Δ | damage_dealt Δ | survival Δ |
|---|---|---|---|---|---|---|
| baseline (0 CC) | 32 | **32/32** | **0.0000%** | **0.0000%** | **0.0000%** | 0.0 |
| control (4 CC) | 32 | 24/32 | **−0.9242%** | **+3.3907%** | **0.0000%** | 0.0 |

All 8 movers sit in one shell, `magic_pack`: aggregate **29.293016 → 26.440500 kpm (−9.7379%)**,
**49.1600 → 54.4944 s (+10.8510%)**, worst single cell **−13.6392%**. Direction uniform (all slower).
Smoke frame corroborates: control `magic_pack` −9.8883% kpm / +11.0383% duration, worst −12.2952%.

**No KPM band verdict flips.** `magic_pack` band is `(12.52, 102.86)` (`gauntlet_sim.py:504`); all 16
mover values span `25.358810 … 29.459902`, every one interior. **Caveat for your scrutiny:** the
harness discards the `in_band` return value and neither JSON contains it — the no-flip conclusion is
**my arithmetic against the band constant**, not a recorded verdict field. See § 5.4.

Byte-neutrality claim is narrow and was stated that way in the math note (§ 6): identical only for
entities never carrying a live `stun`/`freeze`/`root`/`silence`/`chill`. The 32/32 zero-CC result is
the specificity evidence for that claim.

### 4.3 Player-side, verified by reading the committed file (not assumed)

`_select_skill_for_entity` is defined once at `:2066` (action lock at `:2109`) and has exactly two
production call sites: **`:4369` (player)** and **`:4564` (mob)**. The action lock and silence gate
are therefore **free on the player side** — one function, two callers, one gate. Player *movement*
was not free: `_navigate_entity` returns early on `is_player`, so the movement lock was wired
separately into the inline `run()` block at `:4291`, composed into the existing `_e4_move_scale`
rather than as a parallel gate.

---

## 5. What Gate 2 should scrutinize

Five items, in the order I would review them. The first three are the ones the dispatch and the
report flag as the substantive review surface; the last two are things I found in my own work.

### 5.1 The composition rule — `M = σ · (1 − δ)`, successive multiplication

**Math note § 3.1.** The load-bearing question: *is the rule sound, and is "ratifies an existing
declaration" an honest framing or a dodge?*

My claim is that the rule was **pre-declared, not invented here** — `damage_resolver.py:483-486`'s
own consumer contract already reads *"Apply MULTIPLICATIVELY on the defender's per-tick movement
magnitude … NOT additive with chill/root (each modifier honors its own LOCKED cap individually;
composition is successive multiplication)."* That sentence was written in Wave-D against consumers
that did not exist. The audit's finding is that chill/root never got theirs. So I implemented the
declared rule and stated it is now load-bearing rather than aspirational.

**Scrutinize:** (a) whether that reading of the Wave-D docstring is fair, or whether I used a comment
to skip a design decision that should have gone to gandalf/Matt; (b) the two rejections — additive
(`max(0, 1 − 0.90 − 0.40) = 0`, which manufactures a **de-facto root out of two soft slows**, jointly
violating two independently LOCKED caps) and strongest-only (`min(0.10, 0.60) = 0.10`, which makes a
second slow **free** and inverts control-archetype design intent). Both rejections are asserted
against in `test_composition_chill_x_decrepify_is_successive_multiplication` — the measured
`0.0300 m` discriminates all three rules; (c) **§ 3.3, the derived bound `M_min = 0.10 × 0.60 =
0.06`** — I **stated** it and did **not** clamp it, on the grounds that inventing a combined floor is
a balance decision without design authority. If you think a 6%-movement asymptote is itself a balance
decision that needed authority *before* shipping, that is a legitimate BLOCK and I want it raised
now, not after the ladder runs.

### 5.2 The silence per-skill gate, hoisted out of `skill_ready`

**Math note § 2.1, code `:2135`.** `SKILL_BLOCKED(E, i) ≡ Z(E) ∧ role(skill_i) ∉ {mobility,
defensive}`, with the silence scan **hoisted once per selector call** rather than evaluated per-skill
inside `skill_ready`.

**Scrutinize:** (a) the hoist is a **performance-motivated restructuring of a correctness gate** —
confirm it cannot change semantics (the effect list does not mutate within a selector call, so the
hoisted value is invariant across the per-skill loop; I believe this holds, but it is exactly the
kind of thing that is true today and false after someone adds an effect-expiry inside the loop);
(b) the **accessor asymmetry**: the live selector reads role from a **dict** (`skill.get("role","")`)
where the kernel reads a **dataclass attribute** (`ss.skill.role`). Same string domain, different
accessor — a genuine drift risk if the two ever diverge; (c) **absent-role skills (`""`) are treated
as offensive** (blocked under silence). That is a judgement call I made to match the kernel's `not
in` test against a role that will never equal `mobility`/`defensive`. It is defensible; it is not
forced.

### 5.3 The shared player/mob selector — coverage claim

**Code `:2066` / `:2109`, call sites `:4369` and `:4564`.** The claim is that wiring one gate covers
both actors.

**Scrutinize:** (a) confirm those are the only two production call sites (I ran
`grep -n '_select_skill_for_entity'` and found the definition, two calls, and four comment
references — please confirm independently, since "free on the player side" rests entirely on it);
(b) the **asymmetry that remains**: the action lock is shared, but movement is **not** — the player
path is inline in `run()` and `_navigate_entity` bails on `is_player`. Two movement consumers now
implement the same law in two places. That is a maintenance seam, and it is where a future divergence
will appear; (c) **player-side `curse:decrepify` (δ) is deliberately NOT wired** (math note § 4.2),
on the grounds that it is Wave-D scope and wiring it would move W-D Axis-1 mobility measurement
outside this dispatch's blast radius. Confirm that boundary is the right one, or rule that the
asymmetry (mobs eat δ, the player does not) should not ship.

### 5.4 The A/B measured soft CC only — hard CC has ZERO in-sim exercise

**This is the finding I would most want a second pair of eyes on, and it is mine, not the dispatch's.**

The CC census over the kit pool: **66 configs — 61 with `cc_effects = 0`, 5 with `cc_effects = 4`**,
and the census `magnitudes` dict has exactly **one key, `chill`**, at one magnitude
(`slow_percent 0.35`, `duration_seconds 3.0`). Runtime confirms it: the full-frame post arm records
`nav_slowed = 12180` and has **no `select_action_locked` key and no `nav_move_locked` key** — the
harness's `bump()` creates a key only on first increment, so their absence is a hard zero across
5.66 M navigate calls and 1.69 M selector calls.

**Therefore:** the −9.74% `magic_pack` delta is **entirely the chill slow**. The stun / freeze / root
/ silence locks — the actual F8 subject — **never fired in 64 cells**. Their blast radius is not
small; it is **unmeasured**. Their correctness rests on the 35-assertion unit suite (which does
exercise the DR immunity window end-to-end through the applier, and the boss resist tier), not on
in-sim evidence.

**Scrutinize:** (a) whether that is acceptable for a Gate-2 pass, or whether it warrants a
conditional pass pending a hard-CC-bearing synthetic kit run; (b) the routing — I judged this
**generation-side** (the pool emits no hard CC) and routed it to rocket via knight-rider rather than
patching. Confirm or redirect; (c) **the L0 ladder consequence rides on this** — see § 6.

Also in this bucket: **the `in_band` discard.** `w4g2_tier_2_full_sim` returns `in_band` as its third
value and the harness drops it (`grep -c in_band` = 0 on both JSONs). My "no verdict flips"
conclusion is band arithmetic against `gauntlet_sim.py:504`, which is sound for **band membership**
but is **not** a re-run of the verdict function. Any verdict predicate consulting something other
than the KPM band is **UNVERIFIED**. If that matters to the pass, the harness needs a one-line change
and a re-run.

### 5.5 Two defects in my own artifacts

Raised by me so you do not have to find them:

1. **Math note § 8 claims a "verified" line map; 2 of its 10 rows are off.** `_f8_move_locked` is
   cited at `577` but its `def` is at **`561`**; `_f8_slow_factor` is cited at `595` but its `def` is
   at **`579`**. Both cited lines land *inside* the correct function, so the map is navigable and
   every **site** is right — but a commit whose entire purpose was correcting line numbers should not
   have two wrong ones. Re-verified line-by-line in the report § 1. Not amended (no code change would
   justify a third commit); your call whether it needs one.
2. **The corpse-chill statistic in `9f3135a`'s message and in MIGRATION.md is UNVERIFIED.** The claim
   — *"546 of 587 chill landings (93%) hit a defender already at `hp ≤ 0`"*, offered as the reason
   three of four shells show zero delta — **cannot be reproduced from disk**. The harness instruments
   only `attempt:<name>` / `landed:<name>` (`…-ab.py:137-141`); it has no defender-liveness counter,
   and neither JSON contains 546 or 587. It came from an ad-hoc trace in the dead session that was
   not persisted. The mechanism is plausible and the shape is consistent (`landed:chill 5116` of
   `attempt:chill 14802`), but **the figure should be re-measured before it is cited as fact**, and
   it should **not** be treated as ratified by this Gate 2 on the strength of a commit message. It is
   already routed to gandalf/Matt as an upstream application-ordering question; I am flagging that
   the routing should carry the UNVERIFIED stamp with it.

---

## 6. Ladder consequence gated on this review

**The L0 no-CC character constraint retires when this clears Gate 2.**

It existed because the ladder could not place a CC-bearing character honestly — the engine emitted
control effects that consumed nothing, so a CC-carrying character was scored as though those effects
were free flavor. With consumption wired, a CC-bearing character can be laddered on realized behavior
rather than declared behavior.

The retirement is **contingent on your verdict**, and the evidence beneath it is **asymmetric**: the
soft-CC arm is measured across 64 cells; the hard-CC arm is unit-tested with zero in-sim exercise
(§ 5.4). Not, in my judgement, a reason to hold the retirement — but a reason the first hard-CC
ladder run is the one to watch, and a reason § 5.4(b) should route regardless of the verdict here.

---

## 7. Cross-seam and schema

**No schema change.** No new `SpatialFightResult` field, no new `FightResult` field, no new
`CombatantState` field, no telemetry column, no export contract change. Under a strict reading, no
MIGRATION entry was required.

One was filed anyway, because the change is **value-level** and star-lord's exports carry the
affected values. Downstream impact, per the MIGRATION entry:

- Telemetry fight rows (duration, kills, KPM, damage) — **values shift for kits that land CC**; no
  columns change.
- **Historical vs new telemetry is not directly comparable for CC-bearing kits** across 2026-07-25.
  Zero-CC kits are byte-identical (32/32 measured) and need no asterisk.
- `spatial_engine.WIRE_HARD_CC` — new module-level bool, default `True`; setting it `False`
  reproduces the pre-2026-07-25 engine exactly.
- **BC `control density` axis** — pre-2026-07-25 it measured an emitted *property* with no realized
  *effect*. Flagged, **not** re-derived (cross-seam).

**No action required of star-lord** — informational, no migration to author. I did not touch
`telemetry/`, `export/`, or `output/`.

---

## 8. Requested verdict

PASS / PASS-with-findings / BLOCK on:

1. The composition rule and its "ratifies a pre-declaration" framing (§ 5.1), including whether
   leaving `M_min = 0.06` unclamped was mine to decide.
2. The silence hoist and its accessor asymmetry (§ 5.2).
3. The shared-selector coverage claim and the movement asymmetry it leaves (§ 5.3).
4. Whether zero in-sim hard-CC exercise (§ 5.4) is compatible with a pass, or requires a conditional.
5. Whether the two self-reported artifact defects (§ 5.5) need remediation commits before close.
6. Whether the L0 no-CC ladder constraint may retire on this verdict (§ 6).

**Signed:** gamora, 2026-07-25.
