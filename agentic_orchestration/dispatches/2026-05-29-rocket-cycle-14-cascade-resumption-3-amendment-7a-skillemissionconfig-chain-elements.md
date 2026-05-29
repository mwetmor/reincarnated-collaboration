# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 Amendment 7a: SkillEmissionConfig chain_elements (Behavioral Hybrid Fix)

**Date:** 2026-05-29 evening late
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam)
**Authority:**
- Matt 2026-05-29 evening late + gandalf URGENT HALT directive
- gandalf Disc #42a Instance 6 #4 surface: SkillEmissionConfig not extended; chain_2.element on ChainSpec is metadata-only at skill emitter layer; hybrid kits structurally hybrid but behaviorally mono at SKILL CONTENT layer
- A2-1 RE-FIRE-3 already fired + CLOSED on partly-broken substrate (engine `85d8b41` + tag; $0.15 LLM cost burned; PASS technically true but substrate-led emergence promise NOT fully delivered for hybrid kits)
- Hive-mind decision-routing (Matt 2026-05-23 + Amendment 4 hive-state clarification) — gandalf design-steward authorized fix; rocket implementation seam; KR auto-routes in-scope

**Pattern:** Pattern A-light follow-up fix (~30-60min implementation + tests + smoke + Phase 2-4 re-fire verification)
**R48.4 / R48.5 RETIRED per Amendment 3**

---

## 0. TL;DR

**Extend `SkillEmissionConfig` with `chain_elements` field; thread per-chain element through `emit_skills_for_kit` so hybrid kits' chain_2 skills produce content-distinct (element=secondary) skills rather than namespace-only variation.**

Closes **Disc #42a Instance 6 #4** — the cascade-r3 fourth surface where chain_2.element exists on ChainSpec as metadata but per_skill_emitter.py uses single config.element for all chains.

**Effort:** ~30-60min. Backward-compatible (existing callers without chain_elements default to mono behavior). Auto-commit per CLAUDE.md addendum.

**Post-fix:** Phase 2-4 re-fire ($0 verification) → jack-ryan Gate-2 quick composition review → S6c production cascade Phase 5 LLM re-fire ($0.15-1.50; total cascade cost still <4% of $50 cap).

---

## 1. Required first reads (in order)

1. gandalf URGENT HALT (this dispatch authority) — Disc #42a Instance 6 #4 surface + Amendment 7a scope spec
2. Amendment 7 spec at `agentic_orchestration/gandalf/notes/2026-05-29-amendment-7-element-coverage-e4c-plus-hybrid-spec.md` § 2.3 Layer 3 (intended chain element assignment behavior)
3. `reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` — SkillEmissionConfig + emit_skills_for_kit
4. `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` lines 901-907 (chain_elements threading point per gandalf scope)
5. `tests/test_cascade_r3_amendment_7_element_coverage_hybrid.py` — Amendment 7 acceptance tests (verify these still PASS post-Amendment-7a)
6. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — Amendment 7 + A2-1 RE-FIRE-3 CLOSED checkpoint
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 + #2 + #11 + #41 + #42a + #45 LOAD-BEARING

---

## 2. Scope (gandalf URGENT HALT spec)

### 2.1 Extend SkillEmissionConfig (per_skill_emitter.py)

ADD field:
```python
chain_elements: dict[str, str] | None = None
```

- Maps chain_id → element
- None = use config.element for all chains (existing mono behavior; backward compatible)
- Non-None dict = per-chain element resolution

### 2.2 Amend emit_skills_for_kit inner loop (per_skill_emitter.py:400+)

Resolve per-chain element at skill emission point:

```python
chain_elem = (config.chain_elements or {}).get(chain_id, config.element)
```

Use `chain_elem` for:
- Placeholder name (if element appears in placeholder string template)
- `skill.element` field (the load-bearing change)

Backward-compatible: existing callers without `chain_elements` default to `config.element` (mono behavior).

### 2.3 Thread chain_elements at season_generation_pipeline.py:901-907

At kit-skill-emission integration point:

```python
if kit.is_hybrid:
    chain_elements = {
        "chain_A": kit.element,           # PRIMARY identity preserved
        "chain_B": kit.secondary_element, # HYBRID chain
        "chain_C": kit.element,           # SUPPORT primary identity
    }
else:
    chain_elements = None  # existing mono behavior
```

