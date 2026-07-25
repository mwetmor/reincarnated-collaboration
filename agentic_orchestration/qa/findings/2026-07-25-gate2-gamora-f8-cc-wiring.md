# Finding — 2026-07-25 — gamora: F8 hard-CC consumer wiring

**Reviewer:** jack-ryan (DEV-MODE, Gate 2, pre-registered in dispatch)
**Severity:** WARN — **VERDICT: CLEAR-WITH-CONDITIONS**
**Target:** tag `gamora/v-f8-cc-1` → `fe5d5ea` (+ `9f3135a`), `~/Games/reincarnated-engine`, branch `main`, **not pushed**
**Developer:** gamora (simulation seam)
**Request:** `agentic_orchestration/qa/pending/2026-07-25-gamora-f8-cc-wiring-gate2.md`
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (contract docs as truth), #5 (severity matters)
**Disciplines cited:** #1 math-before-code · #3 no parallel regens · #10 empirical inspection over assumption · #12 name every semantic shift

---

## Verdict

**CLEAR-WITH-CONDITIONS.** The wiring is correct, the math note is sound, the composition rule is
honestly framed, the shared-selector coverage claim holds under independent verification, and the
test suite reproduces. Five conditions below. Two of them (C1, C2) gate the L0 retirement.

**L0 no-CC test-character constraint: retirement is CONDITIONAL — it does NOT fire on this verdict
alone.** It fires when **C1** and **C2** are closed. C3/C4/C5 do not gate it. See § "L0 ruling".

Nothing here escalates to Matt. All remediations are within-seam code/doc fixes (ADR-002 tier:
jack-ryan approves). Push remains Matt-gated per ADR-006.

---

## What I found

### CLEARED — the four items the request named for scrutiny

**1. Composition rule `M = σ·(1−δ)` — CLEAR.** The "ratifies a pre-declaration, does not invent"
framing is **honest, verified verbatim.** `damage_resolver.py:484-487` reads
*"apply MULTIPLICATIVELY on the defender's per-tick movement magnitude … NOT additive with
chill/root (each modifier honors its own LOCKED cap individually; composition is successive
multiplication)"* — written in Wave-D against consumers that did not exist. Implementing the
declared rule is the correct move; escalating it to gandalf would have been re-litigating a settled
contract. Both rejections are substantively right: additive jointly violates two independently
LOCKED caps (`combatant.py:424` σ-floor 0.1; `damage_resolver.py:468`
`WAVEC_CURSE_DECREPIFY_MOVEMENT_REDUCTION_MAX = 0.40`) and manufactures a counterfeit root;
strongest-only makes a second slow free.

*One framing correction (INFO, no remediation):* the report and math note say the measured
`0.0300 m` "**falsifies**" additive and strongest-only. It does not — the code implements successive
multiplication, so the probe measures the implementation. What
`test_composition_chill_x_decrepify_is_successive_multiplication:255-256` actually does is **pin**
the rule so a future silent substitution fails at the test rather than in a balance run. That is
real value; it is a regression pin, not an empirical discrimination. Discipline #10 precision.

**`M_min = 0.06` left unclamped — CLEAR, correct call.** Introducing a combined floor without design
authority would have been the violation, not the omission. Stated-and-routed is right. No condition.

**2. Silence per-skill hoist — CLEAR.** The hoist is **semantics-invariant**: `_f8_silenced` is
computed at `spatial_engine.py:2135-2139` and read only inside the `skill_ready` closure at `:2150`;
nothing between the hoist and the selection loop mutates `active_effects` (no expiry tick, no
applier call). Verified by read. gamora's own concern — "true today, false after someone adds an
effect-expiry inside the loop" — is legitimate and is now recorded here as the reason the invariant
should be re-checked on any future edit to that function.

*On "is that the ailment-layer spec's intent?" — the premise does not hold.* **There is no
ailment-layer spec intent for silence.** `silence` is not in `config/ailments.yaml` (16 entries:
burn, chill, root, knockback, bleed, shock, consecrate, drain, sunder, freeze, stun, poison, blind,
curse, fear, execute) and is explicitly documented as out-of-registry at
`src/reincarnated/foundation/effect_categorization.py:36` — *"silence is a non-ailment status effect
(not in registry)"*. It has a live producer (`damage_resolver.py:1182-1187`) and a generation
dimension (`generation/layer2_dimensions.py:75`), but its only semantic declaration anywhere is
`combatant.py:461`. The wiring transcribes the only authority that exists. That is the right call;
the math note §2.1 should not imply spec grounding it does not have (INFO, folded into C3).

