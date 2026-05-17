# Gandalf request to knight-rider — Environment tileset catalogue sweep + VS2a per-season selection framework

**From:** gandalf
**To:** knight-rider (for legolas Mode B + small gandalf authoring + downstream drax dispatch routing)
**Date:** 2026-05-17 (Day 5 — Matt direct catch)
**Authorized by:** Matt direct ("one of the worst parts of [demo v1] was the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls" + "would it make sense for legolas to look for anything that might match to our static dimensions of floors/walls? This could REALLY make the difference in the demo.")
**Type:** Catalogue-sweep + design-framework + Matt-selection commission — closes a load-bearing demo-visual-quality gap for VS2a
**Severity:** 🔴 VS2a-gating (recommended) — same logic as Drift-14: don't ship VS2a with another known-low-quality dimension when the closure is bounded
**Estimated effort:** Legolas Mode B ~5-8h; gandalf framework ~2h; Matt selection ~30 min; drax integration ~3-5 days (separate downstream dispatch)

**Source context:** Matt direct catch surfaces a P6 forward-audit instance — environment tileset / wall / prop sourcing was IMPLICIT in the catalogue work (Step B Tier-1 inventory scoped to VFX + characters; environment assets never explicitly scoped). Demo v1 shipped with geometrically-drawn placeholders that read as a known quality drag in family playtest. Drax v0.12 room/hallway topology committed VS2a to Diablo/PoE-style framing but the visual fill remains geometric primitives at present.

---

## Why this commission exists

The catalogue research to date scoped TWO axes:
- **VFX** (Pimen GREEN-list 11/13 elements + CreativeKind for monsters)
- **Characters** (chierit Elementals + CreativeKind monster sprites)

The THIRD axis — **environment assets (floor tiles + wall tiles + props / scenery objects)** — was implicit-deferred without being named as a deferred axis. This is the same P6 pattern as movement-speed-baseline (Drift-11A), geometry × element VFX coverage (Drift-11B), per-season vocabulary VFX-coherence (Drift-14): a load-bearing dimension implicit-bundled into "later" until "later" became upstream of a near-term ship.

The demo v1 empirical signal is unambiguous (per Matt): geometric walls + geometric "random seasonal structures" read as low-quality; geometric floor tiles read as merely acceptable. The room/hallway topology drax shipped Day 4 morning targets ARPG-genre framing where environmental visual identity is load-bearing — Diablo II's per-act tilesets, Diablo III/IV's per-zone visual identity, PoE's per-map tile families, Hades's per-region chamber visuals, Octopath/Sea of Stars/Eiyuden Chronicle HD-2D environmental detail — ALL of these treat environment art as foundational, not decorative.

**Matt's "this could REALLY make the difference" framing is correct.** Genre canon requires environmental visual identity at our scale; we've been shipping geometric placeholders against it.

---

## Two-track commission + forward downstream extension

### Track A — Legolas Mode B catalogue sweep for environment tilesets

**Owner:** legolas (Mode B — systematic catalogue crawl; read-only)
**Estimated effort:** 5-8h
**Output:** `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md` + per-vendor catalogue JSONL entries

**Scope:**

1. **Crawl Tier-1 pixel-art vendors** for environment tileset packs that meet our criteria:
   - **Style register:** HD-2D-shaped pixel-art (Candidate B per `canonical/story/style-register.md`) — NOT retro pixel-art (Stardew-class), NOT vector/clean-line, NOT anime hand-drawn
   - **Tile dimensions compatible with PIXELS_PER_METER=48:** ideal source-tile sizes 32×32 / 48×48 / 64×64 / 96×96; pack-level scale-compatibility with our 48 px/m convention so a 1m tile fills 48×48 rendered pixels (or simple integer scale-factor to reach this)
   - **License:** CC-BY or commercial-royalty-free with attribution; flag any pack with restrictive licensing
   - **Coverage:** ideally packs that ship floor + wall + props as a single coherent set (tile coherence matters); standalone floor-only packs acceptable as secondary candidates

