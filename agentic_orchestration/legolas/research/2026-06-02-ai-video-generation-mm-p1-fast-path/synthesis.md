# Research — AI Video Generation for MM-P1 Fast-Path — 2026-06-02

**Mode:** A (analytical)
**Commissioner:** gandalf per Matt 2026-06-02 ratification
**Priority:** URGENT
**Sources consulted:** See Source List below. Primary sources: official API docs, vendor research pages, OpenRouter benchmark listings. Secondary sources: independent pricing/review aggregators (CheckThat.ai, MagicHour.ai, eesel.ai). Tertiary: community analysis (Medium, Substack), blog roundups.
**Knowledge cutoff caveat:** This is a fast-moving space. Pricing, availability, and features for all candidates below are subject to change. All rates cited are as of May-June 2026 per sources accessed. Model names may have newer variants by the time this is consumed.

---

## Summary (5 sentences)

The AI video generation landscape in mid-2026 is genuinely capable of producing MM-P1 quality output — the "visually compelling video performance" target — at costs of $20-80 and within 1-3 days of production work for 5 characters × 4 stages. Runway Gen-4.5 is the strongest candidate for the MM-P1 use case because it combines single-reference-image character consistency with native 60-second multi-shot generation, an available API, commercial license, and direct applicability to staged narrative sequences (Stage A constellation → Stage B materialization → Stage C customization → Stage D gear-reveal). Google Veo 3.1 is a credible second option offering superior raw visual quality and structured JSON prompting support, but at higher per-second cost and with an 8-second clip cap requiring manual stitching. The fundamental limitation of the video approach relative to UE is that it produces a fixed-frame performance rather than an interactive artifact — the Chernoff parameter-binding (player molds parameters → character morphs) cannot be demonstrated, only illustrated by showing multiple pre-generated variants side-by-side. The honest assessment is: this IS a much faster path to MM-P1 as Matt hypothesizes IF the acceptance criterion is "visually compelling video demonstration of what the experience will look like"; it is NOT a viable path if MM-P1 requires the interactive parameter-binding to be demonstrable.

---

## Section 1: Candidate Survey

### 1.1 Google Veo 3.1

**Status:** Active, production-available (June 2026). Veo 3.1 supersedes Veo 3 and Veo 2; Veo 3.1 Lite/Fast/Quality are the three tiers.

**Input format:** Text prompts + up to 4 reference images ("Ingredients to Video"). Supports frames-to-video (two anchor images). Structured JSON prompting is natively supported per multiple sources. Does NOT accept arbitrary JSON character specs directly — these must be translated to natural language prompts (see Section 5).

**Video length:** 8 seconds per clip. Multi-clip narrative requires manual stitching. However, up to 20 chained clips are supported via Veo's scene extension feature, enabling 140+ second total narratives.

**Character consistency:** "Ingredients to Video" — upload up to 4 reference images; the model uses them for character, object, style, and background continuity. Fast model: ~94.2% frame consistency; Quality model: ~96.7%. Cross-generation consistency (separate API calls) requires re-supplying reference images each time — no persistent character token.

**Quality:** Best raw visual fidelity in class (June 2026). True 4K at 3840×2160, up to 60fps. Native synchronized audio in a single pass. "Veo 3.1 Quality" tier is the cinematic-grade option.

**API access:** Available via Gemini API, Vertex AI, fal.ai, Replicate, and OpenRouter. Fully pay-per-use.

**Pricing:**
- Veo 3.1 Lite: ~$0.03-0.05/sec (no audio)
- Veo 3.1 Fast: ~$0.10-0.15/sec (with audio)
- Veo 3.1 Quality: ~$0.20-0.40/sec (with audio, best consistency)
- For 5 characters × 4 stages at 8 sec/clip via Quality tier: 160 seconds × $0.40 = ~$64 at ceiling; ~$32 at midpoint. More practical estimate with Fast tier: ~$16-24 total for 20 clips.
- Google AI Pro subscription: $19.99/month. Ultra: $249.99/month (first 3 months at $124.99).

**Latency:** Generation time not specified per clip in sources; Fast mode noted as "speed-optimized."

**Commercial license:** Full commercial rights on paid plans.

**Accessibility:** Available now globally via Gemini API and partner platforms.

---

### 1.2 OpenAI Sora 2

**Status:** API-only as of April 26, 2026 (consumer app discontinued). API scheduled to sunset September 24, 2026. This creates a hard deadline risk for any ongoing use.

