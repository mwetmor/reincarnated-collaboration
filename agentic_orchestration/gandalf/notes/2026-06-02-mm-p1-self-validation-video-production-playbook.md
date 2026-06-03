# MM-P1 Self-Validation — Video (Stage A→B) + Meshy Gear Manifest (Stage D L50 reveal)

**STATUS:** CURRENT (production playbook; Matt-executable artifact)
**Date:** 2026-06-02
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-02 verbatim: "So it is actually a video just for me right now, but I will likely show people. I want to first validate my own concept" + "we can keep it to 8 seconds by choosing only one character if needed" + "Duskweaver of the Eclipsed Meridian is the new name of the top candidate" + "3rd step being level 50 decked out" + "i'll do it myself in meshy if you pass my alll of the gear and details of the gear and llm gear names"
**Goal:** validate Matt's chernoff-celestial-body concept via (a) an 8-second AI-generated video covering Stage A constellation emergence → Stage B materialization, AND (b) a Meshy-built L50 decked-out reveal still appended as the third transformation. TOP-1 character: "Duskweaver of the Eclipsed Meridian" (kit_shadow_000007).

---

## 0. TL;DR — what Matt does

1. **Generate reference portrait** — Midjourney or FLUX prompt in § 3; 1-3 generations; pick best (~$2-5, ~15 min)
2. **Generate Veo 3.1 video (Stage A→B)** — prompt in § 4 + reference portrait as image-input; 1-3 takes (~$20-60, ~30 min)
3. **Build L50 decked-out Duskweaver as 3D model in Meshy** — composite character prompt + gear manifest in § 4.5; Matt-handled (~$15-30 Meshy credits, ~1-2 hours)
4. **Assemble final piece** — Veo 8s video → crossfade → 3D model display (rotation render, Sketchfab embed, or screencap held for ~3s); Matt-handled in any video editor (~15 min)
5. **Evaluate against acceptance criteria** in § 5
6. **Decide:** validated / iterate / pivot per § 7

**Total budget:** $40-95, ~3-4 hours of Matt time (Veo video may be a single sitting; Meshy work may be a separate sitting).

---

## 1. Why 8s on Stage A→B specifically

The 8-second window must validate the SINGULAR NOVEL HYPOTHESIS of the chernoff-celestial-body concept:

> Can a 2D constellation outline of a humanoid form, layered with 3D depth and resolving into a tattered-clothing character, deliver the emergent-identity reveal that the chernoff-substrate vision promises?

Stages C (customization) and D (L50 decked-out reveal) are conventional ARPG presentation territory. They do not need video validation; they need standard art-direction work. Stage A→B is the chernoff-architecture-specific moment that nothing else in ARPG genre prior art validates for us.

**Why not Stage A alone:** Stage A constellation by itself is half the test. Matt needs to see whether the materialization payoff carries the constellation setup. Stage A→B together is the full hypothesis.

**Why not Stage A→D condensed:** 8s across four stages = 2s/stage. Insufficient breath; no stage validates. Better to test 2 stages at 4s each at full visual density.

---

## 2. Service selection — Google Veo 3.1

| Criterion | Veo 3.1 | Runway Gen-4.5 | Verdict |
|---|---|---|---|
| 8s native cap | YES (perfect fit) | NO (multi-shot stitching) | Veo |
| Visual ceiling at 8s | HIGHEST per Legolas synthesis | Lower at stylized-VFX | Veo |
| Integrated audio | YES (chernoff-emergence ambience free) | Separate layer | Veo |
| Cost per take | $20-40 | $45-95 multi-shot | Veo |
| Re-roll budget | 2-3 takes within $60-120 | 1-2 takes within $90-190 | Veo |
| Image-input support (reference portrait) | YES | YES | Tie |
| Stylized-VFX coherence | Strong | Mid | Veo |

**Selection:** Google Veo 3.1.

**Fallback:** if Veo 3.1 is unavailable or produces poor results on first 2 takes, pivot to Runway Gen-4.5 with same prompt structure (Veo→Runway prompts translate cleanly).

---

## 3. Stage 1 — Reference portrait generation

