# Decisions-log entry drafts — Style register + Naming triad

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source canonical docs:** `canonical/story/style-register.md`, `canonical/story/naming-triad.md`
**Process:** Gandalf flagged these canonical locks as requiring decisions-log entries per ADR-002. Knight-rider drafts → Matt approval (or jack-ryan Gate 1 first) → write to `reincarnated-engine/design/decisions/decisions-log.md`.

---

## Entry 3 — Style register locked

### 2026-05-15: Style register locked — Hand-drawn pixel-art (HD-2D-shaped)

**Decision:** The project's primary visual style register is **Candidate B — Hand-drawn pixel-art (HD-2D-shaped)** per `reincarnated-collaboration/canonical/story/style-register.md`. This is the locked register against which all rendering, catalogue filtering, and asset commissioning operates.

The register is **a consumption-time filter, not a crawl-scope constraint** (per the score-don't-filter principle codified in AGENTS.md for the catalogue work). Legolas Mode B crawls all viable sources regardless of style; assets are tagged by register at extraction; the engine + design pipeline filters at consumption.

**Reasoning:** The empirical asset landscape (per `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`) shows that hand-drawn pixel-art HD-2D-shaped sources (pimen, CreativeKind, Elthen, LuizMelo, Foozle, ansimuz when curated) cover the project's mechanical needs across all Tier-1 elements (fire/ice/lightning/water/earth/wind/holy/dark/poison/explosion) and most Tier-2/3 niches without per-season bespoke art. This register matches:

- Reincarnated's mythic-ARPG-with-isekai-DNA tone (cf. Solo Leveling adaptation's hand-drawn-influenced palette)
- The 200ms ARPG recognition target (sufficient silhouette + palette differentiation; see decisions-log enemy-visual-legibility entry)
- Family-pace sustainability (no per-season custom art required; palette/aura overlay on stable archetype registry)
- Pixi.js consumption (cleanest workflow per source research)
- The Court framing's narrative weight (named retainers reading as characters, not avatars)

**Alternatives considered:**

- **Candidate A — Retro pixel-art (current state by inheritance):** demo1's current implementation. Rejected as the locked target. Reads as retro-genre-specific rather than mythic-ARPG; insufficient fidelity for the Court's character-weight register. Demo1 may continue in this state until v0.7-encounter-analytics + Court hub work justifies the register migration.
- **Candidate C — Pure hand-drawn 2D anime:** narratively appropriate but operationally infeasible at family pace; catalogue coverage is sparse for monsters and VFX; would require commissioning. Out of scope.
- **Candidate D — Vector / clean-line:** technically clean (CraftPix vector packs available) but visually too "infographic" for an ARPG; loses the mythic weight the Court framing requires.

The "HD-2D-shaped" descriptor specifically signals: pixel-art *informed by* HD-2D fidelity targets (Octopath Traveler / Triangle Strategy reference), not retro-only pixel-art. The locked register accepts pixel-art assets that read as illustrated rather than 8-bit/16-bit retro.

**Status:** Active. Implementation cascades:

- **Legolas** — Mode B catalogue crawls tag each asset's `style_register`; sources prioritized by register-coverage density (pimen first per separate dispatch)
- **Elrond** — catalogue DB schema includes `style_register` as a curated dimension; consumption-time filter queries reference this column
- **Drax** — demo + loadout rendering targets the locked register; existing demo1 retro-pixel assets remain operationally accepted until next refresh
- **Gandalf** — design conversations and downstream story-docs reference this lock; new design proposals that imply a different register get pushback at design-track viability gate

**Status of demo1's current visual state:** demo1's existing retro-pixel rendering is operationally accepted as legacy; the locked register applies to forward work. Migration sequencing is drax + knight-rider's call when the next visual-layer refresh is dispatched.