**Input format:** Text prompts + image references (JPEG/PNG/WebP as first-frame conditioning). Formal JSON batch API supported (`POST /v1/videos` with JSON payload). Character assets stored via `POST /v1/videos/characters` endpoint — a formal character registry.

**Video length:** Up to 20 seconds per generation (up to 120 seconds via 6 chained extensions of 20 seconds each). Character consistency works best on 2-4 second clips per documentation.

**Character consistency:** Formal `characters` endpoint — upload reference, reference by name in prompts across multiple generations. Single video supports up to 2 characters simultaneously. This is the most technically rigorous character persistence mechanism of any candidate.

**Quality:** Sora 2 / Sora 2 Pro. 720p (Standard) or true 1080p (Pro). Physics accuracy noted as a strength in comparative reviews.

**API access:** Available via `developers.openai.com`. Programmatic batch API documented.

**Pricing:**
- Sora 2 Standard: $0.10/sec (720p), $0.05/sec Batch
- Sora 2 Pro: $0.30/sec (720p), $0.50/sec (1080p), $0.70/sec (1024p) Standard; ~half on Batch
- For 20 clips × 8 sec at Sora 2 Standard: $16. At Sora 2 Pro 1080p: $112. Batch 50% discount applies.

**Latency:** Not specified; asynchronous with polling/webhooks.

**Commercial license:** User owns generated content with rights to distribute/sell per OpenAI policies.

**Accessibility:** Available now but SUNSET RISK: full shutdown September 24, 2026. Any MM-P1 pipeline relying on Sora 2 has a hard 4-month usage window.

**SUNSET NOTE:** This is a material risk flag. If MM-P1 video mock is produced with Sora 2, the pipeline dies in September 2026. Not recommended for any sustained use.

---

### 1.3 Runway Gen-4.5

**Status:** Active production. Gen-4.5 released December 1, 2025. API available February 10, 2026.

**Input format:** Text prompts + reference images (1-4 images for character/location/object consistency). The reference image system encodes identity (facial structure, body proportions, style) into every frame without fine-tuning.

**Video length:** Up to 60 seconds in a single generation pass (Gen-4.5 multi-shot mode). Single-prompt multi-shot sequencing — describe a wide establishing shot, medium shot, and close-up in one prompt and receive a single output with transitions while maintaining character and environmental continuity. This is the strongest feature for MM-P1 staged sequences.

**Character consistency:** "Identity encoding" system — 95%+ character consistency across shots from a single reference image. Described as "infinite character consistency with a single reference image." Front-facing 1024×1024 portrait with even lighting and neutral expression yields best results; off-angle or low-quality references drop consistency by ~30%.

**Quality:** Ranked #1 in Artificial Analysis Video Arena blind preference tests in early 2026 (overtook Veo 3.1 and Sora 2 Pro). "Physical + cinematic" generation. Native synchronized audio.

**API access:** Documented REST API. Runway also provides access to Google Veo, Kling, Seedance, FLUX, and Seedream through a single subscription — ecosystem breadth.

**Pricing (Gen-4.5):**
- API: 25 credits/sec = $0.25/sec (at $0.01/credit)
- Per 5-second clip: $0.30 (12 sec × $0.25 = $3.00 for a 12-second reveal sequence in a single pass)
- For 5 characters × 4-stage sequence in 60-sec passes: potentially 5 × 1 generation = $5 × ($0.25 × ~30 effective seconds per character) ≈ $37.50 at ceiling
- More realistically at 15 sec per character: 5 × 15 × $0.25 = $18.75 total
- Subscription: Standard $12-15/month, Pro $35/month, Unlimited $95/month

**Latency:** Not explicitly stated; asynchronous standard.

**Commercial license:** Runway ToS explicitly states they claim no rights over user-generated videos. Commercial use confirmed on paid plans.

**Accessibility:** Available now globally.

---

### 1.4 Kling 3.0 (KuaiShou)

**Status:** Active production (Kling 3.0 as of mid-2026).

**Input format:** Text prompts + image/video references. "Motion Control" — extract motion pattern from reference video and apply to different subject.

**Video length:** Up to ~30 seconds per generation. Native multi-shot storyboard with character locking.

**Character consistency:** "Character locking" — model creates latent representation of character, maintains across all shots in a generation. Described as "uniquely strong for character-driven content." Multi-angle subject consistency specifically highlighted.

