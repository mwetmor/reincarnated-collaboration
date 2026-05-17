# Embodiment-Narrative Display — Loadout-Side Spec

**Status:** Canonical-story design spec. Authored 2026-05-16 (Day 4 close) by gandalf at Matt's authorization. Locks the visual structure, naming surface, narrative-beat conventions, and engine emission requirements for the VS2b loadout-side embodiment-narrative display. Scoped to loadout-first; demo-side surface is post-VS2b (VS2c+).

**Why this spec exists.** Form-bias Stage 1 shipped today (embodiment-axis additive field on `PlayerClass`). The engine can now describe non-humanoid embodiment in schema. Display surface to make that reality visible to the player does NOT yet exist anywhere. Per P6 forward audit § VS2b embodiment-display (CRITICAL severity) and gandalf council response (Q4 today): loadout-first, narrative-beat-first, demo follows.

**The load-bearing argument.** Per Q3 of today's council answers, chierit roster ships humanoid character archetypes. Reincarnated's structural realignment commits to non-humanoid embodiment as a player-visible reality. **Text can describe non-humanoid embodiment BEFORE sprite differentiation exists.** The story does the work first; the body follows later. This spec defines the surface that lets non-humanoid embodiment be a real player experience in VS2b without waiting for non-humanoid sprite commissioning (a separate post-VS2b legolas sweep).

**Strategic frame.** This is the moment of meeting between player and incarnated form. Diablo III's class-select screen is the canonical reference — portrait + voice line + one paragraph — but Reincarnated extends it: the form is not a *choice* the player makes, it's a *fate* the Wheel turned (per `cosmology-reincarnated.md`). The narrative beat describes what the player IS this season, not what they picked.

**What this spec is NOT.**
- Not the demo-side in-fight embodiment surface (post-VS2b)
- Not a Spirit Guide voice spec (lives at `spirit-guide-voice.md`; this surface is third-person about the embodiment, not first-person from Spirit Guide)
- Not a lore-dump surface (≤40 words; concrete; sensory)
- Not a build-recommendation surface (build coach is Stage A7)
- Not an interactive surface in VS2b (read-only; player encounters the form, doesn't customize it)

**Companion docs:**
- `canonical/story/embodiment-narrative-layer.md` — architectural framing of embodiment-as-narrative-skin (this spec operationalizes that into a visible surface)
- `canonical/story/cosmology-reincarnated.md` — Wheel / Earth Self / seasonal descent (the conceptual layer this surface surfaces)
- `canonical/story/court-of-forms.md` — Court framing + dual-label pattern C8 (spirit-name vs anchor-name)
- `canonical/story/naming-triad.md` — anchor → spirit name → embodiment-flavored name (display structure)
- `canonical/story/style-register.md` — HD-2D-shaped pixel-art register
- `canonical/story/spirit-guide-voice.md` — Spirit Guide voice (reference for tone calibration; this surface uses different voice convention)
- `canonical/16-project-roadmap.md` § VS2b — sequencing context

**Predecessor design locks honored:**
- Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) per doc 37 § 4
- Three-layer model (L1 substrate / L2 grouping / L3 vocabulary) — narrative beat consumes L3 per-season vocabulary post-Stage-3 cipher migration
- Style register HD-2D-shaped pixel-art
- Court framing dual-label pattern (spirit name vs anchor)
- chierit element-only character mapping (per Q3 council answer today)
- Embodiment-axis additive field on `PlayerClass` (Stage 1 shipped today)

---

## 1. Strategic frame — what the player experiences

When the player opens loadout and selects a class, they see **first** the form they are this season — portrait, name, a few words of who-this-is. Then the mechanical detail (skills, gear, encounters) follows below.

The narrative beat is the moment that makes embodiment-as-narrative-skin a real player experience rather than a schema field. Without this surface, embodiment is engineering theory; with it, embodiment is what the player remembers about their season.

### Genre precedent — what we are and what we are not

**Reference: Diablo III class-select screen.** Per-class large portrait + voice-line audio + one-paragraph class summary. Reads in 5 seconds; conveys identity instantly; doesn't pretend to be lore depth.

**What we add beyond D3:**
- Per-SEASON variation (the same anchor archetype embodies differently each season per the Wheel)
- Embodiment-revealing language (non-humanoid embodiment surfaces in TEXT before SPRITE)
- Per-season L3 vocabulary integration (post-Stage-3 cipher migration)

