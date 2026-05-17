# VS2a VFX Scene-Needs Spec

**Authors:** gandalf (sections 1, 3, 4, 5) + drax (section 2)
**Commission:** `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md`
**Status:** PARTIAL — Section 2 authored by drax (2026-05-17). Sections 1/3/4/5 pending gandalf.
**Micro-decisions locked:** A = HYBRID a3 (canonical-7 at combat-text; per-season at flavor only; register-fence rule) | B = Mix-mode (humanoid + non-humanoid; ~75% expected generative failure; curation selects) | C = Option II (VS2a + VS2b forward-looking; ~80-120 lines per scene type)
**Downstream consumer:** elrond (Pimen subset selection + VS2b attribution-pipeline schema dispatch)

---

## Section 1 — Encounter-type inventory (gandalf design framing)

**(Pending — gandalf parallel session)**

---

## Section 2 — Per-skill VFX slot enumeration (drax render-constraint framing)

**Author:** drax
**Date:** 2026-05-17
**Scope:** This section enumerates per-archetype-aggregate VFX slots — the SHAPE of what the render pipeline needs, not a per-skill listing. Framed entirely from the consumption side: what Pixi.js must load, when it fires, how layers stack, what the performance ceiling is.

### 2.0 — Render pipeline baseline (how VFX lands in demo today)

Before enumerating slots, the render infrastructure they plug into:

**Layer stack (demo `src/rendering/stage.ts`):**
```
app.stage (Pixi root)
  └─ bg         (static arena floor / color fill)
  └─ arena      (wave decorations, ambient motes)
  └─ entities   (combatant sprites + attached bars/labels)
  └─ particles  (ALL ability VFX + floating damage numbers)  ← VFX target layer
  └─ ui         (HUD — always on top)
```

All VFX lives in `_layers.particles`. This is a flat `Container` — no sub-layering within it today. The slot enumeration below surfaces where sub-layering WITHIN particles will be necessary (specifically: cast-charge behind the caster; projectiles above the floor but below the caster entity; impacts composited above the entity at peak and then below on fade). These sub-container slots are a VS2a integration task.

**Object model (demo `src/main.ts` vfxPools):**
VFX is pool-managed: `projectiles`, `aoeRings`, `hitFlashes`, `meleeFlashes`, `totems`, `auras`, `beams`, `spriteVfx`, `floatingNumbers`, `chainArcs`, `ringAoes`, `vortexPulls`, `whirlwinds`. Each pool is tick-advanced each frame via the main ticker. Sprite-based VFX (Pimen packs) enter via `spriteVfx` pool today; the pool handles `AnimatedSprite` lifecycle (spawn, tick, despawn on animation complete).

