# Finding — 2026-06-11 — forward-architecture-contract (Gate-1)

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO (Gate-1 critique-pair; verdict per-dimension below)
**Target:** `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` (base + § 8.1 + § 8.2 amendments)
**Developer / Author:** gandalf (story-and-design steward)
**Invoking peer:** gandalf (Gate-1 critique-pair); Matt-authorized this session
**Principles applied:** Review Principle 4 (decisions-log as truth), Principle 5 (severity matters), Principle 3 (cross-seam impact); Disciplines #1 (math-before-code), #7 (telemetry tag), #24 (single-parameter isolation), #51 (Gate-1 critique-pair); ADR-004 (MIGRATION cross-seam), ADR-006 (read-only-by-default).

## Verdict

**PASS-with-INFO.** The contract is coherent, the amendments do not contradict the base or each other, the binding numbers faithfully represent the measurement evidence, and the cited audit commit hashes verify. Three INFO items and one WARN below; none blocks authoring or the § 9 dispatch sequence. The single WARN is a verifiability-precision gap (kernel interface not yet function-bound in the contract) that the contract's own § 2 interface-naming obligation is designed to close downstream — I flag it so KR does not let the first dispatch consume an undeclared boundary.

## Per-dimension findings

### Dimension 1 — Kernel-boundary verifiability — WARN (soft, downstream-closable)

§ 2 names five kernels by *description* ("Resolver math (fight engine core: damage resolution, three-path routing per doc 47, ailment/control mechanics, tick loop)"). The simulation audit (gamora § 1, § 4) establishes the boundary is drawable TODAY at a specific named interface — `fight_engine.simulate_fight(...) -> FightResult` (`fight_engine.py:107`), a pure deep-copying function with grep-confirmed zero telemetry/DB/LLM coupling across all 7 kernel files. The contract **cites** this evidence but does **not bind** the function/file as the enforceable boundary; it defers interface naming to each seam's MIGRATION.md (§ 2 line 50, "interface declaration IS the wrap boundary"). That deferral is architecturally sound — but it means the contract as written is enforceable only once those MIGRATION.md declarations land. **The gap is the evidence is strong and specific while the contract text remains descriptive.** Not a BLOCK: the obligation exists and the audit hands the seam the exact signature to declare. WARN so KR holds the first gamora/rocket dispatch to declaring `simulate_fight` (sim) and the generation-core entry-points (gen) in MIGRATION.md *before* the parallel runner / naming-orchestration code consumes them — otherwise "undeclared kernel entry-points are not consumed" (§ 2) is unenforced on the first pass.

### Dimension 2 — Protocol enforceability — PASS-with-INFO

§ 3's five steps are each after-the-fact verifiable: math-note (artifact), golden-master corpus committed as oracle (artifact), isolated change (Discipline #24, diff-checkable), re-run delta-vs-prediction (artifact comparison), telemetry tag (Discipline #7, queryable). **INFO-1:** the golden-master capture obligation (§ 3 step 2) names the corpus *shape* ("fixed seed-set of fights across encounter types + kit archetypes" / "fixed seed-set of kit tuples → emitted kits") but not the corpus *size, the pin location, or the commit convention*. For the first application (spatial recalibration) the gandalf design-spec § 2.1 says "pin the current spatial engine's outputs on a reference corpus" — also unsized. Recommendation: gamora's math-note fixes the concrete corpus (N fights, which encounter types, which archetypes, pinned path) as part of the proving run; the protocol then has a worked reference for every subsequent application. This is the protocol's proving run by design, so leaving it to the math-note is acceptable — INFO, not WARN.

### Dimension 3 — Numbers fidelity — PASS

§ 4's six binding rows reproduce the 2026-06-10 verdict § 3 table exactly (9 ms / 9.7 s / 54 s / 10–35 min+$12.4 / 9 s warm–43 s cold / Mac 0.7–3.5 h–PC 0.3–1.3 h). ASSUMED-vs-MEASURED status is carried honestly: § 4 re-measure triggers flag the 50 req/min rate-limit as ASSUMED-in-code (star-lord verifies); § 8.2.2 correctly flags the PC 12× parallel factor as ASSUMED (re-profile S4) and bans banking the combined Mac+PC number until measured; § 8.2.2 correctly names the convergence-iteration multiplier as OUT OF MODEL (re-profile scaffold S7) and partitions filter (MEASURED) / cycling (UNMEASURED, not production-authorized) / hybrid (intent, re-gate multiplier to be modeled). This is the strongest dimension — the per-gauntlet-pass caveat is exactly the gap Matt caught, and the contract now states it precisely rather than letting the § 4 numbers read as full-cycle costs. No drift.

### Dimension 4 — Amendment coherence — PASS

