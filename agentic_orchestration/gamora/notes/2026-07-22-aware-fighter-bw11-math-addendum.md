# Aware-Fighter BW-1.1 — Math-Note Addendum (F2 ALIGN + F9 NORMALIZE)

**Author:** gamora (seam owner, `simulation/`), 2026-07-22
**Discipline #1 (math-before-code):** this addendum lands BEFORE any BW-1.1 code. It fixes the F2
target-reuse pathway and the F9 normalization form, and proves BLIND-neutrality for each — the
property the 256-fight equivalence battery re-gates.
**Parent note:** `2026-07-22-aware-fighter-bw1-math.md` (§0 seam recon, §1–§2 seam algebra, §3 map,
§4 battery). This addendum extends it; all §-refs to the parent stand.
**Governing dispositions:** jack-ryan Gate-2 findings `agentic_orchestration/qa/findings/2026-07-22-gate2-aware-fighter-bw1.md`
F2 (INFO, latent — E4 commitment-site coherence) + F9 (INFO — distance dominance in mixed configs).
**Conductor:** gandalf RUN-CONDUCTOR (run ledger L-25).
**Hard gate:** full 256-fight equivalence battery via the policy seam under BLIND, post-both-changes,
must stay 256/256 bit-equal (metric triples AND decision traces) vs the recorded BW-1 BEFORE leg.

---

## §A0 — Empirical site recon (Discipline #11; verified at HEAD `a9e2bc7`)

Line numbers as FOUND (the brief cited ~:3130 / ~:3226; empirically):

- **E4 mid-flight move-cancel** — `spatial_engine.py:3129–3133`, inside `_e4_service_commitment`
  (def `:3063`). Gated `if not self._e4_blind:` (`:3129`). Body:
  `nearest = min(alive_mobs, key=lambda t: p.distance_to(t))` (`:3130`), fed to
  `csm.project_target_position(nearest, …)` (`:3131`) → `_point_in_template` whiff check (`:3134`).
- **E4 wind-up initiation** — `spatial_engine.py:3225–3231`, inside `_e4_initiate_commitment`
  (def `:3214`). Gated `if not self._e4_blind:` (`:3225`). Body:
  `nearest = min(alive_mobs, key=lambda t: p.distance_to(t))` (`:3226`), fed to
  `csm.project_target_position(nearest, …)` (`:3227`) → `_point_in_template` whiff check (`:3230`).