**Note on chain_id naming:** Use the codebase's existing chain_id convention (chain_A/B/C OR chain_1/2/3 OR equivalent). Rocket verifies the correct chain_id naming at the threading point; the dispatch lists chain_A/B/C as illustrative based on gandalf scope wording.

### 2.4 Tests (~5-10 new)

At `tests/test_cascade_r3_amendment_7a_skillemissionconfig_chain_elements.py`:

- Hybrid kit's chain_2 (chain_B) skills have `skill.element = kit.secondary_element` (NOT kit.element)
- Hybrid kit's chain_1 (chain_A) + chain_supporting (chain_C) skills have `skill.element = kit.element` (primary)
- Mono kit's chains all share `skill.element = kit.element` (unchanged behavior; backward-compat verification)
- 8-element coverage verification preserves Amendment 7 acceptance (all 8 elements present in primary+secondary at population level)
- Skill content layer distinct (NOT just namespace) — verify skill.element values per chain differ for hybrid kits

### 2.5 Smoke test + Phase 2-4 re-fire post-fix

- Smoke: emit_skills_for_kit on hybrid kit produces chain_2 skills with secondary element
- Phase 2-4 re-fire (smoke=False; halt_at_phase=5; ~50sec wall-clock; $0 LLM cost) to verify chain_elements threading produces behavioral-distinct hybrid chain_2 at full season scale
- Verify Amendment 6 + Amendment 7 composition still PASS (Pareto-2 + S7 deepcopy + S8 Bound 4 + STAT_ELEMENT_POOLS + Hybrid 17.5%)

---

## 3. Pre-ratified contingent decisions

| Decision point | Pre-ratified action |
|---|---|
| chain_elements default | None (backward-compatible mono behavior) |
| chain_id naming | Rocket verifies against codebase convention; gandalf scope lists chain_A/B/C illustratively |
| skill.element semantic | Per-chain element drives skill.element field (load-bearing for content-distinct emission) |
| Backward compatibility | Existing callers without chain_elements maintain mono behavior |
| Schema location | `chain_elements` in SkillEmissionConfig only (NOT new dataclass) |

---

## 4. Acceptance criteria

### 4.1 SkillEmissionConfig extended

- `chain_elements: dict[str, str] | None = None` field present
- Backward-compatible default

### 4.2 emit_skills_for_kit per-chain resolution

- Inner loop resolves `chain_elem` per chain_id via `config.chain_elements.get()` or fallback to `config.element`
- `skill.element` populated from `chain_elem`

### 4.3 Season pipeline threading

- Hybrid kits at line 901-907 thread `chain_elements` dict with primary/secondary/primary assignment
- Mono kits thread None

### 4.4 Tests PASS

- All new tests (§ 2.4) PASS
- Amendment 7 tests at `test_cascade_r3_amendment_7_element_coverage_hybrid.py` still PASS (no regression)
- Amendment 6 tests at `test_cascade_r3_amendment_6_combined_fix.py` still PASS
- All other existing tests PASS

### 4.5 Smoke + Phase 2-4 re-fire verification

- Smoke shows hybrid kit chain_2 skills have skill.element = secondary
- Phase 2-4 re-fire (smoke=False; halt_at_phase=5) closes without halt; 54 base + ~585 variants + 8-element coverage + hybrid rate within CI
- LLM cost = $0 (HALT at Phase 5 entry per halt_at_phase=5)

### 4.6 Tag

- Engine commit + tag (rocket prefix per CLAUDE.md: e.g., `rocket/v1.0-cascade-r3-amendment-7a-skillemissionconfig-chain-elements-1`)

---

## 5. Out-of-scope