2. **Tier-1 vendors to crawl (priority order):**
   - **Pimen** — already in catalogue; check for environment packs beyond VFX
   - **CreativeKind** — already in catalogue for characters/monsters; check for environment packs
   - **Ansimuz** — known retro pixel-art vendor; sweep for any HD-2D-shaped sets
   - **Pipoya** — RPG tile sets; pixel-art-leaning
   - **Foozle** — dungeon tile sets
   - **Elthen** — hand-drawn pixel-art vendor (HD-2D-register adjacent); LIKELY-HIGH-FIT
   - **CraftPix** — mixed register; filter to pixel-art packs only per the Drift-13 vendor-mixed-register lesson
   - **Time cap if Tier-1 returns insufficient:** flag for Tier-2 vendor sweep as separate dispatch (CodeManu, FrostWindz, BraCKEYs, Pixogen already partially crawled — re-evaluate for environment packs)

3. **Per-pack characterization** (extends existing catalogue JSONL schema):
   - Standard fields (vendor, pack-name, license, intrinsic frame sizes, file format)
   - **NEW field: `primary_fit_seasons`** — gandalf-fillable later; legolas-tag with descriptive themes per pack (e.g., "dark cave / cathedral interior / forest grove / desert ruin / ice cavern / volcanic peak / abandoned village") so gandalf can map themes to season anchors
   - **NEW field: `coverage`** — enumeration of what's in the pack (floor / wall / props / overlays / animated_objects / lighting_layer)
   - **NEW field: `tile_dimensions`** — source-tile pixel size + scale-compatibility note
   - **Sample image URLs or asset-extraction screenshots** for gandalf visual inspection

4. **Output document structure:**
   - Vendor-by-vendor scout (similar shape to `2026-05-16-character-track-vendor-scout-2026-05-16.md` from the character-track sweep)
   - Cross-vendor inventory consolidated to single JSONL at `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl`
   - Summary table: top 5-10 candidate packs across vendors with primary-fit-themes named
   - Findings-blockers if any: vendors with mixed register, licensing concerns, asset-quality issues

**Constraints:**
- Read-only across all vendor sources
- $0 LLM budget; pure analytical research
- 8h time cap; surface findings if catalogue insufficient at Tier-1 (signals need for paid acquisition or Tier-2 sweep)

**Required reading:**
- `canonical/story/style-register.md` — HD-2D-pixel-art register + score-don't-filter principle
- `canonical/story/arena-room-hallway-system.md` — drax room/hallway topology + 30m default room + PIXELS_PER_METER=48 scale anchor
- `canonical/story/drift-audit.md` § Drift-13 — vendor-mixed-register lesson (CraftPix split)
- Prior scout docs: `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` + `monster-track-vendor-scout-2026-05-16.md` (methodology reference)

### Track B — Gandalf per-season environmental theming framework

**Owner:** gandalf
**Estimated effort:** ~2h
**Output:** `canonical/story/per-season-environmental-theming-2026-05-17.md`

**Scope:**

Author a small canonical-story doc defining the decision framework + Matt-decision dimensions for per-season environment selection. Spec must define:

1. **Decision unit:** ONE environment-pack selection per season at season-generation time. Matt picks from legolas-curated candidates.

2. **Decision dimensions:**
   - **Thematic fit to season anchor** (e.g., Hermit → cave/cathedral interior; Full Moon → moonlit forest; Capricorn → mountain peak; Death → abandoned ruin; Waxing Crescent → new-growth forest)
   - **Visual coherence with chierit characters + Pimen VFX** (HD-2D pixel-art register; tile-vs-character pixel-density compatibility; chierit at 2.5× scale per Path A-prime means tiles must look right at corresponding pixel densities)
   - **Coverage completeness** (floor + wall + at least one prop category for visual richness; floor-only packs ship VS2a but flag VS2c+ expansion)
   - **License + attribution coherence** (CC-BY attribution surfaces via F1 credits overlay)

