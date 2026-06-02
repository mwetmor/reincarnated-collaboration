# QDX-5 Generator-Path Strategic Decision — Matt-touch warranted

**STATUS:** 🟡 PENDING Matt decision (Phase 3 routing GATED on this)
**Date:** 2026-06-02
**Author:** knight-rider (orchestrator)
**Authority:** Phase 1 + Phase 2 PASS empirically establish the QDX integration works; Phase 3 (QDX-5 full fire) gates on this decision per LOCK L 1st-BLOCK + escape clauses #1 / #7 / #9
**Companion docs:**
- `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md` § 2 Phase 3 status
- `agentic_orchestration/qa/findings/2026-06-02-qdx-phase-1-phase-2-gate-2.md` (jack-ryan Gate-2 unified review with QDX-4 supplement; commit `2352d54`)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 1 Phase 2 (canonical substrate-bound architecture)
- `canonical/story/2026-06-02-eaa-chain-wave-close-record.md` § EAA-5 v1 BLOCK forensic + EAA-5 v2 ClassGenerator workaround

---

## 0. TL;DR

QDX Phase 1 (3 integration workstreams) + Phase 2 (LOCK S smoke-gate) ALL PASS empirically. Phase 3 routing is CONDITIONAL YES pending **one architectural decision: which generator path drives QDX-5's full fire?**

