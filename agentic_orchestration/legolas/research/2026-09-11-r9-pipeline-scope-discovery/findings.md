# Research — R9: SCOPE DISCOVERY for a complete painted-2D ARPG art pipeline — 2026-09-11

**Mode:** A (analytical). **Commissioner:** gandalf (ARCHITECT / RUN-CONDUCTOR, Astra burst lane).
**Brief:** `agentic_orchestration/gandalf/requests/2026-09-11-legolas-mode-a-r9-pipeline-scope-discovery.md`
**Input complemented:** `agentic_orchestration/gandalf/notes/2026-09-11-painted-2d-pipeline-scope-map.md` (v0.1, ~70 scopes / 9 groups) ✓ read first.
**Sibling commission (not duplicated, cited where it composes):** `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` (R6/R7/R8).
**Companion:** `sources.json` (same directory).
**Constraint honoured:** read-only; two focused search passes per thread, then the gap is recorded (§ 5); no paid resources; no images; no code; no sub-agents.

## Grading key (on every claim)

| Grade | Meaning |
|---|---|
| **VERIFIED** | Stated in a primary source I fetched and read this session, quoted. |
| **PRACTITIONER-REPORT** | Published practitioner / community-standard practice or reverse-engineering corpus; real but not measured. |
| **SECONDARY** | Trade-press or community report *about* a primary source I could not open. |
| **UNVERIFIED** | Plausible, named, not evidenced. Includes my own inference — always labelled as mine. |
| **GAP-RECORDED** | Two passes spent, not found. Listed in § 5 with the next source to try. |

**Legend reused from gandalf's map — Gen:** A = Astra generates · D = deterministic tool derives · E = engine/runtime · H = human-authored · A→D = Astra generates, tool derives the usable data · **V = vendor-supplied (may not be generated or drawn)**. **When:** C-1 · C-2 · P · M.

---

## 0. Summary