*Cross-seam INFO (route to star-lord, non-blocking):* `src/reincarnated/export/season_exporter.py:266`
publishes to players *"`silence` | Prevents ability use"* with no mobility/defensive carve-out. That
player-facing text now under-describes realized behavior.

Accessor asymmetry (dict `skill.get("role","")` vs dataclass `ss.skill.role`) and absent-role→
offensive are both correctly judged. Shared string domain; the `not in` match is faithful.

**3. Shared-selector coverage claim — CLEAR, independently verified.**
`_select_skill_for_entity` is defined once at `spatial_engine.py:2066`. Exactly **two** production
invocation sites: `:4369` (player action phase) and `:4564` (mob action phase). All other
occurrences (`:2599`, `:2872`, `:3337`, `:3441`, `:4277`) are comments — confirmed by reading each.
No dynamic dispatch. I additionally checked for a **third** actor class the request did not name:
ally proxies (`:4163`) route through `_navigate_entity` (so the movement lock covers them) and are
nav-only with no realized damage in W1 (`:4159-4162`), so no third action-selection consumer exists.
The "free on the player side by construction" claim is sound.

The movement asymmetry (two implementations of one law — `_navigate_entity:1770` and the inline
`run()` block at `:4291`) is a genuine maintenance seam, and it is **exactly where C1 landed.**

Player-side `curse:decrepify` deliberately unwired — **CLEAR, correct boundary.** It is Wave-D scope;
wiring it would move W-D Axis-1 mobility measurement inside a blast radius this dispatch was
chartered to hold fixed. Named follow-on, not a silent gap.

**4. Root does not action-lock — CLEAR, spec-conformant, not a bug.** `config/ailments.yaml:91-96`:
*"root — Positional immobilization. **Locks the target's movement**; held until duration expires or
root is broken."* `is_control: hard`, `category: hard_control`. A root that blocked action would be
a freeze (`config/ailments.yaml:238-242`: *"freeze — Full movement + action immobilization"*).
The dispatch §3's "all five CC arms must flip to `None`" was the imprecise sentence; the math note
§7 divergence note is the correct reading. *Citation correction (INFO, folded into C3):* math note
§2 and `spatial_engine.py:547` both cite "ailment-layer spec §3/§4" as root's authority, but §3 is
freeze and §4 is stun — the actual authority is the registry entry `config/ailments.yaml:91-96`.

---

### NEW FINDING (not self-reported) — C1

**A hard-CC'd mob beyond its leash radius never latches `is_leashing`, and under `root` this makes
the mob strictly more dangerous than not CC-ing it.**

`entity.is_leashing = True` is set at `spatial_engine.py:1826`, **after** the F8 move-lock early
return at `:1770`. `is_leashing` is not a movement state — it gates the **mob action phase** at
`:4536` (`if mob.is_leashing: continue`). So the lock suppresses a *combat-disengagement latch*, not
just displacement.

Empirically confirmed (read-only probe against HEAD `fe5d5ea`, mob at 50 m from spawn,
`leash_distance_m = 10.0`):

```
no CC   -> is_leashing=True   pos=(50.00,0.00)
root    -> is_leashing=False  pos=(50.00,0.00)
stun    -> is_leashing=False  pos=(50.00,0.00)
chill   -> is_leashing=True   pos=(50.00,0.00)
```

Under **stun/freeze** the action lock catches the mob anyway, so the exposure is masked. Under
**`root` there is no action lock** — the rooted out-of-leash mob keeps attacking for the root's full
duration (registry range 1.5–4.0 s, `config/ailments.yaml:98-101`), where the un-rooted mob would
have latched and stopped. **Applying root to an out-of-leash mob is currently a player-adverse
action.** That is a behavioral inversion.

Two things follow:

- Math note §3.4 claims to name the semantic shifts the placement creates and names three. This is a
  **fourth**, and it is the only player-adverse one. Discipline #12 requires it be named.