**Player-only by construction (Discipline #11):** both `_e4_service_commitment` and
`_e4_initiate_commitment` bind `p = self.player` (`:3220`, and the service body). Their only callers
are `:4026` (service) and `:4063` (initiate), BOTH inside the player action phase. **There is NO mob
path through these two sites** — the mob commitment machinery does not exist here (mobs use the
instant path). So "mob paths unchanged" (D1 brief) holds trivially: there are no mob paths at
:3130/:3226 to change. This is reported as-found, not as-briefed.

**`_e4_blind` is a SEPARATE axis (do NOT touch its gating semantics).** `self._e4_blind`
(constructor param `e4_blind_pilot`, `:2422`; doc `:606`) is the criterion-18 E4-blind ablation
pilot — a wind-up/commitment-COMPETENCE axis (does the pilot project whiff and cancel, or ride every
wind-up out?). It is ORTHOGONAL to the aware/blind POLICY axis (`self._policy_config`). The F2 fix
changes ONLY the argument passed INTO `csm.project_target_position` on the `not self._e4_blind`
branch; it does NOT alter the `if not self._e4_blind:` predicate, does NOT add/remove a branch, and
does NOT change when the projection fires. The E4-blind axis behaviour is preserved bit-for-bit.

---

## §A1 — F2 ALIGN: reuse the seam's chosen target for the whiff projection

### §A1.1 The incoherence (AWARE-only) and why BLIND is neutral
Today both E4 sites LOCALLY recompute `nearest = min(alive_mobs, key=distance_to)`. The action phase
that INITIATES the commitment first ran `_select_skill_for_entity(self.player, alive_mobs, …,
policy_config=self._policy_config)` (`:4048`), whose player branch (`:1957`) chose the attack-target
`nearest_target = _policy_choose_target(entity, targets, config=policy_config)`. Under **AWARE**,
that seam attack-target can DIFFER from raw-nearest — so the wind-up projects at a mob the policy did
NOT choose to attack (an in-arm incoherence: project the whiff for the wrong target). Under **BLIND**,
`choose_target` reduces to `min(alive_mobs, key=distance_to)` (parent §1.4, proven + battery-verified)
— so the local recompute and the seam choice select the SAME entity, byte-identically.

### §A1.2 The fix — project at the seam's ATTACK-target, not raw-nearest
Replace, at BOTH sites, the local `nearest = min(alive_mobs, key=distance_to)` (player path only —
the whole site is player-only, §A0) with the policy seam's chosen target:

    nearest = _policy_choose_target(p, alive_mobs, config=self._policy_config)

**Which boss_focus?** The E4 commitment is a CAST/ATTACK wind-up initiated in the action phase
immediately after `_select_skill_for_entity` chose the skill against the ATTACK-target. The
BW-1-established attack-target semantics (parent §2; code `:1951–1957`) call the seam **WITHOUT**
`boss_focus` — because the legacy player attack-target was plain nearest (boss-focus is a MOVEMENT
property applied only at `_get_player_primary_target`, `:1574`). For the E4 whiff projection to check
the mob the policy is actually going to ATTACK, it must use the SAME attack-target semantics →
`_policy_choose_target(p, alive_mobs, config=self._policy_config)` with **no boss_focus arg**
(boss_focus defaults to None in `choose_target`). This makes the projection coherent with the
attack-target the seam chose at `:1957` under AWARE, and is identical to raw-nearest under BLIND.

To reach `self._policy_config` inside the two methods, thread it. Both methods are private engine
methods on `SpatialFightEngine`, so `self._policy_config` is already in scope — **no signature change
required.** (Verified: both are `def _e4_*(self, …)` methods; `self._policy_config` is set at `:2407`
per BW-1.) The fix is a one-line body change at each site; no new parameters, no caller change.

### §A1.3 BLIND-neutrality proof (F2)
Under BLIND (`self._policy_config` = the `{distance}` config, `normalize=False`, weight 1.0):

    _policy_choose_target(p, alive_mobs, config=BLIND, boss_focus=None)
      → seam.choose_target boss_focus limb: boss_focus is None → skip (`:54`)
      → single-{distance} fast path (`:68–79`): best = alive_mobs[0]; for m in alive_mobs[1:]:
        if p.distance_to(m) < best_d: best = m  ← IDENTICAL replacement predicate to
        min(alive_mobs, key=lambda t: p.distance_to(t))
      ⇒ returns the SAME entity, tick-for-tick, as the local recompute (parent §1.4.1: min and this
        fast-path both keep the FIRST extremum on ties; identical replacement predicate → identical
        selection; negation of an IEEE-754 double is exact → no epsilon, no tolerance band).

**∴ under BLIND the F2 change is a NO-OP at the entity level** — `csm.project_target_position`
receives the identical `nearest`, so `_point_in_template`, the move-cancel / initiation decision, and
every downstream metric (mobs_killed, aoe_hits, damage_total) AND the decision trace are byte-
identical. The battery (§A3) re-verifies this empirically over 256 fights.

**Battery-frame corollary:** the W3′ 32-cell frame is ALL `all_mobs_killed` (parent §1.5), so
`self._boss_focus_entity` is None throughout the battery. The no-boss_focus choice is therefore
neutral in-frame regardless; the boss_focus reasoning above is for AWARE coherence out-of-frame.

---

## §A2 — F9 NORMALIZE: distance normalized in MIXED configs; BLIND fast-path exact

### §A2.1 The dominance defect (AWARE mixed configs)
In `AWARE_CANDIDATE_CONFIG` the `distance` consideration pulls the SAME registry entry BLIND uses:
`Consideration("distance", _score_distance, normalize=False)` (`considerations.py:117`). Its raw
score is `-distance` (magnitude ~tens of meters, e.g. −0.5 … −40 on the 36–44 m gate arenas). The
other five considerations normalize to [0,1] (`seam.py:92`). In the general utility path the sum
`Σ w_i s_i` therefore adds a ~[−40,0] term to five ~[0,1] terms — **raw distance dominates the
argmax** and the geometry considerations are numerically inert. That is F9.

### §A2.2 The normalization form (the machinery I propose; prereg pins weights)
The seam already has the correct primitive: `_normalize_scores` (`seam.py:33–41`) — per-decision
min-max over the candidate set → [0,1], all-equal → 0.5 (parent §3.3.1). The general path ALREADY
applies it to any consideration whose `normalize=True` (`:92`). So the ENTIRE F9 fix is: make the
`distance` consideration **normalize in MIXED configs** while **BLIND keeps `normalize=False`** (for
the fast-path exactness). The chosen form is the seam's existing exposure-map-consistent min-max
kernel — NOT a new kernel. Concretely:

    s_distance_normalized(c) = _normalize_scores([ -distance(player, c') for c' in candidates ])[c]
      = ( -d(c) - min_c'(-d(c')) ) / ( max_c'(-d(c')) - min_c'(-d(c')) )    (all-equal → 0.5)