**Spritesheet consumption model (demo `src/abilities/vfx.ts` + ingest pipeline):**
- Pimen packs ingested via `scripts/pimen-ingest/` stages 1-3 → produce `public/assets/pimen/<slug>/sheets/<anim-name>.png` + `metadata.json`
- `metadata.json` schema: `{ pack_slug, animations: [{ name, frame_count, canvas_width, canvas_height, sheet_width, sheet_height, cols, rows, fps_hint }] }`
- Pixi loads the spritesheet via `Texture.from(sheet_path)` + subdivides into frame-count textures using `canvas_width × canvas_height` frame dimensions
- `AnimatedSprite` constructed from the texture array; `animationSpeed` set from `fps_hint / app.ticker.FPS` (12.5fps default for Pimen's 80ms frame rate)
- Loop behavior per slot: see § 2.3 below

**Performance budget:** The existing vfxPools architecture keeps each frame's VFX tick at <0.5ms on a typical encounter. The demo's current bottleneck is sprite rendering, not JS tick logic. For VS2a content density (single-player combat, ~5-15 VFX objects active simultaneously), the constraint is texture-swap count, not arithmetic. **Rule: no more than 1 texture atlas per VFX slot per encounter if avoidable** — atlas consolidation per element is the optimization target for VS2b attribution pipeline.

---

### 2.1 — Archetype families and their VFX slot demands

The engine emits skills against these archetype families (per `b6_archetype_templates.py` + `archetype_composer.py`):

| Archetype family | Representative tags | Dominant skill roles | Key geometry palette items |
|---|---|---|---|
| **Elemental mage** | `fire_mage`, `water_mage`, `lightning_mage`, `holy_mage`, `shadow_mage` | `burst_damage`, `primary_attack` | `projectile_straight`, `impact_burst`, `nova_radial` |
| **Elemental caster** | `fire_caster` (= fire_mage alias), `earth_caster`, `wind_caster`, `lightning_caster`, `holy_caster`, `shadow_caster` | `area_damage`, `primary_attack` | `nova_radial`, `nova_wave`, `ground_targeted_circle`, `cone` |
| **Elemental controller** | `fire_controller`, `water_controller`, `earth_controller`, `wind_controller`, `lightning_controller`, `holy_controller`, `shadow_controller` | `control` (ailments), `area_damage` | `vortex_pull`, `aura_radial`, `ring_aoe`, `ground_slam_directional` |
| **Physical warrior** | `physical_warrior`, `physical_grappler`, `physical_skirmisher` | `burst_damage`, `area_damage`, `control` (CC), `defensive` | `melee_arc`, `melee_strike`, `ground_slam_directional`, `leap_strike` (composite) |
| **Hunter** | `hunter` | `burst_damage`, `mobility`, `defensive` | `projectile_straight`, `impact_burst`, `dash_attack` |
| **Rogue** | `rogue` | `burst_damage`, `mobility` (×2) | `dash_attack`, `projectile_straight`, `melee_strike` |
| **Hybrid mage** | `hybrid_mage` | `area_damage` (×2), `burst_damage` (×2), `damage_over_time`, `defensive`, `utility` | `nova_radial`, `nova_wave`, `aura_radial`, `beam_channel`, `projectile_straight` |

The VFX slot enumeration that follows covers these families in aggregate. Per-archetype variations are noted where they materially differ.

---

### 2.2 — VFX slot taxonomy

Six canonical slots. All skills cast by any archetype family consume a subset of these slots; the subset depends on geometry and effect type.

#### Slot A: Cast-charge

| Property | Constraint |
|---|---|
| **What it is** | Pre-release visual at the caster's position: the "preparation moment." Wind-up glow, energy gathering, stance shift, particle accumulation. |
| **Duration** | Tightly coupled to skill's `cast_time` engine field. For VS2a at current archetype templates: 0–0.4s typical; instant-cast skills (e.g., primary_attack projectiles) may emit a 1-3 frame "muzzle-prep" flash only. |
| **Anchor** | Caster sprite origin (`entities` layer coordinate). VFX Container must track caster position if cast_time > 0.1s (the caster can be repositioned by a knockback mid-cast; the cast-charge should follow or snap-cancel). |
| **Layer** | `particles` layer, BEHIND caster entity in Z-order. Implemented as a `particles` sub-container rendered before `entities` re-addition, OR as a separate VFX injected at `entities` z-index - 1 (to-be-resolved at VS2a integration). |
| **Sprite vs procedural** | Procedural acceptable for VS2a (radial glow Graphics object scaled to element color). Pimen asset preferred when available — cast-charge from `aura_radial` pack subset (the "charging" frame range of an aura animation). |
| **Substrate-tag target** | `<element>-cast-charge` (e.g., `fire-cast-charge`, `water-cast-charge`). One per canonical-7 element. For physical archetypes: `physical-cast-charge` (melee stance). |
| **Loop behavior** | Loop ON during cast_time; terminate on skill-released OR interrupted. Must be interruptible mid-loop cleanly (pool.release() must not leave a zombie AnimatedSprite). |
| **Archetypes that skip this slot** | Instant-cast `primary_attack` skills in hunter / rogue (e.g., ranged auto-fire) may use a minimal 2-frame muzzle-flash variant rather than a sustained cast-charge. |
| **VS2b forward hook** | Per-embodiment narrative-skin: the "charging moment" for a non-humanoid form (e.g., Slime swelling, Spider raising forelegs) is character-animation territory, not VFX territory. Slot A for non-humanoid is thin (element-glow only; character animation owns the preparation gesture). |

---

#### Slot B: Projectile / movement

| Property | Constraint |
|---|---|
| **What it is** | In-flight visual for skills with a travel leg: projectile moving toward a target, dash-arc of the caster, or beam channel from caster to impact point. |
| **Applies to** | `projectile_straight` (mage/caster/hunter/rogue), `beam_channel` (hybrid_mage), `dash_attack` + `defensive_dash` (rogue/hunter/skirmisher). Does NOT apply to instant-delivery geometries (`impact_burst`, `nova_radial`, `ground_targeted_circle`). |
| **Duration** | Travel-time-bound: `range / speed` engine fields. Typical: 0.1–0.5s for melee range; 0.3–1.2s for max-range projectile. Beam_channel: sustain duration, 0.5–2s. |
| **Anchor** | Moving: projectile Container translates from `fromX/fromY` to `toX/toY` each frame via `tickProjectiles()`. Current demo implementation moves a Graphics-drawn circle; Pimen sprite replaces the circle primitive. |
| **Layer** | `particles` layer, ABOVE arena floor but BELOW entity sprites (so a projectile travels "through" the world plane rather than over the caster). Z-index between `bg` and `entities`. |
| **Sprite vs procedural** | Sprite preferred (the "in-flight" frame of a spell-effect pack). Typically 1–4 looping frames from the projectile sub-animation. The Pimen `projectile` and `bullet` mechanic-tagged assets are the catalogue source. |
| **Substrate-tag target** | `<element>-projectile` for straight projectile; `<element>-beam` for channel; `<element>-dash-trail` for movement. Physical: `physical-projectile` (arrow/bolt), `physical-dash-trail` (motion blur). |
| **Loop behavior** | Loop ON while in flight; STOP on arrival (replaced by Slot C impact). The transition from B → C must be frame-exact to avoid visual double-flash. In practice: when `tickProjectiles` calls the impact handler, it despawns the Slot B sprite in the same tick and spawns the Slot C impact. |
| **Special: beam_channel** | Beam is rendered as a STATIC sprite (or tiled repeat) between two anchor points, not a moving object. Pixi Graphics `moveTo/lineTo` with a custom GLSL shader is the correct path for non-trivial beams; a simple sprite strip (repeated texture at fixed intervals) is acceptable for VS2a. |
| **Special: dash_attack / defensive_dash** | The caster entity moves, leaving a "trail" — this is the Slot B visual for dash geometries. Trail is typically a fading alpha of the caster's sprite (or a motion-blur smear). Pimen `smear` tag is the catalogue source. NOT the same as a projectile. |
| **VS2b forward hook** | For non-humanoid embodiments: the "dash trail" visual depends on the creature's silhouette (a Slime's dash leaves a different trail than a humanoid's). Tag: `<element>-<embodiment>-dash-trail` (VS2b schema; VS2a uses `<element>-dash-trail` only). |

---

#### Slot C: Impact

| Property | Constraint |
|---|---|
| **What it is** | Hit-resolution visual at the target's position (or AOE center): the "strike landed" moment. Explosion burst, slash flash, energy wave, terrain slam. |
| **Applies to** | ALL skills that deal damage or apply control. This is the most visually load-bearing slot — the player's primary hit-confirmation read. |
| **Duration** | Short: 0.15–0.5s. One-shot (play once and despawn). For AOE skills, the impact may play simultaneously at multiple positions (per-target instance) or as a single centered radial (per-geometry). |
| **Anchor** | Target position (`tx, ty` from the engine hit event). For AOE radial skills: the AOE center coordinate. For `cone` and `ground_slam_directional`: the center of the cone's arc or the slam's forward point. |
| **Layer** | `particles` layer, ABOVE entity sprites at peak frame (the brightest frame should read over the caster/target). Fade frames drop below entities. Sub-layering within `particles` needed: a `particlesBelow` / `particlesAbove` split, where impact-peak frames use `particlesAbove` and fade frames use `particlesBelow`. |
| **Sprite vs procedural** | Sprite required for VS2a — this is the visible frame the player reads as "hit confirmed." The demo currently uses procedural `hitFlashes` (Graphics circles); Pimen `impact` / `explosion` / `hit-effect` mechanic-tagged assets replace these. |
| **Frame discipline** | The "peak impact frame" (the brightest, most readable frame) must land on frame 1 or 2 of the animation, not after a build-up. Pimen's `impact` packs generally respect this (most are front-loaded). Verify at acquisition: if a pack has a 3-5 frame build-up before the peak, it is NOT suitable for Slot C (it reads as a delayed hit, not a crisp hit-confirm). |
| **Substrate-tag target** | `<element>-impact` for direct-hit skills; `<element>-aoe-impact` for AOE radial skills; `physical-impact` for melee; `physical-slash` for melee-arc. Sub-tags needed: `fire-impact`, `water-impact`, `earth-impact`, `wind-impact`, `lightning-impact`, `holy-impact`, `shadow-impact`. Physical sub-tags: `physical-impact`, `physical-slash`, `physical-slam`. |
| **AOE scaling note** | For large AOE radials (radius > 150 demo-px), the impact sprite must scale. Do NOT use `Transform.scale` on a single-canvas animation without first verifying canvas_width at the intended scale. Pimen's `impact_burst` packs (many at 64×64 canvas) will pixelate at 3× scale. The correct path for large AOEs: source a larger-canvas asset OR use a tiled/layered multi-instance ring pattern (existing `aoeRings` pool) as the outer ring and a single impact at center. |
| **VS2b forward hook** | Per-embodiment impact skins: a Slime taking a fire hit receives a `fire-impact-slime` override (bubbling scorch rather than standard explosion). Tag structure: `<element>-impact-<embodiment>`. VS2a: single skin only. |

---

#### Slot D: Status-application

| Property | Constraint |
|---|---|
| **What it is** | The visual moment when a status effect attaches to the target: a brief overlay flash or ring that confirms "ailment applied." Distinct from the ongoing Slot E ambient. |
| **Applies to** | Skills with `control` role (controller archetypes) that apply ailments (stun, root, slow, burn DoT, etc.). Also: `damage_over_time` skills (fire_mage burn tick, shadow DoT). |
| **Duration** | Very short: 0.1–0.3s. One-shot, concurrent with the tail of Slot C. Slot D fires immediately after Slot C peak; the player reads "hit + ailment applied" as a single compound event. |
| **Anchor** | Target position, same as Slot C. If multiple targets receive the ailment simultaneously (AOE controller skill), one Slot D instance per target. |
| **Layer** | `particles` layer, ABOVE entity sprites. Rendered slightly after Slot C (1 frame delay) so the status ring appears to emerge from the impact flash. |
| **Sprite vs procedural** | Sprite preferred. The Pimen `buff`/`debuff`/`status-effect` packs are the catalogue source. The `debuff` packs apply here — they are "application" animations (a ring, swirl, or overlay appears on the target). |
| **Substrate-tag target** | `<element>-status-apply` for elemental ailments (fire: burn-apply, water: slow-apply, earth: root-apply, wind: knockback-apply, lightning: stun-apply, holy: blind-apply, shadow: curse-apply). `physical-status-apply` for control-with-ailment (grappler `require_control_with_ailment` constraint). |
| **Register-fence note (Sub-decision A)** | The status-application VFX is a VISUAL SUBSTRATE signal — it uses canonical-7 element vocabulary in the sprite substrate-tag, NOT per-season vocabulary. The LLM-authored skill name that appears in the combat log at this moment uses per-season vocabulary. The VFX asset catalogue is indexed by canonical-7 substrate tag only. This register-fence is load-bearing for the attribution pipeline. |
| **Concurrency** | A target may receive multiple ailments simultaneously (multi-ailment controller skill). Each ailment fires its own Slot D instance. The `spriteVfx` pool handles concurrent AnimatedSprites at the same position — no special de-dup needed, but visual stacking must be tested: 3 status-apply rings at the same (x,y) must read as distinct, not as a combined blob. Spacing offset (~8px radial jitter) recommended at integration. |
| **VS2b forward hook** | Control ailment secondary-damage signatures (`project_ailment_damage_thematic.md` — DEFERRED per `680a3f1`). If that design lands post-B14.5, Slot D may need to split into "ailment application + secondary-damage flash" as a compound event. No action at VS2a. Tag: `<element>-status-apply-secondary` reserved. |

---

#### Slot E: Status-ambient

| Property | Constraint |
|---|---|
| **What it is** | The ongoing visual while a status effect persists on the target: slow-pulse, aura tint, particle emission above the afflicted entity. Confirms to the player that the ailment is still active. |
| **Applies to** | All control ailments (stun, root, slow, burn DoT, etc.) that have non-zero duration. The `aura_radial` and `ambient` mechanic-tagged packs in the Pimen catalogue are the source material. |
| **Duration** | Matches ailment duration from the engine. Typical: 1–4s. Must sustain at loop for the full duration and terminate cleanly on ailment-clear. |
| **Anchor** | Target position, updated per frame (the afflicted enemy may still move while slowed/rooted — the ambient must track). For rooted targets: fixed anchor is fine. For slowed targets: the ambient Container must follow the entity's current position. |
| **Layer** | `particles` layer, BELOW entity sprites for ambient halos (a burn aura below the target reads as "ground fire"), ABOVE entity sprites for debuff overlays (a frost lattice over the target reads as "frozen"). Two sub-layers needed within `particles`: `particlesGroundLevel` (below entities) and `particlesOverlay` (above entities). |
| **Sprite vs procedural** | Sprite strongly preferred — this is a sustained visual and procedural particles (Graphics) will produce Z-fighting artifacts if not managed. The Pimen `buff`/`debuff`/`status-effect` packs' looping animations are intended for this slot. Catalog observation: these packs have high animation-frame-density (Pimen's buff/debuff packs have 9 assets with `status-effect` tags) — well-suited for sustained loop. |
| **Substrate-tag target** | `<element>-status-ambient` per ailment family: `fire-burn-ambient`, `water-slow-ambient`, `earth-root-ambient`, `wind-knockback-ambient` (brief; most wind ailments are short-duration), `lightning-stun-ambient`, `holy-debuff-ambient`, `shadow-curse-ambient`. Physical: `physical-stun-ambient` (stagger stars). |
| **Performance discipline** | If 4-6 enemies in a room are simultaneously rooted/burned/slowed, the `status-ambient` slot will have 4-6 concurrent AnimatedSprites. At 12.5fps each with typical Pimen 9–17 frame cycles: ~12-17 texture-object updates per frame. This is within budget but is the slot most likely to cause performance pressure at pack-content density. **Rule: status-ambient sprites must use the same Texture atlas across all instances of the same ailment type** (e.g., all `fire-burn-ambient` instances pull from the same loaded spritesheet, not re-loaded per instance). Pixi's texture cache handles this automatically if loaded once via `Texture.from()`. |
| **Termination discipline** | When ailment clears (engine `ailment_cleared` event), the Slot E AnimatedSprite must despawn cleanly. A brief 2-4 frame "dissipate" animation is preferred to abrupt pop-off — the `spriteVfx` pool's on-complete handler should trigger the dissipate variant rather than immediate pool.release(). **TODO(drax): dissipate variant support is not yet in `spriteVfx` pool — add at B11 integration.** |
| **VS2b forward hook** | Per-embodiment ailment rendering: `fire-burn-ambient-slime` (Slime burns differently than humanoid). Tag structure reserved. VS2a: single skin only. |