**Quality:** "Physical + cinematic," good motion quality. Noted slightly behind Runway in character consistency benchmarks, but significantly improved in 2026.

**API access:** Available via direct API and third-party platforms (fal.ai at ~$0.90/10-second clip).

**Pricing:**
- API: ~$0.07-0.14/sec (standard vs. priority)
- fal.ai: ~$0.90/10-second clip
- Subscriptions: Standard ~$10/month, Pro ~$37/month, Ultra ~$180/month

**Commercial license:** Commercial use on paid plans.

**Accessibility:** Available. Chinese company; no noted geographic restrictions for API access.

---

### 1.5 Hailuo 2.3 (MiniMax)

**Status:** Active production. Hailuo 2.3 released 2026; previously Hailuo 02.

**Input format:** Text prompts + subject reference image (face photo for facial consistency within single generation). Up to 9 images + 3 video clips + 3 audio files in a single multimodal request.

**Video length:** Not explicitly cited; typical clips are 5-10 seconds based on pricing context. Multi-shot support present.

**Character consistency:** Subject reference maintains facial consistency within a single generation using `subject_reference` parameter. Cross-generation (separate API calls) does NOT maintain consistency without re-supplying reference. Facial recognition + body tracking for intra-clip consistency.

**Quality:** Strong for anime/illustration/game CG styles. Noted for "frame-perfect motion precision for facial expressions and choreographed sequences." Good fit for stylized fantasy rather than photorealism.

**API access:** Direct API at platform.minimax.io. Also available via Atlas Cloud and third-party aggregators.

**Pricing:**
- API: ~$0.01-0.03/sec (Fast tier); ~$0.19/5-second video
- Subscription: Standard $9.99/month (1000 credits), Unlimited $94.99/month
- Lowest per-second cost of all candidates

**Commercial license:** Commercial use available on paid plans.

**Accessibility:** Available globally.

**MM-P1 note:** Best price-to-quality ratio for stylized/game-art aesthetic. Weakest for photorealistic cross-generation character persistence.

---

### 1.6 Luma Dream Machine (Ray3.14)

**Status:** Active production. Latest model Ray3.14 (2026 update).

**Input format:** Text prompts + reference images. "Character Seeds" — maintain identity consistency across multiple generated clips (introduced 2026 update).

**Video length:** 10 seconds per clip standard. Ray3.14 is 4x faster than predecessor, lower cost.

**Character consistency:** "Character Seeds" feature for cross-clip identity persistence. Single reference image suffices.

**Quality:** Solid mid-tier. 1080p native. Ray3.14 HDR is the premium tier.

**API access:** Comprehensive developer API at $0.32/million pixels generated, billed separately from consumer subscriptions.

**Pricing:**
- API: $0.32/million pixels — complex to estimate directly; roughly comparable to mid-tier competitors for standard 1080p 10-second clips
- Subscriptions: Plus $30/month, Pro $90/month, Ultra $300/month

**Commercial license:** Commercial rights on paid plans.

**Accessibility:** Available globally.

---

### 1.7 Seedance 2.0 (ByteDance)

**Status:** Active production. Released early 2026.

**Input format:** Text + up to 9 images + 3 video clips + 3 audio files in a single request. Up to 12 reference assets. Text-to-video, image-to-video, multimodal.

**Video length:** Multi-shot native generation. Director-level control. Specific per-clip max not confirmed but multi-shot narrative is core feature.

**Character consistency:** Rated "best in industry" for character consistency preservation across serialized content by multiple 2026 sources. Particularly strong for recurring-character content.

**Quality:** Cinematic. Native audio. "Physical + cinematic" generation with "synchronized audio in a single pass."

**API access:** Available via OpenRouter and Atlas Cloud. API is live.

**Pricing:**
- $0.081/sec (Fast mode), $0.10/sec (standard quality)
- ~5 characters × 4 stages at 10 sec/clip = 200 sec × $0.10 = $20 total

**Commercial license:** Commercial use on paid plans.

**Accessibility:** Available now. ByteDance origin; no noted geographic restrictions for API access.

---

### 1.8 Pika 2.0+

**Status:** Active but API access limited to select partners. Not suitable for programmatic batch generation at this time.

**Character consistency:** Drag-and-drop character-into-scene feature. Trails Runway and Sora in photorealism.

