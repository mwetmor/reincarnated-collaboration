# Research — AI tells in painted game art · art-bible practice · deterministic oracles — 2026-09-11

**Mode:** A (analytical). **Commissioner:** gandalf (RUN-CONDUCTOR, Astra burst lane Run C-1).
**Brief:** `agentic_orchestration/gandalf/requests/2026-09-11-legolas-mode-a-ai-tells-art-bibles-oracles.md` (+ R8 ADDENDUM relayed mid-session, 2026-09-11, Matt-raised).
**Anchors viewed before writing:** `astra_test_01/design/experiments/E07V/art/F04.png`, `…/F03.png`, `astra_test_01/run_03/evidence/vfx_style_match.png`. ✓
**Companion:** `sources.json` (same directory).

## Grading key (used on every claim)

| Grade | Meaning |
|---|---|
| **VERIFIED** | Stated in a primary source I read directly (vendor documentation, peer-reviewed paper, studio-published post) with the numbers/wording quoted. |
| **PRACTITIONER-REPORT** | A real practitioner/production artifact or community-standard practice, published but not measured. |
| **SECONDARY** | Trade-press or community report *about* a primary source (e.g. a GDC talk I could not open). |
| **UNVERIFIED** | Plausible, named, not evidenced. Includes my own inference. |
| **OBSERVED** | My own first-hand inspection of our three anchor images this session. Declared as such; it is evidence about *our* assets, not about the world. |
| **FOLKLORE** | Circulating practice claim with no support and, where noted, positive evidence against. |

Every finding carries a tag line: **`[rule-class → yield]`** per brief § 4. Yields: **prompt lever** · **oracle** · **JUDGE axis** · **bible field**.

---

## 0. Summary

1. **The tell gandalf named "detail without ownership" is the single most prevalent artifact class in the literature, and the hardest for humans to catch.** CHI 2025 (599 images, 50,444 participants, 749,828 observations) finds *functional implausibilities* — "objects unable to function properly, implausible object placement/usage, distorted fine details (clothing print, buttons, buckles)" — present in **58.7%** of annotated AI images, ahead of anatomical (51.4%) and stylistic (39.0%), while sitting at the **lowest** human detection accuracy of the three big classes (**64.1%**). The hypothesis is not merely supported; it names the class that most needs a *deterministic* gate rather than a judge, because a judge is the thing that misses it.
2. **"Motif bleed" has no name in the artifact literature.** The CHI taxonomy has no category for it. The nearest literature construct is *incorrect attribute binding* / *catastrophic neglect* (Attend-and-Excite, SIGGRAPH 2023) — and that mechanism is demonstrated on Stable Diffusion's UNet cross-attention, **not** on GPT-image-class architecture. The phenomenon is real in our assets; the mechanism story is unverified for our model.
3. **One clause of gandalf's hypothesis needs correcting, and it changes the plan.** "Material-nouns over-texture" implies material-first prompting is the safer register. F03 shows it is not safer — it *relocates* the failure: doubled straps and buckles that close nothing are **functional implausibility**, the most prevalent and least-detected class, not mere over-texture. Material-first trades semantic leakage for the worse-measured tell family. (§ 1.6, clause 2.)
4. **Placement boxes cannot be enforced at generation time. They can only be declared and then measured.** OpenAI's own documentation, verbatim: *"Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision."* And there is **no `negative_prompt` parameter** and **no seed parameter** in the Image API. Under Run C-1's built-in-only lock there is no mask surface at all. **Consequence: the bible's `placements[]` and `exclusions[]` are oracle inputs first and prompt text second.**
5. **The transcribe→compare pattern Matt described has a strong published precedent under a different name:** TIFA (ICCV 2023) and DSG (ICLR 2024) — declared truth → atomic questions → a model answers by perception → a deterministic script scores. VQA-based *compliance* gating is also published in construction safety. What does **not** exist in the literature: this pattern applied to art-asset conformance, and any reliability figure for VLM part-inventory transcription on *illustrated* images.
6. **The transcriber must never be asked for boxes.** GPT-4V on object localization: mean IoU **0.16**, only **7.6%** of images above IoU 0.5; counting is the lowest-accuracy VLM task family measured (64.0–74.7%). Ask for presence/absence and per-part counts, cross-check counts deterministically, and use known-bad controls.
7. **T0 tooling is one package thinner than the brief assumes.** First-hand probe of the system interpreter: `PIL 10.3.0`, `numpy 2.4.6`, `scipy 1.17.1`, `sklearn 1.8.0` **present**; **`cv2` MISSING, `skimage` MISSING, `torch` MISSING, `onnxruntime` MISSING**; no `.venv` in `reincarnated-engine`, `reincarnated-collaboration`, or `astra_test_01`. Good news: every closed-form oracle below is reachable without OpenCV (`scipy.ndimage` + `scipy.signal.fftconvolve` cover labelling, morphology, gradients and normalised cross-correlation; `sklearn.cluster.KMeans` covers palette work). Bad news: every model-backed metric (DINO-I, CLIP-I, MaSC, SAM-class) is a dependency decision, not a free option.
8. **Nine of the ten shortlisted oracles are closed-form and standable-up at T0.** The tenth (identity across frames) needs a model. Six of ten need part masks; the cheapest route to part masks is **designing the costume with disjoint per-part palettes** — which has two independent precedents and two named failure modes (anti-aliasing at borders; shading collapsing chroma).

---

## 1. Thread R6 — AI tells in painted / illustrated game art

### 1.1 The taxonomy, anchored

**Primary anchor:** *Characterizing Photorealism and Artifacts in Diffusion Model-Generated Images*, CHI 2025 (arXiv 2502.11989). Method: 599 images (149 real photographs, 450 generated by Midjourney / Firefly / Stable Diffusion); **50,444 participants**, **749,828 observations**; three-step taxonomy development (literature + online discourse review → parallel generation/curation and crowdsourced experiment → integration of participant feedback). **VERIFIED.**

Five high-level categories, with the sub-items as listed:

| Category | Sub-items (as published) | Prevalence in annotated images | Human detection accuracy (images >80% excluded) | Mentioned in participant comments |
|---|---|---|---|---|
| **Functional implausibilities** | objects unable to function properly; implausible object placement/usage; distorted fine details (clothing print, buttons, buckles); text errors / distorted glyphs | **58.7%** | **64.1%** (lowest) | 21% |
| **Anatomical implausibilities** | extra/missing fingers; disproportionate body parts; distorted facial features; merged body parts; biometric artifacts (eye size, nose structure, interpupillary distance, ear shape, moles/scars) | 51.4% | 65% | **61%** (highest) |
| **Stylistic artifacts** | waxy/glossy/shiny skin; plastic-like textures; overly perfect / photoshoot-like appearance; excessively soft hair; cinematic/picturesque quality; smudge distortions at component edges; resolution inconsistencies | 39.0% | 64.9% | 30% |
| **Violations of physics** | shadows pointing in diverging directions; misaligned reflections; depth/perspective warping; trajectory misalignment | 9.17% | — | 15% |
| **Sociocultural implausibilities** | socially implausible contexts; cultural norm violations; historical inaccuracies; public figures in unlikely settings | 5.50% | — | 4% |

Also VERIFIED from the same source: overall accuracy **76%** on AI images / **74%** on real; **72%** accuracy at 1 s display vs **82%** at 20 s.

> **The gap that bounds everything in this section:** the study "exclusively examined photorealistic diffusion model outputs" and contains **no discussion of stylized or illustrated images**. I found no published artifact taxonomy for painted / illustrated generation. Every transfer of the table above to painted-2D is therefore an assumption, not a result. **VERIFIED (that the gap exists).**

**Adjudication of gandalf's candidate list against the taxonomy:**

