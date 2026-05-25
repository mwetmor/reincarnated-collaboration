# gandalf — SO-1, SO-2, SO-4 Sign-Off Verdicts (Pattern A-light)

**Date:** 2026-05-25
**Author:** gandalf (story-and-design steward)
**Authority:** dispatch `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 10 Gate routing + composition policy v1 § 7.4 empirical-criterion-for-completion (Matt + gandalf sign-off on distribution report)
**Companion notes:**
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md` (LOAD-BEARING evidence)
- `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md` (SO-3 Pattern A-deep)
- `agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md` (composition policy § 7.4 verdict)

---

## 0. TL;DR

| Sign-off | elrond recommendation | gandalf verdict | Conditions |
|---|---|---|---|
| **SO-1** historical register at +5.0pp edge | ratify | **RATIFY** | accept substrate-led skew per Sketch D |
| **SO-2** PCFS 12/17 FAIL routing | accept Sidecar B / Stage 3.5 routing | **RATIFY-WITH-AMENDMENT** | accept routing + surface PCFS-vs-register-share tension as v1.1+ architectural-decision queue per elrond Finding 3 |
| **SO-4** 1,152 NULL-typed (37.9%) in v1_scope | ratify + Stage 4 priority signal | **RATIFY-WITH-AMENDMENT** | ratify substrate-led behavior + flag D1c-subtype-classifier extension to Tier-A NULL-subtype pool as PRECONDITION to clean Phase 2 form-generation (NEW finding from 50-row spot-check) |

All three are RATIFY-class verdicts. None requires re-engaging composition policy v1 architecture. SO-2 and SO-4 carry amendments that ROUTE to follow-on work without blocking Stage 3 completion.

The 50-row spot-check FAIL (separate doc) is a parallel signal that modifies the OPERATIONAL meaning of these ratifications: ratify the algorithmic posture, BUT acknowledge that the v1_scope material will need a Path-A remediation pass before Phase 2 form-generation fires against it. See companion 50-row spot-check note for details.

---

## 1. SO-1 — Historical register at +5.0pp edge

**Question (per Phase 3 distribution report § 9 + § 2.1):** historical register share landed at 57.5% (+5.0pp at the ±5pp gate edge). Per composition policy § 2.1 target band 50-55%. Two interpretations:
- Substrate-led acceptance (Sketch D) — ratify the +5.0pp at the spirit of substrate-led skew acceptance
- Tighter band interpretation — evict ~75 Tier-A historical rows to fall within strict 50-55%

**elrond posture:** ratify per Sketch D substrate-led skew acceptance (Phase 3 report § 9 item 1).

### gandalf verdict: **RATIFY**

**Reasoning anchored on canonical docs:**

1. **Per composition policy § 2.1, the historical target is "~50-55% (slight trim from substrate's 66.4%)."** The substrate's actual historical share is 66.4%; the target represents a TRIM, not a strict band. 57.5% is consistent with "slight trim" language — it represents a 9pp trim from substrate without being arbitrary.

2. **Per Sketch D (referenced in composition policy § 2.1 and authored at `v1-bc-target-intent-2026-05-24.md`), substrate-led skew is the spirit, not strict bands.** Sketch D's decision was to ACCEPT historical-european over-representation as a feature of the genre (medieval-fantasy-isekai), not a bug. Tightening to 50-55% strict would contradict Sketch D's intent.

3. **The +5.0pp delta is policy-trade-off-bounded, not algorithm-bounded.** Per elrond Phase 3 report § 5 Finding 3, lifting under-floor STR archetypes (GC-1 + GC-4) would require historical share to EXCEED +5.0pp. The 57.5% landing represents the sampler honoring the cap. If we tighten the cap to 50%, those failing archetypes get worse, not better. Net design-coherence cost of tightening exceeds net benefit.

4. **Player-experience consequence:** at 57.5% historical share, the resulting v1 form-library will feel medieval-fantasy-leaning with strong historical-anchored named-bearer presence (Arthur, Roland, Cleopatra, Karna, etc.) — matches the Sketch D + Fate-genre alignment per `fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`. A 50% trim would dilute this signature toward generic Pan-Fantasy. The +5pp at edge IS the genre lean.

5. **Diablo / Path of Exile / Last Epoch comparison:** Diablo III + IV have player-facing universes that are ~70-80% historical-european medieval-Gothic. Path of Exile sits ~60-70% historical / 30-40% explicit fantasy. Reincarnated v1 at 57.5% historical is genre-conservative even compared to the comparator class. There is no over-representation risk at this share for genre-readability.

