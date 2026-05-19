# Dispatch — 2026-05-19 — drax — VS2a B6 skill-tree UI surface decomposition

**From:** knight-rider
**To:** drax (presentation seam — B6 skill-tree UI surface OWNER; drax-authored design dispatch + prototype)
**Approved by:** AUTONOMOUS — VS2a hive-mind continuation under Matt directive 2026-05-19 (no per-dispatch Matt approval; B6 UI surface is a CRITICAL VS2a gap per `canonical/16-project-roadmap.md` § VS2a "Design watch-items" + P6 forward audit; drax-side decomposition authority confirmed per autonomous-operation protocol § 4.0)
**Estimated effort:** Design phase 1–2 days drax authoring; prototype implementation 1–2 weeks
**Acceptance:** Design dispatch authored by drax + prototype B6 skill-tree UI surface shipped to `reincarnated-demo` per drax-decided architecture + visual smoke screenshot captured + AGENT_STATE.md updated. Tag fires: `vs2a/v0.6-b6-skilltree-ui-decomposition`.
**Hive context:** VS2a hive ACTIVE; engine-rebuild v1.0 batch CLOSED. F4 is a **first-fire batch** dispatch — fires immediately under autonomous mode, no upstream gate. **Resolves the single most-load-bearing VS2a UI gap.** Engine emits skill-tree data; demo has NO surface to render it. Without F4, B6 main work (S2) ships invisible to the player.

---

## TL;DR — what you're doing

The roadmap (`canonical/16-project-roadmap.md` § VS2a) flags **B6 skill-tree UI surface** as 🔴 CRITICAL gap:

> Engine emits tree data; demo has no surface to render it. Per P6 forward audit.

This dispatch hands you the gap with full autonomous authority to:

1. **Author the design dispatch** — your own decomposition document captured at `agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md` (the *design* dispatch, sibling to this *commission* dispatch). Document rendering shape (vertical / horizontal / radial / hybrid), node icon strategy, unlock-feedback affordance, mobile-first sizing, tap-to-allocate UX, point-allocation visualization, undo/respec semantics — all under drax L1 authority. Gandalf design-consult is available on naming-triad / telegraph-art / register coherence questions; route via hive log.

2. **Ship a prototype B6 skill-tree UI surface** in `reincarnated-demo` against the design you author. Mobile-first per project default (Reincarnated-demo target). Iterate visually; no engine-side coupling beyond the existing tree-data emission contract.

Drax owns the entire surface — design + implementation. Knight-rider commissions; drax decomposes and executes. Gandalf is consult, not gate.

---

## Context — why this gap is in front of you NOW

### The structural state

- **B6 — Class kit composition + Hierarchical Skill Tree** is the central VS2a content workstream (per `canonical/16-project-roadmap.md` § VS2a scope table + `canonical/28-engine-arpg-rebalance-design.md`)
- Engine emits tree data (rocket pre-work + gamora main work; pre-work dispatch shipped earlier under engine-rebuild flow; main work depends on F2 kit-redesign approach decision per scope-of-work-vs2a § 2.3)
- **The demo has NO skill-tree rendering surface today.** No `skill-tree.ts`, no `skillTreePanel.ts`, no Pixi container for skill-tree nodes. Inspecting `reincarnated-demo/src/ui/`: `characterSheet.ts`, `combatHud.ts`, `combatLog.ts`, `inventoryPanel.ts`, `dashCooldownHud.ts` exist. No skill-tree surface exists.
- VS2a SHIP GATE (per `scope-of-work-vs2a.md` § 2.10 L1): single regenerated season demonstrates updated gauntlet + new geometry palette + end-game-anchored movement-speed + **B6 kit composition** + first Pimen + chierit. B6 ships invisible to the player if there's no UI surface to render it.

### P6 forward audit signal

This gap is a classic P6 (Pattern P6 — silent-deferral) instance:
- B6 engine-side work shipped iteratively
- B6 player-facing surface was implicit-deferred without being named as a deferred axis
- The roadmap's design-watch-items section names it once; never sequenced into a dispatch
- Now VS2a is the ship gate; the gap is the binding constraint on the player experience

