# Dispatch — 2026-05-16 — gamora — Modifier range investigation (post-B10.4 Option 2)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 (yellow-flag follow-up from B10.4 Option 2 close)
**Status:** COMPLETE
**Estimated effort:** 1 session (~2-3 hours); math-before-code investigation; mitigation proposal but not necessarily mitigation execution in-session.
**Acceptance:** Math note describing the empirical picture; root-cause hypothesis with evidence; mitigation path proposed (in scope to ship if small AND root-cause unambiguous; otherwise file findings + queue follow-on).

## Context — the yellow flag

B10.4 Option 2 full regen (`v1.3-b10-4-swarm-calibration`) produced **10/10 convergence** but with **modifier range 0.09–0.52** — substantially below the file 29 target of **0.85–1.15**.

Gamora's note from B10.4 close: *"not a regression — same state existed before Option 2; now visible because convergence actually works."* The implication is that under the prior 2/10 convergence regime the issue was masked; Option 2 made it surface.

Flagged in `skill_handoff_2026-05-16.md` as "Yellow flag — modifier range outside target band" and as "worth investigation before B10 V2 begins."

## What the math should resolve

This is a math-before-code investigation (Discipline #1). Three nested questions:

### Q1 — Is the 0.09–0.52 range a true class-overtuning indicator, or an artifact of the convergence semantic change?

Under B10.4 Option 2, convergence binary-search now operates on `convergence_winrate` (non-pack WR) instead of overall WR. The `final_modifier` value emerges from where the binary search lands. Two possibilities:

- **(a) Class overtuning.** Classes generate with too-high baseline power vs the non-pack target; binary search has to apply a low modifier (0.09–0.52) to dial them down to 50% non-pack WR. Implies the generation-side inputs are mis-scaled relative to the simulation's calibration.
- **(b) Artifact of semantic shift.** The 0.85–1.15 target band in file 29 was set against the prior overall-WR semantic. Under Option 2's non-pack semantic, the equivalent in-band might be different. The 0.85–1.15 target may no longer be the right band to compare against.

Resolving Q1 likely requires running the convergence math in both semantics to see what range would emerge if file 29's target were re-stated in Option 2 terms.

### Q2 — Does the wide-low-modifier range survive B7's variance-percentile check?

File 29's B7 specifies a pass/fail gate at 50th/75th/95th/99th percentiles of class power. The B7 work hasn't fully landed yet (Stage A2 item). But the math is conceptually applicable now: if classes have modifier 0.09–0.52, what's the percentile spread of their final effective power? Are the percentiles within the B7 gate, or is the modifier compression masking a wider underlying spread?

This question may need partial B7-style telemetry queries against `season_001005` data.

### Q3 — Structural cause: input stats or skill power-budgets?

If the answer to Q1 is (a) overtuning, then the next question is WHICH input is overtuned:
- Class-stat distributions (per Stage A1 lock — stats sum to 270; per-class allocations are auto-assigned)
- Skill power budgets (per-skill `scaling_coefficient` engine-determined)
- Both interacting

Trace the math from generation inputs through simulation to find where the overshoot originates.

## What to produce

Math note + findings file. Specifically:

0. **Step 0 — Verify the WR semantic provenance of the 0.85–1.15 band BEFORE running any telemetry queries.** Read `canonical/29-design-overview.md` § "Design philosophy: shaped balance over numeric scaling" + the 2026-05-16 View A lock entry in `decisions-log.md` (line 1206+). If the band was aspirational/conceptual (not simulation-calibrated under any specific convergence semantic), state this explicitly in the math note and adjust the comparison framing accordingly. This may collapse Q1 to a decisions-log update + new target band, rather than a balance investigation. Five-minute read; prevents 30-minute analysis against a mismatched benchmark.



1. **Empirical picture** — Query `data/telemetry.db` for season_001005 modifier distribution; cross-reference with prior seasons (001001-004) to see if this is season-specific or roster-wide.
2. **Q1 resolution** — Concrete evidence whether 0.09–0.52 is overtuning vs semantic artifact. If overtuning, characterize magnitude.
3. **Q2 resolution** — Spot check whether B7-style percentile spread is in-band.
4. **Q3 resolution** — Locate the structural cause (if Q1 lands as overtuning).
5. **Mitigation proposal** — One of:
   - **(a)** Generation-side calibration adjustment (rocket dispatch territory if so)
   - **(b)** Simulation-side target band update (your seam; small change)
   - **(c)** Both
   - **(d)** Some other structural fix surfaced during investigation
   - **(e)** "Wait for Stage A2's B14 multi-band sim to land; this becomes moot" — if applicable, justify

## What this investigation does NOT do

- **No code modifications to `balance_loop.py` or related sim files** unless the mitigation is small AND the root cause is unambiguous AND the fix is genuinely your seam (i.e., simulation tuning). If root cause is in rocket's seam (class generation), file findings and queue a rocket dispatch.
- **No full regen.** The 10/10 convergence regen from B10.4 Option 2 is the empirical baseline. Re-running just to confirm the modifier range numbers is wasteful — query the existing telemetry DB.
- **No engagement with B7 variance-percentile gate implementation.** That's Stage A2 item; this investigation just uses B7-style queries as evidence.

## Required reading

- `simulation/math/b10-4-option-2-convergence.md` (your own math note from B10.4)
- `design/decisions/decisions-log.md` 2026-05-16 entries (View A lock; B10.2 supersession; reference what convergence_winrate semantics mean)
- `canonical/29-design-overview.md` (the source for the 0.85-1.15 target band; verify whether the target framing was overall-WR or non-pack-WR pre-Option-2)
- `src/reincarnated/simulation/balance_loop.py` (Option 2 implementation; understand which modifier the binary search emits)
- `src/reincarnated/simulation/validation_report.py` (in-band check uses `convergence_winrate`)
- `design/b10-gauntlet-analysis.md` § 15 (your own full regen findings; the 0.09–0.52 data point)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_b14_5_sidecar_analyses.md` (hunter modifier-range 1.82 finding from earlier sidecar analyses; cross-reference)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #11 (attribution), #12 (semantic-shifting — especially relevant since this question IS about a semantic shift)

## Cross-seam considerations

- **Rocket seam (potential):** If Q3 root cause lands in class generation, knight-rider authors a rocket dispatch with your findings as input. Don't touch generation/.
- **MIGRATION.md:** If the answer changes any simulation-output semantic that drax/star-lord consume, MIGRATION.md needs an entry. Likely NOT for an investigation pass; may be for a follow-on mitigation.

## Open questions for gamora to resolve during investigation

- The file 29 target band 0.85–1.15: was that authored under overall-WR semantics or non-pack semantics? If overall-WR, the comparison to Option 2 modifier output is apples-to-oranges; resolve the right comparison band first.
- The hunter modifier-range 1.82 finding from `project_b14_5_sidecar_analyses.md` — is that the same phenomenon being looked at here, or a separate axis (hunter-archetype-specific cross-seed range vs overall modifier scale)? **Note: the 1.82 figure is cross-seed modifier range (consistency axis, Discipline #10 attribution territory), separate from the 0.09–0.52 calibration-level (Discipline #12 semantic-shift territory). Confirm whether it's a compounding factor or an orthogonal axis, then record the distinction explicitly in the math note** — don't conflate the two phenomena.

## Acceptance criteria

- [ ] Math note describing the empirical picture filed (at `simulation/math/` or equivalent)
- [ ] Q1/Q2/Q3 each have explicit resolution (or noted as "couldn't resolve, here's what's needed")
- [ ] Mitigation proposal with rationale (one of (a)-(e) above)
- [ ] Findings file at `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`
- [ ] If shipping mitigation in-session: smoke test + tag + MIGRATION.md if cross-seam
- [ ] Knight-rider notified at completion with mitigation status + cross-seam implications

---

## Completion record

**Completed:** 2026-05-16  
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md`  
**Findings file:** `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`  
**Q1 resolution:** NOT semantic artifact, NOT generation overtuning. Root cause is sim-side energy mechanics (rage starts at 0 vs mana starts full; physical miss rate ~15%; armor ~18.6% vs elemental resistance ~0%). Key negative finding: both hybrid_mage and physical_warrior use identical tier 25–50 skills with nearly equal estimated DPS at mod=1.0 (~77k each).  
**Q2 resolution:** B7 concern noted for planning (low-modifier state amplifies relative gear affix impact). Non-blocking.  
**Q3 resolution:** Three compounding sim-side factors produce ~3–5× DPS-per-modifier disadvantage for physical rage classes. See math note §4.3 for derivation.  
**Mitigation status:** Option (e) — no code changes. Wait for B6 generation (energy-type-aware tier assignment) + B14.5 V2 energy-type levers. Calibration epoch declared: 0.09–0.52 is the B10.4 Option 2 operational baseline (mean |mod-1.0| ≈ 0.82).  
**Notes for knight-rider:** Two follow-on actions needed: (1) Author rocket dispatch for B6 pre-work: "energy-type-aware skill tier assignment" — rage/physical archetypes need ~1.5–2× higher tier bounds in templates to compensate for sim-mechanical disadvantages documented in math note §4.3. (2) Star-lord summary_formatter.py fix (convergence_winrate vs actual_winrate) remains open from B10.4 close. No Gate 1/Gate 2 review needed for this investigation deliverable — no design decisions changed, no code changed.