This maps closest→1.0, farthest→0.0, weight-comparable to the five [0,1] geometry scores. It is the
IDENTICAL normalization the geometry considerations already use — chosen for scale-commensurability
consistency (parent §3.3.1), not a bespoke form.

**Implementation shape (registry, not tuning):** keep the raw `_score_distance` (it stays the exact
`-distance` the BLIND fast-path needs). Register TWO named considerations off the one scorer:
- `"distance"` → `Consideration("distance", _score_distance, normalize=False)` — **unchanged**;
  BLIND_CONFIG references this; the `seam.py:70` fast-path predicate
  (`cons.name == "distance" and not cons.normalize and weight > 0.0`) still fires → IEEE-exact argmin.
- `"distance_normalized"` → `Consideration("distance_normalized", _score_distance, normalize=True)`
  — MIXED configs (AWARE_CANDIDATE_CONFIG) reference THIS; it flows through the general path's
  `_normalize_scores` (`:92`) → [0,1], weight-comparable. Same scorer, `normalize=True`.

`AWARE_CANDIDATE_CONFIG`'s `("distance", 1.0)` entry becomes `("distance_normalized", 1.0)`. This is
machinery only — the weight stays 1.0 at PROPOSAL; the GATE weights are pinned at prereg (charter
§2.2, parent §3.3). `"distance_normalized"` is added to the map-consumer EXCLUSION the same as
`"distance"` (it reads no ExposureMap — `_MAP_CONSUMERS` excludes both), so a MIXED config that is
purely `{distance_normalized}` still builds no map. Actually: `_MAP_CONSUMERS =
frozenset(REGISTRY) - {"distance"}` today; it must become `- {"distance", "distance_normalized"}`
so neither distance variant marks a config as needing the map.

### §A2.3 BLIND fast-path exactness proof (F9)
BLIND_CONFIG is UNCHANGED: `weighted=(("distance", 1.0),)` → the singleton `{distance}` with
`normalize=False`. The `seam.py:68–79` fast-path predicate is unchanged and still matches
(`len==1`, `cons.name=="distance"`, `not cons.normalize`, `weight>0`) → the raw `-distance`
comparison runs → `argmax(-distance) ≡ argmin(distance)`, IEEE-exact (parent §1.4.2). **F9 adds a
SECOND consideration to the registry and re-points the AWARE config; it does not touch BLIND_CONFIG,
the `distance` registry entry, or the fast-path predicate.** ∴ BLIND is byte-identical post-F9.

