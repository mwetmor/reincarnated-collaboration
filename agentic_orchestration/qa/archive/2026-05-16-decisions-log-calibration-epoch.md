# Decisions-log entry draft — Calibration epoch declaration (B10.4 Option 2 modifier baseline supersedes file 29 aspirational target band)

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source:** gamora's modifier-range investigation (math note `simulation/math/modifier-range-root-cause.md`, findings `qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`). Investigation commission: `dispatches/2026-05-16-gamora-modifier-range-investigation.md`.
**Process:** Knight-rider drafts → jack-ryan Gate 1 → Matt approval → knight-rider commits to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as prior qa/pending entries.

**Target location:** before the "Recently considered, not yet decided" section, after (and chronologically alongside) the 2026-05-16 engine-balance-stewardship entry. This entry is companion-to / extension-of that entry: View A locks the AOE philosophy and the divergence framework; this entry locks the OPERATIONAL CALIBRATION BASELINE that the framework reads against.

---

## Entry — Calibration epoch declared: B10.4 Option 2 modifier baseline is the regression standard; file 29 0.85–1.15 band is aspirational

### 2026-05-16: B10.4 Option 2 modifier baseline (mean |mod-1.0| ≈ 0.82) declared the operational calibration epoch; file 29 0.85–1.15 band reclassified as full-system aspirational target

**Decision:** The modifier range of **0.09–0.52** observed across 7 recent seasons (001001–001007) under B10.4 Option 2 convergence semantics is hereby declared the **operational calibration baseline**. The file 29 (`canonical/29-design-overview.md`) target band of **0.85–1.15** is reclassified as an end-state aspirational target requiring B6 generation work + B14.5 V2 energy-type levers to achieve. The two figures are NOT comparable as regression-monitoring inputs; they live at different stages of the architecture.

The metric for regression monitoring going forward is **mean |modifier - 1.0|** per convergence semantic (non-pack WR = 50%), computed across non-experimental classes in a full-converged season.

| Stage | Mean \|mod - 1.0\| | Modifier range | Status |
|---|---|---|---|
| **B10.4 Option 2 calibration epoch (current)** | **≈ 0.82** | 0.09–0.52 | Operational baseline; this is what regression compares against. |
| **B6 + B14.5 V2 target** | ~0.50 | wider band, tighter to 1.0 | Future milestone; rocket B6 pre-work + B14.5 V2 energy-type lever close most of the gap. |
| **File 29 full-system target** | ~0.10 | 0.85–1.15 | End-state aspirational; requires full architectural completion (B6 + B14.5 V2 + further calibration work). |

**Reasoning:** Gamora's modifier-range investigation (math note §4.3 + findings file) established three load-bearing facts:

1. **The 0.09–0.52 range is not a regression and not generation-side overtuning.** It is the expected output of the current simulator given a structural mechanical gap between elemental mana classes and physical rage classes. The gap is ~3–5× DPS-per-modifier disadvantage for physical rage classes — composed of rage energy startup (~1.5–2.0×; rage starts at 0 vs mana starts full), physical miss rate (~1.18×; 15% miss vs elemental always-hit), armor vs elemental resistance (~1.23×; ~18.6% vs ~0%), and melee positioning delays (~1.1×).
2. **The file 29 0.85–1.15 band was set aspirationally** before the current gauntlet, before B14.5 V1, before B10.4 Option 2. It assumed energy-system power differentials would be compensated elsewhere. They have not been yet. The band was never calibrated against any specific convergence semantic.
3. **Key negative finding — generation is not the cause.** Both hybrid_mage/water (modifier=0.095) and physical_warrior (modifier=0.525) use tier 25–50 skills with nearly identical magnitude distributions (~77k DPS estimate at mod=1.0). The ~5.5× modifier gap between them is entirely from sim mechanics, not from generation producing different power budgets.

The architectural fix is in generation (B6 energy-type-aware tier assignment) and B14.5 V2 (energy-type lever in primary recompose loop), NOT in sim. A targeted sim patch (e.g., 15–20 starting rage) would compress modifiers by ~20% without closing the structural ~3–5× gap.

**Operational implications:**

- **Regression monitoring:** any future regen producing modifier behavior outside the B10.4 Option 2 epoch (significantly tighter than 0.09–0.52, or significantly wider) is the signal that requires investigation. Use mean |mod-1.0| ≈ 0.82 as the comparison anchor. Crossing toward 0.50 is the expected direction once B6 pre-work lands; crossing past it without B6 lands is a red flag.
- **Validation against file 29:** the 0.85–1.15 band is the target-state, not the regression-state. Validators (CLI summary, in-band check in `validation_report.py`, etc.) should display the current epoch baseline as the comparison standard, with the file 29 target as an aspirational marker — not the pass/fail line.
- **Archetype gradient is monotonic and known.** Per gamora's findings (all 7 recent seasons): fire_mage 0.068 → water_mage 0.070 → earth_caster 0.084 → hybrid_mage 0.098 → wind_caster 0.109 → wind_controller 0.134 → fire_controller 0.137 → earth_controller 0.145 → water_controller 0.187 → physical_warrior 0.317 → hunter 0.594 → experimental/physical 0.718. The gradient corresponds to (DPS density × fight-mechanical efficiency). This is the empirical state of the calibration epoch.

