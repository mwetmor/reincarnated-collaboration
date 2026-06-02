# Gate-2 Finding — EAA-1 WS1A.4-lite — Structural Prompt Fitness Review

**Finding type:** Gate-2 (post-implementation structural review)
**Finding ID:** 2026-06-02-eaa-1-ws1a-4-lite-gate-2
**Authored by:** jack-ryan (QA / quality guardian)
**Date:** 2026-06-02
**Reviewer scope:** structural prompt fitness and discipline compliance (per dispatch § 3.4 and Gate-1 INFO-2 scope clarification — NOT aesthetic judgment)
**Artifact under review:** commit `54215d8` / tag `star-lord/v1.4-eaa-1-ws1a-4-lite-1`
**Files reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/ws1a4_lite_flavor_judgment.py`
- `/Users/admin/Games/reincarnated-engine/tests/test_ws1a4_lite_flavor_judgment.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/MIGRATION.md` (EAA-1 entry)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/__init__.py` (export additions)

---

## Verdict: PASS-with-INFO

No structural BLOCKs. No WARNs. Three INFOs. Pipeline integration (rocket co-owner scope) can proceed.

---

## Structural criteria evaluated

### SC-1 — Schema compliance (output schema validation at boundary)

**Result: PASS**

`_validate_output()` enforces the contract `{flavor: bool, flavor_word: str | null, skill_name: str}` at the LLM response boundary before any result is accepted. Validation confirms: (a) flavor=True requires flavor_word present and in Q18 pool; (b) flavor=False forces flavor_word=null regardless of LLM response (defensive null override). Discipline #8 (schema validation at boundaries) satisfied.

### SC-2 — Q18 pool source correctness

**Result: PASS**

