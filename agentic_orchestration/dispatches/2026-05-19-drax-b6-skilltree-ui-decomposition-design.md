# Design Dispatch — 2026-05-19 — drax — B6 Skill-Tree UI Surface Decomposition

**From:** drax (presentation seam)
**Authored:** 2026-05-19 (Phase 1 — design phase)
**Authority:** F4 autonomous; drax L1 in-seam; ladder to gandalf for register/respec open questions
**Companion commission:** `2026-05-19-drax-vs2a-b6-skilltree-ui-decomposition.md`
**Status:** DESIGN COMPLETE — prototype implementation follows in same session

---

## TL;DR

The B6 skill tree ships as a **tier-row layout with chain columns**: 4 horizontal tier rows (T1 Primaries → T4 Keystones) crossed by 2–4 thematic chain columns, rendered inside a `DrawerShell` on mobile and a full-width overlay on desktop. Tap-node → immediate-allocate flow with no confirmation dialog (revertible within session). Point pool shown at top. Node icons are **primitive + color-coded** for prototype; chierit/Pimen integration is post-prototype polish. The § 7 data contract is the central handoff to rocket + gamora S2.

---

## § 1 — Rendering shape decision

**Decision: Tier-row layout (hybrid of D2-style + Last Epoch per-skill node arrangement)**

### Options considered

| Shape | Pros | Cons | Genre examples |
|---|---|---|---|
| Vertical / PoE-style | ARPG-authentic; reads as big tree | Extremely wide mobile; hard to navigate without pan+zoom on phone | Path of Exile passive tree |
| Horizontal / D2-style | Multi-column, left-to-right; classic; readable at small width | Tier depth fights portrait orientation | Diablo II skill trees |
| Radial / D3-style | Visually striking; category sectors natural | Hard to extend; complicated parent/child traversal; pan gesture conflicts with scroll | Diablo III paragon (partial) |
| Hybrid collapsible / accordion | Mobile-first; compact | Loses the "tree" feel entirely; skills feel like a list | Various mobile ARPG menus |
| **Tier-row layout** (chosen) | Mobile-first; natural top→bottom progression; chain grouping is column-native; each tier is a row = scannable; parent-child arrows between rows are readable | Less visually spectacular than PoE; "grid" feeling rather than organic tree | Last Epoch, Grim Dawn devotion rows, Diablo IV paragon board |

### Rationale

Reincarnated's tree has a **defined structure** (B6 spec: 4 tiers, 2–4 chains, 10–15 skills total). This is not a 1,300-node passive sphere. The tree is intentionally small and legible — more Grim Dawn devotion or D4 paragon board than PoE passive. Mapping that structure to a tier-row layout preserves every design dimension:

- **Tier (vertical power axis)** → renders as horizontal row bands (T1 topmost, T4 bottommost)
- **Chain (thematic axis)** → renders as columns within each tier row
- **Parent-child unlock** → explicit arrow connectors between parent (row N) and child (row N+1); same column for same-chain; cross-column arrow for cross-chain unlock classes (multi-element classes)
- **Cross-chain unlock asymmetry** → arrow visibility: single-element classes show only same-column arrows (same-chain locks enforced visually); multi-element classes show cross-column arrows available

### Register coherence (HD-2D-shaped pixel-art)

The tier-row layout renders naturally in HD-2D register:
- Node circles/hexes are pixel-art-styled (flat fill + 1px pixel border + skill icon centered)
- Tier row labels ("Tier 1 — Primaries") in the project's existing typography + seasonTheme.accent tint
- Chain column headers LLM-named per class (per B6 spec: "Spark", "Inferno", etc.) — these names come from engine output; prototype uses placeholder names
- Connector lines between parent/child nodes: 1–2px lines, tinted by chain color palette
- Background panel: same `0x060f1c` dark fill as DrawerShell; chain column backgrounds subtly tinted per chain palette (alpha ~0.08 — readable without overwhelming)

The layout feels like a structured ARPG build board, not a spreadsheet. PoE's organic free-form tree is the genre high-bar; the tier-row form is the practical variant that works on a phone in portrait orientation.

---

## § 2 — Node icon strategy

**Decision: Primitive geometric icons (element-coded color + geometry-coded shape) for prototype; chierit/Pimen forward-flagged for post-prototype polish**

### Options and rationale

