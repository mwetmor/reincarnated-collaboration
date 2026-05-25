# Parked Loadout Amendments — Post-v1-Narrow Fast-Follow

> **STATUS:** PARKED 2026-05-25 — awaiting Matt signal for KR dispatch authorization. Hold until KR has a clear pause; do NOT distract Cycle 12 critical-path work.

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-25 — verbatim "yes but let's save both of these amendments up for a clear pause in knight-rider's work. I do not want to distract. When the moment is right, I'll let you know."
**For:** drax (loadout app implementation) + KR dispatch routing
**Bundled together:** two amendments combine cleanly because both touch the same loadout components (form display + skill tree panel)

---

## Amendment 1 — Design-mode toggle for engine-layer fields

**Source:** gandalf Q2 surfacing 2026-05-25; Matt ratification "Yes, I agree with Option 2."

**Scope:** add a toggle to loadout form-display panel that switches between:
- **Player-mode** (default; current M1-M6 surface) — uniform archetypal naming; engine-internal fields hidden per bi-modal form-library architecture (per skill-system § 12.3 + § 12.4)
- **Design-mode** (toggle-activated) — exposes engine-layer fields for T4 post-mortem authoring:
  - `named_bearer` / `named_mythological_match` (engine-layer identity per Sketch F anchors)
  - `mechanical_substrate_triple` (per L9 — the BDI math substrate tuple)
  - `source_library` (provenance: generator_v2 / engine_authored_gap_fill_v1 / legacy)
  - `bc_target_cell` (5-tuple identity)
  - `converged_modifier` (Layer 4 output)
  - Optional: `t4_alteration_output` raw struct (alongside spirit-guide narration)

**Why parked:** non-blocking for engine v1 narrow generation milestone; T4 post-mortem can proceed with CLI/notebook tooling for engine-internal data; design-mode toggle is convenience tooling, not a milestone gate.

**Drax effort estimate:** ~0.5 day (toggle component + field surfacing per existing M-item components)

---

## Amendment 2 — Cultural / period / quality-tier badge surfacing

**Source:** gandalf weapon-visibility clarification 2026-05-25 surfacing that M1-M6 ratified weapon NAME display but didn't explicitly ratify cultural / period / quality_tier badge display.

**Scope:** add to loadout form-display per main weapon + off-hand item:
- **Cultural tag badge** — from weapon's `cultural_lineage_canonical` (european / east_asian / mesoamerican / etc.)
- **Period tag badge** — from weapon's `historical_period_canonical` (classical / medieval / contemporary / mythological / etc.)
- **Quality-tier badge** — from weapon's `quality_tier` (S / A / B / C) — functions as INFORMATIONAL rarity for v1 viewing purposes (Tier S forms feel legendary; Tier B forms feel common); NOT the player-game ARPG drop rarity mechanic (which is v1.1+ territory)
- **Substrate provenance** — if quality_tier is engine-authored gap-fill (per M5 existing badge), preserve current treatment

**Why parked:** non-blocking for engine v1 narrow generation milestone; weapon name already displays via M1 + provenance flag via M5; the cultural / period / quality-tier badges enrich design-mode review but aren't milestone gates.

**Drax effort estimate:** ~0.25 day (badge components consuming existing weapon record fields)

**Combined drax effort (both amendments):** ~0.5-0.75 day; bundles cleanly because both touch loadout form-display + skill-tree panel components

---

## Re-engagement trigger

**Matt signals "fire the loadout amendments"** when KR has a clear pause in Cycle 12 critical-path work. Likely natural seams:

1. **Cycle 12 closes + engine generation run completes + ~30-40 forms displayed in loadout** — this is the v1 narrow milestone Matt is aiming for tonight; once Matt confirms the forms look right via player-mode display, design-mode + badge enrichment can fire as fast-follow without distracting from milestone
2. **T4 post-mortem session 1 surfaces a specific gap** — if Matt's first post-mortem review finds he wants design-mode toggle to evaluate engine-layer choices (named_bearer alignment with T4 keystone; substrate_triple congruence; etc.), this becomes the natural fire trigger
3. **Cycle 13 opening** — could absorb as part of Cycle 13 scope alongside whatever Layer 7 / BDI test framework / next-cycle scope lands

**Matt's call on timing.** Per his verbatim: "When the moment is right, I'll let you know."

---

## KR dispatch authoring (when triggered)

Single drax dispatch authoring both amendments per bundled scope above. KR routes via:
- Standard Pattern B dispatch authoring per dispatches/README.md
- gandalf Pattern A-light consultation if Matt amends drax recommendations on specific UI placement / badge styling
- jack-ryan Gate-2 validates output

---

## What this note does NOT touch

- **Player-facing ARPG rarity mechanics** (common / uncommon / rare / epic / legendary) — v1.1+ design territory; separate from quality_tier badge surfacing
- **Faction membership display** — deferred per roadmap § 3.4 faction architecture
- **Per-fight spatial telemetry display** — v1.1+ multi-seam work per gandalf 2026-05-25 honest assessment
- **Other M7+ loadout items** — out of scope; this note covers ONLY the two amendments Matt ratified this session

---

## Sign-off

**Author:** gandalf 2026-05-25
**Status:** PARKED — awaiting Matt signal for KR dispatch authorization
**Re-engagement criterion:** Matt-explicit signal ("When the moment is right, I'll let you know")
**Combined drax effort estimate when triggered:** ~0.5-0.75 day
**Downstream consumers:** drax (implementation); jack-ryan (Gate-2); Matt + gandalf (T4 post-mortem benefits from design-mode toggle especially)
