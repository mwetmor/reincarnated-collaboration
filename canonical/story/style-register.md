# Reincarnated — Visual Style Register

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Status:** **Canonical. Locked 2026-05-15 by Matt** in Pattern B dialogue with gandalf. Authored 2026-05-15 by gandalf with empirical grounding from `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (Legolas-filed catalogue research, Matt-contributed).

This is the project's **canonical visual style register** — the load-bearing reference for catalogue work, demo2 development, LLM image generation, Court / Spirit Guide presentation, and all downstream visual-asset decisions. Pivoting the register later is possible because Elrond's catalogue is score-don't-filter (per AGENTS.md § "Score-don't-filter principle"), but pivots are operationally expensive once content has been generated against a locked register.

**The locked decision:** **Hand-drawn pixel-art (HD-2D-shaped) as the single canonical register.** Rationale below.

**Pending:**
- knight-rider to draft a decisions-log entry capturing the lock (per ADR-002; cross-seam by nature — affects Legolas catalogue, Drax demo, Star-lord LLM image generation, future commission scoping)
- This doc is the canonical reference until the decisions-log entry lands; afterward, the decisions-log entry is the primary lock and this doc is the design-intent expansion

**This doc supersedes:** any implicit register defaults inherited from demo1's existing Pixi.js + Super Pixel Effects tooling (which operates in a *retro pixel-art* register that the proposal below moves away from).

**Companion docs:**
- `cosmology-reincarnated.md` — what the register renders (the cosmological frame)
- `court-of-forms.md` — where the register matters most at endgame (Court presentation)
- `enemy-visual-legibility.md` — load-bearing requirement on the register (see § "Enemy-legibility cross-reference" below)
- `gandalf-design-lineage.md` Layer 2 + 5 — Diablo / isekai aesthetic precedents
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — the empirical asset landscape

---

## TL;DR

**Lock: hand-drawn pixel-art in an HD-2D-shaped register.** Single register throughout — combat VFX, character sprites, Court portraits, Spirit Guide presentation, Trial cinematic frames, ascension cutscenes. Within-frame consistency preserved (per the style-coherence finding from catalogue research). Isekai-genre-positioned visually (per pitch). Operationally manageable for solo/family pace. Asset-library-supported (CreativeKind hand-drawn pixel sets; itch.io HD-2D-adjacent vendors).

This is **not** retro pixel-art (the current demo1 default). This is **not** anime hand-drawn 2D (the pure-isekai register; operationally infeasible at family pace). This is the **shipped middle ground that Octopath Traveler / Triangle Strategy / Live A Live HD-2D Remake / Eastward use**: pixel-resolution sprites rendered in a hand-drawn-illustration register, often paired with detailed environmental art and lighting.

---

## Why this is a senior-design call

Per my agent definition: *"The locked register becomes a consumption-time filter on the catalogue data (not a crawl-scope constraint — see Legolas / Elrond). Pivoting the register later is possible because the catalogue is scored, not pre-filtered."*

The style register's downstream impact:

1. **Catalogue scoring** — Elrond's curation tags each asset with its style register. Once locked, the catalogue's consumption-time filter on this register determines which assets surface to Drax's demo pipeline. Other-register assets stay in the catalogue (for pivot insurance) but don't surface by default.
2. **Demo2 development** — Drax's next iteration inherits the locked register. Demo1 currently operates in retro pixel-art via Super Pixel Effects pack; the locked register may require pipeline adjustment.
3. **LLM image generation** — Star-lord's `visual_prompt` work (file 19 § Phase 02) needs the register as a prompt-construction parameter so generated images cohere across calls.
4. **Court / Spirit Guide design** — `court-of-forms.md` C2 (navigable spatial presentation) and the Spirit Guide's translucent-partial-presence presupposes a renderable register. Lock unblocks design intent.
5. **Pitch positioning** — per `pitch-2026-05-18/one-pager.md`, Reincarnated positions as "isekai mobile ARPG." The visual register must read as isekai-coded, not indie-coded. Pixel-art is genre-ambiguous; hand-drawn pixel-art (HD-2D) is closer to genre-correct.

This is exactly the kind of decision that drifts unobstructed if not named — Discipline #13 territory. **The current demo1 register is retro pixel-art by inheritance, not by canonical decision.** Naming the register canonically (whether to confirm retro or to move to HD-2D or to commit to something else) protects against silent drift.

---

## The empirical asset landscape

Summarized from the Legolas-filed catalogue research (2026-05-16-pixijs-compatible-2d-vfx-libraries.md):

**Volume is in pixel-art.** itch.io (the largest single repository) is dominated by pixel-art vendors — pimen, ansimuz, Pipoya, Foozle, Frostwindz, unTied Games, Elthen, ppeldo, LuizMelo. OpenGameArt.org is CC-licensed pixel-art-leaning. CraftPix has some vector packs.

**Within pixel-art, there are sub-registers.** The research distinguishes:
- *Retro pixel-art* — ansimuz, Pipoya, Foozle — 16-bit-shaped, low-resolution, classic indie register
- *Hand-drawn pixel-art* — CreativeKind, Elthen — higher-fidelity pixel-art with hand-drawn illustration sensibility
- *Higher-resolution pixel composites* — pimen's spell effect series — animation-rich, mid-fidelity

**Hand-drawn anime / vector / HD raster:** poor asset-library coverage. CraftPix has vector packs (scale cleanly but indie-coded); CreativeKind has hand-drawn (pixel-bound, not anime-bound). For a fully hand-drawn anime register, the project would commission OR LLM-generate every asset, not pull from libraries.

**Tier-1 element coverage** (multiple full packs from multiple vendors): Fire, Ice, Lightning, Water, Earth, Wind, Holy, Dark, Poison, Explosions. All buildable from the catalogue. Doc 37 § 6 cipher novel-variants (vacuum, plasma, void, cosmic) have viable representation via palette-shifts and composites of the Tier-1 set.

**The style-coherence finding (load-bearing):**

> *"The libraries above are predominantly pixel art style. If your engine is targeting higher-fidelity 2D (hand-drawn, vector, or HD raster), you'd want to filter more aggressively toward CraftPix's vector packs and CreativeKind's hand-drawn sets, and away from the retro pixel vendors. The style coherence problem we discussed earlier applies: mixing pixel-art VFX with hand-drawn characters reads badly. Pick a style register first, then curate within it."*

**This finding is what reshaped my proposal between Phase 2 and this doc.** In Phase 2 I sketched an "intentional-hybrid: pixel-art base + hand-drawn anime story moments" pattern. The catalogue research surfaced that within-frame mixing of pixel and hand-drawn reads badly. The proposal below resolves that.

---

## The candidate space

Four registers were considered seriously:

### Candidate A — Retro pixel-art (current state by inheritance)

- **Pros:** lowest cost; highest consistency; demo1's existing register; mobile-friendly; Tier-1 asset library support is extreme (the bulk of itch.io is here).
- **Cons:** indie-coded, not isekai-genre-native; positions Reincarnated against shipped indie-ARPGs (Hades / Crawl / Caves of Qud) rather than against isekai games (which are overwhelmingly anime-coded); narrative moments (Trial choice, ascension, Court portraits) lack visual weight at this fidelity; LLM image generation in retro-pixel register is *poor* (LLMs do not generate clean retro pixel well).
- **Shipped precedent:** Stardew Valley, Hyper Light Drifter (closer to hand-drawn pixel), Dead Cells, Crawl.

### Candidate B — Hand-drawn pixel-art (HD-2D-shaped) ← **RECOMMENDED**

- **Pros:** isekai-genre-readable (pixel sprites in hand-drawn illustration register; Octopath Traveler / Triangle Strategy / Live A Live HD-2D Remake all sit here and are JRPG/isekai-adjacent); single register avoids style-coherence problem; asset-library supported via CreativeKind + pimen + the higher-fidelity end of itch.io; narrative moments render with weight at this fidelity (Court portraits are *hand-drawn pixel portraits*, not raster anime, preserving consistency with combat sprites); LLM image generation in hand-drawn pixel register is *feasible* (LLMs handle "hand-drawn pixel game art" prompts well).
- **Cons:** higher per-asset cost than retro pixel-art (CreativeKind packs ~$5-15 each vs Pipoya / Foozle free or near-free); transition from demo1's retro-pixel register to HD-2D requires sprite refinement; LLM consistency requires careful prompt-engineering / style-reference-image discipline; the register's mid-fidelity may not satisfy players expecting either Hades-quality 2D or Diablo-quality 3D.
- **Shipped precedent:** Octopath Traveler (Square Enix HD-2D pattern); Triangle Strategy; Live A Live HD-2D Remake; Eastward; CrossCode; Sea of Stars.

### Candidate C — Pure hand-drawn 2D anime

- **Pros:** isekai-genre-native (this is the anime register); maximum narrative weight; matches the genre's mainstream-medium register (anime / manga / light novel illustration); Hades-quality possible if executed.
- **Cons:** **operationally infeasible at family/solo pace.** Hand-drawn anime at full coverage requires either commissioned artists (prohibitive at scale) or LLM-image-generation with severe consistency-engineering overhead (current LLM models drift between calls). Asset library coverage for this register is poor. Demo1 pipeline replacement is required. Per-season visual-asset budget would jump by an order of magnitude.
- **Shipped precedent:** Hades (Supergiant; 20-person team over years); most anime visual novels and JRPG-with-anime-cutscenes patterns.

### Candidate D — Vector / clean-line

- **Pros:** scales cleanly across resolutions; LLM-image-generation handles vector cleanly; mobile-friendly; relatively low cost.
- **Cons:** indie-coded toward Slay-the-Spire register, not isekai; narrative weight at moments is structurally limited (vector is *clean*, not *emotional*); asset library coverage is thin compared to pixel.
- **Shipped precedent:** Slay the Spire, Monument Valley, Mini Metro.

---

## The proposal

**Lock Candidate B: hand-drawn pixel-art (HD-2D-shaped) as the single canonical visual register.**

### What this means in practice

**One register throughout.** Combat, world, characters, VFX, Court portraits, Spirit Guide presentation, Trial cinematic frames, ascension cutscenes, UI chrome — all in the same register. This honors the style-coherence finding from the catalogue research and avoids the within-frame mixing problem.

**Within the single register, two fidelity tiers** (separated by *moment*, not by *style*):

- **Combat tier** — sprite-sheet animations at the pixel resolution typical of itch.io higher-fidelity vendors (CreativeKind, pimen, Elthen, Foozle's higher-fidelity packs). Animation-ready. Hand-drawn illustration sensibility within pixel constraints. This is what the player sees during seasonal-journey play, in seasonal-dungeon combat, on the HUD.
- **Narrative-moment tier** — higher-resolution hand-drawn pixel portraits + cinematic frames, used at full-screen-takeover moments (Court entry, Trial choice screens, ascension cutscene, third-faction reveals). Still pixel-bound; just zoomed-in fidelity. Octopath Traveler's character-introduction frames are the closest shipped precedent — same register as gameplay, larger canvas, more detail.

The two tiers are **the same register** — only the resolution and the asset-canvas-size differ. There is no within-frame mixing. The player sees register-consistent art throughout.

### What this rules out

- **Retro / 16-bit pixel-art register** as the canonical register. Demo1's current Super Pixel Effects sourcing is acceptable for transitional development but not the canonical target. Future asset selection (and the Phase-1 demo2 pipeline) should reach for the higher-fidelity hand-drawn pixel register.
- **Hand-drawn 2D anime** outside the pixel-grounded register. No raster anime portraits; no anime cinematic art; no hybridization with pixel-art frames. The isekai-genre register is acknowledged as the genre's mainstream-medium register, but Reincarnated commits to its game-medium variant of that register (HD-2D pixel) rather than to anime fidelity.
- **Mixed-register frames.** No frame ever contains both pixel-art and hand-drawn anime elements. The Court portrait is pixel; the combat scene is pixel; the Trial choice screen is pixel; the ascension cutscene is pixel. All hand-drawn-illustration-coded; all pixel-resolution.

### Per-embodiment register awareness

The locked register applies to all embodiments. A humanoid form renders in HD-2D pixel; a slime form renders in HD-2D pixel; a swarm form renders in HD-2D pixel; a dragonling form renders in HD-2D pixel; a cloud-being renders in HD-2D pixel. The register is form-agnostic at the visual layer. **Embodiment variance happens within the register** (different sprite shapes, different animations, different palette work) not across registers (different forms don't get different fidelity treatments).

This honors doc 37's form-bias structural-realignment work — the visual register doesn't privilege humanoid form over non-humanoid form. The catalogue's per-embodiment asset coverage (via Legolas Mode B crawls) will need to surface non-humanoid pixel-art sources; the empirical research doesn't yet detail non-humanoid asset coverage (a Legolas follow-on commission territory).

### Operational precision — deferred to Elrond's rubric design

The register categories named in this doc (retro pixel-art / hand-drawn pixel-art / vector / hand-drawn-2D anime / HD raster) are **design-conversation precise but operationally vague.** They support project-level decision-making (which register to lock) but are insufficient as catalogue-tagging criteria — two curators looking at the same asset (a Pipoya item, a CreativeKind pack, a CraftPix vector set) could legitimately classify it differently depending on their mental anchor. The catalogue cannot ship against subjective categories.

**Operational precision is required before catalogue work begins.** Matt caught this gap 2026-05-15. Per Option B agreement: this is acknowledged as a known gap; the rubric work is commissioned to Elrond (per AGENTS.md ownership boundary — Elrond owns abstraction-analysis tables and schema design); gandalf provides the proposed rubric axes; Elrond designs the schema and curator-tagging guidance.

The commission request lives at `agentic_orchestration/gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md`. It includes gandalf's six-axis proposal (sprite resolution / palette size / shading technique / linework style / animation frame density / derived stylistic register), worked-example tables for Reincarnated's locked register expressed against those axes, and Matt's explicit request that Elrond invoke gandalf directly for the rubric-design dialogue.

**This deferral does not affect this doc's canonical status.** The register decision is locked (hand-drawn pixel-art, HD-2D-shaped). The operational implementation of that decision in the catalogue rubric is Elrond's domain to design with gandalf's collaboration. The canonical reference for the rubric, once landed, lives in Elrond's curated domain (referenced from here); this doc remains the canonical reference for the design intent.

### Path A reconciliation — "80–100 px HD-2D target" is register aesthetic reference, not operational pixel-count constraint (added 2026-05-16 Day 4)

The "80–100 px HD-2D target" phrasing used elsewhere in this doc (and grounded in legolas's pixel-scale research § 3 against Sea of Stars / Octopath Traveler overworld camera precedent at displayed 1080p resolution) is a **register aesthetic reference** — it names the visual register and asset family the project takes as its style anchor. It is **NOT an operational pixel-count constraint** on the project's specific source assets.

**Path A operationalization (Matt-locked Day-4 close):** the chierit Elementals pack ships at intrinsic figure-content sizes of 34–57 px per character. Under the Path A re-anchoring (`canonical/story/historical/per-slug-scale-lookup-path-a-2026-05-16.md`), chierit characters render at default scale `1.0×` → ~44 px player baseline midpoint. Monster sprites scale proportionally to Path A tier ranges (trash 26–37 px / elite 44–57 px / mini-boss 66–88 px / boss 110–176 px), re-anchored against this 44 px chierit player figure rather than the 80 px SoS-class reference. Path B (upscale chierit ~1.85× to reach 80 px) was rejected by Matt on player-experience grounds (*"scaling that up would just look awkward"*) plus viewport-pressure concerns documented in the per-slug doc.

**What this preserves:** the HD-2D *aesthetic* — pixel-resolution sprites in a hand-drawn-illustration register, paired with detailed environmental art — survives Path A intact. The chierit author's drawn pixel size is the source-of-truth at scale `1.0×`; no upscale artifacts, no pixel-art quality loss. The register lock above (Candidate B: hand-drawn pixel-art HD-2D-shaped) is the same register; Octopath Traveler / Triangle Strategy / Live A Live HD-2D Remake remain the genre-precedent anchors. What differs from those references is the per-asset pixel count, which is determined by the source-asset author's intrinsic frame-content sizes, not by an asserted universal pixel-count floor.

**What this clarifies:** earlier reads of this doc that interpreted "80–100 px" as an *operational pixel-count floor* on every project asset are corrected. Future catalogue work, vendor-pack selection, and per-character scale decisions take the *register* as the lock — not the *pixel count*. The Q1 open question above ("specific fidelity target — 64–128px sprite resolution?") is partially-resolved by Path A: the chierit player baseline lands at ~44 px (below the prior 64–128 range), and monster tier ranges follow proportionally. Q1's resolution is now: **per-source-asset-derived, not universal-target-asserted.**

**Cross-references for this reconciliation:**
- `canonical/story/historical/per-slug-scale-lookup-path-a-2026-05-16.md` — Path A authoritative operationalization (per-slug scales, tier ranges, schema additions for drax refactor)
- `canonical/story/historical/sprite-scale-math-impossibility-rulings-2026-05-16.md` — the four math-impossibility rulings the Path A re-anchoring resolves (chierit ~44 px makes angel-guardian a clean downscale; fire-elemental tier-coherence violation accepted at VS2a; god-of-lightning blocked on Matt-decision pending palette-shift)
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § 3 — legolas ground-truth pixel-scale research grounding the 80–100 px SoS/Octopath reference (preserved as register-aesthetic anchor, not pixel-count operational floor)

### Path A-prime reconciliation follow-on — ARPG-anchored operational target (added 2026-05-16 Day 4 evening; ⚠️ supersedes Path A operationalization above)

**Authority:** Matt direct authorization 2026-05-16 Day 4 evening ("all authorized"), following gandalf surfacing the ARPG-vs-JRPG pixel-scale reframing per Legolas Section 4d ground-truth resolution.

**What this follow-on does.** Resolves an incompleteness in the Path A reconciliation above. The Path A framing correctly distinguished *register aesthetic reference* from *operational pixel-count constraint* — but its specific Path A operationalization (chierit at 1.0× → ~44 px player baseline) was anchored against JRPG-overworld pixel-scale conventions which Reincarnated does NOT inherit.

**Why the Path A 44 px chierit baseline was wrong.** Reincarnated is an **ARPG** (single camera; Diablo/PoE room/hallway topology committed Day 4 morning by drax v0.12). Single-camera ARPG genre convention at 1080p displayed resolution = **100-130 px** character rendered height (Diablo IV ~110-130; Diablo III ~100-110; PoE ~100-120; Last Epoch ~100-110; Grim Dawn ~90-110). JRPG dual-camera architecture (overworld 80-100 px + battle camera 75-130 px) does not apply. The ~44 px chierit baseline was anchored against JRPG-overworld conventions per the pre-resolution 80-100 px target framing; per Legolas Section 4d ground-truth measurement + gandalf's ARPG genre lineage call, the correct operational target is ARPG single-camera 100-130 px.

**Path A-prime operationalization (Matt-authorized Day 4 evening):**

| Parameter | Path A (mid-day; superseded) | **Path A-prime (operational)** |
|---|---|---|
| Chierit operational scale | 1.0× | **1.31×** (ARPG midpoint of 100-130 band) |
| Chierit rendered figure-content | ~44 px | **~115 px** |
| Acceptable chierit scale range | 1.0× only | **~1.14-1.48×** corresponding to 100-130 ARPG band |
| Tier midpoint table | trash 32 / elite 51 / mini-boss 77 / boss 143 | **trash 83 / elite 132 / mini-boss 201 / boss 374** |
| Nearest-neighbor enforcement | recommended | **CRITICAL** (most monsters now upscaled; bilinear interpolation produces visible blur) |
| Per-slug scale values | per Part 3 of per-slug doc | **per Part 6 of per-slug doc (Path A-prime amendment)** |

**What this preserves:**
- The "register aesthetic reference, not operational pixel-count constraint" distinction at line 138 above (still correct as a framing); Path A-prime simply adopts the correct *operational* anchor for an ARPG context
- Matt-locked Diablo genre ratios (swarm/trash/magic/elite/mini-boss/boss tier scales) — only the absolute baseline shifts
- The HD-2D-shaped pixel-art register (Candidate B above; locked) — register is about visual style, not absolute pixel scale; chierit at 1.31× upscale (with nearest-neighbor) remains HD-2D-coherent
- The Octopath / Triangle Strategy / Live A Live HD-2D Remake genre-precedent anchors for the register aesthetic — but adopts ARPG operational scale conventions on top of that register

**What this corrects (vs Path A above):**
- The "chierit at 1.0× scales render at the chierit author's intrinsic drawn size" framing was correct for source-asset preservation but operationally undersized for ARPG genre signal. Path A-prime upscales chierit to 1.31× with nearest-neighbor enforcement; pixel-art register coherence preserved through scaler choice, not through staying at native scale.
- The "Path B rejected on player-experience grounds (*scaling that up would just look awkward*)" framing — Matt's rejection was specifically of the 1.85× upscale Path A had derived against the 80-100 px JRPG-overworld reference. Under Path A-prime, the operational scale is 1.31× (modest) against the ARPG-correct 100-130 px target. The "awkward" concern was specific to the prior framing's larger upscale ratio.

**Per-slug monster scale values shift accordingly** — see `canonical/story/historical/per-slug-scale-lookup-path-a-2026-05-16.md` § Part 6 ("Path A-prime amendment") for the full 11-slug table. Same Matt-locked Diablo ratios applied to the corrected 115 px baseline; most monsters now upscale (1.04-2.40×) where previously they downscaled (0.13-0.85×).

**Verification before drax refactor lands:** drax v0.20.6 composite at Path A-prime scales (knight-rider authors per per-slug doc § 6.7) confirms ARPG-genre coherence in actual room/hallway topology before MONSTER_SCALE_BY_SLUG refactor fires. Knight-rider's intuition is that Path A-prime scales fit drax's already-shipped room/hallway topology cleanly; composite is cheap insurance verifying this.

**Forward implications:**
- Q1 open question above (specific fidelity target) — Path A-prime resolves this concretely: **ARPG 100-130 px target at 1080p displayed resolution**, chierit operational scale 1.31×, monster tier midpoints per Part 6 of per-slug doc
- Future vendor-pack acquisitions for VS2c+ should target this 100-130 px ARPG band (or have intrinsic frames sized to land cleanly within 1.0-2.0× scale of the band)
- The Q1 partial-resolution from Path A ("per-source-asset-derived, not universal-target-asserted") is replaced by Path A-prime's stronger statement: **per-source-asset scale to land at ARPG genre operational target; the operational target is universal, the per-asset scale factor is derived**

### Path A-prime ARPG-operational-target second amendment (gandalf, 2026-05-16 Day 4 close — supersedes 1.31× chierit-scale figures above)

**Authority:** gandalf authoring per knight-rider dispatch `agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-path-a-prime-v2.md` (Matt-confirmed Path A-prime; v2 lookup table + style-register follow-on amendment authorized in same session).

**Why this second amendment exists.** The first Path A-prime amendment above (added Day 4 evening) correctly identifies the JRPG→ARPG framing shift and the 100–130 px ARPG band as the operational target. **But the specific chierit operational scale figure (1.31×) was anchored against an obsolete baseline (the legolas pre-PIL estimate of ~88 px character figure-in-canvas) rather than the PIL-corrected figure-content baseline (34–57 px per character).** Mathematically: 44 px (Group B mid PIL-corrected figure-content) × 1.31× = **57.6 px rendered**, which is BELOW the 100–130 px ARPG band, not within it. The 1.31× × 88 px → 115 px arithmetic uses the obsolete 88 px canvas figure-in-frame estimate that drax v0.20.4 PIL inspection corrected. This second amendment authors the operationally-correct chierit scale recommendation against the corrected baseline.

**Correct chierit operational scale at Path A-prime: uniform 2.5×** (sub-option (i-prime) per `canonical/story/historical/per-slug-scale-lookup-path-a-prime-2026-05-16.md` Part 1).

| Parameter | First Path A-prime amendment (obsolete baseline) | **Second amendment — operationally-correct (PIL-corrected baseline)** |
|---|---|---|
| Chierit operational scale | 1.31× (vs obsolete 88 px estimate) | **2.5×** (vs PIL-corrected 44 px Group B mid figure-content) |
| Chierit rendered figure-content | claimed ~115 px but math doesn't hold | **~108 px mean** (Group A 133–142 / Group B 105–110 / Group C 85–98) |
| Acceptable chierit scale range | 1.14–1.48× | **2.3–2.9×** (corresponding to 100–130 ARPG band against figure-content) |
| Tier midpoints (px rendered) | trash 83 / elite 132 / mini-boss 201 / boss 374 | **trash 84 / elite 132 / mini-boss 200 / boss 370** (effectively same — first amendment's midpoints happened to be approximately correct via different arithmetic) |
| Nearest-neighbor enforcement | CRITICAL | **CRITICAL** (unchanged; in fact stronger — six monsters upscale at Path A-prime, not "most monsters") |
| Per-slug scale values | per Part 6 of v1 doc (which doesn't exist; first amendment referenced phantom Part 6) | **per `per-slug-scale-lookup-path-a-prime-2026-05-16.md` Part 3 (v2 doc; new-doc supersession of v1)** |

**Why the math discrepancy matters operationally.**

If drax implements chierit at 1.31× per the first amendment, the rendered figure-content for Group B characters lands at ~58 px (not 115 px) — **below** ARPG band-floor by 42%, closer to the prior JRPG-overworld 80–90 px reference than the ARPG 100–130 px target. The first amendment's narrative framing (ARPG operational target) and its numeric recommendation (1.31×) are not internally consistent against PIL-corrected figure-content.

If drax implements chierit at 2.5× per this second amendment + v2 lookup table, the rendered figure-content for Group B lands at 105–110 px — **in-band** at ARPG-genre operational target. Group A overshoots ceiling by 3–13% (Diablo-IV-Druid-style class-fantasy weight); Group C undershoots floor by 5–15% (Diablo-IV-Necromancer-style class-fantasy compactness). Intra-class variance preserved as design feature; mean rendered height lands at band-floor; matches ARPG genre convention.

**What both amendments agree on (preserved):**
- ARPG single-camera framing per the room/hallway arena topology — correct
- 100–130 px ARPG band as the operational target — correct
- HD-2D pixel-art register preserved (Path A-prime is scale-within-register, not register change) — correct
- Nearest-neighbor enforcement HARD REQ across monster roster (because most monsters upscale at Path A-prime) — correct (and stronger at Path A-prime than at Path A)
- Q1 resolution: operational target IS universal (100–130 px ARPG band), per-asset scale factor IS derived — correct framing; operationalization corrects to 2.5× chierit baseline

**What this second amendment corrects (vs first amendment):**
- Chierit operational scale: **1.31× → 2.5×**
- Chierit rendered figure-content claim: **"~115 px" with 1.31× → ~108 px mean (105–110 Group B) with 2.5×**
- Acceptable scale range: **1.14–1.48× → 2.3–2.9×**
- Per-slug doc reference: **"v1 Part 6 phantom" → `per-slug-scale-lookup-path-a-prime-2026-05-16.md` Part 3 (new v2 doc, supersession-clear from v1)**
- The first amendment's table values were correct in concept (tier midpoints, nearest-neighbor criticality) but inconsistent with its own chierit-scale figure; this second amendment restores arithmetic consistency end-to-end

**Why sub-option (i-prime) uniform 2.5× over sub-option (ii-prime) per-character normalization** — per `canonical/story/historical/per-slug-scale-lookup-path-a-prime-2026-05-16.md` Part 1:
- Intra-class silhouette variance is a feature (Diablo D2/D3/D4 class-stature variance lineage; Shadow Stalker tall / Ground Monk compact is author-drawn design intent)
- Sub-option (ii-prime) collides with form-bias structural-realignment work (homogenization erases the embodiment-substrate variance)
- Sub-option (ii-prime) at 3.0–3.4× for Group C pushes pixel-art quality threshold further than uniform 2.5× does

**Cross-references for this second amendment:**
- `canonical/story/historical/per-slug-scale-lookup-path-a-prime-2026-05-16.md` — **canonical operational source-of-truth for Path A-prime; supersedes v1**; chierit at 2.5×; full per-slug table; viewport-pressure analysis (NEW at Path A-prime); bbox-rendering follow-on Matt-decision; Fire_Lord_Creativkind thunder-shift; nearest-neighbor HARD REQ across roster
- `canonical/story/historical/embodiment-display-loadout.md` § 1.1 (gandalf 85ce42f) — ARPG-anchored framing on the loadout UI surface; ARPG 100–130 px in-game-character target referenced
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` — drax v0.20.4 PIL measurements that corrected the obsolete 88 px legolas estimate; figure-content 34–57 px per character is the PIL-correct baseline this second amendment anchors against
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § 3 + § 4d — legolas ARPG-vs-JRPG ground truth (both amendments cite this; both correctly identify ARPG band; only the chierit-scale arithmetic differs)
- `canonical/story/historical/arena-room-hallway-system.md` — single-camera ARPG room/hallway topology (load-bearing for the JRPG-vs-ARPG framing; both amendments correctly cite)