**Why this matters specifically for Reincarnated:** Diablo's class is what the player *picked*. Reincarnated's class is what the Wheel *turned* this season. The class-select-style surface still applies — but the meaning shifts. The player isn't browsing options; they're meeting the form they've already been given.

### What this surface is NOT trying to be

- **Not a class-PICKER** — class assignment is canonical (Wheel-turned); player encounters their season's roster, doesn't browse alternatives
- **Not a lore wiki** — every beat is concrete, sensory, ≤40 words. Players who want lore depth read Spirit Guide commentary or in-world ritual moments (post-VS2b surfaces)
- **Not a build planner** — separate surface (Stage A3 Spirit Guide build coach)
- **Not a Spirit Guide voice surface** — Spirit Guide speaks first-person ABOUT the player; this surface speaks third-person about the embodiment itself

### 1.1 Pixel-scale framing — ARPG-anchored, not JRPG-anchored (added 2026-05-16 Day 4 close)

This spec's portrait dimensions (96×96 desktop, 64×64 mobile) are UI-surface sizes — the cropped portrait card-cell on the loadout class-header. They are independent of the **in-game character rendered pixel-height target**, which lives in the demo-side embodiment surface (post-VS2b; see § 14).

For the in-game character rendering when it eventually ships, the **operational pixel-scale target is 100-130 px at 1080p displayed resolution** — anchored to ARPG-genre convention (Diablo IV ~110-130; Diablo III ~100-110; PoE ~100-120; Last Epoch ~100-110). This supersedes the earlier 80-100 px framing which referenced JRPG overworld conventions (Octopath overworld 80-90; Sea of Stars battle 75-90). Resolution from Legolas Section 3 ground-truth measurement 2026-05-16 Day 4 close (`agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` Section 3 + Section 4d).

**Why ARPG band, not JRPG band:**
- JRPGs have TWO cameras (overworld 80-100 px / battle 75-130 px depending on title). Reincarnated has ONE camera — the room/hallway arena topology drax shipped (`canonical/story/arena-room-hallway-system.md`) commits us to a Diablo/PoE single-camera framing where exploration and combat happen in the same view.
- ARPG single-camera convention sits at ~100-130 px to give characters enough screen-presence for positional combat readability against pack encounters.
- The HD-2D-shaped pixel-art register (`style-register.md`) is preserved at this scale — register is about visual style (chunky pixel edges, limited palette, intentional pixel-art aesthetic), not absolute pixel scale.

**Implication for demo-side embodiment-narrative surface (post-VS2b, § 14):** when authored, target chierit characters render at 100-130 px in-fight. This shifts back-derives the chierit `MONSTER_SCALE_BY_SLUG` baseline to ~1.0-1.4 (from the prior 0.45 mid-candidate that was below ARPG genre convention).

**Implication for VS2b loadout-side (this spec):** none. Portrait card-cell crops are UI surfaces sized for the loadout class-header layout; they're independent of in-game character pixel-height target. This § 1.1 is a forward-reference for the demo-side surface, not a binding constraint on this spec.

**Implication for Diablo III class-select reference (§ 1 above):** the D3 reference applies to *visual surface conventions* (portrait + voice line + one paragraph), NOT to absolute pixel scale. D3 class-select portraits are ~256×256 or larger; we use 96×96 because that's the right size for the loadout card-cell context. The reference is about WHAT the surface does, not HOW BIG the portrait is.

---

## 2. Visual anatomy

```
┌─────────────────────────────────────────────────────┐
│  ┌──────────┐                                       │
│  │          │     CINDERBORN                        │ ← spirit name (display priority 1)
│  │ PORTRAIT │     reaver                            │ ← anchor (display priority 2)
│  │ (96×96)  │                                       │
│  │          │                                       │
│  └──────────┘                                       │
│                                                     │
│  "A wandering Reaver, ember-touched. The Cinderborn │ ← narrative beat (≤40 words / 2 lines)
│  carry the Trial's first fire — quick blades and    │
│  faster grudges."                                   │
│                                                     │
│  ─────────────────────────────────────────────────  │ ← separator to existing class detail
│  [existing skill list / gear loadout / etc.]        │
└─────────────────────────────────────────────────────┘
```

### 2.1 Layout convention

