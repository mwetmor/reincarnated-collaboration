# Dispatch — Gandalf — Cycle 14 Cascade-Resumption-3 Math-Note Review (Amendment 5 Expanded Scope)

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** gandalf (story-and-design steward)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendments 1-5 (Amendment 5: Matt-gate at Phase 5 entry of S6c per gandalf commit `7f3fb54`)
- Gamora Phase 7 mechanical gate fix CLOSED (engine `496814b` + tag `gamora/v2.17-cascade-r3-phase7-mechanical-gate-fix-1`); math note at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md`
- Hive-mind decision-routing (Matt 2026-05-23) + Matt 2026-05-29 hive-state clarification (KR auto-routes in-scope)
- Amendment 5 sub-action: gandalf math-note review EXPANDED SCOPE — Wave B firing logic (per-variant vs per-base-kit) feeds Matt-gate cost projection

**Pattern:** Pattern A-light analytical review (~15-30min; NO code modification; output feeds Matt-gate cost projection)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Parallel-firing companion this batch:** rocket S6c-Phase-2-4 (Phase 2-4 production fire + HALT at Phase 5 entry; ~30min-1h)

---

## 0. TL;DR

**Review gamora math note at `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md` per Amendment 5 expanded scope:**

1. **Threshold change validation** (0.70 → 0.50 `P7_GAUNTLET_PASS_FLOOR`) per W-α6 calibration anchor
2. **Cost projection at full-season scale** — Wave A call count × cost + F-C call count × cost + Wave B call count × cost; 3-season cascade projection vs $50 soft cap
3. **Wave B firing logic clarification** — per-variant vs per-base-kit? Determines Wave B call count (54 base kits vs 810 variants) — material cost projection difference
4. **Output feeds Matt-gate cost projection** at S6c Phase 5 entry (Amendment 5 § "Gate surface content" item 4)

**Effort:** ~15-30min. NO code modification (analytical review only). Output: review note + cost projection table for Matt-gate consumption.

---

## 1. Required first reads

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Amendment 5 (header) + sub-action capture
2. `reincarnated-engine/src/reincarnated/simulation/math/cascade-r3-phase7-mechanical-gate-alignment-2026-05-29.md` — gamora math note (review target)
3. `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-cascade-resumption-3-phase7-mechanical-gate-fix.md` — gamora Phase 7 fix completion record (§ (e) smoke re-fire: 12/18 shipped + cost projection inputs)
4. `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-phase7-mechanical-gate-investigation.md` — gamora investigation (Verdict B + Option α reasoning)
5. `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — Wave A + F-C + Wave B prompt templates + spec (informs cost projection)
6. `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — Wave A + F-C + Wave B implementation (per-cluster vs per-pair vs per-kit semantics)
7. `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — Phase 5 hook (S5b integration; sequence Wave A → F-C → Wave B)
8. Recognition record Amendment 3 (variant inheritance H0/H1) — informs Wave B per-variant vs per-base-kit framing

---

## 2. Scope (analytical review; NO code modification)

### 2.1 Threshold change validation

Review gamora math note derivation of `P7_GAUNTLET_PASS_FLOOR = 0.50`:
- A2-1 Step 1 calibration anchor: `eligible_encounters_passed(cohort) >= 9` against W-α6 24-cell `ENCOUNTER_COHORT_KPM_BAND`
- 9/18 = 0.50 (strict greater-than preserved per gamora math note § 3.2)
- Cohort midpoint semantics preserved at high level
- Verify: alignment math sound; W-α6 anchor canonical

Output: PASS / WARN / BLOCK on threshold derivation

### 2.2 Cost projection at full-season scale

Per full-season cardinality estimates:
- **Phase 2 base kits:** 54 (18 BC × N=3 per S7)
- **Phase 4 archive variants:** ~810 (270 cells × 3 invest profiles per S2 Option C → ~810 enumerated; ~810 shipped post-strip-and-ship per gamora research)

**Wave A** (faction-level LLM): per-cluster call. Number of clusters = 4 GMM clusters at S6a smoke (598 variant input). Full season: similar 4-7 clusters expected. Cost: ~4-7 calls × $0.X = $X-Y per season.

**F-C** (per-pair inter-faction): per-pair call. 4 clusters → C(4,2) = 6 pairs. Cost: 6 × $0.X = $Y per season.

**Wave B** (per-kit identity LLM): **firing logic question** — per-base-kit (54 calls) OR per-variant (810 calls)? Difference is **~15× cost differential.**

| Wave B firing | Calls per season | Cost per season (rough) | 3-season total | vs $50 cap |
|---|---|---|---|---|
| Per-base-kit | 54 | ~$0.50-1 | ~$1.50-3 | well under $50 |
| Per-variant | 810 | ~$8-15 | ~$24-45 | approaches $50 |
| Hybrid (per-unique-(BC×lineage)) | ~50-150 | ~$0.50-1.50 | ~$1.50-4.50 | well under $50 |

### 2.3 Wave B firing logic clarification

