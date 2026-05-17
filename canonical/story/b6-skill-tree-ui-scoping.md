# B6 Skill-Tree UI Scoping Spec

**Status:** Canonical-story design spec. Authored 2026-05-16 (Day 4 close) by gandalf at Matt's authorization. Locks the visual shape, node states, unlock-gate visualization, and implementation expectations for B6's player-facing skill-tree surface. Scoped to VS2a read-only ship + forward-compat hooks for Stage A3 player-controlled SP allocation.

**Why this spec exists.** Per P6 forward audit § B6 (CRITICAL severity), the engine will emit tree-shaped data via B6 schema fields (`tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`) and the demo has no surface to render that data. Without this spec, drax improvises a tree shape under VS2a ship pressure; the result drifts from B6 engine semantics (Discipline #13a risk) and the playtest signal on skill-tree UI comprehensibility (Playtest Cycle 1 criterion) becomes invalid.

**What this spec is.** A design lock on tree shape + visual conventions that lets drax implement concurrent with gamora's B6 engine work rather than sequential after. Saves ~2-3 weeks on VS2a critical path.

**What this spec is NOT.**
- Not an implementation plan (drax owns implementation details)
- Not a code-level component spec (no React/Pixi.js prescriptions)
- Not a binding lock on SP allocation interaction (Stage A3 territory; this spec only covers read-only-with-forward-compat-hooks for VS2a)
- Not Spirit Guide build-coach UI (Stage A7 territory)

**Companion docs:**
- `canonical/story/style-register.md` — HD-2D-shaped pixel-art register; constrains visual approach
- `canonical/story/court-of-forms.md` — Court framing + 8 structural commitments
- `canonical/story/embodiment-narrative-layer.md` — embodiment-as-narrative-skin (relevant for per-class tree visual identity)
- `canonical/16-project-roadmap.md` § VS2a — sequencing context
- `canonical/16-project-roadmap.md` § Stage A3 — B9 series where SP allocation interaction lands

**Predecessor design locks honored:**
- B6 templates (Stage A1; commit 4f5cd93) — 14 archetypes with kit size / AOE share / chain count + depth / cross-chain rule / required roles
- B6 forward-compat schema fields (Stage A1; commit 1aa99b5) — `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- B9 endgame baseline (locked) — level 50, 120-point skill budget, per-skill cap 15, kit size 10-15
- Hierarchical unlock gates (per file 32 / 33) — ≥3 ranks tier-1 unlocks tier-2; ≥5 unlocks tier-3; ≥8 unlocks tier-4
- B9c reset model — strict during play, paid endgame
- Trait floors 1/12/25/38 (file 32 Section 4) — relevant context; traits render adjacent to skill tree in Stage A3

---

## 1. Strategic frame — what the player experiences

The skill tree is **the player's relationship to their incarnated form, made visible.** When a player levels up, the tree is where they encounter the structural reality of what their class IS — not just "a fire warrior" but a specific shape of capability with branching specializations and earned depth.

### Genre precedent — what we are and what we are not

**Reference shape: Last Epoch's base-skill specialization tree.** Per-skill 3-tier branching with clear unlock gates. NOT Last Epoch's broader passive tree (too vast for our scale); not PoE's tree (way too vast); not Diablo II's three-column-per-class (too simple for our hierarchical-with-cross-chain structure); not Diablo IV's paragon board (too complex; assumes endgame grind we don't have).

**Why Last Epoch specialization shape:**
- Fits on one screen at desktop AND mobile
- Visual hierarchy (tier rows) reads instantly
- Branching is meaningful (each branch makes a different build)
- Per-skill rank investment is the unit of progression (matches our per-skill cap 15)
- Cross-branch unlocks are visible and earnable

**What we add beyond Last Epoch specialization:** cross-chain rules per B6 templates (same-element strict vs multi-element flexible) — these become visible "bridges" between chains.

### What this is NOT trying to be

- **Not the player's seasonal-identity canvas** — that's the Court of Forms layer and Loadout's per-class portrait + narrative beat. Skill tree is the *mechanical* face of class identity, not the *narrative* face.
- **Not a build planner** — Stage A3 ships the build-coach (Spirit Guide marginal-value analysis). VS2a's tree is read-only; the engine has already chosen the optimal allocation per band via B14 multi-band convergence.
- **Not a discoverable mystery** — every node is visible from L1. Locked nodes are clearly locked (not hidden, not greyed-into-obscurity). Players plan ahead; they don't fog-of-war their own progression.

---

## 2. Tree shape — visual structure

### 2.1 Layout

**Vertical tier-rows; horizontal chain-columns.** Tier 1 at the top; Tier 4 at the bottom (descending = deepening commitment, matching the "seasonal descent" cosmology framing per `cosmology-reincarnated.md`).

```
              CHAIN A           CHAIN B           CHAIN C
            (e.g. Cinder)    (e.g. Hearth)     (e.g. Ember)

  TIER 1     [N] — [N] — [N]   [N] — [N]         [N] — [N] — [N]
              │  ╲ │  ╲ │       │  ╲ │             │  ╲ │  ╲ │
  TIER 2     [N] — [N]         [N] — [N] — [N]   [N] — [N]
              │     │           │     │  ╲ │       │     │
  TIER 3     [N] — [N]         [N] — [N]         [N]
              │                 │                 │
  TIER 4              [N — capstone]                 [N — capstone]
                                       ╲          ╱
                                  (cross-chain bridge if rules permit)
```

- **Tier row** = horizontal band. All Tier-1 skills share a row; all Tier-2 share the next; etc.
- **Chain column** = vertical cluster within the row. A chain's skills sit together visually.
- **Connector lines** = parent-skill relationship (`parent_skill_ids` schema field). Solid line within-chain; thinner / dashed line for cross-chain.
- **Cross-chain bridge** = explicit visual element where B6 template allows cross-chain unlock. Renders as a connector between chains, gated by unlock condition (see § 5).

### 2.2 Per-archetype chain count

B6 templates specify chain count + depth per archetype (commit 4f5cd93). Examples:
- **Single-element mage** — 2-3 chains, all same element, deep specialization (4-tier depth)
- **Multi-element controller** — 3-4 chains, cross-element, moderate depth
- **Hybrid mage** — 3 chains, two elements, asymmetric depth
- **Hunter** — 3 chains, physical + 1-2 elements, balanced

**The chain count drives column count.** A 2-chain class has a narrower tree than a 4-chain class. Mobile responsiveness handles this by adjusting column widths, not by scrolling — the whole tree must fit one screen at all breakpoints (see § 9).

### 2.3 Tier-row vs chain-column emphasis

**Tier rows are the dominant visual axis.** A glance at the tree reads "what tier am I working on" before "what chain am I committed to." This matches the hierarchical-unlock-gate gameplay: tier-1 ranks are what gate tier-2 access; tier is the temporal axis of progression.

Convention:
- Tier rows visually separated by faint horizontal bands (alternating background tint)
- Tier number labeled at far-left of each row ("T1", "T2", "T3", "T4")
- Chain columns visually grouped by chain header at the top ("Cinder", "Hearth", "Ember") — chain names per-season per L3 vocabulary

---

## 3. Node states — five visual states

Each node (skill) renders in one of five states. Drax owns the exact palette/styling within style-register coherence; the spec locks the *distinction* between states.

| State | Meaning | Visual convention |
|---|---|---|
| **LOCKED** | Tier prerequisite not met (player hasn't earned ≥N tier-prev ranks) OR cross-chain rule not satisfied | Dimmed; lock icon overlay; faint connector lines to it |
| **AVAILABLE** | Prerequisites met; not yet allocated; player COULD spend SP here (Stage A3+) | Full opacity; subtle pulse or glow; standard connector lines |
| **ALLOCATED** | Player has ≥1 rank in this skill; not yet maxed | Full opacity + rank pip count ("3/15"); slight border emphasis |
| **MAXED** | Player has 15 ranks (per-skill cap) | Full opacity + "MAX" badge replaces rank pips; capstone-style border |
| **NOT-ON-PATH** | Skill in another chain that current chain choices have made unreachable (cross-chain rules) | Greyed but not lock-iconed; visible but de-emphasized |

**Why NOT-ON-PATH is distinct from LOCKED.** LOCKED means "you haven't earned this yet." NOT-ON-PATH means "given your current investments, the rules say this isn't reachable from here." Different player consequence; different visual.

**VS2a state coverage.** VS2a ships read-only with engine-chosen allocation. Players will see ALLOCATED + MAXED for nodes the engine picked; AVAILABLE for nodes the engine could have picked but didn't (Spirit Guide build-coach commentary in Stage A7 explains why); LOCKED for nodes the engine couldn't reach at current level. NOT-ON-PATH may not surface in VS2a if engine never picks contradictory paths.

---

## 4. Node visual anatomy

Each node renders as a card-like element with consistent anatomy across states:

```
   ┌─────────────┐
   │  [ICON]     │ ← node icon (see § 6)
   │             │
   │  Skill Name │ ← per-season vocabulary (L3); falls back to canonical at VS2a
   │  3/15  ▮▮▮  │ ← rank pip count + rank-investment bar
   └─────────────┘
```

- **Icon** — § 6 strategy
- **Name** — per-season vocabulary from L3 (post-Stage-3 cipher migration); falls back to canonical-four naming at VS2a since Stage 3 has not yet shipped
- **Rank pips** — "current/max" numeric + visual bar; bar fills as rank increases
- **Hover/tap target** — entire node card is the interaction surface

**Mobile size:** node card minimum 48×48 px (touch-friendly hit target per WCAG 2.5.5 Level AAA). Desktop default ~80×80 px with hover affordances.

---

## 5. Unlock-gate visualization

The hierarchical unlock gates (≥3 ranks tier-1 unlocks tier-2; ≥5 unlocks tier-3; ≥8 unlocks tier-4) need a clear visual surface. Player must be able to see at a glance: "I have 2 ranks in tier 1; one more rank and tier 2 opens."

### 5.1 Tier-unlock indicator

Each tier row has a **tier-unlock indicator** at its left edge showing:
- Current count: "2 / 3 ranks in T1"
- Status: locked / will-unlock-with-next-allocation / unlocked
- Visual progress: bar or pip cluster filling toward unlock threshold

### 5.2 Cross-chain bridge visualization

Cross-chain rules per B6 template specify whether unlock can flow across chains and under what conditions (single-element strict = no cross-chain; multi-element flexible = cross-chain allowed at specific gate ranks).

**Visual convention:**
- **Single-element-strict archetype** — chains visually isolated; no cross-chain connectors rendered (zero implication of crossing)
- **Multi-element-flexible archetype** — chains visually connected via faint bridge connectors; bridges render LOCKED until cross-chain gate ranks are met; UNLOCK on threshold

The bridge connector becomes a **deliberate design object** — its presence/absence per-class is itself information about class identity. A controller seeing "I have bridges between my elements" understands they're playing a hybrid; a single-element mage seeing "no bridges" understands they're playing a specialist.

### 5.3 Unlock-feedback affordance

When player allocates a rank that triggers a tier unlock or cross-chain bridge unlock:

- **Brief flash** on the newly-unlocked tier/bridge (~300ms)
- **Audio cue** (post-Phase-1; deferred per `audio-strategy-phase0.md`)
- **One-line caption** at top of tree: "Tier 2 unlocked — Hearth chain available"

**Convention:** the flash is brief, readable, and does NOT block input. Reference: Diablo's level-up flash. Small, clear, doesn't interrupt play.

---

## 6. Node icon strategy

### VS2a — placeholder-procedural

**Default for VS2a ship:** procedural placeholder icons. Per-node visual = named glyph + tier color + chain accent.

Convention:
- **Named glyph** — drax-procedural based on skill geometry type (projectile / cone / area / etc.) — small library of ~10 abstract glyph shapes
- **Tier color** — Tier 1 → bronze; Tier 2 → silver; Tier 3 → gold; Tier 4 → iridescent / animated. Matches Diablo's tier-as-color convention.
- **Chain accent** — small color band per chain (chain A = warm red; chain B = cool blue; chain C = green). Per-class assigned by engine; drax-rendered.

**Why placeholder for VS2a:** commissioning per-skill icons across 14 archetypes × 10-15 skills = 150+ custom icons. Not viable for VS2a budget or timeline. Procedural placeholders are register-coherent (HD-2D-shaped pixel-art achievable in code) and give playtest signal on tree comprehensibility without binding asset spend.

### Stage A2 closeout — per-skill icons

When B11 VFX integration matures and Pimen catalogue full integration is operational, commission per-skill icons from the same vendor for register coherence. Estimated ~150 icons; per-icon cost manageable when bundled with VFX commission.

### Why not commission icons NOW

- Drax bandwidth is the binding constraint (Risk-1, locked in roadmap)
- Per-season vocabulary is not yet shipping (Stage 3 cipher migration pending) — icon names would have to be canonical-four-coded, which violates the substrate-realignment direction
- Playtest Cycle 1 validates *tree comprehensibility* not *icon polish* — placeholder icons are the right fidelity for that signal

---

## 7. Tooltip design

Hover (desktop) or tap-hold (mobile) on a node opens a tooltip with:

```
┌─────────────────────────────┐
│ [Skill Name]                │ ← bold; per-season L3 vocabulary
│ Tier 2 · Chain: Hearth      │ ← chain context
├─────────────────────────────┤
│ Rank 3 / 15                 │ ← current rank
│ 245 damage / 8 mana / 1.4s  │ ← current rank stats
├─────────────────────────────┤
│ Next rank: 268 damage       │ ← preview of rank +1
│ +5% per rank cooldown reduce│
├─────────────────────────────┤
│ Locked: needs 5 total ranks │ ← only if LOCKED state
│ in Tier 1 before allocating │
└─────────────────────────────┘
```

**Convention:**
- Current-rank stats shown plainly
- Next-rank preview shown explicitly (the "+X" delta + the new absolute value)
- Lock-reason explained in plain language (not just "locked"; tell the player WHY)
- Spirit Guide build-coach commentary slot — reserved blank in VS2a; populated in Stage A7 with "Strong/Solid/Marginal/Sidegrade/Downgrade" verdict

**Length cap:** tooltip ≤ 200 visible characters in body content. Long mechanics descriptions live in a separate "details" expansion (tap "?" icon).

---

## 8. SP not yet a player choice — VS2a read-only with forward-compat

### VS2a ships read-only

The tree is fully rendered with the **engine-chosen optimal allocation** per band (engine computes via B14 multi-band convergence post-VS2a; VS2a ships pre-B14 with engine-chosen per-fight allocation as the default). Player cannot click to allocate; the tree is informational only.

**Why ship read-only:** SP allocation interaction belongs to Stage A3 (B9b). Forcing player choice in VS2a without the B14 build-coach math layer means players make choices the engine can't evaluate — bad playtest signal.

### Forward-compat hooks drax must include

So Stage A3 doesn't re-implement the surface:

1. **Click-handler stubs on nodes** — wired to a no-op in VS2a; Stage A3 wires to allocation logic
2. **SP-pool HUD slot** — rendered at top of tree but shows "auto" in VS2a; Stage A3 shows "23 / 47 SP remaining"
3. **Available-state visual** — already in § 3 state list; ensures Stage A3 can flip nodes from ALLOCATED-as-engine-default to AVAILABLE-for-player-choice without re-styling
4. **Reset-button slot** — rendered placeholder in VS2a; Stage A3 wires to B9c reset mechanism

### What VS2a explicitly does NOT include

- Player click-to-allocate
- Spirit Guide build-coach Strong/Solid/Marginal/Sidegrade/Downgrade
- Build-reset interaction
- Spirit Guide proactive act-transition reset recommendation
- Trait display (B9a; Stage A3 — renders adjacent to skill tree, separate surface)
- Multi-band optimal-vs-current comparison (B14 + Stage A7)

---

## 9. Mobile + accessibility

### Mobile responsiveness

- **One-screen rule:** entire tree fits one screen at mobile breakpoint (320px width minimum). No scrolling within the tree surface; pinch-zoom permitted for fine inspection.
- **Adjusted node spacing:** mobile nodes pack tighter; connectors thinner; tier labels abbreviated ("T1" vs "Tier 1").
- **Hit targets:** 48×48 px minimum per WCAG 2.5.5 AAA.

### Accessibility

- **Color is not the only differentiator** — tier color is reinforced by tier-number label; chain accent reinforced by chain-name header
- **Locked-state lock icon** explicit (not just dimmed; icon makes state legible at low contrast)
- **Tooltip text** screen-reader accessible; tab navigation supported
- **Keyboard navigation** — arrow keys move between nodes; Enter opens tooltip; Esc closes

### Style-register alignment

HD-2D-shaped pixel-art register per `style-register.md`:
- Procedural icon glyphs render in pixel-art-coherent style (chunky pixel edges; limited palette; intentional pixel-art aesthetic NOT vector approximation)
- Connector lines: 1-2 px pixel-art-edged (not anti-aliased curves)
- Tier-row background tints: subtle; pixel-coherent
- Hover/unlock flashes: pixel-art shimmer not glow-effect blur

---

## 10. What drax needs from engine emission

Confirm with rocket (B6 pre-work) + gamora (B6 main) that the following fields populate reliably per skill:

| Field | Source | Use |
|---|---|---|
| `tier` (1-4) | B6 main | Tier-row placement |
| `chain_id` | B6 main | Chain-column placement |
| `chain_position` | B6 main | Within-chain ordering |
| `parent_skill_ids` | B6 main | Connector lines |
| `scaling_coefficient` | B6 main | Per-rank stat scaling for tooltip preview |
| `cross_chain_rule` (per-class) | B6 templates | Bridge rendering convention (strict vs flexible) |
| `unlock_gate_thresholds` (per-tier) | B6 main | Tier-unlock indicator math |
| `skill_name_per_season` | Stage 3 cipher migration | Display name (falls back to canonical at VS2a) |
| `skill_icon_hint` (geometry type) | existing schema | Procedural icon glyph selection |
| `current_rank` | engine-chosen allocation (VS2a) → player allocation (Stage A3) | Rank pip count |
| `max_rank` (= 15 per B9 lock) | static | Per-skill cap |

**If any field is missing or unreliable at B6 ship time, drax surfaces to knight-rider; do NOT improvise.** Discipline #13a (implementation-vs-intent drift) — placeholder fields invented in demo become locked-in by playtest signal and drift the engine spec.

### 10.1 Stage B export-DTO forward-compat protection (added 2026-05-16 Day 4 close)

Per finding `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md` (Pattern P7 #3 silent-drop instance): engine-side schema fields can be silently dropped at the Stage B export-DTO boundary (`ExportClass` / `ExportMonster` / `ExportSkill` constructors in `season_exporter.py`) before reaching the demo-facing consolidated JSON.

**The 11 fields in § 10 above are individually vulnerable to this drop pattern.** When B6 main ships and emits real `tier` / `chain_id` / `chain_position` / `parent_skill_ids` / `scaling_coefficient` / `cross_chain_rule` / `unlock_gate_thresholds` values, they will silently drop at Stage B unless:

1. **`ExportSkill(...)` constructor** in `season_exporter.py` is extended to pull all the new fields explicitly OR converted to a model-driven approach
2. **Stage B export-boundary validator** (analogous to Stage A's `_REQUIRED_CLASS_KEYS` in `season_writer.py:322-333`) is added to enumerate the required skill fields

**Required precondition for B6 ship:** the star-lord Track A dispatch per commission `2026-05-16-star-lord-export-dto-stage-b-fix-and-r11b.md` MUST land before B6 main ships, OR knight-rider authors a complementary dispatch that extends `ExportSkill` to include the B6 fields specifically.

**Drax verification on first B6-emitting season:** after B6 main lands + first regen, run `grep -c "\"tier\"" exports/<season_id>/classes.json` — count should equal `(number of classes) × (skills per class)`. If 0, Stage B drop fires; surface to knight-rider before further demo implementation.

This is the same kind of forward-compat protection the B6 schema fields had in Stage A1 (commit `1aa99b5`). The Stage A→B boundary is the gap the Pattern-P7 finding closed; B6 ship is the first major regen-cycle event after the finding lands.

---

## 11. Open questions for drax

Things drax should call back on after first pass:

1. **Chain header naming** — VS2a ships pre-Stage-3 cipher migration; chain headers can either show canonical-four-coded names ("Cinder Chain") or generic labels ("Chain A / B / C"). Recommend canonical names since the player needs *some* identity hook; per-season L3 vocabulary lands at Stage 3.
2. **Bridge connector animation** — when cross-chain bridge unlocks, is the connector a static reveal or animated (line drawing toward target chain)? Recommend static reveal for VS2a; revisit if playtest signal demands more game-feel.
3. **Per-archetype tree visual identity** — should the tree itself look different per class (e.g., warm palette for fire-element class, cool for water)? Recommend YES via chain accent colors but NOT via tier color (tier color stays universal for cross-class legibility). Subtle differentiation; not heavy theming.
4. **Tier-4 capstone treatment** — Tier 4 typically has 1-2 nodes (the deepest commitments). Should capstones render visually distinct (larger node? gilded border?) to telegraph their weight? Recommend YES — slight size increase + capstone border. Reference: Last Epoch's specialization capstone has visible weight.
5. **Empty-chain handling** — if a class has a 2-chain tree with a 3-chain layout slot, does the empty slot render blank or collapse? Recommend collapse (responsive width) for visual cleanliness.

---

## 12. Implementation cascade

### Immediate (no engine dependency)

- Drax can begin component scaffolding NOW against this spec: tree layout component, node component, tier-unlock indicator, tooltip component, mobile-responsive grid
- Procedural icon glyph library can be authored now (~10 glyphs)
- Style-register sample colors / connectors / tier tints can be finalized now

### Gated on B6 engine ship

- Wiring engine emission fields to render
- Engine-chosen optimal allocation as the rank-state source
- Per-archetype tree shape validation (does the engine actually emit a 3-chain hunter tree as templates promised?)

### Gated on later stages

- Click-to-allocate interaction (Stage A3 B9b)
- Spirit Guide build-coach commentary in tooltip (Stage A7)
- Reset interaction (Stage A3 B9c)
- Multi-band optimal-vs-current comparison (Stage A2 closeout B14 + Stage A7)
- Per-skill custom icons replacing procedural (Stage A2 closeout)

### Estimated drax effort

- Component scaffolding (no engine dep): ~3-5 days
- Engine integration (post-B6 main ship): ~3-5 days
- Polish + mobile tuning + accessibility: ~2-3 days
- **Total VS2a load:** ~2 weeks (vs. ~3-4 weeks if drax also designs the shape from scratch)

---

## 13. What this spec does NOT cover

- **Specific React component / Pixi.js implementation** — drax owns
- **Animation timing / easing curves** — drax owns within game-feel norms
- **Specific RGB palette** — drax owns within HD-2D-shaped pixel-art register
- **Build-recommendation engine** — Stage A7 Spirit Guide build-coach
- **Trait surface** — B9a; renders adjacent to skill tree but separate component
- **Loadout / gear interaction** — separate surface; tree is skills only
- **Tutorial / onboarding for first encounter** — gandalf authoring later if playtest signal demands
- **Multi-class comparison** — single-class view only for VS2a
- **Seasonal-vocabulary chain naming** — pre-Stage-3 falls back to canonical-four-coded; Stage 3 cipher migration lands per-season chain names

---

## 14. Recommended next actions

For knight-rider:
1. Author drax dispatch for B6 skill-tree UI implementation against this spec — scoped to "scaffolding can begin now; engine integration when B6 main ships"
2. Confirm with rocket + gamora that B6 schema fields per § 10 will populate reliably
3. Add to handoff doc / CHANGELOG: B6 UI scoping landed; drax unblocked on scaffolding

For drax (when dispatch lands):
1. Read this spec end-to-end before scaffolding
2. Call back on § 11 open questions before locking visual conventions
3. Build component scaffolding against mocked engine emission until B6 main ships
4. Surface any spec ambiguity to gandalf via knight-rider (not improvise)

For gamora (B6 main, when starting):
1. Confirm § 10 schema fields populate reliably
2. Surface any per-archetype template edge cases that don't fit the 4-tier-N-chain shape (this spec assumes the templates per commit 4f5cd93 are the canonical structure)

For gandalf (self):
1. Re-read this spec when drax surfaces open-question responses; refine if playtest signal demands
2. Author trait-surface adjacency spec at Stage A3 authoring window (companion to this doc)
3. Re-evaluate icon strategy at Stage A2 closeout — does Pimen/Pixogen/etc. catalogue support per-skill icons, or commission separately?

---

— gandalf, 2026-05-16 (Day 4 close)
