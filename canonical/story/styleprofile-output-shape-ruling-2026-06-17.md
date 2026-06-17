# StyleProfile Output-Shape Ruling — §7.6 of the Gear-Spec Deferred-Architecture Record

> **STATUS:** CURRENT (load-bearing as of 2026-06-17) — see `canonical/00-ground-state.md` § 1. Resolves the **§7.6 gandalf design-seam decision** of `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` ("rule on the StyleProfile output shape once the slice verifies the UV reality"). The ruling fires NOW because the §4 empirical resumption gate **just resolved** (galadriel slice-verification, both predictions YES). This is the gated commitment whose gate cleared — not a premature one.

**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward; design seam per the architecture record §7.6)
**Gate that resolved:** §4 resumption gate — CLEARED on the geometry-verification half by `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/slice-verification-2026-06-17.md` (galadriel; predictions **#2 UV-region separability** + **#3 accent-rig sockets** both **VERIFIED YES**, 2026-06-17, commit `8da65d1`).
**Companions:**
- `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — the what-locked / what-deferred record this resolves a clause of.
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/slice-verification-2026-06-17.md` — galadriel's empirical answer (the substrate that forced this shape).
- `matt_notes_handoff_docs/armor-weapon-pipeline-recommendation.md` § 4–5 — the StyleProfile schema + parametric-restyle layer this rules on.
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 6–7 — the consumer (element-flavor palette/finish/emission + the glowing-aura apex land in this StyleProfile).

---

## 0. The ruling in one line

The StyleProfile `palette` carries a **per-region palette array** that **gracefully degrades to a single whole-tint entry** when the bound mesh exposes no per-region mask. One schema, two fill-densities, keyed by the lane the bound mesh belongs to. This is the **additive-nullable pattern** (`cd7cba3`, cited architecture record § 3.1) applied at the output.

## 1. Why this shape — the substrate forced it (not a guess)

galadriel cracked the slice. Two substrate shapes, **empirically verified**, not assumed:

| Lane | Source packs (verified) | Recolor granularity | Mask present? |
|---|---|---|---|
| **Per-slot lane** | Modular Fantasy Heroes | per-region, **5 discrete zones** (WHITE / CYAN / BLUE / YELLOW / MAGENTA — pure RGB-corner keys) | YES — 4× `_Texture_Mask` (1024²) |
| **Silhouette lane** | Adventure / Fantasy Kingdom / Samurai (named characters) | whole-atlas palette-swap (A/B/C atlas variants; skin-tone whole-swaps) | NO — grep for `mask` → zero hits |

The §7.6 decision is **forced** by this bifurcation: the StyleProfile output field set is NOT uniform across the catalogue. A single rigid schema fails both ways — over-fit the modular lane and the silhouette lane carries dead null fields; under-fit to whole-tint and we throw away the 5-zone richness **Synty ships natively** (their own A/B/C-palette × per-region-mask is the very lever the architecture generalizes). The additive-nullable shape is the only shape that fits both lanes without waste or loss.

## 2. The schema (design-spec-as-math)

`StyleProfile.palette` is a structured field:

```
palette: {
  mode: "per_region" | "whole_tint",          # MESH-DERIVED at bind time (see rule 1)
  regions: [                                   # present iff mode == per_region; length = mesh's verified zone count (5 on Modular Fantasy Heroes)
    { region_key: primary | secondary | metal | leather | accent,   # semantic labels — EXPECTED-but-unrendered (rule 3)
      tint:     <RGB>,                          # per-region color the shader applies via mask-channel test
      finish:   <matte | satin | metallic | …>, # finish-per-region (pipeline doc §4)
      emission: <scalar 0..1 + RGB>             # emission-per-region — drives the six-profile aura apex (six-profile §7)
    }, …
  ],
  whole_tint: { tint: <RGB>, finish, emission } # ALWAYS present — the degrade target + the L3 fallback (rule 2)
}
```

**Rules:**
1. **`mode` is mesh-derived, not generator-chosen.** The bind step reads whether the bound Synty mesh ships a `_Texture_Mask`. If yes → `per_region` (`regions[]` populated, length = the mesh's verified zone count). If no → `whole_tint` (`regions[]` empty; `whole_tint` is the only palette field consulted). The generator does not get to pick richness it cannot render.
2. **`whole_tint` is ALWAYS present** — even on `per_region` meshes — as the L3 validation+fallback target (architecture record § 3.3). If a per-region mask read fails at render, the adapter falls back to `whole_tint` rather than rendering untinted. No render path is ever left without a tint.
3. **`region_key` semantics are EXPECTED-but-unrendered** (galadriel slice § 5 caveat). The 5-zone **count** is decision-grade (5 ≥ the ≥3 threshold prediction #2 required); the per-zone **semantic label** (which zone is "metal" vs "leather") needs one Godot/Blender import render to lock. Until that render lands, the manifest carries the labels as **provisional**. This is NOT a gate on the schema — the schema is correct regardless; only label-to-zone binding awaits the render (galadriel §7.4 hook).

## 3. What this unblocks — and what it explicitly does NOT

**UNBLOCKS** (the §7 acceptance hooks that were gated on this ruling):
- **rocket §7.2** — the L2 restyle-leaf master `ShaderMaterial` can be built against a 5-region mask + per-region palette (per_region lane) with a whole-tint shader path (silhouette lane). Field set is specified.
- **rocket §7.2** — the **accent-attachment system** fires **unconditionally**: galadriel verified 12 named sockets (`All_00`..`All_12`) + 4 cape sockets, so the "if §4 step 2 confirms rig sockets" condition is satisfied. Maps to Godot `BoneAttachment3D` / UE `SocketName` per L4 neutrality.
- **star-lord §7.3** — the constrained API-LLM StyleProfile-fill now has a concrete field set to fill (per-region tints drawn from the manifest palette menu; D7-narrow-blank preserved).
- **elrond §7.1** — the manifest substrate half knows the field shape to supply per mesh (mode + zone count + provisional region labels).
- **drax §7.5** — the L4 adapter knows the abstract render-intent shape to translate to a Godot `.tres`.

**DOES NOT unblock / still gated:**
- The per-zone **semantic labels** (metal vs leather) — one render pass locks these (galadriel §7.4); provisional until then.
- The drive-router **leaf implementations** (shader code, LLM-fill wiring) — rocket/star-lord build work, sequenced **after** the manifest design-owned half + elrond's substrate slice land.
- Whether to **adopt any procgen-assembly tool** (legolas options matrix) — separate, future, Matt-gated; nothing here depends on it.

## 4. Sequencing note (carried into the autonomous run)

This ruling is a **pre-condition, not a build trigger.** rocket's §7.2 build fires only after BOTH (a) this ruling [done] AND (b) the manifest design-owned half + elrond's substrate slice land (so the shader has a real field set AND real values to consume). In the v2 run, rocket §7.2 is **Tier-2-gated-on-manifest**, not fire-immediately. The ruling removes gandalf from the critical path; it does not collapse the remaining sequencing.

## 5. Sign-off

**Recognition → validate → commit honored:** architecture locked 2026-06-16 (recognition); §4 empirical gate cleared 2026-06-17 via galadriel YES/YES (validate); this ruling fires the §7.6 commitment (commit). The ruling is the gated commitment whose gate just resolved — not premature, not time-driven.

**Signed:** gandalf, 2026-06-17.