3. **Selection cadence:**
   - VS2a: ONE pack for the regen season; Matt picks from legolas Top-5 candidates
   - VS2b: ONE additional pack (different theme; per-season variety begins)
   - VS2c+: full per-season-decision cadence; legolas continues catalogue expansion as needed

4. **Asset acquisition flow:**
   - legolas catalogue surfaces candidates → gandalf shortlist (2-3 per season) → Matt picks → drax integration dispatch (separate; knight-rider authors)
   - Acquired packs added to `data/seasonal_elements/environment-packs.json` (new file; elrond data-architecture call) with metadata + per-season usage tracking

5. **What environmental theming is NOT trying to be:**
   - **Not procedurally generated** — pick from acquired packs; no engine-side procedural tile generation in Phase 0
   - **Not fully unique per season** — VS2a/VS2b ship 1-2 packs; full uniqueness per season is VS2c+ scope
   - **Not animated environments** — Phase 0 ships static environment tiles; animated tiles (waterfalls, torches) is post-Phase-0 polish
   - **Not interactive environment** — destructible walls, breakable props, etc. are out of Phase 0 scope

6. **Cross-references for downstream consumers:**
   - drax: room/hallway renderer extension consumes environment-pack manifest reference at season-load time
   - star-lord: season export packet includes `environment_pack_id` per season (manifest field forward-compat)
   - elrond: catalogue schema extension for environment-pack tracking
   - rocket: no engine generation change; environment is a consumption-time concern not a generation-time concern

**Required reading:**
- Track A return doc (legolas catalogue scout)
- `canonical/story/style-register.md`, `cosmology-reincarnated.md`, `arena-room-hallway-system.md`, `court-of-forms.md`, `season-feel-rubric.md`

### Track C — Matt VS2a environment-pack selection

**Owner:** Matt direct
**Estimated effort:** ~30 min
**Output:** decisions-log entry (knight-rider drafts) + commission to drax for integration

**Scope:**

After Track A + Track B complete, gandalf produces a 2-3 candidate shortlist for VS2a's regen season. Matt picks one. Knight-rider drafts decisions-log entry capturing the choice + rationale. Drax integration dispatch authored separately.

### Track D — Drax integration (downstream; separate dispatch)

**Owner:** drax (NEW dispatch knight-rider authors after Track C closes)
**Estimated effort:** ~3-5 days drax (depends on existing renderer flexibility)
**NOT SCOPED in this commission** — surfaces as forward-flag for knight-rider authoring queue

**Scope (forward-reference):**

1. Room/hallway renderer extension — consume environment-pack manifest reference at season-load
2. Floor tile rendering — replace geometric primitives with sprite-tile rendering at room+hallway floors
3. Wall sprite rendering — replace geometric wall lines with wall-sprite rendering at room+hallway boundaries
4. Prop / scenery rendering — place props at room interiors per spawn rules (TBD: density, anchor points, placement randomization)
5. Attribution credits overlay — environment-pack CC-BY attribution wired through F1 credits per existing chierit pattern
6. Visual regression smoke — compare environment-rendered VS2a vs current-geometric VS2a; gandalf review for HD-2D-register coherence

---

## VS2a-gating recommendation

**🔴 Recommend VS2a-gating reclassification — same logic as Drift-14.**

VS2a is being shaped as the end-game-anchored playtest representation of Reincarnated's actual feel. If demo v1's known-low-quality geometric scenery ships in VS2a, the playtest signal is contaminated by visual-quality drag that doesn't reflect the project's actual intent. Closure is bounded (1.5-2 weeks total: Track A + Track B + Matt selection + drax integration); the regen cycle for VS2a is already scheduled; environment integration folds in alongside the other VS2a-gating closures.

