# 2026-05-17 — elrond — Icon + interactable-prop curation (QUEUED — auto-fires after legolas-1 crawl lands)

**Authority:** Matt L3 2026-05-17 (~21:30 EDT). Commission queued; auto-fires when legolas icon/prop crawl completes.
**Type:** Pattern B — curation + subset selection (~0.5-1 day; data-steward work in elrond's seam).
**Predecessor (gates auto-fire):** legolas icon + interactable-prop catalogue crawl (`agentic_orchestration/dispatches/2026-05-17-legolas-icon-and-prop-catalogue-crawl.md`).

**Status:** 🟡 **QUEUED — DO NOT EXECUTE until legolas-1 ships completion record.** Knight-rider will activate when legolas-1 lands.

---

## Why this matters

Same pattern as elrond's Pimen subset selection that shipped today: consume legolas's raw catalogue and produce a curated subset + manifest that downstream consumers (drax for eventual demo integration) can wire directly. The 9 asset categories Matt named have different curation logics (floor loot needs rarity-tier coverage; ambient props need interaction-state coverage; UI icons need clean register coverage), but the curation discipline is consistent.

---

## Required reading (when activated)

1. Legolas icon + interactable-prop crawl output at `agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/` (floor-loot.jsonl + ambient-props.jsonl + ui-icons.jsonl + summary.md)
2. `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf sizing canon (your curation criterion alongside legolas raw catalogue)
3. `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` — your own Pimen pattern (template for this commission's output)
4. `reincarnated-demo/public/assets/` — current acquired inventory (for gap-vs-existing analysis)

---

## Scope

### Item 1 — Per-sub-asset-class subset selection

Three parallel subsets, one per legolas sub-asset-class:

**Subset A — Floor loot:**
- Per-rarity-tier coverage matrix (white / magic / rare / unique)
- Per-gear-type coverage (sword / staff / bow / etc; helm / chest / boots / etc)
- Potion variants (health + mana; multiple fill levels if available)
- Gold pile size variants
- Identify GREEN cells (clean attribution, sized to canon), YELLOW (CC-BY upgrade candidates), RED (no coverage; acquisition target)

**Subset B — Ambient interactable props:**
- Per-prop-type coverage (chest / coffin / stand / urn)
- State coverage per prop (open / closed / destroyed where applicable)
- Variant coverage (small / medium / large; visual diversity)
- Same GREEN/YELLOW/RED matrix

**Subset C — UI icons:**
- Gear icon per type per rarity matrix
- Potion icon variants
- Gold icon
- Clean register (pixel-perfect at-rest; UI-tier not world-tier)
- Same GREEN/YELLOW/RED matrix

### Item 2 — Manifest authoring

Three manifest files at `agentic_orchestration/research/curated/`:

- `floor-loot-subset-vs2a-2026-05-17.jsonl`
- `ambient-props-subset-vs2a-2026-05-17.jsonl`
- `ui-icons-subset-vs2a-2026-05-17.jsonl`

Schema-match elrond Pimen pattern (asset_id / vendor / category / subcategory / specific_type / rarity_tier / pixel_size / attribution_class / pack_origin / cost_usd / encounter_compatibility (if relevant) / render_notes).

### Item 3 — Acquisition shortlist + summary doc

Author `agentic_orchestration/research/curated/icons-and-props-subset-vs2a-selection-2026-05-17.md`:

1. Executive summary per sub-asset-class
2. Coverage matrix per sub-asset-class (GREEN / YELLOW / RED)
3. Gap closure status (which RED cells become acquisition targets)
4. Acquisition shortlist (cost + vendor links from legolas) — for Matt's eventual review
5. Manifest references (paths + row counts)
6. Cross-references to gandalf sizing canon + legolas crawl

### Item 4 — Cross-seam handoffs

- **Drax:** manifest paths for eventual demo integration (post-VS2a M5 panel redesigns + ambient prop dispatches)
- **Matt (PARKED):** acquisition shortlist requires Matt sign-off on new vendor commissions

### Item 5 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry + HANDOFF → drax + HANDOFF → matt (PARKED for acquisitions)
- No tag (curation work; not code; standard authoring discipline applies)

---

## Out of scope (DO NOT)

- ❌ DO NOT commission new vendor crawls without Matt sign-off
- ❌ DO NOT modify the legolas crawl output (consume only)
- ❌ DO NOT touch drax's ingest pipeline or wiring code
- ❌ DO NOT pre-empt drax M5 panel redesigns or any post-VS2a integration work
- ❌ DO NOT extend to character/monster/VFX assets (separate scope)

---

## Acceptance criteria (when activated)

- [ ] Floor-loot subset manifest authored
- [ ] Ambient-props subset manifest authored
- [ ] UI-icons subset manifest authored
- [ ] Per-sub-asset-class coverage matrix (GREEN/YELLOW/RED)
- [ ] Acquisition shortlist with cost + links
- [ ] Summary doc authored
- [ ] Hive-log STATE + HANDOFFs

---

## Coordination

- **AUTO-FIRE TRIGGER:** legolas icon + interactable-prop catalogue crawl ships completion record. Knight-rider monitors and spawns elrond agent at that time.
- **Parallel-safe with legolas-2 (broader 2D/sprite catalogue survey):** they target different scopes; no overlap in vendor coverage
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3. ~0.5-1 day when activated. Append completion record when done.*