- Phase 5 LLM re-fire (KR fires post-Gate-2; separate dispatch)
- A2-1 RE-FIRE-3 re-execution (cascade re-fire after Amendment 7a Gate-2)
- jack-ryan Gate-2 Pattern E review (KR fires post-rocket close)
- Modifications to Amendments 6 + 7 mechanical code (preserved; composition verification only)
- Phase 7 mechanical gate / Wave A / F-C / Wave B implementation (gamora + star-lord seams; CLOSED)
- LLM prompt template modifications (gandalf seam; closed)
- A/B comparison protocol

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **chain_id naming convention surprise** | Codebase uses different convention than chain_A/B/C OR chain_1/2/3 | Document at completion record; surface to KR |
| **skill.element field consumer breakage** | Downstream code consumes skill.element with assumptions about uniformity per kit | Document + surface to KR — may need additional follow-on |
| **Amendment 6/7 regression** | Existing tests fail post-Amendment-7a | Halt + surface to KR — fix coordination needed |
| **per-chain element produces unexpected skill content shifts** | Skill mechanics depend on element in non-obvious ways | Document at completion record; not necessarily blocking |
| **Disc #42a framing-audit catch beyond Instance 6 #4** | Q1-Q6 surfaces ADDITIONAL pre-imposed assumption | Halt + surface to KR — Instance 6 #5 candidate |
| **Effort exceeds ~2h** | Implementation significantly beyond ~30-60min | Surface to KR — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #2 smoke-test before tag** | § 4.5 smoke gate |
| **Disc #11 empirical inspection** | § 4 acceptance gates + Phase 2-4 re-fire verification |
| **Disc #41 substrate-led discipline** | LOAD-BEARING — hybrid intent is behavioral per Matt design call authorization; metadata-only fails substrate-led at content layer; Amendment 7a closes the gap |
| **Disc #42a framing-audit Q1-Q6** | LOAD-BEARING — Instance 6 #4 SYSTEMIC surface; Disc #42a Q2 (cheapest-empirical-refutation) caught at pre-Phase-5 layer; gandalf authored Amendment 7a fix |
| **Disc #45 vocabulary lock** | Element vocabulary at canonical names (per Amendment 7) |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |
| **Recognition → empirical validation → commit** | Recognition: gandalf Instance 6 #4 surface; Validation: § 4 acceptance + Phase 2-4 re-fire; Commit: rocket auto-commits per CLAUDE.md addendum |

---

## 8. Deliverables

1. **Engine commit(s)** — per_skill_emitter.py (SkillEmissionConfig extension + emit_skills_for_kit inner loop) + season_generation_pipeline.py:901-907 (chain_elements threading) + tests + tag (rocket prefix per CLAUDE.md)
2. **Completion record appended to this dispatch file** — captures: (a) SkillEmissionConfig extension evidence; (b) emit_skills_for_kit per-chain resolution evidence; (c) season pipeline threading evidence (hybrid + mono cases); (d) new tests results; (e) Amendment 6 + 7 regression check (still PASS); (f) Phase 2-4 re-fire verification (smoke=False; halt_at_phase=5; $0 cost; 8-element coverage preserved; hybrid rate within CI); (g) any § 6 surface findings; (h) Instance 6 #4 closure confirmation
3. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — Amendment 7a CLOSED + jack-ryan Gate-2 queued + S6c Phase 5 LLM re-fire queued
4. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per gandalf URGENT HALT directive + Matt 2026-05-29 evening late authority (Amendment 7a fix dispatch for Disc #42a Instance 6 #4)

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads (especially gandalf URGENT HALT + Amendment 7 spec § 2.3 Layer 3 intended behavior + per_skill_emitter.py current state + season_generation_pipeline.py:901-907 threading point)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Instance 6 #4 awareness LOAD-BEARING (verify implementation closes the structural-vs-behavioral gap at SKILL CONTENT layer)
3. Execute § 2 scope (extend SkillEmissionConfig + amend emit_skills_for_kit + thread season pipeline + tests + smoke + Phase 2-4 re-fire)
4. Apply § 4 acceptance gates
5. Surface per § 6 if triggered — auto-route in-scope per hive-mind decision-routing
6. Author § 8 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on Amendment 7a close:**
1. KR Disc #42a meta-observation 5 verification
2. Fire jack-ryan Gate-2 quick composition review of Amendment 7a (~30min; Pattern E)
3. Per Gate-2 PASS → fire S6c production cascade Phase 5 LLM re-fire (Wave A + F-C + Wave B at chain-element-content-distinct substrate) OR full Phase 2-7 re-fire (KR election based on Gate-2 + Amendment 8 + cost cap; production cascade likely full re-fire for clean season_001 with content-distinct hybrid)
4. Continue cascade A2-2 → A2-7 per existing sequence
5. Matt-surface at Amendment 7a CLOSE per gandalf URGENT HALT directive

**Cascade trajectory:** Amendment 7a → jack-ryan Gate-2 → S6c production cascade re-fire (full Phase 2-7 with content-distinct hybrid substrate) → A2-2 → A2-7 + D13 parallel → Cycle 14 v1 MVP D9 close.

**Signed:** knight-rider (orchestrator)