The P6 prevention prescription (per `canonical/story/p6-forward-audit-2026-05-16.md` lineage + Discipline #18 candidate language) requires: explicit closure dispatch before VS2a ship. **F4 IS that closure.**

### The 4 sibling P6 instances pattern

This is the FIFTH P6 instance in 2026-05-16/17 closure cascade (after Drift-11A movement-speed, Drift-11B geometry × element VFX coverage, Drift-14 pool VFX-mapping, Drift-15 environment-tileset). Same shape: load-bearing dimension implicit-deferred until "later" became upstream of a near-term ship. The B6 UI surface is that exact pattern for the skill-tree axis.

---

## What you're authoring (the design dispatch)

**Path:** `agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md` (sibling to this commission dispatch; you author it; it captures your design)

Your design doc decomposes:

### § 1 — Rendering shape decision

Pick ONE; document trade-off; cite genre precedent.

- **Vertical (PoE-style)** — branching tree extending downward; classic ARPG; tight on mobile widths
- **Horizontal (D2-style)** — multi-column tree; reads left-to-right; constrained vertical depth
- **Radial (D3-style)** — circular layout with category sectors; visually striking; harder to extend
- **Hybrid / collapsible** — accordion-style nested rows; mobile-first; compact but less "tree-feeling"
- **Other** — your call. Document the choice + rationale.

Cross-reference genre precedent and the Reincarnated design intent (Diablo/PoE-style room sequence framing per roadmap § VS2a; isekai narrative skin lands at VS2b). The skill tree's visual identity should support the ARPG genre commitment.

### § 2 — Node icon strategy

Pick approach; document chierit / Pimen catalogue integration:

- Use chierit Elementals zip archive iconography? (currently for character rendering per drax dispatch shipped 2026-05-16)
- Use Pimen VFX preview frames as node icons?
- Use primitive icons (geometric shapes color-coded by archetype)?
- Hybrid (primitive default + chierit/Pimen for "named" nodes)?

Surface to gandalf via hive log if a register-coherence question emerges (e.g., "chierit at 2.5× scale vs Pimen at native frame size — what's the node-icon size convention?"). L1 drax decision otherwise.

### § 3 — Unlock-feedback affordance

How does the player KNOW they unlocked a node?

- Particle burst on click? (Pimen integration here is forward-flag)
- Audio cue + visual highlight? (audio shipped post-Phase-0 polish; visual only for now)
- Animated edge-traversal showing the unlock propagating from current node?
- Modal confirmation?

Mobile-first: tap-to-allocate UX must feel responsive. No double-tap-required confirmations unless the unlock is irreversible (which depends on respec semantics — § 6).

### § 4 — Mobile-first sizing

- Minimum touch target size per project standard (drax to confirm against existing inventoryPanel + combatHud conventions; e.g., 44×44 px minimum touch target per iOS Human Interface Guidelines / Material 3)
- Scroll vs zoom interaction (pan-to-explore the tree; zoom-to-cluster vs zoom-to-node)
- Reincarnated-demo target: phone landscape and portrait; tablet; desktop. Surface dimensions decision (e.g., tree rendered at constant logical size + scaled per viewport).

### § 5 — Tap-to-allocate UX

- Tap node → spend point → unlock (immediate)
- Tap node → preview cost / dependencies → confirm
- Drag-to-allocate? (multi-touch / desktop-only)
- Long-press for "details" affordance?

Surface the interaction taxonomy. Pick the simplest path that satisfies the genre intent + mobile-first constraint.

### § 6 — Point-allocation visualization + undo/respec semantics

- Show point pool ("3 points to spend" or "0 / 50 allocated")?
- Show which nodes are unlocked / allocated / available / locked?
- Respec mechanic — is undo supported? Per-session? Per-character? Cost? 
- Surface to gandalf via hive log if cross-cutting design question emerges (respec UX is partially design-policy, partially UI-affordance)

### § 7 — Data contract with engine

Engine emits the tree (rocket pre-work; gamora main work). What's the contract?

- Where in season-output JSON does the tree live? (likely under skill catalogue or per-class manifest)
- What fields per node? (node-id; parent-id; cost; prerequisite-ids; unlocked-effect-references; icon-hint; archetype-tag)
- Per-class trees vs catalogue-wide tree?
- Drax surfaces the contract YOU need; rocket + gamora can adapt at S2 main-work time. Don't constrain B6 main work shape from the UI side; ask for the shape you want.

This subsection is your handoff to rocket / gamora for S2 alignment. Surface in hive log when authored so they consume your contract requirements at S2 dispatch time.

### § 8 — Scope phasing

What ships in F4 (the prototype) vs what's left for post-F4 polish:

- F4 prototype: rendering + tap-to-allocate + basic unlock-feedback + point pool visualization (minimum viable; placeholder data acceptable until S2 ships)
- F4 post-prototype polish: chierit/Pimen integration; audio cues; respec UX; mobile-tablet-desktop responsive polish

Decide what the "ship line" is for F4 acceptance.

---

## Context drax should consult before authoring

**Required reading:**

1. **`agentic_orchestration/dispatches/2026-05-19-drax-vs2a-b6-skilltree-ui-decomposition.md`** (this dispatch) — the commission shape
2. **`agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.1 (F4) + § 2.3 (S2 B6 main work) + § 2.10 (L1 ship gate)** — F4 deliverables + B6 main-work dependency + ship-gate semantics
3. **`agentic_orchestration/hive-mind/coordination-matrix-vs2a.md`** § 1 F4 row (drax OWNS design dispatch; rocket reads B6 main; gamora reads) + § 3 concurrent-edit hot-spots
4. **`canonical/16-project-roadmap.md` § VS2a + § "Design watch-items (gandalf)"** — the gap framing + chierit per-archetype mapping forward-flag
5. **`canonical/28-engine-arpg-rebalance-design.md`** B6 spec — design intent + criteria the engine-side tree-data emission honors
6. **`canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9** — autonomous-operation; Matt-only-at-wind-down
7. **`reincarnated-demo/AGENT_STATE.md`** — your last checkpoint (post-v0.15 + in-flight C1+C2+C3+C4)
8. **`reincarnated-demo/src/ui/`** — existing UI surface conventions (`inventoryPanel.ts`, `characterSheet.ts`, `combatHud.ts`, `creditsOverlay.ts` for typographic + interaction conventions; `drawerShell.ts` for the modal-surface convention)
9. **`reincarnated-demo/src/ui/seasonTheme.ts`** + **`reincarnated-demo/src/ui/typography.ts`** — design-token surface
10. **`canonical/story/style-register.md`** — HD-2D-pixel-art register; score-don't-filter principle
11. **`reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — particularly Discipline #1 (design-before-build) + Discipline #11 (attribution) + Discipline #13 (drift watch)
12. **Genre precedent:** PoE skill tree, D2 skill trees, D3 paragon, D4 paragon board, Grim Dawn devotion screen, Last Epoch passive trees, Wolcen + Path of Exile mobile (latter for mobile-first reference). Don't quote them; absorb the visual identity space they occupy.

---

## What you are NOT doing in F4

- **NOT shipping B6 main work data.** S2 is rocket + gamora's joint dispatch (separately authored after F2 lands per scope-of-work-vs2a § 2.3); your UI prototype consumes placeholder data until S2 ships.
- **NOT touching engine-side tree emission.** That's rocket pre-work + gamora main work. Your design § 7 surfaces the contract you need; they adapt.
- **NOT picking chierit per-archetype mapping.** That's a gandalf decision flagged in roadmap § VS2a design watch-items; parallel to F4, not gating F4. If chierit per-archetype mapping decision lands while you're working on F4, integrate; if not, prototype against element-only-default placeholder.
- **NOT integrating Pimen VFX for node-unlock affordance polish.** Forward-flag for post-prototype polish; F4 ships with primitive affordance (color burst, font animation, or similar).
- **NOT addressing respec costs / economy.** Surface the UX shape required; cost economics is a gandalf-design + B6 spec decision. If gandalf hasn't decided, your prototype assumes free-respec or no-respec (drax-pick); document.
- **NOT escalating to Matt.** F4 is autonomous per protocol § 4.0. Matt re-enters only at wind-down.

---

## Cross-seam contract change? (Principle 6 gate)

**Design dispatch + prototype implementation in `reincarnated-demo`.** The data contract you author in § 7 (the contract drax wants from rocket + gamora's S2 main work) is a forward-looking specification, not a current cross-seam contract change. When S2 ships, rocket + gamora honor your § 7 contract; MIGRATION.md authoring happens at S2 dispatch time, not F4.

**Round-trip: not applicable in this dispatch — drax-only prototype with placeholder data. S2 dispatch carries the engine-side contract + round-trip smoke requirement when it fires.**

---

## Scope

### Drax design phase (1–2 days)

- [ ] Design dispatch authored at `agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md` covering § 1–§ 8 above
- [ ] Genre precedent + Reincarnated-demo register-coherence rationale documented
- [ ] § 7 data contract surfaced in hive log for rocket + gamora consumption at S2 dispatch time
- [ ] Open questions for gandalf design-consult routed via hive log (if any surface during authoring)

### Drax prototype phase (1–2 weeks)

- [ ] Prototype B6 skill-tree UI surface in `reincarnated-demo` per design § 8 ship-line definition
- [ ] Placeholder data fixtures (skill-tree JSON; per-class trees representative of B6 design intent; drax authors or extracts from prior B6 pre-work outputs if rocket pre-work emits them)
- [ ] Mobile + desktop responsive at minimum viable level
- [ ] Visual smoke screenshot captured (galadriel sub-agent restriction is in effect per protocol § 7; drax captures directly per existing convention, or no-screenshot acceptable if drax decides)
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request surfaced in hive log: `vs2a/v0.6-b6-skilltree-ui-decomposition` (knight-rider fires)

### Joint scope (handoff to S2)

- [ ] Hive log entry: drax STATE entry capturing § 7 data contract requirement at design phase + STATE entry at prototype phase completion + HANDOFF to rocket + gamora for S2 contract integration
- [ ] If chierit per-archetype mapping decision lands during F4 (gandalf authors), drax integrates and surfaces in hive log; if not, drax forward-flags
- [ ] If gandalf design-consult surfaces register/naming-triad/telegraph-art question during F4, drax routes via hive log; gandalf responds per autonomous-operation cadence

---

## Acceptance criteria

- [ ] Design dispatch authored at `agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md`
- [ ] All 8 design sections present (rendering shape; node icons; unlock-feedback; mobile-first sizing; tap-to-allocate UX; point-allocation + respec; data contract with engine; scope phasing)
- [ ] Prototype B6 skill-tree UI surface shipped in `reincarnated-demo`
- [ ] Placeholder data exercised; mobile + desktop rendering validated
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE / HANDOFF entries on design phase complete + prototype phase complete
- [ ] Tag fire request: `vs2a/v0.6-b6-skilltree-ui-decomposition`
- [ ] § 7 data contract surfaced to rocket + gamora for S2 dispatch integration

---

## Out of scope (explicit non-goals)

- B6 main work data emission (rocket pre-work + gamora main work; S2 dispatch; gated on F2)
- chierit per-archetype mapping decision (gandalf; parallel to F4; not gating)
- Pimen VFX node-unlock affordance polish (post-prototype; not VS2a-blocking)
- Respec-cost economy design (gandalf; B6 spec territory)
- Audio cues for unlock-feedback (post-Phase-0 polish)
- C1 movement-speed implementation work (in-flight; independent timeline per drax AGENT_STATE)
- C2 B11 GREEN-list VFX integration (in-flight; independent timeline)
- C3 chierit character rendering (in-flight; independent timeline)
- C4 Pimen curation pipeline support (in-flight; independent timeline)
- Drift-15 Track D environment-tileset integration (held post-Matt-selection per F3 framework + scope-of-work-vs2a M1)

---

## Open questions for drax to resolve (in-seam L1 / cross-seam L2 routing)

- **Rendering shape choice** — L1 drax. Genre precedent + Reincarnated visual identity + mobile-first practicality drive the choice. Document trade-offs in design § 1.
- **Node icon strategy** — L1 drax. If chierit/Pimen integration question surfaces register-coherence concern (e.g., scale-anchor mismatch between chierit 2.5× + Pimen native), route to gandalf via hive log. L1 default: primitive iconography for prototype; chierit/Pimen forward-flag.
- **Mobile-first sizing conventions** — L1 drax. Project default convention is mobile-first (Reincarnated-demo target). Drax confirms touch-target sizing against existing UI conventions.
- **Tap-to-allocate confirmation flow** — L1 drax. Simplest viable; document choice.
- **Respec semantics** — L2 surface to gandalf via hive log if drax decides B6 spec hasn't named the convention. Default for prototype: no-respec (single-session allocation; reset on character switch).
- **Data contract field set (§ 7)** — L1 drax authoring; surface in hive log; rocket + gamora consume at S2 dispatch.
- **Per-class trees vs catalogue-wide tree** — L1 drax; cross-reference B6 design spec; surface if cross-cutting design tension.
- **Scope phasing ship-line** — L1 drax. Define what's prototype-acceptable vs post-prototype polish. Default: rendering + tap-to-allocate + basic unlock-feedback + point pool. chierit/Pimen + audio + respec-polish post-prototype.

---

## References

- `canonical/16-project-roadmap.md` § VS2a (B6 UI gap; design watch-items)
- `canonical/28-engine-arpg-rebalance-design.md` (B6 spec)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.1 (F4) + § 2.3 (S2 dependency) + § 2.10 (L1 ship gate)
- `agentic_orchestration/hive-mind/coordination-matrix-vs2a.md` § 1 (F4 row) + § 3 (concurrent-edit hot-spots) + § 4 (MIGRATION.md S2)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9
- `canonical/story/style-register.md` (HD-2D-pixel-art register)
- `reincarnated-demo/AGENT_STATE.md`
- `reincarnated-demo/src/ui/` (existing UI conventions)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #11, #13)
- Sibling P6 closures (architectural pattern reference):
  - Drift-11A: movement-speed (resolved 2026-05-16 Day-4 verdict reversal)
  - Drift-11B: geometry × element VFX coverage (resolved B11 + Pimen first integration)
  - Drift-14: pool VFX-mapping (in-flight per F3 framework)
  - Drift-15: environment tileset (in-flight per F3 framework)

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0 (inherited):

- **In-seam decisions** — L1 drax; no escalation
- **Cross-seam decisions** — L2 via knight-rider in hive log
- **Design-direction question** (e.g., respec semantics, chierit per-archetype mapping, register-coherence on node icons) — route to gandalf via hive log
- **No Matt-wait at any point during F4.** Matt re-enters only at wind-down.
- **Tag-firing** — surface request in hive log; knight-rider fires + pushes per ADR-006 amendment.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. F4 closes the fifth P6 instance in the closure cascade. Engine emits a skill tree; the player needs a surface to see it. Drax owns the surface — design and build. The road to L1 ship continues; the player needs every workstream visible.*

---

## Completion record

**Completed:** 2026-05-19 by drax
**Demo commits:** `54c17dac6` (prototype), `08a9f325e` (AGENT_STATE)
**Collab commit:** `1f1e40e` (design dispatch + hive log)
**Build smoke:** tsc --noEmit CLEAN; npm run build 536 modules, 0 errors

### Acceptance criteria status

- [x] Design dispatch authored: `agentic_orchestration/dispatches/2026-05-19-drax-b6-skilltree-ui-decomposition-design.md`
- [x] All 8 design sections present (§ 1 rendering shape; § 2 node icons; § 3 unlock-feedback; § 4 mobile-first sizing; § 5 tap-to-allocate; § 6 point-allocation + respec; § 7 data contract; § 8 scope phasing)
- [x] Prototype B6 skill-tree UI surface shipped in `reincarnated-demo` (src/ui/skillTree/)
- [x] Placeholder data fixture exercised (SAMPLE_FIRE_MAGE_TREE; 9-node fire_mage; 2 chains; 4 tiers)
- [x] Mobile + desktop responsive at minimum viable level (DrawerShell + desktop modal; hitR(44) touch zones)
- [x] AGENT_STATE.md updated
- [x] Hive log: STATE (design phase) + HANDOFF (§ 7 S2 contract) + STATE (prototype phase)
- [ ] Tag fire request surfaced: `vs2a/v0.6-b6-skilltree-ui-decomposition` — knight-rider fires
- [x] § 7 data contract surfaced to rocket + gamora in hive log HANDOFF entry

### Open items carried to next session

- Portrait 2×2 chain sub-grid (design complete; wiring deferred)
- Mobile TouchIcons button (KeyT keyboard only today)
- chierit per-archetype icons (pending gandalf mapping decision)
- Pimen VFX affordance (pending C4 pipeline)
- Respec cost UX (pending gandalf B6 spec decision)
- S2 fixture replacement (gated on rocket + gamora S2 dispatch)
