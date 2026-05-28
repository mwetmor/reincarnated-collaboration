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

**Completed:** 2026-05-27 (gandalf)

**Deliverable:** `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` — 12 sections; 6 measurement dimensions fully specified per Matt pre-ratification #3; 3 open questions Q-AB-1/2/3 resolved within protocol; composition with Phase 7 HELD verdict logging (Discipline #43 audit data feed); 6 new failure-modes appended to register.

**6 dimensions specified:**
1. **Dim #1 — Archetype shape coverage** (§ 3): 8-BC-axis signature match against doc 48 § 3.1 baseline; ≥6-of-8 axes agreement; ≥0.80 B-PASS / 0.60-0.79 INCONCLUSIVE / <0.60 A-PASS
2. **Dim #2 — Substrate-anchor distribution** (§ 4): ~32% Sketch F target; 0.22-0.42 B-PASS band; symmetric A-PASS at <0.15 + >0.50 (both fail substantial-but-not-dominant intent)
3. **Dim #3 — Faction pairwise-distance distribution** (§ 5): Mahalanobis pairwise; ratio_max_min ≥1.50 HIGH-DISTANCE B-PASS / 1.05-1.49 WARN / <1.05 ALL-CLOSE A-PASS
4. **Dim #4 — Personage convergence test (Q2 D-Sharpened H1 vs H2)** (§ 6): Q-AB-1 RESOLVED → Bayesian Dirichlet-Multinomial posterior + Bayes factor PRIMARY; Fisher's exact supplementary; chi-squared REJECTED at violated asymptotic assumption; BF≥3.0 B-PASS
5. **Dim #5 — Surprise-emergence count** (§ 7): Q-AB-2 RESOLVED → ≥1 surprise B-PASS at Wave 5; 0 FOLLOW-UP-DEFER (small-n cannot distinguish either-direction); 4-all-surprises A-PASS (architectural decoupling)
6. **Dim #6 — Throwaway-cluster count** (§ 8): Q-AB-3 RESOLVED → dual-floor (member_count < max(3, 10% total) AND compactness < 0.40); BOTH must fail for THROWAWAY; THIN-COHERENT + FAT-INCOHERENT recorded separately

**Composite verdict synthesis (§ 9):** B-PASS requires ≥4 of 6 dimensions B-PASS/LEAN-B AND zero A-PASS; A-PASS requires ≥2 A-PASS OR any single A-PASS on dim #1 OR dim #4 (architectural-load-bearing dimensions); INCONCLUSIVE for any other outcome. Composite feeds Discipline #43 wave-close design-quality audit A1+A2+A4.

**Risks register (§ 10):** F-11 (premature commitment under small-n) + F-12 (Bayesian methodology mis-application) + F-13 (doc 48 baseline interpretation drift) + F-14 (Phase 7 data-pipeline integrity cascade) + F-15 (surprise-emergence interpretation drift) + F-16 (doc 48 VESTIGIAL retraction pressure) — all appended to `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` § 1.

**Discipline composition (§ 11):** #11 empirical-inspection (statistical rigor; Bayesian methodology; PRE-EXECUTION DATA INTEGRITY REPORT); #41 substrate-led (doc 48 baseline = COMPARISON not PRESCRIPTION); #42 framing-audit at entry (Q1/Q2/Q3 executed before authoring); #43 design-quality audit composition (composite verdict feeds A1+A2+A4); #45 vocabulary lock (kit/faction/substrate-anchor vocabulary throughout; doc 48 references use candidate-archetype-shape framing per canonical/story/ exemption interpretation); #46 DB anti-materialization (bounded queries; bounded contingency tables); #40 not-scaffold (operational decisions per Q-AB-1/2/3 resolutions; no scaffold flags); #18 math-hotspot routing (Bayesian for dim #4; elrond consultation reserved for F-12 trigger).

**Incremental commit cadence (per dispatch directive):**
- Commit 1 `00a3872`: scaffold + § 0-2 (TL;DR + Phase 7 composition + sample size preamble)
- Commit 2 `1c8230a`: § 3-4 (dim #1 + dim #2)
- Commit 3 `38593af`: § 5-6 (dim #3 + dim #4 with Q-AB-1 resolved)
- Commit 4 `1b1e832`: § 7-8 (dim #5 + dim #6 with Q-AB-2 + Q-AB-3 resolved)
- Commit 5 (final): § 9-12 + failure-modes register additions + completion record

**Hand-back:** A/B comparison protocol READY for Wave 5 close execution. KR routes execution at Wave 5 close (post canonical-promoted production season at audit-gate PASS). gandalf executes protocol; produces per-dimension audit records at `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-dim-N-output.md` per dimension; produces composite verdict record at `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-wave-5-ab-comparison-composite-verdict.md`; composite verdict feeds Discipline #43 wave-close design-quality audit record.

**Signal:** A/B comparison protocol READY for Wave 5 close execution.
