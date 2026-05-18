# Request — Star-Lord — Pitch-To-Life Vercel Automation Sprint

**From:** gandalf (story-and-design steward).
**To:** star-lord (orchestrator + LLM integration owner for this sprint).
**Approved by:** Matt (mhwetmore@gmail.com), 2026-05-18 — directive: bring the story/game-pitch to life inside the existing Vercel loadout app; integrate image-gen LLM API for season flavor text → hero portrait + season hype piece; structure as a star-lord-orchestrated dispatch that invokes gandalf / drax / elrond / galadriel as sub-agents.
**Status:** **AWAITING STAR-LORD ENGAGEMENT.** Activation requires star-lord session-open + Matt L3 on § 5 (vendor spend authorization).
**Priority:** **HIGH.** Drives the afternoon Marketing Director conversation with concrete artifacts.
**Operating mode:** Pattern-A orchestration sprint; star-lord is the integrator + LLM-call owner per seam definition; gandalf authors curation + copy; drax implements UI; elrond validates assets; galadriel captures the rendered pitch artifact for sharing.

---

## § 0 — TL;DR

A new pitch surface in the loadout app at `/pitch` (drax may pick `/showcase` or `/inside` — drax owns slug) presents Reincarnated as a publisher/exec-ready showcase. Three things drive it:

1. **One "Hero of the Engine"** — gandalf-curated single hero (across all current seasons) chosen by cohesiveness × uniqueness × flavor; rendered as a hand-painted-quality character portrait via image-gen LLM; presented with substrate-coded framing prose
2. **One "Season Hype Piece" per season** — all heroes of a chosen season composed as a multi-character lineup (generated individually + composited client-side; one anchor per season for iteration-1; iterate across remaining seasons in subsequent passes)
3. **Pitch narrative scaffolding** — copy that places these artifacts in the project's story: substrates, LLM-thematic-universe, agentic hive, mobile-feel target, paths-to-market

**Provider call:** Midjourney v8 (primary if API access confirmed) → GPT Image 2 (production fallback, low-risk default).

**Cost ceiling:** ≤$15 vendor spend per generation pass; Matt L3 on the spend authorization in § 5.

**Sprint shape:** star-lord orchestrates 4 sub-agents along a critical-path DAG (§ 7); single-night-class effort if Matt L3 on vendor spend lands fast; otherwise the dispatch is staged dispatch-ready and waits on L3.

---

## § 1 — The directive (Matt's words 2026-05-18 afternoon)

Matt:

> *"draft a completely automated plan for star-lord to invoke you and others as sub-agents and bring the story/game-pitch to life inside of our existing vercel web app. Importantly, I would like you to build an API call into the structure and feed it the flavor text of the season so that we can invoke the best image generating LLM to commission two images: 1 of the top hero across all seasons (most cohesive, most unique, most flavor) and one of all of the heroes of a given season as a seasonal hype piece."*

**Interpretation.** The pitch needs to be a *thing Matt can show*, not a *thing Matt has to describe*. Two specific image artifacts (top hero + season hype piece) anchored in real engine output (substrate identity + per-season cosmological vocabulary + class data) make the pitch tangible. The vercel-deployed loadout app is the shareable URL surface.

---

## § 2 — Scope

### § 2.1 — Image-gen pipeline (star-lord owns; gandalf authors prompts)

**Deliverable 1.** Build-time image generation script in the engine repo at `reincarnated-engine/scripts/pitch/generate_hero_images.py` (path indicative; star-lord may relocate per his seam conventions):

- Reads from `output/standard-demo-regen-2026-05-17/season_*/manifest.json` + `cosmological_vocabulary.json` + `classes/*.json`
- For each class: constructs a prompt from substrate identity + cosmological vocab + archetype + iconic_verbs + iconic_register via the locked prefix template (§ 4.2)
- Calls chosen image-gen provider API per § 4
- Stores generated images under `reincarnated-loadout/public/pitch/heroes/<season_id>/<class_slug>.png` (or whichever public-assets path drax confirms is loadable)
- Generates a manifest at `reincarnated-loadout/public/pitch/heroes-manifest.json` mapping season → class → image-path + prompt-used + provider + generation-timestamp

