# Finding — 2026-08-25 — godot forward-axis convention (Gate 1, DESIGN-MODE)

---

> ## ⚑ FORWARD POINTER — 2026-08-25, later the same day. **CORRECTED, NOT SUPERSEDED. Nothing below is back-edited.**
>
> Three things in this file were later measured and two of them ran against me. **The text below stands as written; read it with these three amendments.**
>
> **1. § Q4 — "the contamination is not common-mode" — RIGHT CONCLUSION, WRONG MECHANISM.** I argued the fx-on/fx-off difference fails to cancel *because body-anchored effects emit along body-forward*. On these rows that mechanism **does not obtain**: every `add_child` in `s2c_dash_attack.gd` attaches to `self`, and placement is by `global_position` read from the mover, never by parenting to its basis. **The effects are NOT body-anchored here.** The real leak is the caster's own silhouette occluding payload pixels inside a scored disc. The conclusion survives; the argument was replaced.
>
> **2. § Q4 — PENDING-RECAPTURE was CORRECT and is now DISCHARGED for rows 1–2.** 874/874 co-named frames differ between corpora; the fix reached them. The sealed verdict **HOLDS** and is reclassified `OFF-PATH` → **`ON-PATH-INVARIANT`**: the defect *was* on the causal path, and it was **SUPPRESSING** the separation — the margin **widened** on repair, pooled **+0.2069 → +0.3807**. ⚑ **The figure `+0.2069` must no longer be quoted as a measurement; it is a pre-fix-contaminated understatement.**
>
> **3. ⚑ § Q3 — I AUTHORED `#80.x` IN THIS FILE AND THEN VIOLATED IT ONE RULING LATER.** The clause reads: *check whether the arm can go red at all; if it cannot, its green is not evidence.* I then staked a pre-registered falsifier on **Mob3** as a control without checking its signal level. Mob3 is `UNEVALUABLE-BELOW-FLOOR` in **all four cells, both corpora** (peak added luma 0.0009–0.2544 against a floor of 1.0). **My control could not go red in either direction.** The real control — `blink`, signal-carrying and 75× less responsive — was in the data the whole time and I did not name it. **`#80.x` now has a second founding instance, and it is the clause's own author.**
>
> **Full derivation, flake floor, per-mob table, and the rows 3–8 pre-registration:**
> `agentic_orchestration/qa/findings/2026-08-25-s2c-prepost-limb2-disposition.md`

---

**Reviewer:** jack-ryan
**Severity:** WARN (with one conditional BLOCK, § Q1)
**Target:** pre-fire — drax dispatch, S2 facing fix. No code landed.
**Developer:** drax
**Referrer:** knight-rider, on galadriel adjudication `a1690fe0`
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity)
**Disciplines cited:** #75, #78, #80, #79 cl. 6, #25

---

## What I found

The repo does not hold two conventions. It holds **three formulas and two rig
regimes**, and the third formula is algebraically the second (`atan2(d.x,d.z)+PI`
— `vh_brief_cast:142`, `vh_brief_aura:99`, `vmur_race_rig:175/181`,
`vpro_race_rig:190/197`, `wr1_facing_witness:92`, `shoot_kit_replica:329`,
`build_walltop_void_test:122`). More consequentially: **this exact question was
already measured and adjudicated in-repo, twice, and the answer was recorded in
code rather than in the decisions-log** — which is why KR and galadriel both had
to rediscover it.

1. **`wr1_facing_probe.gd` (drax, WR1-ROOMS Block A fix 1, 2026-07-29)** measured
   the rig's forward off bone rests — shoulder line, hand line, head-hips lean,
   three readings, one dead reading reported as dead — and concluded **+Z
   forward**. Same symptom as here (Matt's eye said "facing backwards"; the
   0.0000° retarget metric could not see it).
2. **`mobcast_stride_probe.gd:264-283`** independently re-derived from the cross
   product and cross-checked against seven Synty clip labels: for a +Z-forward
   body, `right = forward × up = (0,0,1)×(0,1,0) = (-1,0,0)`, therefore
   **local +X is the body's LEFT.**