---

#### Slot F: Skill-expired / cooldown-feedback

| Property | Constraint |
|---|---|
| **What it is** | Optional sixth slot — a brief visual at the caster confirming the skill has finished executing and the cooldown has begun. Not a hit-confirm (that is Slot C). Not a status (that is Slots D/E). This is "your skill is now on cooldown" feedback. |
| **Applies to** | High-visual-impact skills where the player must know the skill window has closed: `burst_damage` finisher skills, long-cooldown `area_damage` nukes, `defensive` skills (the player needs to know dash is now cooling). |
| **Duration** | Very short: 0.05–0.2s. Minimal — one-shot at caster position. |
| **Anchor** | Caster position. |
| **Layer** | `particles` layer above entities (brief overhead flash at caster). |
| **Sprite vs procedural** | Procedural acceptable (a single-frame "puff" of element-colored particles). Sprite overkill for VS2a. |
| **Substrate-tag target** | Not a hard substrate tag requirement for VS2a. Mark as `<element>-skill-expired` if a Pimen asset naturally fits. Low priority for VS2a first integration — the `DashCooldownHud` HUD element (shipped at drax/v1.4) provides the primary cooldown read; Slot F is a secondary reinforcement. |
| **Rationale for inclusion** | Surfaced by gandalf's VFX design notes in `canonical/story/court-of-forms.md` context: the player needs clear "skill-window-open vs closed" legibility particularly on the burst archetypes. The HUD radial sweep handles this for the active player skill; Slot F handles it for the player's observed cooldown on NPC combat (the player watching an enemy burst-mage needs to know when the burst window resets). |
| **VS2b forward hook** | Cooldown feedback on enemy archetypes is a VS2b narrative-skin concern: a Dragon-Hatchling mage's cooldown tells a different story than a humanoid mage's. Slot F for VS2a = minimal / procedural. |