**Forward-process note for knight-rider:** the first amendment authored under different attribution (added 2026-05-16 Day 4 evening) anchored against the legolas pre-PIL 88 px estimate; this second amendment authored under gandalf attribution per Matt-Day-4-close directive anchors against drax v0.20.4 PIL-corrected 34–57 px figure-content. The numeric divergence between 1.31× and 2.5× is **load-bearing for drax MONSTER_SCALE_BY_SLUG refactor + chierit-scale-revision dispatches** — both held pending v2 lookup table return (this is the v2 lookup table return). Drax should implement against 2.5× per the v2 lookup table; first amendment's 1.31× figure should be treated as superseded.

### Enemy-legibility cross-reference

The locked register has a **load-bearing requirement** beyond its own internal consistency: it must support clear visual distinction between enemies and player combatants. This requirement is canonicalized in `enemy-visual-legibility.md` (authored 2026-05-15 by gandalf on Matt's commission, after demo1 family-playtest finding).

The headline of that doc: **enemies must NOT be rendered as scaled-up player-class sprites.** They must come from a separate sprite-archetype registry; carry distinct element-palette-shift; carry tier-coded aura class; carry tier-coded name-banner treatment. The Mirror-fight is the canonical exception (the Mirror IS the player's class, rendered as such — but with recognition-coded subtle cues per cosmology-reincarnated.md).

For this style-register doc specifically, the cross-reference implies:
- The locked register must support distinct-from-player enemy sprite assets (the empirical catalogue research confirms this — itch.io vendors Elthen, LuizMelo, ansimuz, pimen extensions ship abundant monster sprite assets at the HD-2D-pixel register)
- The locked register's element-palette catalogue must include both player-class palettes AND enemy-class palettes; they can share a palette space but the rendering rules separate them
- The locked register's aura asset coverage (Tier-2 in the empirical research) supplies enemy tier-coded auras (swarm cluster aura, magic shimmer, elite visible aura, mini-boss strong aura, boss signature, act-boss cinematic)
- The Legolas Mode B priority list should include **monster-sprite vendors specifically** (not just spell-VFX vendors); the current empirical research file leans toward VFX coverage and would benefit from a follow-on commission targeting monster-sprite coverage

The legibility requirements **do not change the register lock** above — they're satisfied within the HD-2D-pixel register, not in conflict with it. They do, however, raise the priority of monster-sprite catalogue coverage relative to the original VFX-heavy research scope.

### Cipher-architecture compatibility

Doc 37 § 6's canonical-four cipher (per-season vocabulary; abstract pair-structure; hidden canonical four) is **register-agnostic** at the visual layer. Each season's vocabulary surfaces as in-register asset selection: a "pressure" season's pressure-element VFX is selected/composited from existing pixel-art Earth + Implosion + impact-distortion assets (per the catalogue research's pre-locked pairings). The register doesn't change; the per-season visual content does.

---

## What this locks operationally

**For Legolas (Mode B catalogue crawls):**
- Crawl all registers broadly per the score-don't-filter principle.
- Prioritize **higher-fidelity pixel-art** vendors for initial Mode B sampling (CreativeKind, Elthen, pimen, Foozle higher-tier packs).
- Tag each asset's style sub-register (retro-pixel / hand-drawn-pixel / vector / hand-drawn-2D / hd-raster) at extraction or via Elrond curation.
- Per-embodiment coverage (non-humanoid sprite assets) is a known gap; a follow-on commission targeting non-humanoid pixel-art sources is queued.

**For Elrond (catalogue curation):**
- Style-register tag is a load-bearing curated dimension.
- Consumption-time filter for Reincarnated's surface defaults to `hand-drawn-pixel` register.
- Other registers remain in the catalogue for pivot insurance.

**For Drax (demo work):**
- Demo1's retro-pixel register is transitional, not canonical.
- Demo2 development should target the HD-2D register.
- Migration cost: sprite-asset upgrade pass + Court / Spirit Guide / Trial-cinematic-frame asset commissioning or LLM-generation.
- Pixi.js pipeline does NOT need replacement (Pixi handles HD-2D pixel cleanly via sprite sheets + atlases).

**For Star-lord (LLM image generation):**
- Visual prompts include the locked register as a prompt-construction parameter.
- Suggested prompt-register language: *"hand-drawn pixel-art game illustration, HD-2D style reminiscent of Octopath Traveler, [content-specific description], consistent isekai-genre aesthetic"* (refine via iteration).
- Style-reference-image discipline: maintain ~3-5 canonical reference images that future generations check against for register-coherence.
- Per-season visual asset budget: ~12-20 LLM-image calls per season (Court portrait for ascension + Trial cinematic frames + Spirit Guide variations + key narrative-moment art) at ~$0.10-0.50 per call = ~$1-10/season additional LLM cost on top of existing $5-10/season projection.

**For future canonical design docs:**
- Reference this doc when discussing visual presentation.
- Defer to this doc on register matters.

---

## Open questions

These do not block the lock proposal but should be resolved as adjacent work lands.

### Q1 — The "HD-2D-shaped" register's specific fidelity target

Octopath Traveler's HD-2D pattern combines pixel sprites with 3D environmental backgrounds and dynamic lighting. Reincarnated does NOT need 3D environments (the seasonal world stays 2D). What Reincarnated takes from HD-2D is **the hand-drawn pixel sensibility at modern resolutions** — sprite resolution roughly 64-128px per character, with detailed shading and palette work. Open: is this the right resolution target, or should it be higher (closer to Hyper Light Drifter's 32-48px) or lower (closer to Stardew Valley's 16px)?

My recommendation: 64-128px sprite resolution for character forms; 32-64px for monsters / smaller entities; tile-based environments at 32px per tile. This is family-pace-feasible AND HD-2D-coded.

### Q2 — Court portrait fidelity

Court portraits are full-screen-takeover moments at the Earth-Self hub. They CAN be higher resolution than combat sprites without breaking style-coherence (same register; just larger canvas). My recommendation: **256-512px per portrait, hand-drawn pixel sensibility, illustrated rather than animated.** Each portrait is generated once at ascension and persists in the Court forever. Open for Matt's input on whether portraits should be animated (more cost; more presence) or static (lower cost; sufficient for hub presentation).

### Q3 — Animation density

Combat VFX in hand-drawn pixel register can be either:
- **High-frame animation** (12-24 frames per spell effect; expensive but smooth)
- **Lower-frame stylized animation** (6-8 frames; lower cost; more "intentional" feel)

itch.io vendors split here. CreativeKind tends higher-frame; Pipoya tends lower-frame. My recommendation: lower-frame stylized animation (6-8 frames per VFX) — better for family-pace asset budget AND for the isekai-game aesthetic, which often uses fewer but more deliberate frames.

### Q4 — Spirit Guide presentation specifics

The Spirit Guide is partial-presence (translucent / opacity-as-ontology-signal per doc 37 § 5). In the HD-2D register, this is implementable as a hand-drawn pixel character with semi-transparency rendering. Open: should the Spirit Guide have one canonical sprite (always-the-same Guide) or per-player canonical variation (the Guide's visual presence is generated to match the player's Earth Self's first-form somehow)? Per-player variation has cost; same-Guide has consistency-and-recognizability.

My recommendation: **same Spirit Guide across all playthroughs.** One canonical sprite. Recognizable. The Guide IS the Guide — every player gets the same visual presence. The "yours" claim from cosmology-reincarnated.md is *experiential* (the Guide is yours-by-relationship) not *visual* (the Guide is differentiated-per-player).

### Q5 — Marketing / promotional art register

The pitch one-pager and any future marketing material is a separate context from in-game. Marketing art for Reincarnated could plausibly use a **more anime-styled raster register** in promotional materials (key art, store-page art, trailer thumbnails) while the in-game register stays HD-2D pixel. This is shipped-game-standard practice (Octopath Traveler's marketing uses anime-style key art alongside in-game HD-2D). Open: lock the marketing register canonically too, or leave it as a per-asset decision?

My recommendation: **lock the in-game register here (HD-2D pixel); leave marketing register as a per-asset decision when marketing work begins.** The in-game register is what player-experience inherits from; marketing is a separate audience and a separate decision space.

---

## Pivot insurance

Per AGENTS.md § "Score-don't-filter principle": *"Catalogue crawls are NOT scope-restricted by Gandalf's locked style register. Crawl widely; score/tag each asset by style register as curated metadata. The locked style register becomes a consumption-time filter applied by the engine + design pipeline, not a crawl-scope constraint. This preserves pivot flexibility — if the project's needs shift, the catalogue already contains the data."*

If Matt ever wants to pivot register (e.g., the project gains team capacity and can move to pure hand-drawn 2D anime; OR the project simplifies to retro pixel-art for shipping speed; OR a new register emerges that better serves):

- **The catalogue is ready.** Elrond's per-asset style-register tags mean a register pivot is a *re-filter* operation, not a re-crawl.
- **The cost is in generated content.** Already-generated seasons' visual content (sprite sets, Court portraits, Trial cinematic frames) would need regeneration in the new register. This is a meaningful cost but not catastrophic given the per-season LLM-image budget.
- **The decision-archaeology is preserved.** This doc + future pivot decisions provide the history. The reasoning stays inspectable.

The pivot path exists and is intentional. Lock with confidence; pivot if the work demands.

---

## Cross-references

- `cosmology-reincarnated.md` — the cosmological frame this register renders
- `court-of-forms.md` — endgame Court presentation; the highest-stakes use of the narrative-moment fidelity tier
- `gandalf-design-lineage.md` Layer 2 (Diablo art direction lineage) + Layer 5 (isekai studio aesthetic precedents)
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical asset landscape
- `canonical/story/historical/per-slug-scale-lookup-path-a-2026-05-16.md` — Path A operationalization (chierit ~44 px player baseline; monster tier ranges; per-slug scale recommendations) — consumes this register's lock; surfaces the "80–100 px = aesthetic reference, not pixel-count constraint" reconciliation (see § "Path A reconciliation" above)
- `canonical/story/historical/sprite-scale-math-impossibility-rulings-2026-05-16.md` — math-impossibility rulings the Path A re-anchoring resolves; consumes this register's lock as consumption-time filter
- `agentic_orchestration/AGENTS.md` § "Viability-gate workflow (catalogue work)" — the design-track of catalogue viability-gates, where this register is the load-bearing reference
- `agentic_orchestration/AGENTS.md` § "Score-don't-filter principle (catalogue data)" — the pivot-insurance pattern
- File 19 § Phase 02 — the visual_prompt LLM field that consumes this register downstream
- Pitch `pitch-2026-05-18/one-pager.md` § "The Game" — the isekai positioning this register serves

---

## Maintenance protocol

This doc is canonical as of Matt's lock 2026-05-15.

When future register-relevant decisions arise (sprite resolution refinements, animation-density tuning, per-embodiment asset gaps): append sections; preserve canonical-lock history; reference the original lock.

When (and if) the project pivots register: a new section captures the pivot decision; the prior register-lock is marked superseded but preserved for archaeology. Per pivot-insurance pattern above, the catalogue serves the pivot without re-crawl.

When LLM image generation work needs the register as prompt context:
- Use the canonical register language: *"hand-drawn pixel-art game illustration, HD-2D style reminiscent of Octopath Traveler, [content-specific description], consistent isekai-genre aesthetic"*
- Maintain style-reference-image discipline per § "What this locks operationally" → Star-lord
- Default register filter on catalogue consumption is `hand-drawn-pixel`

When new canonical design docs touch visual presentation:
- Reference this doc.
- Defer to this doc on register matters.
- Cross-reference for register-coherence checks at Gate 1.

— gandalf, with Matt's canonical lock 2026-05-15
