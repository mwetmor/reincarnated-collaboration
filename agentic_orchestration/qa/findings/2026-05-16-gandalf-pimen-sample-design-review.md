# Finding — 2026-05-16 — gandalf design-track Pimen sample review

**Reviewer:** gandalf
**Severity:** **PASS**
**Target:** Legolas Pimen sample (20 rows; `research/catalogue/pimen/sample-2026-05-16.json`)
**Track:** design (viability-gate of three)

## Verdict (one line)

**PASS — Pimen positions cleanly as a primary anchor source for Reincarnated's locked HD-2D-shaped pixel-art register, with strong element coverage and consistent hand-drawn-pixel sub-register on paid tier-03+ packs; minor flags surface for wiring (monolithic character decomp) and curation (free packs uncertain on sub-register) but do not block design-track approval.**

## Per-criterion assessment

### 1. Thematic coherence — STRONG

The 20-row sample reads as **deeply coherent across the paid tier**. Every row carries the `handmade` tag, and Pimen's "handmade animated sprite sheets" marketing claim is borne out in metadata signals:

- **Consistent canvas-size discipline** — paid tier-03 packs cluster on 32x32 to 64x64 with explicit per-effect dimensions documented (Ice 02, Holy, Dark, Wind 03, Acid all show this discipline)
- **Consistent frame rate** — 80ms/s appears across nearly every row; the rare divergence (Holy at 80 FPS stated; Water 01 at 80ms/s) is consistent timing
- **Consistent format pattern** — paid tier-03+ packs ship PNG spritesheet AND individual frames; consumer can choose extraction approach
- **Animation density scales with price** — free packs typically 3-5 animations with mid frame counts; paid tier-03 packs reach 10-22 animations with cinematic frame counts (150-200+ frames per pack); the price ladder corresponds to fidelity ladder
- **No generative AI used** — stated on every row; important for AI-content compliance per pitch positioning

**Mixed-register signal within packs is acceptable.** Several paid packs (Holy, Acid) have minor 16x16 retro-band outliers alongside hd2d-pixel primary. Elrond should tag these per-asset at curation; the pack-level primary classification holds.

**Coherence verdict:** Pimen's aesthetic profile is **internally consistent at the artist level** — the same hand produces all of it, with quality scaling per price tier. This is the most valuable thematic-coherence pattern a single-creator source can offer.

### 2. Style-register match (HD-2D-shaped pixel-art) — STRONG MATCH

**Pimen's primary register IS the locked register.**

| Sub-register evidence | Sample data |
|---|---|
| **Hand-drawn-pixel tag explicit** | Fire 03, Water 03, Ice 02, Holy, Dark, Earth 03, Wind 03, Thunder 03, Acid, Mega Pack, Buff/Debuff, Hit Spark — 12 of 20 rows |
| **Resolution band hd2d-pixel confirmed** | Fire 03, Water 03, Ice 02, Holy, Dark, Wind 03, Acid, Skeleton Enemies, Buff/Debuff, Hit Spark — 10 of 20 rows with explicit canvas data |
| **Primary canvas in HD-2D-shaped range** | 32x32 to 64x64 dominant; 48x48 / 48x64 common; occasional 96x+ narrative-band outliers |
| **Architectural fit** | Paid tier-03+ packs are unambiguously the register Reincarnated locked |

