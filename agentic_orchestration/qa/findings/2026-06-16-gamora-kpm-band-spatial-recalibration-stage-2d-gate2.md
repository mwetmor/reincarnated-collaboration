# Finding — 2026-06-16 — gamora KPM-band spatial recalibration Stage-2d (band wire-in)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no WARN, no BLOCK)
**Target:** engine commit `92c040f` (tag intent `gamora/v1.1-kpm-band-spatial-recalibration-2d`); composes with prior `1032560` (Stage-2a/2b numerator fix)
**Developer:** gamora (simulation seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam/MIGRATION), 4 (decisions-log truth); Disciplines #12 (semantic-shift framing), #11 (empirical inspection), #9 (attribution), #1 (math note)

## What I found

The combined semantic-shift + band wire-in is correct, in-seam, honestly framed, and empirically verified on both witnesses plus the load-bearing consumer audit. I did not take gamora's evidence on faith — I reproduced Witness A (clean import + wired-band readback) and Witness B (the routing spot-check through the REAL `_route_tier_1` predicate against the WIRED `ENCOUNTER_COHORT_KPM_BAND`) independently. All 6 shells route central-mass → PROVISIONAL_PASS, slog (low tail) → REJECT, trivialize (high tail) → REJECT. The numerator shift (`kills = 1 if fr.player_kill else 0` → `kills = fr.mobs_killed`, denominator unchanged) flows through the `observed_kpm` property correctly; `fr.mobs_killed` exists on the spatial result (`spatial_engine.py`). The gate predicate `_route_tier_1` band_override path (`if lo <= observed_kpm <= hi`) is a direct inclusive-range check, UNCHANGED. The RESOLVE band `SPATIAL_ENCOUNTER_KPM_BAND` is NOT in the diff — untouched; the RESOLVE cert (`gauntlet_sim.py:1003/1029`) reads it, not the swapped constant, so there is no interaction between the band swap and the cert, and the cert is CORRECTED-not-broken by the upstream numerator fix. Commit 92c040f touches exactly 3 files, all in-seam (`gauntlet_sim.py`, `MIGRATION.md`, the Stage-2d math note); no stray changes. MIGRATION numbering reconcile is collision-free (v1.72 retained by AOE re-home; t4-repoint renumbered v1.72→v1.75; Stage-2d v1.76; v1.73/v1.74 sequential).

## Rationale

- **Discipline #12 (semantic-shift framing):** SATISFIED at both layers. The numerator shift's meaning-change (rooms/min → mobs/min for every `observed_kpm` consumer) is declared in commit message, inline comment (`t4_sim_cycling.py:~1077`), docstring (`:1030`), MIGRATION v1.74, and the STAGE2A math note §4 14-consumer audit. The band-value shift is framed in commit message, inline block comment, MIGRATION v1.76, and the STAGE2D math note. This is a design decision dressed AS a design decision — exactly what #12 requires. No rationalization-after-the-fact.
- **Consumer-set audit (the semantic-shift risk surface):** CONFIRMED clean. Every `observed_kpm` band-comparison consumer (W4G gate, RESOLVE cert, Track-1, phase7) judges against a mobs/min-derived band; all were silently mis-comparing under the prior rooms/min numerator and are corrected by the fix. NO consumer silently depends on the old rooms/min meaning. The star-lord export field (`tier_1_kpm`/`tier_2_kpm`) shifts magnitude-meaning but not shape — documented in MIGRATION v1.74 (a) for star-lord to reinterpret.
- **Principle 1 / Discipline #1 (math-before-code):** SATISFIED — math note authored before edit, bands traced to the n=3078 determined-slice population.
- **Principle 2 (smoke-gate):** SATISFIED — smoke output present and independently reproduced.
- **Principle 3 / ADR-004 (cross-seam):** SATISFIED — MIGRATION.md carries the numerator-shift consumer enumeration and the band-swap entry. The only cross-seam exposure (star-lord export magnitude reinterpretation) is explicitly called out.