- **Portrait at left, naming at right** — Diablo III pattern
- **Narrative beat below the portrait+name row** — full width of the class-header surface
- **Separator to existing class detail** below the beat — clear delineation between "who is this" (new surface) and "what do they do" (existing surface)

### 2.2 Spacing

- Portrait + name row: ~120 px tall (96 px portrait + padding)
- Beat: ~60 px tall (2 lines × 24 px + padding) at desktop; flexes for mobile
- Total surface footprint: ~200 px tall, inserts above existing class-detail content

### 2.3 Mobile responsiveness

At mobile breakpoint (≤640 px width):
- Portrait downsizes to ~64×64
- Name typography downsizes proportionally
- Beat reflows to 3 lines at narrower width (still ≤40 words; ≤200 visible characters)
- Total surface: ~160 px tall on mobile

---

## 3. Per-class portrait

### 3.1 Source

**chierit Elementals roster.** Element-coded per Q3 council answer (Fire Knight = fire-element class; Water Priestess = water-element class; etc.). Same character sprite serves all archetype variations of a given element (fire_warrior and fire_mage both render with Fire Knight portrait).

### 3.2 Crop convention

**Head + upper-body crop.** From chierit's idle-pose source sprite, crop:
- Top: ~10% above head (small headroom)
- Bottom: ~mid-torso (chest height)
- Left/right: tight to character silhouette + ~5% padding each side
- Aspect: 1:1 square (96×96 desktop; 64×64 mobile)

**Why head + upper-body, not full body:** identity recognition lives in the face/upper body. Full-body crop wastes resolution on legs/feet that don't carry character identity. D3, PoE, Last Epoch all crop class-select portraits to upper body for the same reason.

### 3.3 Animation

**Static portrait for VS2b.** The first idle-anim frame is the canonical portrait pose. No animation in the class-header surface — animation would compete with the narrative beat for attention.

Forward-compat: if a future polish pass adds subtle ambient anim (breathing, hair sway), the existing frame structure supports it. Not VS2b scope.

### 3.4 Element-coding via portrait

The portrait is the FIRST visible element-coding the player sees. Reinforced by:
- Background tint (subtle, element-themed — fire portrait gets warm-tinted bg; water gets cool; etc.)
- Border accent (thin element-colored border around portrait)

These reinforcements are LIGHT — they don't overwhelm the portrait or fight the HD-2D pixel-art register. Convention follows the loadout card-cell element-badge pattern drax shipped in v0.5.2.

### 3.5 Fallback for missing chierit coverage

Per Q3 today: chierit ships 10 element-mapped characters; Reincarnated canonical elements are 6 (physical / fire / wind / water / earth / hybrid). Mismatches:
- **physical**: no chierit character explicitly maps; use a non-elemental chierit character (TBD — knight-rider should authorize a small reconciliation dispatch per Q3 follow-up)
- **hybrid**: no chierit character explicitly maps; flex strategy needed (TBD same dispatch)
- **chierit characters with no Reincarnated element mapping** (Lightning Ronin, etc.): out of scope; not used

**Fallback for portrait absence:** if engine emits a class with element category that has no chierit mapping, surface renders a placeholder portrait (silhouette-style, element-tinted) with the narrative beat still visible. Player still gets the embodiment moment; just not the chierit-grade portrait.

---

## 4. Naming display — naming-triad architecture

Per `canonical/story/naming-triad.md` — three names per class:

| Component | Example | Display priority |
|---|---|---|
| **Spirit name** (Court of Forms cohort identity per season) | "Cinderborn" | 1 — big text, primary identity hook |
| **Anchor** (mechanical archetype) | "reaver" | 2 — smaller text, mechanical role |
| **Embodiment-flavored name** (narrative-skin descriptor) | "ember-touched Reaver" | 3 — embedded in narrative beat, not in name display directly |

### 4.1 Display structure

```
CINDERBORN     ← spirit name, all-caps or initial-cap; ~24-28 px font; primary visual weight
reaver         ← anchor, lowercase; ~14-16 px font; muted color; sits beneath spirit name
```

### 4.2 Why spirit name takes priority over anchor

The Court of Forms framing (per `court-of-forms.md` C8 dual-label pattern) commits to spirit name as the player's season-identity hook. "Cinderborn" is what the player CALLS their class this season; "reaver" is what the class IS mechanically. Player-facing surface prioritizes the season-identity (spirit name); the anchor sits below as the mechanical reference.

