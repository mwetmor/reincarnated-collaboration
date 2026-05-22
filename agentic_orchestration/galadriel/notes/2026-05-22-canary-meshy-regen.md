# Canary of the Drowned Seam — Meshy-Compat Regeneration

**Date:** 2026-05-22
**Steward:** galadriel (visual-perception sub-agent run, bounded)
**Commissioned by:** Matt, via gandalf-routed request
**Output:** `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_meshy_test/canary-meshy-ready-2026-05-22.png`
**Cost:** $0.04 (single gpt-image-1 call, logged in cost-ledger as `note: "canary-meshy-regen-2026-05-22"`)
**Script:** `/Users/admin/Games/reincarnated-engine/scripts/pitch/canary_meshy_regen.py` (Meshy-compat one-shot; inherits API-key and ledger conventions from `canary_reroll.py`)
**Reference spec source:** `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/pipeline-integration-notes.md` §§ Stage 1 + Stage 2

---

## 1. What was generated

Full-body front-facing T-pose stylized fantasy character of Canary of the Drowned Seam, redrawn for clean Meshy 3D-model intake. Plain white background, single character, symmetric outfit, anatomically correct hands, no shoulder canary, no flooded-mine backdrop.

## 2. Prompt used (verbatim)

```
Full-body character reference sheet for 3D model conversion. Stylized fantasy
character art, cel-shaded, clean line work, flat ambient studio lighting, no
dramatic chiaroscuro, no atmospheric effects. Plain pure white background,
completely empty, no scenery, no shadows on ground, no smoke, no embers, no
atmospheric glow.

A young human fire-mage, slim build, late teens, short tousled red-brown hair,
soft determined face, fair complexion with faint soot smudges on the cheekbones.
She stands in a clean symmetric T-pose, facing the camera straight on, feet
shoulder-width apart pointing forward, legs straight, both arms held out
horizontally to the sides at shoulder height, elbows straight, palms facing
forward, fingers separated and clearly visible. No crossed limbs, no hidden
limbs, no foreshortening.

She wears a soot-stained dark brown miner's robe of medium length, ending just
above the knee, cinched with a simple leather belt at the waist. The robe has
canary-yellow trim at the collar, at both sleeve cuffs, and at the hem —
symmetric on both sides. Beneath the robe she wears dark charcoal-grey leggings
or trousers, and sturdy dark leather boots that rise to mid-calf with a thin
canary-yellow band at the top of each boot. The outfit is fully symmetric
left-to-right: matching sleeves, matching boot bands, matching belt pouches on
either hip.

Above her right open palm a small, simple flame shape floats — flat, stylized,
ember-orange, no smoke, no glow halo, just a clean flame icon sitting an inch
above her hand. The left palm is empty and open.

Color palette: soot-stained dark brown robe, canary-yellow trim, ember-orange
flame, dark charcoal leggings, warm fair skin tone, red-brown hair. High
contrast between the character and the pure white background — sharp edge
silhouette, no soft fade to background, no rim-light bleed.

Single character only. No companion creature. No bird. No text. No UI
elements. No props besides the small flame above her right palm. No weapon.
No shoulder accessories. No cape. No hood (head bare and clearly visible).
Full body visible from head to feet, centered in frame, with even margin all
around.

Anatomically correct: five fingers per hand, fingers separated and clearly
individuated, natural hand proportions, both hands fully visible with palms
forward, two arms, two legs, two feet, one head, symmetric body.

Do not render: photorealistic style, painterly Octopath HD-2D pixel-art, dark
moody chiaroscuro, atmospheric depth-of-field, flooded mine scenery, coal seam
glow, ember smoke, fog, hooded face, raised arm, crossed arms, hidden hands,
sitting pose, action pose, dynamic pose, 3/4 view, side view, back view,
multiple characters, perched bird, shoulder companion, extra fingers, missing
fingers, three fingers, four fingers, six fingers, fused fingers, malformed
hands, anatomically incorrect hands, text overlay, UI borders, frame border.
```

## 3. Meshy-compat departures from the canonical Canary

Each departure is justified by a specific legolas-cited Meshy failure mode.

