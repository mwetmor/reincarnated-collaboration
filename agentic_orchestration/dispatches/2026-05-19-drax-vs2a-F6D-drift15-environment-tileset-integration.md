# Dispatch — 2026-05-19 — drax — VS2a F6-D Drift-15 environment-tileset integration (Track D)

**From:** knight-rider
**To:** drax (presentation seam — Track D renderer extension + integration OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires post-M1 Matt-selection at wind-down per F3 framework Track C/D separation
**Estimated effort:** ~3–5 days drax (depends on existing renderer flexibility)
**Acceptance:** Per § Acceptance. Tag fires: `vs2a/v0.16-drift15-drax-integration-complete`.
**Hive context:** VS2a hive HELD-post-M1. F6-D is the downstream-of-Matt step. Activates after Matt picks the VS2a environment pack at wind-down session (M1).

---

## Context

Per F3 framework + F6 Track A legolas sweep + Track B gandalf shortlist + Track C Matt selection (M1 wind-down step). After Matt picks the VS2a regen-season environment pack:

- Knight-rider drafts decisions-log entry capturing the Matt-selected pack + rationale
- Drax integrates: replace geometric placeholders in `reincarnated-demo` with sprite-tile rendering for floor/wall/props using the Matt-selected pack
- VS2a regen demo ships with HD-2D environment tiles instead of geometric placeholders

This dispatch is **PRE-AUTHORED with the Matt-pack placeholder as `<matt-selected-pack>`**. Drax substitutes the actual pack identifier at fire-time once Matt's selection lands.

---

## Required reading

In order:
1. Decisions-log entry for Matt-selected pack (knight-rider drafts at wind-down; lives at `reincarnated-engine/design/decisions/decisions-log.md`)
2. `canonical/story/per-season-environmental-theming-2026-05-19.md` (F3 framework with autonomous-vs-Matt-gated step separation)
3. Gandalf Track B shortlist doc (authored post-F6 Track A return; references Matt-selected pack)
4. Legolas F6 Track A scout doc (`agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-19.md`) — for pack metadata + sample images + licensing info
5. `canonical/story/arena-room-hallway-system.md` (drax topology; PIXELS_PER_METER=48; 30m default room) — renderer surface to extend
6. `canonical/story/style-register.md` (HD-2D-pixel-art register coherence requirement)
7. `reincarnated-demo/AGENT_STATE.md` (your last checkpoint)
8. `reincarnated-demo/src/world/` (room/hallway renderer code paths)
9. `reincarnated-demo/src/ui/creditsOverlay.ts` (existing CC-BY attribution pattern; F1 credits surface)
10. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Drax integration tasks

- [ ] **Asset acquisition + licensing**: pull Matt-selected pack assets into `reincarnated-demo/assets/environments/<pack-id>/` (drax-authored convention; consistent with existing `assets/` layout)
- [ ] **Manifest entry**: add pack metadata to `data/seasonal_elements/environment-packs.json` (new file per F3 framework asset-acquisition flow; elrond co-authors data-architecture call if cross-cutting)
- [ ] **Room/hallway renderer extension** — `reincarnated-demo/src/world/`:
  - Consume environment-pack manifest reference at season-load time
  - Replace geometric primitives with sprite-tile rendering at room+hallway floors
  - Replace geometric wall lines with wall-sprite rendering at room+hallway boundaries
  - Place props at room interiors per spawn rules (density, anchor points, placement randomization — drax-decided per genre intent + Matt-selected pack's prop availability)
- [ ] **Attribution credits overlay**: wire pack CC-BY attribution through F1 credits per existing chierit pattern (`reincarnated-demo/src/ui/creditsOverlay.ts`)
- [ ] **Visual regression smoke**: comparison render env-tile VS2a vs current-geometric VS2a; capture screenshot for gandalf register-coherence review
- [ ] **Mobile + desktop responsive validation**: tile-rendering performance at portrait/landscape/desktop viewports
- [ ] **AGENT_STATE.md updated**
- [ ] **Tag fire request**: `vs2a/v0.16-drift15-drax-integration-complete`

### Optional polish (drax judgment within seam)

- [ ] Animated tiles if pack ships them (waterfalls / torches / wind motion) — Phase 0 ships static; animated tiles flagged as future polish per F3 framework "What environmental theming is NOT"
- [ ] Per-room tile variation seeding (avoid visible repetition tiling artifacts)
- [ ] Lighting-layer integration if pack ships separate lighting tiles

---

## Cross-seam contract change? (Principle 6 gate)

**`data/seasonal_elements/environment-packs.json`** — NEW file per F3 framework. Additive; backward-compat (legacy demo without pack manifest falls back to geometric primitives per existing renderer).

**`reincarnated-demo` assets/ layout extension** — additive; no breaking change.

**Demo renderer extension** — additive consumer of new manifest; legacy seasons without pack reference render via existing geometric primitives.

**Round-trip smoke**: end-to-end fixture — season load → pack manifest read → renderer consumes → screenshot capture. Field-presence check at pack manifest boundary. **REQUIRED** per Principle 6 (new data contract for environment-pack consumption).

**MIGRATION.md** at `reincarnated-demo/MIGRATION.md` capturing the pack-manifest consumption contract (drax appends).

---

## Acceptance criteria

- [ ] Matt-selected pack integrated into `reincarnated-demo/assets/environments/<pack-id>/`
- [ ] `data/seasonal_elements/environment-packs.json` populated with pack metadata
- [ ] Room/hallway renderer extension shipped: floor + wall + props rendered with sprite tiles instead of geometric primitives
- [ ] CC-BY attribution wired through F1 credits overlay
- [ ] Visual regression smoke screenshot captured + gandalf register-coherence review surfaced via hive log
- [ ] Mobile + desktop responsive validated
- [ ] Round-trip smoke: season load → pack manifest read → renderer consumes → render
- [ ] MIGRATION.md appended at `reincarnated-demo/MIGRATION.md`
- [ ] AGENT_STATE.md updated
- [ ] Hive log: drax STATE on start + HANDOFF on completion + OBSERVATION if register-coherence requires gandalf review
- [ ] Tag: `vs2a/v0.16-drift15-drax-integration-complete`

---

## Out of scope

- Multiple environment packs in one demo build (VS2a ships one pack; VS2b adds the second per F3 selection cadence)
- Procedural tile generation (Phase 0 picks from acquired packs; not procedural)
- Destructible environment / interactive props (post-Phase-0 polish)
- Per-season environment SELECTION logic (drax integrates the Matt-selected pack; selection is M1 step)
- L1 demo regen orchestration (separate dispatch; L1 fires after F6-D + S1 + S2 + S3 + C-series all land)

---

## Open questions for drax

- **Pack identifier substitution** — at fire-time, drax reads the decisions-log entry capturing Matt's selection; substitutes `<matt-selected-pack>` throughout. If decisions-log entry hasn't landed (e.g., knight-rider hasn't drafted yet), drax surfaces in hive log + waits
- **Prop spawn rules** — L1 drax. Density / anchor points / placement randomization decisions per genre intent + pack's prop availability. Document in drax STATE entry.
- **Renderer extension shape** — L1 drax. Augment existing room/hallway code paths or new module under `src/world/environment/`?
- **Animated tiles integration** — L1 drax. If pack ships them, OK to ship animated for VS2a; if scope-creep concern, defer to post-VS2a per F3 "What environmental theming is NOT"
- **Per-room tile variation seeding** — L1 drax. Avoid visible repetition; default acceptable for VS2a
- **Cross-pack inventory** — VS2b adds 2nd pack per F3 cadence; ensure VS2a integration is generalizable for VS2b extension (not pack-specific hardcoded paths). L1 drax.

---

## References

- `canonical/story/per-season-environmental-theming-2026-05-19.md` (F3 framework; upstream)
- `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` (original commission with Track D forward-reference)
- `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-19.md` (F6 Track A output; will exist post-F6 landing)
- `reincarnated-engine/design/decisions/decisions-log.md` (Matt-selection entry; knight-rider drafts at wind-down)
- `canonical/story/arena-room-hallway-system.md`
- `canonical/story/style-register.md`
- `canonical/story/drift-audit.md` § Drift-15
- `reincarnated-demo/AGENT_STATE.md` + `reincarnated-demo/src/world/`
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 3.1 (M1) + tag plan entry `vs2a/v0.16`
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** M1 lands (Matt-selected environment pack at wind-down). Until M1, F6-D cannot fire — the pack identifier doesn't exist yet.

**Post-activation:** autonomous L1 drax execution per protocol § 4.0. Matt re-enters only at next wind-down (after L1 ships or if drax surfaces register-coherence concern requiring Matt eye).

**Pre-approval rationale:** Authoring F6-D now lets Matt approve the integration shape at the same moment he approves M1 framework. Post-M1, drax executes without further authoring needed.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. F6-D closes the environment-art VS2a gap with the pack Matt picks at wind-down. The geometric placeholders give way; the demo gains the HD-2D environmental identity ARPG canon requires.*