**Deliverable 2.** Per-season cosmological vocabulary normalized into a loadout-app-consumable bundle at `reincarnated-loadout/src/data/pitch/seasons.json` — flattens the per-season cosmological_vocabulary.json + anchor + theme_element + class-list + roster into a single bundle. Drax consumes this in his React components.

**Deliverable 3.** Cost ledger at `reincarnated-loadout/public/pitch/cost-ledger.json` — every API call logged with provider, image-count, cost-per, total, timestamp. Matt audits.

### § 2.2 — Top-hero curation pass (gandalf as sub-agent)

**Deliverable 4.** Gandalf authors `agentic_orchestration/gandalf/findings/2026-05-18-pitch-top-hero-curation.md` selecting:

- **One "Hero of the Engine"** across all seasons — single cross-season standout
- **One "Hero of the Season"** per season — one anchor hero per season for the hype-piece center position

Curation rubric per § 6. Output names: class_slug, season_id, substrate, archetype, role, the cosmological_vocabulary fields that make this hero sing, and **the bespoke prompt** for the image-gen call.

### § 2.3 — `/pitch` page implementation (drax as sub-agent)

**Deliverable 5.** New React route `/pitch` (or chosen slug) in the loadout app. Structure per § 6.

- Component scaffold: `pages/Pitch.tsx`; section components per § 6
- Consumes `seasons.json` + `heroes-manifest.json`
- Renders Hero of the Engine spotlight + Season Hype Pieces + pitch narrative copy + cross-links into `/the-work` analytics suite (if iteration-1 of that ships in parallel)
- Mobile-first per Matt's standing mobile-feel-target lock
- Push to main triggers Vercel preview auto-deploy

### § 2.4 — Asset validation (elrond as sub-agent)

**Deliverable 6.** Elrond produces a short validation pass at `agentic_orchestration/elrond/findings/2026-05-18-pitch-asset-validation.md`:

- Confirms every selected class has a substrate-icon mapping in the existing icon library (or flags the gap)
- Confirms substrate-accent palette per § 3 of `loadout-analytics-suite-information-architecture-2026-05-18.md` is colorimetric-coherent with generated image dominant hues (sanity check; not blocking)
- Surfaces any catalogue asset that could augment the rendered page (e.g., anchor-location concept art if it exists in the curated catalogue)

### § 2.5 — Pitch artifact capture (galadriel as sub-agent)

**Deliverable 7.** Galadriel captures the deployed `/pitch` page at multiple viewports + as a shareable single-image artifact:

- Full-page captures at desktop 1920×1080, tablet 1024×1366, mobile portrait 1290×2796
- Hero-of-the-Engine spotlight as standalone shareable image (cropped frame with attribution-bar overlay)
- Filed at `agentic_orchestration/galadriel/captures/2026-05-18-pitch/`
- Surfaces in hive log + provides Matt with paste-ready URLs for the afternoon meeting

### § 2.6 — Vercel deployment posture

- **Preview-URL deployment is PRE-AUTHORIZED** (auto-deploys on push to main; standard loadout pattern)
- **Production-URL promotion is MATT L3** (different question from preview; production-URL pitch surface needs Matt sign-off before any external sharing)

---

## § 3 — Per-seam initial tasking