| Approach | Fit | Cost | Notes |
|---|---|---|---|
| chierit Elementals icons | Register-coherent; already in pipeline | Medium — requires extracting single frames, cropping to icon size | chierit per-archetype mapping decision not yet landed (gandalf flag); can't implement correctly without that decision |
| Pimen VFX frames as icons | High visual impact | High — Pimen frames are full-canvas VFX at 512+ px; extracting 44px node icons is lossy; frame-appropriate-moment selection required | Forward-flag for post-prototype only |
| Primitive geometric + element color | Instant; register-coherent at small size; unambiguous visual encoding | Zero | Proven ARPG convention: PoE gem icons; D4 paragon node shapes |
| Hybrid primitive + named-node-specific art | Best of both | Medium/high | Natural future state: T3/T4 nodes get chierit/Pimen treatment; T1/T2 stay primitive |

**Chosen: primitive geometric with element-coded color + tier-coded shape.**

Node shape by tier:
- T1 (Primaries): circle, 40px diameter
- T2 (Mids): square/diamond, 40px
- T3 (Advanced): hexagon, 44px
- T4 (Keystones): large hexagon or star, 52px

Node fill: element color palette derived from existing `SEASON_THEMES` + element color conventions already used in HUD (resource globe colors, VFX tints). Element color is per-chain (each chain has one primary element; node fill = that element's accent color at 60% saturation for locked state, full saturation for unlocked, +bright border for available-to-unlock).

Node state encoding:
- **Locked** (prerequisite not met): dark fill, no border glow, greyed label
- **Available** (prerequisite met, no points spent): element accent border glow, dim fill, label at half-alpha
- **Allocated** (points spent, 1–N ranks): bright fill, rank count displayed inside node, gold border glow proportional to rank
- **Maxed** (rank cap reached): full bright fill + white inner highlight ring

// TODO(drax): replace primitive icons with chierit per-archetype icons when chierit per-archetype mapping lands (gandalf design watch-item, `canonical/16-project-roadmap.md` § VS2a). Likely T3/T4 nodes first; T1/T2 can retain primitive.
// TODO(drax): replace T3/T4 node icons with Pimen VFX frames (cropped to icon canvas) when C4 Pimen pipeline ships full catalogue.

---

## § 3 — Unlock-feedback affordance

**Decision: Immediate visual state change + brief color burst + rank counter animation. No audio (deferred per audio-strategy-phase0.md).**

### Affordance chain on tap-to-allocate

1. **Tap → immediate state transition**: node fill transitions from "available" to "allocated rank 1" (or rank N+1 if re-tapping). No delay; no spinner. The visual state change IS the feedback.
2. **Color burst**: radial circle particle-lite effect — 6–8 small squares (px-art style) emanating outward from node center, fading over ~0.3s. Implemented with a Graphics-based particle pool (no Pimen VFX for prototype — the burst is 6 Graphics rectangles animated via Ticker). Element-colored squares. Functional on mobile (no GPU-heavy effect).
3. **Rank counter pop**: rank count text inside node scales up 1.0→1.3→1.0 over 0.2s (scale pop). Simple Ticker tween.
4. **Edge traversal animation**: if this allocation unlocks a child node in the tier below (rank threshold met), the connector line to that child node pulses from grey to element-accent over 0.4s. This is the "propagation feels alive" signal — the tree responds to investment.
5. **Point pool counter decrements**: the point pool display at the top of the panel decrements by 1, with same scale-pop.

### No confirmation modal

Tap-to-allocate is immediate. No "Are you sure?" dialog. Mobile-first rationale: confirmation dialogs on mobile ARPGs are friction. PoE mobile, Last Epoch mobile, D4 mobile all use immediate allocation. Respec provides the safety net (§ 6).

### Insufficient points feedback

If player taps an available node with 0 points in pool: node shakes (±4px horizontal oscillation, 3 cycles, 0.25s total), pool counter shakes in sync, no point deducted. Standard mobile "shake = can't do that" affordance.

---

## § 4 — Mobile-first sizing

**Decision: Minimum 88px CSS touch target; tree renders at fixed logical canvas size, scales per viewport.**

### Touch target sizing

Per existing project convention (`typography.ts` `hitR()` function): `hitR(88)` = 88 CSS px centroid target at 375px viewport. In canvas space on mobile (375px viewport → 1800px landscape canvas → 4.8× ratio): `hitR(88) = 88 × 4.8 = 422 canvas-space px` as the hit zone radius.

Node visual sizes (canvas space):
- T1/T2 node visual diameter: 80px canvas (= 16.7 CSS px on mobile — intentionally smaller visual; actual hit zone extended)
- T3/T4 node visual diameter: 96px canvas
- Hit zone radius on ALL nodes: `hitR(44)` = 211 canvas-space px (44px CSS centroid for HIG guideline; extended to `hitR(44)` per existing `hitR` convention)

Wait — correction: node visual is small (80–96 canvas px); but the tap target must be larger. Using `hitR(44)` = 211px canvas hit radius means nodes could overlap in a dense grid. Tree layout accounts for this: minimum node center-to-center spacing = `hitR(44) * 2 = 422px` canvas in both axes. At 1800px canvas width with 4 chains: 1800/4 = 450px per chain column — tight but sufficient. Portrait (944px canvas width): 944/4 = 236px per chain column — marginal at 4 chains. At 3 chains: 944/3 = 315px — comfortable.

Portrait constraint: for 4-chain classes, portrait mode uses a 2×2 sub-grid layout (2 chains per row, 2 rows of chains) rather than 4-column single-row. Single-element classes (2 chains) are always comfortable in portrait.

### Scroll vs zoom

No zoom interaction for prototype. The full tree fits within the DrawerShell content area (55% canvas height) for any class because the tree is designed to be small (10–15 skills, 4 tiers = 4 rows). Scroll: if tree height exceeds drawer content area, vertical scroll within the content area (Pixi Container mask + pointer-drag). For prototype, assume tree fits without scroll for all classes in the fixed tier-row layout.

### Canvas geometry

The tree panel renders inside DrawerShell (mobile) or a centered modal of width 900px, height 600px (desktop), matching the existing desktop modal pattern from `inventoryPanel.ts` / `characterSheet.ts`.

---

## § 5 — Tap-to-allocate UX

**Decision: Tap node → spend point → immediate unlock (single-tap allocate). Long-press → skill detail overlay.**

### Interaction taxonomy

| Gesture | Result |
|---|---|
| Single tap on available node (points > 0) | Allocate 1 rank immediately; feedback per § 3 |
| Single tap on available node (points = 0) | Shake feedback; no allocation |
| Single tap on locked node | Shake feedback + brief tooltip showing "Requires X ranks in [parent skill name]" |
| Single tap on allocated node (not maxed) | Allocate 1 more rank (same flow) |
| Single tap on maxed node | No effect; brief "Maxed" flash on node |
| Long press (>400ms, per `inventoryPanel.ts` LONG_PRESS_MS convention) on any node | Show skill detail overlay (effect description, current rank, max rank, scaling per rank) |
| Swipe down on drawer | Close drawer per DrawerShell convention |
| Tap backdrop above drawer | Close drawer per DrawerShell convention |

**No drag-to-allocate**: drag is used for scroll (if needed) and swipe-dismiss; conflates gestures on mobile.

**No double-tap**: double-tap is a browser zoom gesture on mobile; never use for allocation.

**Single-tap = single-rank**: each tap allocates exactly 1 rank. To reach rank 5 on a node, the player taps 5 times. This is intentional — it keeps the allocation feel deliberate and tactile without a numeric picker. PoE gem upgrade and Last Epoch node allocation both use single-click-per-rank or explicit +/- controls. The tap-per-rank approach is simpler for prototype.

### Skill detail overlay

Long-press fires a tooltip-style overlay (same pattern as `inventoryPanel.ts` `_addLongPress`):
- Positioned above the tapped node (or below if near top of drawer)
- Contains: skill name, current rank, max rank, effect at current rank, effect at next rank (if not maxed), unlock requirement (parent + rank threshold)
- Dismisses on tap elsewhere

---

## § 6 — Point-allocation visualization + undo/respec semantics

### Point pool visualization

Top of the tree panel, full width:

```
SKILL POINTS: [3] available  [12 / 15] allocated
```

- "3 available" = unspent points (large number, accent color)
- "12 / 15 allocated" = spent / total earned (smaller, muted)
- Both decrement/increment in real-time as player allocates
- At 0 available: pool counter shown in grey; tap-on-node fires shake feedback

### Node state visual legend

Bottom of the tree panel (or a brief inline legend in the header area):
- Small colored node sample: Locked | Available | Allocated | Maxed
- 1-line legend per state

### Undo / respec semantics

**Prototype default: free per-node undo within current session. Respec of full tree: free per session, does not persist past session close.**

Rationale:
- Respec cost economics is explicitly deferred to gandalf (B6 spec territory); prototype cannot presuppose a cost mechanic
- Free per-session respec is the lowest-friction prototype default; it lets players explore the tree without penalty during the VS2a playtest
- Per-node undo (tap the same node again to un-allocate the last rank) is the minimum viable undo affordance

**Implementation of per-node undo:**
- Single tap on an already-allocated node: if rank > 0, show "Tap again to remove 1 rank" micro-overlay (1s duration) — prevents accidental de-allocation
- Second tap within 1s window: de-allocate 1 rank; point returned to pool; node state reverts accordingly

**Full respec:**
- "Reset tree" button at the bottom of the tree panel
- Returns all allocated ranks to the pool
- No confirmation modal (respec is free in prototype; no loss to confirm)
- Button label: "Reset All"

**Cross-session persistence:**
- In prototype: tree allocation state persists in-memory only (per `SkillTreePanel` instance lifecycle). When character switches or session ends, state is discarded.
- Forward-flag: when engine S2 ships real data and player-save layer exists, tree allocation will serialize to localStorage with key `skill_tree_alloc_{class_id}_{season_id}`. Schema: `{ skills: { [skillId]: number } }` (rank per skill).

// TODO(drax): wire full respec semantics when gandalf closes respec-cost design (B6 spec territory). Remove "Reset All" free-respec button and replace with engine-defined respec cost mechanic at that time. Track in AGENT_STATE.md.
// TODO(drax): localStorage persistence when player-save layer exists in demo (currently no cross-session state).

**Gandalf consult queued via hive log:** respec semantic choice surfaced — prototype is free-per-session. If gandalf has a prior decision on respec cost or scope that I've missed, amend prototype assumption at that point.

---

## § 7 — Data contract with engine (rocket + gamora S2 handoff)

This is the **canonical contract drax needs from rocket + gamora's S2 main work**. Surface in hive log for S2 dispatch consumption.

### Season-output JSON location

The skill tree data for each class should live under the class record in the per-season class manifest. Proposed path:

```
season_XXXXXX/
  classes/
    {class_id}/
      manifest.json   ← class record; skill tree root attached here
```

Or within the existing season export format, the `ClassData` object gets a `skill_tree` field.

### Per-class tree object: `SkillTree`

```jsonc
{
  "skill_tree": {
    "class_id": "fire_mage",
    "element_distribution": "single",   // "single" | "multi" — governs cross-chain unlock rules
    "chains": [
      {
        "chain_id": "spark",
        "label": "Spark Chain",           // LLM-named
        "element": "fire",                // primary element of this chain
        "palette_hex": "#ff4422",         // chain color; used for node tint + connector line
        "skills": [/* see SkillNode below */]
      }
    ],
    "cross_chain_unlock": "strict"        // "strict" (single-element) | "permissive" (multi-element)
  }
}
```

### Per-skill node: `SkillNode`

```jsonc
{
  "skill_id": "spark_bolt",
  "name": "Spark Bolt",             // LLM-named
  "chain_id": "spark",
  "tier": 1,                        // 1–4
  "chain_position": 0,              // 0-indexed position within chain at this tier
  "parent_skill_ids": [],           // empty for Tier 1; list of parent skill_ids for Tier 2+
  "rank_unlock_threshold": 0,       // ranks required in parent(s) to unlock this node (0 for T1)
  "rank_cap": 5,                    // max ranks (varies per tier: T1=5 soft, T4=3 typical)
  "rank_cap_formula": "min(15, floor(level/3.33))",  // optional; if present, rank_cap is level-gated
  "scaling_coefficient": 1.06,      // per-rank power multiplier (T1: 1.05-1.08)
  "effects": [
    {
      "type": "damage",             // type of effect
      "base_value": 45,             // base at rank 1
      "per_rank_delta": 4           // per-rank increase (or use scaling_coefficient × base)
    }
  ],
  "energy_cost": 12,
  "cooldown_seconds": 1.5,
  "geometry_type": "cone",          // from F1 schema field
  "range_m": 8.5,                   // from R3 schema field
  "icon_hint": "fire_cone_basic",   // optional; used to pick chierit/Pimen icon when available
  "archetype_tag": "fire_mage"      // for cross-reference + future filtering
}
```

### Point budget

The engine should emit the player's current point budget alongside the tree, OR drax derives it from level. Preferred: engine emits `skill_points_available: number` on the character/class record alongside `skill_points_spent: number`. If the engine doesn't emit this, drax derives `skill_points_available = floor(level / 2)` as a default until the real formula ships.

### Fixture shape for prototype

Until S2 ships, drax uses a local fixture file at `src/ui/skillTree/fixtures/sampleTree.ts`. The fixture conforms to the schema above. It represents a fire_mage with 2 chains × 4 tiers (8 nodes), single-element strict-chain-unlock rule.

### What drax does NOT need from the engine

- Respec cost economics — UI uses free-respec until gandalf lands B6 spec cost mechanic
- Rank cap per player level — UI uses `rank_cap` from the node; `rank_cap_formula` is advisory; UI enforces via `min(rank_cap, actual_rank)` comparison at level-load time
- Chain-palette generation — UI derives palette from `palette_hex` per chain; no engine-side color computation needed

---

## § 8 — Scope phasing

### F4 prototype ship-line (what ships in this session)

| Feature | Ship in F4? |
|---|---|
| Tier-row layout with chain columns | YES |
| Node state encoding (locked / available / allocated / maxed) | YES |
| Tap-to-allocate (single-rank per tap) | YES |
| Long-press skill detail overlay | YES |
| Point pool display (available + allocated / total) | YES |
| Color burst unlock feedback | YES |
| Rank counter pop animation | YES |
| Edge traversal pulse on child unlock | YES |
| Node shake on insufficient-points tap | YES |
| Per-node undo (double-tap within 1s) | YES |
| Free full respec ("Reset All" button) | YES |
| Mobile + desktop responsive (DrawerShell + desktop modal) | YES |
| Placeholder data fixture (fire_mage sample tree) | YES |
| TypeScript build clean, no console errors | YES |
| Portrait 2×2 chain sub-grid for 4-chain classes | YES |

### Post-F4 polish (not in this session)

| Feature | Deferral reason |
|---|---|
| chierit per-archetype icons on nodes | gandalf chierit mapping decision not yet landed |
| Pimen VFX for node-unlock affordance | C4 Pimen pipeline not complete |
| Audio cue on unlock | Deferred per `audio-strategy-phase0.md` (Phase 1+) |
| Respec cost UX | Gandalf B6 spec territory; free-respec in prototype |
| Season-themed chain palette variations | Nominal — season theme already applied via `getSeasonTheme()`; full LLM-named palettes pending S2 |
| Cross-session localStorage persistence | Player-save layer not yet designed |
| S2 engine data consumption (replace fixture) | Gated on rocket + gamora S2 dispatch + MIGRATION.md |
| Animated chain-reveal intro | Nice-to-have; no blocking reason other than scope |
| Spirit Guide tree recommendation overlay | Stage A3 scope (B9 series, Spirit Guide build coach) |

### F4 acceptance criteria (per commission dispatch)

- [ ] `src/ui/skillTree/skillTreePanel.ts` exists and builds without error
- [ ] `src/ui/skillTree/fixtures/sampleTree.ts` fixture in contract-compliant shape
- [ ] Panel renders in DrawerShell (mobile) and desktop modal
- [ ] Tap-to-allocate works with all node states
- [ ] Point pool decrements correctly
- [ ] Unlock-feedback affordances (burst, pop, edge pulse) visible
- [ ] `tsc --noEmit` clean + `npm run build` 0 errors
- [ ] Demo launches, renders one frame without console errors (smoke)

---

## Open questions surfaced (routed per authority)

### For gandalf (via hive log — L2 design consult)

1. **Respec semantics**: prototype assumes free-per-session. If B6 spec has landed a respec-cost decision I haven't seen, please surface via hive log so I can amend prototype assumption.
2. **chierit per-archetype mapping**: dispatch noted as parallel-to-F4, not-gating-F4. When decision lands, I integrate. No change to prototype timeline.

### L1 drax decisions (already made above, per autonomous authority)

- Rendering shape: tier-row layout — DECIDED
- Node icon strategy: primitive geometric for prototype — DECIDED
- Unlock-feedback: color burst + rank pop + edge pulse — DECIDED
- Mobile-first sizing: hitR(44) canvas-space touch zone — DECIDED
- Tap-to-allocate: single-tap single-rank immediate — DECIDED
- Respec semantics: free per-session — DECIDED (with TODO for gandalf follow-on)
- Data contract field set — DECIDED per § 7

---

*Authored 2026-05-19 by drax. Phase 1 complete. Phase 2 (prototype implementation) follows immediately.*
