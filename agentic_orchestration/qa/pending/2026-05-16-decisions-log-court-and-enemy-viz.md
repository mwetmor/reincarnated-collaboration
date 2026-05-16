# Decisions-log entry drafts — Court canonical + Enemy visual legibility

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source canonical docs:** `canonical/story/court-of-forms.md`, `canonical/story/enemy-visual-legibility.md`
**Process:** Gandalf identified these canonical locks as requiring decisions-log entries per ADR-002. Knight-rider drafts → jack-ryan Gate 1 (optional) → Matt approval → write to `reincarnated-engine/design/decisions/decisions-log.md`.

**Target file:** `reincarnated-engine/design/decisions/decisions-log.md` — append at the top of the active-decisions section, matching existing entry format.

---

## Entry 1 — Court canonical + meaning-of-the-arc statement

### 2026-05-15: Court of Forms as form-library framing; meaning-of-the-arc locked

**Decision:** The Earth Self's hub holds the **Court** — a navigable assembly of named retainers with stations and (over time) presence. The Court framing supersedes prior gallery / roster / inventory / gacha vocabulary for the form library. Eight structural commitments are locked (C1-C8 per `canonical/story/court-of-forms.md`), and the **meaning-of-the-arc statement** is canonical for downstream design, copy, pitch, and LLM-prompt context:

> *Reincarnated rewards the patient. Each season is a life-lived; each form a self-tried. You ascend the one you chose to live with — and over many seasons, your Court accrues those choices. The depth of the Court is the measure: how many forms have you been willing to become; how many have you ascended through their full journey; how many seasons has the Wheel turned with you still walking. There is no final form because there is no final you; there is only what the Court remembers.*

**The depth-of-Court is the meta-measure, read on three axes simultaneously:**

1. Diversity of ascensions (how many forms have you been willing to become)
2. Completion quality (how many ascended through full journey vs Mirror-Trial vs Passage)
3. Longevity (how many seasons has the Wheel turned with you still walking)

**Reasoning:** File 29 identified the cross-season meta-progression spine ("Earth Self is the meta-layer spine") and file 32 § 11 locked the one-ascension-per-season pace. Their player-experience weight was underspecified. Prior framings reached for gacha-language ("accumulation of LLM-generated ascended spirits"), mechanically accurate but emotionally thin — gacha collections are inventories, not relationships. Matt's recognition 2026-05-15: *"The court adds weight to the end game that I didn't understand before."* The end-game weight problem is structurally load-bearing for retention in shipped ARPGs; the Court framing makes the project's existing seasonal-descent + return-to-Earth pattern explicit.

**Alternatives considered:**

- **Fate/Zero / Nasuverse Throne of Heroes as canonical reference** — rejected for substrate-incompatibility. Fate's lore-weight derives from pre-Servant *humanoid* historical/mythical existence; canonical commitment would silently teach the player that non-humanoid forms (the isekai breadth doc 37 protects) are "not real Heroes." This is exactly the **implicit-pillar drift pattern** doc 37 § 9.1 names. The Fate frame is retained as a *design-conversation lens* but does NOT enter the canonical layer; downstream docs / dispatches / prompts / UI should not echo Fate-specific vocabulary (Saber, Master, Servant, Command Seal, Throne, etc.).
- **Single humanoid-coded class-role label set** (Knight / Berserker / Archer / etc.) for Court class-roles — rejected for the same substrate-incompatibility. Replaced by C8's dual-label pattern (universal function tag + embodiment-flavored class-name), structurally parallel to doc 37 § 4 Position C's gear-slot architecture.
- **Single universal-mechanical label set only** (Front-Line / Ranged / Control / etc.) — form-agnostic but dulls the narrative register; reads as tactical inventory not retainers. C8 layers the embodiment-flavored name on top.

**Canonical-cited precedent retained:** A-1 Pictures' Solo Leveling Shadow Army (Sung Jin-Woo's accumulated army of named retainers with rank and presence). Shadows include non-humanoid forms (Beru the ant-king, Tank the lion), meaning the precedent's substrate already admits the isekai breadth Reincarnated requires.

**Status:** Active. Implementation cascades to: drax (Earth-Self-hub presentation, ascension cutscenes, Court UI), rocket (LLM-generated Court-names preserved through to hub display per C3), star-lord (LLM prompt context honors Court framing and meaning-of-the-arc), telemetry (eventual depth-of-Court measurement on the three locked axes per C7).