| Seam | Initial task | Why first |
|---|---|---|
| **Star-lord** | (a) Verify Matt L3 on § 5 vendor spend; (b) Pick provider per § 4 (MJ v8 if API access confirmed, else GPT Image 2); (c) Author the image-gen script scaffold + cost-ledger; (d) Sequence gandalf curation pass + drax UI scaffold + elrond validation in parallel; (e) Once gandalf curation lands, run image-gen pipeline; (f) Coordinate drax push → Vercel preview → galadriel capture | Star-lord owns LLM integration; star-lord orchestrates the sub-agent chain; vendor-spend authorization is the critical first gate |
| **Gandalf (sub-agent invocation)** | Curation pass per § 6.1: read all 5 canonical-7 seasons' classes + cosmological vocab + manifest; rank by the rubric; select Hero of the Engine + Hero per Season; author bespoke prompt per selected hero using § 4.2 template; file at `gandalf/findings/2026-05-18-pitch-top-hero-curation.md` | Curation is gandalf-judgment work, not numeric; depends only on existing season output; can begin in parallel with drax scaffold |
| **Drax (sub-agent invocation)** | Author `/pitch` page scaffold per § 6 component structure; placeholder for image assets (gandalf's curation determines which); consume seasons.json + heroes-manifest.json from star-lord's pipeline; do NOT depend on actual generated images to begin scaffolding (use placeholder boxes); after star-lord pipeline produces real images, swap placeholders | Implementation work parallelizable with curation; final assembly waits on both gandalf + star-lord landing |
| **Elrond (sub-agent invocation)** | Asset-validation pass per § 2.4; substrate-icon coverage + accent-palette coherence + catalogue augmentation surfacing | Independent of other tracks; informs drax's final assembly polish |
| **Galadriel (sub-agent invocation)** | Capture pipeline against deployed Vercel preview URL; multi-viewport + shareable single-image artifact; filed and surfaced | Final step — depends on drax push + Vercel preview live |

**Knight-rider's role:** OBSERVATIONAL ONLY. Star-lord is the orchestrator for this sprint; knight-rider may observe in hive log and route halt-condition surfaces if any arise, but does not coordinate.

---

## § 4 — Image-gen provider call

### § 4.1 — Locked recommendation (gandalf's call; star-lord may amend with Matt L3)

**Primary: Midjourney v8** if Matt confirms Pro-tier API access. Quality leads for dark painterly fantasy character portraiture; that is the Reincarnated register.

**Fallback: GPT Image 2** if MJ v8 API gated, flaky, or unavailable at Matt's account tier. Full official API; no access ambiguity; strong prompt-following; clean commercial license.

**Avoid:** unofficial MJ wrappers (ToS-violation risk); Imagen 4 (competitive but not the register lead); Flux 2 Pro (strong but rate is higher than GPT-2 with no quality advantage for this job); Adobe Firefly (best for legal indemnification; reserve for future commercial-ship deal, not pitch).

**Star-lord verifies** the chosen provider's API key is present + functional before committing to the generation pass. If provider X fails health-check, fall back to provider Y without re-asking Matt.

### § 4.2 — Locked prompt prefix template (gandalf-authored; star-lord interpolates)

**Register lock per `canonical/story/style-register.md` (Matt-locked 2026-05-15): Hand-drawn pixel-art in HD-2D register.** This is the Octopath Traveler / Triangle Strategy / Live A Live HD-2D Remake / Sea of Stars / Eastward family — pixel-resolution character sprites rendered with hand-drawn-illustration sensibility, painterly atmospheric lighting, depth-of-field environmental backdrop. **NOT** Diablo-IV / DoE grimdark painterly (which is the mobile-UX-feel target — a separate register decision; do not conflate).

```
HD-2D hand-drawn pixel-art character portrait. Octopath Traveler / Triangle Strategy / 
Sea of Stars / Live A Live HD-2D visual register. Pixel-resolution character sprite 
with hand-drawn illustration sensibility, painterly cinematic lighting, atmospheric 
depth-of-field backdrop. {SUBSTRATE}-elemental aesthetic with {SUBSTRATE_ACCENT_COLOR} 
highlights and {SUBSTRATE_TEXTURE_HINT}. 3/4 view portrait, {ARCHETYPE_POSE_HINT}, 
isekai-genre-readable. The character {ICONIC_VERB_1} and {ICONIC_VERB_2}. Style register: 
{ICONIC_REGISTER}. {COSMOLOGY_INFLECTION_PHRASE}. 
HD-2D illustrated pixel-art quality, single character centered, no text, no UI elements.

Negative: photorealistic, Diablo grimdark painterly, dark concept art, retro 16-bit 
pixel, modern anime line-art, cel-shaded, oversaturated, AAA realism, vector art, 
multiple characters, text overlay
```

**Provider choice may also shift slightly for HD-2D register.** Re-rank for this register:
- **Midjourney v8** — best general fantasy quality but HD-2D pixel-art handling variable; works with explicit Octopath/Triangle Strategy style references in prompt
- **GPT Image 2** — strong prompt-following; can hit HD-2D reliably with style anchoring
- **Imagen 4** — competitive on stylized pixel-art; worth A/B testing
- **SDXL with HD-2D community LoRA (via Replicate)** — potentially the BEST register-consistency answer if a viable LoRA exists; this needs Legolas follow-up before star-lord locks provider. Community LoRAs trained on Octopath/Triangle/Sea-of-Stars-style art do exist; quality varies.

**Star-lord's first pre-flight task:** run a 3-image sample per provider for ONE selected hero (gandalf's Hero of the Engine), with the HD-2D prompt template. Surface the samples to gandalf for register-coherence selection. Provider locks AFTER that sample comparison. ~$0.50 cost.

