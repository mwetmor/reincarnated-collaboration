# Forge / Loadout Web-App — Design-Learnings Note (captured as the loadout seam's forward roadmap is paused)

**STATUS:** DESIGN-LEARNINGS NOTE — heuristics + interaction models worth carrying into UE-side tooling, captured as active forward development on the loadout web app is paused (no further roadmap)
**Date:** 2026-06-10
**Author:** drax (Opus 4.8)
**Context:** Loadout-seam roadmap pause (Matt-authorized). The app — including the 2D cosmograph (`/forge`) — **stays live on Vercel as-is**, and the **original cosmograph form is explicitly retained** (Matt still plans to use it). This is **frozen, NOT retired and NOT dark.** What is paused is only the FORWARD roadmap; the learnings below remain valuable design knowledge for UE-side tooling even while the web surface lives on. (Scope-corrected 2026-06-10 — an earlier framing of these notes as "salvage before killing the app" was based on an over-broad retirement reading that Matt narrowed to a roadmap freeze.) Dispatch + scope-correction note: `agentic_orchestration/dispatches/2026-06-10-drax-forge-loadout-wind-down.md`.
**Companion:** gandalf rationale `agentic_orchestration/gandalf/notes/2026-06-10-forge-windown-recommendation-for-kr.md`

---

## 0. What does NOT migrate (state plainly first, per drift-guard)

- **The 2D web layout itself does NOT migrate.** UE computes the sphere from the embedding per the cosmograph spatial-layout contract ("sphere positions only" after the `forge_2d` projection clause is dropped — see § 3.6 of the radagast manifestation review). The forge's force-directed 2D placement is a web-canvas artifact; the UE surface derives 3D-shell positions from the substrate embedding directly.
- **Per-primitive iconography** was already RETIRED at the § 12 framing scope (~80 icons obviated; 29 Phase 4 placeholder icons deprecated, replaced with cycling text-list). Nothing to salvage there.
- **The forge-provenance open question** (radagast review § 3.3, routed to drax) is **MOOT** with one surface — dropped, not migrated.

What follows is what DOES carry forward: heuristics, interaction models, voice-template learnings, and data-shape findings — not pixels.

---

## 1. Layout heuristics (carry as design knowledge, not code)

These are empirical findings from `src/utils/constellationModeLayout.ts` (Mode B kit-as-bounded-constellation spike, 2026-06-07). They are about the SHAPE of the substrate, so they transfer to the UE 3D-shell layout problem even though the 2D code does not.

1. **UMAP primitive-space centroids are degenerate for kit-level placement.** All 1000 kit centroids spanned only **43×56 px** on the 2D canvas at 1.0× zoom — smaller than ONE constellation radius (70px). Mean nearest-neighbor distance between kit centroids = **1.3 px**. This is structural: all kits share the same primitive vocabulary, so all kit centroids collapse toward the center of primitive space.
   - **UE consequence:** if UE tries to place kit-constellations using the primitive-space embedding centroid, kits will pile on top of each other. UE needs a **separate kit-to-kit similarity embedding** (or a force-directed inter-constellation layout using shared-primitive-fraction as the edge weight) to spread constellations across the sphere. This is the `// TODO(drax)` the forge carried (engine never shipped a Mode-B-valid embedding) — it becomes an **engine/elrond requirement for the UE surface**, not a drax override.
2. **Two-stage layout decomposition works.** Stage 1 places N constellation centroids (repulsion between all pairs; spring attraction ∝ shared-primitive-fraction → similar kits adjacent, all well-separated). Stage 2 places per-kit primitive instances within a bounded radius of the centroid. The bounded-radius discipline (MAX_CONSTELLATION_RADIUS = 70px, tuned from a 60–80 range; 40px read as too tight) is the readability anchor — it keeps each constellation legible as a unit. UE's 3D-shell equivalent wants the same "bounded local cluster per kit" discipline so a constellation reads as one thing.
3. **Lasso dedupe-before-score semantics.** When a lasso captures per-kit primitive INSTANCES (`kit_001:fire`, `kit_002:fire`), DEDUPE to unique primitive_ids BEFORE composite-score resolution — otherwise shared primitives double-count. This is a selection-math rule that transfers directly to UE's Path-L lasso (the dual-path creation moment).

## 2. Cascade / spirit-guide interaction model (the load-bearing migrate-forward)

This is the most valuable salvage. From `src/data/cascadeData.ts` + `src/components/Cosmograph/CascadePanel.tsx` (Phase 5, per Earth-Avatar Creation Moment Architecture § 12 canonical lock).

