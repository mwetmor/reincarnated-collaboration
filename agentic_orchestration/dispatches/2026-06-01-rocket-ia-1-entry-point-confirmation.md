# Dispatch — 2026-06-01 — rocket — IA-1 entry-point confirmation (V1 season generation)

**From:** knight-rider (immediate-arc orchestrator)
**To:** rocket (engine generation seam)
**Approved by:** Matt 2026-06-01 strategic reset + pre-commitment ratification LOCK A (rocket + star-lord autonomous on config/prompt; KR routes per pre-commitment) + star-lord IA-1 readiness assessment (commit `4a2abf2`)
**Workstream tag:** `IA-1-V1-baseline-season-generation`
**Phase / phase-gate:** Pre-IA-1-V1-fire (entry-point confirmation; per star-lord routing)
**Estimated effort:** ~5-15 minutes (single-question confirmation)
**Acceptance:** Entry-point confirmation at `agentic_orchestration/rocket/notes/2026-06-01-ia-1-entry-point-confirmation-response.md` (or appropriate rocket-seam path)

---

## 1. Context

Matt 2026-06-01 strategic reset + pre-commitment ratification (LOCK A: rocket + star-lord autonomous on config/prompt). Star-lord IA-1 pre-fire response (commit `4a2abf2`) identified MINIMAL-SETUP-REQUIRED with two items:

1. Environment: `ANTHROPIC_API_KEY` must be set at execution-environment level
2. **Rocket coordination (this dispatch):** confirm IA-1 V1 entry point

Star-lord's read on entry-points:
- **CLI path** `python -m reincarnated.cli generate-season` (SeasonOrchestrator) — READY; reads pool.json v1.1 cleanly; flows vocabulary into LLM prompts automatically; zero code changes
- **Alternative** `run_season_generation()` in `season_generation_pipeline.py` — hardcodes `SEASON_ID = "cycle-13-mechanical-season-001"` + hardcoded cohort assertions; this is **Cycle 13 Wave 5 mechanical pipeline**, almost certainly NOT IA-1 V1 target

**This dispatch requests rocket confirmation of the CLI path as IA-1 V1 entry point** OR rocket's alternative recommendation if a different entry-point better serves IA-1 V1 scope.

---

## 2. The confirmation question

> For IA-1 V1 baseline season generation, is `python -m reincarnated.cli generate-season` (SeasonOrchestrator) the correct entry-point that consumes pool.json v1.1 vocabulary into Phase 5+ LLM-named season output?
>
> If YES, confirm; KR fires IA-1 V1 immediately on confirmation.
>
> If NO, name the correct entry-point + any minimal-setup needed (config flags / CLI arguments / season-id specification / etc.).
>
> If the CLI path is correct BUT requires specific arguments (e.g., a specific season-id format, cohort spec, output path), name them.

---

## 3. Context for confirmation

### 3.1 IA-1 V1 scope (per immediate-arc queue § IA-1)
- Run engine's existing Phase 5+ pipeline against current substrate (post-Q18-lock pool.json v1.1 + existing weapon substrate)
- Produce new season output with LLM-named skills using current Phase 5 cohesion-judge + skill-naming + faction-naming pipeline
- NO Q16/Q17/Q19 or WS1A.3/4 architecture required — engine uses existing prompt design
- Q18 vocabulary in pool.json available as substrate; engine consumes for naming context without bounded-judgment infrastructure
- Output: new season JSON artifact (becomes input substrate for IA-2 gap analysis + IA-3 drax loading)

### 3.2 Engine state (per star-lord IA-1 response)
- `data/seasonal_elements/pool.json` v1.1 (100 Architecture-A locked + 114 legacy preserved-quarantined)
- `data/seasonal_elements/physical_taxonomy.json` (9 entries; Architecture A taxonomy registry)
- `src/reincarnated/element/schema.py` (PoolElement extended with 4 additive fields; backward-compat verified)
- Pool.json v1.1 reads cleanly from star-lord seam
- LLM-call infrastructure operational at commit `62f1429` (phase5_orchestrator.py)
- Drift-14 auto-demote at load: 58/100 lock entries auto-demote to eligible until vfx_coverage_manifest extended; ACCEPTABLE V1 baseline per strategic reset (vfx_coverage_manifest DEFERRED long-arc)

