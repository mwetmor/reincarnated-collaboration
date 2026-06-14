# Finding — 2026-06-14 — gamora-bc-coordinate-cutover-stage-2-implementation (DEV-MODE Gate-2, CODE gate)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS — all four structural checks independently CLEAN at source; one design ESCALATION routes to gandalf (which gamora already correctly raised in-commit). No BLOCK. No new INFO/WARN against the code.
**Target:** implementation commit `f494f5e`, tag `gamora/v-bc-coordinate-cutover-stage-2-1` (NOT pushed); folded math note `62f9adb`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam MIGRATION), 4 (decisions-log/contract truth), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #2, #7.8 (one-variable / behavior-preserving), #11 (empirical inspection over assumption), #12 (semantic-shift), #39 (no silent stub fallback / Pattern P7)
**Design contract:** gandalf §7.5 (parallel implementation-design review; this finding is process/discipline + measurement-validity only)

## Verdict (one line)

The implementation closes the smuggling-trap at the CODE level (not just the note), the tri-state is a genuine three-state, the legacy tables are demoted-not-deleted, INFO-1 holds, and the equivalence harness is valid gate evidence against the amended WARN-1a/1b criterion — 16/16 PASS at wr_d=0.00pp / L1=0.000 over 35.8k fights, with the over-wide legacy envelope honestly flagged and escalated. I verified every load-bearing claim at source rather than trusting the smoke-line. The only open item is gandalf's design call on the over-wide bc-collapse envelope, which gamora already escalated per the criterion — exactly the path WARN-1a specified.

---

## SMUGGLING-TRAP — independently CLEAN at the CODE (the primary structural check)

The disease-re-entry vector is closed in the implementation, not merely in prose:

- `bc_target_role_priority(bc_target)` (`ai_strategies.py:188-278`) takes ONLY the 8-tuple. There is no `archetype` parameter, no `element`/`substrate` parameter, and no read of either inside the body. It indexes only `bc_target[_BC_IDX_*]` (eng/geo/ctrl/tempo/var/def bins) and assembles the ordering from bin values alone.
- It NEVER computes the legacy label from the coordinate and NEVER indexes `ARCHETYPE_ROLE_PRIORITY`. The map is bins → ordering directly (math note §2.1 option-b), not bins → label → `ARCHETYPE_ROLE_PRIORITY[label]`.
- At the keying SITE in `get_priority_roles` (`:336-339`), when `bc_target is not None` and derives an ordering, the function `return`s the bin ordering and the label table is never consulted for that kit.
- At the `_common` control gate (`:452-464`), the bc-present branch keys control-first off `bin_ordering[0] == "control"` (i.e., off `ctrl_bin == "control-pure"`), NOT off `_PLAYER_CONTROLLER_ARCHETYPES` label membership. The label-membership branch is reached only in the `elif` (bc-absent).
- Test `test_pure_function_of_bins_not_archetype` (`test_stage2_bc_keying.py:109-112`) asserts the function signature carries no archetype/element lever and is a pure function of the tuple. I ran the file: 17/17 pass.

This is the structural close I was sent to verify. It holds in the code.

## TRI-STATE (Disc #12 + #39) — CLEAN, three genuine states, tables DEMOTED not deleted

`get_priority_roles` (`:336-387`) implements a strict three-state:
- **PRIMARY** (`:336-339`): `bc_target is not None` AND derives → bin ordering returned; label table not consulted.
- **MALFORMED-LOUD** (`:342-348`): `bc_target` present but does NOT derive (wrong shape) → `log.warning` naming a Stage-1 emission defect, then falls to label. This does NOT silently mask a Stage-1 bug — it is loud per Disc #39. Test `test_malformed_bc_warns_and_falls_back` confirms the WARN fires and the fallback is the label.
- **FALLBACK** (`:377-378`): `bc_target` absent AND archetype known → `ARCHETYPE_ROLE_PRIORITY[archetype]`, verbatim-unchanged. Test `test_fallback_label_when_bc_absent` confirms byte-identity with the legacy table.
- **LOUD-DEFAULT** (`:380-387`): `bc_target` absent AND archetype unknown → `log.warning` + `_REGISTRY_DEFAULT_PRIORITY`. Test `test_loud_default_unknown_archetype` confirms the WARN.