Three options. jack-ryan recommends Option B. KR recommends Matt-touch because this is ADR-002 architectural-commitment-tier and the empirical EAA-5 v1 vs v2 history makes this a substrate-led discipline (#41) interpretation question that lives at gandalf+Matt level, not seam level.

**Action requested from Matt:** select Option A / B / C; OR direct a different path (e.g., defer QDX-5 pending elrond substrate enrichment; OR fire all 3 in parallel for comparison; OR pivot QDX-5 scope).

---

## 1. What Phase 1 + Phase 2 empirically established

| What | Verified |
|---|---|
| WS1A.4-lite integration into Phase 5 (QDX-1) | ✅ PASS — 10/10 tests + variety smoke (Wraith Binding / Void Strike / Soul Slip etc.); Q18 pool validated; ADDITIVE-ONLY |
| kit_space_emitter wired into QD-engine terminal (QDX-2) | ✅ PASS — 14/14 tests; both skip paths verified; FK linkage; ADDITIVE-ONLY (zero changes to existing public APIs) |
| Single-entry-point fire script orchestration (QDX-3) | ✅ PASS-with-INFO — 8-phase composition Phase 1→2→4→5(a/b/c)→Wave A→Wave B→7→8 verified end-to-end; smoke wall=0.3min cost=$0.025; FK linkage; Wave B non-template ("Brute of the Unmarked Ground") |
| QDX-4 LOCK S smoke (non-physical forced) | ✅ PASS-with-INFO — variety check 0.429; Q18 validated; FK linkage; Wave B non-template ("Null-Shadow, Unresolved Range"); cost $0.09 |
| jack-ryan Gate-2 unified Gate-2 review | ✅ PASS-with-INFO (commit `2352d54`); 0 BLOCKs accumulated |

**The integration works.** Phase 5 + WS1A.4-lite + Wave A/B identity LLM + kit_space emit all compose cleanly. The pipeline is ready for full fire.

---

## 2. What surfaced empirically during Phase 2

**Substrate-coverage signal (rocket forensic; jack-ryan ratified):**

- `BcTargetSubspaceGenerator` (the canonical 39 substrate-bound Phase 2 generator) produces ~98% physical kits from current substrate
- Root cause: `infer_element_from_name()` returns "physical" as residual fallback for canonical-weapon names lacking elemental keywords
- 500-kit sample produced **0 shadow kits**; QDX-4 had to synthesize stubs to fire non-physical
- **This is the SAME root cause that BLOCKed EAA-5 v1.** EAA-5 v2 worked around it via `ClassGenerator` + round-robin canonical element assignment.

**Implication for QDX-5 full fire:**

If QDX-5 fires `BcTargetSubspaceGenerator` (canonical 39 path) as-is, the empirical prediction is ~30-40 PHYSICAL kits — failing the Cycle 14 wave-5-equivalent quality goal Matt's chain-close goal requires.

---

## 3. The three options

### Option A — BcTargetSubspaceGenerator (canonical 39 substrate-bound) as-is

| Property | Value |
|---|---|
| **Architectural posture** | Canonical 39 § 1 Phase 2 substrate-bound; Discipline #41 substrate-led honored |
| **Empirical prediction** | ~30-40 kits, ~98% physical; 1-2 non-physical if substrate has any elemental-keyword matches |
| **Element diversity** | LOW (substrate-bound under current substrate state) |
| **Cycle 14 wave-5 quality goal** | NOT met — same insufficient-diversity issue Matt called out at EAA chain close |
| **Cost** | $5-30 (LOCK R bound; mostly wasted on a result that doesn't meet quality goal) |
| **Substrate enrichment dependency** | Implicit prerequisite to make this option viable |
| **Discipline #41 (substrate-led)** | ✅ Honored |

### Option B — ClassGenerator + round-robin canonical element assignment (EAA-5 v2 path)

| Property | Value |
|---|---|
| **Architectural posture** | NOT canonical 39 substrate-bound; canonical element selected first, substrate filled to fit |
| **Empirical prediction** | 30-40 kits, 8/8 element coverage (matches EAA-5 v2 element distribution) PLUS the QDX richness (Pareto + cohesion + Wave A/B + multi-T4) that EAA-5 v2 lacked |
| **Element diversity** | HIGH (forced via round-robin canonical-7+1) |
| **Cycle 14 wave-5 quality goal** | Likely MET — diversity + Pareto + cohesion + Wave A/B + multi-T4 + WS1A.4-lite (this is the actual goal Matt verbalized) |
| **Cost** | $5-30 |
| **Substrate enrichment dependency** | None — works against current substrate |
| **Discipline #41 (substrate-led)** | ⚠️ Partial — substrate determines fill (cultural-tradition + period + skill structure) but element-axis is forced via round-robin; departure from "substrate determines element selection" |
| **jack-ryan recommendation** | YES |

### Option C — BcTargetSubspaceGenerator + synthetic fallback at full scale

| Property | Value |
|---|---|
| **Architectural posture** | Canonical 39 substrate-bound + LOCK S synthetic-stub fallback applied at scale |
| **Empirical prediction** | 30-40 kits with element diversity via synthesis BUT `t4_selection=null` on all non-physical kits (synthetic stubs have no BC-axis contribution data; T4 algorithm Option F exhausted) |
| **Element diversity** | HIGH (via synthesis) |
| **Cycle 14 wave-5 quality goal** | PARTIALLY MET — diversity yes; multi-T4 NO on majority of kits |
| **Cost** | $5-30 |
| **Substrate enrichment dependency** | None — but t4_null is institutionalized at scale |
| **Discipline #41 (substrate-led)** | ❌ Departure — synthesis-on-demand violates substrate-led at generation layer |
| **jack-ryan assessment** | "Least clean"; institutionalizes QDX-4 marginal outcome at scale |

### Option D — Defer QDX-5 pending elrond substrate enrichment

| Property | Value |
|---|---|
| **Architectural posture** | Wait for elrond non-physical weapon substrate enrichment workstream |
| **Timeline** | Multi-day workstream (elrond would need to design + acquire + curate non-physical weapon substrate; gandalf canon support; design-spec-as-math handoff for element keyword library) |
| **Cycle 14 wave-5 quality goal** | Eventually MET (once substrate enriched); deferred |
| **Cost** | Higher (substrate enrichment workstream + delayed QDX-5 fire) |
| **Substrate-architecture purity** | Highest — canonical 39 substrate-bound under properly-covered substrate |
| **Matt empirical-truth-moment timing** | Delayed |

---

## 4. KR analysis + recommendation

### Why this is Matt-touch, not seam-level

This decision touches three canonical commitments simultaneously:
1. **Discipline #41** (substrate-led at generation layer) — Option B violates partially; Option C violates substantially
2. **Canonical 39 § 1 Phase 2** (substrate-bound at Phase 2) — Option B doesn't honor; Option C honors with synthesis
3. **Matt's chain-close verbalized goal** (Cycle 14 wave-5-equivalent richness) — Option A fails empirically; Option B meets

No seam-owner has authority to amend canonical commitments unilaterally. ADR-002 tier-1 architectural decisions are Matt's. The empirical EAA-5 v1 vs v2 history shows this is NOT a hypothetical concern — this exact tension surfaced and was navigated by ad-hoc seam-level workaround (ClassGenerator round-robin) without canonical re-ratification. Under QDX scope it deserves a real ratification call.

### KR soft-lean

**Option B + canonical re-ratification of "partial substrate-led under current substrate state" as INTERIM discipline pending elrond substrate enrichment as PARALLEL workstream.**

Reasoning:
- Empirically delivers Cycle 14 wave-5-equivalent quality goal Matt verbalized
- Bounded LLM cost ($5-30) for definitive Matt-feedback artifact
- Honors Discipline #41 at "substrate determines fill, canonical-7+1 determines element-axis coverage" interpretation (NOT "substrate determines element")
- Composes with future Option D (elrond substrate enrichment as PARALLEL workstream → future QDX-9+ fires use canonical-39-pure substrate-led path naturally)
- Matches jack-ryan independent recommendation

But **KR DOES NOT WANT TO DECIDE THIS WITHIN KR AUTHORITY** because:
- It implicitly amends Discipline #41 interpretation (KR has no canonical-amendment authority)
- It implicitly amends canonical 39 § 1 Phase 2 in practice (KR has no canonical-amendment authority)
- It's the chain-purpose-determining decision (cost of wrong path = wasted $5-30 + chain-close that doesn't meet Matt's goal)

---

## 5. Specific Matt-touch ask

Matt's choice from:

**(a) Option B — fire QDX-5 with ClassGenerator round-robin element assignment** (KR + jack-ryan soft-lean recommendation; bounded ratification of "partial substrate-led" interpretation)

**(b) Option A — fire QDX-5 with canonical 39 substrate-bound path as-is** (empirically predict ~98% physical; chain delivers what substrate currently supports; Matt explicitly accepts the diversity-vs-discipline trade-off)

**(c) Option D — defer QDX-5 pending elrond substrate enrichment** (route to elrond + gandalf for substrate-enrichment workstream; multi-day; chain pauses)

**(d) Some other direction** — e.g., fire all 3 in parallel for direct empirical comparison; OR amend QDX-5 scope; OR strategic pivot

**Also welcome:**
- Confirmation/amendment of KR's interpretation that this is genuinely Matt-touch (not seam-level)
- Any explicit canonical re-ratification language for the path chosen
- Direction on elrond substrate enrichment as parallel workstream (regardless of Option A/B/C/D for QDX-5)

---

## 6. State preservation

If Matt selects Option B + parallel elrond enrichment, the chain proceeds:
- QDX-5 dispatch authored with generator path explicitly named (Discipline #56 candidate compliance)
- QDX-5 fires under bounded cost ($5-30 LOCK R) + bounded kit count (30-40 LOCK R) + bounded wall-clock (multi-hour)
- elrond substrate enrichment workstream forks in parallel
- QDX-6 (Gate-2 acceptance verification) follows
- QDX-7 (drax MVP refresh) follows
- QDX-8 (wave-close) follows

All Phase 1 work-products preserved unchanged. EAA chain preserved as historical. Existing seasons preserved per Path α.

---

**End of QDX-5 generator-path strategic decision request.**
