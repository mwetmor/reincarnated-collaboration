# Legolas commission — Mode B sample crawl, Pimen (first catalogue source)

**Date:** 2026-05-16
**Commissioner:** knight-rider (per Matt's 2026-05-16 directive — first catalogue work now that Gandalf has locked style register, naming triad, court, and enemy visual legibility)
**Mode:** B — systematic catalogue crawl (sample phase)
**Priority:** **HELD** as of 2026-05-16 — see Status block below.
**Output location:** `agentic_orchestration/research/catalogue/pimen/sample-2026-05-16.json` (JSON Lines format recommended)

## Status — RELEASED 2026-05-16

**Knight-rider release signal:** This commission is now ACTIVE. Execute when you have capacity.

**Release context:**
- Elrond's catalogue-rubric work landed (`research/curated/catalogue-rubric-schema.md` + `catalogue-schema.md`)
- Drax wiring-track schema review returned PASS WITH FLAGS — schema is wireable in current demo + loadout state
- Elrond addressed the flags + completed missing artifacts (MIGRATION.md, empty catalogue.db, curation-pipeline.md, pivot-insurance-ledger.md, validation report)
- All gates upstream of this commission are clear

**Tagging note:** the six-axis rubric is at `research/curated/catalogue-rubric-schema.md` and the curator-tagging guide should be alongside. Use those for your style-register classification per asset (axes 1-5 are mechanically checkable; axis 6 derives from the others per Elrond's deterministic rule). The `outline-profile` secondary tag, `quality_flag` for borderline R7 cases, and the `manual-review` escalation path are all documented in the rubric work — read it before crawling.

---

## Why this commission exists

The catalogue-based form-bias resolution path (doc 37 § "Catalogue-based form-bias resolution path") requires populating a catalogue database with structured per-asset metadata sourced from external 2D/3D libraries. Gandalf's 2026-05-15 lock of the **HD-2D-shaped pixel-art style register** (per `canonical/story/style-register.md`) plus the **enemy visual legibility** lock (per `canonical/story/enemy-visual-legibility.md` S1 — sprite-archetype registry sourced from itch.io vendors including pimen) make Pimen the highest-quality first source per Matt's contributed research at `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`.

This is a **sample phase** crawl. Full crawl waits on three-track viability gate (Elrond structural / Drax wiring / Gandalf design) per AGENTS.md.

## Scope — sample only

**Crawl ~20 representative items from Pimen's element spell effect series** spanning style/category variation across the eight elements pimen covers (fire, water, ice, holy, dark, earth, wind, and any additional pimen-produced sets).

**Diversity required in the sample:** the sample MUST span:
- At least 5 of the 8 element packs (fire, water, ice, holy, dark, earth, wind, etc.)
- Both character/enemy assets AND VFX-only assets if pimen produces both
- Both monolithic-atlas-shape and decomposed-spritesheet-shape assets if both exist
- **Free AND paid packs equally** — capture both with full metadata. Decisions about which to acquire happen downstream based on cost/coverage analysis (Elrond + Matt); your job is to make sure paid packs are represented in the catalogue with accurate `cost` field so those decisions are data-grounded. **Do not preferentially sample free assets.**

The intent is to give the viability-gate reviewers (Elrond / Drax / Gandalf) a representative cross-section, not a homogeneous slice — AND give Elrond's eventual cost/KPI analysis comprehensive paid-asset data to work with.

**Cost field accuracy is critical.** Capture: exact price; cost model (per-seat / per-project / one-time / subscription); bundle membership if applicable. For paid packs, also capture per-pack pricing if pricing is pack-level vs per-asset (Pimen tends to sell as packs). This metadata feeds Elrond's downstream cost/coverage KPI work.

## Required metadata per asset (Mode B field specification)

Per `~/.claude/agents/legolas.md` Mode B, each row must contain:

- `asset_id` — pimen's product identifier
- `source` — "itch-pimen"
- `url` — full URL to the asset's pimen/itch.io page
- `name` — pimen's product name
- `category` — `character` / `enemy` / `vfx` / `environment` / `ui` / `audio` / `other`
- `dimensionality` — `2d` (Pimen is 2D pixel-art)
- `style_register` — your assessment: `pixel-art` likely, but inspect each asset's fidelity register and flag if any read as `hand-drawn-pixel` (HD-2D-shaped per Gandalf's lock) vs `retro-pixel-art` (lower fidelity register that does not match the lock)
- `style_tags` — secondary tags (e.g., `retro`, `anime-influenced`, `dark-fantasy`, `cartoony`, `mythic`)
- `decomposition` — for character/enemy: `monolithic` / `decomposed` / `partial` / `unknown`. **Critical for Drax's wiring viability assessment** — flag this carefully per asset.
- `file_format` — PNG / sprite sheet / Aseprite source / etc.
- `license` — pimen's license terms per the asset's page (typically royalty-free commercial; verify per asset)
- `cost` — numeric price; 0 for free
- `crawl_date` — 2026-05-16

**Plus one Pimen-specific additional column worth capturing:**

- `pimen_element` — the element pack the asset belongs to (`fire` / `water` / `ice` / `holy` / `dark` / `earth` / `wind` / etc.) — useful for downstream element-coverage analysis. Treat as a `style_tags` extension or as a separate column at your discretion.

## Constraints

- **Read-only across all sources.** Public web only. Respect robots.txt and rate limits (default: 1 request per 2 seconds).
- **No fabrication.** If a field is genuinely unknown from inspection, leave it null and flag in an `extraction_notes` column. Do NOT guess license or cost.
- **Time-bound:** ~1-2 hours of Legolas work for sample-phase. This is a quick representative crawl, not a deep dive.
- **Append-only.** Output is JSON Lines (one JSON object per line) at `research/catalogue/pimen/sample-2026-05-16.json`. New samples (if needed) get new files; don't overwrite.

## Out of scope

- **Full crawl of pimen's catalogue.** This is sample only. Full crawl waits on viability-gate green-light.
- **Other sources.** Even if pimen's page links to other vendors (Elthen, LuizMelo, etc.), don't follow. One source per commission.
- **Asset download.** This is metadata extraction. Do not download the actual asset files. URLs in the output are sufficient.
- **Curation.** Raw extraction only. Elrond curates separately.

## What happens after this sample lands

1. **Knight-rider** receives the sample completion signal
2. **Three-track viability gate** invoked:
   - **Elrond — structural track** (metadata completeness, schema-fits-his-DB-design, license clarity, decomposition signal coherence)
   - **Drax — wiring track** (Pixi.js consumption viability; sprite-sheet shapes; decomposition sufficient for animation rigging)
   - **Gandalf — design track** (thematic coherence; style-register match to the locked HD-2D-shaped register OR reasonable-pivot-target; aesthetic quality for the Court-tier presentation)
3. **Verdict** — pass / conditional / fail. Pass → full pimen crawl green-lit. Conditional → adjust extraction strategy + re-sample. Fail → skip source; Elrond logs rejection rationale; next source moves up.

## Required reading

- `~/.claude/agents/legolas.md` — your own definition; Mode B field specification + score-don't-filter principle
- `canonical/story/style-register.md` — Gandalf's locked register (for tagging context; remember score-don't-filter — you don't restrict by it)
- `canonical/story/enemy-visual-legibility.md` § S1 — informs monster-sprite-specific considerations
- `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — contextual research that informed Pimen as first source

## Completion record

**Completed:** 2026-05-16
**Agent:** legolas

### Output path

`agentic_orchestration/research/catalogue/pimen/sample-2026-05-16.json`

### Assets sampled: 20

All 20 lines valid JSON. Validated with Python json.loads pass.

### Element-pack coverage achieved

| Element | Packs sampled | Free tier | Paid tier |
|---|---|---|---|
| fire | 2 (Fire 01, Fire 03) | Fire 01 | Fire 03 ($3) |
| water | 2 (Water 01, Water 03) | Water 01 | Water 03 ($3) |
| ice | 2 (Ice 01, Ice 02) | Ice 01 | Ice 02 ($4.99) |
| holy | 1 (Holy) | — | Holy ($4.99 min) |
| dark | 1 (Dark) | — | Dark ($4.99 min) |
| earth | 2 (Earth 01, Earth 03) | Earth 01 | Earth 03 ($3) |
| wind | 2 (Wind 01, Wind 03) | Wind 01 | Wind 03 ($3) |
| thunder | 2 (Thunder 01, Thunder 03) | Thunder 01 | Thunder 03 ($3) |
| acid | 1 (Acid) | partial (VFX 01-02 only) | Full ($4.99) |
| multi | 1 (Mega Pack 01) | — | $12.75 |
| status/buff | 1 (Buff n Debuff 01) | — | $2.55 |
| battle/impact | 1 (Battle VFX Hit Spark) | — | $4.25 min |

**8 of 8 pimen primary elements covered** (fire, water, ice, holy, dark, earth, wind, thunder/lightning). Acid captured as 9th element.

### Category coverage

- **VFX-only assets:** 17 of 20
- **Enemy character:** 1 (Fantasy Skeleton Enemies)
- **Player character:** 1 (Fantasy Platformer Character)
- **Mixed VFX + enemy character:** 1 (Earth Spell Effect 03 — bundled Earth Elemental character)

### Price tier coverage

- Free (NWYP, no minimum): 8 assets
- Paid tier $2.55–$4.99: 9 assets
- Bundle tier $12.75: 1 asset (Mega Pack)
- Partial-free freemium: 2 assets (Acid, Battle VFX Hit Spark)

### Decomposition signal

**VFX assets (17):** decomposition = `not-applicable`.

**Character/enemy assets (3):**
- Fantasy Skeleton Enemies: `monolithic` — confirmed explicitly. Single spritesheet per character, body/weapon baked. Aseprite source not included.
- Fantasy Platformer Character: `monolithic` — inferred. Aseprite source not listed.
- Earth Spell Effect 03 Earth Elemental: `unknown` — embedded in VFX pack, likely monolithic per pimen pattern.

**Flag for Drax:** All confirmed character/enemy sprites are monolithic. Battle VFX Hit Spark and Mega Pack 01 are the only assets with Aseprite source files included — wiring advantage for those two.

### Resolution band coverage

9 assets confirmed `hd2d-pixel`; 11 assets `unknown` (canvas dims not listed on free pack pages). No retro or narrative-pixel band confirmed at pack level; outlier effects (16x16) within hd2d-pixel-primary packs noted.

### Palette/shading/linework axes

All 20: `palette_size`, `shading_technique`, `linework_style` = `unknown`. Visual inspection of actual sprites required during Elrond's curation pass. Inference (not recorded as values): paid packs with high frame counts likely carry `expansive` palette and `gradient-ramp` shading based on VFX libraries research classification.

### Extraction difficulties

1. Free packs do not list canvas dimensions — 11 `resolution_band: unknown` results.
2. Freemium pricing on Acid and Battle VFX Hit Spark — full-pack cost recorded, partial-free noted in extraction_notes.
3. Sale prices at crawl time: Buff n Debuff 01 ($2.55 vs $3.00 base); Mega Pack ($12.75 vs $15.00 base).
4. Water Spell Effect 02 returned a network fetch error — not included; water coverage is adequate from Water 01 and Water 03.

### Flag-worthy observations for viability-gate reviewers

**For Elrond:**
- 11/20 assets have `resolution_band: unknown` — primary curation gap.
- Holy and Dark are highest-quality free-pack documentation in sample (explicit frame counts + canvas dims for all effects).
- Acid freemium: VFX 01-02 free only; full 15 effects at $4.99.

**For Drax:**
- Character sprites: monolithic, no Aseprite source. Not re-riggable without manual slicing.
- Battle VFX Hit Spark: Aseprite with per-part layers — palette swap and layer manipulation possible.
- Mega Pack 01: Aseprite source for all 9 element packs — highest wiring-value single purchase.
- Ice Spell Effect 01: distributes individual frames (not pre-built spritesheet) — extra atlas-assembly step for Pixi.js.
- Non-square canvas shapes in Dark Spell Effect (32x48, 72x32) and Water 03 (64x48, 96x64, 48x80) — may need padding in texture atlases.

**For Gandalf:**
- Earth Spell Effect 03 bundles a full Earth Elemental enemy character — suggests pimen has enemy character coverage beyond the explicit character packs. Worth a targeted follow-on crawl of pimen enemy sprites.
- Wind Spell Effect 01 uses green (nature/druidic) coloring — may not match Reincarnated's neutral-air wind palette expectation.
- Acid element: cross-reference against Reincarnated's canonical element vocabulary needed (acid may map to earth-acid or cipher variant).
- Sub-register: paid tier-03 packs assess as `hand-drawn-pixel` (consistent with locked register). Free tier-01 packs are sub-register-uncertain — possibly retro-pixel. Visual confirmation needed.

### Ready-for-viability-gate signal

**READY.** Sample filed at `research/catalogue/pimen/sample-2026-05-16.json`. All 20 assets extracted and validated. Element diversity (8/8 primary), price tier diversity, and category diversity (VFX + enemy + character) requirements met. Awaiting three-track viability gate: Elrond (structural) / Drax (wiring) / Gandalf (design).