§ 8.1 and § 8.2 are internally consistent and consistent with the base. Checks performed:
- **Commit hashes (§ 8.1):** `477dee3` (gamora audit) + `8910168` (rocket audit) — both VERIFIED against `git log`. Citations are accurate.
- **Audit counts:** § 8.1 reports sim 8/2/0 and gen 5/4/1 — both match the source audit § 3 / count-summary tables exactly.
- **Disposition-3 RESOLVED cross-ref:** § 8.1 disposition 3 ("gandalf design-lean (b)... RESOLVED → § 8.2: Matt authorized (b)") is clean — § 8.2.1 does authorize remedy (b), retires the simplified model as commit-grade, and binds re-point + recalibration as one work item. No dangling pointer; the lean and the resolution agree.
- **Base-vs-amendment:** § 8.2.1's "re-point invalidates SPATIAL_DAMAGE_SCALE=4.0 by construction" is consistent with § 3's "first scheduled application" (spatial recalibration) and § 5's gate ("spatial does not hold commit-grade until recalibration completes"). The amendment tightens the base; it does not contradict it.
- **§ 9 reclassification:** § 8.1 disposition 1 RECLASSIFIES the § 9 "cache-hygiene boundary case" row to module-targeted-greenfield-under-oracle ("it is not a patch"). This supersedes the § 9 row text. INFO-2: § 9 line 111 still reads "Boundary case — classify via audit; if counter state lives inside generation core, fix routes through § 3." That row is now resolved by § 8.1 but the § 9 table was not edited to point forward. Not a contradiction (the audit POST-DATES the table and § 8.1 explicitly reclassifies), but a reader hitting § 9 first sees stale routing. Recommendation: add a one-line "(RECLASSIFIED — see § 8.1 disposition 1)" to the § 9 cache-hygiene row. Documentation-polish, INFO.

### Dimension 5 — Process — PASS-with-INFO

Amendment-record discipline is sound: both amendments carry their own authority line, evidence cites, and date; § 10 routing pre-declared the in-place-amendment path. Routing table (§ 9) is complete across the four seams (gamora/rocket/star-lord/PC-consult) with kernel-touching flags. **INFO-3 (decisions-log vs contract text):** § 8.2.3's T4-native-recompose requirement declares the recompose-lever vocabulary "T4-profile-native-pending" and makes "full T4 skill-profile design upstream of the cycling regime." That is an **architectural sequencing commitment** (a future cycle is gated on a design that does not yet exist), which is decisions-log-grade per the decision-log-format when-to-file table, not merely contract prose. I am folding it into the combined decisions-log entry (deliverable 2) so the gate is queryable from the log, not only discoverable inside a story doc. Flagging here so the routing is on record.

## Rationale

The contract correctly operationalizes the WRAP verdict and answers Matt's Pattern-B challenge by construction (kernel-freeze retires change-isolation churn; kernel-preservation + golden-master retires silent-omission drift). The measurement evidence is represented faithfully (Dimension 3), the amendments cohere (Dimension 4), and the protocol is after-the-fact verifiable (Dimension 2). The one WARN (Dimension 1) is not a defect in the contract's logic but a verifiability-timing gap: the enforceable boundary lives in MIGRATION.md declarations that the first dispatch must produce before consuming the kernel. Holding KR to that ordering closes it. Per Principle 5, this is INFO/WARN-grade softness, not a principle violation — nothing here conflicts with a locked decisions-log entry, and the cross-seam export-contract discipline (§ 7, additive-per-Principle-6) is intact.

## Action

- [ ] gandalf (INFO-2): add "(RECLASSIFIED — see § 8.1 disposition 1)" to the § 9 cache-hygiene row so first-read routing is not stale. Documentation-polish; ADR-002 self-approvable.
- [ ] KR (WARN, Dimension 1): hold the first gamora + rocket dispatches to declaring kernel entry-points in MIGRATION.md (`simulate_fight(...) -> FightResult` for sim; generation-core entry-points for gen) BEFORE consuming-code lands. Enforces § 2 line 50.
- [ ] gamora (INFO-1): the spatial-recalibration math-note fixes the concrete golden-master corpus (size, encounter types, archetypes, pin path) as the protocol's worked reference.
- [x] jack-ryan: combined decisions-log entry written (greenfield verdict + this contract + § 8.2.3 T4-sequencing gate) — engine repo, this session.

## References
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` (review target; § 2, § 3, § 4, § 5, § 7, § 8, § 8.1, § 8.2, § 9, § 10)
- `canonical/story/2026-06-10-engine-greenfield-verdict-wrap-and-extend.md` (verdict operationalized)
- `agentic_orchestration/gamora/notes/2026-06-11-gap-register-architecture-fit-audit-simulation.md` (commit `477dee3`; 8/2/0; `simulate_fight` boundary)
- `agentic_orchestration/rocket/notes/2026-06-11-gap-register-architecture-fit-audit-generation.md` (commit `8910168`; 5/4/1; id-substrate FIGHTS)
- `agentic_orchestration/gandalf/notes/2026-06-11-spatial-repoint-recalibration-math-note-design-spec.md` (first § 3 application spec)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (combined entry, this session)
