# Dispatch — 2026-06-02 — EAA-1 — WS1A.4-lite implementation

**From:** knight-rider (orchestrator)
**Primary owner:** star-lord (LLM prompt + per-skill judgment integration in skill-naming pipeline)
**Co-owner:** rocket (engine skill-naming pipeline integration; emission path)
**Sub-agent:** gandalf-as-subagent for prompt template authoring per LOCK L
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 1)
**Authority:** Matt 2026-06-02 Pattern B substantive design session + Locks A-P pre-commitment package (LOCK L active for prompt design authority)
**Wave tag:** `EAA-1`
**Wave-open dispatch:** `agentic_orchestration/dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md` (READ FIRST)
**State file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
**Wave-open Gate-1 finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` (PASS-with-INFO)
**Estimated horizon:** ~3-5 sessions including prompt iteration cycles
**Gates:** jack-ryan Gate-1 pre-fire on this dispatch + Gate-2 on each prompt iteration

---

## 1. Authoritative reading (READ IN ORDER before any action)

1. `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.2 — per-skill flavor-or-canonical mechanism specification (binding)
2. `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` — Q18 vocabulary lock + Architecture A LOCK (per-primary rotating flavor pools + physical-as-taxonomy-sibling)
3. `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` v1.1 — load-bearing Q18 lock state; per-primary flavor word source
4. Wave-open dispatch (see header) — full chain context
5. `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md` — INFO-2 (jack-ryan Gate-2 scope clarification for EAA-1)

---

## 2. Scope

Implement WS1A.4-lite — per-skill LLM judgment that decides whether each skill name is **flavored** (uses a word from the kit's primary element's Q18 pool) or **canonical** (uses canonical naming convention). The LLM is invoked PER SKILL during the existing skill-naming pipeline; the decision is binary, with the flavor branch picking from the locked Q18 pool for that kit's primary element.

**Reference example from canonical record § 3.2 (Shadow primary necromancer kit, 6 skills):**

```
Skill 1: LLM picks YES + "bone"   → "Bone Spear"
Skill 2: LLM picks NO             → "Shadow Bolt"
Skill 3: LLM picks YES + "wraith" → "Wraith Touch"
Skill 4: LLM picks NO             → "Shadow Drain"
Skill 5: LLM picks YES + "shade"  → "Shade Veil"
Skill 6: LLM picks NO             → "Shadow Curse"
```

Kit identity stays **Shadow Necromancer** (primary element only; emergent kit concept derives from primary + cultural-tradition + period + chain composition + T4). The flavor word is a contextual skill-name flavor; NOT a kit identity tag.

**Architectural retirement (composes with EAA-2):** WS1A.4-lite REPLACES the cosmological_vocabulary slot-fill mechanism (ignition / suffusion / bulwark / etc. themed per-season). EAA-2 introduces skip-flags to bypass the legacy mechanism; EAA-1 introduces the replacement WS1A.4-lite per-skill judgment.

---

## 3. Sub-tasks

### 3.1 Prompt template authoring (gandalf-as-subagent per LOCK L)

star-lord invokes gandalf-as-subagent (Pattern A or Pattern A-deep per LOCK L authority) to author the initial WS1A.4-lite LLM prompt template.