**These settle `king_rig.gd:191`, and against it.** KR's read that the comment is
internally inconsistent is correct and *understated*: `+Z forward` / `−X left`
does not merely fail to close on itself, it contradicts two independent in-repo
measurements. It also has a live shipped consequence — `_sword_yaw_left_deg :=
12.0` is built "toward the body's LEFT (−X)", so **the blade currently yaws to the
king's RIGHT**, i.e. Matt's CHANGE 1 of 2026-06-22 ("10–15 degrees left of
forwards") is mirrored in the shipped rig. That is a separate, smaller defect and
it should be ticketed separately, not folded into the S2 fix.

galadriel was right to decline the comment as dispositive. She stopped one step
short: the repo had already settled it elsewhere, with measurement.

---

## Q1 — RULING: galadriel's shape is right; her remedy needs a narrower name, and a sequence

**Both risks are real and neither dominates, because they are separable by
sequencing rather than by scope.** Land two commits:

- **Commit A (behaviour-changing, recapture-gated):** fix only the wrong sites —
  `s2a_stage:303`, `s2c_dash_attack:320`, `s2c_blink:285`, `s2c_teleport:258`,
  `s2c_leap_strike:282`, plus the non-mover rows' inherited-by-omission rest yaw.
- **Commit B (no-op refactor, separate):** introduce the single named helper
  (`face_toward(node, dir)`) and adopt it at the already-correct player-facing
  sites. **Those sites already compute `atan2(d.x,d.z)`; adopting the helper there
  is provably a no-op — verifiable by byte-identical re-render against pre-change
  captures.** A refactor whose no-op-ness is receipted is not a regression risk;
  it is a receipt (#75 — the instrument must bind the artifact that ships).

KR's stated fear — "a centralization that regresses working player-facing code to
fix a benchmark harness" — is legitimate and is exactly what Commit B's byte
identity check exists to refute. Do not let it argue for five scattered sign
flips; that fixes the symptom and preserves the trap, as KR says.

**⚑ CONDITIONAL BLOCK — a blanket flip of every `atan2(-x,-z)` in the repo must
not land.** Two reasons, both verified:

1. **The correct formula at a call site depends on whether the rig it yaws
   carries a body-level correction, and nothing at the call site says which.**
   `vh_caster.gd:78` sets `MODEL_FORWARD_YAW := 180.0` **at the body**,
   deliberately, "so callers need no change and the next room scene inherits the
   fix for free." For that rig family the `-Z` formula is **correct**. Flipping it
   re-opens the WR1 defect. (`s2a_stage` is safe to flip: it instantiates
   `KingRig` + `rig_mob_d2_skeleton.tscn`, neither of which carries a body-level
   correction — checked, not assumed.)
2. **Not every `atan2(-x,-z)` is a rig yaw.** `s2c_cone.gd:339` and
   `s2b_melee_arc.gd:359/450` use atan2 to construct fan vertices and to compute
   bearings; camera azimuths, shader azimuths and sim-heading conversions
   (`replica_playback`, `wr2_playback`, `kc2_baton`) are further non-yaw uses. A
   sign sweep over the token would corrupt geometry that is currently correct.

**Therefore the helper must carry, in its own docstring, the one fact that makes
it usable: it assumes a rig whose VISUAL forward is local +Z, and rigs corrected
at the body are out of its domain.** That sentence is the deliverable. The atan2
is incidental.

---

## Q2 — RULING: yes, a decisions-log entry is owed, and its absence is the root cause

The convention was settled by measurement on 2026-07-29 and recorded **only in
GDScript comments** — in two files, neither of which is an authority surface. The
result is precisely what the log exists to prevent: a third rediscovery, at the
cost of a 305-sample Jacobian fit and a 25-minute recapture. Entry filed
(`+Z forward / +X left / −X right`, with both probes named as evidence). I own
that file; this is within ADR-002 direct-approval authority.

---

## Q3 — RULING: this is a face of #80, not a new number

**#80:** *"A gate's GREEN is not evidence until that gate has been shown to go
RED, on this population, in this configuration."* KR's shape — a default
parameter value at which correct and incorrect implementations produce identical
output — is #80 with the insensitivity located in **a parameter value** rather
than in a detector. At `aim=0` the arm was *structurally incapable* of going red,
so its green was never evidence. The clause KR compared it to (5(b), gates
adopting keys by complement) is a different face; the headline rule already
covers this one.

What KR's framing adds, and what #80 does not currently say, is the **selection
pressure**: the degenerate value is the *default*, and defaults are what get run
most, so this failure mode is not merely possible but *preferentially* sampled.
That earns a sub-clause, not a number:

> **#80.x (candidate, pending ratification) — degeneracy at the default.** Where
> a gate has a default parameter value, check whether the correct and incorrect
> implementations coincide *at that value*. If they do, the default arm cannot go
> red and its green is not evidence for the whole population — and because the
> default is the most-run arm, this blindness is preferentially sampled. The gate
> must carry at least one off-default arm that separates them, and that arm's
> separating power must be stated.

Recording it as a candidate rather than minting it: KR offered it as a candidate,
#77's VACANT-BY-CONTAMINATION status shows this corpus takes numbering hygiene
seriously, and a sub-clause under a proven number is cheaper to cite than an
81st.

---

## Q4 — RULING: the seal split is CORRECT. Ratified, with one scope amendment

- **Determinism receipt SURVIVES.** Reproducibility is a property of the pipeline
  and is orthogonal to pose. A deterministic renderer that renders the wrong pose
  twice identically has proven exactly what it claimed. Correct.
- **Archetype separation verdicts MUST NOT SEAL.** Correct, and for a stronger
  reason than KR gave. The tempting counter-argument — "fx-on minus fx-off share
  the same wrong pose, so it differences out as common-mode" — **fails**:
  body-anchored effects emit along body-forward, so a 180° body rotates the
  effect region itself into different world space. galadriel's
  `cn_cathedral_fire_04-fan-full` frame (fan erupting out of the King's back) is
  the proof that it does not cancel. The contamination is not common-mode.
- **PENDING-RECAPTURE per #79 cl. 5(a) rather than FAIL** — correct. The
  measurement is not wrong, it is *about the wrong object*; FAIL would assert a
  defect in the effect that has not been shown.

**Scope amendment (the one thing to change):** KR scoped PENDING-RECAPTURE by
reference to silhouette-scored rows (`dash_attack` § 3.1.11 "silhouette +
knockback"). **Widen it to every row in which a body appears.** `s2a_stage:303`
mis-yaws *every staged mob on every row*, and the non-mover rows inherit the same
180° by omission. Sealing a non-silhouette row is still sealing a number taken of
a back — and per #25 it becomes inherited design substrate.

---

## On the two disclosed KR errors

Both are the narrow-instrument family (#79 cl. 6), both self-reported unprompted
and before the ruling. That is the behaviour the process is built to produce and
it does not reduce the weight given to KR's Q4 split — which I ratified after
independently checking it against the code, not on KR's authority. One note the
disclosure earns: the `defensive` ≡ control identity is **a passed receipt the
gate reports as data**, and the fix is one line of intent — the gate should
`assert` the predicted identity, not measure across it and publish the zero. An
unasserted prediction is indistinguishable from an unnoticed defect.

---

## Action

- [ ] **drax:** land Commit A (five sites + non-mover rest yaw). Do NOT blanket-flip.
- [ ] **drax:** land Commit B separately — `face_toward()` helper, docstring stating
      the +Z-forward domain and excluding body-corrected rigs; prove no-op by
      byte-identical re-render at the already-correct sites.
- [ ] **drax:** reconcile `king_rig.gd:191` — `+Z forward / +X left / −X right`.
- [ ] **drax (separate ticket, do not fold in):** `_sword_yaw_left_deg` currently
      yaws the blade to the king's RIGHT. Matt's CHANGE 1 asked for left.
- [ ] **drax:** recapture must include ≥1 off-default aim arm per #80.x.
- [ ] **knight-rider:** widen PENDING-RECAPTURE to all rows in which a body appears.
- [ ] **jack-ryan:** decisions-log entry — DONE.
- [ ] **Matt:** ratify #80.x, or rule it adequately covered by #80 as written.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/findings/2026-08-25-dash-attack-facing.md`
- `/Users/admin/Games/reincarnated-godot/scripts/wr1_facing_probe.gd`
- `/Users/admin/Games/reincarnated-godot/scripts/vh_caster.gd:47-78,120-123`
- `/Users/admin/Games/reincarnated-godot/scripts/mobcast_stride_probe.gd:264-283`
- `/Users/admin/Games/reincarnated-godot/scripts/king_rig.gd:187-194`
- `/Users/admin/Games/reincarnated-godot/scripts/s2a_stage.gd:270-303`
- `/Users/admin/Games/reincarnated-godot/scripts/s2c_cone.gd:339`
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md`
