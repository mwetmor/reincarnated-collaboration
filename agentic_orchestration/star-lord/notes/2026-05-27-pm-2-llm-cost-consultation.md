# Pattern-A Response — PM-2 Faction-Label Assignment LLM Cost + Architecture Consultation

**Author:** star-lord (export / output / telemetry / LLM seam owner)
**Pattern:** A-deep (methodology-anchored verdict + cost projection; file output requested by KR)
**Date:** 2026-05-27
**Invocation authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Disciplines applied:** #18 (methodology-before-execution), #11 (empirical inspection), #46 (LOAD-BEARING), #1 (math-before-code)

**Source docs consulted:**
- `reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md`
- `reincarnated-engine/src/reincarnated/llm/client.py` (retry infrastructure)
- `reincarnated-engine/src/reincarnated/llm/tracked_client.py` (cost tracking infrastructure)
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` (seam state)

---

## Top-line

gandalf's D-Hybrid + D-Separate recommendation is **CONFIRMED** from the LLM-call-infrastructure perspective. All six architectural questions receive favorable dispositions with no blocking issues. One non-blocking architectural surprise is noted (two-phase sequencing dependency creates a call dependency that must be explicit in the Dispatch 3B implementation spec). Framing-audit Q1/Q2/Q3 applied per Discipline #42; verdict is PROCEED. The full response follows for KR integration into Matt-gate routing.

---

## 1. Cost Projection — PM-2 D-Separate within SC-3 Envelope

### Empirical baseline (SC-3 Pattern B PRIMARY per SC-3 § 7)

SC-3 estimates ~2,100 total calls per season at the per-skill + per-gear-slot granularity, with character-identity calls (~16 per season) as the load-bearing quality subset. Budget envelope: $0.50–$5 per season. At Claude Sonnet 4.6 pricing (the current `DEFAULT_MODEL` per `client.py` line 10: `"claude-sonnet-4-6"` at $3.00 input / $15.00 output per million tokens per `tracked_client.py` lines 18-20), the empirical per-call cost at 2,100 calls × ~$0.002/call (typical per SC-3 context window) lands within the $0.50–$5 envelope.

### PM-2 D-Separate incremental calls

PM-2 D-Separate adds **3–5 LLM calls per season** — one call per emergent cluster from PM-1. These are cluster-level calls, not per-kit calls. Context window per call: larger than a per-kit call (cluster_id + member_count + modal substrate fields + 3 kit reps + faction_label_placeholder + season_id), but bounded. Empirically:

- SYSTEM prompt: ~300-500 tokens (thematic-identity synthesizer instruction + negative examples + THEMATIC_REGISTRY subset at 30-50 terms per element × cultural_lineage cell)
- USER prompt: ~400-600 tokens (CLUSTER_LAYER fields + KIT_REPS_LAYER 3 reps + SUBSTRATE_CONTEXT)
- Output: ~100-200 tokens (faction_name 2-5 words + faction_identity_narrative 1-2 sentences + faction_thematic_tags 3-5 keywords)

Per-call cost estimate at Claude Sonnet 4.6:
- Input: 900 tokens × $3.00/M = $0.0027
- Output: 150 tokens × $15.00/M = $0.0023
- Per call: ~$0.005

At 3–5 calls per season:
- Baseline: 3 × $0.005 = **$0.015**
- Maximum: 5 × $0.005 = **$0.025**
- With 2× regeneration worst-case (cross-faction diversity check fails and all clusters regenerate): 5 × 2 × $0.005 = **$0.05**

**gandalf's estimate of $0.15–$0.25 per season is the ceiling, not the expected cost.** The expected cost is $0.015–$0.025. The $0.15–$0.25 upper bound in PM-2 § 3.2 appears to assume a larger model or larger context windows than the actual per-cluster scope warrants. However, the $0.15–$0.25 ceiling is structurally sound as a conservative estimate for THEMATIC_REGISTRY growth (if the registry expands to 100-200 terms per cell at full gandalf authoring scope, input token counts will grow proportionally).

**Conclusion on cost:** PM-2 D-Separate fits **well within** the SC-3 Pattern B envelope of $0.50–$5. Total season cost with PM-2 additions = SC-3 baseline + $0.015–$0.05. This does not materially change the per-season LLM cost regime. The $0.15–$0.25 gandalf estimate is CONFIRMED as conservative upper bound; the tighter expected range is $0.015–$0.05. KR should record both the expected and ceiling values in the Matt-gate ratification artifact.

**Note on model tiering:** SC-3 § Recommendation 1 suggests tiering — smaller model for volume calls (skill naming, gear descriptors), larger for character_name + core_identity_narrative. PM-2 faction-label calls are low-volume (3-5 per season) + high-quality requirement (faction names are structural markers in Phase 7 joint-gate). Star-lord recommendation: faction-label calls use Claude Sonnet 4.6 minimum (not the cheaper haiku model). At $0.005/call × 5 calls, the cost differential from upgrading is negligible ($0.025 sonnet vs ~$0.008 haiku). Quality justifies sonnet. This is a Dispatch 3B implementation decision, not gating.

---

## 2. LLM Call Architecture Composition — Per-Kit and Per-Cluster Sequencing

### Current infrastructure capability

The existing `LLMClient` + `TrackedLLMClient` infrastructure (`client.py`, `tracked_client.py`) is fully capable of supporting both per-kit Pattern B calls (Option α Note 4) and per-cluster Pattern B calls (PM-2) within the same season-emit pipeline. `set_context(purpose=..., entity_type=..., entity_id=...)` stamps every call with its classification — per-kit calls use `entity_type="kit"`, per-cluster calls use `entity_type="faction_cluster"`. Cost tracking is automatic via `TrackedLLMClient.complete()`. No infrastructure changes needed.

### Sequencing dependency: faction-labels-BEFORE per-kit canonical names

This is the key architectural finding. The two call types are NOT independent and NOT fully parallel:

**PM-2 D-Separate calls MUST fire BEFORE per-kit Pattern B calls that include faction_name in the per-kit output context.**

Rationale: SC-3 Pattern B's per-kit structured output schema includes `spirit_guide_hooks` and `skill_flavor_keys`, which may reference the kit's parent faction identity for thematic coherence. If the per-kit call fires first without knowing the faction_label_canonical, one of two sub-optimal outcomes follows:

1. The per-kit call produces output with no faction-context — then faction_label_canonical must be injected post-hoc (awkward; faction context was available at call time but unused)
2. The per-kit call produces output that implicitly invents faction framing (AI-tell risk — the kit LLM call will pattern-match "what faction is this kit from" without constraint)

**Correct sequencing:**
```
Phase 4: faction_label_placeholder (deterministic; no LLM; fires at archive-insertion time)
Phase 5, Step 1: PM-2 D-Separate LLM calls (3-5 calls; one per cluster; fires FIRST)
  → faction_label_canonical + faction_identity_narrative + faction_thematic_tags produced