**No amendment required.** Composition policy § 2.1 language already covers "slight trim from substrate's 66.4%"; 57.5% is within spirit.

---

## 2. SO-2 — PCFS 12/17 FAIL (70.6%); 5 archetypes under-floor

**Question (per Phase 3 distribution report § 9 + § 3.1):** PCFS archetype-gate result is 70.6% (12 of 17 archetypes at or above floor), below the implicit 85% threshold. The 5 failing archetypes are policy/substrate-trade-off-bounded per elrond § 5 of sampling rationale. Two interpretations:
- Accept routing to Sidecar B / Stage 3.5 (current Phase 2 posture per autonomous in-scope decision) — surface PCFS-vs-register-share tension as v1.1+ architectural-decision queue
- Re-engage composition policy § 2.1 register-share caps for STR-heavy archetype floor satisfaction

**elrond posture:** accept routing per Finding 3 in § 7 of report (Phase 3 report § 9 item 2).

### gandalf verdict: **RATIFY-WITH-AMENDMENT**

**Reasoning anchored on canonical docs + design discipline:**

1. **Substrate-led discipline says: the substrate's structural bias toward STR-historical at Tier-A is binding.** Per Discipline #11 substrate-led principle + Pattern 4-5-6 retirement spirit, we sample against the substrate's actual composition. The PCFS-vs-register-share tension is a real architectural finding, not a sampling artifact. The 5 failing archetypes (GC-1 through GC-5) are NOT local-optima that LP could improve — they are genuine policy-trade-off conflicts.

2. **The under-floor archetypes are all addressable via existing routing per composition policy § 4.1:**
   - GC-1 `(ranged, low, STR)` + GC-4 `(melee, high, STR)` → Sidecar B fantasy/cross-cultural STR enrichment (composition policy § 4.1 cell-level routing already covers this implicitly via "thin-cell-enrichment targets")
   - GC-2 `(mid, medium, DEX)` + GC-5 `(mid, high, DEX)` → Sidecar B DEX-mid enrichment (compound priority signal — both share the small-pool diagnosis)
   - GC-3 `(mid, low, DEX)` → Sidecar B fantasy + classical/medieval DEX-mid-low enrichment (avoids the military_modern 80% trim)
   - GC-6 `(ranged, low, WIS)` → already routed to Sidecar B WIS-broad enrichment per composition policy § 4.1 (substrate-bounded; excluded from PCFS gate)

3. **The 70.6% PCFS result is NOT a v1-ship blocker** — Sidecar B is in-flight per composition policy § 1.6, and Stage 3.5 gap-fills are in-scope for Wave 6. The 5 failing archetypes will be addressed in the natural sequence of Cycle 10 work, not blocked.

4. **Design-coherence reasoning:** the archetypes failing PCFS are NOT genre-critical to a v1 ship at minimum. The Pan-Fantasy + medieval-isekai genre signature lives in the 12 PASSING archetypes (`(melee, medium, STR)` = barbarian; `(melee, medium, WIS)` = monk-archetype; `(ranged, medium, DEX)` = ranger/archer; etc.). The failing archetypes are second-tier silhouettes that will round out diversity but do not anchor genre identity. The sequencing — ship v1 form-library on PASSING archetypes + lift failing archetypes via Sidecar B in parallel — is genre-coherent.

5. **Path-of-Exile design philosophy comparison:** GGG's PoE design talks frequently invoke "ship the strong silhouettes first; round out the secondary silhouettes after live feedback." Reincarnated v1 with 12/17 archetypes at-or-above floor is exactly that posture. Diablo IV's pre-launch postmortem (cited in `canonical/story/gandalf-design-lineage.md` predecessor work) reinforces: thin archetypes that ship at 60-70% saturation get audience-testing signal that informs Sidecar B priorities. Shipping FULLY saturated risks over-investing in archetypes that don't earn it.

**Amendment to ratification:**