**API access:** Restricted/select-partner only. NOT suitable for automated pipeline.

**Verdict:** Exclude from MM-P1 recommendation due to API access limitations.

---

### 1.9 Adobe Firefly Video

**Status:** Video generation available via Firefly plans and via API (enterprise agreement required).

**Character consistency:** Not a documented feature of Firefly Video at current state.

**API access:** Enterprise agreement required; $1,000/month minimum commitment. Not suitable for small-scale use.

**Commercial license:** Strongest commercial safety story — trained only on Adobe Stock, openly licensed, and public domain content. Output is explicitly cleared for commercial use with indemnification.

**Verdict:** Commercial safety advantage is real but the enterprise-minimum barrier and lack of character consistency features make it unsuitable for MM-P1 fast-path. Could become relevant if legal clarity on generated content becomes a requirement.

---

### 1.10 Stable Video Diffusion / Open Source

**Status:** Stable Video Diffusion (SVD) and its successors (CogVideoX, etc.) are available open-source.

**Character consistency:** No native cross-generation character persistence without fine-tuning (LoRA/DreamBooth training).

**Quality:** Behind top commercial models for photorealism. Suitable for stylized outputs with effort.

**API access:** Self-hosted or via Replicate. Low cost but requires technical setup.

**Verdict:** Requires significant ML engineering to achieve character consistency. Not on the MM-P1 fast path. Worth flagging for Phase 2 if custom model fine-tuning becomes desirable.

---

## Section 2: Per-Candidate Analysis Matrix

| Candidate | Input Formats | Character Consistency | Clip Length | Multi-Shot Native | API Available | Pricing (20 clips ×8s) | Commercial | Accessibility |
|---|---|---|---|---|---|---|---|---|
| **Veo 3.1** | Text + 4 images | 94-97% (in-session) | 8s max | Extension chaining | Yes | ~$16-64 | Yes (paid) | Global, now |
| **Sora 2** | Text + image ref + formal character API | Formal character registry | 20s max (120s extended) | Extension model | Yes | ~$16-112 | Yes | API-only; SUNSETS Sep 2026 |
| **Runway Gen-4.5** | Text + 1-4 image refs | 95%+ single-ref | 60s native multi-shot | YES (native) | Yes | ~$18-37 | Yes (no claim) | Global, now |
| **Kling 3.0** | Text + image/video | Strong (character locking) | ~30s | Native storyboard | Yes | ~$14 | Yes (paid) | Global, now |
| **Hailuo 2.3** | Text + 9 imgs + 3 vids + 3 audios | Intra-clip only (no cross-gen) | ~5-10s | Some | Yes | ~$4-6 | Yes (paid) | Global, now |
| **Luma Ray3.14** | Text + image | Character Seeds (cross-clip) | 10s | Some | Yes | ~$20-30 est | Yes (paid) | Global, now |
| **Seedance 2.0** | Text + 12 assets | Best-in-class (per sources) | Multi-shot native | YES (native) | Yes | ~$20 | Yes (paid) | Global, now |
| **Pika 2.0** | Text + image | Moderate | ~5-10s | No | Restricted | N/A | N/A | Partner-only API |
| **Adobe Firefly** | Text + image | Not documented | 5-8s | No | Enterprise ($1K/mo) | N/A | Strongest | Enterprise only |
| **SVD (open source)** | Text + image | Requires fine-tuning | ~3-4s | No | Self-hosted | Low + setup | Varies | Requires ML setup |

---

## Section 3: Recommended Path for MM-P1 Fast-Path Video Production

### Primary recommendation: Runway Gen-4.5

**Rationale:** Runway Gen-4.5 best matches MM-P1 requirements across all five critical dimensions:

1. **Native 60-second multi-shot generation** — a single prompt can describe the full 4-stage character reveal arc (constellation form → materialization → customization → gear reveal) and produce it as one coherent clip with transitions. This directly maps to the Stage A/B/C/D narrative structure without requiring manual stitching between separate API calls.

2. **Single-reference-image character consistency at 95%+ across shots** — one well-composed portrait of the character (generated via image model first) can anchor all 5 characters across their full reveal sequences.

3. **Commercial license is unambiguous** — Runway ToS explicitly disclaims rights over user output. No downstream legal complexity for MM-P1 demo use.

4. **API is live and documented** — can be called programmatically. Character specs can be translated to structured prompts (see Section 5) and batch-generated.