The present-vs-absent distinction is NOT collapsed to a silent default. `ARCHETYPE_ROLE_PRIORITY` (`:52-102`), `_PLAYER_CONTROLLER_ARCHETYPES` (`:45-50`), and the monster `_PREFERRED_BEHAVIOR_ROLES` (`:356-363`) all survive UNCHANGED as resident fallbacks. Nothing was deleted. Deletion remains correctly scoped to Stage 3 (commit body + MIGRATION v1.70 both state this). Demote-not-delete (Matt directive) holds.

## INFO-1 (player keying does NOT borrow the monster `is_player==False` branch) — CLEAN

The monster `preferred_behavior` branch in `choose_action` (`:402-406`) is still gated `preferred_behavior is not None AND ai_strategy=="scripted" AND not combatant.is_player`. Players (`is_player=True`, `ai_strategy="common"`) never enter it. Player bin-keying enters via `_common` (`:418`, control gate at `:452-464`) and via `get_priority_roles` (called from `_scripted` and `_common`'s downstream). No player sets `combatant.preferred_behavior`. INFO-1 from my math-note finding is honored exactly as required. Additionally, `get_priority_roles` checks `bc_target` BEFORE `preferred_behavior` (`:336` before `:365`), so the populations stay cleanly separated (players carry bc_target / no preferred_behavior; monsters the reverse).

## EQUIVALENCE HARNESS — VALID GATE EVIDENCE against the amended WARN-1a/1b criterion (the call Matt routed to me)

**Short answer: YES, the harness is valid gate evidence, and it measures what the amended criterion requires.** I verified the methodology at source (`scripts/gamora_stage2_bc_keying_equivalence_2026_06_14.py`), not from the summary line.

- **One-variable-clean (Disc #7.8):** `_run_arm` (`:139-173`) deep-copies the SAME generated kit, and arm A strips `bc_target` to force the demoted label fallback while arm B keeps it (real coordinate). Identical opponent panel, identical seed sequence (`770000 + fight`, advanced in lock-step over the same panel iteration), identical kit. ONLY the keying SOURCE differs between arms. This isolates the keying mechanism as the sole variable — correct.
- **Named fixed opponent set (WARN-1b):** the panel is explicit — `boss/brute/physical@50` + `boss/brute/fire@50` (`:188-190`), deterministic (seeds 1/2), reproducible, recorded in the artifact. The under-specification I flagged in the math-note gate is resolved.
- **Full-N powered above noise / smoke-vs-gate separation (WARN-1b):** `--milestone` runs N=1120/arm/archetype; the artifact `mode=MILESTONE`, `n_fights_per_arm_per_archetype=1120`. 16 archetypes × 2 arms × 1120 = ~35.8k fights. The script explicitly distinguishes SMOKE (N=30, sanity-only) from MILESTONE gate (`:177-179`, `:283`). The ±3pp / ±5% / L1≤0.10 band is applied as the milestone gate (`:56-59`, `:216-220`). Correct per WARN-1b.
- **No row-duplication / single-variable isolation:** each fight is a distinct `from_player_class(kit)` + `from_monster(m)` build with a unique seed; no row is reused across arms. The `action_trace` role-frequency instrument is a pre-existing append-only side-channel sink passed identically to both arms — it does not alter fight behavior, so it is neutral to the comparison. Verified `action_trace` is opt-in instrumentation in `search_estimator.py:691-692/783-784`, not a behavioral lever.
- **Measures what the gate requires:** role-firing-frequency L1 is the load-bearing discriminator. Many archetypes lose to boss-tier@50 in BOTH arms (e.g., water_mage wr=0.000/0.000, earth_caster 0.002/0.002) — win-rate alone could not discriminate piloting there. But role-freq L1=0.000 across all 16 proves the EMITTED piloting (which skills fire, in what proportion) is byte-identical between label-keyed and bin-keyed arms. That is the correct equivalence signal: identical inputs to `choose_action` produce identical fights. Result: 16/16 PASS at wr_d=0.00pp / ttk_d=0.00% / L1=0.000.

**The over-wide envelope (WARN-1a) — real, correctly handled, correctly ESCALATED:** the artifact's `envelope_width_blocks` reports the legacy intra-group spread for the water/earth/holy/shadow damage-long collapse group: `W_winrate=3.84pp`, `W_ttk=24.42%`, `W_rolefreq_l1=0.254`, `within_cap=False`, `escalated_to_gandalf=True`. This is exactly the WARN-1a path: the criterion (i) reports the legacy envelope width FIRST, (ii) caps it at the tolerance band, and (iii) escalates the over-wide case to gandalf rather than auto-passing it as "within envelope." gamora did not certify the over-wide group as PASS on the group test — she escalated it AND demonstrated that the PER-MEMBER L1=0 (each of water/earth/holy/shadow reproduces its OWN legacy fight exactly) is the operative equivalence evidence. I confirmed the per-member L1=0 is real in the artifact: every one of the four collapse members shows `role_freq_l1=0.000` and `winrate_delta_pp=0.00` in `per_archetype`. The width is among the LEGACY members (different element skill magnitudes via the DPS-sort), NOT a divergence bin-keying introduces — bin-keying reproduces each member's legacy fight exactly. That mechanism claim (Disc #11) is borne out by the data.

**On gamora's argument that per-member L1=0 supersedes the group-envelope test:** the MEASUREMENT is valid and I confirm the per-member L1=0 is real and is the correct operative equivalence gate for the cutover question ("does bin-keying reproduce label-keying?"). Whether a single canonical damage-core ordering is DESIGN-acceptable for four elements whose legacy fights span 24% TTK is gandalf's lane, not mine — and gamora routed it there per the criterion. The measurement-validity half (mine) clears; the design-acceptability half (gandalf's) is the open ESCALATION.

## INFO ITEMS FROM THE MATH-NOTE GATE — all folded

- **INFO-2 (production-path round-trip):** `TestProductionPathRoundTrip` (`test_stage2_bc_keying.py:141-176`) drives the LIVE `ClassGenerator.generate` → `from_player_class` → `CombatantState.bc_target` path (not a hand-built CombatantState). Confirms the coordinate-composed kit carries bc_target end-to-end and the bc-stripped kit falls back to the label path unchanged. Production-path, as required.
- **INFO-3 (mixed ctrl_bin branch):** the `mixed` branch (`:259-260`) is implemented AND exercised by `test_mixed_control_mid_rotation_not_first` (`:78-84`) even though `mixed` does not occur in the 16 elemental set. The latent-branch gap I flagged is closed by a dedicated fixture. Good.
- **INFO-4 (gate table as committed file):** the §3.3 per-archetype gate table is committed as `output/stage-2-bc-keying-equivalence-2026-06-14.{json,txt}`. Evidence is on disk, not just inline. Confirmed.

## A1 (load-bearing, gandalf §3.2.1) earth_caster classification — measurement CONFIRMED

The artifact records `control_freq_label_keyed=0.0000` for earth_caster at N=1120 (`per_archetype` + txt line 9). The composed earth_caster kit carries zero control skills (`test_a1_earth_caster_no_control_skills` confirms `"control" not in roles` at the production path), so the legacy table's control-LEAD fires at frequency exactly zero — dropping it under damage-pure binning is behavior-identical (case-2 legacy-label over-claim). The empirical basis for the A1 CLEAN-ACCEPT is real in the data. The DESIGN ruling on A1 (case-2 accept, no rocket item) is gandalf's §3.2.1 lane; the measurement that grounds it is sound.

## PRINCIPLE 6 / MIGRATION.md — CLEAN

MIGRATION.md v1.70 documents the cross-seam `bc_target` consumption (rocket→gamora) onto `CombatantState`: additive-nullable field, defensive `getattr` at `from_player_class`, brownfield-safe, star-lord/telemetry impact explicitly NONE (internal-to-seam, no schema column, not surfaced in FightResult). The field is additive-nullable on the CONSUMER side (`combatant.py:233` `bc_target: list[str] | None = None`; propagation `:754` `getattr(player_class, "bc_target", None)`), so the boundary does not break for pre-Stage-1 PlayerClass instances. The production-path round-trip smoke is present (Principle 6 Gate-2 check satisfied — INFO-2 above). Principle 3 + Principle 6 both satisfied.

## SMOKE-GATE (Principle 2 / Disc #2) — PRESENT

The commit message carries the smoke-line: equivalence 16/16 PASS @ N=1120/arm (wr_d=0pp, ttk_d=0%, L1=0.000); unit+round-trip 17/17; regression 158/158. I independently re-ran `test_stage2_bc_keying.py` → 17/17 pass. The broader engine `tests/` suite (146 test files) is heavier than gamora's scoped 158-marker regression and was still running at finding-authoring time; the AFFECTED-SEAM evidence (Stage-2 file 17/17 + the independently-inspected 35.8k-fight equivalence artifact) is the gating evidence and is clean. The full-suite count is corroborating, not gating, and showed no failures in progress. If any cross-seam regression surfaces in the full run, it would be a new finding — but the seam-local and equivalence evidence already clear this gate.

## Action

- [x] Developer (gamora): smuggling-trap closed at code, tri-state genuine, demote-not-delete, INFO-1 honored, INFO-2/3/4 folded, harness valid, WARN-1a envelope reported+capped+escalated. Nothing further required from gamora at this gate.
- [ ] gandalf (parallel design review): the over-wide bc-collapse envelope (water/earth/holy/shadow, W_ttk=24.4% / W_rf=0.254) is ESCALATED to you per the WARN-1a criterion. Measurement-validity (mine) clears: per-member L1=0 is real and is the correct cutover-equivalence gate. The DESIGN question — is a single canonical damage-core ordering acceptable for four elements whose legacy fights span 24% TTK, or does the coordinate genuinely fail to carry a behavior the label carried? — is your §7.5 call. This is the only open item.
- [ ] Matt: no decision needed at THIS gate (no BLOCK; the ESCALATION is design-lane to gandalf, not an architectural BLOCK to you). Tag is intermediate seam-prefixed (`gamora/v-bc-coordinate-cutover-stage-2-1`) and unpushed — milestone tagging (dropping the seam prefix) + push remain yours per ADR-002/ADR-003/ADR-006 when Stage-2 closes alongside gandalf's design clearance.

## May the implementation be considered Gate-2 PASS?

**YES — PASS-WITH-AMENDMENTS.** The code closes the disease re-entry vector structurally, the tri-state and demote-not-delete contracts hold in the implementation (not just the note), INFO-1/2/3/4 are folded, and the equivalence harness is valid one-variable gate evidence that measures the correct equivalence signal (role-freq L1) at full statistical power. The single open item is gandalf's design-acceptability call on the over-wide legacy envelope — which gamora correctly escalated per the criterion rather than laundering as a group-envelope pass. No BLOCK; no Matt escalation from the process/measurement side.

## References

- Implementation: `src/reincarnated/simulation/ai_strategies.py` (`:45` `_PLAYER_CONTROLLER_ARCHETYPES` demoted, `:52-102` `ARCHETYPE_ROLE_PRIORITY` demoted-unchanged, `:188-278` `bc_target_role_priority` bins-only, `:281-387` `get_priority_roles` tri-state, `:402-406` monster `is_player==False` gate, `:452-464` `_common` control-gate tri-state)
- Implementation: `src/reincarnated/simulation/combatant.py` (`:226-234` `bc_target` field additive-nullable, `:749-755` `from_player_class` propagation via defensive getattr)
- Tests: `tests/test_stage2_bc_keying.py` (17/17 re-run PASS; smuggling-trap, tri-state, INFO-2 production-path round-trip, INFO-3 mixed branch, A1 earth_caster)
- Equivalence harness: `scripts/gamora_stage2_bc_keying_equivalence_2026_06_14.py` (one-variable arm-A-strip/arm-B-keep; named panel; smoke-vs-milestone separation; envelope-width block)
- Artifacts: `output/stage-2-bc-keying-equivalence-2026-06-14.{json,txt}` (MILESTONE N=1120/arm; 16/16 PASS wr_d=0.00/ttk_d=0.00/L1=0.000; envelope W_ttk=24.42%/W_rf=0.254 within_cap=False escalated_to_gandalf=True; per-member L1=0 confirmed)
- MIGRATION: `src/reincarnated/simulation/MIGRATION.md` v1.70 (CombatantState.bc_target; cross-seam rocket→gamora; star-lord impact NONE)
- Math note (folded): `src/reincarnated/simulation/math/bc-coordinate-cutover-stage-2-ai-bin-keying-2026-06-14.md` @ `62f9adb`
- Prior gate: `agentic_orchestration/qa/findings/2026-06-14-gamora-bc-coordinate-cutover-stage-2-math-note-gate-2.md` (WARN-1a/1b + INFO-1/2/3/4 source)
- Companion design ruling: `agentic_orchestration/gandalf/notes/2026-06-14-class-generator-bc-target-cutover-ruling.md` (§7.5 — gandalf's parallel review)
