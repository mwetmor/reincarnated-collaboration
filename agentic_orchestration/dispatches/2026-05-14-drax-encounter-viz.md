# Dispatch — 2026-05-14 — drax — encounter visualization tier 1

**From:** knight-rider
**To:** drax
**Approved by:** Matt, 2026-05-14
**Estimated effort:** 3–4 hours
**Acceptance:** `/encounters` route loads in the app; selecting Lantern-Keeper of Yomi's Winds shows a swarm pack of ~8 monsters with an AOE radius overlapping most of them, annotated "8/8 hits → ~8x damage vs single target." Hollow Wind Ascetic shows the same pack with a single-target indicator on 1 monster.
**Tag:** `drax/v0.6-encounter-viz` (milestone tag `v0.6-encounter-viz` requires Matt approval on visualization quality)
**Gate 1:** Skipped — single-seam, no decisions-log impact, no cross-seam schema change.

**SEQUENCING: Do not start until `v0.5-real-gear` is tagged and shipped.**

---

## Context

B10.2 ships empirical evidence that AOE classes get ~8x damage on swarm packs via PackProxy mechanics (one AOE skill hitting all N pack members simultaneously). This is the ARPG genre payoff the balance system was designed to produce. Players, reviewers, and eventual playtesters need a way to *see* why this matters. A static SVG schematic per class illustrates the AOE-vs-pack interaction without needing animated fight playback.

---

## What knight-rider already knows about the data (do not re-investigate)

**Skill geometry field:** Does NOT exist in the current class JSON schema. Skills have `effect_category` (`area_damage`, `single_target_damage`, `burst_damage`, `damage_over_time`, `control`, etc.) but no geometric primitive field. Use `effect_category` to infer geometry:

| effect_category | Geometry to render |
|---|---|
| `area_damage` | Circle (AOE radius) |
| `single_target_damage` | Arrow / point indicator |
| `burst_damage` | Point indicator |
| `damage_over_time` | Point indicator |
| `control`, `mobility`, `defensive`, `sustain`, `utility` | Not rendered in encounter viz |

**Future wiring note:** When rocket's B11 work produces a real `geometry` field on skills, replace the inference table above. Leave a `// TODO: wire B11 geometry field` comment in the component.

**Primary attack field:** `role: "primary_attack"` IS a real engine field — not a cooldown heuristic. Skill `role` values include: `primary_attack`, `area_damage`, `burst_damage`, `damage_over_time`, `control`, `mobility`, `defensive`, `sustain`, `utility`. Use this field to identify which skill to highlight as the class's featured skill in the visualization.

**Three confirmed classes for v1:**

| File | Name | Archetype | AOE skills | Range |
|---|---|---|---|---|
| `class_0001.json` | Lantern-Keeper of Yomi's Winds | `hybrid_mage` | 1 / 14 | long |
| `class_0005.json` | Miasma Warden of the Sunken Gale | `physical_skirmisher` | 1 / 10 | close |
| `class_0010.json` | Hollow Wind Ascetic | `experimental` | 0 / 10 | close |

**Key insight for visualization:** No Yomi class has more than 1 `area_damage` skill. The AOE vs non-AOE contrast is binary — either a class has one AOE skill (8x on pack) or it has none (1x single-target). The multiplier comes from PackProxy mechanics (one AOE hitting all N pack members), not from having many AOE skills.

**Pack composition (from B10.2 design intent — treat as ~values until B10.2 ships real code):**
- Pack size N: approximately 8 (exact value locked by gamora in B10.2 math phase)
- Pack homogeneity: same element + same archetype within a pack
- Tier: swarm-tier (smallest circles)

---

## What to build

### New route: `/encounters`

Matt leaves the layout to drax. Options: new route or new tab on `/sample`. Keep mobile-first (375px).

### SVG schematic per class

Render a two-panel diagram side by side (or stacked on mobile):

**Left panel: AOE class against pack**
- Pack of N circles arranged in a loose cluster
  - Circle size: small (swarm tier)
  - Circle color: pack's `dominant_element` color (read from the class's element palette or use element color map)
  - Label cluster: "Swarm Pack (N)"
- AOE skill overlay: large semi-transparent circle centered on the pack
  - Color: class's primary AOE skill color (read `color_value` from skill JSON)
  - Should visibly overlap most or all pack members
- Annotation: `"[Skill Name] hits Y/N → ~[Y]x vs single target"`