---

### 2.3 — Slot activation matrix by archetype family

Which slots fire, in what sequence, per archetype family aggregate.

| Archetype family | Slot A (cast-charge) | Slot B (projectile/movement) | Slot C (impact) | Slot D (status-apply) | Slot E (status-ambient) | Slot F (expired) |
|---|---|---|---|---|---|---|
| **Elemental mage** | YES — full sustained | YES — projectile | YES — impact burst | Rare (only if skill has ailment) | Rare (only if DoT) | YES on burst finisher |
| **Elemental caster** | YES — full sustained | No (instant AOE delivery) | YES — AOE impact | No (damage only) | No | YES on major AOE |
| **Elemental controller** | YES — brief (cast_time short) | Situational (vortex_pull has travel; most control is instant) | YES — impact flash | YES — per ailment applied | YES — per ailment sustained | YES on control finisher |
| **Physical warrior / grappler** | YES — brief stance (melee windup) | No (melee range delivery) | YES — slash/slam impact | YES (grappler: `require_control_with_ailment`) | YES (grappler only) | Optional |
| **Hunter** | Minimal (auto-attack: muzzle flash only) | YES — arrow/bolt projectile | YES — impact burst | No | No | No |
| **Rogue** | Minimal | YES — dash trail | YES — impact at end of dash | No (rogue is damage only at current templates) | No | No |
| **Hybrid mage** | YES — full sustained | YES — beam channel (sustained; Slot B and Slot C are concurrent for beam skills) | YES — AOE impact | YES (DoT slot: damage_over_time role) | YES (DoT sustained) | YES |

