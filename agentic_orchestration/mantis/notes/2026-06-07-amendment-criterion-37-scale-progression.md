# Amendment Record — Criterion 3.7 STRETCH Scale Progression

**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward), relayed via Matt direct to mantis session 2
**Authority:** gandalf cross-cutting design authority on spike dispatch amendments
**Relay rationale:** Radagast offline; spinning a Radagast session purely to relay a Mac-authored dispatch amendment is overhead; Radagast drift-discipline § 6 does not fire (this is a gandalf-authored amendment to a Mac-authored dispatch); direct relay is cleanest
**Inheritance:** when Radagast comes online for findings review, inherits the amended scope from this record

---

## Amendment

### Original scope (criterion 3.7 per 2026-06-06-mantis-ue-architecture-validation-spike.md § 8)
- 100 stars at procedurally-generated 3D positions
- Procedural constellation lines + nebula volumetric
- 60fps PC target measurement

### Reason for amendment
Original 100-star spec predates Phase A empirical scale data:
- Phase A landed **570 primitives + 1,000 PROVISIONAL constellations** at /forge
- Drax Mode B Phase 2 scales to **~15,000 nodes** (1,000 constellations × ~15 primitive instances)
- 100-star test produces no signal about real production behavior at either scale

### Amended scope — three-tier scale progression

**Tier 1 (BASELINE — was original spec):**
- 100 stars + procedural constellation lines + nebula volumetric
- 60fps PC measurement
- Status: Tier 1 star data already generated (2026-06-07 Session 2)
- Continue if mid-build; complete as data point. Skip if not started → go directly to Tier 2.

**Tier 2 (PRODUCTION-MIN):**
- 1,000 stars matching /forge PROVISIONAL constellation count
- Full effects stack: procedural constellation lines + nebula volumetric
- Measure FPS at 60fps target on PC
- Mobile projection via UE Editor mobile preview if available

**Tier 3 (PRODUCTION-ASPIRATIONAL):**
- 15,000 stars matching drax Mode B Phase 2 target
- Full effects stack
- Measure FPS — expected: will NOT sustain 60fps without LOD
- Record actual FPS distribution
- Flag LOD architecture needed for UE port:
  - Per drax Mode B Phase 2 LOD spec: centroid dots at low zoom; reveal at higher zoom
  - Document what Niagara LOD configuration achieves this

### Deliverable per criterion
Report including:
- Tier 1 / 2 / 3 FPS measurements
- Niagara emitter config notes per tier
- LOD recommendations for production
- Projected mobile feasibility at each tier
- If Tier 3 reveals fundamental Niagara constraints → load-bearing data for WS2 UE port commission scoping

### Cost note
- Meshy API cost: $0 (no Meshy calls; cosmograph test is UE tooling only)
- LLM cost: spike dispatch states $0 LLM
- Time cost: ~3-5 hours interactive session (expanded from 1-2 hr)
- Budget impact on $17 remaining Meshy budget: NONE
- Total spike time: 8-15 hours across remaining criteria (up from 6-12 hr)

### Other criteria: unchanged
- 3.2, 3.4, 3.6: original spec, no amendment

---

## Radagast inheritance note
This amendment was authored mid-mantis-session-2 before Radagast came online. When Radagast reviews session 2 findings:
- Read this amendment record
- Criterion 3.7 scope = three tiers as above
- PC-seam design authority on cosmograph Niagara architecture (Tier 3 LOD recommendations) is within Radagast's scope
- Cross-cutting cosmograph framework decisions (does 15K node density change the cosmograph metaphor?) → consult Mac-gandalf per drift-discipline § 6.2

---

*End of amendment record.*