- **Spirit-guide-driven elicitation cascade** validated as an interaction shape at the web layer: spirit guide opens "What is most important for your journey this season?" → player names a precedent → **7 Tier 1 anchors** (Race / Element / Weapon / Power / Style / Harvest / Horizon — CANONICAL per § 12.3) → nested cascade 3–5 layers deep (Tier 1 → Tier 2 → Tier 3 → final emergence) → nearest-kit-centroid lookup → spirit guide narrates the emergent kit identity.
- **Cycling text-list preview UX** (§ 12.4) proved out: text-list cycling with touch swipe + keyboard nav + arrow nav + breadcrumb path. The **iPad-text / sky-runes split** (text labels at every cascade layer on the tablet; runes-only in the sky per the § 11 visual register) is the cross-surface input model. UE inherits this as the creation-moment input architecture — the cascade STRUCTURE migrates even though the React component does not.
- **INPUT vs OUTPUT primitive distinction** (§ 12): player SELECTS input primitives (the cascade anchors); engine EMERGES output primitives, surfaced via spirit-guide narration. This separation is a design invariant UE must preserve — it keeps the player's agency (input) distinct from the substrate's emergence (output).
- **Sky-region-illuminates-on-soft-preview** coupling: each Tier 1 anchor maps to a sky region that illuminates on soft-preview before commitment. In the forge these positions were SCAFFOLD (drax discretion, canonical spatial lock deferred to Pattern B). UE recomputes them from the embedding — but the COUPLING (anchor → region illumination → commitment) is the migrate-forward, not the coordinates.

## 3. Voice-template learnings (D31 neutral-data-oracle)

From the Phase 5 follow-on (`cascadeData.ts` tier1_commit template edit, commit `2d8d539`):

- **Neutral-data-oracle voice (D31, canonical 40 D28–D32) is operationally distinct from interior-state language.** Concrete worked example: `"Your path projects toward …"` (oracle-narrated, substrate-emergent projection — CORRECT) vs `"You are drawn to …"` (editorialized interior-state language — WRONG; replaced). The oracle narrates what the substrate PROJECTS, it does not assert what the player FEELS.
- **D7 discipline held:** all spirit-guide voice patterns are fully TEMPLATED (no raw LLM dialogue at runtime). UE's spirit-guide narration should inherit the templated-voice discipline — the oracle voice is a finite template library keyed off substrate emergence, not a live LLM call in the creation loop.
- **Grep-audit discipline:** when correcting a voice violation, grep the whole voice corpus for sibling instances ("You are drawn to" had no other instances — verified). UE-side voice authoring should carry the same audit habit.

## 4. Data-shape work (consumer-side schema findings)

- The forge consumes `public/kit-space/kit_star_sign_assignments.json` (rocket/elrond sidecar; injectivity-enforced v1.1 at HEAD `aae190a`) and per-season kit-space exports. The **kit ↔ star-sign 1:1 binding (Branch A)** data shape is validated as renderable — UE inherits the same sidecar contract.
- **Substrate-trace + categorical-label packet shape** (engine pre-generates corpus offline → JSON packet ships kits with substrate-trace + categorical labels + identity content → surface does substrate-selection → character-LOOKUP, NOT generation) is the cosmograph-pivot architecture. The forge proved the consumer side of this packet works; UE consumes the SAME packet shape. No re-derivation needed — the data contract is the durable artifact.

## 5. Forward-looking discipline note (NOT a drax action item — flag for radagast / mantis / david-h)

Per gandalf rationale § 4: **the web iterated faster than UE's compile/DDC loop.** As the forge retires, the team should preserve SOME fast design-iteration path UE-side — even an internal-only tool — so design exploration of the creation moment (cascade vocabulary, anchor tuning, voice templates, layout heuristics) isn't strangled by the UE editor/compile cadence.

This is a **forward-looking note for radagast / mantis / david-h consideration at the PC/UE seam** — it is NOT a drax action item and NOT a reason to keep the web app. The forge's iteration-speed VALUE is real; the recommendation is to recreate that speed UE-side, not to retain the retired surface.

---

**Sign-off:** drax, 2026-06-10. Design-learnings captured as the loadout seam's forward roadmap is paused. The 2D web surface — including the cosmograph — STAYS LIVE; these heuristics, the cascade/spirit-guide interaction model, the D31 voice-template learnings, and the packet/sidecar data contracts carry forward into UE-side tooling as design knowledge. Composes with the cosmograph-pivot architecture and the Earth-Avatar Creation Moment Architecture § 12 canonical lock.