This honors the Court framing: the player IS a Cinderborn this season — that's their cohort, their identity, their season's voice. Next season's fire-reaver might be Hearthborn or Scorchkin or Coilworn-Wearing-Fire — the spirit name shifts per season; the anchor (reaver) does not.

### 4.3 Embodiment-flavored name lives in the beat

Don't render embodiment-flavored name as a third visible label — that crowds the header. Instead, the beat embeds it naturally:

> "A wandering ***Reaver, ember-touched***. The Cinderborn carry the Trial's first fire..."

The italicized phrase IS the embodiment-flavored name surfacing in context. Player reads it without recognizing it as a separate label.

---

## 5. The narrative beat — voice, length, content

### 5.1 Length cap

**≤40 words OR 2 lines at desktop / 3 lines at mobile, whichever is shorter.**

Why ≤40 words: any longer becomes a lore-dump. The beat is sensory, concrete, identity-revealing — not exposition. Players who want more depth find it elsewhere (Spirit Guide commentary, ritual moments, end-of-season reflection).

### 5.2 Voice convention

**Third-person, present-tense, sensory-concrete.**

| Convention | Example | Anti-pattern |
|---|---|---|
| Third-person POV | "The Cinderborn carry..." | "You are a Cinderborn carrying..." (first-person breaks the "the Wheel turned" frame) |
| Present tense | "A current that learned to walk" | "Once was a current that learned to walk" (past tense distances) |
| Sensory-concrete | "ember-touched", "quick blades", "drifting minds" | "powerful warrior class with strong attacks" (mechanical-abstract) |
| Embodiment-revealing | "drifting minds wearing borrowed bodies" | (silence on what the embodiment IS) |
| Genre-coherent | "first fire", "faster grudges" | (modernism, slang, anachronism) |

### 5.3 Exemplar beats — the bar

These exemplars establish the bar drax + LLM generation should hit. Each is ≤40 words; third-person; present-tense; sensory-concrete; embodiment-revealing.

**Fire warrior — Cinderborn Reaver:**
> *"A wandering Reaver, ember-touched. The Cinderborn carry the Trial's first fire — quick blades and faster grudges."*

**Fire mage — Hearth-Witch:**
> *"A keeper of warm flames, a remember-er of slights. The Hearth-Witches tally every kindness owed them and burn the ledger when collection comes."*

**Non-humanoid parasite embodiment — Coilworn Reaver:**
> *"This season your Court is the Coilworn — drifting minds wearing borrowed bodies. The Reaver-shape you see is the husk the Coilworn animated this turn."*

**Aquatic-elemental embodiment — Tideborn Adept:**
> *"A current that learned to walk. The Tideborn are not bodies — they are pressures the Sea shapes when it needs a will."*

**Earth non-humanoid hive embodiment — Crowned Stonebloom:**
> *"You are not a body; you are a Bloom. The Crowned Stoneblooms spread from a single root mind, each flower-form a strand of your seasonal voice."*

**Wind controller embodiment — Stormwheel Conductor:**
> *"A Conductor who tunes the air. The Stormwheel hear songs the rest of the Wheel forgot — and answer with weather."*

### 5.4 Why the Coilworn / Tideborn / Stonebloom exemplars matter

These three deliberately describe **non-humanoid embodiment** — parasite-puppet, water-pressure-shaped-will, hive-bloom — while the player sees a chierit humanoid sprite. The text does the embodiment work that the sprite cannot yet do.

**This is the strategic value of loadout-first.** The story tells the player "you are a Bloom" before the sprite has to render a Bloom. By VS2c when non-humanoid character art enters scope (post-VS2b legolas sweep), the player has already met these forms in text and is primed to accept their sprite revelation.

### 5.5 LLM generation pipeline

Beats are LLM-generated per class per season:
- **Input**: class `embodiment_tag` + element + archetype + per-season L3 vocabulary (post-Stage-3) + Court framing prompt context
- **Output**: 1-3 candidate beats; engine selects best per quality rubric; selected beat persisted to class schema
- **Cost**: small per-class call; negligible additional LLM budget per season (fits in existing per-season cost envelope)
- **Timing**: generated during season creation; cached on `PlayerClass` schema; drax loadout consumes as text field

### 5.6 Beat regeneration triggers