**The alternative (defer to VS2b/VS2c+) is structurally indefensible** given that we now have:
- Drax room/hallway topology committed to ARPG single-camera framing (Day 4 morning)
- Path A-prime sprite scales committed to ARPG-genre 100-130 px character heights (Day 4 evening)
- Drift-14 closure committed to canonical-bias-clean per-season vocabulary (Day 5)
- Movement-speed end-game-anchored values committed to actual-game-feel (Day 4 evening)

Shipping all of these visual-quality + design-intent commitments alongside geometric environment placeholders would be incoherent. The environment gap is structurally analogous to all four of the above — load-bearing dimension that was implicit-deferred and now needs explicit closure for VS2a's player-experience contract to hold.

---

## Acceptance criteria (Track A + B; Track C is Matt-decision; Track D is separate downstream)

- [ ] Track A: legolas scout doc filed; cross-vendor inventory JSONL produced; top 5-10 candidate packs identified with primary-fit-themes named; sample images / extraction screenshots accessible
- [ ] Track A: findings-blockers surfaced if Tier-1 catalogue is insufficient (signals need for paid acquisition or Tier-2 sweep)
- [ ] Track B: gandalf framework doc filed; per-season environmental theming decision dimensions defined; selection cadence + acquisition flow + cross-references all populated
- [ ] Track B: gandalf shortlist of 2-3 candidate packs for VS2a regen season ready for Matt review
- [ ] Track C: Matt picks VS2a pack from shortlist; decisions-log entry drafted; commission to drax authored separately by knight-rider

---

## Drift-audit framing — Drift-15 candidate

This commission's existence is itself the empirical surface of a new drift instance. Filing as **Drift-15 candidate** in `canonical/story/drift-audit.md` § "Drift instances observed and archived":

**Drift-15 — Environment tileset / wall / prop sourcing implicit-deferred without being named as a deferred axis (P6 instance).** Same pattern shape as Drift-11A (movement-speed), Drift-11B (geometry × element VFX coverage), Drift-14 (pool VFX-mapping). The catalogue work explicitly scoped VFX + characters; environment was the third axis that never got named at scoping time. Matt direct catch 2026-05-17 surfaced it by reference to demo v1 empirical signal. **Same prevention prescription as Drift-11 sibling-cluster-sweep:** when scoping a multi-axis catalogue workstream, enumerate ALL load-bearing visual axes (VFX + characters + environment + UI + audio) at scoping time and explicitly defer any out-of-scope axis with named ship-gate tied to the deferred milestone.

Forward-flag: gandalf authors Drift-15 entry alongside the Track B framework doc in same commit.

---

## Sequencing — flexible but ideally HIGH priority for VS2a

Independent of:
- Movement-speed cascade (rocket + gamora + drax + star-lord)
- Drift-14 pool VFX-mapping audit (legolas + gandalf)
- B6 main + B6 UI (rocket + gamora + drax)
- Stage B export-DTO fix (star-lord)
- Character-track ingest (drax)
- Suno music prompt pipeline (gandalf + star-lord; LOW priority)

Can run in parallel with all VS2a-gating items above; only consumes legolas + gandalf bandwidth in Tracks A + B. **Recommended priority: HIGH (VS2a-gating).** Track A fires immediately when knight-rider has capacity; Track B follows legolas return; Matt selection is ~30 min; Track D drax integration sequences alongside other drax VS2a work.

---

## What this commission unblocks + delivers

- **VS2a visual quality lifts from "geometric placeholders" to "HD-2D environment tiles"** — closes a known demo v1 quality drag; aligns with ARPG-genre + HD-2D-register commitments shipping in VS2a
- **Per-season environmental variety becomes a named design dimension** with documented decision framework rather than implicit "drax invents geometry"
- **Forward catalogue work** (VS2b + VS2c+ environmental packs) inherits the framework — no per-season re-architecture
- **Drift-15 prevention prescription** propagates to future multi-axis catalogue commissions — environment + UI + audio axes explicitly enumerated at scoping time

---

— gandalf, 2026-05-17 (Day 5 — Matt direct catch on environment-art gap)