5. **Narrative control** — multi-shot sequencing with described camera compositions supports the "performance" framing Matt described.

**Recommended workflow for 5 characters:**

Step 1 — Character portrait generation (1-2 hours): Use Midjourney v7 or FLUX to generate a single reference portrait per character, anchored to their element and archetype. This is the "character seed" image.

Step 2 — Prompt authoring (2-4 hours): For each of the 5 characters, author a single ~1000-token Gen-4.5 multi-shot prompt describing the 4-stage sequence. Substrate JSON fields map directly to prompt components (see Section 5).

Step 3 — Generation (1-3 hours, mostly wait time): Submit 5 API calls with reference images. At 60 seconds/generation and async execution, total generation time is likely 30-90 minutes of wall-clock time.

Step 4 — Review and iterate (2-6 hours): Review outputs; regenerate clips where staging doesn't land. Budget for 2-3 iterations per character.

Step 5 — Light post-production (optional, 1-4 hours): Add title cards, music, VFX overlay. Can be done in CapCut, DaVinci Resolve, or Adobe Premiere.

**Total estimated horizon:** 1-3 days of focused effort for a single operator.

### Secondary recommendation: Seedance 2.0

For the specific goal of sustained character consistency across serialized content (if MM-P1 requires re-generating the same character across many sessions), Seedance 2.0's "best-in-class" character consistency rating makes it worth evaluating in parallel. Cost is also lower ($20 total for all 20 clips at $0.10/sec).

### For highest raw visual quality: Google Veo 3.1 Quality tier

If visual fidelity is the single most important criterion (cinematic-grade output for an investor or publisher demo), Veo 3.1 Quality tier produces superior visual output. The trade-off is 8-second clip max (requires stitching), no native multi-shot sequencing, and higher cost. This would require a "Veo stitched" post-production step but the output quality ceiling is the highest available.

---

## Section 4: Estimated Cost + Horizon vs. UE Pipeline

### Video-mock path (Runway Gen-4.5, primary recommendation)

| Cost component | Estimate |
|---|---|
| Reference portrait generation (5 chars, Midjourney) | $0 (existing subscription) or ~$10 ad hoc |
| Runway Pro subscription (1 month) | $35/month |
| API overage / extra generations | $20-50 (buffer for iterations) |
| Light post-production tool (CapCut or free DaVinci) | $0 |
| **Total cost** | **$45-95** |
| **Production horizon** | **1-3 days** |
| **Prerequisites** | Runway account, reference images, prompt authoring |

### UE pipeline path (comparison baseline)

| Cost component | Estimate |
|---|---|
| FAB asset acquisition (CC5 chars, Synty, Mutable) | $200-800+ |
| Niagara VFX pack | $80-200 |
| UE seam agent role definition + dispatch authoring | 1-2 weeks team coordination |
| UE project setup (landscape, lighting, Sequencer) | 1-3 weeks engineering |
| Character rigging + Sequencer cinematics for 5 chars | 2-4 weeks |
| **Total cost** | **$280-1000+ in assets + engineering time** |
| **Production horizon** | **4-12 weeks** |
| **Prerequisites** | UE5 seam established, agent roles defined, assets acquired |

**Delta:** Video-mock path is ~50-100x faster and 10-20x cheaper at this scope. The cost differential narrows significantly if the UE pipeline is built for reuse (i.e., MM-P2 real implementation would reuse the work). But the HORIZON differential — days vs. months — is the deciding factor for Matt's question about a "much faster path."

---

## Section 5: Composition with Character Spec JSON

### Translation pathway

None of the candidate services accept raw JSON as a direct ingestion format. All require natural language prompts. However, a prompt-generation layer is readily constructed from the kit JSON fields:

**Kit JSON fields → Prompt components:**

```
primary_element → "shadow energy", "flame-wreathed", "gale-force wind", etc.
emergent_kit_concept → character name and archetype basis
skills[].name → ability visuals in gear-reveal stage
skills[].flavor_text → direct prompt fodder (e.g., "From the void between worlds, darkness condenses into a bolt of pure shadow energy")
t4_selection.spirit_guide_narration_metadata.manifestation → T4 visual moment description
t4_selection.spirit_guide_narration_metadata.thematic_rationale → character arc framing
bc_range → spatial positioning in video (ranged: staff raised, distant targeting)
bc_attribute → visual class (INT: robes, glowing runes, caster aesthetics)
```