| Departure | Canonical | Meshy-compat | Justification (legolas pipeline-integration-notes §) |
|---|---|---|---|
| Render style | HD-2D Octopath painterly chiaroscuro | Cel-shaded stylized fantasy, flat ambient lighting | Stage 2 § Known failure modes: "Low-contrast or poorly-lit reference image → surface reconstruction artifacts." The canonical Canary's dark moody backdrop with rim-light face is exactly the low-contrast pattern that produces those artifacts. |
| Background | Flooded coal mine + smoldering seams + ember atmosphere | Pure white empty studio | Stage 1 § Mitigation: "plain white background" recommended. Stage 1 § Known failure modes: "Complex backgrounds included in 3D mesh → background geometry corrupts model." |
| Composition | 3/4 view chest-up portrait, raised hand | Full-body front-facing T-pose | Stage 3 § Critical constraints: "Character must be in T-pose or A-pose with feet pointing forward" — Mixamo hard requirement. Stage 1 § Critical constraints: "Character limbs must be visible and separated (T-pose preferred)." |
| Shoulder canary | Yellow canary perched on shoulder | REMOVED | Stage 2 § Critical constraints: humanoid auto-rig assumes single head/torso/arm/leg structure. A perched bird reads to the rigger as a secondary body and produces fused-mesh/bone-placement artifacts. The canary semantics remain in the character's *name* and could be re-introduced at the Unity-VFX stage (Stage 4) as an attached companion sprite with its own root. |
| Flame | Cupped in raised hand, glowing into the face | Small flat flame icon floating above outstretched open palm | T-pose forbids the raised-arm signature pose. The flame is preserved as a small flat shape (minimal volumetric content) above the open palm. *Note:* model swapped sides — flame landed above **left** palm in the output, not right as prompted. Not load-bearing for Meshy (symmetric body, one palm flamed / one empty either way), but flagged for transparency. |
| Outfit asymmetry | Robe + accents drift L/R in canonical | Strictly symmetric: matching sleeve cuffs, matching boot bands, matching hip pouches | Stage 2 § Known failure modes: "Asymmetric character design → poor bone placement in rigging step." |
| Hood | Hooded in some prior iterations | Bare head, hair visible | Stage 3 § Known failure modes: "Missing body part definition (hidden elbows in costume) → incorrect bone placement." The same principle applies to a hood concealing head/neck topology. |

## 4. Visual observations on the output (Mirror, descriptive)

- Pose: clean T-pose. Arms horizontal at shoulder height. Palms facing forward. Fingers separated and individuated. Feet pointing forward, shoulder-width. No crossed limbs. No hidden limbs. **Rig-clean.**
- Background: pure white, no shadow cast, no fade-bleed. **Silhouette extraction-ready.**
- Anatomy: five fingers each hand, both hands fully visible, two arms, two legs, one head. **No flags.**
- Symmetry: collar trim, sleeve cuffs, boot bands, hip pouches all symmetric L/R. Belt centered. **Rig-friendly.**
- Outfit: soot-stained brown robe, canary-yellow trim at collar/cuffs/hem/boot-tops, brown leggings, mid-calf boots. **Identity-preserving outfit semantics.**
- Hair, face, build: short tousled red-brown hair, soft determined face with faint soot smudge readable on cheekbones, slim late-teens build. **Reads as the same character as the canonical Canary.**
- Flame: small flat ember-orange flame icon floats above the **left** palm (prompt drift; not load-bearing). Right palm empty and open.
- Style register: cel-shaded clean-line stylized fantasy. Not the canonical HD-2D Octopath painterly register.

## 5. Concerns / surfaces for Matt to weigh

1. **Style-register departure is real.** The canonical Canary's brand register was *painterly HD-2D + chiaroscuro + atmospheric depth-of-field*. The Meshy-compat regen is *cel-shaded flat-lit stylized fantasy*. These are different visual languages. Confidence read: **the character identity (outfit, palette, face, build) survives the shift cleanly, but the "Reincarnated brand feel" is partially carried by the canonical register itself.** If the Meshy pipeline is being evaluated for the entire character roster, the team should decide whether the brand can be re-established at the post-Meshy stage (lighting, post-process, VFX) or whether the brand requires the painterly register at the source.

2. **Shoulder canary lost.** The character's *name* still does the semantic work — the canary is in the title regardless. But the *visual* canary-on-shoulder was a recognizable composition element in the canonical. If Matt wants the canary preserved in the 3D character, the workflow option is to attach it at the Unity stage as a separate companion sprite/mesh with its own root (Stage 4), not as part of the rigged humanoid.