| gandalf's candidate | Status | Anchor |
|---|---|---|
| ornament without function | **CONFIRMED, and it is the #1 class** | CHI functional: "objects unable to function properly" |
| non-functional armor / impossible anatomy | **CONFIRMED** (splits across functional + anatomical) | CHI |
| glyph gibberish (pseudo-text sigils) | **CONFIRMED** | CHI functional: "text errors / distorted glyphs" |
| material confusion at boundaries · edge halos | **CONFIRMED** (one item) | CHI stylistic: "smudge distortions at component edges" |
| specular-on-everything / HDR sheen | **CONFIRMED** | CHI stylistic: "waxy/glossy/shiny…plastic-like textures" |
| photographic artifacts in painted work | **CONFIRMED-adjacent** | CHI stylistic: "cinematic/picturesque quality" |
| hands & weapon grips | **CONFIRMED** | CHI anatomical: extra/missing fingers, merged body parts |
| intra-object perspective drift | **CONFIRMED** | CHI physics: "depth/perspective warping" |
| the default face | **PARTIAL** — split across stylistic ("overly perfect/photoshoot-like") and anatomical (biometric artifacts) | CHI |
| near-symmetry drift | **PARTIAL** — not a named item; nearest is "overly perfect" | CHI |
| texture stutter / repeating micro-pattern | **WEAK** — absent from CHI; supported only by tertiary "how to spot AI art" listicles | tertiary |
| **motif bleed / semantic leakage** | **ABSENT from the taxonomy** — see § 1.2 | — |

**Extensions I add, graded:**

