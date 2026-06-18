# galadriel spike — cross-era per-region-mask generalization (restyle-multiplier gate)

**STATUS:** REQUEST (gandalf → galadriel, routed via KR)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 — author the cross-era generalization spike (Q2 gate 2).
**Seam:** galadriel (visual perception). Read-only catalogue analysis; same toolchain as the 2026-06-17 slice-verification.
**Companions:**
- `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/slice-verification-2026-06-17.md` — the fantasy-era baseline this spike extends (predictions #2 + #3 YES on Modular Fantasy Hero Characters).
- `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` — the §7.6 ruling; the `per_region` path is the § 4.1 palette-remap lever.
- `agentic_orchestration/gandalf/notes/2026-06-17-synty-acquisition-run-ruling.md` § Q2 (gandalf, same session) — the three-gate framing this closes gate 2 of.

---

## 0. Framing — gate 2 of the gear-spec upstream-wiring decision

The per-region `_Texture_Mask` restyle scheme (the §7.6 `per_region` path = the pipeline doc § 4.1 **palette-remap lever**, the *dominant differentiation multiplier* — "hundreds of distinguishable looks from this alone") is empirically verified on **one pack in one era**: `POLYGON - Modular Fantasy Hero Characters` (fantasy; 5 zones WHITE/CYAN/BLUE/YELLOW/MAGENTA). The content engine produces **all eras** (`canonical/48` ships industrial/modern classes; sci-fi roadmapped). So the restyle multiplier — and the accent-rig socket system (§4 prediction #3, the only torso/legs silhouette-breaker) — must generalize across eras, and both are **UNVERIFIED** outside fantasy.

Why it matters: per the differentiation budget (gear-spec record § 3.6), base-mesh-spread is FIRST, accents SECOND, palette-remap restyle THIRD — *the multiplier on top*. If UV-region separability FAILS for an era (regions baked into one atlas, no mask), the restyle multiplier degrades to whole-atlas tint for that era and differentiation leans entirely on base-mesh-spread + accents (the §4 "if FALSE" reshape). This spike measures whether that reshape is forced at the modern/sci-fi era-edges — extending §4 resumption-gate predictions #2 (UV-region separability) + #3 (accent-rig sockets) from fantasy to all eras.

## 1. The two questions

1. **Mask generalization:** do modern + military/near-future Synty **skinned armor/character** packs ship a per-region `_Texture_Mask` (→ `per_region`; full restyle multiplier across eras) OR a whole-atlas swap (→ silhouette; restyle degrades to whole-tint for that era)?
2. **Sci-fi-body existence:** does a POLYGON sci-fi **skinned-character** pack exist at all, or is sci-fi-body a register-gap (only `SIMPLE - Space Characters` seen) that routes to Sidekick/Meshy? (An *absence* here is itself a decision-grade answer.)

## 2. Sample (galadriel's final pick from the catalogue; named candidates)

- **Modern:** `POLYGON - City Characters Pack` (clearest modern-register skinned characters).
- **Military / near-future:** `POLYGON - Military Pack` OR `POLYGON - Apocalypse Pack` / `POLYGON - Apocalypse Wasteland` (soldiers/survivors).
- **Sci-fi existence-check:** investigate whether ANY POLYGON pack carries sci-fi *skinned characters* (`Sci-Fi Horror`? `Sci-Fi City`?); if none, that absence answers Q2.
- **Fantasy re-baseline:** re-confirm against `Modular Fantasy Hero Characters` (the known `per_region` exemplar) so the cross-era reads are calibrated to the same method.

## 3. Method (same as slice-verification-2026-06-17 — NO mesh-render needed; honor the tooling gap)

- grep each pack for `mask` / `_Texture_Mask` texture files.
- For any mask found: PIL/numpy **zone-count** (how many discrete RGB-corner zones? — Modular Fantasy Heroes had 5).
- FBX **node-name** string check for accent sockets (`All_NN`, cape sockets) — does the cross-era rig carry the same socket convention the §7.2 accent system depends on?
- Classify each sampled pack: `per_region` (full restyle multiplier) | `silhouette` (whole-atlas swap; restyle degrades to whole-tint) | `absent` (no skinned-character coverage — gap).

## 4. Deliverable + scope discipline

**Deliverable:** per-pack {mask YES/NO, zone-count, socket-presence, restyle-classification} + an explicit statement on the **sci-fi-skinned-character gap**. Path: galadriel's call; recommend `agentic_orchestration/research/catalogue/synty-recon-2026-06-16/cross-era-mask-spike-2026-06-17.md`.

**Scope:** this is a SPIKE — 1 modern + 1 military + the sci-fi existence-check + the fantasy re-baseline. **Hours, not days.** It de-risks the restyle multiplier + accent system across eras; it does NOT need exhaustive coverage of all ~101 POLYGON packs (elrond's parallel tagging covers breadth; this spike covers mask-mechanism depth at the era-edges).

**How it pairs with elrond:** galadriel answers the **mask-mechanism** half (does the restyle lever generalize across eras?); elrond answers the **coverage** half (which packs/eras/cultures exist?). Together they resolve Q2 gates 1+2 and tell us whether the gear-spec upstream wiring can go all-era or fantasy-first.

**gandalf reviews on return:** the restyle-classification feeds my §7.2-honors-§7.6 conformance review and the all-era-vs-fantasy-first wiring call.

**Signed:** gandalf, 2026-06-17.