**Purpose:** anchor Veo 3.1 with a strong character-identity image so the materialization beat resolves into THIS specific Duskweaver, not a generic shadow-mage.

**Tool:** Midjourney v6+ OR FLUX.1 Pro.

**Prompt (paste verbatim, adjust style tokens to taste):**

```
A solitary figure standing in shallow profile, three-quarter view, against a deep
indigo-to-black void background. The character is "Duskweaver of the Eclipsed
Meridian" — a shadow-aligned caster of fallen station. Wearing tattered ceremonial
robes in muted dark-violet and ash-grey, edges frayed as if from long passage. Hood
half-raised, face partially shadowed but visible — gaunt, intent, neither young nor
old. One hand extended at waist height, palm down, drawing dim threads of dusk-light
that curl around the fingertips. The other hand resting at the side.

Composition: centered, isolated figure, full body visible, head-to-feet framing with
some void above and below. Cinematic lighting: rim-light only, deep-violet key with
faint cool-cyan fill at the trailing edge. Painterly digital-illustration style;
hand-painted texture; concept-art register. Color palette: indigo, charcoal, muted
violet, deep teal, faint silver star-points scattered in the background void.

NO bright glow. NO obvious magic VFX. NO weapons. NO armor pieces — only ceremonial
fabric. NO text. NO logos. The mood is solemn, liminal, the moment before something
emerges.

--ar 9:16 --style raw --stylize 250
```

**Iteration discipline:** generate 4-grid; pick best 1; refine via `--cref` or vary-strong if close-but-not-quite. Budget: 1-3 generations.

**Acceptance for reference portrait:**
- Reads as A character, not a class illustration
- Tattered period-clothing register lands
- Mood is solemn / liminal (not heroic, not menacing)
- Color palette stays muted (the dusk-light threads should be the ONLY warm element if any)

---

## 4. Stage 2 — Veo 3.1 video generation

**Prompt (paste verbatim into Veo 3.1 with reference portrait as image-input):**

```
An 8-second cinematic shot. Black void background throughout. Stylized digital
concept-art register, hand-painted texture, painterly.

BEAT 1 (0-2s): Absolute black void. Individual silver-violet stars appear one by
one across the frame, slow and deliberate, pulsing softly. By 2s, roughly 30-40
stars scattered in a humanoid distribution — the silhouette of a standing figure
visible only as the spatial arrangement of star-points.

BEAT 2 (2-4s): Thin luminous lines connect the stars in sequence, drawing the
constellation outline of a humanoid form — head, shoulders, torso, arms at sides,
legs apart in shallow stance. The lines glow faint cool-cyan, the stars remain
silver-violet. By 4s, the full 2D constellation-outline of the figure is complete
against the void.

BEAT 3 (4-6s): The 2D constellation gains depth. The flat outline rotates very
slightly — perhaps 5 degrees — revealing volumetric form. Dim translucent indigo
mass begins to fill the interior of the outline, like a figure resolving from deep
water. The stars at the vertices remain bright; the connecting lines fade slightly
as the volume takes over.

BEAT 4 (6-8s): Materialization. The volumetric form crystallizes into the figure
from the reference image — Duskweaver of the Eclipsed Meridian, in tattered dark-
violet and ash-grey ceremonial robes, hood half-raised, one hand extended palm-down
drawing dim threads of dusk-light. The stars at the vertices fade to faint
afterglow points behind/around the figure, marking the constellation that birthed
them. Final pose holds for the last ~0.5s.

Camera: locked, no movement. Composition: figure centered, full body in frame.
Color palette: indigo, charcoal, muted violet, deep teal, silver star-points,
faint cool-cyan constellation lines. NO warm colors except the faint dusk-light
threads at the hand in Beat 4. NO bright magical glow. NO weapon flash. NO text
or overlays.

Audio: low ambient drone, single soft chime at Beat 2 line-connection, a longer
sustained tone rising slightly through Beat 3, and a soft resonant impact at Beat 4
materialization. No music. No voice.

Mood throughout: solemn, cosmic, the resumption of a station long vacant.
```