Phase 5, Step 2: Per-kit Pattern B calls (Option α Note 4; 16-40+ calls per season)
  → Each kit call receives its parent faction's faction_label_canonical as a SUBSTRATE_CONTEXT field
  → Enables thematic coherence between kit identity and faction identity
  → Satisfies Phase 7 joint-gate cohesion criterion (kit identity coherent with parent faction label)
```

This sequencing also addresses PM-2 § 7.1 Q2 (dependency ordering) directly: **faction-label calls fire FIRST; per-kit calls fire SECOND.** The per-kit call can receive faction_name as an additional SUBSTRATE_CONTEXT input, enabling the kit's core_identity_narrative to be thematically consistent with the faction without being determined by it.

**Practical parallelism opportunity:** Per-cluster PM-2 calls (3-5 calls) CAN fire in parallel with each other (clusters are independent). Then, once all PM-2 cluster calls complete, per-kit calls for all kits CAN fire in parallel with each other (kits within a cluster are independent once faction_label_canonical is known). This is a two-wave pattern within Phase 5: wave A = parallel faction calls, wave B = parallel kit calls.

**Dispatch 3B must make this sequencing explicit.** It is the load-bearing implementation constraint from this consultation. If Dispatch 3B authors the per-kit and per-cluster calls as fully independent parallel fires, per-kit outputs will lack faction context, and Phase 7 joint-gate cohesion will be structurally weaker.

**Discipline #8 implication:** the export schema at `schemas.py` will need a `faction_label_canonical` field added to the per-kit export output (likely `ExportAlterationOutput` or a Phase 5 overlay model). This field flows from PM-2 cluster output into the per-kit call context AND into the export packet. This is a new field — MIGRATION.md entry required at Dispatch 3B time. Star-lord flags this now so Dispatch 3B's scope includes the MIGRATION.md requirement.

---

## 3. `faction_visibility = invisible` Short-Circuit Policy

**Disposition: CONFIRM short-circuit is architecturally supportable; recommend ENGINE-FLAG-GOVERNED deferral of PM-2 LLM canonical layer for Reincarnated v1.**

The `TrackedLLMClient.set_context()` infrastructure already supports purpose-tagging. The short-circuit pattern is:

```python
if profile.faction_visibility == "invisible" and not profile.monster_contrast_enabled:
    # Skip PM-2 LLM canonical layer entirely
    # faction_label_canonical = None
    # faction_identity_narrative = None
    # faction_thematic_tags = None
    # Use faction_label_placeholder for all engine-internal consumers
    pass