1. **The map's single most time-critical error is a timing one, and the world moved under it three days before it was written.** OpenAI shipped **GPT-Image-2.5 (Flare + Sunburst) on 2026-09-08**; `gpt-image-1`, `gpt-image-1.5`, `gpt-image-1-mini` and `chatgpt-image-latest` were announced deprecated **2026-06-02 with shutdown 2026-12-01**; `dall-e-2`/`dall-e-3` were announced 2025-11-14 and shut down 2026-05-12. OpenAI's stated floor is *"Generally available models: At least 6 months"* of notice. **VERIFIED.** The map files `model_drift_probe.py` as *"C-1 (define) → P"*. The evidence says it is a **C-1 run item**: the generator is a depreciating asset with a ~6-month observable horizon, and the phenomenon is not hypothetical drift but scheduled retirement.
2. **And the built-in path cannot pin a version at all.** The API path *can*: `gpt-image-2.5-sunburst-2026-09-08` is a dated snapshot and OpenAI states *"Snapshots let you lock in a specific version of the model so that performance and behavior remain consistent."* The lane's F4 lean is **built-in-only** (Codex `image_gen__imagegen`), which exposes no model id, no snapshot, no seed, no size. **Consequence: under F4-built-in there is no model identifier to record in a receipt, so a frozen probe set is not *an* observability mechanism — it is the *only* one.** (VERIFIED on the vendor docs; the consequence is my inference, and it composes with the sibling R6 finding that the API exposes no seed and no `negative_prompt`.)
3. **Our own pipeline destroys the provenance the generator attaches.** OpenAI: C2PA manifests carry `issuer` / `model` / `generated_at`, and *"Editing, converting, or sharing a file can remove its metadata"*; SynthID is an embedded watermark that *"may survive some transformations."* **VERIFIED.** Green-plate matting, atlas packing and downsampling are exactly such transformations. So: capture C2PA **at ingest, before matting**, into the receipt — and expect the shipped sprite to carry a watermark signal even after the metadata is gone.
4. **An entire compliance group is absent from the map.** Steam's **Content Survey** has a mandatory Generative AI Content section; *Pre-Generated* is defined as *"Any kind of content that ships with your game and is consumed by players that is created with the help of AI tools during development"* and requires a developer attestation that the content is not illegal or infringing and is consistent with marketing. **VERIFIED.** This makes the lineage ledger (map 8.9) **externally** load-bearing, not merely internal hygiene: it is the evidence base for a store-page statement.
5. **The map has a colour-vision gate and no photosensitivity gate — in the genre where screen-filling flashes are the core verb.** Xbox Accessibility Guideline 118 gives closed-form thresholds: a flash is *"a 10% change in luminance"*; failure at *"approximately more than three per second"* over *"approximately 20 percent or more"* of the screen; a separate red-flash rule (saturated red where `R/(R+G+B) >= 0.8`, flash when `(R-G-B) × 320 > 20`); and a spatial-pattern rule. **VERIFIED.** Every one of these is computable in numpy on frame sequences we already produce. This is the cheapest high-consequence oracle I found that the map does not have.
6. **`7.3` rests on a precedent that does not exist.** The map says *"D2R re-rendered for 4K."* Blizzard did not re-render sprites: GDC 2022, *An Overview of the 'Diablo II: Resurrected' Renderer* (Kevin Todisco, Blizzard) describes **building a new 3D renderer from scratch** — lighting, skin rendering, **HDR colour grading**, order-independent transparency — over the original game's logic and sprite-driven simulation, with per-animation framerate unlocked on the render layer to preserve feel. **VERIFIED (talk record) + SECONDARY (dev interviews).** The one team that faced "take a pre-rendered sprite ARPG to 4K" concluded the sprite path would not scale and replaced the renderer. **The resolution decision is therefore a mint-time lock with no re-mint path — and § 0.1 says the minting model will be gone before a re-mint could be commissioned.**
7. **Regional content variants are a generated pipeline's cheapest advantage and the map does not tag for them.** Diablo IV's Chinese release replaced blood with *a brown, transparent dust effect*, rebuilt a skeleton boss *out of rock*, and altered skull-bearing icons; WoW China gave skeletons flesh and turned bone markers into graves. **SECONDARY (consistent trade press, multiple outlets).** A human pipeline re-arts these by hand. We can mint a variant — **but only if `content_flags{blood, skeletal, religious_iconography}` is recorded at mint time**, which costs nothing now and is unrecoverable later.
8. **Pairwise frame-similarity is documented as insufficient for the exact job `identity_vector.py` is being asked to do.** *Sprite Sheet Diffusion: Generate Game Character for Animation* (Hsieh, Zhang, Yan; arXiv 2412.03685, Dec 2024 / rev. Mar 2025) is the closest published precedent to our animation problem — generate a character's animation frames from one designed reference. **VERIFIED (title/authors/abstract/framing).** The reported methodological point — that frame-to-frame similarity metrics proved insufficient for subject consistency, so a sheet-level Subject Consistency Score (VBench) was adopted — is **SECONDARY** (the PDF exceeded fetch limits; see § 5). Practitioner literature names the failure modes independently: frame-level flicker, identity drift, warble, motion discontinuity.
9. **Twenty-three scopes are missing or materially under-specified.** They are in § 1. The five that would change C-1 if they were wrong are: model retirement + snapshot policy (A1), reference-image provenance (A5), provenance capture before matting (A3), photosensitivity gate (B1), and the bake-vs-grade decision that sets the plate-library size (C7).

---

## 1. The gap table

> **Reading the table:** *Present?* is against gandalf's map v0.1. "partial" means the words are there but the deliverable, the combinatorics, or the gate is not. Precedents are cited inline; full bibliography in `sources.json`.

### Group A — AI-pipeline scopes