**Iteration discipline:** 1 take first; evaluate against § 5; if any criterion fails, re-prompt with targeted adjustment per § 6. Budget: 2-3 takes maximum within this session.

---

## 4.5 Stage 3 — Meshy 3D Gear Manifest (L50 Decked-Out Reveal; Matt-handled)

**Purpose:** the third transformation. The 8s Veo video carries Stage A→B (constellation → tattered materialization). Stage 3 carries the journey's terminus — L50 Duskweaver in restored station, the chernoff substrate's emergent identity fully ascended. Delivered as a 3D model in Meshy by Matt.

**Two paths** — Matt chooses based on Meshy fluency + iteration appetite:
- **Path 1 — Composite character prompt:** single Meshy text-to-3D-character prompt that produces the full L50 figure with all gear. Faster; less control.
- **Path 2 — Piece-by-piece:** generate each gear item individually + a base character; assemble in Meshy or external 3D tool. Slower; full control + iteration per piece.

### Path 1 — Composite character Meshy prompt (paste verbatim into Meshy character mode)

```
Duskweaver of the Eclipsed Meridian — a humanoid sovereign-restored figure, L50
ascended form. Three-quarter view, standing pose, weight settled, both hands at
chest height drawing braided cords of cool-cyan dusk-light that arc between them.

GARMENTS: ceremonial mantle of restored station — dark-violet silk layered over
charcoal underrobes, edged in silver constellation embroidery; long flowing cloak
in deepest indigo with hem fading into scattered silver star-points; fingerless
dark-leather forearm gauntlets laced with silver cord and wrapped in faint cool-
cyan dusk-light braids around the knuckles; wide woven sash in dark-violet and
silver knotted with seven small silver star-points dangling at the front; deep-
charcoal underrobe leg-wraps with silver vertical constellation embroidery; matte-
black low-cut soft-leather slippers edged in thin silver.

ACCOUTREMENTS: a slim silver-and-black-iron circlet at the brow set with three
small star-points; a slim silver scepter ~24 inches held in the off-hand, capped
at one end with a starburst of silver points and at the other with an obsidian
sphere; a floating polished obsidian orb ~4 inches diameter suspended above the
opposite open palm, bearing a single visible silver crescent of frozen mid-eclipse
on its surface, ringed by faint cool-cyan corona; a small obsidian-and-silver
pendant at the throat; a slim silver band on the left index finger; a heavier
silver-and-black-iron signet on the right hand.

FACE/HEAD: composed expression, neither triumphant nor solemn; gaunt mid-aged
features; hood lowered fully revealing the circlet; dark hair shoulder-length
pulled back; eyes faintly luminous cool-cyan.

STYLE: stylized fantasy ARPG hero character; painterly digital concept-art
register; hand-painted texture in surface materials; medium-poly clean topology
suitable for game use; color palette indigo, charcoal, muted violet, deep teal,
silver, faint cool-cyan accents; no warm colors except the dusk-light cords;
PBR materials.
```

### Path 2 — Piece-by-piece gear manifest (13 items; each LLM-named per refined discipline)

Each entry: SLOT — LLM name | visual description | Meshy text-to-3D prompt (single-object, Matt pastes verbatim).

#### 1. HEAD — "Circlet of the Twiceborn Meridian"

Slim silver-and-black-iron circlet, three small star-points set at brow + temples, faint cool-cyan glow at each star-point, fine constellation engraving traceable along the band.

> Meshy prompt: "A slim circlet for a humanoid head, ~7 inches diameter. Made of polished silver with thin black-iron edge inlay. Three small spiked star-points rise from the band — one at the brow center, one above each temple — each star tip glowing faint cool-cyan. Fine engraved constellation lines run along the band between the star-points. Stylized fantasy ARPG style, PBR materials, medium-poly clean topology."

#### 2. SHOULDERS/MANTLE — "Mantle of the Resumed Throne"

Layered shoulder mantle in dark-violet silk over charcoal undercloth, edged in silver constellation embroidery. Asymmetric: right shoulder bears a silver pin shaped as an eclipsed disc.