**Alternatives considered:**

- **(a) Hold file 29 0.85–1.15 as the regression standard.** Rejected. The band predates the current gauntlet + B14.5 V1 + B10.4 Option 2. Comparing the current state against an aspirational target that requires unbuilt architecture (B6 generation refactor + B14.5 V2 energy-type lever) confuses "current operational baseline" with "target state." Two distinct concepts deserve two distinct entries.
- **(b) Ship a sim-side patch to bring the modifier range up.** Rejected per gamora's investigation. A starting-rage gift (~15–20) would compress modifiers ~20% without closing the structural ~3–5× gap. Better to fix in generation (B6) where the lever is architectural.
- **(c) Wait until B6 lands, then re-declare baseline.** Rejected. The current state needs a name and a metric NOW to keep regression-monitoring honest in the interim. B6 pre-work (energy-type-aware tier assignment) will shift the baseline; when it does, this entry gets a successor entry recording the new epoch. That's the lifecycle.
- **(d) Use convergence WR alone as the regression standard, ignore modifier range.** Rejected. Convergence WR is one input to the multi-dimensional divergence framework (locked in the 2026-05-16 engine-balance-stewardship entry). Convergence WR tells us **whether** balance landed (did the binary search converge to 50% non-pack WR per class); modifier range tells us **where** it landed across the energy-system mechanical gradient (how much numeric compensation each archetype needed to get there). The two are orthogonal in this specific sense: a regen could fully converge (good WR signal) while sitting at the wrong end of the modifier gradient (bad calibration signal), or vice versa. Both metrics are needed; one alone is insufficient.

**Cross-seam cascades:**

- **Rocket:** B6 pre-work dispatch authored (`2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md`) — energy-type-aware skill tier assignment in `b6_archetype_templates.py`. ~1.7× tier-range shift for rage/physical archetypes. Held on jack-ryan Gate 1 + Matt approval before execution. When it lands, the next regen should produce a tighter modifier range (closer to the mean |mod-1.0| ≈ 0.50 target).
- **Gamora:** B14.5 V2 design work — when sequenced — adds an energy-type lever to the primary recompose loop (skill_swap, geometry_mix, cooldown_energy → + energy_cost distribution). Not authored yet; this is the deferred half of the architectural fix.
- **Star-lord:** `validation_report.py` and `summary_formatter.py` reading the in-band check should reference this epoch baseline (mean |mod-1.0| ≈ 0.82, range 0.09–0.52) as the operational comparison. The file 29 band remains for display as the aspirational target.
- **Drax:** no immediate change. Loadout viz consumes modifier values via existing schemas; the values don't change meaning until a fresh regen reads against this entry.
- **Jack-ryan:** future gate reviews should reference this entry's baseline-vs-aspirational distinction. Don't flag a regen as a regression just because it's outside 0.85–1.15.

**Status:** Active.

**Implementation cascade:**

- **Rocket B6 pre-work dispatch** (energy-type-aware tier assignment) — held on Gate 1 + Matt approval; expected to shift the epoch toward mean |mod-1.0| ≈ 0.50 when it lands.
- **Gamora B14.5 V2 energy-type lever** — not authored yet; closes remaining gap toward file 29 target.
- **Validation tooling** (star-lord side) — display the epoch baseline as the operational comparison; file 29 band as the aspirational marker. Small future fix; not blocking.

**Related:**

- `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md` (the empirical basis)
- `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md` (gamora's math note — full §4.3 derivation of the ~3–5× combined factor)
- `agentic_orchestration/dispatches/2026-05-16-gamora-modifier-range-investigation.md` (the investigation commission)
- `agentic_orchestration/dispatches/2026-05-16-rocket-b6-pre-work-energy-type-aware-tiers.md` (the architectural-fix dispatch this entry sets up)
- `canonical/29-design-overview.md` § "shaped balance over numeric scaling" (the philosophy; 0.85–1.15 band lives here as aspirational)
- 2026-05-16 engine-balance-stewardship entry (companion entry; View A lock + multi-dimensional divergence framework + movement-modeling abstraction limitation) — this entry is the calibration-baseline half of that framework
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_b14_5_sidecar_analyses.md` (hunter modifier-range 1.82 — cross-seed consistency axis, separate from this entry's calibration-level axis per gamora's Discipline #12 distinction)

---

## Knight-rider note (NOT for decisions-log; for jack-ryan Gate 1)

Two ground questions for jack-ryan to test in Gate 1:

1. **Distinct-entry justification:** is this entry's content load-bearing enough to deserve its own decisions-log entry, or should it be folded into the engine-balance-stewardship entry as a subsection? My read: distinct entry is right, because (a) it has its own operational-vs-aspirational reclassification that's separable from the View A lock, and (b) it sets up the rocket B6 pre-work dispatch as a cascade. Folding it loses the architectural progression. Jack-ryan: confirm or push back.

2. **Discipline #12 (semantic-shifting) compliance:** the entry distinguishes "B10.4 Option 2 convergence semantic" from "pre-Option-2 overall-WR semantic" and locks the new metric (`mean |mod-1.0|` at non-pack WR = 50%) explicitly. Verify the framing doesn't conflate the two semantics anywhere in the entry body.

If both pass, this is ready for Matt approval and commit.