**Interpolation map** (per-substrate; gandalf provides these constants):

| Substrate | accent_color | texture_hint | iconic_register | (sample) cosmology_inflection_phrase |
|---|---|---|---|---|
| fire | ember-orange and deep red | charred edges, glowing seams | martial | "the substrate of escalation; what begins small and becomes total" |
| water | deep cyan and pale blue | wet sheen, ice-edge condensation | mystic | "the substrate of pervading presence; state-change by immersion" |
| earth | loam-brown and burnt amber | weathered stone, root tangle | martial | "the substrate of unyielding; what does not move and will not be moved" |
| wind | pale slate and silver-white | kinetic streak, drifting particulate | mystic | "the substrate of motion; kinetic rearrangement" |
| lightning | discharge-yellow and electric white | arc-burn marks, jagged refraction | scientific | "the substrate of sudden traversal; interruption" |
| holy | clerical amber and warm gold | radiant motes, soft glow halo | clerical | "the substrate of revelation; amplification-of-aligned" |
| shadow | quiet purple and deep grey | withdrawal-blur, dim creep | shadow | "the substrate of withdrawal; occlusion" |
| physical | gunmetal grey and bone-white | scarred leather, weight-bearing stance | martial | "the substrate of contact; what cannot be argued with" |

The `ARCHETYPE_POSE_HINT` is gandalf-authored per selected hero in the curation deliverable (§ 2.2). Per-class iconic_verbs come from substrate identity declarations.

### § 4.3 — Per-image generation budget

| Image type | Count | Provider | Cost-per (est) | Subtotal |
|---|---|---|---|---|
| Hero of the Engine | 1 (with 2-3 reroll variants) | MJ v8 or GPT-2 | $0.04 | $0.16 max |
| Hero of the Season (× 5 seasons) | 5 (with 1-2 reroll each) | MJ v8 or GPT-2 | $0.04 | $0.60 max |
| Supporting heroes per season hype piece (~5 per × 5 seasons) | ~25 | MJ v8 or GPT-2 | $0.04 | $1.00 max |
| Variant / reroll budget | up to 100 images cumulative | -- | -- | $4.00 max |
| **Total** | **≤120 images** | -- | -- | **≤$15** |

**Hard ceiling:** $15. If a generation pass approaches the ceiling, star-lord halts and reports.

### § 4.4 — Image-gen pipeline error handling

- API call timeout or rate-limit → exponential backoff retry (3 attempts) → log + skip + flag in cost-ledger
- Generated image fails sanity check (uniform color; obvious artifact) → re-roll once; if second attempt also fails, log + skip
- Provider unavailable mid-run → fall back to secondary provider without Matt re-authorization (within ceiling)
- Cost ceiling reached → halt; preserve all generated assets; surface in hive log; queue resumption for Matt L3

---

## § 5 — Matt L3 surfaces (pre-authorization required BEFORE sprint fires)

These three decisions must land before star-lord begins the vendor-spend portion. Pre-authorize all three, OR star-lord stages the dispatch and waits.