## INFO carried (non-blocking)

- **[INFO-1] Sub-gate-3 zero-damage-floor interaction (`t4_sim_cycling.py:714`):** CONFIRM gamora's WARN-not-BLOCK assessment. The `_check_zero_damage_floor` predicate `f.kills == 0` shifts from "did not clear the room" (win-flag false-positive on 7/8-mob near-clears) to "killed literally zero mobs in a ≥119s fight" — which IS the sub-gate's named intent. The interaction moves toward correctness and, being a WARN sub-gate, cannot harden any kit's verdict to BLOCK. No action required; recorded for the archaeology trail.
- **[INFO-2] Cohort-column collapse is INTENTIONAL, not accidental flattening.** The per-shell band is replicated identically across all 4 cohort columns so the `[shell][cohort]` lookup stays structurally intact. gandalf ruled cohort-invariance ("do NOT add per-cohort variation"); the 2b characterization confirmed it empirically (per-shell cohort means ≤0.1 mobs/min apart). The cohort dimension is now degenerate at this gate by design. INFO so a future reader does not mistake the degeneracy for a bug.
- **[INFO-3] Packet line-number drift:** the submission packet cites `ENCOUNTER_COHORT_KPM_BAND` at `gauntlet_sim.py:206`; the constant body / wired values sit at `~:281`. `:206` is the declaration header line. Cosmetic; values verified by readback, not by line number.
- **[INFO-4] Provenance / re-fit dependency on `MOB_HP_DIFFICULTY_MULTIPLIER`:** the bimodal-shell `p25-lo` cut excludes the 1.5× HP-wall low mode. The provenance stamp (MIGRATION v1.76) correctly frames the bands as re-fit candidates IF that multiplier changes — documentation, not a code dependency. The separate `MOB_HP` workstream (Matt-scheduling-pending) is out of scope here; no blocking interaction.

## Disposition

**PASS-WITH-INFO. Interim guard LIFTED.** Phase-3 season-gen output becomes canonical-eligible again for the KPM-gate dimension as of this clearance (it has been NON-CANONICAL since the `de09d8b` repoint). The four INFO items are recorded, not blocking. ADR-002: this is a within-seam threshold recalibration with an explicitly-framed semantic shift, fully consumer-audited — within jack-ryan Gate-2 PASS authority; no Matt escalation required for the close. Push remains Matt-gated (not lifted here).

## Action
- [x] Developer (gamora): none required — work is clean. Note INFO-1/INFO-2 for the record.
- [ ] star-lord (downstream, non-blocking): reinterpret `tier_1_kpm`/`tier_2_kpm` export magnitude as mobs/min per MIGRATION v1.74 (a) — already flagged in MIGRATION, not gated here.
- [ ] Matt: none required for the close. Push of `92c040f` (+ prior `1032560`, `eb026ab`) remains Matt-gated. `MOB_HP_DIFFICULTY_MULTIPLIER` workstream scheduling unchanged.

## References
- `src/reincarnated/simulation/gauntlet_sim.py` (`ENCOUNTER_COHORT_KPM_BAND` ~:281; `_route_tier_1` consumers; RESOLVE band untouched)
- `src/reincarnated/simulation/t4_sim_cycling.py` (`observed_kpm` property :244; `_route_tier_1` :682; numerator fix :~1077; sub-gate-3 :714)
- `src/reincarnated/simulation/MIGRATION.md` (v1.72 / v1.73 / v1.74 / v1.75 / v1.76)
- `src/reincarnated/simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2D-BAND-WIREIN.md`, `…-STAGE2A-NUMERATOR-FIX.md`, `…-STAGE2B-MOBSMIN-CHARACTERIZATION.md`
- `agentic_orchestration/dispatches/2026-06-16-gamora-kpm-band-spatial-recalibration.md`
- `agentic_orchestration/qa/pending/2026-06-16-gamora-kpm-band-spatial-recalibration-stage-2d-gate-2.md` (submission)