**Example prompt fragment for kit_shadow_000007 (Penumbra Caster):**

```
STAGE A (0-8 seconds):
A celestial constellation in deep void space, individual stars pulsing with shadow energy, slowly assembling into a humanoid outline of pure absence — an anti-light figure against the star field. The silhouette breathes, darkness folding into itself.

STAGE B (8-20 seconds):
The constellation collapses inward and a robed shadow caster materializes in tattered medieval scholar's garments, intelligence burning in pale eyes, shadow energy coiling at their fingertips. From the void between worlds, darkness condenses around their form.

STAGE C (20-35 seconds):
Close on face — angular features, shadow-dark skin, silver runes along jaw and temple, hair dissolving at edges into wisps of shadow. A bone-carved staff forms in their grip.

STAGE D (35-55 seconds):
Full reveal: the character stands in T4 power. The entire shadow chain collapses inward simultaneously — bolt, burst, eruption all folding at once into a dense matte shell (Penumbral Inversion Shell). Armor of crystallized mana-absence absorbs incoming light. The air goes flat and cold.
```

**Pipeline design:** A thin Python script (30-50 lines) could take each kit JSON, extract the fields above, fill a prompt template with LLM assistance (Claude Haiku or GPT-4o-mini at near-zero cost), and emit a Runway Gen-4.5 API call. This makes the full 5-character batch programmable.

### LLM-mediated prompt generation

The kit flavor_text fields and spirit_guide_narration_metadata fields are already high-quality narrative copy. Passing them through a brief LLM prompt ("Convert the following character spec into a Runway Gen-4.5 multi-shot video prompt following this 4-stage structure:...") will produce usable prompts without manual authoring, reducing the Step 2 effort from 2-4 hours to 15-30 minutes.

---

## Section 6: Honest Viability Assessment

### What the video path CAN deliver

- Visually compelling 60-second reveal sequences per character with cinematic quality
- Consistent character appearance across stages of the reveal within a single generation
- Fantasy/dark-fantasy aesthetic appropriate to the Reincarnated aesthetic register
- A watchable "video performance" that communicates the MM-P1 character design vision to any viewer
- Production-ready in days, not months
- Cheap enough to be disposable / re-runnable as designs evolve

### What the video path CANNOT deliver

**The Chernoff parameter-binding is not demonstrable.** The core MM-P1 architectural concept is "player molds chernoff parameters → character form responds." A video is a fixed playback — a viewer watches the same reveal every time. There is no interaction, no molding, no parameter control. The video can ILLUSTRATE the intended experience ("here is what it will look like when a player chooses shadow + ranged + variable amplitude"), but it cannot demonstrate that parameters actually drive the output.

**Implication for MM-P1 framing:** If Matt's "visually compelling mock-up of what it will look like as a video performance" is primarily a COMMUNICATION artifact (showing investors, Matt's son, early playtesters what the game WILL look like), the video path is fully viable. If MM-P1 needs to be an INTERACTIVE proof of concept where someone can actually move a slider and see a character change, the video path is not viable — a lightweight interactive prototype (even a static HTML parameter → image-swap would demonstrate this better than video).

### Fidelity ceiling comparison

| Dimension | Video mock (Runway Gen-4.5) | UE5 pipeline |
|---|---|---|
| Visual quality of single frame | Near-cinematic (AI-generated, dreamlike) | Photorealistic to stylized (controllable) |
| Character consistency within reveal | 95%+ | 100% (deterministic) |
| Character consistency across re-runs | Variable (re-generation differs) | 100% (deterministic) |
| Interactive parameter binding | NOT POSSIBLE | Full (intended architecture) |
| Fantasy VFX quality | Good (prompt-driven, unpredictable) | Excellent (Niagara, controllable) |
| Art direction control | Moderate (prompt fidelity ~60-80%) | High (direct placement) |
| Reproducibility | Low (each generation is unique) | High |
| Time to produce 5-char demo | 1-3 days | 4-12 weeks |
| Cost | $45-95 | $280-1000+ |
| Requires UE expertise | No | Yes |
| Platform for MM-P2 | No (dead end; must rebuild in UE) | Yes (direct continuation) |

### Is this "a MUCH faster path to MM-P1"?

**Yes, with a specific framing caveat.** If MM-P1 = "I can show someone a compelling video of what the character creation experience will look and feel like," then AI video generation delivers this in 1-3 days for under $100. That is unambiguously much faster and much cheaper than the UE pipeline.