3. **Flame-side prompt drift.** Model put the flame above the left palm, not the right. Not a Meshy problem (symmetric body either way), but worth knowing if Matt has downstream specs that assume right-hand flame attachment for VFX bone-parenting (Stage 4 § VFX attachment convention: cast effects typically attach to RightHand).

4. **Dynamic-pose vs rig-compat tradeoff.** The canonical Canary's signature pose (raised hand cupping flame, lit face from below) is *expressive* — it conveys the character's role and the substrate-of-escalation theme. The T-pose conveys *none of that*; it is functional reference, not character storytelling. Recommendation: **Matt should evaluate whether the 3D-rigged character, once posed/animated downstream of Meshy+Mixamo, recovers the storytelling that the T-pose strips out.** If Mixamo's animation library can produce a "cast small flame from cupped hand" pose, the loss is recoverable. If not, the Meshy pipeline may need a per-character "hero pose" variant captured separately from the rig-source variant.

## 6. Style-register confidence read

Does the regen still feel like Reincarnated, or did Meshy-compat compromise the visual brand?

**Partial.** The character identity (outfit, palette, face, build) survives — somebody looking at the canonical Canary and this regen would identify them as the same character. The *brand register* (painterly atmospheric HD-2D) does not survive — this is a cleaner, flatter, more generic stylized-fantasy register. That is the cost of Meshy-compat as the spec is written.

The finding that emerges is useful regardless of how Matt judges the tradeoff:

> **The Reincarnated brand is carried more by outfit-semantics + palette than by render-style.** A flatter render still reads as "the same character" when the outfit and palette are tight. That suggests the Meshy pipeline can preserve roster identity across the line — provided the source-art briefs lock outfit + palette per character before the prompt is run.

If Matt tests this through Meshy and the 3D character (post-rig, post-animation, post-VFX, post-Unity-lighting) recovers the brand atmosphere through downstream stages, the Meshy pipeline is viable. If it does not, the test will surface a load-bearing constraint: **the source-art register itself has to carry brand**, and the Meshy specs (T-pose + plain white + cel-shaded) are too brand-erasing to use as-is.

That is the question this regen exists to answer. The picture is ready. Bring back what Meshy makes of it.

---

*Galadriel — Mirror voice, brief. The character is the same person. The register is not. Whether that matters is the test.*

---

## 7. V2 regeneration — empirical test of shoulder-canary preservation (2026-05-22, post-Meshy-run)

**Trigger:** Matt ran the v1 output (`canary-meshy-ready-2026-05-22.png`) through Meshy. The `.glb` was rig-clean but reads as "Ember Apprentice" — the canary identity was lost because the canary was not in the source image. Matt flagged that my v1 precaution (legolas: "second body geometry would fail auto-rig") was *theoretical, not empirically tested*. A small static perched accessory may register differently than a posed second body. This v2 runs that experiment.