> Meshy prompt: "A ceremonial shoulder mantle for a humanoid figure. Two-layer construction: outer layer dark-violet silk with subtle sheen, inner layer matte charcoal cloth. Edged along all seams with embroidered silver thread tracing constellation patterns. Asymmetric detail — right shoulder bears a circular silver pin ~1.5 inches diameter shaped as a black-disc eclipse with a silver corona ring around it. Drapes naturally over shoulders, falling to mid-upper-arm. Stylized fantasy ARPG style, PBR materials."

#### 3. CHEST/ROBE — "Vestment of the Unbroken Eclipse"

Long ceremonial robe of layered violet silks over deep-charcoal underrobe. Chest panel bears central embroidered eclipse motif — black disc ringed with silver corona — running shoulder to waist. Slim-fitted sleeves gathered at wrist.

> Meshy prompt: "A long ceremonial robe for a humanoid figure, floor-length. Outer layer dark-violet silk with subtle sheen, inner layer deep-charcoal underrobe visible at neckline and sleeve cuffs. Chest panel features a large embroidered motif: a black disc ringed by silver radiating corona threads, running from upper sternum down to waist sash line. Sleeves slim-fitted from shoulder to wrist, gathered at the cuff with silver cord. No belt — leaves waist exposed for the sash. Stylized fantasy ARPG style, PBR materials."

#### 4. HANDS — "Gauntlets of Woven Dusk"

Fingerless dark-leather gauntlets rising to mid-forearm, laced with silver cord. Faint braided cords of cool-cyan dusk-light wrap around the knuckles continuously.

> Meshy prompt: "A pair of fingerless leather gauntlets covering the forearm from wrist to mid-forearm, in matte dark-brown leather with black-iron rivets at the cuff. Laced up the inner forearm with silver cord. Across the back of the hand and knuckles, faint translucent braided cords of glowing cool-cyan light wrap and weave continuously — the dusk-light is part of the gauntlet's effect. Fingertips uncovered. Stylized fantasy ARPG style, PBR materials with emissive cool-cyan accents."

#### 5. BELT/SASH — "Cordage of Star-Reckoning"

Wide woven sash in dark-violet and silver, knotted with seven small silver star-points dangling on fine cord at the front — one per canonical primary, marking station within celestial reckoning.

> Meshy prompt: "A wide woven sash worn around the waist of a humanoid figure, ~5 inches tall, made of interleaved dark-violet and silver fabric strands. Tied at the front with a hanging tail. From the tail, seven small silver star-points dangle on fine silver cord at staggered lengths, each star ~0.4 inches tip-to-tip, gently swaying. Stylized fantasy ARPG style, PBR materials."

#### 6. LEGS/UNDERROBE — "Greavewrap of the Hollow Court"

Underrobe leg-wraps in deep-charcoal cloth, bound at the calves with silver cord. Subtle silver vertical constellation embroidery along the outer leg.

> Meshy prompt: "A pair of leg-wraps for a humanoid figure covering thigh to ankle, in deep-charcoal matte cloth with no sheen. Bound at the calves with crossed silver cord lacing. Subtle vertical silver embroidery runs along the outer side of each leg, tracing a thin constellation pattern from hip to ankle. Drapes loosely; not skin-tight. Stylized fantasy ARPG style, PBR materials."

#### 7. FEET — "Slippers of Silent Passage"

Low-cut soft-leather slippers in matte-black with thin silver edging. Designed for silent walking; sole barely contacts ground.

> Meshy prompt: "A pair of low-cut soft-leather slippers in matte-black, ankle-height, no laces, slipped on. Edged at the top opening with thin silver piping. Thin flexible sole. Stylized fantasy ARPG style, PBR materials."

#### 8. WEAPON-PRIMARY (focus orb) — "The Sealed Apogee"

A floating polished orb, ~4 inches diameter, dark obsidian with a single visible silver crescent on its surface — frozen mid-eclipse. Suspended above the open palm without touching it; faint cool-cyan corona surrounds it.