The strategic question is whether that is SUFFICIENT for Matt's MM-P1 success criterion. The commission brief cites Matt's exact words: "a visually compelling mock-up of what it will look like as a video performance." The word "performance" is load-bearing — it suggests fixed-frame video is the intended output, not an interactive prototype. If that reading is correct, the video path is the right path for MM-P1.

If however the intent was "a mock-up that demonstrates the parameter-to-character pipeline working," video cannot demonstrate that. A lightweight browser prototype (even using static images swapped by a slider) would be needed.

**Recommendation:** Surface this framing question to Matt before committing to either path. The question is: "Is MM-P1 a video you show people, or a prototype you hand to people?" If video: proceed with Runway Gen-4.5 immediately. If interactive: the video path is supplementary (useful for visual reference), but a minimal interactive prototype is also needed.

---

## Section 7: Trade-Off Matrix

| Factor | Video-Mock Path | UE-Pipeline Path |
|---|---|---|
| **Production speed** | 1-3 days | 4-12 weeks |
| **Cost** | $45-95 | $280-1000+ (assets) + engineering time |
| **Interactive** | No | Yes |
| **Parameter binding demonstrable** | No | Yes |
| **Visual quality (single viewing)** | Near-cinematic | Photorealistic to stylized |
| **Art direction control** | Moderate | High |
| **Reproducibility** | Low | High |
| **Reusable toward MM-P2** | No (throwaway) | Yes (foundation) |
| **UE seam setup required** | No | Yes (team effort) |
| **FAB asset purchases required** | No | Yes |
| **Risk of failure** | Very low (models are proven) | Moderate (UE pipeline complexity) |
| **Demonstrates game vision** | Partially (visual only) | Fully (interactive) |
| **Suitable for investor/publisher demo** | Yes (for concept) | Yes (for interactive demo) |
| **Suitable for Matt's son to play with** | No | Yes |
| **Suitable for game page teaser** | Yes | Yes |

---

## Knowledge Gaps Not Resolved

1. **Runway Gen-4.5 exact generation latency per 60-second clip** — sources describe it as async but don't specify wall-clock time. Likely 5-15 minutes per generation based on comparable models; needs empirical testing.

2. **Veo 3.1 JSON prompt structure** — sources confirm structured JSON prompting is supported; the exact schema is not documented in accessible public sources. Would require API testing.

3. **Sora 2 character API persistence** — whether the formal `POST /v1/videos/characters` endpoint maintains cross-session consistency (i.e., does the character persist between API calls from different sessions, or only within a session). Sunset risk makes this moot for sustained use.

4. **Runway Gen-4.5 multi-shot sequencing for the specific Stage A (celestial/constellation) → Stage B (human materialization) transition** — this is a demanding stylistic transition (abstract cosmic → realistic human). Quality of this specific type of transition is not confirmed in sources. Empirical testing would be needed.

5. **Seedance 2.0 character consistency across separate API calls** — sources describe it as "best in class" but do not specify whether this requires re-supplying the same reference assets each call or if there's a persistent character token.

6. **Commercial license nuances for game-commercial use** — all sources cite "commercial use on paid plans," but none specifically address use of AI-generated video as part of a shipped commercial game product vs. a demo/mockup. For MM-P1 as an internal mockup this is not a concern; for a published game trailer it warrants legal review.

---

## Source List