else:
    # Fire PM-2 D-Separate LLM calls
    faction_label_canonical = llm_client.complete_json(...)
```

**Star-lord recommendation:** the Dispatch 3B implementation should wire this as an engine-flag check at the Phase 5 pipeline entry point. When `faction_visibility = invisible` AND monster-contrast pipeline is `False` (per profile config), PM-2 LLM canonical layer fires zero calls. The deterministic placeholder is sufficient for:

- Phase 7 joint-gate cohesion check (placeholder is machine-readable; cohesion can be evaluated against placeholder tokens)
- Engine-internal telemetry (placeholder is stored; LLM canonical is null; telemetry schema must accept null)
- Archive analysis (placeholder is fully adequate for sidecar queries)

**What the short-circuit does NOT disable:** the `faction_label_placeholder` algorithm in PM-2 § 3.4 still fires at Phase 4 archive-insertion time regardless of flag value. The placeholder is always produced; only the LLM canonical layer is gated by the flag.

**Phase 7 joint-gate note:** if Phase 7 cohesion check is designed to require `faction_label_canonical` (LLM-produced), and Reincarnated v1 runs `faction_visibility = invisible` (short-circuiting canonical), Phase 7 must accept placeholder for cohesion evaluation. This is a Phase 7 design constraint that surfaces from the short-circuit policy. Flag for gandalf / gamora awareness at Phase 7 design-spec time.

**Cost implication of short-circuit for Reincarnated v1:** PM-2 LLM calls per season = 0. SC-3 baseline is the total Phase 5 cost. The $0.015–$0.025 PM-2 increment only applies when `faction_visibility = visible` OR monster-contrast is enabled.

---

## 4. Cross-Faction Diversity Check + Regeneration Policy

**Disposition: CONFIRM cross-faction diversity check is architecturally correct; AMEND regeneration policy.**

### The check

PM-2 § 5.1 specifies: post-generation cosine similarity check on faction_name + faction_identity_narrative across season's 3-5 emergent factions; threshold cosine > 0.85 flagged. This is consistent with SC-3 Recommendation 3 (same 0.85 threshold for cross-character similarity; per SC-3 § Recommendation 3).

The check is one embedding call per faction narrative (~3-5 embedding calls) + pairwise cosine matrix computation. At 3-5 factions: 5×5 = 25 comparisons maximum. Trivially cheap. Total cost: <$0.005. Confirmed within envelope.

**Implementation note:** embedding calls are NOT the same as generation calls. If star-lord's infrastructure uses the Anthropic embedding API, these are a separate call type (not currently tracked in `TrackedLLMClient` per code inspection — it handles `messages.create` calls only). Dispatch 3B should include embedding call tracking or use a lightweight cosine approach (e.g., sentence-transformers locally) to avoid untracked Anthropic API calls. Star-lord flags this as a Dispatch 3B implementation detail, not a gate.

### Regeneration policy (AMENDMENT to PM-2 § 5.1)

PM-2 § 5.1 states "cosine > 0.85 flagged for regeneration" without specifying the retry policy. Star-lord fills this gap:

**PM-2 regeneration policy:**

1. If cosine similarity check flags a faction pair (similarity > 0.85): fire one regeneration call for the LOWER-QUALITY faction in the pair (determined by: whichever faction has weaker substrate-grounded provenance per faction_label_placeholder alignment). Maximum **1 regeneration per faction per season** (caps worst-case cost at 1× overhead per faction = 2× per-faction LLM calls at maximum).

2. If regeneration produces a replacement faction_name that still collides with the original collision partner (cosine > 0.85 after regeneration): **accept the regeneration output anyway** (do not retry further). Log the collision flag to telemetry. This is the 3-attempt ceiling applied at the faction-cluster level: original call = attempt 1, regeneration = attempt 2, second regeneration is NOT fired. The collision is noted in telemetry for sidecar analysis; it does not block season emission.

3. If PM-2 generates labels via a model that has consistently high cross-faction similarity (caught in sidecar analysis), this is a signal to increase THEMATIC_REGISTRY diversity (gandalf seam), not to add more retry depth.

**Rationale:** the existing `_call_with_retry()` in `client.py` handles API-level failures (RateLimitError, APIConnectionError, 5xx) with 3-attempt exponential backoff. That retry logic is independent of semantic quality retries. The PM-2 semantic-quality retry (cosine similarity) is distinct from the API retry — it fires at the orchestration layer above `complete_json()`, not inside the client. Dispatch 3B must implement this as application-level retry logic, not as a modification to `_call_with_retry()`. The boundary is correct per Discipline #5 (blocking vs downstream triage).

**Cost worst case under this policy:** 5 clusters × 2 calls (1 original + 1 regeneration maximum) = 10 calls × $0.005 = $0.05. This is the upper bound (all 5 factions trigger regeneration). Expected cost (typical: 0-1 regenerations per season) = $0.015–$0.025 + $0–$0.005 = $0.015–$0.03.

---

## 5. Latency + Concurrency Disposition

**Disposition: CONFIRM parallel firing is architecturally correct; name the two-wave pattern.**

### Phase 5 total call count at D-Hybrid + D-Separate

- PM-2 D-Separate cluster calls: 3-5 (wave A)
- Per-kit Pattern B calls (Option α Note 4): SC-3 estimates 16-40+ for identity generation (character_name + core_identity_narrative per SC-3 Recommendation 1); additional per-skill + per-gear-slot calls at volume for the ~2,100 total (wave B)
- Cross-faction diversity check embeddings: 3-5 (fires after wave A; trivially cheap; same latency as wave B if overlapped)

### Latency model

**Wave A (PM-2 cluster calls, parallel):** 3-5 calls at ~2-4 seconds per call (typical Anthropic API latency for ~1K token context + 150 token output) = **2-4 seconds wall-clock** (calls fire in parallel; limited by slowest cluster call).

**Wave B (per-kit calls, parallel):** SC-3's ~16-40 identity calls at ~2-4 seconds per call, parallel = **2-4 seconds wall-clock** for the identity generation subset. Volume calls (skill naming, gear descriptors) at ~2,100 total can be parallelized in batches; at 10 concurrent requests × 210 batches × 2-4 sec = **7-14 minutes** for full volume generation at aggressive concurrency. At more conservative batching (5 concurrent), 20-28 minutes.

**Wave A dependency:** Wave B per-kit identity calls that include faction context must wait for Wave A completion. Wave B skill-naming and gear-descriptor calls (which do NOT need faction context) can fire in parallel with Wave A.

**Revised pipeline:**
```
T=0:   Wave A fires (faction-label calls; 3-5 parallel)
T=0:   Volume calls (skill naming / gear descriptors; no faction dependency; batch-parallel)
T=2-4s: Wave A completes → faction_label_canonical available
T=4-8s: Per-kit identity calls (Wave B-identity; 16-40; parallel; receive faction context)
T=?:   Volume calls still running (7-28 min range)
T=?+4s: Per-kit identity calls complete
```

The faction-label step adds ~4-8 seconds of serialization to the Phase 5 pipeline (2-4 sec Wave A + 2-4 sec Wave B-identity). This is negligible relative to the total volume call latency (7-28 minutes). No latency concern for the Wave 5 season-generation budget.

**Anthropic API concurrency note:** the existing `LLMClient._call_with_retry()` is synchronous (single-threaded blocking calls per invocation). At ~2,100 calls, achieving the parallel batching described above requires either threading, asyncio, or a process pool at the orchestration layer. Dispatch 3B must specify the concurrency strategy. Star-lord does not block on this for the math note consultation, but notes it as a Dispatch 3B implementation scope item. The current infrastructure does not have built-in concurrent dispatch — it was designed for sequential generation. Phase 5 at ~2,100 calls at 2-4 sec each = 70-140 minutes sequential, which is likely unacceptable. Dispatch 3B must include the concurrency pattern.

---

## 6. Court-of-Forms Future Scope — Cycle 15+ LLM Architecture Note

**Disposition: ADVISORY — no Cycle 14 gate; flag for Cycle 15+ Dispatch authoring.**

PM-2 § 7.1 Q6 and Math Note 5 raise: cross-season persistence of faction labels as canonical-archetype-shapes at Court-of-Forms scope. Star-lord's scaling note:

### What PM-2 establishes that Court-of-Forms inherits

- `faction_label_canonical` (LLM-produced string; stored in telemetry DB per season)
- `faction_identity_narrative` (LLM-produced string; stored per season)
- `faction_thematic_tags` (list; stored per season)
- `faction_label_placeholder` (deterministic string; always stored; stable)

These are written to the telemetry DB at Phase 5 emission time (Discipline #8 — schema validation at write boundary required; MIGRATION.md needed). The placeholder is reproducible given same PM-1 inputs; the canonical is LLM-produced (non-deterministic; cache-keyed on prompt content).

### Court-of-Forms LLM call additions (advisory estimate)

At Cycle 15+, if Court-of-Forms requires cross-season faction-name CONTINUITY verification (same canonical-archetype-shape across two seasons should produce consistent `faction_label_canonical` or an explicit reincarnation-variant), two patterns are possible:

**Pattern X — Cache-first continuity:** PM-2 faction-label calls at Phase 5 cache-key on `(faction_label_placeholder, THEMATIC_REGISTRY_hash)`. If a prior season produced a faction with the same placeholder, the cache hit returns the prior season's canonical label — continuity by cache design. No additional calls needed. This leverages the existing `DiskCache` infrastructure. **Star-lord recommendation for Court-of-Forms v1.**

**Pattern Y — Explicit continuity judge call:** At Court-of-Forms initialization, a new LLM call per persisted canonical-archetype-shape verifies label consistency across seasons and generates a "spirit reincarnation" narrative. 1 call per persisted faction × N persisted factions per season × S seasons = call count grows as O(F × S). At 3-5 factions × 5 seasons = 15-25 additional calls per Court-of-Forms initialization. Tractable but requires explicit scope authorization at Cycle 15+.

**Star-lord scaling assessment:** the current infrastructure (TrackedLLMClient + DiskCache + TelemetryRecorder) scales to Pattern X with zero changes — cache keying handles cross-season continuity implicitly. Pattern Y requires orchestration-layer additions (Court-of-Forms initialization pass; cross-season faction matching logic). Pattern X is the CORRECT first approach; Pattern Y is additive if design intent demands explicit reincarnation narrative generation.

**No Cycle 14 action required.** PM-2 should ensure `faction_label_placeholder` is stable and stored durably (it is, per § 3.4 — reproducible algorithm outputs). The cross-season continuity mechanism follows from cache-keying on placeholder content.

---

## 7. Architectural Surprises

### Surprise 1 — Sequencing dependency is non-obvious but load-bearing

The PM-2 math note presents PM-2 as potentially independent of Option α Note 4's per-kit calls (D-Separate fires per cluster; per-kit calls fire per kit; "independent" dimensions per § 12.2). But if per-kit calls are to receive faction context (enabling Phase 7 joint-gate cohesion criterion: "does kit identity cohere with parent faction label?"), the calls are NOT independent — PM-2 calls must precede per-kit identity calls. This was NOT stated explicitly in the PM-2 math note; it emerges from composing PM-2 § 6 (Phase 7 joint-gate cohesion criterion requires faction-kit alignment) with the question of when faction context is available.

**Implication for Dispatch 3B:** the implementation spec must explicitly state the two-wave pattern (PM-2 cluster calls first; per-kit identity calls second; volume calls independent). If Dispatch 3B fires without this constraint, the Phase 7 cohesion criterion will be weakened (kit identities will lack faction context at generation time).

### Surprise 2 — Concurrency infrastructure is not yet built

The existing `LLMClient._call_with_retry()` is synchronous. At ~2,100 total Phase 5 calls, sequential execution is 70-140 minutes, which is likely unacceptable for Wave 5 generation latency. This concurrency gap is entirely outside PM-2's math scope but must be in Dispatch 3B's implementation scope. Star-lord flags it now so KR can include it in the Dispatch 3B spec rather than discovering it mid-implementation.

### Surprise 3 — Embedding calls for cross-faction diversity check are untracked

The existing `TrackedLLMClient` wraps `messages.create` (generation calls) but not embedding API calls. If the cross-faction diversity check uses Anthropic's embedding API, those calls will be invisible to cost tracking. Alternative: use a local sentence-transformer model (e.g., `sentence-transformers` Python package) for the cosine similarity check — no API call, no cost, no tracking gap. Given the tiny input size (5 faction strings of 2-5 words + 1-2 sentence narratives), a local embedding model is fully adequate. Star-lord recommends local embedding for the diversity check; Anthropic API embedding for this use case is unnecessary complexity.

---

## 8. Summary Disposition Table

| Question | Disposition | Notes |
|---|---|---|
| Cost projection — D-Separate within SC-3 envelope | CONFIRM | Expected $0.015–$0.025/season; $0.05 worst-case with regeneration; $0.15–$0.25 gandalf ceiling confirmed conservative; all within envelope |
| LLM call architecture composition | CONFIRM with amendment | Two-wave sequencing required (faction calls first; per-kit identity calls second); NOT fully parallel; see § 2 |
| `faction_visibility = invisible` short-circuit | CONFIRM | Engine-flag-governed; zero PM-2 LLM calls for Reincarnated v1; placeholder always produced; Phase 7 joint-gate design must accept placeholder; see § 3 |
| Cross-faction diversity check + regeneration policy | CONFIRM + AMEND | 1 regeneration max per faction per season; no further retry after regeneration; collision logged to telemetry; see § 4 |
| Latency + concurrency | CONFIRM; flag concurrency gap | Wave A 2-4 sec; Wave B-identity 2-4 sec additional; volume calls dominate at 7-28 min; concurrency infrastructure not yet built (Dispatch 3B scope item); see § 5 |
| Court-of-Forms future scope | ADVISORY: Pattern X (cache-first) sufficient for v1 | Current infrastructure scales to Court-of-Forms via cache-keying; Pattern Y (explicit continuity judge) is Cycle 15+ additive scope if design intent demands; see § 6 |

---

## 9. Schema Migration Flag (Discipline #8)

PM-2's output introduces three new fields that must land in the export schema before Phase 5 implementation fires:

- `faction_label_placeholder` (str; deterministic; produced at Phase 4 archive-insertion time)
- `faction_label_canonical` (str | None; LLM-produced; null when `faction_visibility = invisible`)
- `faction_identity_narrative` (str | None; LLM-produced; null when short-circuited)
- `faction_thematic_tags` (list[str] | None; LLM-produced; null when short-circuited)

These fields should land in a new `ExportFactionCluster` model (or equivalent) in `schemas.py`. MIGRATION.md entry required. MIGRATION.md is star-lord's seam; entry will be authored at Dispatch 3B time per standard protocol. Flagging now so KR / Matt-gate ratification record captures this requirement explicitly.

---

## 10. Framing-Audit (Discipline #42 per gandalf OP § 4.1)

**Q1 — What load-bearing framing assumptions does this consultation depend on?**
1. PM-2 § 3.3 D-Hybrid + D-Separate is the recommended policy; this consultation answers LLM-infrastructure questions relative to that policy.
2. SC-3 Pattern B PRIMARY is the call architecture for per-kit AND per-cluster calls; both use `complete_json()` with structured output.
3. Faction-label calls fire at Phase 5 time (not earlier); deterministic placeholder fires at Phase 4 time.
4. Reincarnated v1 runs `faction_visibility = invisible`; PM-2 LLM canonical layer may be short-circuited.

**Q2 — What evidence could refute these assumptions?**
1. If PM-1 smoke test produces only 1 cluster (critically sparse season), PM-2 D-Separate fires 1 call (not 3-5). Cost projection holds at lower bound.
2. If Dispatch 3B architects per-kit calls as fully independent of faction context (by design choice), the two-wave sequencing is not required and the Surprise 1 finding does not bite. But Phase 7 cohesion criterion weakens.
3. If `faction_visibility = invisible` is reversed for Reincarnated v1 (e.g., Matt decision to surface faction labels in UI), the short-circuit policy inverts. Architecture supports this without code changes; flag value change only.

**Q3 — Is refinement warranted before executing?**
No. All refutation paths are downstream of this consultation (PM-1 smoke test, Dispatch 3B design call, Matt visibility decision). The consultation's findings are internally consistent and empirically grounded on the existing LLM infrastructure. PROCEED.

---

## 11. Sign-off

**Author:** star-lord
**Date:** 2026-05-27
**Status:** COMPLETE — Pattern-A response filed for KR integration into Matt-gate routing

**Anchor docs cited:**
- PM-2: `reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`
- SC-3: `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md`
- LLM infrastructure: `reincarnated-engine/src/reincarnated/llm/client.py` + `tracked_client.py`

**Disciplines applied:**
- #1 (math-before-code): cost projections computed from first principles against empirical token estimates and actual pricing in `tracked_client.py`
- #11 (empirical inspection): cost figures derived from the actual `_COST_PER_MILLION` table in production code; sequencing dependency identified from PM-2 § 6 composition, not assumed
- #18 (methodology-before-execution): framing-audit applied; consultation fires before Dispatch 3B implementation; methodology lock complete on PM-2 questions 1-6
- #42 (framing-audit): Q1/Q2/Q3 documented at § 10
- #46 (DB anti-materialization + stream): N/A direct to this consultation; flagged for Dispatch 3B — Phase 5 LLM output storage in telemetry DB will need to respect Discipline #46 at the write site

**Open items queued for Dispatch 3B (not gating this consultation):**
1. Concurrency strategy for ~2,100 Phase 5 calls (sequential = 70-140 min; async/threaded required)
2. `ExportFactionCluster` schema addition + MIGRATION.md entry (star-lord Dispatch 3B scope)
3. Two-wave sequencing explicit in Dispatch 3B spec (cluster calls → per-kit identity calls)
4. Embedding approach for cross-faction diversity check (recommend local sentence-transformers; no Anthropic API call needed)
5. Phase 7 joint-gate design must accept `faction_label_placeholder` when canonical is null (gamora / gandalf awareness item; not star-lord scope)