- `test_dominance_lock_beats_leash_return:509` covers the **already-latched** case only. The
  **latch-suppression** case has no test.

I am not ruling on the fix. Two defensible resolutions exist (hoist the leash-trigger evaluation
above the move lock so the latch is state-not-movement; or accept the suppression and document it as
intended). Either is within gamora's seam. What is not acceptable is shipping it unnamed and
untested into the ladder — see the L0 ruling.

---

### Self-reported defect A (line map) — WARN, and BROADER than reported

Both §8 rows confirmed wrong: `_f8_move_locked` cited at `577`, `def` is at **`561`**;
`_f8_slow_factor` cited at `595`, `def` is at **`579`**. Both land inside the correct body, so the
map is navigable.

**But the correction commit `fe5d5ea` was incomplete.** The stale `:4171 / :4366` selector call-site
pair — corrected in §8 — survives in three places `fe5d5ea` did not touch:

| Location | Stale text |
|---|---|
| `src/reincarnated/simulation/math/…-2026-07-25.md:187` | math note **§4** table: *"call site `spatial_engine.py:4171`"*, and *"inline in `run()` (~`:4110-4130`)"* — actual `:4291` |
| `src/.../spatial_gauntlet/spatial_engine.py:4277` | **shipped production comment**: *"call sites :4171/:4366"* |
| `tests/test_f8_hard_cc_consumer.py:410` | test docstring: *"the SAME selector (:4171 / :4366)"* |

A commit whose sole stated purpose was correcting a line map left the stale map in production
source. Severity WARN, remediation is doc/comment-only.

### Self-reported defect B (corpse-chill statistic) — WARN, MANDATORY remediation

Independently confirmed **unverifiable**. The harness wraps `_try_apply_ailment` with a
`len(defender.active_effects)` delta counter only
(`agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab.py:130-143`) — there is no
defender-liveness read anywhere in it. Neither JSON contains the counters; `exercise_post` is
verbatim `{nav_calls, select_calls, attempt:chill, landed:chill, nav_slowed, attempt:burn,
landed:burn}`.

The escalating factor gamora under-weighted: **this is not only in a commit message.** It is at
`src/reincarnated/simulation/MIGRATION.md:50` as a **bolded assertion** —
*"**93% of all soft-CC applications land on an already-dead defender** (546 of 587 chill landings…)"*.
`MIGRATION.md` is the cross-seam contract document star-lord and elrond read as ground truth
(REVIEW_PROCESS #4). An unreproducible measurement published there as bolded fact is the specific
failure mode Discipline #10 exists to prevent. It must be struck or replaced with a re-measured
figure before close. Commit messages are immutable history and get a correction-of-record note, not
a rewrite.

### A/B evidentiary asymmetry — HALF of it I closed; half stands

**The hard-CC in-sim exercise gap is real and gamora's account of it is exact.** Independently
re-derived from `…-ab-full.json`: 66 configs, `Counter({0: 61, 4: 5})`, `magnitudes` = exactly one
key `chill` at one magnitude `{"duration_seconds": 3.0, "slow_percent": 0.35}`. `exercise_post`
contains `nav_slowed: 12180` and **no** `select_action_locked` / **no** `nav_move_locked` key. The
absence-is-hard-zero inference is correct given the `bump()` create-on-first-increment pattern.
So: stun / freeze / root / silence fired **zero times in 64 cells**. Unmeasured, not small. Confirmed.

**The `in_band` discard, however, is now VERIFIED — gamora's UNVERIFIED stamp can be removed.** I
traced both band predicates at HEAD:

1. `_shell_result_passed` (`gauntlet_sim.py:961-970`) — the predicate behind `w4g2_tier_2_full_sim`'s
   pass verdict — reads `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]`, which for `magic_pack` **is**
   `(12.52, 102.86)` (`gauntlet_sim.py:504`). gamora's manual arithmetic reproduces this predicate
   **exactly**, not approximately. All 16 mover values 25.358810…29.459902 interior ⇒ no flip.
2. The **Track-1 override** at `gauntlet_sim.py:1572-1580` sets the authoritative
   `enc_result.in_band` from `get_archetype_cohort_kpm_band(damage_scaling_path, cohort)`. I checked:
   `_ARCHETYPE_COHORT_KPM_BAND is None` at HEAD, so it falls back to `COHORT_KPM_BAND[cohort]` =
   `(82.0, 97.0)` DPS-min-maxer / `(71.0, 79.0)` Balanced. All 16 mover values are **below the floor
   in both arms** ⇒ FAIL pre, FAIL post ⇒ **still no flip.**

**No verdict flip under either predicate. The discarded field could not have changed the
conclusion.** No harness re-run required.

*But a factual correction is owed:* report §4.3 states without qualification *"every one interior to
the band."* Under the Track-1 predicate they are **not interior — they are below floor, pre and
post.** True-but-partial. Fold into C3.

### Tests — VERIFIED

Reproduced independently at HEAD `fe5d5ea` with `python3 -m pytest` (no venv, `python` not on PATH):

```
tests/test_f8_hard_cc_consumer.py                         → 35 passed in 0.06s
+ spatial_gauntlet_scenarios, ailment_layer_gamora_slice,
  ailment_layer_rocket_slice, ailment_registry,
  wd_spatial_bc_measurement                               → 261 passed in 4.10s
```

The wider "1615 passed" claim from `9f3135a` remains UNVERIFIED. **I do not require the stash-bisect
re-run.** The F8-scoped subset is the correct gate scope and no conclusion here rests on the wider
count. Leave it stamped UNVERIFIED; do not cite it as evidence.

*Coverage gap (C4):* the one site that is **not** shared — the player movement wiring at
`spatial_engine.py:4291-4297` — is the one site with **no behavioral test**.
`test_player_movement_predicates:444` exercises `_f8_move_locked` / `_f8_slow_factor` on a player
entity; it does not exercise the `_e4_move_scale` composition line. That line is verified by reading
only. Given C1 is a placement bug in the *other* movement consumer, the untested one deserves a pin.

---

## Rationale

- **C1** — Discipline #12 (name every semantic shift; §3.4 claims to and misses one) + REVIEW_PROCESS
  #5 (severity: a player-adverse inversion on a registry-emittable ailment is not an INFO).
- **C2** — REVIEW_PROCESS #4 (contract docs are truth) + Discipline #10 (empirical inspection over
  assumption). A number that cannot be reproduced from disk must not sit bolded in `MIGRATION.md`.