`Q18_FLAVOR_POOL` transcribed directly from `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 2. Automated tests verify entry counts per primary: fire(16), water(14), earth(18), wind(13), lightning(13), holy(14), shadow(12) = 100 rotating entries. Pool is immutability-tested (modification raises TypeError). User prompt injects only the kit-primary's pool — no cross-primary contamination path exists.

### SC-3 — Per-skill independence

**Result: PASS**

`apply_ws1a4_lite_to_kit()` driver passes `cross_skill_names` as `list[str]` (prior skill names only — for naming cohesion context). It does NOT pass decision history, FlavorJudgmentResult objects, or any prior flavor/canonical verdict. Each LLM call is structurally isolated. Per-skill independence requirement (dispatch § 3.3 bullet 3) satisfied.

### SC-4 — Physical opt-out handling

**Result: PASS**

`PhysicalPrimaryOptOut` raised immediately in `judge_skill_flavor()` when `primary_element.lower() == PHYSICAL_PRIMARY`. Raised before any prompt construction, before any LLM call, before any pool lookup. No LLM tokens consumed for physical kits. Physical as taxonomy-sibling (not a flavor pool) correctly enforced per Q18 lock § 4.2.

### SC-5 — Decision binary integrity

**Result: PASS**

Output admits exactly two branches: `flavor=True` (flavor_word from Q18 pool, non-null, skill_name incorporates it) or `flavor=False` (flavor_word null, skill_name canonical). Validation rejects any response not conforming to this binary. No tertiary or ambiguous state is possible post-validation.

### SC-6 — No canonical-7+1 catalog semantic leakage into prompt

**Result: PASS**

System prompt references "Shadow Necromancer" conceptually (from canonical record § 3.2 example) but does NOT embed or reference canonical-7+1 catalog entries, element hierarchy, or foundation layer semantics. The prompt is scoped to: (1) Q18 pool for the kit's primary, (2) skill node structural properties (node_type, tier, chain_id), (3) kit_concept string, (4) prior skill names for cohesion. No catalog leakage path identified.

---

## Findings

### INFO-1 — "bone" example in system prompt not in shadow Q18 pool

**Severity:** INFO
**Principle:** Discipline #8 (schema validation at boundaries), Discipline #11 (empirical inspection)

The system prompt uses "Bone Spear" from canonical record § 3.2 to illustrate per-skill flavor-word usage. "bone" is not in the shadow Q18 pool (shadow pool: shade, wraith, void, eclipse, phantom, dusk, umbra, hollow, obsidian, veil, crypt, shadow = 12 entries). If an LLM reads this as an example of an acceptable shadow flavor word, validation catches it: `_validate_output()` rejects any flavor_word not in the primary's pool and triggers retry → fallback.

Structural guard is present and correct. The example serves illustrative intent (flavor-word-not-kit-identity pattern) and is grounded in the canonical record's own example. No remediation required before pipeline integration.

**Empirical criterion for re-engagement:** if smoke-test log shows systematic retry on "bone" for shadow kits (>1 fallback per 10 shadow skills), revisit the prompt example. Current test coverage covers this path (retry-on-invalid-word test passes).

### INFO-2 — Dead backoff entry at `_BACKOFF_SECONDS[2]`

**Severity:** INFO
**Principle:** Discipline #11 (empirical inspection)

`_BACKOFF_SECONDS = [2.0, 4.0, 8.0]` has 3 entries but `_MAX_ATTEMPTS = 3` means the third backoff (8.0s) is never reached: the retry loop exhausts at attempt 3 without sleeping. This is future-proofing: if `_MAX_ATTEMPTS` is raised to 4, the 8.0s backoff fires correctly.

Not a correctness issue. Not a cost issue. No remediation required.

### INFO-3 — `ws1a4_attempt_number` field: 1-indexed semantics should be noted in MIGRATION.md consumer obligations

**Severity:** INFO
**Principle:** Discipline #8 (schema validation at boundaries), ADR-004

`ws1a4_attempt_number` is 1-indexed (1=first attempt, 2=second, 3=third). The MIGRATION.md EAA-1 entry documents the field exists and its semantic (attempt on which the accepted result was returned) but does not explicitly state 1-indexed. Downstream consumers (drax, analysis queries) should not assume 0-indexed.

No blocking concern — the intent is clear from code inspection. Recommended: one-line clarification in MIGRATION.md consumer obligations block on next routine MIGRATION.md touch. Not a release-blocking item.

---

## Smoke-test coverage note

34 automated tests authored and all PASS. Tests cover:
- Physical opt-out (1 test)
- Unknown primary rejection (1 test)
- No-LLM canonical fallback path (1 test)
- Q18 pool entry counts, parametrized all 7 rotating primaries (7 tests)
- Per-skill independence structural guarantee (1 test)
- Output schema validation (6 subtests)
- LLM mock happy paths (2 tests)
- Invalid-word retry → fallback path (1 test)
- Kit-level driver (3 subtests)
- Pool immutability (1 test)
- Q18 spot-checks, parametrized 7 primaries (7 tests)
- Prompt structural elements (1 test)
- User prompt correct pool injection (1 test)

Discipline #2 smoke-gate: SATISFIED. Full integration in rocket's pipeline can proceed.

---

## MIGRATION.md coverage

EAA-1 entry in `/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/MIGRATION.md` documents:
- New module and public API
- Skill JSON schema additive extension (4 new fields)
- Token delta per 20-kit run (~$0.24-0.40)
- Retry policy (3 attempts, exponential backoff 2s/4s/8s, canonical fallback on exhaustion)
- Consumer obligations (physical opt-out; attempt_number field semantics)
- Backward-compat guarantee (additive only; old seasons remain readable)
- Smoke-test gate reference

ADR-004 cross-seam contract documentation: SATISFIED.

---

## Sign-off

**Gate-2 PASS.** EAA-1 prompt template and module are structurally fit. Integration into skill-naming pipeline (rocket co-owner scope) can proceed. LOCK L escape clause not triggered (zero structural BLOCKs; first Gate-2 iteration).

**Author:** jack-ryan
**Date:** 2026-06-02
**Anchor docs cited:** dispatch § 3.4, dispatch § 3.3, Q18 lock § 4.2, canonical record § 3.2, Discipline #2, Discipline #8, Discipline #11, ADR-004
**Commit under review:** `54215d8` / `star-lord/v1.4-eaa-1-ws1a-4-lite-1`