**Related:**
- `canonical/story/court-of-forms.md` (full canonical doc, 8 structural commitments + 5 open questions)
- `canonical/story/cosmology-reincarnated.md` (Court sits within the broader cosmology)
- `canonical/story/embodiment-narrative-layer.md` (forthcoming — authoritative dual-label vocabulary per C8)
- `canonical/29-design-overview.md` § Cross-season meta-progression (the latent intent this lock realizes)
- `canonical/32-progression-design.md` § 11 (one ascension per season — already locked)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 4 (Position C — same architectural pattern as C8)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 9.1 (Discipline #13 — the Fate-rejection is a worked instance)

---

## Entry 2 — Enemy visual legibility canonical + anti-pattern rejection

### 2026-05-15: Enemy visual legibility — sprite-archetype registry; sprite-from-player-pool rejected as anti-pattern

**Decision:** Enemy presentation is locked as **player-perception architecture** with seven structural commitments (S1-S7 per `canonical/story/enemy-visual-legibility.md`). Enemies are rendered from a **separate sprite-archetype registry**, NOT from the player-class sprite pool. The anti-pattern of "enemies rendered as scaled-up player-class sprites with no further visual differentiation" is **canonically rejected at Gate 1** for any future dispatch proposing it.

**The six perceptual axes the player must classify at the genre's 200ms recognition target:**

| Axis | Player question | Primary signal |
|---|---|---|
| Tier | How threatening? | Silhouette complexity + aura presence |
| Element | What strategy/resistance? | Primary palette coloring |
| Archetype | How does it fight? | Sprite shape and silhouette |
| Trial-encounter | Act's culmination? | Cinematic frame on encounter |
| Mirror-of-me | My reflection? | Same-palette mirrored animation |
| Pack-vs-individual | Swarm or discrete? | Density + per-unit simplicity |

**The seven structural commitments:**

- **S1** — Sprite-archetype registry separate from player pool. 6-12 base monster archetypes mapping to engine's brute/caster/controller/sniper/swarmer/tank taxonomy. Asset sourcing: locked-style-register catalogue (Legolas Mode B work).
- **S2** — Element communicated via primary palette coloring (Pixi.js tint), canonical per-element palettes specified.
- **S3** — Tier-coded aura class (none / faint / standard / visible / strong / signature / cinematic).
- **S4** — Trial encounters trigger cinematic frame + LLM-name-banner + Spirit Guide voice line + Body-swap/Mirror choice screen.
- **S5** — Name-banner tier coding (no per-unit swarm / small magic / standard trash / colored elite / iconed mini-boss / cinematic boss / full-banner Trial).
- **S6** — Pack rendering for swarm tier — per-unit simple silhouette + unified cluster aura + single pack-name (engine emits via PackProxy entity per B10.2).
- **S7** — Mirror-fight exception: when `is_mirror_encounter=true`, opponent renders using player's current sprite/animations/palette with recognition-coded subtle cues. Canonical exception to S1.

**Reasoning:** Demo1 family-playtest 2026-05-15 (Matt finding) surfaced that Trial bosses — mechanically generated as player classes by the engine's bestiary architecture — were rendered using the same sprite tooling as playable classes (larger, but visually identical in archetype, palette, and silhouette). The player could not visually distinguish "this is a Trial boss" from "this is a scaled-up version of my own class" without reading the encounter banner. This:

1. Defeats the genre's at-a-glance threat-assessment expectation (200ms recognition target empirically required by loot-ARPG combat)
2. Conflates trial-boss-as-narrative-culmination with trial-boss-as-numerically-tuned-player (the engine's mechanical fact must not surface visually)
3. Specifically breaks the Mirror Trial vs Body-swap Trial visual distinction — if every Trial visually reads as a mirror, the body-swap-path's narrative weight is undercut
4. Compounds with the form-bias work (doc 37) — humanoid player class scaled up looks more like *another humanoid player class*, not like the seasonal cosmology's culminating opponent

The anti-pattern is **canonically rejected** as a Discipline #13 application — a load-bearing player-perception pillar now structurally enforced by being named, locked, and referenced.

**Engine emit-surface fields specified (mostly derivable from existing data):**

`sprite_archetype_tag`, `display_color_primary`, `display_color_secondary`, `display_aura_tier`, `display_silhouette_complexity`, `display_name_banner_class`, `is_trial_encounter`, `is_mirror_encounter`.

**Status:** Active. Implementation cascades:

- **Rocket** — emit the eight new fields per monster (most derivable from existing generation; small emit-surface dispatch).
- **Star-lord** — schema migration for the new export fields; MIGRATION.md per ADR-004 (cross-seam to drax consumption).
- **Drax** — maintain sprite-archetype registry; apply element tint at runtime; render aura per tier; route Mirror encounters to player-sprite rendering; NEVER fall back to player-class sprites for non-Mirror enemies (error rather than degrade).
- **Legolas** — Mode B catalogue work expands to cover monster-sprite registry needs (Elthen, LuizMelo, ansimuz, pimen monster extensions, etc., per locked HD-2D pixel register).

**Related:**
- `canonical/story/enemy-visual-legibility.md` (full canonical doc, 7 structural commitments + 5 open questions)
- `canonical/story/style-register.md` (the visual-idiom decision this protects under)
- `canonical/story/cosmology-reincarnated.md` § Mirror (S7 routes here)
- `canonical/story/trial-moment-ritual.md` (forthcoming — S4 cinematic frame consumes this)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 9.1 (Discipline #13 — anti-pattern rejection is a worked instance)
- B10.2 PackProxy decisions-log entry (S6 pack-rendering consumes this)

---

## Notes for jack-ryan (if Gate 1 invoked)

Specific stress-test questions worth running:

1. **Does Entry 1's framing risk conflating Court (canonical locked) with Earth Self hub (file 29's TBD)?** Both are locked; Court is what the Earth Self hub HOLDS; the hub itself is still TBD per file 29. Worth confirming the entries don't accidentally lock the hub.
2. **Does Entry 2's S1 over-specify the asset registry sizing (6-12 base archetypes) before Legolas has crawled?** Gandalf's doc names this as initial; rocket's eventual implementation may want flexibility. Worth confirming "initial registry sizing" reads as initial, not final.
3. **Both entries reference forthcoming docs** (`embodiment-narrative-layer.md`, `trial-moment-ritual.md`). Do those references load-bear on the canonical lock or just point at future work? If load-bearing, lock waits; if just pointers, no issue.

If jack-ryan finds nothing substantive, the entries can commit to decisions-log directly.