| # | Decision | Recommendation | Matt approves? |
|---|---|---|---|
| L3-1 | **Vendor spend ceiling: up to $15 for image-gen API** | APPROVE | ☐ |
| L3-2 | **Provider choice: MJ v8 if API access confirmed; else GPT Image 2** | APPROVE star-lord to pick at his judgment within the two | ☐ |
| L3-3 | **Deployment: Vercel preview-URL only (production-URL deferred for separate Matt L3 after preview review)** | APPROVE preview-only; defer prod | ☐ |

**Pre-authorization HARD NOs (unchanged from project conventions):**
- No production-URL Vercel deploy without separate explicit L3
- No CLAUDE.md / AGENTS.md modifications
- No load-bearing canonical-doc amendments
- No git push --force on any branch
- No external-publishing of the deployed page (the preview URL stays internal-only until Matt L3)

---

## § 6 — Pitch page structure

### § 6.1 — Top-hero curation rubric (gandalf's curation pass)

**"Hero of the Engine" criteria** (cross-season selection):

1. **Cohesiveness** (1–5) — substrate identity, archetype, iconic_verbs, cosmological vocab inflection, and role all sing in the same register. A fire_mage in a fire-themed season with `ignites/burns/scorches` iconic verbs and a `flicker`-flavored cosmology slot scores 5.
2. **Uniqueness** (1–5) — not a class shape we've seen repeatedly across seasons; an emergent archetype, an unusual substrate × role combination, or a class whose generated name and flavor reads as one-of-one. An `experimental` class is a likely 5; a fifth fire_mage is a 2.
3. **Flavor density** (1–5) — the per-class generated names, descriptions, and the season's cosmological vocab around it form a multi-clause, evocative read. A class whose name + season vocab triggers an immediate mental image scores 5.
4. **Visual generatability** (1–5) — would the locked prompt template produce a portrait that *carries* the hero's identity? Some classes (specific geometries, distinct iconic verbs) generate cleanly; others (generic warriors) generate generically. This is the gating axis.

Aggregate: simple sum (max 20). Top score wins; ties broken by uniqueness then by gandalf judgment.

**"Hero of the Season" criteria** (per-season anchor selection): same rubric, applied within-season; top-scoring class per season becomes the lineup center for that season's hype piece.

**Gandalf's curation output** lives at `agentic_orchestration/gandalf/findings/2026-05-18-pitch-top-hero-curation.md` with:
- Per-season rubric scoring (table)
- Selected Hero of the Engine (1) — full justification + bespoke prompt
- Selected Hero per Season (5) — name + bespoke prompt each
- Recommended supporting-hero lineup per season (3-5 classes) — for the hype-piece composite

### § 6.2 — `/pitch` page sections (drax implementation)

**§ 6.2.1 — Headline + Hero of the Engine (above-the-fold)**

- Large headline: *"Reincarnated — an LLM-authored seasonal ARPG"* (or gandalf-revised wording at impl time)
- Hero of the Engine portrait, large, centered (mobile) / right-third (desktop)
- Adjacent prose card: hero's class name + season + substrate + 2-3 sentences from gandalf describing why this hero exemplifies the engine
- Substrate-accent rule line per § 3.2 of the analytics-IA doc

**§ 6.2.2 — The Engine in One Paragraph**

- Single prose paragraph framing the project: *"Eight Claude agents. A canonical-7 substrate set. An LLM that authors a new world every season — substrate vocabulary, cosmological slot-fills, hero names, monster mythos. Mobile-feel target: Dungeon of Exile-class. Solo dev, hand-crafted engine, AI-augmented production."* (gandalf revises at impl time)
- Three small stat cards beneath: Seasons (n) · Heroes (n) · Substrates (7)

**§ 6.2.3 — Season Hype Pieces (one per season; scrolling carousel on mobile, grid on desktop)**