1. [Google Veo Pricing Calculator — CostGoat](https://costgoat.com/pricing/google-veo)
2. [Veo 3 API Pricing 2026 — veo3ai.io](https://www.veo3ai.io/blog/veo-3-api-pricing-2026)
3. [Google Veo 3.1 Review 2026 — BuildFastWithAI](https://www.buildfastwithai.com/blogs/google-veo-3-1-ai-video-generator)
4. [Google Veo 3 adds 1080p, 9:16, drops prices — The Decoder](https://the-decoder.com/google-veo-3-adds-1080p-916-video-and-drops-prices-by-half/)
5. [Veo 3.1 API Pricing — OpenRouter](https://openrouter.ai/google/veo-3.1)
6. [OpenAI API Pricing](https://openai.com/api/pricing/)
7. [Sora 2 Complete Guide 2026 — WaveSpeed](https://wavespeed.ai/blog/posts/openai-sora-2-complete-guide-2026/)
8. [Sora 2 API Pricing — CostGoat](https://costgoat.com/pricing/sora)
9. [Video generation with Sora — OpenAI API docs](https://developers.openai.com/api/docs/guides/video-generation)
10. [Sora Pricing 2026 — MagicHour](https://magichour.ai/blog/sora-pricing)
11. [Runway API Pricing & Costs — Runway docs](https://docs.dev.runwayml.com/guides/pricing/)
12. [Introducing Runway Gen-4 — Runway Research](https://runwayml.com/research/introducing-runway-gen-4)
13. [Introducing Runway Gen-4.5 — Runway Research](https://runwayml.com/research/introducing-runway-gen-4.5)
14. [Runway Gen-4.5 Review — AdCreate](https://adcreate.com/blog/runway-gen-4-5-review-features-pricing-2026)
15. [Runway Gen-4.5 Pricing — MagicHour](https://magichour.ai/blog/runway-gen-45-pricing)
16. [Runway Pricing 2026 — CheckThat.ai](https://checkthat.ai/brands/runway/pricing)
17. [Runway Gen-4 Character Consistency Guide — SelfieLab](https://selfielab.me/blog/runway-gen-4-character-consistency-guide-20260215)
18. [Creating with Gen-4 Image References — Runway Help](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References)
19. [Kling AI Pricing 2026 — MagicHour](https://magichour.ai/blog/kling-ai-pricing)
20. [Kling AI Complete Guide 2026 — AI Tool Analysis](https://aitoolanalysis.com/kling-ai-complete-guide/)
21. [AI Video Generation API Pricing April 2026 — BuildMVPFast](https://www.buildmvpfast.com/api-costs/ai-video)
22. [Hailuo AI Complete Guide 2026 — AI Video Bootcamp](https://aivideobootcamp.com/blog/hailuo-ai-complete-guide-2026/)
23. [MiniMax Hailuo 2.3 Review 2026 — ThePlanetTools](https://theplanettools.ai/tools/minimax-hailuo-2-3)
24. [Video Generation — MiniMax API Docs](https://platform.minimax.io/docs/guides/video-generation)
25. [Adobe Firefly API Pricing 2026 — SudoMock](https://sudomock.com/blog/adobe-firefly-api-pricing-2026)
26. [Adobe Firefly Video Pricing 2026 — ToolColumn](https://www.toolcolumn.com/learn/adobe-firefly-video-pricing)
27. [Seedance 2.0 API — OpenRouter](https://openrouter.ai/bytedance/seedance-2.0)
28. [Seedance 2.0 API Complete Guide — Atlas Cloud](https://www.atlascloud.ai/blog/ai-updates/seedance-2-0-api-complete-guide-to-multimodal-video-generation-2026)
29. [Luma Dream Machine Pricing 2026 — MagicHour](https://magichour.ai/blog/luma-dream-machine-pricing)
30. [Luma AI Review 2026 — GoEnhance](https://www.goenhance.ai/blog/luma-ai-review)
31. [Best AI Video Generators 2026 — GetAIPerks](https://www.getaiperks.com/en/blogs/44-best-ai-video-generators-2026)
32. [Sora 2 vs Veo 3 vs Runway Gen-4 — genra.ai licensing guide](https://genra.ai/blog/sora2-runway-gen4-veo3-ai-video-licensing-guide)
33. [AI Multi-Shot Video Character Consistency 2026 — AI Magicx](https://www.aimagicx.com/blog/ai-multi-shot-video-character-consistency-2026)
34. [JSON Prompting for AI Video Generation — ImagineArt](https://www.imagine.art/blogs/json-prompting-for-ai-video-generation)
35. [JSON Prompting for Video & Image Generation — LTX Studio](https://ltx.studio/blog/json-prompting-for-video-image-generation)
36. [Sora 2 vs Veo 3 vs Runway Gen-4 2026 comparison — Lushbinary](https://lushbinary.com/blog/ai-video-generation-sora-veo-kling-seedance-comparison/)
37. [The 2026 AI Video Production Playbook — Medium/DSC](https://medium.com/data-science-collective/the-2026-ai-video-production-playbook-bc683d5b85da)
38. [State of AI Video Generation February 2026 — Medium/Cliprise](https://medium.com/@cliprise/the-state-of-ai-video-generation-in-february-2026-every-major-model-analyzed-6dbfedbe3a5c)