**Related:** `reincarnated-collaboration/canonical/story/style-register.md` (full canonical doc, 4 candidates + 4 open questions); `canonical/story/enemy-visual-legibility.md` (S1 sprite-archetype registry sourcing aligned with this lock); `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (empirical landscape); `canonical/37-form-bias-diagnosis-and-recovery.md` § Catalogue path (the score-don't-filter principle this lock operates under).

---

## Entry 4 — Naming triad locked + per-season variation pattern

### 2026-05-15: Naming triad — Trial / Mirror / Passage locked as universal frame; per-season variation pattern locked

**Decision:** The three player-facing choice-moments in a season's arc are canonically named:

- **The Trial** — the act-culmination encounter where the player faces the seasonal cosmology's confrontation. Retained from existing locked terminology.
- **The Mirror** — the doppelganger-fight option at Trial. **Renamed from "doppelganger"** for substrate-incompatibility (the pejorative-coded prior name imported a humanoid-narrative bias) and to invoke the cosmological register the meaning-of-the-arc statement establishes.
- **The Passage** — the death-respawn / form-loss option. **Renamed from "death-body-swap"** for neutrality (the prior name read as failure-coded; "passage" frames the moment as cosmological transition consistent with the Wheel's turning).

These three names are the **universal frame** — stable across all seasons; used in design docs, telemetry technical names (engine-side fields like `doppelganger_validation_runs` can retain technical names until export-boundary or rendering-layer rename), cross-season Spirit Guide references, choice-screen helper-text.

Each season ALSO carries **per-season variants** of these universal-frame names — flavored to the season's cosmology and prose register. Both coexist: the universal frame stays stable so the player learns the vocabulary across seasons; seasonal flavor surfaces in-season for cosmological resonance.

**Generation integration with the cipher architecture (doc 37 § 6):** per-season triad variants are generated in the **same LLM call** as the seasonal elemental vocabulary. One coherent cosmological-vocabulary call per season — not four separate calls — bounding LLM cost and ensuring intra-season cosmological coherence.

**Worked example — Yomi season Passage moment** (per `canonical/story/naming-triad.md` for downstream drax choice-screen reference):

```
THE WHEEL TURNS.

→ Refuse the Pomegranate
  (Refuse the Passage — respawn, small XP loss)

→ Accept the Pomegranate
  (Accept the Passage — transform, this form lost forever to this season)
```

The Yomi variant invokes the Izanami myth's binding-via-pomegranate mechanism applied verbatim to the season's death-mechanic. This level of cosmological resonance is the kind of finding the cipher work makes possible.

**Reasoning:** Prior terminology (`doppelganger` for Mirror, `death-body-swap` for Passage) was technically descriptive but carried substrate-bias and tonal problems. "Doppelganger" is humanoid-coded (doppels are pejorative humanoid-imitation tropes from European folklore). "Death-body-swap" reads as failure-state mechanical naming, fighting the cosmological framing the meaning-of-the-arc statement establishes.

The universal-frame + per-season-variant pattern preserves:

- **Player learnability** — universal frame teaches the same three moments across all seasons; the player recognizes Trial-Mirror-Passage as the season's core choices regardless of seasonal flavor
- **Per-season cosmological weight** — seasonal variants invoke the specific season's mythology, making each season's death/transformation/confrontation feel native to its cosmos
- **Operational stability** — engine-side technical names (telemetry columns, code identifiers) need not churn per season; the rename surfaces at export-boundary or rendering-layer

**Alternatives considered:**

- **Keep "doppelganger" / "death-body-swap"** — rejected for substrate-bias + tonal-mismatch reasons above.
- **Single per-season vocabulary with no universal frame** — rejected for player-learnability cost. Players would have to re-learn three terms each season.
- **Single universal frame with no per-season variation** — rejected for missing the cosmological-weight opportunity the cipher architecture enables.

**Status:** Active. Implementation cascades:

- **Star-lord LLM prompt construction** — per-season cosmological-vocabulary generation call now includes triad-variant generation alongside elemental-vocabulary generation. One call, four outputs. Anti-bias scaffolding (Discipline #14 candidate) applies — no canonical four element labels in prompt, no universal frame literals as anything other than design-frame instruction.
- **Drax choice-screen rendering** — choice screens display seasonal-variant primary text + universal-frame helper-text in parentheticals per the Yomi worked example above.
- **Engine-side telemetry retention** — existing field names (e.g., `doppelganger_validation_runs`) can stay; rename optionally at export-boundary or rendering-layer at next-touch convenience. Not urgent.
- **Spirit Guide voice** — in-season references use seasonal-variant primary; cross-season references use universal frame (per spirit-guide-voice.md when authored).

**Five open questions parked** (per source doc): variant length register; variant stability within season; player-naming of variants; marketing register; existing-season retrofit. None blocking.

**Related:** `reincarnated-collaboration/canonical/story/naming-triad.md` (full canonical doc); `canonical/story/cosmology-reincarnated.md` (Trial/Mirror/Passage sit within); `canonical/story/court-of-forms.md` § meaning-of-the-arc (the Passage and Mirror moments contribute to "how many ascended through their full journey"); `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 (cipher architecture this generation-integration leverages); forthcoming `canonical/story/spirit-guide-voice.md` (voice-line patterns at each triad moment).