- New season generation (fresh beats per class per season)
- Embodiment-axis schema change (Stage 1 fields evolve)
- Player-facing per-season vocabulary change (Stage 3 cipher migration adjustments)
- Manual regen via knight-rider dispatch if specific beats land poorly in playtest

NOT triggered by: gear changes, skill allocation, level changes, in-season player choices. The beat is the SEASON's incarnation, not the moment-to-moment build.

---

## 6. Cipher-migration integration (Stage 3 dependency)

### 6.1 Pre-Stage-3 ship state

VS2b can ship embodiment-narrative-display BEFORE Stage 3 cipher migration fully closes IF beat templates use grouping-layer abstractions or per-season vocabulary substitutes rather than canonical-four labels directly.

**Pre-Stage-3 beat:** "ember-touched" (descriptive; works regardless of cipher state)
**Post-Stage-3 beat:** "ember-touched" still works AND per-season vocabulary like "scorch-skinned" or "kindling-veined" becomes available for substitution.

**Convention:** beats avoid canonical-four labels ("fire", "water", "earth", "wind", "physical") as the primary embodiment-revealing word. Use descriptive analogues:
- ✅ "ember-touched" / "scorch-skinned" / "kindling-veined" (descriptive; cipher-safe)
- ❌ "fire-attuned" / "wielder of fire" (canonical-four label; cipher-leak)
- ✅ "current-shaped" / "Sea-pressured" (descriptive)
- ❌ "water-aligned" / "water mage" (canonical-four label)

### 6.2 Post-Stage-3 ship state

Per-season L3 vocabulary fully drives beat generation. The LLM prompt receives the season's per-element vocabulary substitutes; beats are generated against those.

Each season's beats become uniquely flavored without sharing vocabulary across seasons. Season 1's Cinderborn beats might use "ember", "kindling", "scorch"; Season 2's fire-court (different spirit name) might use "magma", "ash", "smoulder".

### 6.3 Forward-compat hook for drax

Drax displays beat as plain text from the engine-emitted field. No client-side cipher logic. When Stage 3 ships, beats arrive in player-visible per-season vocabulary; drax displays without code changes.

---

## 7. Embodiment_tag surfacing — visible or invisible?

**Invisible to the player.** `embodiment_tag` is an engine-side label (e.g., `parasite_puppet`, `aquatic_elemental`, `hive_bloom`). It DRIVES beat generation but does NOT surface as a visible label.

**Why invisible:** the player meets their embodiment THROUGH the beat, not through a category tag. Showing "embodiment: parasite_puppet" alongside a poetic beat about Coilworn would break the spell. The tag is internal; the beat is the surface.

**For Spirit Guide build-coach context (Stage A7):** the tag may surface in Spirit Guide commentary ("Your Coilworn-style embodiment favors evasion") but only mediated through Spirit Guide voice, not as a bare tag.

---

## 8. Integration with existing loadout UI

### 8.1 Insertion point

**Insert above existing class-detail surface**, at the top of the per-class view. Does NOT replace existing UI; augments it.

Drax has shipped:
- Class selector (which class is active)
- Per-class skill list
- Gear loadout
- Encounter analytics view
- Card-cell components (skill cards, gear cards)

The embodiment-narrative-display becomes a **class-header surface** that sits above all of these when a class is selected. Persistent (always visible when class is selected); not dismissable.

### 8.2 Class-selector interaction

