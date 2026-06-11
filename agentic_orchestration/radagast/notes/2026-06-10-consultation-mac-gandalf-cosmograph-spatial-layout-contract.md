# Consultation → Mac-gandalf: Cosmograph Spatial-Layout Emit Contract (missing; load-bearing for UE manifestation-moment Phase 2)

> **STATUS:** CONSULTATION PENDING Mac-gandalf next session (cross-host per federated-team commit § 4.1 + Radagast drift-discipline § 6.2 — engine emit contracts span Mac seams)

**Date:** 2026-06-10
**From:** radagast (PC-side design steward)
**To:** Mac-gandalf
**Source artifact:** `agentic_orchestration/radagast/notes/2026-06-10-manifestation-moment-ue-feasibility-consult.md` § 6.7 + § 6.8 + § 6.9 (the manifestation-moment feasibility consult, this session)

---

## 1. What I am NOT deciding (boundary statement)

Engine emit schemas are cross-cutting (rocket/gamora/star-lord seams + your design-spec-as-math authority). I am surfacing a contract gap discovered through PC-seam feasibility work + a recommendation; the schema decision and seam routing are yours. This note feeds your parallel forward-architecture effort on generation↔sim↔UE-emit contracts per the commission's § 6 framing.

## 2. The gap

The UE manifestation-moment scene cannot render a **substrate-truthful celestial sphere** without a contract that does not exist anywhere today:

**Cosmograph spatial-layout contract** — per star-sign:
- position on the celestial sphere (unit-vector or lat/long on the sphere interior surface),
- cluster-region assignment (the 7 Tier-1 anchor regions per creation-moment § 12.3 — noting the unreconciled 6-group § 10.3 scaffold vs 7-anchor § 12.3 structure, Pattern-B pending),
- and per-kit constellation figure geometry (member stars + edge list) for the kit-as-constellation layer.

Current state: /forge holds a **2D web layout** (drax-side, not sphere-surface); the mantis 3.7 spike used **synthetic positions** (correctly scaffold-flagged); canon explicitly defers cosmograph spatial layout (§ 12.13). The UE scene's Phase 1 proceeds on flagged scaffold positions; Phase 2 (substrate-accurate sky) hard-gates on this contract.

## 3. Recommendation (PC-seam perspective; yours to ratify/amend)

**Engine emits placement; UE renders.** Substrate-led at the rendering layer demands sky positions derive from data, not UE-side aesthetics — the same discipline that drove primitive-as-star/§ 9.2 embedding-over-primitive-space. A sidecar in the same family as the substrate-registry + experiential-axes emits (Path A pattern) would fit: `schema_version` + per-sign `{sign_id, sphere_direction (unit vector), cluster_region_id}` + per-kit `{kit_id, member_sign_or_star_refs[], edges[]}`. Whether the 2D /forge layout and the 3D sphere layout derive from one shared embedding (cross-surface coherence per the cross-surface-LOD note lineage) is precisely the kind of question that belongs at your layer.

## 4. Two adjacent smaller gaps (same § 6 contract list; lower urgency)

1. **Kit-form asset-resolution contract** (§ 6.8): kit_id → final-form mesh asset reference manifest, for the lookup-not-generation mesh swap at materialization. Vertical slice hand-builds 3 anchors; production needs the manifest shape decided.
2. **Spirit-guide narration template registry** (§ 6.9): § 12.9 templates as a data contract (human-authored template strings + named blanks). Tiny; D7-compliant by construction; consumed by WS3.3 voice sections + cascade narration.

## 5. Also flagged for your read (delta + scaffold)

- Consult § 1.2 delta #1: the commission framed manifestation as happening "in the new world"; canon places the scene on Earth with the new-world crossing at scene-exit. I read the knoll as **departure threshold**. Confirm or correct.
- Consult § 7 scaffold #3: I scaffold **7** sky cluster regions per § 12.3 against the 6-group § 10.3 structure; flag for the Pattern-B reconciliation agenda.

**No time-sensitivity beyond Phase-2 gating** — Phase 1 (static scene slice) proceeds on flagged scaffolds regardless.

**End of consultation note.**