**Output:** `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_meshy_test/canary-meshy-with-canary-2026-05-22.png`
**Cost:** $0.04 (entry #65, `note: "canary-meshy-regen-v2-with-canary-2026-05-22"`, `class_slug: "canary-of-the-drowned-seam"`, `season_id: "meshy-test"`)
**Ledger total now:** $2.56
**Script:** `/Users/admin/Games/reincarnated-engine/scripts/pitch/canary_meshy_regen_v2.py` (template-inherited from v1; minimal modification to add canary clause + adjust negative-prompt block to forbid flight/extended-wing/second-subject framings while preserving anti-second-character language on the *human* axis only).

### 7.1 V2 prompt (verbatim)

```
Full-body character reference sheet for 3D model conversion. Stylized fantasy
character art, cel-shaded, clean line work, flat ambient studio lighting, no
dramatic chiaroscuro, no atmospheric effects. Plain pure white background,
completely empty, no scenery, no shadows on ground, no smoke, no embers, no
atmospheric glow.

A young human fire-mage, slim build, late teens, short tousled red-brown hair,
soft determined face, fair complexion with faint soot smudges on the cheekbones.
She stands in a clean symmetric T-pose, facing the camera straight on, feet
shoulder-width apart pointing forward, legs straight, both arms held out
horizontally to the sides at shoulder height, elbows straight, palms facing
forward, fingers separated and clearly visible. No crossed limbs, no hidden
limbs, no foreshortening.

She wears a soot-stained dark brown miner's robe of medium length, ending just
above the knee, cinched with a simple leather belt at the waist. The robe has
canary-yellow trim at the collar, at both sleeve cuffs, and at the hem —
symmetric on both sides. Beneath the robe she wears dark charcoal-grey leggings
or trousers, and sturdy dark leather boots that rise to mid-calf with a thin
canary-yellow band at the top of each boot. The outfit is fully symmetric
left-to-right: matching sleeves, matching boot bands, matching belt pouches on
either hip.

Above her right open palm a small, simple flame shape floats — flat, stylized,
ember-orange, no smoke, no glow halo, just a clean flame icon sitting an inch
above her hand. The left palm is empty and open.

On her LEFT shoulder, a small bright canary-yellow songbird sits perched as a
static accessory. The bird is small — about the size of a fist, roughly five
to eight percent of the character's silhouette volume — with simple rounded
geometry: small round body, wings folded tight against its sides (NOT extended,
NOT spread, NOT in flight pose), short tail, small head with a tiny dark beak
and a single visible dark eye, head facing forward or tilted very slightly to
one side. Its small feet grip the shoulder seam of the miner's robe naturally,
as if perched on a branch. The bird is sitting still — alert but motionless.
Its bright canary-yellow plumage contrasts cleanly against the dark soot-stained
robe shoulder beneath it. The bird is drawn as part of the character's
silhouette, attached to the shoulder, not a separate posed creature in its own
composition.

Color palette: soot-stained dark brown robe, canary-yellow trim, ember-orange
flame, dark charcoal leggings, warm fair skin tone, red-brown hair, bright
canary-yellow shoulder bird. High contrast between the character and the pure
white background — sharp edge silhouette, no soft fade to background, no
rim-light bleed.

Single dominant character body. The shoulder canary is a small static perched
accessory, not a second character. No text. No UI elements. No props besides
the small flame above the right palm and the perched shoulder canary. No
weapon. No cape. No hood (head bare and clearly visible). Full body visible
from head to feet, centered in frame, with even margin all around.

Anatomically correct: five fingers per hand, fingers separated and clearly
individuated, natural hand proportions, both hands fully visible with palms
forward, two arms, two legs, two feet, one head, symmetric human body.

Do not render: photorealistic style, painterly Octopath HD-2D pixel-art, dark
moody chiaroscuro, atmospheric depth-of-field, flooded mine scenery, coal seam
glow, ember smoke, fog, hooded face, raised arm, crossed arms, hidden hands,
sitting pose, action pose, dynamic pose, 3/4 view, side view, back view,
multiple human characters, large bird, flying bird, bird in flight, extended
wings, spread wings, bird as separate composition subject, second posed
creature, extra fingers, missing fingers, three fingers, four fingers, six
fingers, fused fingers, malformed hands, anatomically incorrect hands, text
overlay, UI borders, frame border.
```

### 7.2 Rationale for testing the canary-included variant

Three reasons the test is worth $0.04:

1. **The precaution was inherited as theoretical claim, not verified.** Legolas's pipeline-integration-notes Stage 2 § Known failure modes asserts that humanoid auto-riggers fail on multi-body geometry. That is *true for posed second characters*. It may *not* be true for small static accessory geometry that is visually attached to the humanoid silhouette. The distinction is testable for $0.04 + one Meshy run.
2. **The Ember Apprentice slip is the live cost.** Meshy + Mixamo produced a clean rig from v1, but the Meshy preview interpretation drifted to "ember apprentice" rather than "canary of the drowned seam" because there is no visual canary. The character *name* alone is not load-bearing in the pipeline once the human-readable model preview is generated. The visual canary needs to either (a) ride along through Meshy, or (b) attach at Unity. We need to know which.
3. **The result is a binary pipeline-design decision.** If the canary survives Meshy cleanly: roster source-art briefs can include small perched companions and the pipeline carries them. If the canary fails (gets fused, lost, or breaks the rig): pipeline-design pattern becomes "companion creatures are Unity-side parented sprites via Animation Rigging, never source-art geometry." Either outcome is actionable.

### 7.3 Mirror-voice observations on the V2 output (descriptive, what the picture shows)

**Pose and anatomy (rig-readiness):**
- Clean symmetric T-pose. Arms horizontal at shoulder height. Palms forward. Fingers separated. Feet shoulder-width, pointing forward. **Rig-clean, same as v1.**
- Five fingers per hand visible. Both hands fully extended. No crossed or hidden limbs. **No flags.**
- Symmetry of human body preserved: matching sleeves, matching boot bands, belt centered.

**Background:**
- Pure white, no shadow cast, no atmospheric haze. **Silhouette-extraction-ready.**

**Outfit and identity:**
- Soot-stained dark-brown miner's robe with canary-yellow trim at collar, sleeve cuffs, hem, boot tops. **Matches v1 outfit semantics exactly.**
- Hair, face, build: short tousled red-brown hair, slim late-teens build, soft determined face. **Reads as the same character as v1 — identity preserved.**

**Flame:**
- Small ember-orange flame floats above the **right** palm (character-right, screen-left, since character faces camera). **Note: this is opposite from v1, where the model placed the flame above the screen-right palm.** Both runs put the flame on one open palm with no smoke/halo; the side-laterality drift is a known gpt-image-1 behavior at this prompt-strictness level. Not load-bearing for Meshy.

**Shoulder canary (the test variable):**
- A small, bright canary-yellow songbird sits perched on the character's **left** shoulder (character-left, screen-right). Wings folded tight against the body. Small rounded body, short tail, small head with dark beak and visible dark eye. Head facing forward / very slight tilt. Feet appear to grip the shoulder seam. **The bird reads as a static perched accessory, not as a posed second creature.**
- Silhouette volume: visually estimated at ~6-7% of the character silhouette (consistent with the 5-8% spec). The bird does not exceed the head's silhouette area.
- Attachment quality: the bird's feet appear to touch the shoulder; there is no visible gap; the bird does not float. The shoulder line of the robe is visible behind/beneath the bird, so the bird is *on* the shoulder rather than fused into the shoulder.
- Contrast: bright canary-yellow against the dark soot-stained robe shoulder — high contrast, clean edge silhouette. The bird is visually separable from the human body by edge alone.
- Style register: the bird is cel-shaded in the same flat-ambient register as the rest of the character. Stylistically integrated.

**Overall composition:**
- Single dominant human body. The canary does not compete for compositional weight — it reads as accessory, not as second subject. The frame remains a character reference sheet for a *single* humanoid with a small perched companion. **Compositionally intended.**

### 7.4 Flagged concerns for the Meshy run

1. **Bird silhouette protrudes above the shoulder line.** The bird's head and upper body extend roughly half a head-height above the character's shoulder. From Meshy's perspective, this means the topmost extent of the silhouette is *not* the character's head — it is the bird's head (or close to it). If Meshy's bounding-box logic uses the silhouette extremes to allocate skeleton attention, the bird sits in a region the auto-rigger may treat as "head extension" or "shoulder ornament." Either treatment is plausible; we won't know until it runs.

2. **Bird color overlaps trim color.** The bird is bright canary-yellow; the robe trim is canary-yellow. If Meshy's segmentation step uses color clustering, the bird may get region-merged with the trim despite being spatially detached. The dark soot robe between bird and trim should help, but it is not guaranteed.

3. **Bird-shoulder contact zone has visible feet but limited overlap.** This is a design tradeoff. A bird whose body is *embedded* into the shoulder mesh would read as fused (good for surviving auto-rig, bad for sprite-readability). A bird whose body is *floating above* the shoulder reads cleanly but might fail mesh-connectivity tests. The v2 output sits in the middle: bird-feet on shoulder, bird-body sitting just above shoulder line, no embedded fusion. **This is the right middle ground for testing, but it's the middle ground — which means either failure mode could occur.**

4. **The shoulder line behind the bird is visible.** This is a positive — it means the bird is not fused into the shoulder geometry in the 2D image. But it also means Meshy's surface reconstruction has to decide: is the bird a separate floating object (likely lost in single-mesh extraction) or is it an attached protrusion (likely included)? Meshy's documented behavior on attached accessories is mixed.

5. **Flame-side laterality flipped from v1.** V1 placed the flame above the character-left palm; v2 placed it above the character-right palm. Same source model, same prompt-construction approach, opposite outcomes. Confirms the side-laterality clause is below the model's compliance threshold at this prompt-strictness level. Not Meshy-load-bearing, but worth flagging for any downstream spec that assumes a particular hand for VFX bone-parenting (Stage 4 § VFX attachment convention).

### 7.5 Mirror prediction — will Meshy preserve the canary?

**Galadriel's prediction: 35-50% chance the canary survives cleanly as attached geometry on the rigged humanoid.**

Reasoning:
- **Arguments for preservation (~50%):** The canary sits inside the character silhouette; it has clean contact with the shoulder; it does not have an extended-pose footprint. Meshy is documented to handle "small attached accessories" reasonably (e.g., shoulder pauldrons, belt pouches, hood ornaments). A small perched bird with folded wings is geometrically similar to a shoulder pauldron with a bird-shaped sculpt.
- **Arguments against (~50%):** Meshy's auto-rig expects bilaterally symmetric humanoid topology; the canary is unambiguously asymmetric and protrudes above the shoulder bone target. Even if Meshy *reconstructs* the mesh including the canary, Mixamo's auto-rig may decline to weight a protruding asymmetric mass to the shoulder bone — which would result in either rigging failure, a static unweighted accessory (acceptable!), or a deformed shoulder during animation.
- **Specific failure modes I would not be surprised to see:**
  1. Canary survives as a static disconnected mesh chunk (Meshy reconstructs it but it floats relative to the bone hierarchy — visually fine in T-pose, breaks the moment the character moves). **Probability: ~25%.**
  2. Canary fuses into the shoulder as a deformed ornamental lump (color-merged or geometry-merged). **Probability: ~20%.**
  3. Canary is dropped entirely as not-humanoid (segmentation step excludes it). **Probability: ~15%.**
  4. Canary survives cleanly and rigs cleanly to the shoulder bone with reasonable deformation. **Probability: ~25-35%.**
  5. Auto-rig fails outright because the bilateral-symmetry check rejects the topology. **Probability: ~10-15%.**

**The probability mass is on partial-success outcomes.** Even the "best" likely outcome (clean rig with canary surviving) is uncertain enough that I would NOT recommend committing the pipeline design to "source-art companion creatures" on the strength of this single test. **One sample is not a pipeline policy.** If v2 succeeds, the next test should be 2-3 more characters with shoulder/wrist/staff-perched companions to confirm reproducibility before locking the pattern in.

### 7.6 Decision-tree disposition (galadriel domain only — gandalf/drax own the design-language reading)

| Meshy outcome on V2 | Galadriel recommendation |
|---|---|
| Clean rig, canary preserved, animates without deformation | Pipeline pattern: *source-art companions allowed* (with 2-3 reproducibility tests before locking). Roster brief template gets a "companion accessory" optional clause. |
| Canary preserved as static unweighted mesh chunk | Pipeline pattern: *source-art companions allowed in T-pose model, expect to re-parent at Unity*. Acceptable if Unity Animation Rigging cost is low. |
| Canary fused / deformed into shoulder | Pipeline pattern: *companions are Unity-side only*. Legolas's original precaution upheld for production purposes; the v1 "remove the canary" choice was correct in retrospect. |
| Canary lost entirely | Same as fused/deformed: *companions are Unity-side only*. |
| Auto-rig rejects topology | Strongest signal: *do not put companions in source art for the rigging path*. Companion sprites attach Unity-side as parented separate roots with their own animation. |

### 7.7 Mirror voice — closing

The first picture was the character with the bird subtracted. The second picture is the character with the bird returned. The Mirror does not yet know which picture the pipeline will keep. We have built two stones; the river will keep one or both or neither, and we will see by morning which the current preserves.

The picture is ready. Bring back what Meshy makes of it — and if the canary survives, we have a pattern. If it does not, we have a pattern still. The experiment teaches either way.

*Galadriel — visual perception, v2 closed. $0.08 cumulative on Meshy-compat testing. No sub-spawn. One API call as authorized.*

---

## § 8. V2 EMPIRICAL OUTCOME — addendum (gandalf, 2026-05-22 evening, post-Matt-Meshy-test)

**Outcome notation: surface-survival ≠ usability.** Matt ran the v2 image through Meshy and reported back. The result corrects the celebratory framing the v2 test surface suggested.

### 8.1 What Meshy actually produced

Mesh-reconstruction step: the canary **was preserved** as part of the character mesh. So at the "geometry survives" question, my decision-tree row (§ 7.6 row 1 "Clean rig, canary preserved, animates without deformation") predicted geometry would survive, and it did.

But at the deeper question — *animates without deformation* — the actual outcome is closer to § 7.6 row 2 ("Canary preserved as static unweighted mesh chunk") with a sharper consequence than that row anticipated: **the canary is fused to the arm, not the shoulder.** Because Meshy auto-rig attached the canary to the nearest moving body part (the half-raised arm in the T-pose), animating the character drags the canary around the canvas on a swinging arm, glued to the mesh.

**Result: the character is unusable for animation in this configuration.** Surface geometry was preserved (looked-positive on still-frame inspection); animation behavior is broken (cannot independently animate; rigid-fused to wrong bone).

### 8.2 The actual canonical lesson — refined

The earlier framing "small static accessories survive Meshy cleanly" was a partial truth that masked the load-bearing constraint. The corrected categorization principle (now canonical for Reincarnated character-image pipeline):

| Accessory category | Pattern | Examples |
|---|---|---|
| **Rigidly-attached static** — moves WITH the body part by design | OK in source; baked into mesh; correct behavior | Medallion / emblem; sash; fixed pouch; armor pieces; carried tool that doesn't have independent life; attached holster |
| **Independent-life dynamic** — needs its own movement/behavior separate from the body | **Must be Unity-layer**; never in source | Companion creatures (canary, familiar, spirit-pet); element-derived VFX (flames, lightning, holy glow); flowing cloth (cape, banner); detachable items; spirit-guide manifestations |

The decision criterion is: **"when the character animates, does this thing have its own intended movement OR should it stay rigidly attached?"**

For the canary: it should have its own life (flutter, head turn, fly off the shoulder during combat, return). Conceptually it's never "rigidly attached." Therefore source-art baking is wrong category placement. Unity-layer with separate-root parented to shoulder bone via Animation Rigging is the canonical pattern.

### 8.3 Calibration lesson — for future predictions

My 35-50% prediction in § 7.5 was framed around *surface geometric preservation* of the canary. That framing was incomplete. Future predictions on Meshy-pipeline-output should explicitly distinguish:

1. **Geometric preservation** — does the desired feature appear in the output mesh?
2. **Rig correctness** — is the feature attached to the right bone with the right weights?
3. **Animation usability** — does the feature behave correctly when the character animates?

These are three distinct levels of pipeline success, not a single binary outcome. The v2 test hit level 1 cleanly and failed level 3 catastrophically. Future commission frames should structure prediction around all three levels.

### 8.4 Retrospective on the v1 "remove the canary" decision (§ 7.4)

Re-evaluating: the v1 precaution to remove the canary was **correct for production purposes** (matches § 7.6 row 5: "do not put companions in source art for the rigging path"). Legolas's original second-body warning was directionally right; my v1 precaution was directionally right; Matt's v2 test surfaced the architectural constraint with empirical clarity.

The pattern going forward — **companions are Unity-layer, period** — is now canonical for Reincarnated.

### 8.5 Canonical Meshy-compat source image for the Canary spirit-form (going forward)

- T-pose body of fire-mage
- Soot-stained miner robes with canary-yellow trim, symmetric
- **No canary in source** — Unity-layer companion via Animation Rigging; the canary becomes a separate-root GameObject parented to the shoulder bone with its own mesh, rig, and animation track (flutter, head-turn, fly-off-during-combat all become possible)
- **No flame in source** — Unity VFX layer per separate canonical rule on element-derived effects
- Plain white background

### 8.6 Pattern propagation — for spirits with companions or VFX-bearing elements

Every spirit in the Reincarnated form library that has either a companion creature OR an element-derived visual effect (essentially every fire/water/lightning/holy/shadow spirit) follows this pattern:
- Source image: body + outfit + rigid accessories only
- Unity layer: companions + VFX + flowing-cloth + spirit-guide manifestations

This generalizes to a Reincarnated-wide pipeline rule that the canonical asset-pipeline-meshy-swap doc will encode in tomorrow's authoring session.

*Gandalf — appending the v2 empirical correction with Matt's authority, 2026-05-22 evening. The Mirror sees more clearly after the experiment is run than before.*
