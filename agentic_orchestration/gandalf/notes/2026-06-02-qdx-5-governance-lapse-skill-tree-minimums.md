# QDX-5 Governance Lapse — Skill Tree Minimums

**STATUS:** CURRENT (governance lapse record; for next engine gen workstream)
**Date:** 2026-06-02
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-02 verbatim observation: "we had a governance lapse in skill trees. We have many kits with only 1 or 2 chains (minimum is supposed to be 3-4, and kits with as few as only 5 skills (none passive)"
**Source:** QDX-5 fire output at `~/Games/reincarnated-engine/data/kit_space/kits/` (37 kits; event `kse_20260602_008`)

---

## 0. TL;DR

QDX-5 output empirically violates the chain count + skill count + cultural_tradition + period architectural commitments per canonical 43 (Wave 2 T4 algorithm) + canonical 44 (Wave 3 T4 algorithm). Specifically:

- **100% of 37 kits below canonical 3-chain minimum** (62% have 1 chain; 38% have 2 chains)
- **24% of kits have only 5 skills** (canonical guidance suggests ~8-12 active skills + passives per kit)
- **100% of kits have cultural_tradition=NA + period=NA** (substrate_trace fields not populated)

Root cause: QDX-5 used legacy ClassGenerator path (Option B) per Matt 2026-06-02 ratification; ClassGenerator was not updated to canonical 43/44 multi-T4 architecture nor to produce substrate-trace fields per Architecture B (substrate-BOUND).

Disposition: flag for next engine gen workstream; address before next kit_space expansion fire.

---

## 1. Empirical findings

### 1.1 Chain count distribution (37 kits)

```
chain_count = 1: 23 kits (62%)  ← BELOW MINIMUM
chain_count = 2: 14 kits (38%)  ← BELOW MINIMUM
chain_count = 3:  0 kits  ← canonical minimum (3-chain = 2 T4 + 1 supporting)
chain_count = 4:  0 kits  ← canonical preferred (4-chain = 3 T4 + 1 supporting)
```

**Per canonical 43 (Wave 2 T4 algorithm intent) § "variable 3-or-4 class chain architecture":** kits should have 3-chain OR 4-chain composition. QDX-5 produced 0 of either.

### 1.2 Skill count distribution (37 kits)

```
skills = 5: 9 kits (24%)   ← BELOW canonical guidance (8-12 active expected)
skills = 6: 14 kits (38%)
skills = 10: 1 kit
skills = 11: 11 kits (30%)
skills = 12: 2 kits
```

**Bimodal pattern observed:** kits with chain_count=1 cluster at skills=5-6; kits with chain_count=2 cluster at skills=10-12. Suggests ClassGenerator generates ~5-6 skills per chain; multi-chain kits would extrapolate to ~15-24 skills per canonical 43/44.

### 1.3 Sub-issue: substrate_trace fields not populated

```
cultural_tradition: NA on all 37 kits
period:             NA on all 37 kits
```

Per Architecture B (substrate-BOUND at Phase 2 per canonical 39), kits should carry cultural_tradition + period from substrate composition. QDX-5's ClassGenerator path did NOT populate these fields. This compounds the Wave B identity LLM context-richness issue:

- Wave B saw only `{primary_element, archetype_tag, generation_seed, energy_type, role_orientation, range_profile}` per kit
- Without cultural_tradition + period, Wave B fell back to substrate-thin generic templates
- This is the root cause of the 24.3% Wave B fallback rate jack-ryan flagged at QDX-6 PASS-with-INFO

### 1.4 Sub-issue: passive skill annotation

Matt verbatim: "as few as only 5 skills (none passive)"

Investigation needed: confirm whether QDX-5 skills include any with `role=passive` annotation. If all 5-skill kits are 100% active, that's a second governance lapse on the active/passive skill mix per canonical 40 (gear-balance-guide-architecture) discipline.

---

## 2. Composition with canonical commitments violated

