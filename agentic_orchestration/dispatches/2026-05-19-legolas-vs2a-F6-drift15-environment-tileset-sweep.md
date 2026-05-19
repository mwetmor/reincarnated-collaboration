# Dispatch — 2026-05-19 — legolas — VS2a F6 Drift-15 environment-tileset catalogue sweep (Track A)

**From:** knight-rider
**To:** legolas (research scout — Mode B systematic catalogue crawl OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when F3 lands per gating
**Estimated effort:** ~5–8h legolas Mode B
**Acceptance:** Per § Acceptance. Tag fires: `vs2a/v0.11-drift15-track-a-complete`.
**Hive context:** VS2a hive ACTIVE; F3 gandalf framework is the upstream gate. Closes Drift-15 (P6 instance # 5; environment third visual axis implicit-deferred). Track A only — Tracks B/C/D out of F6 scope per F3 framework's autonomous-vs-Matt-gated separation.

---

## Context

Per F3 dispatch + gandalf 2026-05-17 commission (`agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`): catalogue work scoped VFX (Pimen) + characters (chierit) — environment third axis was implicit-deferred. Drax Day-4 room/hallway topology commits VS2a to Diablo/PoE framing where environmental visual identity is load-bearing. Demo v1 empirical signal: geometric walls + geometric "random seasonal structures" read as low-quality.

Matt direct catch 2026-05-17: *"the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls... This could REALLY make the difference in the demo."* — escalated to VS2a-gating.

F3 (`2026-05-19-gandalf-vs2a-drift14-15-framework.md`) authors the per-season environmental theming framework + per-pack characterization fields. F6 EXECUTES Track A catalogue sweep against that framework.

**Track separation per F3 framework:**
- **Track A (this dispatch)** — legolas Mode B catalogue crawl; autonomous
- **Track B** — gandalf authors shortlist after Track A returns; autonomous (separate gandalf surface; not a knight-rider dispatch)
- **Track C** — Matt picks 1 of 3 candidates; HELD for wind-down (M1)
- **Track D** — drax integration; pre-authored separately as F6-D dispatch; HELD post-M1

---

## Required reading

In order:
1. F3 framework doc once authored: `canonical/story/per-season-environmental-theming-2026-05-19.md`
2. `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` (original commission)
3. `canonical/story/drift-audit.md` § Drift-15
4. `canonical/story/style-register.md` (HD-2D-pixel-art register; score-don't-filter)
5. `canonical/story/arena-room-hallway-system.md` (drax topology; PIXELS_PER_METER=48 anchor)
6. Prior scout docs: `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` + `monster-track-vendor-scout-2026-05-16.md` (methodology reference)
7. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope (Track A only)

- [ ] Crawl Tier-1 pixel-art vendors per F3 framework priority order: **Pimen / CreativeKind / Ansimuz / Pipoya / Foozle / Elthen / CraftPix**
- [ ] Per-pack characterization per F3 framework fields (per pack):
  - `vendor`, `pack-name`, `license`, `intrinsic frame sizes`, `file format`
  - `primary_fit_seasons` (legolas-tag descriptive themes per pack; e.g., dark cave / cathedral interior / forest grove / desert ruin / ice cavern / volcanic peak / abandoned village)
  - `coverage` (floor / wall / props / overlays / animated_objects / lighting_layer)
  - `tile_dimensions` (source-tile px size + scale-compatibility note for PIXELS_PER_METER=48)
  - Sample image URLs or asset-extraction screenshots for gandalf Track B visual inspection
- [ ] Style-register filter: HD-2D-shaped pixel-art (Candidate B per style-register); NOT retro pixel-art (Stardew-class), NOT vector/clean-line, NOT anime hand-drawn
- [ ] License filter: CC-BY or commercial-royalty-free with attribution; flag restrictive licensing
- [ ] Coverage priority: packs shipping floor + wall + props as coherent set; standalone floor-only packs as secondary
- [ ] Time cap 8h: if Tier-1 returns insufficient, surface findings-blockers + recommend Tier-2 sweep (CodeManu / FrostWindz / BraCKEYs / Pixogen) as separate dispatch

---

## Outputs

1. **Vendor-by-vendor scout doc** at `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-19.md` (shape similar to character-track-vendor-scout-2026-05-16.md)

2. **Cross-vendor inventory JSONL** at `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-19.jsonl`

3. **Summary table** in scout doc: top 5–10 candidate packs across vendors with primary-fit-themes named

4. **Findings-blockers** surfaced if Tier-1 catalogue is insufficient (signals need for paid acquisition or Tier-2 sweep)

---

## Cross-seam contract change? (Principle 6 gate)

**Research output only; no production code change.** Downstream contract changes (F6-D drax integration; environment-packs.json data architecture) happen in separate dispatches.

**Round-trip: not applicable — research scout only.**

---

## Acceptance criteria

- [ ] Vendor-by-vendor scout doc filed
- [ ] Cross-vendor inventory JSONL produced
- [ ] Top 5–10 candidate packs identified with primary-fit-themes
- [ ] Sample images / extraction screenshots accessible for gandalf Track B visual inspection
- [ ] Findings-blockers surfaced if applicable
- [ ] Hive log entry: legolas STATE on commission start + STATE on completion + HANDOFF to gandalf for Track B
- [ ] Tag fire request surfaced: `vs2a/v0.11-drift15-track-a-complete`

---

## Out of scope

- Track B gandalf framework + shortlist authoring (separate gandalf surface; not a knight-rider dispatch — gandalf authors as design-steward output post-Track-A return)
- Track C Matt selection (HELD for wind-down)
- Track D drax integration (pre-authored at F6-D dispatch; HELD post-M1)
- Tier-2 vendor sweep (separate dispatch if findings-blockers warrant)
- Paid acquisition negotiations (not in legolas seam)

---

## Open questions for legolas

- **Vendor priority refinement** — F3 framework priority order is reference; legolas adjusts within seam if reconnaissance shifts vendor relevance
- **Sample-image extraction methodology** — L1 legolas. If vendor pack pages don't expose previews accessible without payment, surface as findings-blocker
- **Coverage threshold for "candidate pack"** — L1 legolas. Floor + wall is minimum; props strongly preferred
- **Cross-register vendor filtering** — F3 framework's score-don't-filter principle (`style-register.md`); flag mixed-register packs per Drift-13 lesson rather than auto-excluding

---

## References

- `canonical/story/per-season-environmental-theming-2026-05-19.md` (F3 framework; upstream)
- `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`
- `canonical/story/drift-audit.md` § Drift-15
- `canonical/story/style-register.md`
- `canonical/story/arena-room-hallway-system.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.9 (F6)
- `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` (methodology ref)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** F3 framework lands. Until F3 lands, F6 cannot fire — legolas needs the framework's per-pack characterization field definitions + criteria for "candidate" classification.

**No Matt-wait post-activation.** Matt re-enters at wind-down for Track C selection.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. F6 Track A closes the third visual axis catalogue gap; gandalf shortlists; Matt picks at wind-down; drax integrates post-selection.*