| # | Scope | Present? | Precedent (cited) | Gen | Oracle candidate | Bible field | Run |
|---|---|---|---|---|---|---|---|
| **A1** | **Model *retirement* clock + snapshot-pin policy** (not just drift) | **partial** (8.3 exists, mistimed) | OpenAI Deprecations: `dall-e-2`/`dall-e-3` ann. 2025-11-14 → shutdown 2026-05-12; `gpt-image-1`/`-1.5`/`-1-mini`/`chatgpt-image-latest` ann. 2026-06-02 → **shutdown 2026-12-01** → repl. `gpt-image-2`; *"Generally available models: At least 6 months"*. Models page now lists only **GPT-Image-2.5 Sunburst / Flare**; snapshot `gpt-image-2.5-sunburst-2026-09-08`. **VERIFIED** | D | `model_drift_probe.py` — **deterministic**, frozen probe set, distance-to-approved; alarm threshold set at K1 | `generator.model_id`, `generator.snapshot`, `generator.probe_set_sha`, `generator.observed_fingerprint` | **C-1 (run, not define)** |
| **A2** | **Regeneration shelf-life** — assets are regeneratable only while the minting model lives; approved PNG is the artifact of record | **N** | Same as A1. Corollary is mine. **VERIFIED (facts) / UNVERIFIED (corollary)** | D | `deps_ledger.py` extension: every node carries `regeneratable_until` | `receipt.regeneratable_until` | **C-1 (policy)** → P |
| **A3** | **Provenance capture *before* our own transforms** (C2PA + SynthID) | **partial** (8.6 "C2PA?", 8.9 stamps) | OpenAI content-provenance guide: manifest fields `issuer` ("OpenAI OpCo, LLC") / `model` ("gpt-image") / `generated_at`; *"Editing, converting, or sharing a file can remove its metadata"*; SynthID *"may survive some transformations"*. **VERIFIED** | D | `provenance_capture.py` — read C2PA at ingest; assert receipt carries all three fields; fail closed if absent | `receipt.provenance{issuer,model,generated_at}` | **C-1** |
| **A4** | **Store AI-content disclosure ledger** (what we must be able to *say*, later) | **N** | Steamworks *Content Survey*: mandatory Generative AI section; **Pre-Generated** = *"Any kind of content that ships with your game and is consumed by players that is created with the help of AI tools during development"*; **Live-Generated** = *"…while the game is running"*; attestation that content is not illegal/infringing and is consistent with marketing; policy Jan-2024, clarified Jan-2026 to exempt dev-efficiency tooling. **VERIFIED (doc) / SECONDARY (dates)** | H (statement) + D (ledger) | none — attestation; the ledger is the evidence | `disclosure.pre_generated`, `disclosure.statement` | P (**ledger is C-1**) |
| **A5** | **Reference-image provenance** — what may be fed as `-i` (input hygiene, distinct from output similarity) | **N** | Map 8.6 tests outputs only. Distinction is standard IP practice; the risk asymmetry is my inference. **UNVERIFIED (as a rule) / VERIFIED (that the map omits it)** | H + D | `ref_provenance.py` — every `references[]` entry resolves to a first-party content-addressed asset; no third-party image ever conditions a mint | `receipt.references[].origin` | **C-1** (receipt already records reference roles — near-zero cost) |
| **A6** | **Alpha / matting as a first-class, *model-coupled* stage** | **partial** (G9 dark fringe only) | Lane probe (gandalf's own, this repo): transparent output unreliable under reference conditioning; `gpt-image-2` does **not** support `background=transparent`; GPT-Image-2.5 announcement claims *"better handling of … transparent backgrounds"*. **PRACTITIONER-REPORT (lane) + SECONDARY (2.5 claim)** | D | `matte_quality.py` — edge halo width, chroma spill, alpha-histogram bimodality; **re-run on every drift alarm** | `matting.plate_color`, `matting.tolerance`, `matting.model_coupled=true` | **C-1** |
| **A7** | **Downsample stage as a tell-suppression control** — 627 px native → ~240 px hero | **partial** (7.3 treats it as a decision, not a stage) | R6 sibling finding: HF-energy is the ornament-noise proxy. The stage framing is mine. **UNVERIFIED** | D | run the tell oracles at **display size**, not native; HF-energy cap measured post-resample | `resolution.native_cell`, `resolution.display_target`, `resolution.resample_filter` | **C-1** |
| **A8** | **Temporal coherence / identity drift as its own metric family** (sheet-level, not pair-level) | **partial** (1.2 clip table, 1.5 continuity) | *Sprite Sheet Diffusion* (arXiv 2412.03685) — same problem, one reference → frames. Failure taxonomy (flicker / identity drift / warble / motion discontinuity) is practitioner-standard. **VERIFIED (paper exists, framing) / SECONDARY (the pairwise-insufficiency claim)** | D | sheet-level consistency statistic **alongside** pairwise `identity_vector`; explicit flicker metric (per-pixel temporal variance on aligned masks) | `motion.consistency_floor` | **C-1** |

### Group B — Compliance / platform (the group the map does not have)

| # | Scope | Present? | Precedent (cited) | Gen | Oracle candidate | Bible field | Run |
|---|---|---|---|---|---|---|---|
| **B1** | **Photosensitivity (PSE) gate on VFX and telegraphs** | **N** | **XAG 118** (Microsoft, primary): flash = *"a 10% change in luminance"*, darker value below 0.8; fail at *">3 per second"* over *"~20 percent or more"* of screen; red-flash rule `R/(R+G+B) >= 0.8` and `(R-G-B)×320 > 20`; spatial-pattern rule (>10% band contrast over ~20% screen); tool: **Harding FPA**. *"eliminating game content that can potentially cause photosensitive seizures is preferred over splash-screen warnings."* **VERIFIED** | D | `flash_check.py` — closed-form numpy on any frame sequence; no model, no dependency | `element_palette.flash_policy`, `vfx.max_flash_rate`, `vfx.max_flash_area` | policy **C-1**, gate **C-2** |
| **B2** | **Regional content variants** (CN / DE) tagged at mint | **N** | Diablo IV CN: blood → *"a brown, transparent dust-like effect"*; skeleton boss rebuilt *"made out of rocks"*; skull icons altered. WoW CN: skeletons fleshed, bones → graves. **SECONDARY (multi-outlet, consistent)** | H (policy) + A (variant mint) | `content_flag_coverage.py` — every minted asset carries the flags; variant build asserts zero un-flagged gore | `content_flags{blood, skeletal, religious_iconography}` | **C-2 (tag at mint)** → P (variant) |
| **B3** | **Age-rating content-descriptor ledger** (ESRB / PEGI / USK / AU) | **partial** (8.7 records *refusals*, not *shipments*) | USK is materially stricter on blood/gore and alternate German versions are common; AU Classification Board refusal blocks distribution outright. **SECONDARY** | H | same ledger as B2, different consumer | `content_flags` (shared) | P |
| **B4** | **Small-screen legibility floor** (handheld / Deck) | **N** | Steamworks Deck compatibility review: smallest on-screen font character **never below 9 px at 1280×800**, 12 px recommended; user-configurable text size recommended. **VERIFIED (via Steamworks doc summary)** | D | extend the icon register card with a **minimum-feature-size** check evaluated at 1280×800 scale | `ui.min_feature_px`, `icon_grammar.min_stroke_px` | **C-2** |
| **B5** | **Controller glyph sets — a NEVER-GENERATE class** | **N** | Steam Input exposes `GetGlyphForActionOrigin` / `GetGlyphPNGForActionOrigin`; prompts must come from the live binding, not hardcoded icons. Platform button glyphs are trademarked and vendor-supplied. **PRACTITIONER-REPORT** | **V + E** | `never_generated` list membership check on the asset register | `never_generated[]` | P |
| **B6** | **Store / capsule asset set at exact specs** | **partial** (§9 says "all sizes") | Steamworks store assets: header **920×430**; small **462×174** (auto-derives 120×45 and 184×69); main **1232×706**; vertical **748×896**; page background **1438×810**; ≥5 screenshots ≥1920×1080 16:9; *"your logo should nearly fill the small capsule."* **VERIFIED** | A (art) + H (logo/wordmark stays vector + human) | capsule legibility check at 120×45 (the derived size is where the logo dies) | `marketing.capsule_specs` | M |
| **B7** | **Achievement icon sets** | **N** | Steamworks: each achievement carries an **Achieved Icon** and an **Unachieved Icon**; *"games are limited to 100 achievements at first"* → up to **200 icons** before any profile-feature uplift. **VERIFIED (pairing + cap)**; pixel spec **GAP-RECORDED** (§ 5) | A | icon register card + set-consistency (the same oracles as 5.2 / 6.2) | `icon_grammar.achievement_pair` | P |

### Group C — Technical / runtime

| # | Scope | Present? | Precedent (cited) | Gen | Oracle candidate | Bible field | Run |
|---|---|---|---|---|---|---|---|
| **C1** | **Terrain-transition tile-set combinatorics (autotiling)** | **partial** (3.1 says "transitions") | Blob-47: 8-neighbour bitmask, diagonal gated on both adjacent cardinals → **47 tiles per terrain pair**; marching-squares 4-bit → 16. Supported natively by Godot / Tiled / RPG Maker. **PRACTITIONER-REPORT** | A→D | `autotile_completeness.py` — all required masks present; edge-profile similarity across the whole set | `plate.terrain_sets[]`, `plate.autotile_scheme` | **C-1 (decide)** → P (build) |
| **C2** | **Nine-slice authoring rules for UI panels** | **N** | Godot `NinePatchRect`: corners intact, edges/centre tiled or stretched; TILE mode *"requires seamless textures"*. **VERIFIED** | A→D | `nine_patch_check.py` — stretch/tile regions seam-continuous; ornament confined to corner regions | `ui.nine_patch_margins`, `ui.ornament_zones` | **C-2** |
| **C3** | **Fill-rate / overdraw budget (distinct from memory)** | **N** (7.4 is memory only) | Practitioner budgets: ~500–800 active particles desktop, 150–300 mobile; overdraw dominates translucent-sprite cost; additive cheaper than alpha; **transparent pixels still cost fill rate** → trim empty margins in the atlas. **PRACTITIONER-REPORT** | D | `fill_budget.py` — Σ(alpha-nonzero area × frames × expected concurrent instances) per archetype | `vfx.fill_budget`, `atlas.trim_policy` | **C-2** |
| **C4** | **2D texture import / compression policy** | **partial, and one item is wrong** (7.5 lists Basis) | Godot: VRAM compression *"should be avoided for 2D as it exhibits noticeable artifacts, especially for lower-resolution textures"*; *"Lossless: This is the default and most common compression mode for 2D assets"*; mipmaps in 2D only *"if your project visibly benefits"* (≈33% memory); recommends high base resolution over runtime downscaling; `TextureAtlas` *"reduce[s] memory usage for animated 2D sprites."* **VERIFIED** | D | budget calculator constant fixed at **4 bytes/px (RGBA8)** | `tech.compression_mode`, `tech.mipmaps`, `tech.bytes_per_px` | **C-1** |
| **C5** | **Bake-vs-grade decision for biome mood** | **N** | D2R's bespoke renderer shipped **HDR colour grading** as a named subsystem (GDC 2022). Implication for a painted pipeline is mine: mood baked into plates multiplies the plate library; mood graded at runtime keeps one library + per-biome LUT. **VERIFIED (D2R fact) / UNVERIFIED (implication)** | E + H (LUT) | plate palette distance measured **pre-grade**; LUT round-trip check | `biome.grade_lut`, `plate.mood_baked=false` | **C-1 (decide — it sets plate count)** |
| **C6** | **In-world numeric/label art (damage numbers, ground-item labels)** | **N** | Map 6.4's *"never AI-rendered text"* is right and is not the same as *"this deliverable does not exist."* A bitmap/atlas font with outline treatment readable over painted plates is art, and it meets B4's 9-px floor. **UNVERIFIED (mine), supported by B4** | H → D | min-feature-size check at 1280×800 over the darkest and lightest plates | `ui.numeric_font`, `ui.label_plate` | P |
| **C7** | **Asset-ID stability across regeneration** | **partial** (7.7 / 8.9 give lineage, not slot stability) | Content addressing gives a *version* identity; a regenerated asset gets a new hash while occupying the same slot. **UNVERIFIED (mine)** | D | `deps_ledger.py` keys on `asset_id`, not `content_hash` | `asset_id` (slot-stable) vs `content_hash` (per-version) | **C-1** |

### Group D — Art classes the map does not enumerate

| # | Scope | Present? | Precedent (cited) | Gen | Oracle candidate | Bible field | Run |
|---|---|---|---|---|---|---|---|
| **D1** | Cursor **set** with states (default / attack / talk / loot / invalid) + hardware-vs-software decision | **partial** (named inside 6.1, not scoped) | Game UI Database indexes cursor and HUD classes across 1,300+ games / 55,000+ UI screenshots. **PRACTITIONER-REPORT** | A | icon register card at cursor size | `ui.cursor_states[]` | P |
| **D2** | Loading screens, act-intro plates, narrative panels as a **register of their own** | **partial** (6.5) | Painted story panels are a genre staple (Darkest Dungeon / Hades lineage). **SECONDARY** | A | register card; story review | `registers.narrative_panel` | P / M |
| **D3** | **Ground-item label plates** and rarity-frame art at drop scale | **N** | D2 ground labels are the canonical precedent; a citable primary description was **GAP-RECORDED** (§ 5). **UNVERIFIED** | A + E | contrast-over-plate check | `ui.label_plate` | P |
| **D4** | Photo mode · mod tooling · cosmetic/seasonal sets | **N** (brief named them) | No precedent found within budget — **GAP-RECORDED** (§ 5). **UNVERIFIED** | — | — | — | M / post-P |
| **D5** | **Library assets** (distinct from store capsules) | **partial** (§9) | Store set is specified (B6); the library set is a separate required family — **GAP-RECORDED** (§ 5) | A + H | — | `marketing.library_specs` | M |

### Group E — Process

| # | Scope | Present? | Precedent (cited) | Gen | Oracle candidate | Bible field | Run |
|---|---|---|---|---|---|---|---|
| **E1** | **Approved key/concept frame as a bible-versioned artifact** (not merely an input file) | **partial** (8.2 HITL console gates outputs) | 2026 practitioner reports converge on *"style locks before prompts"*: brushwork, values, materials, palette codified **per biome**; reference-first workflows; prompt packs reused so passes converge. **PRACTITIONER-REPORT** | H + A | the key frame's hash is a bible field; drift probe measures against it | `registers.key_frame_sha` | **C-1** |
| **E2** | **Human paintover — permitted or forbidden, decided explicitly** | **N** | Same corpus: human paintover is reported as *a standard stage* in production AI art pipelines. **PRACTITIONER-REPORT** | H | invalidation graph needs a `human_edited → do_not_regenerate` state either way | `receipt.human_edited` | **C-1 (decide)** |
| **E3** | **`never_generated[]` as one list** (typography, logo/wordmark, platform glyphs, rating icons, licensed fonts) | **partial** (6.4 + §9 only, scattered) | Composition of B5 + map 6.4 + map §9. **VERIFIED (that the components exist) / UNVERIFIED (consolidation)** | H | register-membership assertion at mint | `never_generated[]` | **C-1** |
| **E4** | **Binary-asset repo policy** (LFS / ignore / on-disk budget) | **N** (F8 touches it obliquely) | The lane already holds 2.7 GB with PNGs gitignored (gandalf's own F8). **PRACTITIONER-REPORT (this repo)** | D | disk/ledger reconciliation | `tech.repo_policy` | **C-1 (policy)** |

---

## 2. What I judge WRONG in gandalf's map

**X1 — `7.3`: "D2R re-rendered for 4K" is not what happened, and the correction removes a reassurance.**
GDC 2022, *An Overview of the 'Diablo II: Resurrected' Renderer* (Kevin Todisco, Blizzard) — Blizzard wrote **a new 3D renderer from scratch** (the talk's framing: *"Building a new 3D renderer seems seldom heard of these days"*), covering lighting, skin rendering, **HDR colour grading** and order-independent transparency, layered over the original game's logic; the simulation remains sprite-and-grid driven, and animation framerate was unlocked *on the render layer* to preserve feel. **VERIFIED (talk record) + SECONDARY (developer interviews).**
**Why it matters:** the map implies there is precedent for scaling a pre-rendered sprite corpus to 4K. There is not. The only AAA team that met this exact problem replaced the renderer rather than re-render the sprites — and unlike them, **we will not have the minting model available for a re-mint** (§ 0.1). `7.3` is therefore not "decide the resolution table", it is "**lock the native mint resolution knowing it is unrepeatable.**"

**X2 — `8.3` is filed at the wrong time, and the reason is dated.**
The map files the drift oracle as *"C-1 (define) → P"*. GPT-Image-2.5 shipped **2026-09-08** — the day before the map's companion SPEC and three days before the map. The prior family retires **2026-12-01**. The stated minimum notice is six months. **VERIFIED.** A probe defined-but-not-run through C-1 cannot detect a backend change that is scheduled to happen inside C-1's own calendar. **Move to C-1 run, fired at K1 and at each burst-day boundary.**

**X3 — `8.6` is filed at the wrong time for one of its two halves.**
Output-similarity screening genuinely can wait for C-2 (at C-1 scale there is nothing to cluster). But **reference-image provenance (A5) and the disclosure ledger (A4) are properties of *how each asset was made*** — unreconstructable after the fact. They are C-1 or they are lost. **UNVERIFIED (my judgement), VERIFIED (that the receipt already carries reference roles, so the cost is near zero).**

**X4 — `7.5`: "Basis" does not belong in a 2D compression list.**
Godot's own guidance: VRAM compression *"should be avoided for 2D as it exhibits noticeable artifacts, especially for lower-resolution textures"*; Lossless is *"the default and most common compression mode for 2D assets."* **VERIFIED.** **And this changes 7.4's arithmetic:** the recommended 2D path is lossless-on-disk / **uncompressed RGBA8 in VRAM = 4 bytes/px**, not the ~1 byte/px a block-compressed assumption would give. A budget calculator built on the wrong constant is wrong by 4×, in the unsafe direction.

**X5 — `1.1` / `1.2`: "8 dirs" is a policy, not a precedent.**
D2 animations exist at **1, 2, 4, 8, 16 or 32 directions**, chosen per animation; DCC supports up to 32. **PRACTITIONER-REPORT** (Phrozen Keep / Siramy reverse-engineering corpus). The map's uniform 8 is defensible — but presenting it as inherited from D2 hides the cheapest precedent-backed saving available: low-salience classes (corpses, some overlays, ground items, distant props) ran at fewer directions in the original. Direction count is the largest single multiplier on generation cost in the whole plan.

**X6 — the mode-token list in `1.2` is accurate, and the layer axis it omits is the expensive one.**
NU / WL / RN / A1 / A2 / BL / SC / TH / KK / S1–S4 / DT / DD / GH / TN / TW all check out against the modding corpus (**PRACTITIONER-REPORT**). What the map's clip table does not carry is D2's *second* axis: the **COF composite layer stack** (a COF governs drawing order of several DCCs per unit / mode / weapon-class / direction / frame). The map's 1.4 has slots; the clip table does not cross them. The real D2 matrix is **mode × weapon-class × direction × layer**, and it is the weapon-class axis inside the COF that made D2's inventory large. **This is under-specification, not error** — but `clip_table.json` should carry `weapon_class` as a first-class key now, not later.

**X7 — the map has no consolidated "do not generate" register.** 6.4 (typography) and §9 (logo) each say it locally. B5 adds platform glyphs. Rating icons, platform logos and licensed fonts belong with them. One list, asserted at mint (E3).

**Not wrong, and worth saying so:** `1.10` (hit-flash / outline / shadow are engine, never painted) matches D2's actual construction; `3.4`'s projection-angle oracle has no analogue anywhere I looked and is, as far as this survey can tell, **first-of-kind**; `7.7`'s invalidation graph is the strongest idea in the map and is what makes A2, C7 and E2 cheap to add.

---

## 3. Evidence for the four items the map marks uncertain

**`8.3` model-version drift — VERIFIED, and stronger than drift.** See § 0.1, § 2/X2, A1. Three facts decide it: (a) scheduled retirement with a ≥6-month floor, (b) a new family shipped inside the run's design window with explicitly changed behaviour — *"sharper detail, stronger style adherence, and more control over edits"*, *"more natural lighting, richer textures, and better handling of complex layouts and transparent backgrounds"* (**SECONDARY**, vendor announcement via trade coverage) — and (c) the built-in path exposes **no model identifier at all**, so nothing but a probe set can observe (b) happening.

**`8.6` IP / similarity — split verdict.**
*Tooling:* perceptual hashing is the deployed industry technique for near-duplicate detection (platform-scale precedent); CLIP-embedding distance against an anchor corpus is the published academic approach; a combined RoI + hashing model reports 88.7% infringement identification with false positives cut from 91.8% to 2.8% (**SECONDARY** — abstracts and survey literature, not fetched in full). Both are implementable against a reference corpus; note the sibling R8 finding that **model-backed metrics are a dependency decision on this host, not a free option** (no `torch`, no `onnxruntime`).
*Licence/ToS:* OpenAI's Terms assign output rights to the user and permit commercial use — **but I could not read the primary document: `openai.com/policies/terms-of-use/` and `/policies/row-terms-of-use/` both returned HTTP 403 to two fetch attempts.** Graded **SECONDARY** and recorded in § 5. **Two things Matt should have from the actual document rather than from me:** (i) the standard caveat that a provider assigns whatever rights it has and does not warrant that any exist — material where purely AI-generated works may not be copyrightable; (ii) **the lane authenticates on a ChatGPT subscription, not an API key**, and consumer terms and business terms are different instruments. I flag that, I do not resolve it.
*Provenance:* resolved and actionable — A3.

**`7.3` resolution policy — the precedent is negative (§ 2/X1)**, and one hard external floor exists that the map has no number for: **9 px minimum glyph height at 1280×800**, 12 px recommended (B4). Godot separately advises authoring from a high base resolution rather than downscaling at runtime (**VERIFIED**).

**`7.4` memory / streaming — the constant is wrong before the arithmetic starts (§ 2/X4)**, and the budget is missing its second dimension entirely: **fill rate, not just bytes** (C3). For an ARPG the binding constraint on VFX is overdraw, and the map's N × clips × dirs × frames × layers × 512² formula cannot see it.

---

## 4. What changes in C-1 because of this (15 lines)

1. `model_drift_probe.py` moves from *define* to **run** — fired at K1 and at every burst-day boundary; its probe set is frozen and hashed into the bible.
2. Every receipt gains `generator.observed_fingerprint` (probe-set distance), because under the built-in path **there is no model id to record**; if the paid API path is ever used, record the dated snapshot string instead.
3. Add `provenance_capture` at ingest — read C2PA `issuer`/`model`/`generated_at` **before** matting; our own matting and packing destroy it.
4. Add `ref_provenance` — every `references[]` entry must resolve to a first-party content-addressed asset; no third-party image conditions a mint, ever.
5. Add `matte_quality` to T0 and mark the green-plate decision **model-coupled**: it is re-validated on every drift alarm, not settled once.
6. Run the tell oracles (HF-energy, silhouette read) at **display size**, not at the 627 px native cell.
7. Add a **sheet-level** consistency statistic beside pairwise `identity_vector`; pairwise similarity is reported insufficient for subject consistency.
8. Bible gains `never_generated[]` — typography, logo/wordmark, platform button glyphs, rating icons, licensed fonts — asserted at mint.
9. Bible gains `content_flags{blood, skeletal, religious_iconography}` per asset; costs nothing now, unrecoverable later, and is the whole China-variant option.
10. Bible gains `asset_id` (slot-stable) distinct from `content_hash` (per-version); `deps_ledger.py` keys on `asset_id`.
11. Receipts gain `regeneratable_until`; the approved PNG — not the prompt — is the artifact of record.
12. The 7.4 budget constant becomes **4 bytes/px (RGBA8)** and 7.5 drops Basis for 2D; add a **fill-rate** budget beside the memory budget.
13. `7.3` is locked as an **unrepeatable mint-time decision** (no D2R re-render precedent; no future model to re-mint with), with a 9 px-at-1280×800 legibility floor written into the resolution table.
14. Decide now: **human paintover permitted or forbidden** — the invalidation graph needs a `human_edited → do_not_regenerate` state either way.
15. Decide now: **biome mood baked into plates or graded at runtime** (D2R shipped HDR grading) — it sets the plate-library size before the first plate is minted; and write XAG-118's flash thresholds into `element_palette` while it is still one card.

---

## 5. Knowledge gaps not resolved (two passes each, then recorded)

| Gap | Passes spent | Next source to try |
|---|---|---|
| **OpenAI Terms of Use, primary text** — output ownership, commercial use, non-uniqueness clause | `/policies/terms-of-use/` → 403; `/policies/row-terms-of-use/` → 403 | `openai.com/policies/services-agreement/` and `/policies/service-terms/`; or read the ToS in a browser and quote it into the bible. **Consumer-subscription vs API terms is the open question, not ownership.** |
| **Steam achievement icon pixel spec** | Steamworks achievements doc (pairing + 100 cap confirmed; dimensions absent) | Steamworks *Achievements* → "Setting up achievements" sub-page, or the partner uploader UI |
| **Steam library asset set** (distinct from store capsules) | store/assets/standard fetched (store set confirmed) | `partner.steamgames.com/doc/store/assets/libraryassets` |
| **Supergiant's actual Hades pipeline talk** | two passes; found interviews and an art-book write-up, no GDC pipeline talk | GDC Vault search by speaker; *Art of Hades* book; Jen Zee interview transcript (Game Informer) |
| **Sprite Sheet Diffusion full text** (the pairwise-insufficiency claim + Subject Consistency Score) | `arxiv.org/pdf/2412.03685` exceeded fetch size; abstract page read | `ar5iv.labs.arxiv.org/html/2412.03685`, or the HTML v2 listing |
| **D2 ground-item label rendering** (the label plate under item names) | two passes, community sources only, nothing citable | Phrozen Keep knowledge base; `paul.siramy.free.fr` DC6 documentation |
| **Photo mode / mod tooling as art scopes** | one pass, no precedent surfaced | GDC postmortems by title (e.g. Hades, Darkest Dungeon) rather than by symptom |
| **Per-asset counts for a shipped ARPG** (PoE/D2 icon and sprite inventories) | two passes; only a partial count (246 PoE2 skill-gem icon files on the wiki) | Datamining corpora (PoEDB, spriters-resource indices) — countable, but it is a Mode-B crawl, not a Mode-A pass |
| **PlayStation / Xbox certification art requirements** | not attempted — behind NDA'd partner portals | Out of reach read-only; treat B5/B6 as the public-surface proxy |

---

## 6. Source list

Full machine-readable bibliography with per-source load-bearing quotes: **`sources.json`** (same directory), 26 entries, each graded and stamped with access method and date (2026-09-11).

Primary sources fetched and read this session: OpenAI Deprecations; OpenAI Models index; OpenAI GPT-Image-2.5 Sunburst model page; OpenAI Content-provenance guide; Microsoft Xbox Accessibility Guideline 118; Steamworks Content Survey; Steamworks Store Assets (standard); Steamworks Achievements; Godot `NinePatchRect` class reference; Godot *Importing images*; GDC Vault entry for *An Overview of the 'Diablo II: Resurrected' Renderer*; arXiv abstract 2412.03685.

— legolas (UNKNOWN-RESEARCHER), 2026-09-11. Report what the world contains; the design call is gandalf's and Matt's.
