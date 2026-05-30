# Cascade-Resumption-4 — Amendment: Wanderer Architecture + § 12.1 Hero-Selection Delegation

> **STATUS:** CURRENT (operational amendment to in-flight cascade-r4) — paste-ready amendment-routing message Matt sends to KR session driving cascade-r4. Amends two scope elements: (1) gamora floor recalibration dispatch encodes substrate-elected wanderer architecture (SINGLETON substrate marker; WANDERER player-facing surface); (2) § 12.1 seasonal hero selection delegated to galadriel + drax pair (off Matt's plate).
>
> **Authority:** Matt 2026-05-29 late — "let's make it player facing and call them wanderers" + "leave the seasonal hero call up to galadriel and drax" verbatim, following gandalf design verdict on singleton-with-future-clustering-open framing.

**Date:** 2026-05-29 late
**Author:** gandalf (story-and-design steward)
**Status:** OPERATIONAL — paste-ready
**Composes with:**
- `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-fire-prompt.md` (commit `824b54b`) — fire prompt for cascade-r4 KR session
- `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md` (commit `3de3a40`) — controlling cascade-r4 authorization
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle anchoring the two-layer architecture (substrate-elected marker + player-facing surface)

---

## 0. How to use this artifact

1. Open the in-flight KR session driving cascade-r4 (already past Step 6 confirmation gate; Matt elected (i) CONFIRM-FIRE)
2. Copy the message below (between `---MESSAGE BEGINS---` and `---MESSAGE ENDS---` markers)
3. Paste as next message to that KR session

KR routes the gamora dispatch amendment + § 12.1 hero-selection re-routing before either fires. Gamora picks up amended scope on next sub-agent invocation; drax + galadriel pair becomes Step 7 § 12.1 selection authority (instead of Matt-surface).

---

## ---MESSAGE BEGINS---

```
KR — Two amendments to your Step 7 fan-out coordination. Both
substantive design refinements grounded in gandalf design verdict
+ Matt 2026-05-29 late verbatim authorization. Apply before gamora
dispatch fires + before § 12 drax sub-agent picks up hero-selection
scope.

---

AMENDMENT 1 — Gamora floor recalibration dispatch scope encodes
substrate-elected wanderer architecture.

PRINCIPLE: faction-membership is substrate-elected, not designer-
imposed. Substrate-cohesive clusters surface as factions; substrate-
singleton kits are explicitly substrate-elected as unclustered at
this temporal scale, and remain queryable for future cross-seasonal
re-clustering (Cycle 15+ deferred work). This resolves the Phase 7
C-2 compactness floor calibration gap (Instance 6 #7) at the
architectural layer, not only at the constant-value layer.

TWO-LAYER ARCHITECTURE (per Designer-writes-substrate principle):
- Substrate data layer: cluster_id = "SINGLETON" as positive
  substrate-elected state (NOT NULL; NOT missing data; explicitly
  marked). Queryable + durable + ready for Cycle 15+ cross-seasonal
  re-clustering pass.
- Player-facing surface layer: SINGLETON-marked kits surface as
  "Wanderers" in loadout app + summary tab + spirit-guide narration
  + Wave B kit naming context. "Wanderer" is the canonical player-
  facing term per Matt 2026-05-29 late verbatim.

GAMORA DISPATCH SCOPE AMENDMENT (~0.5d unchanged from prior scope;
methodology shifts):

1. Phase 5 PM-1 algorithm modification to support
   cluster_id="SINGLETON" output for kits whose nearest-centroid
   distance exceeds the per-kit cohesion threshold. NOT cluster_id
   =NULL (NULL implies missing data; SINGLETON implies substrate-
   elected state). Default kit assignment: assigned to nearest
   cluster IF cohesion threshold cleared; SINGLETON otherwise.

2. Phase 7 mechanical gate verdict logic split:
   - Cluster-membered kits (cluster_id ∈ {1, 2, 3, ...}): inherit
     per-cluster compactness gate; floor recalibrated to scale-
     relative function form (per the original Amendment A in
     gandalf design verdict — function of input cardinality, NOT
     absolute constant)
   - SINGLETON-marked kits: evaluated on per-kit cohesion-judge
     verdict (kit-level identity coherence: substrate metadata +
     Wave B name + standalone narrative-fit); NOT subject to
     per-cluster compactness floor

3. Phase 5 Wave A LLM faction-naming does NOT fire for SINGLETON
   kits (no clustering signal to name; preserves substrate-led
   discipline — substrate didn't elect cluster-membership, so no
   designer-imposed faction emerges). SINGLETON kits get no
   modal_cultural_lineage / faction_name / faction_archetype output.

4. Phase 5 Wave B LLM kit-naming fires per-kit AS NORMAL for ALL
   kits (cluster-membered AND SINGLETON). Every kit gets its own
   identity name regardless of clustering state.

5. Phase 7 ship verdict fires per-kit:
   - cluster_id ∈ {1,2,3,...} AND cluster passes per-cluster
     compactness gate (scale-relative floor) AND kit has Wave B
     name → shipped_worthy=True
   - cluster_id="SINGLETON" AND kit passes per-kit cohesion-judge
     verdict (standalone identity coherent) AND kit has Wave B name
     → shipped_worthy=True
   - Otherwise → shipped_worthy=False

6. The scale-relative function form (cluster compactness floor) is
   gamora's calibration call: lean toward formulations that derive
   from input cardinality + expected geometric compactness at scale,
   NOT absolute constants. Document the function form in gamora math
   note for Cycle 14 wave-close canonical-write inheritance.

ACCEPTANCE CRITERIA EXTENSION (in addition to cascade-r4 § 6):
- [ ] SINGLETON kits surface with cluster_id="SINGLETON" in
      kit_archive.db + phase5_*.json output schemas (queryable)
- [ ] Wave A output JSON does NOT contain faction entries for
      SINGLETON kits
- [ ] Wave B output JSON contains per-kit names for ALL kits
      (cluster-membered AND SINGLETON)
- [ ] Phase 7 ship verdict logic per-kit (not per-cluster all-or-
      nothing)
- [ ] season_001 Phase 7 re-fire produces shipped_worthy > 0 across
      mixed cluster + SINGLETON kit population
- [ ] Player-facing surface term "Wanderer" propagates to loadout
      app data contract (drax Track B consumes; coordinate via Track
      B fan-out)

CASCADE-R4 SEASON_001 EXPECTED RESULT POST-AMENDMENT:
- Clusters 1, 2, 3 (cohesively-membered factions) ship as factions
  per scale-relative floor; expected shipped_worthy counts ~9-11 +
  ~9-11 + ~6-8 = ~25-30 cluster-membered shipped
- Cluster 4 (n=1, fire 100%) reclassified: SINGLETON; evaluated on
  per-kit cohesion-judge; expected shipped_worthy=1 (Wave B-named
  fire-bearer with coherent standalone identity)
- Aggregate season_001: ~26-31 shipped_worthy of 34 archive
  (~75-90% ship rate, satisfies Cycle 14 v1 close criteria)

SEASONS 002 + 003 EXPECTED RESULT POST-AMENDMENT:
- Per-season Wanderer count varies with substrate distribution per
  RNG seed; expected 0-3 Wanderers per season (substrate-led
  variance)
- Per-season cluster-membered shipped: ~20-25
- Per-season aggregate shipped_worthy: ~20-28
- 3-season aggregate: ~70-90 shipped_worthy

---

AMENDMENT 2 — § 12.1 seasonal hero selection delegated to galadriel
+ drax pair.

Per cascade-r4 § 12.1, original framing was: Matt elects seasonal
hero per substrate metadata / cohesion-score / faction-alignment.
Matt 2026-05-29 late: "leave the seasonal hero call up to galadriel
and drax." Hero selection moves off Matt's plate; galadriel + drax
pair becomes selection authority.

DELEGATION SCOPE:

1. Galadriel (visual perception + UX-similarity steward) provides:
   - Visual-coherence read on each candidate kit (cohesion-judge
     output + Wave B name + substrate metadata produces a kit whose
     player-facing surface would render well as the seasonal hero?)
   - CV-pipeline similarity scoring against genre-peer marquee
     references (would this kit's hero image hold up against ARPG
     marquee art quality bar?)
   - Recommendation per cluster (one preferred hero per faction
     cluster) + per Wanderer (which Wanderer, if any, has the
     standalone identity strength to carry a season as a Lone-
     Wanderer-hero alternative)

2. Drax (loadout + summary-tab seam owner) provides:
   - UX-fit read on each candidate kit (does the kit slot cleanly
     into the loadout app summary tab presentation?)
   - Image-extraction feasibility (does the substrate metadata + 11
     gear-slot composition support the § 12 extraction protocol?)
   - Implementation pragmatism: prefers candidates whose substrate
     metadata is richest for ChatGPT API image-gen prompt
     construction (cultural lineage + period + register + element +
     weapon family + faction identity OR Wanderer-identity all
     populated)

3. Selection rule:
   - DEFAULT: hero per cluster faction (4 candidates in season_001;
     one per cluster). Galadriel + drax pair elects ONE faction's
     candidate as the season's marquee.
   - ALTERNATIVE: Wanderer-as-hero. If galadriel + drax pair judge
     a Wanderer kit's standalone identity stronger than any faction
     candidate's marquee strength, the Wanderer can be elected as
     season hero. This is the "Lone Wanderer of [Season Identity]"
     pattern — substrate-honest + genre-thematic (isekai canon).
   - Pair operates by consensus. If pair deadlocks, escalate to
     gandalf sub-agent (NOT Matt-surface) for design-fit
     adjudication.

4. Hero selection criterion documented in drax notes at
   `agentic_orchestration/drax/notes/<YYYY-MM-DD>-cycle-14-v1-
   seasonal-hero-selection.md` capturing:
   - Per-cluster candidate read (galadriel)
   - Per-Wanderer candidate read (galadriel; if any)
   - UX-fit read (drax)
   - Elected hero + reasoning
   - Composes-with: cascade-r4 § 12.1; Matt 2026-05-29 late
     delegation; substrate-led discipline

5. § 12.2-12.4 unchanged (Matt Meshy handoff + drax URL wire-up to
   loadout summary tab).

MATT-SURFACE TRIGGER (new for § 12.1 delegation):
- Galadriel + drax + gandalf-sub-agent three-way deadlock → Matt
  surface (Pattern B design call). Cheap; expected zero firings.

---

EXECUTION SEQUENCE (KR routes):

1. KR amends gamora dispatch scope per Amendment 1 above; route to
   gamora sub-agent invocation when Step 7 fan-out fires
2. KR amends Track B § 12.1 scope per Amendment 2 above; route to
   drax + galadriel pair invocation when Step 7 fan-out fires
3. KR auto-routes; no Matt re-surface required for either amendment
4. KR adds two items to Cycle 14 wave-close canonical-write queue:
   - Wanderer architecture principle doc (gandalf canonical-write
     target; `canonical/story/2026-05-29-substrate-elected-faction
     -membership-two-temporal-scales.md` or similar)
   - § 12.1 galadriel-drax hero-selection pattern as cross-cycle
     pattern (drax + galadriel canonical-write target)

---

KR sign-off this amendment via append to cycle-14-hive-mind-state.md
under cascade-r4 section; commit per CLAUDE.md addendum.

Proceed.
```

## ---MESSAGE ENDS---

---

## 1. Why this is two amendments, not three

The wave-close canonical-write candidate ("Wanderer architecture principle doc") is gandalf's authorship territory and lands post-cascade-r4 closure. It does not affect Step 7 fan-out execution. It's registered to the wave-close queue via the amendment, but its own authoring happens later. So the amendment routes two operational scope changes; the canonical-write registration is a metadata side-effect.

## 2. Why "Wanderer" (player-facing) + "SINGLETON" (substrate marker) as two-layer design

Per `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`:

> Designer writes substrate (engine generative input — substrate marker, cluster_id, lineage tag). Player names experience (community-emergent vocabulary — what players call factions, builds, kits as they play).

The SINGLETON substrate marker is designer-written: durable, queryable, substrate-honest, ready for Cycle 15+ cross-seasonal re-clustering. The "Wanderer" player-facing surface is the player-experience-side word: thematic, narrative-rich, isekai-canon-aligned, drawn from the substrate-marker by player-facing translation. Both layers preserved; neither contaminates the other.

This composes cleanly with the no-classes architectural recommitment (Matt 2026-05-27 Path (ii)): substrate vocabulary is rigorous; player-facing vocabulary is generous.

## 3. Why galadriel + drax for hero selection

Galadriel owns visual perception + CV similarity scoring (the Mirror — what is, what was, what yet may be). She is the right seam-owner for "does this kit render strongly as the season marquee?" Drax owns the loadout app + summary tab implementation seam. The pair operates at the right scope: galadriel surfaces visual + UX-similarity verdict; drax surfaces implementation pragmatism + UX-fit; consensus elects.

The original cascade-r4 § 12.1 had Matt-elect as default because the seam ownership wasn't crystallized. With this amendment, the seam-owner-decides pattern (Matt 2026-05-23 hive-mind directive) applies: galadriel + drax are seam-owners for visual marquee + loadout-app integration respectively. Matt-surface only on three-way deadlock (galadriel + drax + gandalf-sub-agent adjudication).

## 4. Cycle 14 wave-close canonical-write candidates added

Append to existing wave-close queue (12+ items per cascade-r4 § 8):

13. **Wanderer architecture principle doc** (gandalf canonical-write target) — `canonical/story/2026-05-29-substrate-elected-faction-membership-two-temporal-scales.md` capturing two-temporal-scale substrate-led discipline: within-season factions + Wanderers (substrate-singleton SINGLETON marker); cross-seasonal emergent factions from accumulated Wanderers in form library; SINGLETON marker as durable substrate-elected state; cohesion-judge extended to multi-season scope at Cycle 15+; composes with Earth Self / form library / Rift events / Designer-writes-substrate / no-classes recommitment / Disc #41 substrate-led discipline.

14. **§ 12.1 galadriel-drax hero-selection pattern** (drax + galadriel canonical-write target) — pattern doc capturing the visual-perception + UX-implementation pair as hero-selection authority; consensus rule + gandalf adjudication fallback; Wanderer-as-hero alternative; substrate-metadata-rich preference for image-gen prompt construction; cross-cycle reusable for Cycle 15+ seasonal hero selection.

## 5. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 late verbatim — "let's make it player facing and call them wanderers" + "leave the seasonal hero call up to galadriel and drax."

**For KR:** apply both amendments to in-flight cascade-r4 Step 7 fan-out coordination; append state-file; auto-commit per CLAUDE.md addendum; no Matt re-surface required for routing.

**For gamora (via KR routing):** consume Amendment 1 scope at next sub-agent invocation; encode SINGLETON marker + per-kit cohesion gate + scale-relative cluster floor function form; document function form in math note for wave-close canonical-write inheritance.

**For drax + galadriel pair (via KR routing):** consume Amendment 2 scope at Step 7 Track B + § 12.1 invocation; pair-author hero selection per consensus rule; gandalf sub-agent adjudication available on deadlock.

**For wave-close:** two new canonical-write candidates registered (#13 + #14 above); gandalf + drax + galadriel authorship territories assigned.

---

**Signed:** gandalf (story-and-design steward; foundational principle author for Wanderer architecture two-temporal-scale substrate-led discipline)