**Neutrality boundary (Discipline #12):** F9 is a SEMANTIC re-expression of the AWARE candidate set
only. Under BLIND nothing changes (proven above). The `AWARE_CANDIDATE_CONFIG` swap from
`("distance", 1.0)` to `("distance_normalized", 1.0)` CHANGES the AWARE argmax (distance is now
[0,1]-commensurate, no longer dominant) — that is the intended F9 correction, and AWARE is NOT gated
by the battery (charter §2.3; the battery gates BLIND ≡ legacy). Framed here, not buried.

---

## §A3 — Re-gate: the 256-fight battery (post-D1+D2, BLIND ≡ frozen BEFORE)

**Standard (unchanged from parent §4):** bit-equal metric triples per fight AND decision-trace
equality vs the recorded BW-1 BEFORE leg; NO tolerance bands; any mismatch ⇒ red-flag STOP + report;
RNG-divergence-with-identical-decisions is its OWN reportable class (parent §4.4).

**Baseline reuse (Gate-2 action item — worktree removal).** The recorded
`2026-07-22-aware-fighter-bw1-battery-before-full.json` is a self-sufficient frozen legacy baseline:
256 results, each with the full `triple` + `trace` (verified: `engine_bound` =
`/tmp/aware-before-worktree/…`, the stamp-`a3671d4` legacy path). D1/D2 do NOT touch the BEFORE
worktree, so re-spawning the BEFORE leg would reproduce this exact record. Therefore I extend the
runner with a `--baseline-file` mode: spawn ONLY the AFTER leg (main tree, post-D1/D2, BLIND config),
load the recorded before-full.json as the BEFORE record, and run the SAME comparison (triple + trace
bit-equality + RNG-divergence-class detector + the recorded-W3′ cross-check on the AFTER leg). This
lets the `/tmp/aware-before-worktree` be removed BEFORE the final gate (Gate-2 action item) because
the frozen JSON IS the baseline. The `--smoke` and dual-spawn modes are retained unchanged.

**Sequencing:** (i) land D1+D2 + tests; (ii) run `--baseline-file` full battery: AFTER(D1+D2,BLIND)
vs recorded before-full.json → require 256/256 bit-equal; (iii) on PASS, `git worktree remove
/tmp/aware-before-worktree`. On ANY mismatch: STOP, do not remove the worktree, report the class.

---

## §A4 — Semantic-shift declarations (Discipline #12)

1. **F2: E4 whiff-projection target is RE-SOURCED from raw-nearest to the policy seam's attack-
   target.** Under BLIND this is a proven no-op (§A1.3). Under AWARE it CHANGES which mob the wind-up
   projects against (now coherent with the attack the seam chose). The `_e4_blind` axis predicate is
   untouched. Framed, not buried.
2. **F9: a `distance_normalized` consideration is ADDED and `AWARE_CANDIDATE_CONFIG` re-points to it.**
   BLIND keeps raw `{distance}` (IEEE-exact fast path). This changes the AWARE argmax (distance now
   scale-commensurate with geometry considerations); it does NOT change BLIND. The gate weights are
   still pinned at prereg — this is machinery, not tuning.

---

## §A5 — Out-of-scope guardrails (unchanged from parent §7 + brief)

- `_e4_blind` gating semantics: UNTOUCHED (separate criterion-18 axis).
- Mob paths at :3130/:3226: none exist (player-only sites); mob commitment untouched.
- BLIND_CONFIG + `distance` registry entry + fast-path predicate: UNTOUCHED.
- Skill selection (`_select_player_skill_v2`), movement execution, escape/gather overrides: UNTOUCHED.
- Engine writes confined to `simulation/spatial_gauntlet/` + `tests/`. No telemetry schema change,
  no corpus.db touch (READ-ONLY).

## §A6 — Build order (code follows this addendum)
1. F9 (lowest risk, does not touch the seam decision path): add `distance_normalized` to the registry
   + fix `_MAP_CONSUMERS` + re-point `AWARE_CANDIDATE_CONFIG`. (considerations.py only.)
2. F2: re-source `nearest` at :3130 and :3226 to `_policy_choose_target(p, alive_mobs,
   config=self._policy_config)`. (spatial_engine.py only.)
3. Unit tests: F2 target-reuse (player uses seam choice; `_e4_blind` axis preserved; no mob path) +
   F9 normalization (mixed-config distance in [0,1]; BLIND fast-path exactness). All existing green.
4. Extend battery runner with `--baseline-file` mode.
5. Full battery AFTER(D1+D2,BLIND) vs recorded before-full.json → 256/256 or STOP.
6. Remove `/tmp/aware-before-worktree` on PASS. Slice report.