> Meshy prompt: "A single floating spherical focus orb, ~4 inches diameter, surface of polished black obsidian with high reflectivity. One side of the orb bears a single curved silver crescent inlay — frozen at the moment of mid-eclipse — wrapping ~120 degrees of the orb's circumference. Around the entire orb, a faint translucent cool-cyan corona glow extends outward ~1 inch. The orb is suspended in space alone with no support, presented as a standalone floating object. Stylized fantasy ARPG style, PBR materials with emissive cool-cyan corona."

#### 9. WEAPON-SECONDARY (scepter) — "Scepter of the Restored Meridian"

Slim silver-and-black-iron scepter ~24" long, capped at one end with a small starburst of silver points and at the other with a smooth obsidian sphere.

> Meshy prompt: "A slim ceremonial scepter ~24 inches long, shaft of alternating silver and black-iron banding in a clean repeating pattern. One end terminates in a small radiating starburst of seven silver spike-points, each ~1 inch long. The opposite end terminates in a smooth polished obsidian sphere ~1.5 inches diameter. The shaft is thin enough to grip in one hand. Stylized fantasy ARPG style, PBR materials."

#### 10. CLOAK — "Cloak of Constellate Memory"

Long flowing cloak in deepest indigo, hem fading into scattered silver star-points that drift with motion. Inner lining matte-black; outer constellation pattern redraws subtly.

> Meshy prompt: "A long flowing cloak for a humanoid figure, floor-length, falling from the shoulders. Outer surface deepest indigo with a subtle silver constellation pattern embroidered in fine line-work. Inner lining matte-black. The lower hem fades from solid fabric into scattered small silver star-point embellishments, sparser as the hem progresses downward — appearing to dissolve into stars. Fastened at the throat with a small silver clasp. Stylized fantasy ARPG style, PBR materials."

#### 11. AMULET — "Pendant of the First Eclipse"

Small obsidian disc the size of a coin, set in silver, hanging on a fine silver chain at the throat. Bears one engraved line — the first eclipse marked.

> Meshy prompt: "A pendant for a humanoid neck. The pendant body is a small flat circular disc ~0.8 inches diameter made of polished black obsidian, set within a thin silver ring frame with two small loops at the top. The obsidian face bears a single engraved straight line crossing the disc horizontally. Hangs from a fine silver chain ~18 inches long. Stylized fantasy ARPG style, PBR materials."

#### 12. RING-1 — "Band of the Twiceborn Hour"

Slim silver band on the left index finger, engraved with a single wrapping line — the moment of resumption marked in metal.

> Meshy prompt: "A slim silver ring for a humanoid finger, ~0.2 inches band width, polished silver finish. Engraved with one single thin line that wraps all the way around the band's outer surface, slightly offset from center. No gemstone. Stylized fantasy ARPG style, PBR materials."

#### 13. RING-2 — "Signet of the Resumed Station"

Heavier silver-and-black-iron signet on the right hand, faceted with a small eclipse motif on the seal face — usable for sealing documents of restored station.

> Meshy prompt: "A signet ring for a humanoid finger. Heavier construction than a band ring — ~0.5 inches band width. Made of polished silver with black-iron inlay edging the band. Flat oval seal face ~0.7 inches across, engraved in raised relief with an eclipse motif: a small central black-iron disc surrounded by radiating silver corona points. Stylized fantasy ARPG style, PBR materials."

### Set-coherence notes

- **Color palette:** indigo, charcoal, muted violet, deep teal, silver, faint cool-cyan. NO warm colors. NO gold. NO red. NO bright magical glow except the cool-cyan dusk-light at hands.
- **Material register:** silk (drape garments), leather (gauntlets/slippers), polished obsidian (orb/pendant/signet face), silver (metalwork), black-iron (accent metalwork). PBR consistent across all items.
- **Iconographic motifs that recur:** the eclipse (mantle pin, orb surface, signet seal), the constellation pattern (mantle embroidery, leg embroidery, cloak outer surface, circlet engraving), the star-point (circlet, sash dangling stars, scepter starburst, cloak hem dissolution).
- **No weapons of force.** Duskweaver's L50 kit shows authority through ceremonial regalia and a focus-orb + scepter pairing, not through swords or staves of obvious combat function. The character's power is COMPOSITIONAL — read in the integration of items, not in any single weapon.

### Display / assembly