**Right panel: single-target class against same pack**
- Same pack cluster rendered identically
- Single-target indicator: arrow or highlighted ring on ONE circle
- Annotation: `"[Skill Name] hits 1/N → 1x"`

**Class selector:** Dropdown or tab to switch between the three classes. Default to Lantern-Keeper.

**No animation required.** Static SVG. No D3 dependency — hand-rolled SVG with React.

---

## Scope

- [x] Read actual `effect_category` from class JSON to determine AOE vs single-target (no geometry field — use inference table above)
- [x] New `/encounters` route (new tab in nav — drax's call)
- [x] Class selector: Lantern-Keeper, Miasma Warden, Hollow Wind Ascetic
- [x] SVG pack cluster: N=8 circles, colored by dominant_element, swarm-tier radius
- [x] AOE overlay: semi-transparent circle when class has `area_damage` skill; dashed ring when none
- [x] Single-target indicator: ring + tick on closest pack member when class has no `area_damage`
- [x] Annotation: "{Skill Name} hits Y/N → ~Yx vs single target" / "1/N → 1x"
- [x] Leave `// TODO: wire B11 geometry field` comment in geometry inference (in Encounters.tsx)
- [x] Mobile-friendly at 375px (2-col grid, SVG width 100%)
- [x] Verify no regressions on `/loadout`, `/sample`, `/analytics`
- [x] Tag: `drax/v0.6-encounter-viz` on `main`
- [ ] Push to `origin/main` — SKIPPED: no `origin` remote in loadout repo
- [x] Update `AGENT_STATE.md` at session end
- [x] Append completion record to this dispatch file

---

## Completion record

**Completed by:** drax
**Date:** 2026-05-14
**Commit:** `24669c7` (`drax/v0.6-encounter-viz` tag on `reincarnated-loadout` main)
**Preview URL:** https://reincarnated-loadout-cd6428rrk-matthew-wetmore-s-projects.vercel.app

**Implementation notes:**
- Two-panel layout (always shown): AOE panel (left) + single-target panel (right)
  - AOE panel: semi-transparent circle + full-opacity stroke overlaying pack; dashed ring when no AOE
  - Single-target panel: ring highlight + downward tick on pack member at index 4 (closest to center)
- `Skill.color_value` used for overlay/indicator colors, brightened +100/channel for dark UI visibility
  (Yomi palette colors are very dark; brightness boost is presentation-side, value still from engine)
- Pack color from `dominant_element` → element hex map (fire=#f97316, physical=#94a3b8, etc.)
- `Skill.color_value: number` added to Skill type in types.ts (was missing; is a real engine field)
- No D3 dependency — hand-rolled SVG with React as specified
- `// TODO: wire B11 geometry field` comment placed at top of Encounters.tsx geometry section

**Acceptance check:**
- Lantern-Keeper: AOE panel shows "Yomi Lantern Exhale" circle over 8 monsters, "8/8 hits → ~8x"
- Miasma Warden: AOE panel shows "Yomi Gale Rending" circle, same annotation
- Hollow Wind Ascetic: AOE panel shows dashed ring "No area_damage skill"; single-target panel
  shows "Gale from Below" ring indicator on 1 monster, "1/8 hits → 1x" ✓

**Milestone tag (`v0.6-encounter-viz`):** Requires Matt approval on visualization quality per dispatch.
`drax/v0.6-encounter-viz` (intermediate) is on main. Matt promotes to milestone tag when satisfied.

---

## Out of scope (explicit non-goals)

- Animation or real fight playback — static SVG only
- D3 or any new visualization dependency
- More than 3 classes in v1
- Reading actual B10.2 PackProxy code — use N≈8 as design-intent placeholder
- Any engine-side changes
- Skill gate bug fix, Tailwind trim, CC-BY attribution, Tier 3 analytics — still queued separately
- UI-side skill calculations — out of scope per Matt

---

## References

- B10.2 gamora dispatch: `agentic_orchestration/dispatches/2026-05-14-gamora-b10-2-pack-proxy.md` — pack size math (M1), AOE multiplier model (M3)
- Yomi class data: `reincarnated-loadout/data/season_002328/classes/`
- Prior loadout tags: `v0.4-gear-effects`, `v0.4.1-gear-display`, `v0.5-real-gear` (must ship first)
- Mobile pattern: existing GearGrid component (375px-verified)