**Prompt design requirements:**
- Composes against Q18 vocabulary pool + canonical record § 3.2 Architecture A discipline
- Physical opt-out (physical primary may or may not engage flavor branch; consult Q18 lock — physical-as-taxonomy-sibling pattern)
- Per-skill binary flavor-or-canonical decision
- If flavor: pick from kit's primary element's Q18 pool (NOT from a different primary's pool)
- Input context: skill role/archetype within kit + kit primary element + Q18 pool for that primary + canonical naming convention reference
- Output schema: `{flavor: bool, flavor_word: str | null, skill_name: str}`

### 3.2 Engine skill-naming pipeline integration (rocket primary; star-lord coordination)

rocket integrates the WS1A.4-lite call into the existing skill-naming pipeline. star-lord coordinates LLM call infrastructure (llm/ seam ownership).

**Integration requirements:**
- WS1A.4-lite fires per-skill (NOT per-kit; the binary decision is per-skill)
- Q18 pool consumed at flavor branch (Q18 pool source: `pool.json` v1.1 + `physical_taxonomy.json`)
- Kit primary element passed as context
- Emergent kit concept (e.g., "Necromancer") derives from existing per-kit naming logic; NOT changed by WS1A.4-lite
- Result lands in skill JSON entry with metadata (flavor_decision: bool + flavor_word_used: str | null) for downstream traceability

### 3.3 Smoke-test discipline (before full-fire validation)

Per Disc #2 smoke-test discipline:
- Run WS1A.4-lite against ~5-10 skills in isolation (single-kit smoke test) before integrating into full generation pipeline
- Verify Q18 pool consumption correctness (only kit's-primary-element pool consulted)
- Verify output schema validity
- Verify per-skill independence (Skill 1's flavor decision doesn't constrain Skill 2's)

### 3.4 Prompt iteration cycle (LOCK L active)

Per LOCK L:
- Initial prompt fires; star-lord routes output sample to jack-ryan Gate-2
- jack-ryan Gate-2 reviews **structural prompt fitness and discipline compliance** (NOT aesthetic verdict)
- If Gate-2 INFO/WARN: gandalf-as-subagent iterates prompt; star-lord re-fires
- If Gate-2 BLOCK twice (2+ iterations failing): escalate to Matt for aesthetic judgment per LOCK L escape clause

**Aesthetic vs structural scope (per Gate-1 INFO-2):**
- **jack-ryan Gate-2 scope:** structural prompt fitness — schema compliance, Q18 pool source correctness, per-skill independence, physical opt-out handling, decision binary integrity, no leakage of canonical-7+1 catalog semantics into prompt
- **Matt aesthetic judgment scope (per LOCK L escape clause):** whether the per-skill flavor-or-canonical naming quality is acceptable as creative output (grammaticality, naming sensibility, fantasy-genre coherence). Routes via LOCK L escape clause only after 2+ structural Gate-2 BLOCKs.

---

## 4. Out of scope (explicit non-goals)

- **Cosmological_vocabulary slot-fill** — handled by EAA-2 retirement (skip-flag pattern; not this dispatch)
- **R8 inverted-mode theme coalescence** — handled by EAA-2 (not this dispatch)
- **Kit identity logic (e.g., "Necromancer" emergence)** — existing per-kit naming logic; unchanged by EAA-1
- **Q18 pool amendments** — Q18 vocabulary IMMUTABLE per LOCK preservation in canonical record § 2.1
- **WS1A.3 per-kit sub-element selection** — RETIRED per canonical record § 3.2 (per-skill flavor decision replaces per-kit sub-element framing)
- **Per-kit engagement telemetry** — out of scope; deferred per canonical record § 7.4
- **Kit-space output schema** — EAA-3 scope; per-skill metadata fields land in skill JSON entries per existing schema patterns + LOCK K additive extensions if needed

---

## 5. Cross-seam contract (Principle 6)

**Cross-seam touches:**
- star-lord (LLM call infrastructure; llm/ seam) ↔ rocket (engine skill-naming pipeline; generation/ seam): WS1A.4-lite call added to skill-naming pipeline
- Skill JSON output schema extended additively (per-skill flavor_decision metadata fields)

**Discipline:** additive per LOCK J + LOCK K. ADR-004 MIGRATION.md required for skill JSON schema extension.

**Round-trip:** if schema extension breaks backward-compat unexpectedly, escalate per LOCK J escape clause.

---

## 6. Acceptance criterion

EAA-1 PASSES when:
1. WS1A.4-lite prompt template authored by gandalf-as-subagent + jack-ryan Gate-2 PASS on structural prompt fitness
2. WS1A.4-lite integrated into engine skill-naming pipeline (rocket)
3. Smoke-test on ~5-10 skills demonstrates correct Q18 pool consumption + per-skill independence + output schema validity
4. Skill JSON output schema additive extension MIGRATION.md authored (or noted as schema-compatible if no extension needed)
5. No regressions in existing skill-naming pipeline for any unaffected paths

---

## 7. Tag intent

Per CLAUDE.md tag conventions:
- Intermediate work: `star-lord/v1.4-eaa-1-ws1a-4-lite-<n>` or equivalent per star-lord seam discipline
- Cross-seam tag prefix if touching rocket: coordinate per ADR-004
- Wave-close milestone tag deferred to EAA-8 (chain-level)

---

## 8. Auto-commit + auto-push

Per Matt 2026-06-02 explicit cycle-push authorization for EAA chain + CLAUDE.md addendum 2026-05-25:
- Auto-commit work-products as you go (no per-commit Matt re-asking)
- Auto-push per established cycle-push pattern
- Update wave-state file workstream status table on completion

---

## 9. References

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.2
- **Q18 vocabulary lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Pool.json v1.1:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
- **Physical taxonomy:** `~/Games/reincarnated-engine/data/seasonal_elements/physical_taxonomy.json`
- **Wave-state:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- **Wave-open Gate-1 finding:** `agentic_orchestration/qa/findings/2026-06-02-eaa-wave-open-gate-1.md`
- **LLM seam owner:** star-lord operating procedure
- **Generation seam owner:** rocket operating procedure
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

**End of EAA-1 dispatch. Fires after jack-ryan Gate-1 PASS on this dispatch.**

---

## Completion record

**Completed by:** star-lord
**Date:** 2026-06-02
**Status:** COMPLETE (star-lord seam; rocket co-owner scope pending)

### Commits

| Sha | Tag | Repo | Contents |
|---|---|---|---|
| `54215d8` | `star-lord/v1.4-eaa-1-ws1a-4-lite-1` | reincarnated-engine | New module `ws1a4_lite_flavor_judgment.py` + 34 smoke tests + `__init__.py` exports + MIGRATION.md EAA-1 entry |

### Gate-2 verdict

**PASS-with-INFO.** No structural BLOCKs. No WARNs. Three INFOs (none require remediation before pipeline integration).

Finding file: `agentic_orchestration/qa/findings/2026-06-02-eaa-1-ws1a-4-lite-gate-2.md`

INFOs:
- INFO-1: "bone" example in system prompt not in shadow Q18 pool — structural guard (`_validate_output()`) catches any invalid word and triggers retry; no remediation required
- INFO-2: `_BACKOFF_SECONDS[2]` (8.0s) never reached at `_MAX_ATTEMPTS=3` — future-proofing only; no correctness issue
- INFO-3: `ws1a4_attempt_number` 1-indexed semantics not explicit in MIGRATION.md consumer obligations block — no blocking concern; one-line clarification recommended on next routine MIGRATION.md touch

LOCK L escape clause: NOT triggered (zero BLOCKs; first Gate-2 iteration PASS).

### Smoke-test results

34/34 PASS. All structural criteria covered (physical opt-out, Q18 pool correctness, per-skill independence, schema validation, retry/fallback path, kit-level driver, prompt elements).

### Acceptance criterion check

1. ✅ WS1A.4-lite prompt template authored by gandalf-as-subagent + jack-ryan Gate-2 PASS on structural prompt fitness
2. ✅ WS1A.4-lite integrated into engine skill-naming pipeline — COMPLETE (rocket co-owner scope; `apply_kit_space_skill_naming()` + batch driver + `KitSpaceNamingRunStats`; sha=cdc8531 / tag=rocket/v1.4-eaa-1-rocket-wiring-1)
3. ✅ Smoke-test on 34 synthetic skills demonstrates correct Q18 pool consumption + per-skill independence + output schema validity
4. ✅ Skill JSON output schema additive extension MIGRATION.md authored (4 new fields: `ws1a4_flavor_decision`, `ws1a4_flavor_word_used`, `ws1a4_attempt_number`, `ws1a4_is_fallback`)
5. ✅ No regressions in existing skill-naming pipeline (module is additive; existing paths untouched)

### EAA-5 readiness (star-lord perspective)

EAA-1 star-lord seam: COMPLETE. EAA-5 is blocked on EAA-1+2+3+4 all PASS. EAA-2 and EAA-4 have star-lord co-owner scope pending; EAA-3 has star-lord co-owner scope pending. EAA-2+3+4 still FIRING at time of this completion record.

### Files modified / created

- `src/reincarnated/llm/ws1a4_lite_flavor_judgment.py` — NEW (module implementing WS1A.4-lite)
- `tests/test_ws1a4_lite_flavor_judgment.py` — NEW (34 smoke tests)
- `src/reincarnated/llm/__init__.py` — MODIFIED (9 new exports added)
- `src/reincarnated/llm/MIGRATION.md` — MODIFIED (EAA-1 entry appended)

---

## Completion record — rocket co-owner (2026-06-02)

**Completed by:** rocket
**Date:** 2026-06-02
**Status:** COMPLETE — EAA-1 all 5 acceptance criteria MET (both seams)

### Commits

| Sha | Tag | Repo | Contents |
|---|---|---|---|
| `cdc8531` | `rocket/v1.4-eaa-1-rocket-wiring-1` | reincarnated-engine | New module `kit_space_skill_naming.py` + 19 smoke tests + MIGRATION.md EAA-1 entry |

### Gate-2 verdict

**PASS-with-INFO.** No structural BLOCKs. No WARNs. Two INFOs (non-blocking).

Finding file: `agentic_orchestration/qa/findings/2026-06-02-eaa-1-rocket-wiring-gate-2.md`

INFOs:
- INFO-1: Phase 5 overwrites WS1A.4-lite name field — intent ambiguous; clarify at next MIGRATION.md touch whether Phase 5 name is authoritative or WS1A.4-lite name is authoritative
- INFO-2: `ws1a4_attempt_number` 1-indexed semantics (1 = first attempt; 0 = no-LLM fallback) not restated in rocket MIGRATION.md consumer obligations block

### Smoke-test results

19/19 PASS. Coverage: output schema validity, physical opt-out, skip_cosmological_vocabulary=False (WS1A.4-lite not called), skip_cosmological_vocabulary=True (WS1A.4-lite fires), no-LLM mode, per-skill independence, stats accumulation, batch driver, kit summary helper.

### Files modified / created

- `src/reincarnated/generation/kit_space_skill_naming.py` — NEW (EAA-1 rocket wiring module)
- `tests/test_kit_space_skill_naming.py` — NEW (19 smoke tests; 19/19 PASS)
- `src/reincarnated/generation/MIGRATION.md` — MODIFIED (EAA-1 rocket wiring entry prepended)