After Meshy build, Matt has Stage-3 options:
- **Static still render:** render the 3D model from the same three-quarter view used in the Stage-B Veo materialization, append as a still hold (~3-4s) after the video
- **Slow rotation render:** 4-6 second slow turntable, append after the video with a brief crossfade
- **Sketchfab/interactive embed:** for showing peers later (per "I will likely show people"), interactive 3D viewer is the strongest self-validation surface
- **Recommended for first-pass validation:** static still render at three-quarter view — minimizes Matt-handled video assembly work; gives clean A/B comparison to the Stage B tattered figure

---

## 5. Acceptance criteria for self-validation

Matt evaluates the video against these specific questions. The video VALIDATES the chernoff-celestial-body concept if MOST land "yes":

| # | Question | Validates |
|---|---|---|
| 1 | Does the 2D constellation read as a humanoid silhouette at the end of Beat 1, before lines connect? | Chernoff-as-distribution-of-features hypothesis |
| 2 | Do the connecting lines in Beat 2 land as "constellation" (mythic, named-pattern) rather than as "wireframe" (technical, CAD)? | Mythic-register of the substrate visualization |
| 3 | Does the 3D emergence in Beat 3 feel like materialization (depth coming THROUGH the form) rather than inflation (form being filled)? | The substrate-to-body transition narrative |
| 4 | Does the Beat 4 figure feel like THE character birthed by THIS constellation, or like a generic figure dropped in? | Identity-anchoring of the chernoff substrate |
| 5 | Does the 8s composition hold attention, or does it feel rushed / overlong / boring? | Whether the concept earns the screen time it asks for |
| 6 | Would Matt show this to a peer designer and feel proud of the concept it represents? | Self-validation gut-check |
| 7 | Does the Stage-3 L50 3D model feel like THE SAME CHARACTER as the Stage B figure, ascended — rather than a different character entirely? | Continuity of emergent identity across the journey |
| 8 | Does the gear set's compositional integration (eclipse + constellation + star-point recurrence) read as a SET rather than as collected items? | Set-coherence as design language |
| 9 | Does the full Veo-video → L50-model sequence land as a three-beat journey (substrate → tattered → restored) without feeling disjoint at the video→model crossfade? | Whether the concept supports the full arc, not just the opener |

**Validation thresholds (9 questions):**
- 7-9 yes → STRONG VALIDATION; proceed to MM-P2 scope (UE-seam-agent architecture for in-engine version)
- 4-6 yes → PARTIAL VALIDATION; identify which beat or stage fails and re-shoot/re-render that piece
- 0-3 yes → CONCEPT REVISION; chernoff-celestial-body needs design rework before further investment

---

## 6. Iteration adjustments (if first take misses)

| If failure mode is... | Adjust prompt by... |
|---|---|
| Constellation doesn't read as humanoid | Specify star-count + key joint locations more precisely; add "head: 1 star at top, shoulders: 2 stars, hands: 2 stars, feet: 2 stars, ribcage: ~10 stars" specificity |
| Lines feel technical/wireframe | Add "glowing as if drawn by hand"; "imperfect, slightly tremulous lines"; reduce line brightness |
| Beat 3 feels like inflation | Add "form emerges from depth as if rising through indigo water"; "stars remain dimensionally OUTSIDE the volume that fills" |
| Beat 4 figure doesn't match reference | Strengthen image-input weight; add "EXACTLY the figure in the reference image"; reduce prompt-influence weight |
| Pacing feels rushed | Compress Beat 1 to 1.5s, extend Beat 4 to 1s materialization + 1.5s hold |
| Too much VFX flash | Add "minimal magical glow"; "the magic is in the COMPOSITION, not in lighting effects"; "restrained, painterly" |
| Wrong mood | Adjust audio prompt + add explicit mood adjectives ("contemplative" / "reverent" / "elegiac" depending on direction) |

---

## 7. Post-video disposition