When player switches active class (within season's 5-6 class roster):
- Class-header surface refreshes (new portrait, new spirit name, new anchor, new beat)
- Brief transition (~200ms fade) — soft enough not to interrupt, present enough to telegraph the change
- Below-the-header content (skill list, gear) updates normally

### 8.3 Loadout vs class-roster view

If loadout app has a "browse classes in this season" view (TBD; drax repo state to confirm), the embodiment-narrative-display can render as a card per class — same anatomy, smaller scale. Compact form: 64×64 portrait + spirit name + anchor + first ~20 words of beat (truncated with "...").

Tap/click on card → expand to full class-header surface.

---

## 9. Mobile + accessibility

### 9.1 Mobile responsiveness

- Portrait: 96×96 desktop → 64×64 mobile
- Spirit name typography: 28 px desktop → 20 px mobile
- Anchor typography: 16 px desktop → 12 px mobile
- Beat: 24 px line height desktop → 20 px mobile; reflows to 3 lines at narrow width
- Total surface footprint: ~200 px desktop → ~160 px mobile

### 9.2 Accessibility

- **Color is not the only differentiator** — element identity carried by portrait + chierit character identity, not by background tint alone
- **Screen-reader support** — semantic markup: portrait has alt text ("Fire Knight portrait, ember-touched warrior"); name has heading hierarchy (h2 for spirit name; h3 for anchor); beat is paragraph text
- **Keyboard navigation** — tab focus order: portrait → spirit name → anchor → beat → first child of existing class-detail
- **Touch hit targets** — entire surface is informational, not interactive (no in-surface controls); n/a for hit target minimum
- **Text contrast** — meets WCAG AA minimum 4.5:1 for body text on background tint

### 9.3 Style-register alignment

HD-2D-shaped pixel-art register per `style-register.md`:
- Portrait renders pixel-art-coherent (chierit native style)
- Background tint subtle; pixel-art-coherent (no anti-aliased gradients)
- Typography: pixel-art-coherent font OR clean modern sans-serif that doesn't fight the pixel-art register. Drax owns the specific font selection; recommend testing pixel-art-coherent display font for spirit name + clean sans-serif for anchor + beat body.
- Element-themed border accents: 1-2 px solid borders; no glow/blur effects

---

## 10. What drax needs from engine emission

Confirm with rocket (Stage 1 shipped today; Stage 2 follow-on) + star-lord (Stage 2 cosmological-vocabulary; Stage 3 cipher migration) that the following fields populate reliably per class:

| Field | Source | Use |
|---|---|---|
| `embodiment_tag` | Stage 1 (shipped) | Engine-internal; drives beat generation; NOT displayed |
| `embodiment_narrative_beat` (NEW; ≤200 char string) | Stage 2 cosmological-vocabulary generation OR new dedicated narrative-beat generation call | Beat text drax displays verbatim |
| `spirit_name` (per-season) | Stage 2 cosmological-vocabulary OR Stage 3 cipher migration | Display name (big text) |
| `anchor` (mechanical archetype label) | Existing schema | Display label (smaller text beneath spirit name) |
| `element_category` | Existing schema | Background tint + border accent + chierit character mapping |
| `chierit_character_slug` | NEW; per-class lookup from `element_category` via TBD reconciliation dispatch | Portrait source selection |

### 10.1 New schema field — `embodiment_narrative_beat`

**Discipline #14 (internal-vs-generative schema separation) check**: this is a GENERATIVE schema field (player-visible; LLM-produced). Per Discipline #14, lives in the generative-side schema (where star-lord export packet ships it to consumers). NOT in the engine internal schema (which uses `embodiment_tag` and other internal labels).

**Sizing**: ≤200 visible characters (covers 2-line at desktop, 3-line at mobile with headroom).

**Generation cost**: small LLM call per class per season. ~5-6 classes per season × small call = negligible add to per-season LLM budget.

### 10.2 What does NOT need to be new

- `embodiment_tag` already shipped (Stage 1)
- `anchor` already in schema
- `element_category` already in schema
- `spirit_name` per-season exists via existing naming pipeline

**Only one new engine emission**: `embodiment_narrative_beat`.

### 10.3 Stage B export-DTO forward-compat protection (added 2026-05-16 Day 4 close)

Per finding `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md` (Pattern P7 #3 silent-drop instance): engine-side schema fields can be silently dropped at the Stage B export-DTO boundary (`ExportClass` constructor in `season_exporter.py:581-599`) before reaching the demo-facing consolidated JSON that the loadout app consumes.

**`embodiment_tag` is currently dropped at Stage B** despite being shipped on `PlayerClass` (rocket Stage 1) and wired into `_class_to_dict` (commit `4bbc906`). Empirically verified on `season_001010` (regen 22:41 today, post-all-wiring): zero `embodiment_tag` occurrences in consolidated `classes.json`.

**This blocks the entire spec end-to-end.** Loadout app reads `classes.json`; if `embodiment_tag` + `embodiment_anatomy_tags` + `embodiment_action_register` + `class_role_function` + (eventual) `embodiment_narrative_beat` don't reach `classes.json`, the embodiment-display surface has no data to render.

**Required preconditions for VS2b embodiment-display ship:**

1. **`ExportClass(...)` constructor** in `season_exporter.py` extended to pull all embodiment-axis fields (form-bias Stage 1 wiring) — already scoped in star-lord Track A dispatch per commission `2026-05-16-star-lord-export-dto-stage-b-fix-and-r11b.md`
2. **`embodiment_narrative_beat` field** added to both `PlayerClass` schema (rocket) AND `ExportClass(...)` constructor (star-lord) simultaneously — Discipline #14 (internal-vs-generative schema separation) requires the GENERATIVE-side schema be the consolidated export, not the intermediate; the field must reach `classes.json` to be useful
3. **Stage B export-boundary validator** added to enumerate required class fields — catches future-additive embodiment fields silently
4. **Spirit-name per-season pipeline** must also propagate through Stage B — if `spirit_name` lives on a different generation pipeline than the canonical-four substrate, Stage B handling for it is separately required

**Drax verification on first VS2b-emitting season:** after Stage B fix + first regen with embodiment-narrative-beat generation pipeline shipping, run `grep -c "embodiment_tag\|embodiment_narrative_beat\|spirit_name" exports/<season_id>/classes.json` — count should be ≥3 × (number of classes). If 0, Stage B drop fires; surface to knight-rider before loadout-side wiring proceeds.

This protection is what makes the spec's "engine emits beat → drax displays" pipeline reliable. Without it, the spec's Cluster A (display surface) ships against a Cluster E (LLM-bound) data flow that doesn't reach Cluster A's consumer.

---

## 11. Failure modes + fallbacks

### 11.1 LLM-generated beat lands poorly

**Symptom**: beat reads as generic, on-the-nose, off-tone, or breaks voice convention.

**Mitigation**:
- Per-class beat regeneration dispatch (cheap; single class)
- Per-season beat regeneration (more expensive; all classes)
- Hand-edit fallback: knight-rider authorizes star-lord to manually overwrite a beat in the per-season class data file if a generation produces a particularly bad result

**Acceptance criterion** (gandalf authoring): the season-feel rubric (per `season-feel-rubric.md`) evaluates beat quality. Beats that fail rubric → regenerate.

### 11.2 Engine fails to emit beat (LLM call failure, schema bug)

**Surface behavior**: drax displays placeholder text — *"This Court has not yet been named."* — with portrait + naming still visible. Player still gets a recognizable surface; the beat just isn't there for this class until engine fixes.

**Not silent failure**: drax surfaces a small warning indicator to dev console; star-lord follows up to investigate.

### 11.3 chierit portrait fails to load

**Surface behavior**: drax displays silhouette placeholder portrait (element-tinted) with naming + beat still visible. Beat still does identity work even without portrait.

### 11.4 Stage 3 cipher migration delivers per-season vocabulary that breaks beat coherence

**Symptom**: per-season vocabulary substitutions make the beat read weird ("kindling-veined" gets substituted with a per-season fire-vocab that doesn't fit).

**Mitigation**: per-season vocabulary generation includes a coherence check against in-flight beats; substitutions that break coherence trigger beat regeneration for affected classes.

---

## 12. Open questions for drax

Recommended defaults given where they're not blockers. Drax calls back if any default doesn't survive first-pass implementation.

1. **Class-roster view existence** — does the current loadout app have a "browse all classes in this season" view, or only the active-class detail? If yes, the compact-card form (§ 8.3) applies; if no, scope this dispatch to the active-class-only header. Recommend: confirm via current state, scope accordingly.

2. **Insertion point in existing layout** — drax confirms where exactly the class-header surface inserts above existing class-detail. May require small refactor of existing header components.

3. **Typography selection** — pixel-art-coherent display font for spirit name vs clean sans-serif. Drax tests both; gandalf reviews if uncertain.

4. **Background-tint specifics** — element-themed tinting at what intensity? Recommend subtle (~5-10% alpha over neutral base) to avoid fighting portrait.

5. **Transition animation between class switches** — 200ms fade recommended; drax tunes if it feels wrong.

6. **chierit character reconciliation** — physical / hybrid element class portraits need fallback strategy (per Q3 today's discussion). Recommend small knight-rider-authored reconciliation dispatch alongside this implementation: confirm 10 chierit slot assignments to Reincarnated element vocabulary; identify what to do for physical/hybrid mismatches.

---

## 13. Implementation cascade

### Immediate (no engine dependency)

- Drax scaffolds class-header component with placeholder portrait + placeholder beat
- Typography exploration
- Mobile responsiveness implementation
- chierit portrait crop tooling (idle-frame extraction → 96×96 crop)

### Gated on Stage 2 cosmological-vocabulary ship (star-lord; in flight)

- Per-season spirit name display (live data instead of placeholder)
- Per-season L3 vocabulary available for beat generation

### Gated on Stage 3 cipher migration (star-lord; dispatched)

- Beat generation uses per-season vocabulary fully
- Canonical-four labels fully hidden from player-visible beat content

### Gated on new `embodiment_narrative_beat` schema field

- rocket adds field to `PlayerClass` schema (additive)
- star-lord adds field to export packet + manifest
- LLM beat-generation call added to season creation pipeline
- drax consumes the field for display

### Estimated drax effort

- Component scaffolding (no engine dep): ~2-3 days
- Engine integration (post-schema-field ship): ~1-2 days
- Polish + mobile tuning + accessibility: ~2 days
- chierit portrait tooling: ~1 day
- **Total VS2b drax load: ~1-1.5 weeks** for loadout-side

Demo-side embodiment surface: separately scoped, post-VS2b, ~2-3 weeks drax (per-class chierit character rendering in fights — already partially in flight via the character-track ingest dispatch).

---

## 14. What this spec does NOT cover

- **Demo-side embodiment surface** — in-fight character rendering; chierit characters per-class. Covered by separate character-track ingest dispatch + future demo-integration dispatch.
- **Spirit Guide voice surface** — first-person Spirit Guide commentary; separate doc `spirit-guide-voice.md`; surface lives elsewhere in loadout app (e.g., per-skill commentary, per-encounter coaching).
- **Trial / Mirror / Passage ritual moment displays** — separate canonical-story docs (`trial-moment-ritual.md`, etc.); ritual moments use different visual conventions appropriate to those moments.
- **Build-coach / Strong/Solid/Marginal/Sidegrade/Downgrade verdicts** — Stage A7 territory; surfaces alongside skill tree (per B6 UI scoping spec) and gear loadout, not in the class-header.
- **Season-roster overview / Court of Forms canvas** — separate surface (TBD; post-VS2b) where player views all 5-6 classes-as-cohort for the season. Class-header is per-class focused; Court-of-Forms canvas is roster-focused.
- **Beat regeneration UI** — out of scope for VS2b. If a beat lands poorly, knight-rider authorizes a regen dispatch (server-side); player sees the new beat on next load.
- **Localization** — beats are English-only at VS2b. Localization is post-Phase-0.
- **Audio voice-line for beats** — explicitly out per `audio-strategy-phase0.md`; audio deferred to Phase 1+.

---

## 15. Recommended next actions

For knight-rider:
1. Author drax dispatch for loadout-side embodiment-narrative-display implementation against this spec — scoped to "scaffolding can begin now; engine integration when `embodiment_narrative_beat` field ships"
2. Author rocket dispatch for `embodiment_narrative_beat` schema field addition (Discipline #14 — generative-side schema)
3. Author star-lord dispatch for LLM beat-generation call addition (likely folds into Stage 2 cosmological-vocabulary generation pipeline as a follow-on)
4. Author chierit element-reconciliation dispatch (small; ~30 min) confirming 10-character slot assignments + physical/hybrid fallback strategy
5. Surface this spec in next handoff doc — companion to B6 skill-tree UI scoping

For drax (when dispatch lands):
1. Read this spec end-to-end before scaffolding
2. Call back on § 12 open questions before locking visual conventions
3. Build component scaffolding against mocked beat content until `embodiment_narrative_beat` field ships
4. Surface any spec ambiguity to gandalf via knight-rider (not improvise)

For rocket + star-lord:
1. Confirm `embodiment_narrative_beat` field placement (generative-side schema per Discipline #14)
2. Sequence the LLM beat-generation call relative to Stage 2 cosmological-vocabulary + Stage 3 cipher migration

For gandalf (self):
1. Iterate exemplar beats library based on first-season generation results
2. Author season-feel rubric extension specifically for beat quality (currently `season-feel-rubric.md` is general; beat-specific criteria may help LLM prompt engineering)
3. Author Court-of-Forms canvas spec (the season-roster surface) — post-VS2b authoring window
4. Review demo-side embodiment surface need when VS2b loadout ships and playtest signal returns

---

— gandalf, 2026-05-16 (Day 4 close)