| Canonical commitment | Status | Reason |
|---|---|---|
| `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` § "variable 3-or-4 class chain architecture" | **VIOLATED** | All 37 kits at 1-2 chains |
| `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` | **VIOLATED** | Multi-T4 scope dimension not exercised |
| `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § active/passive skill mix | **LIKELY VIOLATED** | Pending passive-skill audit |
| `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` Architecture B substrate-BOUND | **VIOLATED** | Substrate-trace fields NA |

---

## 3. Root cause analysis

**Primary cause:** QDX-5 used legacy ClassGenerator path (Option B per Matt 2026-06-02 ratification) instead of canonical 39 QD-engine workflow's substrate-bound generator (BcTargetSubspaceGenerator).

**Why this surfaced as governance lapse:**
- Option B was chosen as the operative path for element-axis distribution (round-robin canonical-7+1 per LOCK R)
- ClassGenerator is the LEGACY generator (predates canonical 43/44 multi-T4 architecture); was NOT updated to canonical 43/44 chain architecture
- ClassGenerator does NOT populate substrate_trace fields (cultural_tradition / period) per Architecture B
- The QDX chain wired WS1A.4-lite + skip flags + kit_space emit + Pareto + cohesion + Wave A/B identity + multi-T4 selection logic, but NOT chain-count discipline + substrate-trace population

**Why this was NOT caught earlier:**
- QDX-6 jack-ryan acceptance verification's 8 criteria included `t4_selection.is_active` check (caught 4-of-37 missing T4) and `ws1a4_flavor_rate > 0` and `distinct emergent identities`, but did NOT explicitly check chain_count ≥ 3 OR substrate_trace populated
- Discipline #57 (genre-aligned distribution) ratified at QDX-8 covers the distribution side but not chain architecture
- Chain-count + skill-count + substrate-trace governance was implicit canonical, not explicit Gate-2 criterion

---

## 4. Disposition for next engine gen workstream

### 4.1 Required engine work before next kit_space expansion fire

```
WORK ITEM 1 — Wire ClassGenerator (or successor) to canonical 43 + 44 chain architecture
  - Produce 3-chain kits (2 T4 + 1 supporting) OR 4-chain kits (3 T4 + 1 supporting)
  - Per-chain skill count target: ~5-7 skills (so 3-chain = ~15-21 skills total)
  - Composes with multi-T4 selection logic already wired at QDX-3

WORK ITEM 2 — Populate substrate_trace fields per Architecture B
  - cultural_tradition: drawn from substrate composition per Phase 2
  - period: drawn from substrate composition per Phase 2
  - Feeds Wave B identity LLM context richness (addresses 24.3% fallback rate
    via richer per-kit context)

WORK ITEM 3 — Active/passive skill mix per canonical 40 discipline
  - Audit current kit JSONs for `role=passive` skills
  - Enforce mix per canonical 40 architectural commitment
  - Compose with chain-count work item above

WORK ITEM 4 — Gate-2 criterion amendment
  - Add explicit chain_count ≥ 3 to Gate-2 acceptance criteria
  - Add explicit substrate_trace populated to Gate-2 acceptance criteria
  - Composes with jack-ryan Discipline ratification at next wave-close
```

### 4.2 Discipline candidate for next jack-ryan ratification

> **Implicit canonical commitments warrant explicit Gate-2 criteria:** when canonical docs commit to architectural minimums (chain_count, skill_count, substrate_trace population, active/passive mix), the corresponding Gate-2 acceptance criteria should explicitly check those minimums. Implicit canonical commitments without explicit Gate-2 enforcement create governance lapses where pipeline output technically passes Gate-2 while structurally violating canonical commitments.

Composes with #54 (integration-smoke-gate) + #57 (genre-aligned distribution NOW canonical design constraint) + #59 (substrate-coverage as binding quality constraint).

### 4.3 Empirical-evidence trigger for re-engagement

- Next engine gen workstream activation (post-Matt-strategic-direction selection)
- Engine code changes per Work Items 1-4 above
- Re-fire kit_space expansion with corrected pipeline
- jack-ryan Gate-2 against expanded criteria

---

## 5. Composition with curated top-5 artifact

Per `2026-06-02-qdx-5-top-5-character-curation.md`, top-5 picks SURFACE this governance lapse but ARE the best available from QDX-5 output. The curated kits all suffer from:
- 1-2 chain (vs canonical 3-4)
- 5-12 skills (vs canonical ~15-24 expected at 3-chain)
- NA cultural_tradition + period

This caveat is acknowledged in the top-5 artifact's per-kit detail sections. JSON-to-Unreal mock should proceed with current best-available; canonical-architecture-compliant kits await next engine gen workstream.

---

## 6. Sign-off

**Authored:** gandalf 2026-06-02 per Matt verbatim observation on QDX-5 governance lapse
**Composes with:** `2026-06-02-qdx-5-top-5-character-curation.md` + canonical 39 + canonical 43 + canonical 44 + canonical 40 + Discipline #57 + Discipline #59 (substrate-coverage as binding constraint; this lapse manifests substrate-thin-on-architecture-spec rather than substrate-thin-on-content)
**Routing:** flag at next gandalf engagement post-strategic-direction; informs engine work scope before next kit_space expansion fire

**End of governance lapse record.**