- **C3** — Discipline #12 + REVIEW_PROCESS #1. Doc hygiene, low cost, high downstream value.
- **C4** — REVIEW_PROCESS #2. The asymmetric site is the unpinned site.
- **C5** — REVIEW_PROCESS #3 (cross-seam impact). Correct routing, confirmed not redirected.
- Composition rule, silence hoist, selector coverage, root semantics: all CLEAR under Discipline #1
  and #10. The math-before-code discipline was genuinely honored — the note predates the code, the
  rule is pre-declared, and the rejections are reasoned rather than asserted.

---

## Action

- [ ] **C1 (gamora) — BLOCKS L0 RETIREMENT.** Resolve the leash-latch suppression at
      `spatial_engine.py:1770` vs `:1826`. Either hoist the leash-trigger evaluation above the move
      lock, or ratify the suppression as intended. Either way: name it as semantic shift #4 in math
      note §3.4 + the `:1751-1769` comment block, and add a test for the **latch-suppression** case
      (`test_dominance_lock_beats_leash_return:509` covers only the already-latched case).
- [ ] **C2 (gamora) — BLOCKS L0 RETIREMENT.** Strike the "546 of 587 / 93%" corpse-chill statistic
      from `src/reincarnated/simulation/MIGRATION.md:50-53`, or replace it with a re-measured figure
      from an instrumented run. The *mechanism* claim (`_try_apply_ailment` has no liveness gate) may
      stay if stated qualitatively and marked unquantified. Carry the UNVERIFIED stamp on the
      gandalf/Matt routing.
- [ ] **C3 (gamora) — before close, doc-only, may ride one commit with C1/C2.** Complete the line-map
      correction `fe5d5ea` started: math note §4 (`:187` — `:4171` → `:4369`, `~:4110-4130` → `:4291`),
      `spatial_engine.py:4277` comment, `tests/test_f8_hard_cc_consumer.py:410` docstring, and the
      two §8 rows (`577`→`561`, `595`→`579`). Same pass: correct the root citation from "ailment-layer
      spec §3/§4" to `config/ailments.yaml:91-96` (math note §2 and `spatial_engine.py:547`); soften
      math note §2.1's implied spec grounding for silence to "kernel-declared, out-of-registry per
      `effect_categorization.py:36`"; qualify report §4.3's "every one interior to the band" with the
      Track-1 predicate result (below floor, both arms, no flip); and drop the "measurement falsifies"
      language in favor of "regression pin."
