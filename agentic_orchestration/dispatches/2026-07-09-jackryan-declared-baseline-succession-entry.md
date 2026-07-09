# Dispatch — jack-ryan: declared-baseline-move succession decisions-log entry (KR-drafted → you write → PARK)

**From:** knight-rider → **To:** jack-ryan (decisions-log write, his seam)
**Date:** 2026-07-09
**Pattern:** KR-drafts → **jack-ryan-writes (PENDING)** → **PARK at `canonical/matt_decision_needed/`** → Matt approves (do NOT auto-approve; do NOT self-ratify).
**Authority:** pilot_policy entry (4) named this succession (`94ec548`); C3 readout (`0e2ccff`) is the evidence; Matt ratified §4 density disposition **(1)** 2026-07-09 (relayed, FINAL). The underlying disposition is ratified; the formal decisions-log ENTRY gets Matt's approval sign-off per ADR-002.

---

## 1. DRAFTED ENTRY (for your canonicalization)

> Append below the full-run-pivot entry (`a50db87` / status-flip `ea16fb5`). Prose is KR's draft; you own the canonical write + citations + line-precise cross-refs.

---

### 2026-07-09 — Declared-baseline succession: stripped (arm S) → geared (arm G) is the certification baseline; C3 re-validated, bands STAND

**Decision**: The certification declared baseline succeeds from **stripped (arm S)** to **geared (arm G, certification_gear v0)**, as the full-run-pivot's E5-C + pilot_policy instrument-vs-content rider anticipated (`94ec548`). The first content-bearing per-axis run (C3 band re-fit on the E1-widened population, gamora `e1fe99e`, tag `gamora/v1.4-c3-band-refit-1`, readout `0e2ccff`) executed the succession and **re-validated the seven KPM bands at the geared baseline**. Because E1 is an EMITTER change (per-skill geometry), not a room-density change, and the five clear-shell bands are density/geometry-anchored, "re-fit at the declared baseline" is a **re-VALIDATION** (cross-check the arm-G distribution against each anchor), NOT a numeric re-fit. **All seven bands STAND at their current values** (open_arena (20.87,53.33) · chokepoint_corridor (12.52,60.00) · magic_pack (12.52,102.86) · elite_pack (8.26,28.13) · dense_cell (12.52,102.86) · boss_with_adds (2.49,3.78) · mini_boss (0.57,3.30)).

**§4 density disposition — (1) RATIFIED (Matt 2026-07-09)**: three shells' geared distributions run above their stripped-derived ceilings (chokepoint_corridor in-band 19.4% / dense_cell in-band 63.6% / elite_pack p25=29.03 > 28.13) — the EXPECTED consequence of the stripped→geared move (arm G = +35% dmg / +18% armor / +12% hp clears faster → higher KPM), NOT a band error and NOT kit non-viability. **Rider-3 absorbs it:** above-ceiling = `FLAG_PASS_OVERPOWERED` → **difficulty-ladder input**. Bands stand; no ceiling was curve-fit up (rider-4 / anti-Goodhart). Re-anchoring at a geared clear-time intent (disposition 2) was NOT taken — it re-enters only if the geared baseline is later judged durable AND the FLAG_PASS volume too high to be a useful difficulty signal.

**Reframe-validity — falsifier does NOT fire**: the registered falsifier (pilot_policy (4): *if arm G compresses the KPM spread toward point-mass, ruling A's KPM-as-measurement is re-examined*) does not fire — arm-G compression ratio is 0.986–1.021 across all shells. Gear shifts the KPM distribution UP but PRESERVES its spread, so **ruling A ("clear-speed KPM is THE measurement") survives the geared baseline**. Reframe-validity discipline holds: no stripped figure is quoted as the geared baseline; the stripped "~2.4×" is not propagated.

**Two-component delta (INFO-1)**: the band shift reads against a largely **Path-3 geometry-blind** pre-E1 baseline (`small_aoe`/`large_aoe` were never valid `_RICH_TO_SPATIAL` keys → ~2/3 amplitude geometry-blind). Path-3-correction and geometry-variety act on overlapping (~2/3) amplitude space and are NOT cleanly separable — the C3 readout gives the bounding characterization (delta dominated by the joint-overlap region; lower bound on pure variety = the ~1/3 non-blind region), NOT a false split (Disc #12 / reframe-validity).

**Separate instrument item (flagged, not resolved here)**: **elite_pack saturates the KPM=450 instrument cap** (3-mob room + gear → near-instant clear; p90 == max == 450.0) — an instrument-cap artifact, not a content signal. Routed as its own math-note-first unit (cap raise vs clear-time-floor guard).

**Reasoning**: Recorded per Review Principle #4. The succession makes the geared baseline the certification measure of record (E5-C: stripped arm is the scaling-delta diagnostic, not the cert measure). The Discipline #12 semantic-shift is framed, not buried: the baseline MOVED, the bands were re-confirmed against it, and the over-ceiling geared mass is a difficulty-ladder signal by ratified disposition — not a re-balance trigger.

**Alternatives considered**:
- **Disposition (2) re-anchor ceilings at geared clear-time**: NOT taken — larger density-model-review, math-note-first; re-enters only under the two named conditions.
- **Curve-fit ceilings up to green the geared cells**: REJECTED (rider-4 / anti-Goodhart) — endpoints move only on diagnosed density-model mis-specification, never to green pass cells.

**Status**: **PENDING — Matt-approval (parked at `matt_decision_needed/`).** Composes with: the full-run-pivot entry (`a50db87`, E5-C + pilot_policy rider); the pilot_policy two-arm entry (`ce595a7`/`8185098`). No emitter/judge/telemetry change; no MIGRATION.

**Related**:
- Evidence: C3 readout `agentic_orchestration/gamora/notes/2026-07-08-c3-band-refit-e1-readout.md`; math note `simulation/math/c3-band-refit-e1-2026-07-08.md`; report `simulation/output/c3_band_refit_e1/c3_band_refit_e1_report.json`; commit `e1fe99e` / tag `gamora/v1.4-c3-band-refit-1`.
- Parents: pilot_policy `94ec548`/`ce595a7`/`8185098`; full-run pivot `a50db87`/`ea16fb5`.
- Ledger: surface-ledger C3 (✓, re-validated) + E5-C.
- Disciplines: #11 (elite_pack reclassification density-anchor); #12 (declared-baseline semantic-shift framing); Review Principle #4; rider-3 / rider-4.

---

## 2. Completeness checklist (your verification before write)

- [ ] Succession named (stripped arm S → geared arm G) + evidence (C3 run) cited
- [ ] Bands STAND (re-validation not re-fit) + the E1-is-emitter-not-density reasoning
- [ ] §4 disposition (1) ratified + Rider-3-absorbs semantics + no curve-fit (rider-4)
- [ ] Reframe-validity falsifier does-not-fire (compression 0.986–1.021)
- [ ] Two-component delta entangled bounding (no false split)
- [ ] elite_pack KPM-cap flagged as separate item
- [ ] Status PENDING + parked at matt_decision_needed
- [ ] Cross-refs to pilot_policy + pivot parents

## 3. What I need back

1. Decisions-log write commit hash + confirmation the entry is PENDING (not approved).
2. The `matt_decision_needed/` park item path.
3. Any disagreement routed to Matt rather than silently resolved.

Auto-commit (your seam). Do NOT push (KR batches per-run). Do NOT flip any gate. Do NOT self-approve.

**Sign-off:** knight-rider, 2026-07-09. Draft only — no decisions-log write by KR.