---

### 2.4 — Timing and sequencing constraints

**Tick-accuracy requirement:** Slots C and D fire in the same tick as the engine's hit event. The engine emits `skill_hit` events which drax consumes; the slot C+D spawn must happen in the event handler, not deferred by a setTimeout or next-tick. Current `vfxPools` architecture handles this correctly (direct push into pool in the event handler).

**Overlap discipline — Slot A and Slot B:**
- For projectile skills: Slot A plays at caster → Slot A terminates → Slot B spawns at caster position and travels → Slot B terminates at target → Slot C spawns at target.
- For instant AOE: Slot A plays at caster → terminates → Slot C spawns at AOE center simultaneously.
- For beam skills: Slot A plays at caster → Slot B (beam strip) appears spanning caster to target, sustained → Slot C plays at target position during beam sustain.

**Overlap discipline — Slot C and Slot D:**
- Slot D fires 1 frame after Slot C peak. In practice: push Slot D into pool 1 frame delayed (via a 1-frame counter in the event handler, or simply spawn both simultaneously and rely on Slot D's brief build-up frame to create the natural offset).

**Overlap discipline — Slot E and Slot D:**
- Slot E spawns on Slot D complete (or shortly after Slot D's one-shot animation finishes). The `spriteVfx` pool's `onComplete` callback is the hook: Slot D's AnimatedSprite's onComplete spawns the Slot E loop. **This is the primary integration pattern for the controller archetype VFX chain.**

**Slot E termination:**
- Engine emits `ailment_cleared` (or ailment duration expires per engine tick). Slot E AnimatedSprite switches to dissipate variant OR crossfades to invisible over 2-4 frames. The `spriteVfx` pool needs a `releaseWithFade(frames)` method. Currently unimplemented — **TODO(drax): add releaseWithFade() to spriteVfx pool at B11 integration.**

---

### 2.5 — Physical archetype VFX notes (distinct from elemental)

Physical archetypes (warrior/grappler/skirmisher/hunter/rogue) have no element substrate but their VFX slots still require substrate-tagged assets. The physical substrate-tags are:

- `physical-cast-charge` — melee stance/windup (brief; 0.1-0.2s for most melee)
- `physical-projectile` — arrow/bolt (hunter only)
- `physical-impact` — generic strike burst
- `physical-slash` — for melee_arc geometry (the blade-arc flash)
- `physical-slam` — for ground_slam_directional (grappler, physical_warrior)
- `physical-status-apply` — for grappler control ailments
- `physical-stun-ambient` — for grappler stun

**Gap note (from catalogue pre-inventory § 3.4):** The only physical impact/slash assets in the current Pimen catalogue (`pixel-battle-effects`, `cutting-and-healing`) carry CC-BY attribution. If drax-side consumption avoids attribution-required assets, physical impact and slash mechanic coverage in the catalogue collapses to zero. Flag for elrond Pimen subset selection dispatch: the `physical-slash` and `physical-impact` substrate-tags have no attribution-free coverage in the current catalogue. A vendor sweep or additional Pimen acquisition that addresses physical impacts without CC-BY constraint is needed before B11 physical-archetype integration.

---

### 2.6 — Composite-skill VFX (leap_strike and beam_channel)

These two geometry types require composite Slot B rendering — two simultaneous VFX components in the same slot.

**leap_strike (physical_warrior):**
- Slot A: standard melee windup at caster
- Slot B: character leap-arc animation (character-track, NOT a VFX sprite — this is the animated character entity traveling from origin to target; the VFX component is a `physical-dash-trail` or dust-cloud emitted along the arc)
- Slot C: `ground_slam` impact VFX at landing point (Pimen earth/fire/physical slam assets are the source)
- Per `geometry-vfx-coverage-assessment.md` § 2, this composite path (leap arc + ground_slam VFX) is the approved VS2a rendering strategy for leap_strike. Drax wires the composite.

**beam_channel (hybrid_mage):**
- Slot A: standard mage cast-charge at caster
- Slot B: beam strip (static sprite or tiled repeat between caster and target positions; rendered for the full channel duration)
- Slot C: concurrent with Slot B — ongoing `<element>-impact` flash at the target end of the beam, ticking at beam-tick-rate (NOT at 12.5fps — at the engine's DoT tick rate, typically 1/s)
- The Slot B/C overlap for beam is the only case where C is sustained rather than one-shot. Implementation note: spawn C as a LOOPING AnimatedSprite at the target position with loop=true during beam sustain; despawn both B and C simultaneously on beam expiry.

---

### 2.7 — Sub-layer requirement (particles container)

Current `_layers.particles` is a flat Container. VS2a first VFX integration requires partitioning it into at minimum three sub-layers:

```
_layers.particles
  └─ particlesGround   (z: below entities — Slot E auras that read as floor halos)
  └─ particlesMid      (z: same level as entities — Slot B projectiles in flight)
  └─ particlesOver     (z: above entities — Slot C impact peaks, Slot D status rings)
```

**Implementation note:** Pixi renders Container children in insertion order. To achieve these three z-levels relative to `entities`, the options are:
- (A) Split `particles` into `particlesUnder` + `particlesOver` on either side of `entities` in `app.stage.addChild()` order — simplest; covers 90% of cases.
- (B) Add `particlesMid` between under and over — needed for projectile-travels-through-world reading.
- (C) Dynamic z-sort per frame (expensive; not recommended).

**VS2a recommendation: Option (A) minimum — split particles into under/over around entities. Adds particlesMid as a VS2a first-integration deliverable if projectile depth reads incorrectly without it.** This is a ~1-hour refactor of `stage.ts` and `main.ts` + all vfxPools spawn logic.

**TODO(drax): layer split is a prerequisite for correct Slot C (impact above entity at peak, below on fade) and Slot E (aura ground halos below entity). File as VS2a first-integration step 0, before any Pimen sprite integration begins.**

---

### 2.8 — Sprite-vs-procedural summary per slot

| Slot | VS2a target | Rationale |
|---|---|---|
| A — cast-charge | Procedural acceptable (element-color radial glow) | Short duration; low visual bandwidth; Pimen aura-subset assets are a bonus not a requirement |
| B — projectile | Sprite preferred | The "flying spell" is the archetype's primary identity visual |
| B — dash trail | Procedural acceptable (fading caster-sprite alpha) | Character-track problem; VFX is secondary |
| B — beam | Sprite tiled strip | Procedural line would not match HD-2D register |
| C — impact | Sprite required | Primary hit-confirm; must match element substrate exactly |
| D — status-apply | Sprite required | Ailment confirmation; Pimen buff/debuff packs purpose-built for this |
| E — status-ambient | Sprite required | Sustained loop; procedural particles create Z-fighting at density |
| F — expired | Procedural acceptable | Secondary feedback; HUD carries primary cooldown read |

---

### 2.9 — VS2b forward-looking render hooks

Per Sub-decision C = Option II, these hooks are enumerated now and marked as NOT implemented at VS2a:

1. **Per-embodiment impact skins** (`<element>-impact-<embodiment>`): Slot C rendering switches asset based on target's `embodiment_tag`. VS2a: no per-embodiment switch (single skin per element). Hook: `getImpactAsset(element, embodiment)` lookup table in the attribution pipeline; VS2a implementation uses `getImpactAsset(element, 'humanoid')` always.

2. **Per-season vocabulary isolation** at VFX surface: the VFX assets are indexed by canonical-7 element substrate tags. Season-authored skill names (LLM-generated per-season vocabulary) appear ONLY in combat-log text, tooltips, and hotbar labels — never as a lookup key into the VFX catalogue. This register-fence is structural in the attribution pipeline schema. VS2a and VS2b both enforce it; it is not a VS2b addition.

3. **releaseWithFade() for Slot E termination:** a clean dissipate animation variant per ailment. Pimen buff/debuff packs may include dissipate variants in their animation set — elrond should flag this at subset selection. **TODO(drax): remove this TODO when dissipate-variant support lands in spriteVfx pool.**

4. **Atlas consolidation:** VS2a attribution is ad-hoc (one asset per slot, loaded independently). VS2b attribution pipeline consolidates element-substrate VFX into atlas textures to reduce texture swaps. The VS2b schema should define an `atlas_group` field on catalogue rows that guides elrond's subset selection toward atlas-eligible packs. Hook: `metadata.json` schema extended with `atlas_group` field (VS2b ingest pipeline task).

5. **Character-animation track (Slot B dash-trail + leap_strike arc):** physical archetype movement VFX is currently the caster-entity's sprite. VS2b per-embodiment rendering requires character-animation primitives (Mixamo / Spine rigs) to replace the sprite-translation. Slot B for physical archetypes is a character-animation concern, not a VFX-catalogue concern, and is fully out of scope for both Pimen subset selection and the current VS2a VFX integration.

---

*Section 2 authored by drax, 2026-05-17. Sections 1/3/4/5 pending gandalf.*

---

## Section 3 — Substrate-tag inventory needed (gandalf cross-vendor evidence target)

**(Pending — gandalf parallel session)**

---

## Section 4 — Per-encounter scene-walkthroughs (VS2b forward-looking, per Sub-decision C = Option II)

**(Pending — gandalf parallel session)**

---

## Section 5 — Open questions surfaced by the spec

**(Pending — gandalf parallel session; drax open questions embedded in Section 2 via TODO(drax) annotations and § 2.5 CC-BY gap note)**

---

## Completion record

**(To be filled in jointly on full spec completion)**

**Completed:**
**Spec path:**
**Encounter types enumerated:**
**VFX slots enumerated:**
**Substrate-tag inventory size:**
**Gaps flagged (count):**
**Section 4 (VS2b forward-looking) status:** included (per Sub-decision C = Option II)
**Open questions parked (count):**
**Notes for knight-rider:**