- [ ] **C4 (gamora) — follow-on, does NOT gate close or retirement.** Add a behavioral test for the
      player movement wiring at `spatial_engine.py:4291-4297` (the `_e4_move_scale × M(player)`
      composition), not just its predicate inputs.
- [ ] **C5 (knight-rider) — routing CONFIRMED, not redirected.** The "generated kits emit no hard CC"
      finding is correctly generation-side → **rocket**. It should route regardless of this verdict,
      and it is the prerequisite for ever measuring the hard-CC blast radius in-sim.
- [ ] **INFO (star-lord, non-blocking):** `export/season_exporter.py:266` player-facing silence text
      now under-describes realized behavior (no mobility/defensive carve-out).
- [ ] **Matt:** nothing required. Push remains Matt-gated (ADR-006). The `M_min = 0.06` combined-floor
      question and the corpse-chill application-ordering question are already correctly routed to
      gandalf/Matt as design items — neither gates this Gate.

---

## L0 ruling (dispatch §4 / request §6)

**The L0 no-CC test-character constraint does NOT retire on this verdict alone. It retires when C1
and C2 close.**

Reasoning, stated separately from the description above:

The retirement's premise is *"a CC-bearing character can now be laddered on realized behavior rather
than declared behavior."* That premise is satisfied for **soft CC** — chill is wired, measured across
64 cells, and its blast radius is characterized (−9.74% kpm / +10.85% duration, `magic_pack`-confined,
uniform direction, no verdict flip under either band predicate, which I verified). It is **not yet
satisfied for `root`**: C1 shows root's realized behavior currently contains an inversion that would
mis-score a root-bearing character on the exact axis the retirement is meant to make honest.

I am **not** holding the retirement on the unmeasured hard-CC blast radius (§5.4). Withholding the
Gate cannot produce that evidence — the evidence is generation-side, and the sim cannot measure what
is never emitted. The 35-assertion unit suite plus the flag-ablation probe is adequate proof of the
consumer contract, and C5 is the route that will eventually make the in-sim measurement possible.
Gamora's judgement on this was correct.

I **am** holding it on C1, which is a defect rather than an evidence gap, and on C2, which is a false
statement in a cross-seam contract document.

Once C1 and C2 land, the retirement fires without a further Gate — knight-rider confirms closure and
the constraint lifts. When the first hard-CC ladder run happens, watch it: it will be the first
production exercise of `select_action_locked` / `nav_move_locked` in the engine's history.

---

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
  — `:542`, `:561`, `:579`, `:700`, `:1770`, `:1826`, `:1882`, `:1983`, `:2066`, `:2109`, `:2135`,
  `:2150`, `:4277`, `:4291`, `:4369`, `:4536`, `:4564`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py:394-424`, `:452-471`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:468-493`, `:1182-1187`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:327`, `:504`, `:961-970`,
  `:1536`, `:1572-1580`, `:2055-2085`
- `~/Games/reincarnated-engine/src/reincarnated/foundation/effect_categorization.py:35-38`
- `~/Games/reincarnated-engine/src/reincarnated/export/season_exporter.py:266`
- `~/Games/reincarnated-engine/config/ailments.yaml:91-103`, `:238-248`, `:264-273`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/f8-hard-cc-consumer-wiring-2026-07-25.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md:11`, `:50-53`
- `~/Games/reincarnated-engine/tests/test_f8_hard_cc_consumer.py:410`, `:444`, `:509`
- `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab.py:130-143`
- `agentic_orchestration/gamora/notes/2026-07-25-f8-blast-radius-ab-{smoke,full}.json`
- `agentic_orchestration/gamora/notes/2026-07-25-f8-cc-wiring-and-blast-radius.md`
- `agentic_orchestration/dispatches/2026-07-25-gamora-f8-cc-consumer-wiring.md`

**Signed:** jack-ryan, 2026-07-25. Gate 2, DEV-MODE.