- For each of the 5 canonical-7 seasons:
  - Composite image (centered hero of season + 4-5 supporting heroes in lineup pose; client-side composited from individually-generated images per § 2.1 architecture)
  - Season name + anchor + theme element + a 1-2 line cosmological flavor blurb from the season's vocab
  - Below-image: 3-5 cosmological slot-fill chips ("Seam Pressure" / "Damp Creep" / "Forge Remembrance" / "Withdrawal Soot") — direct LLM-thematic-universe evidence
  - "See classes" cross-link into the loadout's existing season-detail surfaces if they exist; else into `/analytics`

**§ 6.2.4 — The Hive (one paragraph; production-credibility frame)**

- Single paragraph: *"Reincarnated is built by an agentic engineering team — eight Claude agents with scoped seams, structured dispatches, gated reviews, and a hive-mind operating protocol. The team has shipped a stable engine, six canonical seasons, a mobile-playable demo, and this analytics surface. The agentic workflow is a production methodology, not a content authorship shortcut: the design, balance, and creative direction are hand-crafted; the LLM accelerates production within those rails."* (gandalf revises at impl time; this exact framing matters per § C of gandalf's framing memo — Larian-style backlash mitigation)
- Optional small "team manifest" component (8 single-line role descriptions) — reuse from `/the-work` if it exists; else hand-author

**§ 6.2.5 — Paths and Conversations (the ask surface)**

- Three short cards naming the open conversations: (a) Engine-as-tool licensing for live-service studios; (b) Mobile-first indie ship with publisher partnership; (c) Platform-deal exploration (Apple Arcade / Netflix Games)
- A clean "contact" line: Matt's email (mhwetmore@gmail.com) + a one-line acknowledgment that this is a private preview surface, not a public marketing page

**§ 6.2.6 — Footer**

- Existing footer (game-icons.net CC BY 3.0 credit)
- Add: *"Hero portraits generated by [PROVIDER] from engine-authored substrate identity + per-season LLM cosmology. Art direction: human-curated. No AI-generated text in shipped product surfaces."* (transparency disclosure; safer to over-disclose than under-disclose per § C of framing memo)

### § 6.3 — Visual register

Inherit ALL register guidance from `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` § 3 (gray-950 palette, substrate-accent colors, mono labels + sans narrative, density rhythm, mobile-first floors). The pitch page is in the same visual family as the analytics suite; they share the loadout app's house style.

The single addition: **the Hero of the Engine spotlight breaks the dense-rhythm rule** — it's a *visual moment*. Big portrait, generous whitespace, single-substrate-accent atmosphere. Don't crowd it.

---

## § 7 — Critical-path sequencing

```
Matt L3 (§ 5) ─┬─→ star-lord pipeline scaffold ─→ gandalf curation pass ─→ image-gen run ─┐
               │                                                                            │
               ├─→ drax /pitch scaffold (placeholders) ───────────────────────────────────┤
               │                                                                            ├─→ assembly ─→ push ─→ Vercel preview ─→ galadriel capture ─→ Matt
               ├─→ elrond validation pass ────────────────────────────────────────────────┤
               │                                                                            │
               └─→ star-lord seasons.json bundle ────────────────────────────────────────┘
```

**Wall-clock estimate** (parallel): ~3-5 hours total active work if Matt L3 lands at sprint open.
- Matt L3: ~5 minutes
- Star-lord pipeline scaffold + bundles: ~45-60 min
- Gandalf curation: ~30-45 min
- Image-gen run: ~10-20 min (API latency + retries)
- Drax UI scaffold: ~90-120 min
- Elrond validation: ~30 min
- Assembly + push: ~30 min
- Vercel preview live: ~5-10 min
- Galadriel capture: ~30 min

If parallelized cleanly, ~3-4h wall-clock.

---

## § 8 — Halt conditions

- Matt L3 surfaces on § 5 do not land → dispatch stages dispatch-ready; pipeline does not fire
- Vendor spend ceiling ($15) breached → halt; preserve assets; surface in hive log
- Image-gen provider returns uniformly broken or off-register output → halt; surface to gandalf for rubric review; do not ship broken images to preview URL
- Vercel preview deploy fails → roll back; queue for morning
- Cross-seam contract drift (drax can't consume star-lord's bundle shape) → 1-hour reconciliation window; if unresolved, halt

---

## § 9 — Ship criteria

The sprint is "done" when:

- [ ] Matt L3 (§ 5) landed
- [ ] Image-gen script functional in engine repo; cost ledger present
- [ ] Hero of the Engine portrait generated + curated (gandalf reviewed)
- [ ] 5 Hero of the Season portraits generated
- [ ] Supporting-hero portraits per season generated (~5 × 5 = 25)
- [ ] Season hype pieces composited client-side per drax
- [ ] `/pitch` page live on Vercel preview URL
- [ ] Elrond validation pass filed
- [ ] Galadriel multi-viewport capture filed + shareable single-image artifact produced
- [ ] Hive log STATE entry per § 14.1.1 PRE-SIGNAL
- [ ] Matt has the preview URL + the shareable image for the afternoon meeting

---

## § 10 — Risk register

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| 1 | MJ v8 API access not actually available at Matt's tier | MEDIUM | Pre-flight check; fall back to GPT Image 2 without re-asking Matt |
| 2 | Image-gen output doesn't land on visual register | MEDIUM | Re-roll within budget; if persistent, escalate to gandalf for prompt revision; do not ship off-register |
| 3 | Curation produces no clear standout (all seasons score similarly) | LOW | gandalf judgment-call breaks tie; document reasoning |
| 4 | Loadout app architecture conflicts with new route | LOW | drax has shipped many routes; pattern is proven |
| 5 | Vercel preview build fails | LOW | loadout has stable build history; build logs surface root cause |
| 6 | Generated image gets cited externally as AI-art before pitch lands | MEDIUM | Preview URL is internal-only per § 5 L3-3; do not share externally pre-Matt-approval |
| 7 | $15 ceiling proves too low | LOW | Halt cleanly; surface to Matt; L3 on ceiling increase |
| 8 | Star-lord session not opened in time for afternoon meeting | MEDIUM | This dispatch is dispatch-ready; if star-lord can't fire today, the pipeline runs tonight for tomorrow's follow-up; Matt can pitch from existing analytics + verbal description today |

---

## § 11 — Cross-references

- `canonical/story/style-register.md` — **load-bearing canonical lock for art register; HD-2D hand-drawn pixel-art** (Octopath / Triangle Strategy / Sea of Stars family); DO NOT conflate with mobile-UX-feel target
- `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` — visual register inheritance + § 3 substrate accent palette (loadout-app interior register; different decision from art register)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate identity source-of-truth for prompt interpolation
- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — **mobile UX feel-target only** (HUD density, atmosphere, vertical reading flow); explicitly NOT the art register
- `agentic_orchestration/legolas/research/2026-05-18-marketing-director-pitch-context-and-paths-to-market.md` — research-pass informing § C of gandalf framing memo + the AI-positioning disclosure language in § 6.2.6
- `output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json` — pitch's literary gold; quoted on `/pitch` page
- `output/standard-demo-regen-2026-05-17/season_*/classes/*.json` — per-class data for curation pass
- This document — gandalf framing memo to Matt for the afternoon Marketing Director meeting (separate from but adjacent to this sprint)

---

## § 12 — Closing

The afternoon Marketing Director conversation can happen *with the pitch page in the room*. Matt opens the laptop; the URL loads; the Hero of the Engine looks out from an HD-2D hand-drawn-pixel-art portrait — Octopath-Traveler-class composition — that the engine itself authored end-to-end. The cosmological pair-rationale prose sits beneath, beautifully typeset. The Hero of the Season hype pieces scroll past — five distinct seasons, each visually one-of-one, all built by one developer with eight agent-collaborators in a few months.

The Director sees what Reincarnated *is*, not what it *describes*. The conversation becomes "where does this slot into the market" instead of "what is this thing."

That is the pitch. The hive ships it.

---

*Authored 2026-05-18 afternoon by gandalf, per Matt directive. Pattern-A orchestration sprint; star-lord-coordinated; image-gen LLM-integrated; Vercel-preview-deployed. Mithrandir signs.*
