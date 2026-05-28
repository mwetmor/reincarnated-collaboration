# Dispatch — 2026-05-27 — gandalf — A/B comparison protocol authoring (Wave 5 close measurement)

**From:** knight-rider
**To:** gandalf (design-side comparison protocol author)
**Approved by:** Matt 2026-05-27 pre-ratification #3 (A/B comparison post-Wave-5 measurement dimensions; 6 dimensions LOCKED)
**Estimated effort:** ~2-3 days authoring (fires at Wave 5 close; consumes Wave 5 production-season output)
**Acceptance:** A/B comparison protocol authored at canonical path; 6 measurement dimensions specified; per-dimension acceptance criteria + measurement procedure + drift-watch criteria; ready for execution against Wave 5 production seasons + historical doc 48 baseline

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** quantify Option α substrate-led emergence vs doc 48 pre-authored taxonomy baseline. Without A/B comparison protocol, Cycle 14 design verdict on Option α effectiveness is qualitative-only. Composes Discipline #11 empirical-inspection at architectural decision verification.

**Refutation conditions:**
- Any of 6 dimensions cannot be empirically measured at Wave 5 close (data not captured)
- Acceptance criteria per dimension produce ambiguous A vs B verdicts
- Doc 48 baseline unavailable (VESTIGIAL retraction lost comparison surface)
- Measurement-dimension #4 (personage convergence Q2) cannot resolve H1 vs H2 with sample size at Wave 5

## Context

**Matt pre-ratification #3 (6 measurement dimensions LOCKED):**

1. **Archetype shape coverage** — did each doc 48 archetype emerge? similarity-threshold match
2. **Substrate-anchor distribution** — % of emergent classes with named-personage substrate-anchor metadata; target ~32% per Sketch F
3. **Faction pairwise-distance distribution** — histogram of pairwise distances; high-distance vs all-close signal
4. **Personage convergence test (Q2 D-Sharpened)** — H1 (null) vs H2 (anchor-correlated) empirical verdict
5. **Surprise-emergence count** — emergent classes with NO doc 48 baseline match
6. **Throwaway-cluster count** — thin/incoherent clusters; substrate-tagging artifacts

**Composition with current state:**
- Doc 48 VESTIGIAL but PRESERVED-FOR-COMPARISON; A/B baseline source
- Phase 4 gamora kit_archive + Phase 5 ExportFactionCluster + F-C ExportFactionRelationship → measurement data sources
- Discipline #45 generative-architecture vocabulary lock (jack-ryan canonical-write firing in parallel) → A/B comparison evaluates whether no-classes vocabulary discipline holds empirically
- Phase 7 2-layer joint-gate output → cohesion + mechanical pass distribution

## Required reading

- `canonical/48-cycle-14-class-roster-2026-05-27.md` (VESTIGIAL — doc 48 baseline for A comparison)
- `canonical/00-ground-state.md` (no-classes architectural recommitment)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` (ExportFactionCluster + ExportFactionRelationship measurement fields)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/phase4_*.py` (kit_archive measurement data source)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (Sketch F + Q2 D-Sharpened theoretical framework)
- Engineering-disciplines.md § Discipline #11 + #41 + #43

## Discipline #46 compliance

- N/A — protocol authoring; no DB queries at authoring (Wave 5 execution will query)

## Discipline #42 framing-audit

- **Q1:** (1) doc 48 VESTIGIAL preserved enough for empirical baseline (yes — content preserved, status only changed); (2) 6 dimensions measurable at Wave 5 close (assumes Phase 4+5+7 impl complete + production-season output captured); (3) ~32% Sketch F substrate-anchor target empirically achievable
- **Q2:** verify doc 48 archetype list capture for dim #1 + #5 measurement; verify Phase 5 ExportFactionCluster/ExportFactionRelationship populated at Wave 5 close
- **Q3:** if dim #4 personage convergence H1/H2 test underpowered at Wave 5 sample size, invoke #44 + route back for revised dim #4 (e.g., defer to Cycle 15 with larger sample)

## Scope

- [ ] Author A/B comparison protocol at `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` (gandalf judgment on canonical path)
- [ ] Per-dimension specification (6 dims; for each):
  - Operational definition
  - Measurement procedure (DB queries + statistical methodology)
  - Acceptance criterion (A passes / B passes / inconclusive thresholds)
  - Drift-watch criterion (Cycle 15+ revisit trigger)
  - Empirical data source (kit_archive / ExportFactionCluster / ExportFactionRelationship / doc 48 archetype list)
- [ ] Per-dimension #4 Q2 D-Sharpened personage convergence test specification (H1 null + H2 anchor-correlated; statistical test; sample size requirement)
- [ ] Per-dimension #2 ~32% Sketch F substrate-anchor target rationale documented
- [ ] Per-dimension #6 throwaway-cluster definition (thin/incoherent thresholds; substrate-tagging artifact criteria)
- [ ] Composition with Phase 7 HELD verdict logging (Discipline #43 design-quality audit data feed)
- [ ] Risks + Watch Items per failure-modes register § 5

### Closure

- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern
- [ ] Signal A/B comparison protocol ready for Wave 5 close execution

## Acceptance criteria

- [ ] 6 measurement dimensions fully specified
- [ ] Per-dimension acceptance criterion + measurement procedure + drift-watch criterion
- [ ] Statistical test for dim #4 personage convergence specified
- [ ] Composition with Phase 7 HELD verdict + Discipline #43 audit
- [ ] Risks + Watch Items embedded
- [ ] Completion record + commit + push

## Out of scope

- Do NOT execute A/B comparison at this dispatch (fires at Wave 5 close)
- Do NOT touch doc 48 (preserved verbatim for baseline)
- Do NOT touch Phase 7 dispatch (separate)
- Do NOT touch Wave 5 production-season dispatch (separate)

## Open questions

- **Q-AB-1:** Statistical test for dim #4 Q2 D-Sharpened personage convergence — chi-squared vs Fisher's exact vs Bayesian posterior? Your judgment per sample size expectation at Wave 5
- **Q-AB-2:** Acceptance criterion for dim #5 surprise-emergence count — low (Option α found new archetypes) is good, but how low is too low (Option α just reproduces doc 48)? Your judgment
- **Q-AB-3:** Throwaway-cluster (dim #6) threshold operational definition — N kits/cluster floor + coherence-score floor? Your judgment

## References

- Matt pre-ratification #3 verbatim (above)
- Doc 48 VESTIGIAL (baseline for A comparison)
- Path III Sketch F + Q2 D-Sharpened framework
- Engineering-disciplines.md § Discipline #11 + #41 + #43

---

## Completion record

(append on completion)