- **E1 — Attribute-binding failure (the literature's nearest relative to motif bleed).** Attend-and-Excite (SIGGRAPH 2023, arXiv 2301.13826) names two semantic failure modes: *catastrophic neglect* ("one or more subjects is not generated") and *incorrect attribute bindings* ("an attribute such as a color is incorrectly matched to a subject"), and locates the mechanism in the cross-attention map (one spatial map per text token). **VERIFIED for Stable Diffusion. UNVERIFIED for GPT-image-class** — different architecture; do not claim the mechanism, only the phenomenon. `[motif → JUDGE axis + oracle]`
- **E2 — Key-light divergence as a *cross-asset* tell.** CHI's physics category covers shadows diverging *within* an image. Our failure is shadows/key diverging *between panels of one sheet* (§ 1.5). No literature; OBSERVED. `[light → oracle + bible field]`
- **E3 — Feature-scale mismatch across canvases.** Same declared effect rendered at two different grain scales because it was generated at two native canvas sizes. OBSERVED; no literature. `[scale → bible field + oracle]`
- **E4 — Sociocultural → faction-fiction implausibility.** CHI's fifth category has a direct analogue for us: an object that violates the *faction's* fiction rather than the world's. Lowest prevalence, and unmeasurable by any closed-form oracle. `[motif/construction → JUDGE axis]`

### 1.2 Stylistic vs structural — is the split real?

**Evidence for the split (VERIFIED numbers, my reading of them marked):**

- Structural classes dominate prevalence: functional 58.7% + anatomical 51.4% vs stylistic 39.0%.
- Structural classes are *not* the ones people talk about: anatomical is mentioned in 61% of comments but annotated in 51.4% of images; functional is annotated in 58.7% but mentioned in only **21%**. **Functional implausibility is the most common tell and the most under-verbalised.** (VERIFIED numbers; the juxtaposition is mine.)
- Detection accuracy is essentially flat across the three big classes (64.1 / 65 / 64.9) — so the classes are not distinguished by *difficulty* but by *prevalence and articulability*. **VERIFIED.**

**My synthesis, marked as such (UNVERIFIED inference from VERIFIED data):** a stylistic tell is a property of the *render* — waxiness, sheen, edge smudge — and the render is exactly what style vocabulary addresses, so restraint vocabulary can move it. A functional tell is a property of the *world model* — this buckle closes nothing — and no amount of "restrained", "production asset", "matte" moves it, because the defect is not how much detail exists but whether each piece of detail is attached to a cause. That is the mechanical reason gandalf's split holds: **the structural half needs authored input because the prompt has no vocabulary for causation, only for appearance.** `[construction → bible field]`

Corroborating frame, different domain: the entire QA-based evaluation line (TIFA/DSG, § 3.2) exists because *faithfulness to a declared spec* is measurable while *aesthetic quality* is not. Structural rules are declarable; stylistic ones mostly are not. **VERIFIED that the line exists; the analogy is mine.**

### 1.3 Prompt-level mitigations for GPT-image-class models

Primary sources: the published OpenAI image-generation guide (`developers.openai.com/api/docs/guides/image-generation`) and the vendored OpenAI `imagegen` skill read in full at `~/.codex/skills/.system/imagegen/` (`SKILL.md`, `references/prompting.md`, `references/image-api.md`, `references/sample-prompts.md`). Both are vendor-authored.

**M1 — There is no negative-prompt control. VERIFIED.** From the published guide: *"No `negative_prompt` parameter exists in the API."* Core parameters are `prompt, model, n, size, quality, background, output_format, output_compression, moderation`. An "avoid" list is ordinary prompt text competing for the same attention as the rest of the prompt.
→ **Corroborating signal, VERIFIED:** OpenAI's own game-asset recipes keep the `Constraints:` line to IP hygiene only — *"no logos or trademarks; no watermark"*, *"no text; no background scene elements"* — and never to visual-restraint negations. The vendor does not model restraint as a negation.
→ **Lever that survives:** assert plainness *positively* and by scope ("the sigil appears on the left pauldron only; all other armour surfaces are plain and undecorated"), not as a prohibition naming the motif again. **UNVERIFIED as to effect size for gpt-image-2** — this is the single highest-value cheap experiment in Run C-1. `[motif, plain-budget → prompt lever]`

**M2 — Edit-with-invariants is the documented drift control. VERIFIED.** *"For edits, say `change only X; keep Y unchanged` and repeat invariants on every iteration to reduce drift."* And *"Start with a clean base prompt, then make small single-change edits… Prefer one targeted follow-up at a time over rewriting the whole prompt."*
→ Two-pass generation (plain planes first; ornament as a second, invariant-constrained edit) is **in-family with vendor guidance**, not folklore. Effect size UNVERIFIED. `[motif, construction → prompt lever]`

**M3 — Masks are guidance, not geometry. VERIFIED, verbatim:** *"Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision."* The vendored skill repeats it: *"Masking is prompt-guided; exact shapes are not guaranteed."* Further: the `mask` parameter is **fallback-CLI/API only** — *"`quality`, `input_fidelity`, explicit masks, `background`, `output_format`… are fallback-only execution controls. Do not assume they are built-in `image_gen` tool arguments."*
→ **Under Run C-1's built-in-only lock (charter F4) there is no mask surface at all, and even with the API there is no guarantee.** This is the finding that decides the bible's shape: **`placements[]` are a measurement contract, not a generation control.** `[motif, plain-budget → bible field + oracle]`

**M4 — Reference conditioning: label by index and role; fidelity is not dialable on gpt-image-2. VERIFIED.** *"Label each image by index and role (`Image 1: edit target`, `Image 2: style reference`)"*; *"If the user provides images for style, composition, or mood guidance and does not ask to modify them, treat the request as generation with references."* And: *"`gpt-image-2` always uses high fidelity for image inputs, so do not set `input_fidelity`."*
→ Copy-vs-interpret has **no parameter**. For an isolated motif crop, forced-high fidelity is what you want at the one declared placement and precisely what you do not want elsewhere. Whether supplying an isolated motif crop *increases* bleed is **UNVERIFIED and is a named experiment**, not an assumption. `[motif → prompt lever]`

**M5 — Intended-use / polish vocabulary is a documented lever. VERIFIED (that the lever exists).** *"Include intended use (ad, UI mock, infographic) to set the level of polish."* The `stylized-concept` slug's own instruction: *"Specify style cues, material finish, and rendering approach (3D, painterly, clay) without inventing new story elements."*
→ **But note the trap:** `stylized-concept` is the **only** game-facing slug, and its templates are concept-art-shaped ("game environment concept art", "game character concept", "neutral hero pose on a simple backdrop"). Our register — *production sprite, not a concept sheet* — is **not** a vendor slug. Declaring it is an unsupported extension. **PRACTITIONER-REPORT at best.** `[silhouette, plain-budget → prompt lever]`

**M6 — No seed. VERIFIED by absence.** Seed appears in neither the core-parameter list nor the CLI reference. **Frame-to-frame consistency cannot be bought with seed locking**; it must come from reference conditioning + invariant edits (M2/M4) and be *measured* (§ 3). `[silhouette, construction → oracle]`

**M7 — Material-first vs motif-first: no vendor guidance either way. UNVERIFIED.** Weak corroboration only, by construction: the vendor's character-concept recipe is entirely material/construction nouns (*"long coat, satchel, practical travel clothing"*) with no motif at all. That is a convention, not a measurement. `[material, motif → prompt lever]`

**Marked FOLKLORE (circulating, unsupported, and in two cases contradicted):**
- *"Phrase negatives as 'without X' and the model honours them."* No vendor support; no API surface. **FOLKLORE.**
- *"Attention-weighting syntax (`word:1.3`) strengthens or suppresses a term."* That is Stable-Diffusion-ecosystem syntax; no counterpart in the GPT Image API. **FOLKLORE for this model.**
- *"Lock the seed for consistency."* **FOLKLORE for this model** — no seed parameter (M6).
- *"Masks give you hard placement boxes."* **CONTRADICTED** by vendor text (M3).

### 1.4 What a tell-free painted asset still needs, to read as "detailed"

This is the thinnest-sourced part of R6; I could not find a citable concept-art-pedagogy primary source stating a "design vs rendering" doctrine in the terms the brief asked for (two passes; recorded as a gap in § 4). What I *can* anchor:

- **Detail as an allocated budget, stated by a studio. PRIMARY (studio-published).** Diablo IV's art direction runs on two pillars, *"old masters"* and *"a return to darkness"*, and the first is explicitly about restraint: classical painters' *"controlled use of detail, tonal range, and expert use of color palettes."* Blizzard says the pillars have been *"instrumental in keeping the team consistent and aligned."*
- **Ornament as a progression currency. SECONDARY** (trade press on the GDC 2012 D3 talk, which I could not open — GDC Vault): armour was designed to *"start barebones but recognizable and end up incredibly ornate,"* giving *"a real sense of accomplishment."* Ornament is *spent*, not defaulted.
- **Legibility before beauty, with a stated value structure. SECONDARY:** background dimmed → midground high-contrast character lighting → foreground UI, *"so proper focus could be put on each and guide the eye accordingly."*
- **Detail placed where the player looks. PRACTITIONER-REPORT** (published production art bible, Fleur's Fabel — § 2): a section literally titled **"Level of details"**, whose content is *where* detail is permitted — 2D sprites carry facial-expression detail during dialogue; *"slight fog in background blurs objects in background & helps draw player's attention to the foreground."*
- **Figure/ground separation as an explicit rule. PRACTITIONER-REPORT:** *"Character colors are generally a bit brighter and lighter than the environment to make the characters stand out."*

**Answer to Matt's question, assembled from the above (synthesis marked):** removing tells does not remove detail, because the detail that survives is a *different substance* from the detail that tells. Value hierarchy, edge control, material response and figure/ground separation are all render properties the model does well and that no restraint clause costs you. What removing tells *does* cost you is **ornament**, and every precedent above treats ornament as an authored, budgeted, spent resource — not an emergent property of prompting. So: **yes, we must supply the insignia, the stitching and the construction ourselves**, and the supply mechanism the industry already uses is the bible. `[plain-budget, material, silhouette → bible field]`

### 1.5 First-hand reading of the three anchors (OBSERVED)

Declared as my own inspection; evidence about our assets only.

**F04 (Keepers).** The ring-and-spoke/armillary primitive appears on, at minimum: the handheld astrolabe (declared), the left pauldron disc, the baldric boss, **three** separate tabard/skirt chart panels, the starter figure's satchel-flap clasp, the chest lid medallion and its interior instruments, two pedestal orbs, the plaza compass-rose floor, the scene armillary, and roundels in the arch stonework. **≥ 11 surfaces on one sheet.** Alongside it: the tabard panels carry pseudo-constellation chart lines that differ panel-to-panel (glyph-gibberish + non-repeatable insignia); the pauldron disc attaches to nothing (functional implausibility).
→ **The correction this forces:** the bleed is **not confined to the character.** The plaza floor, the architecture and the props carry it too. A bible rule scoped only to the character will not fix the sheet. **Every rule needs a `scope` field.** `[motif → bible field]`

**F03 (industrial).** No single graphic motif recurs. Instead a *material treatment* — rust + rivet + strap — is applied uniformly across coat plates, locker, pipes and crates. The character wears doubled belts and a chest harness whose buckles terminate in nothing; the long-arm's action/breech has no coherent mechanism; both hands are soft or occluded at the grip. The scene is lit by warm interior lamps while the character plates are flat front-left key — **key-light disagreement between panels of the same sheet.**
→ **This is the clause-2 correction (§ 1.6):** F03's defects are functional implausibility, not over-texture. Material-first did not buy safety; it bought a different, worse-measured failure family.

**vfx_style_match.png.** Character plate native 512 px, VFX plate native 256 px (labelled in the image). The ice burst reads as a radial star with near-uniform spoke lengths and a blown white core; the staff-tip effect on the character and the standalone VFX differ in crystal facet size and core value. **The same declared element renders at two grain scales across two canvases.** → scale must be declared in *source pixels of the feature*, never as "large/small". `[scale, palette → bible field + oracle]`

### 1.6 Verdict on gandalf's working hypothesis

**Clause 1 — "motif-nouns bleed": SUPPORTED as phenomenon, CORRECTED as formulation.**
Supported by observation (≥11 surfaces) and by an adjacent literature construct (E1). Corrected because F04's bleed lands on nouns the prompt almost certainly *did* ask for as scene content — an armillary sphere in an observatory plaza, a compass rose on an observatory floor. The rule is not "a motif noun leaks onto other nouns." It is: **once a geometric primitive is present anywhere in the scene, it becomes the sheet's default ornament for every surface that needs one.** I would call it **primitive capture**. The operational difference is large: you cannot fix it by removing the motif noun from the character prompt, because the plaza, the props and the architecture will still supply it. You fix it by declaring, per scope, *what ornament each surface class is allowed to carry — including "none."* `[motif, plain-budget → bible field]`

**Clause 2 — "material/construction-nouns over-texture": PARTIALLY REFUTED. This is the finding most likely to change the plan.**
F03 does over-texture (rivets everywhere). But its *load-bearing* defects — doubled straps carrying nothing, buckles closing nothing, a firearm with no mechanism, hands hidden at the grip — are **functional implausibility**, which CHI measures as the most prevalent artifact class (58.7%) and the least-detected of the big three (64.1%). Material-first prompting therefore does **not** escape the structural tell class; it **swaps** semantic leakage for the tell family that humans catch least often and that a JUDGE instance will therefore also most often pass. If Run C-1 concludes "prompt with materials, not motifs, and we're clear", the run will be trading a visible defect for an invisible one. **The mitigation is not a register change; it is construction vocabulary in the bible — every strap declares an endpoint, every fastener declares what it closes.** `[construction → bible field + oracle + JUDGE axis]`

**Clause 3 — "the tell is detail without ownership": STRONGLY SUPPORTED, with a corollary gandalf may not want.**
It is a good vernacular name for CHI's most prevalent category. The corollary: because it is the hardest class for a human observer to catch, **it is the class least suited to a JUDGE and most in need of a deterministic oracle** — which is precisely the hard case (ownership is a relational property; see the R8 backlog, § 3.9). The honest position is that O9 (transcribe→compare, § 3.7) is the *only* shortlisted instrument that reaches it at all, and it reaches it through a model, not through closed form.

---

## 2. Thread R7 — what real ARPG / stylized-2D art bibles contain, and a schema

### 2.1 What I could and could not inspect

**Inspected directly:** a complete, published, real production art bible — *Fleur's Fabel* (Beeyou), `aeno.nl/uploads/Art-bible.pdf`, 20+ slides, read page by page. **PRACTITIONER-REPORT** (real artifact, small-studio, not AAA). Blizzard's official Diablo IV quarterly update on art direction — **PRIMARY (studio-published)**. The polycount wiki *Art Bible* page — **community standard; fetch failed (connection refused), contents known only via search summary → SECONDARY.**
**Not inspected:** the GDC Vault talks (D3 "The Art of Diablo 3"; Bourassa "A Torch in the Dark", GDC 2016 — a copy exists at archive.org as video) and the NZGDC17 GGG art panel. All cited below as **SECONDARY** via trade-press reports. No published art *document* exists for D2/D3/D4, Path of Exile, Grim Dawn or Hades — only talks, art books and interviews. Grim Dawn / Crate returned **nothing usable** (§ 4).

### 2.2 What the real bible actually contains (the concrete precedent)

Section order as published: **Art style** (General → 2D assets → 3D environmental assets → Shaders/VFX) · **Reference / Moodboards** (general art style & textures) · **Character art** (character designs) · **Character design workflow** · **3D production workflow** · **Camera** · **Level of details** · **Atmosphere** · **Reference/Moodboards** (environment atmosphere & colors) · **Color Palette** (environment first area / second area / third area / characters) · **User Interface**.

Rule statements as written — note how short and how *checkable* they are:
- *"Simple, clear shapes"*; *"Flat colors & cel shading, dark outline"*; *"Mostly using natural colors; saturated colors to appeal to target audience."*
- *"Only character using blue in color scheme to create contrast with forest residents."* ← **an exclusion rule with a stated reason, scoped to one entity.**
- *"Flower on hat changes color with emotion."* ← **a placement rule with a state dependency.**
- *"Character colors are generally a bit brighter and lighter than the environment to make the characters stand out."* ← **a figure/ground relation rule, directly measurable.**
- *"Slight fog in background blurs objects in background & helps draw player's attention to the foreground."*
- *"Illustrated cutscenes with multiple panels can make use of a limited color palette without shading to save production time."*
- Per-area palettes are given as **literal swatch strips** (7–12 chips per area), plus a per-character swatch strip under every character.

**The three structural lessons I take from it (marked as reading):** rules are one sentence; palettes are *pictures of colours*, not adjectives; and the document is organised by **scope** (character / environment / VFX / UI / camera) before it is organised by anything else.

### 2.3 How studios keep many assets "one game"

- **Diablo IV — pillars as a filter. PRIMARY.** Two named pillars, *"old masters"* and *"a return to darkness"*, described as *"a lens to filter art through"* and as *"instrumental in keeping the team consistent and aligned."*
- **Diablo III — shared philosophy + archetype with twists. SECONDARY.** *"Style over realism, Strong Silhouettes, Bold Use of Color, Dynamic Animations"*; classes use *"archetypal characterization, though small design twists produced variations"*; legibility subordinates art to gameplay.
- **Overwatch — per-hero distinctness under one render law. SECONDARY.** *"making sure the characters were immediately identifiable in the middle of battle"* as the bedrock of hero design; shape language assigned per hero; 60-30-10 colour distribution as common practice.
- **Fleur's Fabel — shared render law + per-entity palette reservation. PRACTITIONER-REPORT.** One render rule for everybody (flat colour, cel shading, dark outline); a colour *reserved* to one character.

**The pattern across all four (synthesis, UNVERIFIED as a generalisation):** *shared render language; per-entity distinctness carried by palette and silhouette; ornament as the per-entity variable.* F04 does the exact inverse — shared ornament, no per-entity reservation — which is why it reads as one texture rather than one world. `[motif, palette, silhouette → bible field]`

### 2.4 Schema proposal for Faction Bible v0, each field justified

Extending gandalf's draft `RULE {}`. **Bold = additions or changes I am proposing; each carries its precedent and grade.**

```
RULE {
  id
  faction
  scope: character | prop | environment | vfx | ui          ← NEW
  class: motif|material|construction|silhouette|palette|plain-budget|light|scale
  statement            (one sentence)
  placements[]         {where, scale_px, count}             ← scale in SOURCE PIXELS
  exclusions[]         (where NOT — stated positively where possible)
  parts_ref[]          (names from the faction PARTS table) ← NEW
  reference_asset      (crop path | null)
  known_bad            (crop path)
  oracle               {id | JUDGE-only, threshold, inputs, needs_part_masks}  ← NEW sub-field
  source: matt-ruling | bible-author | oracle-feedback
  date, status
}
```

Plus **two faction-level tables the rules reference** (this is the change that makes oracles possible at all):

```
PILLARS[2..3]   { name, one-line filter statement }         ← D4 precedent
PALETTE         { scope, swatches[hex], relation_rules[] }  ← Fleur's Fabel precedent (literal swatches)
PARTS[]         { name, adjacency[], rigidity: rigid|soft|cloth,
                  attachment_to, palette_bin, allowed_motifs[], plain: bool }  ← NEW
LIGHT           { key_azimuth_deg, key_elevation, fill_ratio, source_count }
SCALE           { canvas_px, feature_size_px per class }
```

| Field | Precedent | Grade |
|---|---|---|
| `scope` on every rule | Fleur's Fabel is organised by scope first; polycount's section list is Characters / Environments / UI / Camera / Props / References | PRACTITIONER-REPORT + **OBSERVED necessity** (F04's bleed crosses scopes) |
| `PILLARS` (2–3, filter-shaped) | D4: *"old masters"* + *"return to darkness"*, stated as a consistency device | **PRIMARY** |
| motif inventory + `placements[]` + `exclusions[]` | Fleur's Fabel: *"Only character using blue…"* (exclusion w/ reason); *"Flower on hat changes color with emotion"* (placement + state) | PRACTITIONER-REPORT |
| `PALETTE.swatches[hex]` per scope, literal | Fleur's Fabel prints swatch strips per character and per area; D4 *"expert use of color palettes"* | PRACTITIONER-REPORT + PRIMARY-adjacent |
| `PALETTE.relation_rules[]` (figure vs ground) | Fleur's Fabel: *"Character colors…brighter and lighter than the environment"*; D3 three-layer value structure | PRACTITIONER-REPORT + SECONDARY |
| silhouette / read-at-distance | D3 legibility-first + distinctive silhouettes; Overwatch identifiability | SECONDARY |
| **`plain-budget`** | **No studio names it.** Three adjacent precedents only: D4 *"controlled use of detail"*; D3 barebones→ornate progression; Fleur's Fabel *"Level of details"* section | **EXTENSION — say so in the bible** |
| **`PARTS[]` with adjacency / rigidity / attachment / `palette_bin`** | No art-bible precedent found. Precedent is from the adjacent 3D texturing pipeline: an **ID map** is *"a baked texture where each material region of a model is filled with a flat solid colour"*, used to auto-mask material assignment — i.e. production already decomposes a costume into named regions with reserved flat colours | PRACTITIONER-REPORT (adjacent domain) — **this field is what makes § 3.3(c) possible** |
| `LIGHT` (key azimuth + source count) | CHI physics category makes divergent shadows a tell; Fleur's Fabel states atmosphere/lighting per area | VERIFIED (tell) + PRACTITIONER-REPORT (practice) |
| `SCALE` in source pixels | OBSERVED necessity (`vfx_style_match.png`, 512 vs 256); Fleur's Fabel *"Size ratio depending of screen size"* | OBSERVED + PRACTITIONER-REPORT |
| `reference_asset` | polycount: bibles carry concept art and *"multiple iterations of some of the concepts"* | SECONDARY |
| **`known_bad`** | No art-bible precedent. Comes from ML evaluation practice (negative controls); DSG's contribution is precisely that a checklist without controls yields inconsistent answers | **EXTENSION**, warranted by § 3.2 |
| **`oracle{}`** | No precedent in any art bible. This is the novel half of the instrument | **EXTENSION** |

**Construction logic — the one class with the least precedent and the most need.** No published art bible I found states construction rules ("every strap terminates at a named attachment; every fastener closes a named gap"). Given § 1.6 clause 2, this is the field that carries the most weight and the least borrowed authority. Gandalf should author it knowing it is ours, not inherited. `[construction → bible field]`

---

## 3. Thread R8 — deterministic oracles and judgment gates

### 3.1 Metric inventory

| # | Metric | What it measures | Closed-form or model-backed | Needs part masks? | Known failure modes | Grade |
|---|---|---|---|---|---|---|
| 1 | **CLIP-I / DINO-I** (DreamBooth protocol) | subject fidelity: cosine similarity of CLIP ViT-B/32 or DINO ViT-S/16 embeddings, generated vs reference | model-backed | N (but see #2) | averages over the **whole image including background**; CLIP-I insensitive within a class — DINO preferred *"as it is sensitive to the differences between subjects of the same class"* | VERIFIED |
| 2 | **MaSC** (masked SigLIP2, 2026) | subject fidelity restricted to a foreground mask; scene adherence with foreground masked *out* | model-backed **+ masks** | **Y** | *"depends on externally supplied foreground masks, which can introduce errors when segmentation fails or subjects are small, absent, or ambiguous"*; not applicable to style prompts; single-concept only | VERIFIED |
| 3 | **TIFA** (ICCV 2023) | faithfulness to a declared text spec via auto-generated QA answered by a VQA model | model-backed | N | VQA model error is the floor; questions can be non-atomic | VERIFIED |
| 4 | **DSG** (ICLR 2024) | same, with *atomic and unique* questions in dependency graphs | model-backed | N | built precisely because naive QG/A yields *"inconsistent answers"* | VERIFIED |
| 5 | **VQA compliance checking** (construction safety) | rules → questions → VQA → pass/fail gate | model-backed | N | domain-transfer unproven for art | VERIFIED (that the pattern is published) |
| 6 | **DCT/frequency artifact detection** (ICML 2020) | upsampling grid structure in frequency space | closed-form feature + trained classifier | N | GAN-era; see #7 | VERIFIED |
| 7 | **AI-image detectors** generally | generator-specific compression/encoding regularities — *not* semantics | model-backed | N | poor cross-generator generalisation; degraded by resize, JPEG, inpainting/repaint; framed as an *"unwinnable arms race"* | VERIFIED |
| 8 | **Laplacian variance / radial spectral energy** | high-frequency content ("brush grain") | closed-form (`scipy.ndimage.laplace`, `numpy.fft`) | optional | not a literature style metric — an engineering proxy; scale-dependent (must normalise by source px) | UNVERIFIED as a style oracle |
| 9 | **Hu moments / shape matching** | silhouette similarity | closed-form | Y (silhouette) | *"invariance is proved with the assumption of infinite image resolution"*; *"in case of raster images, the computed Hu invariants…are a bit different"*; **no universal cutoff — calibrate same-class vs different-class on your own imagery** | VERIFIED |
| 10 | **Normalised cross-correlation template match** | count of appearances of a specific crop | closed-form (`scipy.signal.fftconvolve`) | optional (Y to scope by placement) | scale/rotation sensitive → needs a scale pyramid + rotation bank; counts a *crop*, not a *concept* | VERIFIED (method) |
| 11 | **Palette adherence** (quantise → nearest declared swatch in CIELAB) | % of pixels off-palette + off-palette cluster centroids | closed-form (`numpy` + `sklearn.KMeans`) | N (Y for per-part) | anti-aliased borders and deep shadow/specular collapse toward achromatic | UNVERIFIED as published metric; standard practice |
| 12 | **Illumination-direction estimation** (luminance-weighted gradient azimuth) | key-light direction per asset / per part | closed-form (`scipy.ndimage.sobel`) | optional | painted shading is not physical; flat-lit regions give no signal | UNVERIFIED for painted art |
| 13 | **Flip-and-correlate symmetry** | left/right agreement of a part or silhouette | closed-form | Y for per-part | intentional asymmetry is indistinguishable from drift without a declared expectation | UNVERIFIED as published; trivially sound |

### 3.2 The transcribe → compare pattern (R8 addendum, item 1)

**Matt's pattern has a published name in the research literature, and the literature's contribution is exactly the reliability question he is asking.**

- **TIFA (ICCV 2023). VERIFIED.** *"automatically generate several question-answer pairs using a language model"* from the text input, then *"calculate image faithfulness by checking whether existing VQA models can answer these questions using the generated image"* — *"a reference-free metric."* Benchmark: *"TIFA v1.0, a benchmark consisting of 4K diverse text inputs and 25K questions across 12 categories (object, counting, etc.)."* Reported correlation with human judgment: **Spearman ρ = 0.60, Kendall τ = 0.47** for TIFA (mPLUG), *"significantly higher correlation…than all prior evaluation metrics, including CLIPScore"* (the ρ/τ figures are SECONDARY — from a report of the paper, not the abstract I read).
- **DSG (ICLR 2024). VERIFIED.** Produces *"atomic and unique questions organized in dependency graphs, which ensure appropriate semantic coverage and sidestep inconsistent answers."* Its stated motivation is the failure mode we would otherwise walk into: *"QG questions should respect the prompt (avoiding hallucinations, duplications, and omissions) and VQA answers should be consistent (not asserting that there is no motorcycle in an image while also claiming the motorcycle is blue)."* DSG-1k: 1,060 prompts.
- **VQA as a compliance gate, in a safety-critical domain. VERIFIED (that it is published):** construction-safety checking converts *"safety rules into corresponding questions"* and feeds question–image pairs to a VQA model to infer answers. This is the closest published analogue to "the bible is the DAX."

**Direct mapping to Matt's T-Mobile pattern:** bible = the declared truth (his posted DAX) → question set generated *from the bible*, atomic and unique (DSG) → a separate Astra instance answers by perception only (his transcriber) → a deterministic script compares answers to declarations and emits the diff (his comparator). **The precedent is sound. The novelty is only the domain.**

**Measured reliability of the transcriber — the numbers that constrain the design:**
- **Bounding boxes are out of reach. VERIFIED (domain-shifted).** On object localization, *"GPT-4V obtains a mean intersection-over-union (IoU) of 0.16; only 7.6% of test images have an IoU > 0.5."* (Earth-observation imagery — remote sensing, not illustration; the direction of the finding transfers, the magnitude may not.) Corroborating, across a spatial benchmark: *"task-specific vision models outperform general-purpose VLMs by a clear margin for spatial localization"*, with GPT-4o and Gemini 2.5 among the lowest.
- **Counting is the weakest task family. VERIFIED.** *"Counting remains the lowest-accuracy task across state-of-the-art VLMs (64.0 to 74.7%)."* Grounding from an object detector measurably mitigates counting hallucination.
- **Giving the model boxes helps it reason** (*"average accuracy increases over 33 points when given bounding box information"*) — i.e. boxes are a good **input** to the transcriber and a bad **output** from it.

**Therefore, the TRANSCRIBE contract (bible field + oracle):**
1. Ask only for **presence/absence** and **per-part counts** against a **closed list of declared part names** — never for coordinates, never open-vocabulary.
2. Make every question **atomic and unique** (DSG), with dependencies: do not ask "what colour is the satchel clasp" before "is there a satchel clasp."
3. **Cross-check every count with a deterministic counter** (O3) where one exists; the VLM count is the hypothesis, the template count is the measurement.
4. **Known-bad controls are mandatory** in every question set — at least one declared-absent part per run — because DSG's entire contribution is that un-controlled question sets return self-inconsistent answers.
5. Emit a strict inventory JSON with a fixed schema, so the comparator's failures are *parse* failures, not *interpretation* failures.
`[all classes → oracle (O9) + bible field]`

### 3.3 Getting part masks on CPU-only tooling (R8 addendum, item 2)

**(a) Model-generated ID / clown pass — asking the image model to repaint a frame in flat per-part label colours.**
**No published evidence found**, either for or against, in two passes. What I do have is vendor text pointing the wrong way: masking with GPT Image is *"entirely prompt-based… may not follow its exact shape with complete precision"* (M3) — the same prompt-driven machinery you would be relying on for pixel-accurate label alignment. **Grade: UNVERIFIED, with a discouraging adjacent signal.** The *concept* is thoroughly precedented one domain over: an ID map is *"a baked texture where each material region of a model is filled with a flat solid colour"* so that *"a green pixel becomes leather, blue becomes metal, red becomes fabric"* — and the practice carries a warning that transfers directly: keep each colour *"maximally distinct so anti-aliasing at the borders doesn't create an ambiguous intermediate colour that confuses the mask generator."*
→ **If attempted, it must be validated against a hand-made mask on at least one known-good frame before any gate depends on it** — measure per-part IoU between the ID pass and the hand mask, and report it. Do not let an unvalidated ID pass become an oracle input. `[construction → oracle input, gated by validation]`

**(b) SAM-class on CPU.**
**VERIFIED:** MobileSAM runs *"around 10ms per image on a single GPU: 8ms on the image encoder and 4ms on the mask decoder"*, and is *"4 times faster than FastSAM"* (40 ms). **No CPU per-image benchmark found** in two passes — recorded as a gap. Two further constraints, both first-hand: at T0 neither `torch` nor `onnxruntime` is installed, so this is a dependency decision with a real install and a real per-frame cost, not a free option; and **SAM-class is class-agnostic** — it returns regions, not "the satchel." Naming is a separate step (MaSC obtained its masks with *"SAM3 prompted by the canonical concept name"*). **Grade: feasible, unbenchmarked on our target hardware and image class.** `[construction → oracle input, deferred]`

**(c) Deterministic colour-classification given disjoint per-part palettes — "design the costume so the oracle can read it."**
**This is the strongest T0 option and it has two independent precedents.** (i) The ID-map practice above *is* this idea, applied at authoring time, with the explicit purpose of making automated masking work. (ii) Game readability practice already reserves colour per entity: Fleur's Fabel's *"Only character using blue in color scheme to create contrast with forest residents"*; the 60-30-10 distribution convention; Overwatch/D3 identifiability-first design.
**Named failure modes — all three must be in the bible, not discovered later:**
- **Anti-aliasing at every border** produces intermediate colours that belong to no bin. Mitigation: erode each classified region by 1–2 px before measuring; report the unclassified border fraction as a health metric, not as a defect.
- **Shading.** A painted part's colour is a *range* under a value ramp, not a constant. Classify in a luminance-de-weighted space (CIELAB `a*b*` only, or HSV hue+saturation); accept that deep shadow and specular highlight collapse toward achromatic and are **unclassifiable by construction**. Report unclassified-pixel fraction per part; if it exceeds a threshold the part's measurements are void, not failing.
- **The art pays for it.** Reserving disjoint hue bins per part is a genuine aesthetic constraint and it competes with the palette rules in § 2.4. The bible must own the trade explicitly — which parts get reserved bins, and which are deliberately left unmeasurable.
**Grade: PRACTITIONER-REPORT (both precedents), UNVERIFIED for painted-2D sprites specifically.** `[palette, construction → bible field (PARTS[].palette_bin) + oracle]`

### 3.4 Part-level consistency metrics once masks exist (R8 addendum, item 3)

**Warrant for going part-level at all: VERIFIED.** MaSC's finding is exactly this — *"Global cosine for CP averages over the whole image, including background variation that humans correctly ignore when judging identity"* — and masking the measurement lifts agreement with humans to *"Krippendorff α=+0.471 on CP…reaching 72% of the human inter-rater ceiling"* and *"AUC=0.992"* on ORIDa, *"the first non-LLM metric to outscore GPT-4o."* Restricting a similarity measurement to the part you care about is a published, measured improvement, not an intuition.

All of the following are **closed-form given masks**, computable with `numpy`/`scipy` at T0:

| Metric | Defect it catches | Bible input | Notes |
|---|---|---|---|
| **Mask area drift** (per-part area / total figure area, across frames) | "the satchel volume changing" | `PARTS[].name` | normalise by figure area, not by pixels — pose changes total extent |
| **Centroid relative to torso frame** (part centroid in torso-normalised coords) | attachment drift (the pauldron migrating) | `PARTS[].attachment_to` | needs a stable torso reference part; fails on extreme pose |
| **Per-part palette distance** (mean CIELAB distance to declared bin) | material drift | `PARTS[].palette_bin` | de-weight luminance (§ 3.3c) |
| **Motif template count inside vs outside allowed parts** | **motif bleed — the headline oracle** | `placements[]`, `exclusions[]`, motif crop | this is the one metric that directly scores § 1.6 clause 1 |
| **Mirrored-part symmetry** (flip-and-correlate on paired parts) | near-symmetry drift on paired armour | `PARTS[].adjacency`, a `mirror_of` relation | needs a declared expectation; intentional asymmetry otherwise reads as failure |
| **Per-part high-frequency energy** | brush-grain inconsistency; over-texture (F03's rivets) | `SCALE.feature_size_px` | must normalise by source px or it measures canvas size (§ 1.5) |
| **Per-part shading-gradient azimuth** | key-light disagreement between panels | `LIGHT.key_azimuth_deg` | flat-lit parts give no signal; aggregate across parts with a circular mean and report dispersion |

`[construction, material, palette, light, scale, motif → oracles; PARTS[] → bible field]`

### 3.5 Low-resolution / black-and-white silhouette oracles (R8 addendum, item 4)

**What they catch:** gross silhouette identity across frames and turnaround views — the read-at-distance rule that D3 and Overwatch both put first. Downsampling to 48–64 px and binarising discards exactly the ornament that is drifting, which is why it is a *stable* consistency signal while the surface is noisy.

**Instruments, in order of preference:**
1. **IoU after alignment** (centroid + scale normalisation, optionally 1-D rotation search) — the most interpretable, and the one to threshold on.
2. **Contour distance** (e.g. symmetric mean nearest-neighbour distance between boundary point sets) — catches localised silhouette bulges that IoU averages away.
3. **Hu moments** as a *secondary*, cheap screen only. **VERIFIED caveats:** the invariance *"is proved with the assumption of infinite image resolution"*; *"in case of raster images, the computed Hu invariants for the original and transformed images are a bit different"*; and *"there is no universal matchShapes cutoff — you should record same-class and different-class scores from your production imaging setup, then choose a threshold based on acceptable false-positive and false-negative rates."*

**Thresholding practice, therefore: do not import a number.** Calibrate on our own anchors — compute the same-asset-across-frames distribution and the different-asset distribution from the F03/F04 sheets, and set the gate where the two separate. Report both distributions with every threshold the bible states. `[silhouette → oracle (O5) + bible field (threshold recorded with its calibration set)]`

**What they miss:** everything the bible actually cares about — motif placement, palette, material, ownership. A silhouette gate passing means only that the figure is the same shape. It is a *necessary* gate, never a sufficient one.

### 3.6 Game-dev practice and commercial tools

- **Peer-reviewed synthesis (CHI 2026, "Generative AI in Game Development: A Qualitative Research Synthesis").** Full text was **403 to me** (ACM paywall) — so this is **SECONDARY**, via search summary, and flagged as such: it reports that *"without structured post-processing, explicit acceptance criteria, and accountable checks, generated materials fail to satisfy pipeline requirements"*; that specifications *"should state asset-class acceptance criteria and error budgets"*; and that *"integration gates should be supported by evaluation harnesses and provenance capture at hand-off, so that model updates and parameter changes are auditable."* That is a direct, independent endorsement of the instrument gandalf is building — **but I did not read the paper and should not be quoted as having done so.**
- **Scenario.** Two passes over its docs and knowledge base surfaced LoRA style-model training (15–50 reference images, 20–40 min jobs), inpainting, upscaling, reskinning — **no exposed consistency score, no gate, no threshold**. **Grade: no gates found.**
- **Ludo.ai / Layer.ai.** Layer.ai trains studio-style models; Ludo's "Ludo Score" evaluates *game ideas* (originality, market trends, success potential), not art conformance. Third-party reviews score tools on "style consistency" as a **reviewer criterion**, not a product feature. **Frame Lab / SpriteCook / Spriterrific: nothing found in two passes.** **Grade: marketing, not measured.**
- **SPRITE (2026 preprint, mockups → engine-ready game UI).** Read directly. **Employs no deterministic acceptance gate**: evaluation is three senior UI/UX designers on a 10-point Likert scale (visual fidelity 8.5, hierarchical logic 8.0, interaction accuracy 7.0), *"no numerical thresholds for acceptance."* Quality comes from model-backed pipeline stages (VLM scaffolding, GroundingDINO + SAM2, LaMa inpainting). **VERIFIED — and it is a useful negative result: even a 2026 asset-generation pipeline paper ships with expert review, not oracles.**

**Bottom line for R8.2: nobody published has built what we are building.** The acceptance-criteria *principle* is endorsed in the literature; the *instruments* are not on the shelf.

### 3.7 The shortlist — applicable to Run C-1 now (10)

T0 = system `python3` (PIL, numpy, scipy, sklearn; **no cv2/skimage/torch**). "Cost" is my estimate of build effort for a first working version, not of runtime.

| id | Oracle | Enforces (tell / rule class) | Inputs needed **from the bible** | Form | Needs part masks? | T0 cost | Confidence |
|---|---|---|---|---|---|---|---|
| **O1** | **Palette adherence** — quantise asset, nearest declared swatch in CIELAB, report % off-palette + off-palette cluster centroids | palette drift; material drift | `PALETTE.swatches[hex]` per scope; tolerance ΔE | closed-form (numpy + sklearn) | **N** | low (~half a day) | **High** |
| **O2** | **Figure/ground value separation** — mean + spread of luminance inside figure alpha vs outside | the Fleur's Fabel / D3 readability rule | `PALETTE.relation_rules[]`; expected sign + minimum delta | closed-form | N (figure alpha only) | low | **High** |
| **O3** | **Motif-instance count** — normalised cross-correlation of the motif crop over a scale pyramid + rotation bank; count peaks; partition inside vs outside declared placements | **motif bleed / primitive capture** (§ 1.6 cl. 1) | motif reference crop; `placements[]`; `exclusions[]`; scale range | closed-form (`scipy.signal.fftconvolve`) | **Y** to scope by placement; N for a raw sheet-wide count | medium (scale/rotation bank is the work) | **Medium-high** for a raw count; **medium** for scoped |
| **O4** | **Plain-surface budget** — fraction of figure area whose local edge/contrast energy is below a threshold | ornament creep; the plain-budget rule | `plain-budget` target fraction; `PARTS[].plain` | closed-form (`scipy.ndimage`) | **Y** for per-part; N for whole-figure | low-medium | **Medium** (threshold needs calibration) |
| **O5** | **Silhouette consistency at 64 px** — binarise, align on centroid + scale, IoU; contour distance as secondary; Hu moments as a cheap screen | silhouette drift across frames / turnaround | declared frame set; calibrated threshold + its calibration set | closed-form | Y (figure silhouette) | low | **High** (with § 3.5's calibration rule observed) |
| **O6** | **Per-part read via disjoint palette bins** → area drift, torso-relative centroid, per-part palette distance | construction / attachment / material drift | `PARTS[]` with `palette_bin`, `attachment_to`, `adjacency` | closed-form **given the costume is designed for it** | **Y (produces them)** | medium; **plus an art constraint** | **Medium** — two precedents, unproven on painted 2D |
| **O7** | **Key-light azimuth** — luminance-weighted gradient azimuth per asset (and per part where masks exist); circular mean + dispersion across panels | key-light disagreement (§ 1.5, E2) | `LIGHT.key_azimuth_deg`, tolerance | closed-form (`scipy.ndimage.sobel`) | optional | low-medium | **Medium** — painted shading is not physical |
| **O8** | **Brush-grain band energy** — radial spectral profile normalised to source pixels, compared to the anchor | render-register drift; the 512-vs-256 grain mismatch (§ 1.5, E3) | `SCALE.canvas_px` + `feature_size_px`; anchor asset | closed-form (numpy FFT) | N | low-medium | **Medium** — engineering proxy, not a literature metric |
| **O9** | **TRANSCRIBE → COMPARE inventory gate** — bible → atomic DSG-shaped questions → separate Astra answers presence/absence + counts against a closed part list → deterministic comparator; known-bad controls every run | **ownership / functional implausibility** (§ 1.6 cl. 3) — the only instrument here that reaches it | `PARTS[]` closed list; `placements[]`; `exclusions[]`; declared-absent controls | **model-backed** (no local model needed — it is an Astra call) | N | medium — the comparator is easy, the question generator and the control discipline are the work | **Medium** — pattern VERIFIED (TIFA/DSG), reliability on illustrated part inventories **unmeasured** |
| **O10** | **Cross-frame identity** — DINO-I (preferred over CLIP-I) on the masked figure crop; MaSC-shaped if masks exist | character identity drift across a sprite sheet | anchor frame set; mask source | **model-backed — NOT T0** (`torch` absent) | Y (masked variant) | **high** — dependency install + model weights | **Medium-high** as a metric; **low** as a near-term action |

**Standing up O1, O2, O5 first** buys three gates in roughly a day of work, all closed-form, all calibratable on the assets we already have. **O3 is the headline** and should be next. **O9 is the only route to the § 1.6 clause-3 defect** and should be prototyped with known-bad controls before anyone trusts a number from it. **O10 is a deferred dependency decision, not a Run C-1 item.**

### 3.8 Bible ↔ oracle coverage table

Columns per brief § 4 plus the addendum's `needs part masks?`.

| Tell / rule class | Mitigation (prompt lever) | Deterministic oracle | Needs part masks? | JUDGE-only? | Vocabulary the bible must carry | Evidence grade |
|---|---|---|---|---|---|---|
| **Motif placement + bleed** (primitive capture) | positive single-naming + positive plainness assertion (M1); two-pass ornament-as-edit (M2); motif crop as labelled reference (M4) | **O3** | Y to scope; N for raw count | no | motif crop path; `placements[] {where, scale_px, count}`; `exclusions[]`; **`scope`** | phenomenon OBSERVED; mechanism UNVERIFIED for gpt-image; oracle method VERIFIED |
| **Ornament without function / ownership** | construction vocabulary: every strap declares an endpoint, every fastener declares what it closes (§ 1.6 cl. 2) | **O9 only** (partial) | N | **largely yes** | `PARTS[] {attachment_to, adjacency}`; per-part "what does this close" statements | class VERIFIED (CHI 58.7% / 64.1%); oracle coverage weak |
| **Palette / material drift** | declare literal swatches in-prompt; material-first nouns (M7) | **O1**, **O6** (per-part) | N global / Y per-part | no | `PALETTE.swatches[hex]`, ΔE tolerance, `PARTS[].palette_bin` | precedent PRACTITIONER-REPORT; method standard |
| **Plain-surface budget** | positive plainness assertion; "production asset" register (M5) | **O4** | Y per-part | no | target plain fraction; `PARTS[].plain` | **EXTENSION** — no studio names the field |
| **Silhouette / read-at-distance** | silhouette language in prompt; neutral pose declaration | **O5** | Y (silhouette) | no | frame set; threshold **plus its calibration set** | VERIFIED caveats; SECONDARY precedent |
| **Figure/ground readability** | declare relative value of figure vs ground | **O2** | N | no | `PALETTE.relation_rules[]` with sign + minimum delta | PRACTITIONER-REPORT |
| **Key-light consistency** | declare key azimuth + source count per sheet | **O7** | optional | partly | `LIGHT {key_azimuth_deg, elevation, source_count}` | tell VERIFIED; oracle UNVERIFIED for painted |
| **Feature scale / grain** | declare feature size in source px, not adjectives | **O8** | N | no | `SCALE {canvas_px, feature_size_px}` | OBSERVED need; proxy UNVERIFIED |
| **Near-symmetry drift** | declare which parts are mirrored | flip-and-correlate (folds into **O6**) | **Y** | partly | `PARTS[].mirror_of` | trivially sound; UNVERIFIED as published |
| **Glyph gibberish** | forbid rendered text; declare sigils as shapes, not letters | **O3** on a sigil crop (partial) | N | partly | "no rendered text anywhere" as a faction-level rule | class VERIFIED (CHI) |
| **Material confusion at boundaries / edge halos** | declare edge treatment | **none** — border pixels are exactly what O6 must erode away | Y (and it degrades them) | **yes** | edge-treatment statement | class VERIFIED; **no oracle** |
| **Specular / sheen in painted work** | render-register vocabulary (matte, painted, no rim-light) | partial via **O8** (HF energy) | N | **largely yes** | render-law statement (cf. "flat colors & cel shading, dark outline") | class VERIFIED; oracle weak |
| **Anatomy, hands, grips** | pose declaration; hands-visible clause | **none** | N | **yes** | pose/grip statements | class VERIFIED (CHI 51.4%); no closed-form oracle |
| **Intra-object perspective drift** | declare orthographic/isometric intent | **none** | N | **yes** | projection statement | class VERIFIED |
| **Faction-fiction plausibility** | pillar statements (D4 precedent) | **none** | N | **yes** | `PILLARS[2..3]` | analogy to CHI sociocultural; UNVERIFIED |
| **Cross-frame identity** | reference conditioning + invariant edits (M2/M4/M6) | **O10** (not T0) | Y (masked variant) | partly | anchor frame set | VERIFIED metric; not T0 |
| **"Is it AI at all"** | — | **do not build one** | N | n/a | — | **VERIFIED contraindication** (arms race; cross-generator and post-processing fragility) |

### 3.9 R8 backlog — rules with no oracle (JUDGE-only, for now)

1. **Ownership/causation as a relation** — "does this buckle close something." O9 reaches it only through a model's answer; no closed-form form exists. **Highest-value backlog item, because it is the most prevalent and least-detected tell class.**
2. **Anatomy, hands, weapon grips** — no closed-form instrument; specialist detectors exist but are model-backed and none were validated on painted 2D in my passes.
3. **Perspective/projection coherence within an object.**
4. **Material *reading*** — that a surface reads as leather rather than merely occupying leather's colour bin. O1/O6 measure the colour, not the read.
5. **Edge-treatment quality** — and note the perverse interaction: border pixels are simultaneously the site of this tell and the pixels O6 must discard.
6. **Faction-fiction plausibility** — pillar conformance.
7. **Intentional vs accidental asymmetry** — undecidable without a declaration; convert to an oracle by adding `mirror_of` to `PARTS[]`, which is a bible move, not an oracle move.

---

## 4. Knowledge gaps not resolved

Two focused passes per thread were run; these are the gaps that remain, with the next source I would try.

1. **No artifact taxonomy exists for stylized / painted / illustrated generation.** The CHI 2025 taxonomy is explicitly photorealism-only. Every transfer in § 1.1 is an assumption. **And "motif bleed" appears in no artifact taxonomy at all** — its nearest literature relative (attribute binding) is a Stable-Diffusion cross-attention result whose transfer to GPT-image architecture is unverified. *Next source:* illustrator-authored critique corpora and the concept-art community's own discourse, read as a primary corpus rather than via listicles.
2. **No measured reliability figure for VLM part-inventory transcription on illustrated images.** All the numbers I could anchor (IoU 0.16; counting 64.0–74.7%) come from photographic or remote-sensing domains. Since O9 is the only instrument that reaches the highest-prevalence tell class, this is the gap with the most leverage. *Next step, and it is cheap:* measure it ourselves on F03/F04 against a hand inventory, with declared-absent controls — that is a one-session experiment and it would produce a number nobody has published.
3. **No CPU benchmark for MobileSAM / FastSAM per image**, and no evidence at all — for or against — for model-generated ID/clown passes on 2D generated art. Combined with the first-hand finding that `torch`/`onnxruntime`/`cv2` are absent at T0, the entire model-backed masking route is unpriced. *Next step:* time MobileSAM on one of our frames on this hardware before it enters any plan.

Further gaps, recorded without elaboration: no *published art bible document* exists for D2/D3/D4, Path of Exile, Grim Dawn or Hades — only talks, art books and trade-press summaries; **Grim Dawn / Crate returned nothing usable in two passes**. The GDC Vault talks (D3 art direction; Bourassa's "A Torch in the Dark", GDC 2016, also on archive.org as video) were **not inspected** — every D3/Bourassa claim here is SECONDARY. The CHI 2026 gen-AI-in-gamedev synthesis was **403** (ACM paywall) and is cited as SECONDARY only. No concept-art-pedagogy primary source was found articulating "design vs rendering" in the brief's terms. No commercial game-art AI tool was found to expose a gate, threshold or consistency score (Scenario, Layer.ai, Ludo inspected; Frame Lab, SpriteCook, Spriterrific not found).

---

## 5. Source list

See `sources.json` for the machine-readable list with per-source grade and thread. Principal sources, by grade:

**Primary — vendor documentation (read directly):** OpenAI image-generation guide, `developers.openai.com/api/docs/guides/image-generation` (accessed 2026-09-11); the vendored OpenAI `imagegen` skill at `~/.codex/skills/.system/imagegen/` — `SKILL.md`, `references/prompting.md`, `references/image-api.md`, `references/sample-prompts.md`.

**Primary — peer-reviewed / preprint (read directly):** *Characterizing Photorealism and Artifacts in Diffusion Model-Generated Images*, CHI 2025, arXiv 2502.11989 · *MaSC: A Masked Similarity Metric for Evaluating Concept-Driven Generation*, arXiv 2605.22469 · *TIFA*, ICCV 2023, arXiv 2303.11897 · *SPRITE: From Static Mockups to Engine-Ready Game UI*, arXiv 2604.18591 · *The Unwinnable Arms Race of AI Image Detection*, arXiv 2509.21135.

**Primary — studio-published:** Blizzard, *Diablo IV Quarterly Update — March 2022*, news.blizzard.com.

**Primary — practitioner artifact (read page by page):** *Fleur's Fabel* Art Bible, Beeyou, `aeno.nl/uploads/Art-bible.pdf`.

**Secondary (reports of primary sources I could not open):** Game Developer on GDC 2012 *The Art of Diablo III* · GDC Vault entries for *The Art of Diablo 3* and Bourassa's *A Torch in the Dark* (not opened) · CHI 2026 *Generative AI in Game Development: A Qualitative Research Synthesis* (ACM 403) · DreamBooth CLIP-I/DINO protocol · Attend-and-Excite (SIGGRAPH 2023, arXiv 2301.13826) · DSG (ICLR 2024, arXiv 2310.18235) · *Good at captioning, bad at counting* (CVPRW 2024, arXiv 2401.17600) · *Spatial Reasoning in Foundation Models* (arXiv 2509.21922) · MobileSAM (arXiv 2306.14289) · OpenCV shape-descriptor documentation and LearnOpenCV Hu-moments guidance · Frank et al., ICML 2020 · polycount wiki *Art Bible* · Scenario / Layer.ai / Ludo.ai product documentation · Substance Painter ID-map practice references.

**First-hand (this session):** T0 tooling probe of the system interpreter and all three project repos; inspection of `F04.png`, `F03.png`, `vfx_style_match.png`.

---

**Signed:** legolas (UNKNOWN-RESEARCHER). Findings only — no design direction, no tooling authorisation, no generation. gandalf synthesises; Matt rules the vocabulary.