**Sub-register uncertainty on free packs is acceptable.** 6 free packs are tagged `sub-register-uncertain` (Fire 01, Water 01, Ice 01, Earth 01, Wind 01, Thunder 01) — Legolas couldn't inspect frames directly; small archive sizes (3.9-49 kB) suggest possible retro-band or simpler pixel-art rather than hand-drawn-pixel. Per the score-don't-filter principle (AGENTS.md), these are still catalogued; their sub-register gets resolved at curation visual inspection (Elrond's track) without blocking the gate.

**Per `style-register.md` § "Operational precision — deferred to Elrond's rubric design":** Pimen's sample provides exactly the kind of multi-axis material the proposed rubric (resolution / palette / shading / linework / animation / derived register) can classify cleanly. Pimen demonstrates that the rubric design is practical against real catalogue content.

**Register-match verdict:** Pimen is **not adjacent-to-locked-register; it IS the locked register at its best.** Paid tier-03 packs are reference-grade hand-drawn-pixel HD-2D-shaped work.

### 3. Reasonable-pivot register signal — LIMITED BUT INTENTIONAL

Pimen is **pixel-art exclusively.** Does NOT provide pivot-insurance toward:
- Vector / clean-line register
- Hand-drawn 2D anime-cel register
- HD raster / painterly register

WITHIN pixel-art, Pimen provides limited sub-register pivot:
- Retro-band 16x16 outliers exist as minor exceptions within paid packs (Holy VFX9-10; Acid range)
- Free packs likely sit at retro-pixel or simple-pixel sub-register (visual inspection pending)
- Narrative-pixel band (96px+) reached in occasional outliers (Water 03 Water Mine 96x64; Acid 72x80)

**This is fine.** Pimen's role in the catalogue strategy is *primary HD-2D-shaped pixel-art anchor source*, not pivot-insurance. Pivot-insurance for non-pixel registers requires CraftPix vector packs, CreativeKind hand-drawn-pixel (different sub-register), or HD raster sources — none of which Pimen claims to be.

**Score-don't-filter principle held:** the catalogue admits multiple registers; Pimen's role is to anchor one register exceptionally well, not to span all registers thinly.

**Pivot-signal verdict:** Pimen is intentionally narrow on register. The narrowness is a feature, not a limitation.

### 4. Court-tier aesthetic quality — PROMISING BUT SAMPLE-INSUFFICIENT

The sample includes **2 explicit character/enemy rows + 1 hidden character bundled within an elemental pack:**

| Asset | Type | Decomposition | Court-tier read |
|---|---|---|---|
| Fantasy Skeleton Enemies | enemy (warrior + mage variants) | **monolithic** | Enemy registry-grade; suitable for monster sprite archetype per enemy-visual-legibility.md S1 |
| Fantasy Platformer Character | character (battlemage) | **monolithic** | 265 kB archive (largest in sample) implies high fidelity; potentially Court-tier-capable |
| Earth Elemental (bundled in Earth Spell 03) | enemy (elemental form) | **unknown, likely monolithic** | Non-humanoid embodiment evidence — important per embodiment-narrative-layer.md |

**The monolithic-decomposition is a wiring-track concern** (Drax's verdict will address it). For design-track, what matters:

- **Monolithic does NOT preclude Court-tier presentation.** Octopath Traveler's protagonist sprites are monolithic spritesheets; they read as characters per court-of-forms.md C3. Hand-drawn-pixel sensibility at HD-2D-shaped resolution carries character identity even without per-layer decomposition.
- **Monolithic DOES preclude per-form variation by re-skinning.** Per embodiment-narrative-layer.md: when a humanoid Court member ascends, then later a slime Court member ascends, they CAN'T share a base sprite with palette/decoration overlays — each embodiment needs its own sprite-archetype. Pimen's monolithic character work means: *each embodiment needs a separate Pimen pack (or equivalent source) for full Court coverage.*
- **The Earth Elemental in Earth Spell 03 is the most significant signal.** It demonstrates Pimen produces **non-humanoid character sprites** within VFX packs. This is direct evidence for doc 37 § 4 embodiment-axis coverage feasibility from a single-creator source.

**Court-tier verdict:** the Battlemage suggests Court-presentable character fidelity is achievable from Pimen. **Sample insufficient to confirm character-tier breadth** — Pimen's broader character catalogue (beyond the 2 sampled) needs assessment via a follow-on commission or via Mode B full-crawl results. Design-track does NOT block on this; it flags for **a follow-on character-track sub-commission** when broader Pimen character work is needed for Court implementation.

### 5. Element-coverage signal — STRONG (PIMEN ALONE SUFFICIENT FOR CANONICAL COSMOLOGY)

Pimen covers **9 distinct elements** in the 20-row sample:

| Element | Free pack | Paid tier-03 pack | Reincarnated mapping |
|---|---|---|---|
| Fire | ✓ Fire 01 | ✓ Fire 03 ($3) | Canonical four (file 29 + doc 37 § 6 cipher) |
| Water | ✓ Water 01 | ✓ Water 03 ($3) | Canonical four |
| Earth | ✓ Earth 01 | ✓ Earth 03 ($3) | Canonical four |
| Wind | ✓ Wind 01 | ✓ Wind 03 ($3) | Canonical four |
| Ice | ✓ Ice 01 | ✓ Ice 02 ($4.99) | Cipher per-season vocabulary expansion (frost / cold register) |
| Holy | — | ✓ Holy ($4.99) | Cipher per-season vocabulary (light / radiant register) |
| Dark | — | ✓ Dark ($4.99) | Cipher per-season vocabulary (shadow / void register) |
| Thunder | ✓ Thunder 01 | ✓ Thunder 03 ($3) | Cipher per-season vocabulary (lightning / electric register) |
| Acid | — | ✓ Acid ($4.99) | Cipher per-season vocabulary (poison / toxic register) |

**Plus** the Mega Pack ($12.75) bundles all 9 elements with Aseprite source files — the highest-value single purchase in the sample.

**This is genuinely substantial.** Pimen alone provides:
- **Full canonical-four coverage** (file 29 + doc 37 § 6 cipher requires resistance-translation against 4 element identities; all 4 ship)
- **5 expansion-element vocabulary slots** (ice / holy / dark / thunder / acid) for doc 37 § 6 cipher per-season vocabulary work — each season's per-season vocabulary can map to one or more of these for mechanical-signature differentiation (per Position (ii) lock)
- **Status-effect VFX** (Buff/Debuff pack) — useful for combat-feel building blocks per enemy-visual-legibility.md S3 tier-coded aura class
- **Hit-impact VFX** (Hit Spark pack) — combat feedback layer with palette-variant support

**Pimen is a "must-have" anchor source, not a complementary one.** The full-crawl's worth-it bar is exceeded by element coverage alone.

**One thematic-mapping note for design intent:** Pimen's Wind is tagged `nature / druidic` (green coloring) per row 11 — this maps slightly off from a more neutral air-coded wind register. Cipher per-season vocabulary work should flag this when assigning Pimen wind assets to seasons whose wind-flavor isn't nature-coded. Minor; surfaces at curation/season-generation time.

---

## What this catalogue source brings

**Pimen positions as a MUST-HAVE PRIMARY ANCHOR SOURCE for the locked HD-2D-shaped pixel-art register.**

Specifically:

1. **Reference-grade aesthetic at the locked register.** Paid tier-03+ packs are the kind of asset the style-register lock was authored against. The Octopath Traveler precedent (style-register.md § "TL;DR") cited as the locked-register exemplar is functionally what Pimen produces.
2. **Comprehensive element coverage from a single creator.** Single-creator coherence is rare in catalogue work; Pimen offers it across 9 elements at consistent quality. This is operationally valuable — multiple seasons' worth of cosmological vocabulary can source from one consistent visual hand.
3. **Status + impact + character work alongside elemental VFX.** The breadth (Buff/Debuff; Hit Spark; Skeleton Enemies; Battlemage) means Pimen serves not just element-coded skill VFX but also combat-feel layers and enemy/character roster.
4. **Aseprite source files on key packs.** The Mega Pack + Hit Spark include Aseprite source — significant wiring upside (per Drax track); for design-track, this means per-layer color/element customization is feasible without re-commissioning.
5. **Pricing fits family-pace development economy.** Full sample purchase value is ~$50-60; Mega Pack at $12.75 is the highest-value single purchase. This is genuinely affordable for solo/family development per pitch one-pager's family-paced framing.
6. **Active series + No-Gen-AI provenance.** Pimen is actively expanding (wood-type spells forthcoming); "No generative AI used" is stated on every row — important for AI-content compliance per pitch positioning + future App Store ambitions per memory-noted Apple compliance concern.

**Compared to other sources** per the Legolas-filed `2026-05-16-pixijs-compatible-2d-vfx-libraries.md` research file: Pimen sits at the "core" of the recommended shopping list (alongside Brackeys VFX Bundle for free baseline, ansimuz packs for retro-band complementary, CraftPix for additional Tier 2/3 niches). Pimen specifically anchors the HD-2D-shaped pixel-art register; ansimuz fills retro-band; CraftPix fills vector + niche-mechanic gaps.

---

## What this unblocks (PASS)

**Full Pimen crawl release.** Legolas can proceed to full Mode B crawl with high confidence that the design-track register-fit signal is strong.

Specifically:

- **Full element-pack coverage purchasable** when budget is authorized (per AGENTS.md ADR-006 external-system writes; Matt's authorization required for purchases)
- **Mega Pack ($12.75) recommended as priority purchase** — bundles 9 element packs + Aseprite sources + elemental icons; highest single-purchase value
- **Free packs catalogued for visual inspection at curation time** — sub-register classification resolves at Elrond's structural track
- **Character/enemy assets catalogued** but flagged for follow-on character-track assessment when Court implementation work nears (post-Phase-0 Earth-Self hub work)

---

## Cross-track flags (informational for elrond + drax)

These observations belong to other tracks but surface during my review; sharing for cross-pollination per dispatch § "Direct-dialogue option":

**For Elrond (structural track):**

- Sub-register classification gap: 6 free packs need visual inspection to determine `retro-pixel` vs `simple-pixel` vs `hand-drawn-pixel` sub-register. The proposed rubric (per `gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md`) is the right tool — its resolution / palette / shading axes resolve this cleanly when frames can be inspected.
- The Mega Pack's Aseprite inclusion has metadata implications — Elrond may want to capture `aseprite_available: bool` as a per-asset metadata field; this signals wiring-tier capability difference between packs.
- Earth Spell 03's bundled Earth Elemental character is metadata-bundled-within-vfx-row; consider whether bundled-character assets warrant separate catalogue rows OR row-augmentation (`bundled_character: true` field).

**For Drax (wiring track):**

- Monolithic character decomp is the load-bearing wiring concern. Skeleton Enemies (warrior + mage) + Battlemage are monolithic; layer-separation for body-swap reskinning requires source files (Aseprite) not shipped with these packs.
- Non-square canvas sizes (Dark pack's 32x48, 72x32; Buff/Debuff's 48x64 portrait) require Pixi.js atlas canvas-padding strategy. Worth a Drax design pass before purchasing the full Dark pack at $4.99.
- Ice 01 ships individual-frames-only (no spritesheet) — consumer assembles. Pimen offers RPG Maker MV spritesheet export on request — coordination cost.

These do NOT block the design-track verdict; they are observations Drax + Elrond will weigh in their respective tracks.

---

## What this blocks (NEEDS REWORK)

**Nothing.** Verdict is PASS. No re-extraction needed for design-track approval.

---

## Authority boundary note

This verdict addresses design-fit per AGENTS.md viability-gate workflow design-track criteria. The cross-track flags above are informational; Elrond and Drax retain authority over their respective tracks' verdicts. Final purchase / full-crawl scope decisions are Matt's per ADR-006.

If Drax's wiring-track verdict surfaces blocking concerns on monolithic character decomp that this design-track read underweights, escalate to knight-rider for synthesis. My read is that monolithic-character-decomp is a known cost-of-doing-business in the pixel-art register (Octopath Traveler ships monolithic protagonist sprites successfully); the cost is manageable.

---

## Summary recommendation

**PASS. Pimen full-crawl is unblocked from design-track. Mega Pack ($12.75) is recommended priority purchase. Character/enemy coverage warrants a follow-on character-track assessment when Court implementation work nears. Pimen anchors the HD-2D-shaped pixel-art register exceptionally well; the catalogue's primary anchor source for this register is identified.**

— gandalf, 2026-05-16
