# VFX Layered Architecture — 4-Layer Composition Model (VS2a)

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-craftpix-mega-catalogue-curation-extension.md` § Deliverable 4
**Predecessor inputs:**
- Pimen subset selection (`agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md`) — the Layer-1 substrate
- Legolas-3 inventory (`agentic_orchestration/research/catalogue/craftpix-mega-catalogue-2026-05-17/free-characters-and-vfx-inventory.jsonl`) — Layers 2/3/4 candidates
- Drax VS2a first VFX integration step-3 (just shipped per phase-1-p1-log; the sub-container layer split that this architecture composes against)
- VS2a VFX scene-needs spec (`canonical/story/vs2a-vfx-scene-needs.md`) — the substrate-tag × slot grammar Layer 1 was authored against

**Companion JSONL:** `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.jsonl`

---

## 1. Architecture overview

Legolas-3's discovery of Frostwindz (class-archetype VFX + Slashes + Impacts) + Alenia Studios (Atmospheric overlays) opens a layered composition model that the original Pimen-only architecture could not express. The 4-layer model:

| Layer | Source vendor(s) | Role | Render-pipeline target | Replaces / extends |
|---|---|---|---|---|
| **Layer 1 — substrate** | Pimen (curated subset 31 rows / 14 packs) | Element × VFX-slot wiring; canonical-7 × A/B/C/D/E coverage | particlesUnder + particlesMid + particlesOver per slot | (foundational; existing Pimen subset is unchanged) |
| **Layer 2 — class-archetype** | Frostwindz Blood Mage / Necromancer / Rogue / Starcaller / Vampire | Active-spirit visual register; composited ON TOP OF Layer 1 to produce class-specialized visuals for same substrate | particlesMid + particlesOver (same slot positions as Layer 1; overlay tint/composite) | EXTENDS Layer 1 with class-thematic visual register |
| **Layer 3 — physical** | Frostwindz Slashes (G4 close path) + Frostwindz Impacts (Pimen hit-spark alternative) | Physical-archetype Slot B/C; commercial-license alternative to CC-BY pixel-battle-effects | particlesMid (slash) + particlesOver (impact) | **REPLACES** CC-BY `pixel-battle-effects` for physical-slash + **MAY REPLACE** Pimen battle-vfx-hit-spark for physical-impact |
| **Layer 4 — atmospheric** | Alenia Studios Atmospheric (20 effects) | Full-screen room-atmosphere overlays; ambient room-theme effects | full-screen container underlay OR overlay (new pixi layer, BENEATH Layer 1 or ABOVE — see § 4.3) | NEW layer not present in Pimen-only architecture |

### 1.1 Composition order (rendering)

Bottom to top in z-order:

1. **Floor tiles + dungeon tileset** (drax world layer)
2. **Layer 4 atmospheric — underlay variant** (e.g., Phantom Fog, Underwater Caustics, Aurora Borealis behind everything) — full-screen at low alpha
3. **Sprite layer** (characters, monsters, props)
4. **Layer 1 substrate VFX** at `particlesUnder` (cast-prep telegraphs behind caster)
5. **Layer 1 substrate VFX** at `particlesMid` (projectiles between caster and target)
6. **Layer 2 class-archetype VFX** at `particlesMid` (composited on top of Layer 1 projectiles for class-specialized variant)
7. **Layer 3 physical VFX** at `particlesMid` (slash arcs)
8. **Layer 1 substrate VFX** at `particlesOver` (impacts above target sprite)
9. **Layer 3 physical VFX** at `particlesOver` (impact tints, B&W-tint-composited)
10. **Layer 2 class-archetype VFX** at `particlesOver` (class-thematic impact register)
11. **Layer 4 atmospheric — overlay variant** (e.g., Fire Embers, Magic Wind+Fairy Dust above scene) — full-screen at low-to-mid alpha

### 1.2 Why this architecture

The Pimen-only model could not express:
- **Class-thematic visual differentiation** between a generic shadow-mage and a necromancer-specialization (both share the same canonical-7 shadow substrate; Pimen does not vary register by class).
- **Commercial-license alternative for physical-slash** (G4 risk forced acceptance of CC-BY `pixel-battle-effects` attribution surface).
- **Full-screen room-atmosphere** (Pimen has zero coverage for ambient room-theme effects — that's an entirely different asset class).

The 4-layer model:
- Preserves the Pimen substrate × slot canonical grammar (Layer 1 is unchanged).
- Adds class-specialization (Layer 2) as compositing variants without proliferating substrate-tag combinations.
- Resolves G4 (Layer 3 replaces CC-BY).
- Introduces room-atmosphere (Layer 4) as a new design dimension not previously available.

---

## 2. Layer-by-layer specifications

### 2.1 Layer 1 — substrate (Pimen)

**Source:** existing `pimen-subset-vs2a-2026-05-17.jsonl` (31 rows / 14 packs / $26.35 acquisition cost / unchanged).

**Role:** Element × slot wiring is the substrate. Every cast/projectile/impact/status-apply/status-ambient is rooted here.

**Coverage matrix:** see `pimen-subset-vs2a-selection-2026-05-17.md` § 2 (7-element × 6-slot grid; 41 GREEN cells / 0 YELLOW / 7 RED).

**Render targets:** `particlesUnder` / `particlesMid` / `particlesOver` per slot (drax § 2.7 sub-layer split).

**Status:** unchanged by this architecture — Layer 1 is the foundation. The 4-layer model is additive.

### 2.2 Layer 2 — class-archetype (Frostwindz class packs)

**Source vendors:** Frostwindz Blood Mage / Necromancer / Rogue / Starcaller / Vampire — five FREE class packs, all on disk at `reincarnated-demo/public/assets/free_characters_and_vfx/`.

**License:** Frostwindz Asset License Agreement (commercial-permitted with attribution to Frostwindz).

**Role:** Active-spirit visual register. When the player or a key NPC has a class-thematic spirit form (e.g., a "Necromancer Spirit"), the VFX they emit composite Layer-2 class-thematic visuals ON TOP OF Layer 1 substrate. Same canonical-7 element underneath; class-specialized aesthetic on top.

**Class → archetype mapping:**

| Frostwindz pack | Frame counts (free version) | Reincarnated archetype-fit | Substrate-overlay | Slot coverage |
|---|---|---|---|---|
| Blood Mage | VFX1 (3-phase start/loop/end) + VFX2 (12f) + VFX3 (4f) | shadow + blood — controller-shadow-canonical or dark-mage hybrid | shadow | A (VFX1 start), B/C (VFX2/VFX3) |
| Necromancer | VFX1 (9f) + VFX2 (7f) + VFX3 (6f) + VFX4 (15f) | shadow + summoner blend; controller-shadow-canonical primary | shadow | A (9f cast), C (6-7f impact), D/E (15f sustained) |
| Rogue | VFX1-5 (9/6/9/8/17 frames; PSD source included) | physical-rogue primary; hunter-physical secondary | physical | A (9f cast), B (9f projectile/dash), C (6f impact), D (8f status), E (17f sustained) |
| Starcaller | VFX1 (7f) + VFX2 (8f) + VFX3 (15f) | holy + lightning blend; mage-celestial primary | holy + lightning | A (7f cast-charge), C (8f impact), E (15f sustained ambient — cosmic aura loop) |
| Vampire | VFX1 (10f) + VFX2 (9f) + VFX3 (6f) + VFX4 (6f) + VFX5 (11f) | shadow + physical hybrid (vampire archetype); controller-dark-physical | shadow + physical | A (10f cast), B (9f projectile — blood bolt), C (6f impacts × 2), E (11f ambient — life-drain aura) |

**Render targets:** same sub-containers as Layer 1 (`particlesMid` / `particlesOver`) — Layer 2 composites at the SAME slot positions, just with class-thematic aesthetic overlay.

**Class-aware activation:** Layer 2 is OPTIONAL per-spirit. A vanilla fire-mage spirit emits only Layer 1 (Pimen fire-spell-effect-3). A "Blood Mage" spirit emits Layer 1 (Pimen shadow-element substrate) PLUS Layer 2 Blood Mage compositing. The runtime check is `if (spirit.class_archetype in CLASS_VFX_REGISTRY) compose(layer1, layer2_for_class)`.

**Substrate-overlay vocabulary observation:** four of the five Frostwindz class packs (Blood Mage, Necromancer, Vampire, partial Starcaller) overlay on the **shadow** substrate. Rogue overlays **physical**. Starcaller overlays **holy + lightning**. This concentrates Layer-2 visual register on shadow — useful for a campaign with strong shadow-class differentiation but underweighted for fire/water/earth/wind/lightning class differentiation. Forward-flag: future Frostwindz commissions or alternative vendors needed to balance class-overlay coverage across elements.

### 2.3 Layer 3 — physical (Frostwindz Slashes + Impacts)

**Source:** Frostwindz Slashes pack + Frostwindz Impacts pack — both FREE, on disk, commercial-license-permitted with Frostwindz attribution.

**Role:** Physical-archetype Slot B (projectile/slash-arc) + Slot C (impact) — REPLACES the Pimen CC-BY dependency for physical visuals.

**Coverage:**

| Frostwindz pack | Pimen pack(s) it potentially replaces | G4 status | Recommendation |
|---|---|---|---|
| **Slashes** (3 variants × 2 sizes: 128×128, 64×64) | `pixel-battle-effects` (CC-BY-only; physical-slash substrate-tag) | **G4 CLOSE PATH on disk** — Frostwindz Slashes is commercial-permitted with single-vendor attribution; CodeManu acquisition no longer needed | **ACCEPT** (elrond recommendation; pending Matt Q2) |
| **Impacts** (7 effects × B&W + COLOR variants) | `battle-vfx-hit-spark` ($4.25; planned acquisition per Pimen subset) | **PIMEN PURCHASE MAY BE REDUNDANT** — 7 variants > 1 pack; B&W variants enable runtime element-tint composition matching drax's tint-strategy | **SKIP** Pimen hit-spark (elrond recommendation; pending Matt Q3) |

**B&W + COLOR variant advantage (Impacts pack):** the 7 impact effects each ship in B&W and COLOR variants. The B&W variant enables runtime tinting via color-multiply per drax's tint-composition strategy — meaning the same impact sprite can render as fire-impact / water-impact / lightning-impact / etc. by applying an element-specific tint at compose time. This is a SUPERIOR wiring architecture compared to single-tinted Pimen hit-spark.

**Render targets:**
- Slashes: `particlesMid` (slash arcs travel between caster and target)
- Impacts: `particlesOver` (impact tints above target sprite)

**Net cost change if Matt accepts both recommendations:**
- $0 (Slashes free) + $0 (Impacts free) − $4.25 (skip Pimen hit-spark) = **savings $4.25**
- G4 risk eliminated (no CC-BY attribution surface needed)
- No CodeManu acquisition needed for VS2a (deferred to Stage A2 if quality issues surface)

### 2.4 Layer 4 — atmospheric (Alenia Studios)

**Source:** Alenia Studios Pixel Art Atmospheric VFX Pack — 20 effects, FREE, CC BY 4.0 with Alenia Studios additional terms.

**License posture:**
- CC BY 4.0 attribution required ("Alenia Studios" credit in game credits panel).
- Additional terms: no redistribution/resale of raw assets; no AI training on assets; commercial use in integrated products permitted.
- Operational implication: requires single credit-panel line; otherwise same low-friction as Pimen commercial-license.

**Role:** Full-screen room-atmosphere overlays. These are NOT slot-based per-ability VFX. They are AMBIENT room-theme overlays that play continuously while the player is in a particular room type. 48-frame seamless loop, 320×180 base resolution per effect.

**20 atmospheric effects categorized by render-purpose:**

| Effect | Element-thematic fit | Render-purpose | Placement |
|---|---|---|---|
| Fire Embers / Fire Ashes | fire | room-overlay | overlay (above sprites) |
| Cinematic Snow / Cozy Snow / Creeping Frost (Aurora) | water/ice | room-overlay | underlay (snow falls behind) or overlay |
| Aesthetic Rain / Ground Rain+Splashes | water | room-overlay | overlay |
| Aesthetic Wind / Epic Tornado / Magic Wind+Fairy Dust | wind / holy-wind | room-overlay | overlay |
| Fractal Lightning Storm | lightning | room-overlay | overlay |
| Swamp Bubbles / Boiling Bubbles | earth/poison | room-overlay | underlay (bubbles in floor liquid) |
| God Rays | holy | room-overlay | overlay |
| Phantom Fog of War | shadow | room-overlay | underlay (fog of war beneath sprites) |
| Sakura Petals / Autumn Leaves | nature/seasonal | room-overlay | overlay |
| Cozy Spores / Fireflies | ambient-mystic | room-overlay | overlay |
| Meteor Shower | celestial/holy | room-overlay | overlay |
| Underwater Caustics | water (room-type underwater) | room-underlay | underlay (caustics on floor) |

**Render targets:** new pixi container — `atmosphericUnder` (between dungeon tileset and sprite layer) + `atmosphericOver` (above particlesOver, below HUD).

**Element-thematic room concept:** rooms can carry an `atmosphere_theme` attribute that wires one or more atmospheric effects. E.g., a "fire-element trial room" runs Fire Embers (overlay) at low alpha; a "shadow-affinity room" runs Phantom Fog (underlay) at mid alpha. This enables environmental thematic identity without modifying tilesets.

**VS2a vs VS2b scope:** Layer 4 is **VS2b-scope** for full deployment. Per the dispatch out-of-scope rules + drax v1.12 in-flight wiring, only conservative deployment is appropriate for VS2a:
- **VS2a deployable:** 1-2 atmospheric effects as room-overlays for a single demo room (proof-of-concept; informs drax integration cost).
- **VS2b full deployment:** atmosphere_theme attribute on all room types; 20 effects mapped to thematic vocabulary.

### 2.5 Cross-layer dependencies (drax integration)

| Drax integration requirement | Layer(s) | Status |
|---|---|---|
| `particlesUnder` / `particlesMid` / `particlesOver` sub-containers | 1, 2, 3 | DONE per drax VS2a step-3 (just shipped) |
| `atmosphericUnder` / `atmosphericOver` containers | 4 | NEW — drax integration plan needed; not blocking for VS2a |
| `spirit.class_archetype` runtime field for Layer 2 activation | 2 | Engine-side (rocket scope); not blocking for VS2a |
| B&W variant tint-composition pipeline | 3 (Impacts) | Drax has tint-composition for Pimen buff/debuff palette-shift; same primitive extends here |
| Layer-2 compositing-on-Layer-1 alpha-blend mode | 2 | NEW — drax compositing experimentation needed; not blocking for VS2a |
| `atmosphere_theme` room attribute | 4 | Engine-side world/topology amendment (VS2b scope) |

---

## 3. Manifest schema extension (companion JSONL)

The companion JSONL file (`vfx-layered-architecture-vs2a-2026-05-17.jsonl`) adds one row per asset across Layers 2/3/4, with the schema:

```
asset_id            — composite key: <layer>.<pack_slug>.<vfx_id_or_substrate>
layer               — "2" | "3" | "4"
vendor              — "frostwindz" | "alenia-studios"
pack_origin         — pack folder name
acquired_path       — relative path under reincarnated-demo/public/assets/
class_archetype     — Layer 2 only: which Reincarnated archetype this overlay fits
substrate_overlay   — Layer 2/3 only: which canonical-7 substrate this composites on top of
slot                — Layer 2/3 only: "A" | "B" | "C" | "D" | "E" (drax slot taxonomy)
atmosphere_theme    — Layer 4 only: thematic register tag(s)
render_target       — sub-container name (particlesUnder/Mid/Over or atmosphericUnder/Over)
license_class       — "frostwindz-asset-license" | "cc-by-4.0-alenia-additional-terms"
attribution_text    — credit-panel attribution string
animations_in_pack  — list of animation ids/names within the pack
frame_count         — animation length in frames
size_register_fit   — EXACT / CLOSE / MISMATCH per gandalf canon
drax_integration_module — which drax module/container consumes this row
g4_status_implication — Layer 3 only: G-CLOSE-PATH / G-REDUNDANCY / N/A
pimen_overlap       — "EXTENSION" | "UPGRADE" | "REDUNDANCY" | "NONE"
vs2a_status         — "active-poc" | "deferred-vs2b" | "active"
acquisition_status  — "ON-DISK"
matt_decisions_referenced — list of Matt Q-IDs this row depends on
crawl_date          — legolas-3 crawl date
```

---

## 4. Gap-status changes formalized

### 4.1 G4 (physical-slash CC-BY risk) — close path via Layer 3

**Pre-architecture (Pimen-only) status:** PARKED Matt-decision; recommendation Path B (accept CC-BY attribution for `pixel-battle-effects`) OR Path A (CodeManu acquisition Stage A2).

**Post-architecture status:** **CLOSE-PATH on disk via Frostwindz Slashes.** Elrond recommendation = **ACCEPT Frostwindz Slashes** for physical-slash substrate-tag. Net effect:
- CC-BY `pixel-battle-effects` no longer needed for physical-slash.
- CodeManu acquisition deferred indefinitely (only needed if Frostwindz quality issues surface at drax integration).
- Single attribution credit (Frostwindz) covers Slashes + Impacts + 5 class packs.

**Pending Matt Q2:** authorize Frostwindz Slashes as G4 close path (recommendation: ACCEPT).

### 4.2 Pimen battle-vfx-hit-spark redundancy ($4.25 savings opportunity)

**Pre-architecture status:** planned acquisition $4.25 per Pimen subset § 1.2.

**Post-architecture status:** **MAY BE REDUNDANT.** Frostwindz Impacts pack (7 effects × B&W + COLOR variants, on disk, $0) provides superior coverage:
- 7 variants vs 1 pack.
- B&W variants enable runtime tinting (matches drax tint-composition strategy).
- Same commercial-license attribution surface (Frostwindz credit covers all on-disk Frostwindz assets via one line).

**Elrond recommendation:** **SKIP** Pimen battle-vfx-hit-spark purchase; use Frostwindz Impacts. Net savings $4.25.

**Pending Matt Q3:** authorize SKIP of Pimen hit-spark $4.25 purchase (recommendation: SKIP).

### 4.3 G-COFFIN closure via dungeon-tileset Layer (not Layer 1-4 VFX)

(Out of VFX layer scope — handled in dungeon-tileset manifest. See `dungeon-tileset-subset-vs2a-2026-05-17.jsonl` row for `craftpix-net-298079`.)

### 4.4 NightBorne BLOCKED (Q5 pending)

NightBorne character sprite ships GIF-only format with NO license file. Per legolas-3 § 9: cannot include in any curated subset until Matt resolves license verification. **Excluded from this manifest in all layers.** Forward-flag: if license resolves, NightBorne could enter as a character-sprite asset (not a VFX layer — character-sprites are different asset class).

---

## 5. Acquisition cost impact summary

| Item | Pre-architecture cost | Post-architecture cost | Delta |
|---|---:|---:|---:|
| Pimen `pixel-battle-effects` (CC-BY, free, attribution surface) | $0 (attribution surface) | $0 (NOT USED — replaced by Layer 3 Slashes) | $0; CC-BY surface eliminated |
| Pimen `battle-vfx-hit-spark` | $4.25 (planned) | $0 (SKIP — replaced by Layer 3 Impacts) | **-$4.25 savings** |
| CodeManu kinetic-VFX (deferred Stage A2) | TBD ($30-50 est.) | $0 (deferred indefinitely) | TBD savings |
| Frostwindz Slashes | n/a | $0 (on disk, free) | new free asset |
| Frostwindz Impacts | n/a | $0 (on disk, free) | new free asset |
| Frostwindz 5 class packs | n/a | $0 (on disk, free) | new free assets |
| Alenia Atmospheric | n/a | $0 (on disk, CC BY 4.0) | new free asset |
| **Net acquisition delta** | | | **-$4.25 (pending Matt Q3) + CC-BY surface eliminated** |

**Updated VS2a Pimen acquisition list (if Matt approves Q2+Q3):**

| Item | Cost | Status |
|---|---:|---|
| mega-pack-elemental-spell-effects-01 | $12.75 | unchanged |
| battle-vfx-hit-spark | ~~$4.25~~ | **SKIP** (replaced by Frostwindz Impacts) |
| battle-vfx-projectile | $4.25 | unchanged (Slot B hunter-projectile; Frostwindz Slashes is slash-arc not projectile) |
| buff-n-debuff-vfx-pack-01 | $2.55 | unchanged |
| buff-n-debuff-vfx-pack-02 | $2.55 | unchanged |
| pixel-battle-effects | ~~CC-BY~~ | **NOT USED** (CC-BY surface eliminated; replaced by Frostwindz Slashes) |
| **Updated total** | **$22.10** | (vs original $26.35 — savings $4.25) |

---

## 6. Attribution surface (consolidated)

The 4-layer architecture introduces three new attribution credit lines beyond Pimen:

| Vendor | License | Credit text recommendation |
|---|---|---|
| Pimen | commercial-license (purchased packs) | "VFX assets by Pimen — pimen.itch.io" |
| Frostwindz | Frostwindz Asset License Agreement | "Class-archetype + slash + impact VFX by Frostwindz — frostwindz.itch.io" |
| Alenia Studios | CC BY 4.0 with additional terms | "Atmospheric VFX by Alenia Studios (KXLT) — alenia-studios.itch.io" |

**CodeManu** (formerly the G4 close-path vendor) is no longer needed for VS2a; no attribution surface.
**CC-BY surface from `pixel-battle-effects`** is eliminated.

---

## 7. Open Matt-decisions for Layer architecture

Carried forward from legolas-3:

- **Q2 — Frostwindz Slashes as G4 close path:** ACCEPT (elrond recommendation) / DECLINE / DEFER. Recommendation: ACCEPT.
- **Q3 — Skip Pimen $4.25 hit-spark purchase:** SKIP (elrond recommendation) / KEEP / DEFER. Recommendation: SKIP.
- **Q5 — NightBorne license resolution:** BLOCKED until resolved. Recommendation: DEFER NightBorne until license verified.

New Matt-decisions surfaced by Layer architecture:

- **Q-LAYER-1 — Layer 4 atmospheric VS2a deployment scope:** deploy 1-2 effects as POC in single demo room (recommended) / defer entirely to VS2b / deploy all 20 (not recommended for VS2a).
- **Q-LAYER-2 — Layer-2-overlay-on-Layer-1 alpha-blend approval:** authorize drax compositing experimentation at VS2a integration step (recommended) / defer to VS2b. Recommendation: authorize POC during drax integration.

---

## 8. Drax integration plan (handoff)

**Pre-requisite (DONE per drax VS2a step-3):** `particlesUnder` / `particlesMid` / `particlesOver` sub-container split.

**VS2a scope (post-v1.12):**
1. Wire Frostwindz Slashes to physical-slash Slot B/C (Layer 3) — replaces pixel-battle-effects.
2. Wire Frostwindz Impacts B&W variant with element-tint composite — replaces Pimen hit-spark in physical-impact slot. Verify tint-composition produces element-distinct visuals.
3. Optional POC: wire 1-2 Alenia atmospheric effects (Fire Embers + Phantom Fog?) at low alpha for single demo room. Container infrastructure (`atmosphericUnder`/`atmosphericOver`) needs creation.

**VS2b scope:**
1. Add `spirit.class_archetype` runtime field; activate Layer 2 compositing when class matches Frostwindz pack set.
2. Add `room.atmosphere_theme` attribute; full Layer 4 deployment per room type.
3. Layer 2 alpha-blend mode experimentation across class packs.
4. Multi-vendor attribution credit panel.

**Out of scope (further deferred):**
- Element-balance Layer 2 expansion (5 of 7 elements lack class-overlay coverage; future Frostwindz commission OR alternative vendor for fire/water/earth/wind/lightning class-archetype VFX).
- NightBorne integration (Matt Q5 BLOCKED).

---

## 9. Forward observation — Layer 2 element-imbalance

Frostwindz class packs concentrate on shadow + physical + holy+lightning. The 7-element canonical-7 grid coverage at Layer 2:

| Canonical-7 element | Layer 2 coverage | Gap |
|---|---|---|
| fire | NONE | Layer 1 (Pimen fire-spell-effect-3) only; no class-thematic register variant |
| water | NONE | Layer 1 only |
| earth | NONE | Layer 1 only |
| wind | NONE | Layer 1 only |
| lightning | Starcaller (partial) | partial — celestial subset |
| holy | Starcaller | Layer 2 covered |
| shadow | Blood Mage + Necromancer + Vampire | over-covered (3 visual sub-registers) |
| physical | Rogue | Layer 2 covered |

**Implication:** if VS2a-VS2b emphasizes fire/water/earth/wind/lightning class-thematic spirit forms, the architecture has insufficient Layer-2 coverage. Two paths:

- **Path A:** future Frostwindz commission for fire/water/earth/wind/lightning class packs (waits on vendor catalogue extension)
- **Path B:** alternative vendor for class-archetype VFX targeting under-covered elements (legolas-4 scope candidate)
- **Path C:** accept Layer-2 absence for under-covered elements; rely on Layer 1 (Pimen substrate) alone for those element-class spirit forms

Elrond observation (not a recommendation): Path C is workable for VS2a-VS2b narrow slice; the Frostwindz set already covers the highest-priority spirit-archetype set (shadow-class diversity matches dark-fantasy register). Path A or B becomes relevant if/when fire/water/earth/wind/lightning class-thematic spirit forms become load-bearing.

---

*Filed 2026-05-17 by elrond per dispatch authorization. § 4 of dispatch deliverables.*