Read `phase5_orchestrator.py` `run_wave_b_async()` (line 2074) + `_build_kits_input_for_wave_b()` in `wave5_season_orchestrator.py` (line 1019). Determine current logic:

- Does Wave B fire per BASE KIT (54 calls / season; cohesion-judge per-kit identity at base level)?
- Does Wave B fire per VARIANT (810 calls / season; cohesion-judge per (BC × T4 × invest) variant)?
- OR per HYBRID UNIT (e.g., per unique (BC × cultural_lineage_canonical) combination)?

Per canonical § 5 Wave B spec: "per-kit identity LLM" — implies per kit. But "kit" semantics: base kit OR variant kit?

Recognition record Amendment 3 H1 framing: variant inheritance from base kit; per-variant cohesion judge OVER-FIRES if variants inherit base kit identity. Per-base-kit firing aligns with H0 (variant inheritance correct).

Output: clarification of current implementation + recommendation for Matt-gate cost projection

### 2.4 Output (review note)

Authored at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-r3-math-note-review-expanded.md`:

- § 1 — Threshold change validation (PASS/WARN/BLOCK + reasoning)
- § 2 — Cost projection at full-season scale (per-variant vs per-base-kit table)
- § 3 — Wave B firing logic clarification (current implementation + recommendation)
- § 4 — Matt-gate cost projection input (consolidated table KR uses at gate surface)

---

## 3. Acceptance criteria

- § 2.4 review note authored
- Threshold validation verdict explicit
- Cost projection table at full-season scale
- Wave B firing logic clarified (per-variant vs per-base-kit)
- Matt-gate cost projection input ready for KR consumption at S6c Phase 5 entry

---

## 4. Out-of-scope

- ANY code modification (analytical review only)
- Wave A / F-C / Wave B prompt template modification (gandalf seam; S4 closed; Amendment 4 amended regex)
- Canonical doc 47 § 4.6.9 modification (already amended)
- Recognition record Amendment 3 H1 investigation (separable axis; fires at A2-1 RE-FIRE-3 + 3 seasons cascade per recognition record)
- S6c-Phase-2-4 fire (parallel-firing rocket dispatch)
- S6c-Phase-5+ continuation (post-Matt-gate)
- Phase 7 mechanical gate code changes (gamora seam; CLOSED)
- A/B comparison protocol

---

## 5. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Threshold derivation BLOCK** | Gamora math note threshold derivation has architectural issue | Halt + surface to KR — gandalf design-spec-as-math handoff or Matt re-engage |
| **Wave B firing logic ambiguous** | Current implementation doesn't clearly support per-base-kit OR per-variant; semantic gap | Document at review note; surface to KR — may need additional implementation clarification before Matt-gate |
| **Cost projection at full-season exceeds $50** | Per-variant Wave B firing × 3 seasons > $50 cap | Document at review note; Matt-gate will surface with status "approaches/exceeds cap"; Matt election informed |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-review | Halt + surface to KR |
| **Effort exceeds ~1h** | Review complexity significantly beyond ~15-30min | Surface to KR — scope reconsideration |

---

## 6. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | Cost projection grounded in gamora math note + Phase 5 orchestrator code + canonical Wave B spec |
| **Disc #18 math hotspot consultation** | Math-note review IS gandalf design-steward consultation function |
| **Disc #41 substrate-led vocabulary lock** | Cost projection uses locked vocabulary (base kit / variant / lineage / cluster) |
| **Disc #42a framing-audit Q1-Q6** | Applied at review — Instance 2 sub-case awareness (pass_rate semantic alignment documented by gamora); Wave B firing logic semantic clarification |
| **Disc #45 vocabulary lock** | Review output uses locked vocabulary |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |

---

## 7. Deliverables

1. **Review note** at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-r3-math-note-review-expanded.md`
2. **Completion record appended to this dispatch file** — captures: (a) threshold validation verdict; (b) cost projection table; (c) Wave B firing logic clarification; (d) Matt-gate cost projection input ready
3. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 8. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 5 sub-action (gandalf math-note review expanded scope) + hive-state clarification (KR auto-routes in-scope)

**Gandalf session-start protocol:**
1. Onboard via § 1 required first reads
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption
3. Execute § 2 scope (review + clarify + project)
4. Apply § 3 acceptance gates
5. Surface per § 5 if triggered
6. Author § 7 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on close:** consume cost projection + Wave B firing logic clarification for Matt-gate surface authoring (post S6c-Phase-2-4 close).

**Parallel-firing companion this batch:** rocket S6c-Phase-2-4 (Phase 2-4 production fire + HALT at Phase 5 entry).

**Cascade trajectory:** Gandalf review + S6c-Phase-2-4 parallel → KR Matt-surface (5-item gate content) → Matt RATIFY-FIRE → S6c-Phase-5+ → A2-2 → A2-7 + D13 parallel → Cycle 14 v1 MVP D9 close.

**Signed:** knight-rider (orchestrator)
