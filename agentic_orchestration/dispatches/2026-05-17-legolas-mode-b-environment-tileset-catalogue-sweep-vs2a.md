# Dispatch — 2026-05-17 — legolas — Mode B environment-tileset catalogue sweep (VS2a-gating; Drift-15 closure)

**From:** knight-rider (authored per Matt directive 2026-05-17: "Authorized legolas amendment. Please fire" — incorporates 4 knight-rider-proposed amendments on top of gandalf's commission `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`)
**To:** legolas
**Approved by:** Matt at 2026-05-17 (commission authorization + amendment authorization both Matt-direct)
**Status:** READY-TO-FIRE
**Mode:** B (systematic catalogue crawl; read-only across all vendor sources)
**Estimated effort:** 5-8h (per gandalf scoping; hard cap 8h — surface findings + halt if scope exceeds)
**Budget:** $0 LLM

**Gate-1 bypass rationale:** Matt-directed (commission authorization + amendment authorization both Matt-direct); single-seam (legolas-only); read-only research; bounded scope (Tier-1 vendor catalogue crawl); time-cap discipline; VS2a-gating priority (Drift-15 closure aligned with Drift-14, MS verdict reversal, Path A-prime, room/hallway topology).

**Acceptance summary:** Single scout doc filed at `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md` + cross-vendor JSONL at `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl`. Tier-1 vendor sweep for **three sourcing categories** (Maps / Background pieces / Tilesets) matching HD-2D pixel-art register + license-clean + room-dimension-fit-verified for the static demo room dimensions (15m / 30m / 45m at 48 px/m). Top 5-10 candidate packs identified per gandalf framework input. Drift-15 P6 pattern closure.

---

## Why this dispatch exists

Per gandalf commission `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` (cited in full as required reading; key context):

Matt direct catch 2026-05-17: "one of the worst parts of [demo v1] was the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls" + "would it make sense for legolas to look for anything that might match to our static dimensions of floors/walls? This could REALLY make the difference in the demo."

Demo v1 shipped with geometrically-drawn placeholders that read as known-low-quality drag in family playtest. Drax v0.12 room/hallway topology committed VS2a to Diablo/PoE-style framing where environmental visual identity is genre-load-bearing. Catalogue research scoped TWO axes (VFX + characters); environment assets were implicit-deferred without being named — P6 pattern instance, filing as **Drift-15** alongside Drift-11A/B + Drift-14.

VS2a-gating per gandalf logic: shipping end-game-anchored playtest with geometric environment placeholders alongside Drift-14 canonical-bias closure + Path A-prime sprite scales + ARPG room/hallway topology would be incoherent. Closure bounded (5-8h legolas + 2h gandalf framework + 30 min Matt selection + 3-5 day drax integration as separate downstream).

## Knight-rider amendments over gandalf commission (4 items, Matt-authorized)

These amendments operationalize Matt's "exactly fit the pre-determined demo dimensions" + "Each room can be different, they don't have to fit together per say" framing surfaced 2026-05-17. Gandalf's commission captured SINGLE-TILE dimension compatibility; these amendments capture ROOM-DIMENSION-FILL CAPACITY and broaden sourcing taxonomy.

### Amendment 1 — Three-category sourcing taxonomy

Gandalf's commission scoped "tilesets" implicitly. Matt's framing surfaces three sourcing categories: **Maps / Background pieces / Tilesets**.

- **MAP** — full room-sized image shipped as single asset (e.g., a 1440×1440 px painted scene)
- **BACKGROUND_PIECE** — large background panel filling significant portions of a room (e.g., parallax layers, half-room paintings, room-portion panels that compose with other assets)
- **TILESET** — small repeating units (32×32 / 48×48 / 64×64 / 96×96) intended to tile across the floor + wall surface
- **MIXED** — pack ships both tileset + complementary larger pieces (e.g., a tileset with a few drop-in room-feature backgrounds)

Per-pack JSONL field: `sourcing_category` ∈ {MAP, BACKGROUND_PIECE, TILESET, MIXED}.

Maps and Background pieces are first-class candidates — not secondary to tilesets. Some HD-2D-register packs ship as painted room scenes rather than tilesets; these may be IDEAL fits because each room can be visually distinct without per-room tile-coherence engineering.

### Amendment 2 — Room-dimension-fit verification field

Per-pack JSONL field: `room_dimension_fit` ∈ {EXACT_FIT_SMALL, EXACT_FIT_DEFAULT, EXACT_FIT_LARGE, MULTI_BAND, UNDER_VARIETY}

Annotation rules:
- **EXACT_FIT_SMALL:** pack can fill a 720×720 px room (15m × 15m at 48 px/m)
  - For MAP/BACKGROUND_PIECE: ships at 720×720 px directly OR at integer-scale-factor reaching it (e.g., 360×360 at 2× upscale; 1440×1440 cropped)
  - For TILESET: ships ≥4 distinct floor tile variants + ≥4 distinct wall tile variants for credible 15m room without obvious repetition
- **EXACT_FIT_DEFAULT:** pack can fill a 1440×1440 px room (30m × 30m at 48 px/m)
  - For MAP/BACKGROUND_PIECE: ships at 1440×1440 px directly OR at integer-scale-factor reaching it
  - For TILESET: ships ≥8 distinct floor tile variants + ≥6 distinct wall tile variants for credible 30m room
- **EXACT_FIT_LARGE:** pack can fill a 2160×2160 px room (45m × 45m at 48 px/m)
  - For MAP/BACKGROUND_PIECE: ships at 2160×2160 px directly OR at integer-scale-factor reaching it
  - For TILESET: ships ≥12 distinct floor tile variants + ≥8 distinct wall tile variants + at least some prop variety for credible 45m room
- **MULTI_BAND:** pack cleanly covers ≥2 of the three bands (most desirable for per-season flexibility)
- **UNDER_VARIETY:** tileset packs with too few variants for credible default-room fill; flag for VS2b expansion candidacy only OR small-room-only candidacy

Tile-variety floors (≥4 / ≥8 / ≥12) are hand-curated heuristics; flag the actual variant count per pack in the JSONL `tile_variant_counts` field so gandalf can refine thresholds during Track B framework authoring.

### Amendment 3 — "Each room independent" framing

Matt's "Each room can be different, they don't have to fit together per say" removes a constraint legolas might otherwise impose (multi-room-coherence). Do NOT hunt for packs where multiple rooms tile coherently OR where wall tiles compose with floor tiles across room-boundaries.

Each room is an independent visual treatment. A pack that ships ONE great-looking 1440×1440 painted scene that works for ONE room type is valid; a pack that ships tile families intended for multi-room dungeon-coherence is also valid; both are first-class.

This simplifies the audit — broaden the candidate net rather than narrowing it.

### Amendment 4 — Per-pack room-dimension-fit annotation in scout doc

In the scout doc summary table (top 5-10 candidate packs), per-pack rows must include:
- Sourcing category (MAP / BACKGROUND_PIECE / TILESET / MIXED)
- Room-dimension-fit tag (EXACT_FIT_SMALL / EXACT_FIT_DEFAULT / EXACT_FIT_LARGE / MULTI_BAND / UNDER_VARIETY)
- Tile variant counts (for TILESET/MIXED categories)
- Native asset dimensions in pixels (for MAP/BACKGROUND_PIECE categories)

This lets gandalf Track B framework + Matt Track C selection consume room-dimension-fit signal directly without re-derivation from raw catalogue data.

## Cross-seam contract change?

**Round-trip: not applicable** — research output is a doc + JSONL; no schema or contract change; no production state modified. Per R11(b) Principle 6.

## Coordination with in-flight work

- **Gamora Gate 3b sim MS consumption (in-flight):** unrelated seam (simulation); no conflict.
- **All other Day-4 cascade items:** RETURNED (drax Case A + Case D + gandalf Track B + legolas Track A original + legolas Track A REVERSE).
- **Pool-expansion structural-gate decision (Matt pending):** independent workstream; no sequencing dependency with environment audit.

Per-seam discipline: legolas Track A REVERSE just returned, so legolas is now FREE. This is the only legolas dispatch in-flight after firing.

## What this dispatch produces

### Output 1 — Scout doc

Location: `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md`

Structure (per gandalf commission + amendments):

**Section 1 — Methodology + scope**
- Style register: HD-2D pixel-art (Candidate B per `canonical/story/style-register.md`)
- Three sourcing categories with definitions
- Room-dimension-fit annotation rules (per Amendment 2)
- License criteria (CC-BY or commercial-royalty-free; flag restrictive)
- "Each room independent" framing (per Amendment 3)
- Time-cap honored / not honored

**Section 2 — Vendor-by-vendor scout**

Tier-1 vendors in priority order:
- **Pimen** — already in catalogue; check for environment packs beyond VFX
- **CreativeKind** — already in catalogue for characters/monsters; check for environment packs
- **Ansimuz** — known retro pixel-art vendor; sweep for any HD-2D-shaped sets
- **Pipoya** — RPG tile sets; pixel-art-leaning
- **Foozle** — dungeon tile sets
- **Elthen** — hand-drawn pixel-art vendor (HD-2D-register adjacent); LIKELY-HIGH-FIT per gandalf
- **CraftPix** — mixed register; filter to pixel-art packs only per Drift-13 lesson

Per vendor: top packs identified + characterization summary + sample image URLs / extraction notes.

**Section 3 — Top 5-10 candidate packs (cross-vendor)**

Summary table with rows including per Amendment 4:
- Vendor + pack name + license
- Sourcing category
- Room-dimension-fit tag
- Tile variant counts (if TILESET/MIXED)
- Native asset dimensions (if MAP/BACKGROUND_PIECE)
- Theme hooks (descriptive themes — gandalf will map to season anchors via Track B `primary_fit_seasons` field)
- Coverage enumeration (floor / wall / props / overlays / animated / lighting)
- Sample image URLs or extraction screenshots accessible to gandalf

**Section 4 — Findings-blockers**

If Tier-1 returns insufficient candidates:
- Surface need for paid acquisition (specific packs identified for license/cost)
- Surface need for Tier-2 vendor sweep (specific vendors recommended for follow-on; CodeManu / FrostWindz / BraCKEYs / Pixogen already partially crawled — re-evaluate for environment packs)
- DO NOT crawl Tier-2 in this dispatch — surface as follow-on commission

**Section 5 — Hand-off for gandalf Track B framework**

- Top candidate shortlist ready for `primary_fit_seasons` annotation
- Coverage-completeness summary (which packs have floor+wall+props; which are coverage-partial)
- Per-substrate room-fit summary (per-substrate room-band coverage)
- Any cross-reference to prior catalogue work (VFX vendors that also ship environments — Pimen + CreativeKind in particular)

### Output 2 — Cross-vendor JSONL inventory

Location: `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl`

Per-pack JSONL entries with fields (extends existing catalogue schema):

- Standard: `vendor`, `pack_name`, `pack_url`, `license`, `intrinsic_frame_sizes`, `file_format`
- Gandalf-spec NEW: `primary_fit_seasons` (legolas-tag with descriptive themes; gandalf fills final mapping in Track B), `coverage` (enumeration), `tile_dimensions` (source-tile pixel size + scale-compatibility note)
- Knight-rider-amendment NEW:
  - `sourcing_category` ∈ {MAP, BACKGROUND_PIECE, TILESET, MIXED}
  - `room_dimension_fit` ∈ {EXACT_FIT_SMALL, EXACT_FIT_DEFAULT, EXACT_FIT_LARGE, MULTI_BAND, UNDER_VARIETY}
  - `tile_variant_counts` (per-tile-type variant counts for TILESET/MIXED; null for MAP/BACKGROUND_PIECE)
  - `native_asset_dimensions` (px × px for MAP/BACKGROUND_PIECE; null for TILESET)

## Out of scope (explicit)

- **NO design framework authoring** (gandalf Track B; separate)
- **NO Matt selection** (Track C; downstream after legolas + gandalf complete)
- **NO drax integration** (Track D; separate downstream dispatch knight-rider authors)
- **NO Tier-2 vendor crawling** (surface as follow-on commission if Tier-1 insufficient)
- **NO paid asset acquisition** (Matt action; legolas surfaces candidates)
- **NO music / audio asset sourcing** (separate workstream)
- **NO UI element sourcing** (separate workstream)
- **NO animated environment tiles / interactive environment work** (per gandalf commission "Not animated environments" / "Not interactive environment" framing)
- **NO multi-room-coherent tile-family hunting** (per Amendment 3 — each room independent)
- **NO LLM API touchpoints** ($0 budget)
- **NO time-cap overrun** — 8h hard cap; surface findings + halt if scope exceeds

## Required reading

- **Gandalf commission (primary):** `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` — full context, Drift-15 framing, VS2a-gating rationale, Track A/B/C/D structure
- **Style register:** `canonical/story/style-register.md` — HD-2D pixel-art register + score-don't-filter principle
- **Arena topology:** `canonical/story/arena-room-hallway-system.md` — drax room/hallway topology + 30m default / 15m small / 45m large room dimensions + PIXELS_PER_METER=48 scale anchor + hallway 10-30m length
- **Drift-audit:** `canonical/story/drift-audit.md` § Drift-13 (vendor-mixed-register CraftPix lesson) + § Drift-15 (this audit's pattern)
- **Prior scout docs (methodology reference):**
  - `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md`
  - `agentic_orchestration/research/catalogue/monster-track-vendor-scout-2026-05-16.md`
- **Movement-speed source of truth:** `canonical/story/movement-speed-baseline.md` § Verdict Reversal 2026-05-16 (48 px/m anchor consumed by room dimensions)

## Acceptance criteria

- [ ] Scout doc filed at `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md`
- [ ] Cross-vendor JSONL filed at `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl`
- [ ] Tier-1 vendor sweep complete (Pimen / CreativeKind / Ansimuz / Pipoya / Foozle / Elthen / CraftPix-pixel-only)
- [ ] Three sourcing categories enumerated (MAP / BACKGROUND_PIECE / TILESET / MIXED)
- [ ] Room-dimension-fit annotated per pack (EXACT_FIT_SMALL / EXACT_FIT_DEFAULT / EXACT_FIT_LARGE / MULTI_BAND / UNDER_VARIETY)
- [ ] Top 5-10 candidate packs summary table with all Amendment-4 fields populated
- [ ] Sample image URLs / extraction screenshots accessible to gandalf for visual inspection
- [ ] Coverage enumeration per pack (floor / wall / props / overlays / animated / lighting)
- [ ] License + attribution flagged per pack
- [ ] Findings-blockers surfaced if Tier-1 insufficient (paid acquisition + Tier-2 sweep recommendations)
- [ ] Per-pack `primary_fit_seasons` legolas-tagged with descriptive themes (gandalf fills final mapping)
- [ ] Time-cap honored (≤ 8h hard cap; surface to knight-rider if approaching)
- [ ] Knight-rider notified with: scout doc path, JSONL path, vendor sweep summary (which vendors had high/low/zero environment coverage), top-5 candidate packs with sourcing-category + room-fit + theme summary, findings-blockers if any, time spent

## Tag policy

- **No git tag** (research persona; file timestamp suffices)

---

## Completion record

**Completed:** _<date>_
**Scout doc:** _<path>_
**JSONL:** _<path>_
**Vendors swept:** _<list with high/low/zero env coverage>_
**Top-5 candidates:**
1. _<vendor + pack + category + room-fit + theme>_
2. ...
**Findings-blockers:** _<list or "none">_
**Tier-2 follow-on recommendation:** _<list of vendors / "none needed">_
**Paid acquisition recommendation:** _<list of packs + cost estimate / "none">_
**Time spent:** _<hours>_
**Notes for knight-rider:**