- **Surface PCFS-vs-register-share tension as v1.1+ architectural-decision queue item** per elrond Finding 3 (already proposed in elrond's Phase 3 report). This is a genuine architectural decision deferred — composition policy § 2.1 register caps and Sketch B PCFS floors are in tension when substrate is structurally biased. Future iterations (v1.1+) can re-balance one against the other with empirical evidence from v1 play data.

- **Specifically queue:** "PCFS-archetype-gate ≥85% AND register-share caps as currently specified are jointly unsatisfiable given current substrate composition. Future architectural decision: (a) accept substrate-led PCFS skew + retire ≥85% gate, OR (b) tighten register caps to free more Tier-A pool, OR (c) rebalance target_total downward to ~2,700 per elrond's Finding 3 § 5."

- **No re-engagement of composition policy v1 architecture in Cycle 10.** The decision deferred to v1.1+ post-Sidecar-B + post-Stage-4-tagging when the substrate composition and final v1_scope distribution will both have shifted.

**Critical addendum from the 50-row spot-check:** the PCFS gate operates on `proxy_attribute_class + proxy_range_class + proxy_tempo_class` — these axes are NULL on 37.9% of v1_scope rows (Finding 4). The PCFS gate is therefore evaluating only the 1,890 typed rows. The 50-row spot-check revealed that a substantial fraction of the NULL-typed Tier-A rows are D1c-equivalent scope-creep (helmet, riding boot, magazine, sallet, etc.) that should not contribute to floor-satisfaction at all. If those rows were correctly D1c-excluded, the typed-pool fraction would rise AND the PCFS picture would be cleaner. This compounds with SO-4 amendment below.

---

## 3. SO-4 — 1,152 NULL-typed rows in v1_scope (37.9%)

**Question (per Phase 3 distribution report § 9 + § 7 Finding 4):** v1_scope contains 1,890 typed rows (62.1%) + 1,152 NULL-typed rows (37.9%). Sub-phase A (Tier A preferred-include) admitted 940 untyped Tier-A rows without typed-filtering — Tier-protection trumps typed-filtering at the preferred-include phase. Two interpretations:
- Ratify substrate-led Phase 2 behavior (tier-protection is primary signal; Stage 4 mechanical-tagging is the unblock) — flag Stage 4 as priority
- Re-run Sub-phase A with typed-filter to limit NULL-typed admission

**elrond posture:** ratify + flag Stage 4 priority (Phase 3 report § 9 item 4).

### gandalf verdict: **RATIFY-WITH-AMENDMENT**

**Reasoning anchored on canonical docs + design-coherence:**

1. **Substrate-led discipline says: tier-protection is the primary signal.** Per composition policy § 2.5 Tier protection rules + Discipline #11 substrate-led principle, Tier-S/A are protected against eviction by lower-priority signals. Typed-status is NOT a tier-protection criterion in composition policy § 2.5. Imposing typed-filtering at Sub-phase A would VIOLATE tier-protection — it would re-rank Tier-A by an axis (typed-status) that the policy doesn't prioritize.

2. **Per Architecture B Option β + Option C (composition policy § 3.2 + § 3.3), NULL-typed rows CAN be bound to forms.** Option β (caster cells, attribute-level match) and Option C (cross-attribute hybrid) both accept substrate rows that lack full 5-tuple typing. The 1,152 NULL-typed rows are valid Option β / Option C substrate seeds at Phase 2 form-generation.

3. **Stage 4 mechanical-tagging IS the right unblock per composition policy § 1.4 + § 9 + 02-roadmap sequencing.** Stage 4 fires AFTER Stage 3 v1_scope materialization per the dispatch sequence. It re-touches the NULL-typed pool with accurate mechanical-tagging and lifts the typed-rate. This is the architecturally-correct cycle.

**Amendment to ratification — NEW finding from the 50-row spot-check:**

The 50-row spot-check revealed that the 940 NULL-typed Tier-A rows admitted to v1_scope include substantial D1c-equivalent scope-creep that escaped the D1c gate because of NULL `weapon_kind_classified_subtype`. Specifically, in my 10-row Tier-A-historical-european sample, 8 of 10 rows were D1c-equivalent (helmet, sallet, cuisse, riding boot, display plinth, etc.). Naive extrapolation suggests ~500-700 of the 940 NULL-typed Tier-A rows are non-weapon items that should have been D1c-excluded.

**The amendment:** before Stage 4 fires AND before Phase 2 form-generation fires against v1_scope, run a **Phase 0c subtype-classifier extension pass** over the 940 NULL-typed Tier-A pool. This is a tier-respecting + composition-policy-respecting remediation:

- D1c subtype-classifier already exists for Tier-S (Phase 0a)
- Extend it to operate on Tier-A NULL-subtype rows
- Add D1c-classified rows to the D1c-excluded set
- Re-materialize v1_scope (or apply an UPDATE eviction pass)

This does NOT violate substrate-led discipline because it operates within the existing D1c gate framework — it just closes the NULL-subtype escape pathway. It does NOT violate tier-protection because D1c exclusion is composition-policy-explicit (composition policy § 1.1 + § 2.5) and Tier-A protection is NOT tier-protection-against-D1c.

**Cost estimate:** elrond ~half-day to run Phase 0c-extension classifier (940 rows; similar pipeline to Phase 0a) + UPDATE v1_scope=0 on classified-out rows + smoke + gandalf re-spot-check.

**Sequencing relative to Wave 6:**
- Wave 6 dispatch (Stage 3.5 gap-fill) does NOT depend on Phase 0c-extension being clean — gap-fill is engine-authored new rows
- Wave 7 (Stage 4 mechanical-tagging) does depend on clean v1_scope — Stage 4 will mechanical-tag the 940 untyped rows, and tagging a "riding boot" with proxy_range_class is wasted work
- Therefore: Phase 0c-extension should land between Wave 6 fire and Wave 7 fire, OR before Wave 7 fires regardless of Wave 6 timing

**Recommendation:** route Phase 0c-extension to knight-rider as a Wave 5.5 add-on (between Wave 5 close and Wave 6 fire). Knight-rider has authority to amend Wave 7 scope to require clean v1_scope as precondition.

---

## 4. Cross-cutting observation — three sign-offs compose into one architectural picture

SO-1, SO-2, SO-4 are all RATIFY-class. But composed together, they tell a coherent design story:

- SO-1 ratifies substrate-led acceptance of the historical share
- SO-2 ratifies routing of policy-trade-off-bounded archetypes to Sidecar B / Stage 3.5
- SO-4 ratifies tier-protection over typed-filtering + flags D1c-subtype-classifier extension

The three together say: **the Phase 2 sampler executed the composition policy correctly given the gate definitions. The gate definitions themselves are under-specified at the NULL-typed Tier-A boundary, and the substrate composition is structurally tensioned vs the policy's PCFS gate.** Both are addressable WITHOUT re-engaging the composition policy v1 architecture — they route to follow-on work in Cycle 10's natural Wave sequence.

The 50-row spot-check FAIL (separate doc) is the empirical signal that the gate-definition gap is real and load-bearing. The Path-A remediation in the spot-check note + the Phase 0c-extension proposal in this SO-4 amendment + the SO-3 path verdict (separate doc) are the engineering responses.

---

## 5. Recommendation routing for knight-rider integration

- **SO-1 RATIFY** — no follow-on; close as ratified per gandalf + Matt sign-off
- **SO-2 RATIFY-WITH-AMENDMENT** — close as ratified + add v1.1+ queue item: "PCFS-vs-register-share architectural decision" per elrond Finding 3
- **SO-4 RATIFY-WITH-AMENDMENT** — close as ratified + route Phase 0c-extension to knight-rider for Wave 5.5 add-on between Wave 5 close and Wave 6 fire (or before Wave 7 if Wave 6 fires first)

The Phase 0c-extension proposal is in autonomous-scope per Cycle 10 scope-doc § 1 (cycle-internal sequencing decision) but warrants Matt-touch because it's a NEW work-unit not in the original cycle plan. knight-rider can fire OR route to Matt per his choice.

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-25
**Verdict status:**
- SO-1: RATIFY (no amendment)
- SO-2: RATIFY-WITH-AMENDMENT (v1.1+ queue item; no Cycle 10 work)
- SO-4: RATIFY-WITH-AMENDMENT (Wave 5.5 Phase 0c-extension proposal)

**Empirical criterion for next-state landing:**
- SO-1: per Matt sign-off (close)
- SO-2: per Matt sign-off + v1.1+ queue capture in `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` (gandalf to update if Matt ratifies)
- SO-4: per Matt sign-off + knight-rider authoring of Phase 0c-extension dispatch (or escalation to Matt if knight-rider chooses)

**Related notes:**
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md` (50-row spot-check FAIL — empirical evidence for SO-4 amendment)
- `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md` (SO-3 Pattern A-deep verdict — load-bearing on Wave 6 scope)
- `agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md` (composition policy § 7.4 empirical criterion sign-off)