### 3.3 Pre-commitment scope (LOCK A)
- Config-level changes (e.g., pool.json reference paths) — rocket autonomous
- Prompt-level tweaks (e.g., Phase 5 prompt references to Q18 vocab) — rocket autonomous (coordinates with star-lord on Phase 5+ pipeline)
- **Architectural changes** (engine schema, BC axes, substrate composition policy) — ESCALATE per pre-commitment ratification § 3 escape clause

If your entry-point confirmation surfaces architectural-amendment need beyond pre-commitment scope, surface to KR via report-back (KR escalates to Matt per escape clause).

---

## 4. Expected output format

Author response at `agentic_orchestration/rocket/notes/2026-06-01-ia-1-entry-point-confirmation-response.md`:

1. **Entry-point verdict:** CLI-PATH-CONFIRMED / ALTERNATIVE-PATH-RECOMMENDED / BLOCKED
2. **If CLI-PATH-CONFIRMED:** confirm `python -m reincarnated.cli generate-season` consumes pool.json v1.1; name any specific arguments (season-id format / cohort spec / output path); KR fires IA-1 V1 immediately
3. **If ALTERNATIVE-PATH-RECOMMENDED:** name the entry-point + concrete invocation + rationale; KR fires per your recommendation
4. **If BLOCKED:** surface blocker; route to KR (KR escalates per escape-clause if architectural-amendment need surfaces)
5. **Substrate-side V1 pre-fire check** (optional): is the substrate side (generation/element/anchor/foundation) ready for V1 fire? Any rocket-side coordination needed?
6. **Estimated rocket-side wall-clock** (typically 0; this is a configuration confirmation)

---

## 5. Scope constraints

- **THIS IS A CONFIRMATION QUESTION, NOT V1 EXECUTION.** Do NOT fire season generation in this dispatch.
- **Operational confirmation ONLY** — if rocket-side needs additional setup, name it; KR routes setup dispatch first.
- **Substrate state is STABLE** — pool.json v1.1 + weapon substrate are stable; do NOT propose substrate changes in this response.
- **Architectural amendment surface → escalate via report-back** — per pre-commitment ratification § 3 escape clause.

---

## 6. Decision authority

Per pre-commitment ratification LOCK A: rocket entry-point confirmation + config/prompt autonomy are YOURS per rocket seam authority (engine generation seam ownership). Matt is NOT in the loop. KR proceeds per your routing instruction.

If you observe a confirmation requirement that exceeds rocket seam authority (e.g., requires architectural commitment outside pre-committed scope), surface to KR for escape-clause assessment.

---

## 7. Cross-seam contract change? (Principle 6)

**Answer:** NOT applicable. Entry-point confirmation is an operational confirmation artifact; no engine substrate / schema / pipeline modified.

---

## 8. Acceptance criteria

- [ ] Entry-point verdict explicit (CLI-PATH-CONFIRMED / ALTERNATIVE-PATH-RECOMMENDED / BLOCKED)
- [ ] Specific arguments named (if any)
- [ ] Substrate-side V1 pre-fire check brief
- [ ] Auto-commit per CLAUDE.md addendum 2026-05-25

---

## 9. Out of scope

- Season generation execution itself (separate IA-1 V1 fire dispatch)
- Substrate modification (pool.json + weapon substrate stable)
- vfx_coverage_manifest extension (DEFERRED long-arc per strategic reset)
- IA-2 (parallel workstream; elrond seam; currently running in background)
- IA-3 (depends on IA-1 V1 output)
- Long-arc deferred items

---

## 10. References

- **Star-lord IA-1 readiness response:** `agentic_orchestration/star-lord/notes/2026-06-01-ia-1-engine-readiness-pre-fire-response.md` (commit `4a2abf2`)
- **Pre-commitment ratification:** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`
- **Immediate-arc workstream queue:** `agentic_orchestration/immediate-arc-workstream-queue-2026-06-01.md`
- **WS1A.Q18 canonical lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Hypothesis-flow architecture:** `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`
- **Rocket OP:** `agentic_orchestration/operating-procedures/rocket.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**Response artifact:** path + commit
**Entry-point verdict:** CLI-PATH-CONFIRMED / ALTERNATIVE-PATH-RECOMMENDED / BLOCKED
**Specific arguments:** named or N/A
**Substrate-side V1 pre-fire check:** brief
**Routing back to KR:** "fire IA-1 V1 immediately at <entry-point>" / "fire setup dispatch first" / "escalate per escape clause"
```

After your response, KR fires IA-1 V1 dispatch (assuming CLI-PATH-CONFIRMED or alternative explicitly named).

---

**End of IA-1 rocket entry-point confirmation dispatch.**