**If STRONG VALIDATION:**
- Matt may share with peers (per "I will likely show people" framing)
- Triggers MM-P2 scope: UE-seam-agent role definition + Architecture γ in-engine implementation planning per Legolas constellation-form-UE-techniques synthesis (~14-22 UE-seam-agent sessions, ~$95-175 above-baseline FAB cost)
- Composes with drax cycle-18 fix-forward completion (Duskweaver rename feeds /loadout featured-picks rendering)
- Strategic confirmation: chernoff-celestial-body becomes the locked Stage A→B architecture for Realm Expansion content rhythm

**If PARTIAL VALIDATION:**
- Identify which specific beat or criterion fails
- Author targeted design-revision note OR commission Legolas Mode A research on the specific failure mode
- Re-shoot ONCE with prompt adjustments; if still partial, escalate to design call

**If CONCEPT REVISION:**
- The chernoff-celestial-body concept needs design rework BEFORE further engine investment
- gandalf authors recognition record + commission Pattern B design call with Matt to explore alternative Stage A architectures
- MM-P2 scope deferred until revised concept passes self-validation

---

## 8. Operational sequence for Matt

```
STEP 1 — Reference portrait (15-30 min, $2-5)
  - Open Midjourney or FLUX.1 Pro
  - Paste § 3 prompt
  - Generate 4-grid; upscale best; if needed, vary-strong to refine
  - Download best generation as PNG/JPG

STEP 2 — Veo 3.1 video generation, Stage A→B (30-60 min, $20-60)
  - Open Veo 3.1 (Google AI Studio or Vertex AI)
  - Upload reference portrait as image-input
  - Paste § 4 prompt
  - Generate; review against § 5 criteria Q1-Q6
  - If iteration needed, apply § 6 adjustment; re-generate (max 3 takes)

STEP 3 — Meshy 3D model of L50 Duskweaver, Stage 3 (~1-2 hours, $15-30)
  - Open Meshy (text-to-3D)
  - Choose path: composite character (Path 1) OR piece-by-piece (Path 2)
  - Path 1: paste § 4.5 composite character prompt; generate; iterate gear visibility
  - Path 2: generate base character figure; then 13 gear items per § 4.5 manifest;
    assemble in Meshy or external 3D tool
  - Render output: static three-quarter view still OR slow rotation OR Sketchfab embed
  - Review against § 5 criteria Q7-Q8

STEP 4 — Final assembly (~15 min)
  - Open any video editor (Quicktime, DaVinci Resolve free, iMovie)
  - Sequence: Veo 8s video → ~0.5s crossfade → Stage-3 model render (~3-4s static
    still OR 4-6s rotation)
  - Optional: faint sustained tone under Stage-3 hold
  - Export final piece

STEP 5 — Self-validation evaluation (15 min)
  - Watch final piece 3 times
  - Score § 5 criteria Q1-Q9
  - Determine disposition per § 7

STEP 6 — Disposition execution
  - If validated: ping knight-rider to open MM-P2 scope dispatch
  - If partial: ping gandalf to investigate specific failure (Stage A-B vs Stage 3)
  - If revision: ping gandalf to open Pattern B concept design call
```

---

## 9. Sign-off

**Authored:** gandalf 2026-06-02 per Matt MM-P1 path-A ratification + 8-second window confirmation + Duskweaver rename + Stage-3 Meshy-3D-model addition
**TOP-1 character:** "Duskweaver of the Eclipsed Meridian" (kit_shadow_000007)
**Services:** Midjourney/FLUX (reference portrait) + Google Veo 3.1 (Stage A→B video) + Meshy (Stage 3 L50 3D model, Matt-handled)
**Coverage:** Stage A constellation emergence → Stage B tattered materialization (video) → Stage 3 L50 decked-out reveal (3D model)
**Budget:** $40-95, ~3-4 hours of Matt time across one or two sittings
**Composes with:**
- `2026-06-02-mm-p1-top-1-rename-duskweaver.md` (character identity)
- `2026-06-02-qdx-5-top-5-character-curation.md` (TOP-1 source)
- `legolas/research/2026-06-02-ai-video-generation-mm-p1-fast-path/synthesis.md` (Veo service comparison source)
- `legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md` (MM-P2 architecture target if validated)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (Realm Expansion content rhythm that chernoff-celestial-body Stage A→B→3 serves)

**End of production playbook.**
