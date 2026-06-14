# Stage-2 IMPLEMENTATION review — BC-coordinate cutover AI bin-keying (A1 re-confirm + WARN-1a ruling)

**Type:** §7.5 implementation gate (gandalf seam) — the implementation-half of the Stage-2 critique pair (jack-ryan runs Gate-2 DEV-MODE in parallel).
**Date:** 2026-06-14
**Author:** gandalf
**Verdict:** **PASS.** A1 re-confirmation: **CONCUR CASE-2** (legacy-label over-claim; clean accept; no rocket item). WARN-1a ruling: **NON-ISSUE — per-member exact-equivalence is the operative gate; the over-wide legacy group envelope is a pre-existing element-magnitude spread bin-keying does NOT touch and does NOT widen.** No fold-before-land amendment.
**Reviewed:**
- Implementation: commit `f494f5e`, tag `gamora/v-bc-coordinate-cutover-stage-2-1` (not pushed).
- Folded math note: commit `62f9adb`.
- Equivalence artifacts: `~/Games/reincarnated-engine/output/stage-2-bc-keying-equivalence-2026-06-14.{json,txt}` + harness `scripts/gamora_stage2_bc_keying_equivalence_2026_06_14.py`.
- Implementation source: `simulation/ai_strategies.py` (`bc_target_role_priority`, `get_priority_roles` tri-state, `_common` control gate), `simulation/combatant.py:235/756` (field + propagation), `generation/archetype_composer.py` (composition chain for the A1 verification).
**Against:** my math-note review (`2026-06-14-stage-2-math-note-review-bc-collapse-ruling.md`, commit `0d89e1a`) — §A1 (the load-bearing amendment) and §B disposition (gate sequence: "gandalf re-confirms A1 resolution at implementation review").
**Empirical grounding (not ruled blind, §7.8):** verified the composition chain at source AND the equivalence-run JSON per-archetype record for earth_caster directly (not from gamora's summary).

---

## 0. TL;DR

The implementation is faithful to the §7.5 contract and to my math-note rulings. The smuggling trap is closed in code exactly as ruled (the keying function reads only bins, never the label, never element/substrate). The tri-state partitions populations by coordinate PRESENCE, not by label inspection. A1 — the one load-bearing amendment I reserved for this gate — resolves CLEAN CASE-2 against decisive source evidence: the earth_caster kit physically carries zero control skills, so the legacy control-LEAD was the form-bias pathology in its purest demonstrable form (a flat label claiming mechanics the kit never delivered). WARN-1a is correctly framed by gamora and is a non-issue: per-member L1=0 is the operative gate; the over-wide group envelope is a property of the LEGACY members' differing element magnitudes, not a divergence bin-keying introduces. **PASS, no amendment.**

---

## 1. JOB 1 — A1 re-confirmation: CONCUR CASE-2 (clean accept, no rocket item)

My math-note §A1 required: split control-axis members out of the Type-D flavor group; classify earth_caster as either CASE-1 (Stage-1 source mis-bin → route to rocket, hold out of clean-accept) or CASE-2 (legacy-label over-claim → accept + document); decide using the §3.1 role-frequency evidence. gamora's verdict is CASE-2. **I CONCUR, and the evidence is stronger than "control fires rarely" — it fires NEVER, by construction.**

### 1.1 The decisive evidence — verified at source, not from summary

**(a) The composition chain proves the kit cannot contain control.** `earth_caster` is the backward-compat alias for the `(earth, area_damage)` substrate×role pair (`archetype_composer.py:80`). Its composition role is therefore `area_damage`. `_REQUIRED_ROLES["area_damage"]` (`archetype_composer.py:142-144`) = `[(primary_attack,1), (burst_damage,1), (area_damage,1)]` — **no `control` row exists.** The composed earth_caster kit physically cannot contain a control skill. This is the generation-side ground truth, and it is FROZEN Stage-1 — exactly the boundary my §A1 said gamora must not reach into.

**(b) The equivalence-run JSON confirms zero control firing.** earth_caster's `label_role_freq` (arm A, label-keyed) is `{primary_attack: 0.671, area_damage: 0.209, burst_damage: 0.119}` — **the `control` key is ABSENT, not merely small.** The legacy `ARCHETYPE_ROLE_PRIORITY["earth_caster"] = [control, area_damage, burst_damage, primary_attack]` leads with control, but the AI iterates the priority list and skips any role with no matching available skill. Control rank-1 finds nothing, the rotation proceeds to area_damage, and `control_freq_label_keyed = 0.0000`. The bin arm is byte-identical (`role_freq_l1: 0.0`). Dropping the control-lead under `ctrl_bin=damage-pure` is therefore not "approximately behavior-preserving" — it is **exactly** behavior-identical, because the control-lead was already inert in the legacy path.

### 1.2 Is 0.0000 control-fire the CORRECT and SUFFICIENT evidence for label-over-claim (not a generation mis-bin)? — YES.

This is the specific question I posed for myself at this gate, and the answer is unambiguous. The two cases in my §A1 are distinguished by whether the kit's *actual composed skills* are control-meaningful:

- **CASE-1 (mis-bin)** would obtain if earth_caster's composed skills CONTAINED control and the kit genuinely wanted to fire CC first, but Stage-1 binned it `damage-pure` in error. The diagnostic would be: control fires with meaningful frequency under label-keying AND materially shapes the fight.
- **CASE-2 (over-claim)** obtains if the composed skills do NOT contain a control-dominant kit — the control-lead in the table was the LABEL asserting an identity the skills never honored.

The 0.0000 frequency is sufficient to discriminate BECAUSE it is sourced from two independent layers that agree: (i) the composition contract makes control structurally impossible in this kit (`_REQUIRED_ROLES` has no control row for `area_damage`), and (ii) the emitted fight confirms control never fires. There is no scenario consistent with CASE-1 here — a mis-bin would require the kit to contain control skills that the coordinate then suppressed, but the kit contains none to suppress. The coordinate `ctrl_bin=damage-pure` is the FAITHFUL reading of a kit with no control skills, not an erroneous one. **This is CASE-2, cleanly, and there is NO rocket item — the Stage-1 binning is correct, not defective.**

The form-bias framing lands exactly: the `earth_caster` label over-claimed a control identity its mechanics never delivered. The cut exists precisely to stop labels from carrying mechanical claims the coordinate doesn't honor; here the cut DROPS an over-claim that was already inert, with zero behavioral cost. That is the cut doing its designed job.

### 1.3 The `*_controller` / `*_caster` audit — confirmed faithful

The equivalence-run `ctrl_axis` column shows all 7 `*_controller` tags (fire/water/earth/wind/lightning/holy/shadow) pass at L1=0.000 with `ctrl_axis=n/a` — they bin `control-pure`, their legacy tables lead with control, and they DO contain control skills (their composition role is `control`, `_REQUIRED_ROLES["control"]` carries `(control,2)`). Their control-lead is FAITHFUL, not an over-claim, and bin-keying reproduces it. earth_caster was the sole split member (the only `*_caster` whose legacy table led with control while its composition role was `area_damage`), and it resolves clean. The audit my §A1 demanded ("audit `*_caster`/`*_controller` whose legacy table leads with control but whose Stage-1 coordinate bins damage-pure") found exactly one member, and it is CASE-2. **The boundary I tightened in §A1 held: no discriminating-axis deviation rode into the instrument wearing a Type-D label.**

---

## 2. JOB 2 — WARN-1a over-wide-envelope ruling: NON-ISSUE (per-member exact-equivalence supersedes)

**RULING: gamora's framing is SOUND. Per-member exact-equivalence (L1=0 per archetype) is the correct and operative behavior-preservation gate. The over-wide legacy group envelope (W_ttk=24.4%, W_rf=0.254) does NOT expose a design concern that needs resolution before this lands. It is a property of the legacy members themselves, not a divergence bin-keying introduces — and bin-keying provably does not widen it.**

### 2.1 Why per-member exact-equivalence is the operative gate here

My math-note §2.3 endorsed the envelope framing as the right handling **for the collapse** — i.e., when the single bin-derived ordering CANNOT list-match all three members, you require it to land WITHIN the band the members already span, rather than privileging an arbitrary member. That framing presumes the bin ordering DIVERGES from individual members' fights. But the equivalence run shows the stronger result actually obtained: **bin-keying reproduces each member's legacy fight EXACTLY (per-member L1=0.000, wr_d=0.00pp, ttk_d=0.00%).** When the bin ordering matches each member exactly, the group-envelope test is moot — you don't need to prove the collapse lands within the band when you've proven it reproduces every member point-for-point. The per-member L1=0 is the strictly stronger evidence and it supersedes the envelope test. gamora's §3.1 framing (per-member L1=0 supersedes group within-envelope) is correct.

### 2.2 Why the over-wide legacy envelope is not a design concern at THIS gate

The W_ttk=24.4% / W_rf=0.254 spread is measured among the **arm-A (label-keyed legacy) outcomes** of water/earth/holy/shadow damage casters. It is the spread the legacy members ALREADY produce against each other — caused by different element skill magnitudes flowing through the `_common` DPS-sort (different elements roll different damage numbers, so their TTK and role-firing mix differ even at the same coordinate). This spread:

1. **predates this cut entirely** — it is present in arm A, which IS the legacy path;
2. **is not introduced or widened by bin-keying** — arm B reproduces each member exactly, so the bin-keyed group spread equals the label-keyed group spread (the cut is spread-neutral);
3. **is the correct one-variable scope discipline** (§7.8) — fixing the element-magnitude spread would be a CONTENT change (diversification / element re-balance), explicitly out of scope for this pipe change. Bundling it would re-create the cert-wave one-variable error: a regression couldn't be attributed.

This is Discipline #11 (report-don't-force) operating correctly: gamora MEASURED the over-wide envelope, ESCALATED it per the WARN-1a criterion rather than silently tuning it, and routed the design call to me. The right design call is: **the spread is real, it is a legacy property, and it is OUT OF SCOPE for the cutover.** It does not block landing.

### 2.3 Does the over-wide spread expose a design concern worth tracking? — Yes, but as a deferred element-magnitude observation, NOT a Stage-2 blocker.

The 24.4% TTK spread among same-coordinate damage casters is worth a note for the record: it says that at a single BC coordinate (`ranged-slow, large-AOE, solo, damage-pure, medium, flat, mitigator, overflow`), the element-magnitude differences alone move TTK by ~a quarter. That is a legitimate balance signal — but it belongs to the **element-skin / diversification workstream** (Phase-5 cohesion-judge owns element re-skin; the recompose band owns magnitude). It is NOT a discriminating-axis problem and NOT a keying problem. I register it as a deferred observation: **when the element-magnitude / diversification pass runs, the same-coordinate intra-element TTK spread (~24% observed here) is a calibration target.** The empirical criterion that would re-open it is the diversification workstream firing, not anything in this cutover. It does not gate Stage 2.

---

## 3. Faithfulness of the IMPLEMENTATION to the math-note contract (spot-checks beyond the two jobs)

- **Smuggling trap (code-level):** `bc_target_role_priority` (`ai_strategies.py:188-278`) reads `bc_target[_BC_IDX_*]` bins ONLY — never `archetype`, never element/substrate. Confirmed against my §7.5 ruling and the math-note §2.1/§2.5 traps. The function returns `None` on absent/malformed (tri-state honesty), and the caller (`get_priority_roles:336-348`) emits a LOUD WARN on malformed-present rather than silently masking a Stage-1 defect. Trap closed in code.
- **Tri-state partition by PRESENCE not label:** `get_priority_roles` checks `bc_target is not None` FIRST (`:336`); a coordinate-composed kit never touches `ARCHETYPE_ROLE_PRIORITY`. bc-absent + known label → unchanged legacy table (`:377`). bc-absent + unknown → registry default + WARN (`:380`). Matches §4 exactly.
- **Control gate keyed off coordinate:** `_common` (`:452-464`) keys control-first off `bin_ordering[0] == "control"` (i.e., `ctrl_bin==control-pure`) when bc present; falls back to `_PLAYER_CONTROLLER_ARCHETYPES` membership only when bc absent. This is the one-variable change — ONLY the control-gate keying SOURCE shifts (label→coordinate); the damage-core DPS sort below is held identical. Faithful to §2.3.1.
- **Field propagation brownfield-safe:** `CombatantState.bc_target` (`combatant.py:235`) defaults None; `from_player_class` uses `getattr(player_class, "bc_target", None)` (`:756`) so pre-Stage-1 PlayerClass instances degrade to None → demoted label fallback. No crash on old kits. Matches §2.4.
- **Generation untouched:** the change is confined to `ai_strategies.py` + `combatant.py` (the instrument). compose_kit/source/adapter not reached. §7.6 staging held — Stage 2 migrates the instrument and FREES (does not delete) the legacy tables; deletion is Stage 3.
- **A3 kept separate:** the equivalence run is the AI-keying experiment only; composition-fidelity (A3) stays on the generation side per §5. Correct.

---

## 4. Disposition

- **VERDICT: PASS.** The implementation is faithful to §7.5/§7.6/§7.8/§7.9 and to my math-note rulings. No fold-before-land amendment.
- **A1 re-confirmation: CONCUR CASE-2.** Legacy-label over-claim, clean accept, NO rocket item. Evidence is decisive and two-layered: (i) `_REQUIRED_ROLES["area_damage"]` structurally excludes control from the earth_caster kit; (ii) `control_freq_label_keyed=0.0000` (control key absent from `label_role_freq`, not merely small). The 0.0000 frequency IS the correct and sufficient discriminator — a mis-bin (CASE-1) would require control skills to suppress, and the kit contains none. The cut drops an already-inert over-claim at zero behavioral cost. The `*_controller`/`*_caster` audit confirmed earth_caster was the sole split member; all 7 `*_controller` tags bin control-pure faithfully. The boundary my §A1 tightened held.
- **WARN-1a ruling: NON-ISSUE.** Per-member exact-equivalence (L1=0.000 on all 16) is the operative gate and supersedes the group within-envelope test. The over-wide legacy envelope (W_ttk=24.4%, W_rf=0.254) is a pre-existing element-magnitude property of the LEGACY members, not a divergence bin-keying introduces — bin-keying is spread-neutral (arm B reproduces arm A exactly). Resolving it is a CONTENT change (diversification / element re-balance), out of scope for this one-variable pipe cut (§7.8). gamora's report-don't-force escalation (Disc #11) was the correct handling. Does NOT block landing.
- **Deferred observation (not a blocker):** the ~24% same-coordinate intra-element TTK spread is a legitimate calibration signal for the element-magnitude / diversification workstream (Phase-5 element-skin + recompose band own it). Empirical criterion to re-open: the diversification pass firing. Not gated to Stage 2.
- **Gate sequence:** jack-ryan Gate-2 DEV-MODE runs in parallel (his seam: the tolerance numbers' composition with the recompose band, code-quality, regression integrity). This note is the design-half PASS. Stage-3 deletion (legacy table removal, the irreversibility step) remains gated per my §7 ruling — NOT in scope here.
- **Push gate (standing, Matt-gated):** this review note is push-ready pending Matt authorization; NOT pushed. The implementation tag `gamora/v-bc-coordinate-cutover-stage-2-1` is also not pushed (gamora's gate halt).

---

**Signed:** gandalf, 2026-06-14
**For:** the Stage-2 AI-bin-keying IMPLEMENTATION gate — the instrument now MEASURES the kit it is given, not the label it once wore. A1 closed CASE-2 on decisive structural-plus-emitted evidence: the earth_caster control-lead was a flat label claiming mechanics the kit never carried, and the cut drops it at zero cost — the form-bias pathology caught and retired exactly where §7.5 ruled it should be. WARN-1a is a legacy-magnitude shadow the cut neither casts nor deepens; it belongs to a later workstream. PASS.
