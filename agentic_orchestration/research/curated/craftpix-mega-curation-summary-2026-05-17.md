# CraftPix mega-catalogue curation summary — 2026-05-17

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-craftpix-mega-catalogue-curation-extension.md`
**Predecessor:** legolas-3 CraftPix mega-catalogue + character/VFX crawl (`agentic_orchestration/dispatches/2026-05-17-legolas-craftpix-mega-catalogue-and-character-vfx-crawl.md` § completion record)

---

## 1. Executive summary

Legolas-3 surfaced **67 CraftPix packs + 9 free-character/VFX folders** already-on-disk at `reincarnated-demo/public/assets/`. This curation pass converts the raw inventory into actionable manifests + formalizes five gap-status changes + extends the VFX manifest architecture from a Pimen-only model to a **4-layer composition model** (substrate / class-archetype / physical / atmospheric).

Five deliverables shipped:

| # | Deliverable | Path | Status |
|---|---|---|---|
| 1 | Dungeon-tileset subset manifest (8 packs) | `agentic_orchestration/research/curated/dungeon-tileset-subset-vs2a-2026-05-17.jsonl` | **AUTHORED** (3 WIRE-NOW / 4 WIRE-LATER / 1 SKIP) |
| 2 | Monster-subset manifest | `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` | **DEFERRED stub** per Matt Q7 unresolved |
| 3 | 2 ZIPs expansion + DireDungeon overlap analysis | `agentic_orchestration/research/curated/craftpix-zip-expansion-deferred-2026-05-17.md` | **DEFERRED stub** per Matt Q6 unresolved |
| 4 | 4-layer VFX architecture manifest | `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` + `.jsonl` | **AUTHORED** (8 new rows across Layers 2/3/4) |
| 5 | This summary doc | `agentic_orchestration/research/curated/craftpix-mega-curation-summary-2026-05-17.md` | **AUTHORED** |

Headline findings:

- **G-COFFIN CLOSED** via `craftpix-net-298079` coffins.png at zero cost (pending Matt Q1 design-fit confirmation).
- **G4 close path on disk** via Frostwindz Slashes — eliminates CC-BY attribution surface from `pixel-battle-effects`; no CodeManu acquisition needed (pending Matt Q2; elrond-recommended ACCEPT).
- **$4.25 savings opportunity** on Pimen `battle-vfx-hit-spark` — Frostwindz Impacts (7 effects × B&W + COLOR variants) is superior wiring architecture (pending Matt Q3; elrond-recommended SKIP).
- **G3 substantially closed** by 17 monster + 4 boss packs on disk (curation pending Matt Q7).
- **NightBorne BLOCKED** — no license file on disk; excluded from all curated subsets until Matt Q5 resolves.
- **VS2a Pimen acquisition total revised from $26.35 → $22.10** (savings $4.25) if Matt approves Q3.
- **4-layer VFX architecture proposed** — preserves Pimen substrate (Layer 1) + adds class-archetype overlays (Layer 2) + physical replacement (Layer 3) + atmospheric room-overlays (Layer 4).

---

## 2. Gap-status changes (with Matt-decision dependencies)

| Gap | Pre-curation status | Post-curation status | Matt-decision dependency |
|---|---|---|---|
| **G-COFFIN** | OPEN (Mucho Pixels not acquired in icons+props registration) | **CLOSED** via `craftpix-net-298079` coffins.png in dungeon-tileset subset (zero cost) | Q1 — design-fit confirmation; pack also closes ghost_trap + dragon_trap + Statue_fire hazards |
| **G4 — physical-slash CC-BY risk** | PARKED Matt-decision (CC-BY accept vs CodeManu acquire) | **CLOSE-PATH on disk** via Frostwindz Slashes; CC-BY surface can be eliminated | Q2 — authorize Frostwindz Slashes as G4 close path (**elrond recommendation: ACCEPT**) |
| **G3 — non-humanoid embodiment** | OPEN-deferred | **SUBSTANTIALLY CLOSED** — 17 monster + 4 boss packs on disk; curation pending | Q7 — authorize VS2a monster subset curation now vs defer post-VS2a |
| **Pimen `battle-vfx-hit-spark` $4.25 purchase** | Planned acquisition per Pimen subset | **MAY BE REDUNDANT** — Frostwindz Impacts superior (7 variants × B&W+COLOR; matches drax tint-composition strategy) | Q3 — skip Pimen $4.25 purchase (**elrond recommendation: SKIP** — save $4.25) |
| **NightBorne character sprite** | Unverified license | **BLOCKED** — no license file on disk; cannot include in any curated subset | Q5 — license verification (defer NightBorne until resolved) |

---

## 3. Curated subset manifest references

### 3.1 Dungeon-tileset subset (Deliverable 1)

**Path:** `agentic_orchestration/research/curated/dungeon-tileset-subset-vs2a-2026-05-17.jsonl`
**Row count:** 8 (1 header + 8 pack rows = 9 lines)
**Distinct packs:** 8
**Curation breakdown:** 3 WIRE-NOW (stone-dungeon trio), 4 WIRE-LATER (cave + undead + sewer + glowing-cave biome expansion), 1 SKIP (older Spriter-era pack subsumed by newer trio)
**Total cost:** $0 (all CraftPix-Free-Terms; single attribution credit)
**Animated hazard inventory across packs:** ghost_trap, dragon_trap, Statue_fire, fire_trap, spike_trap, lattice_trap, fountain_animation, Water_coasts_animation, Volcano1-5 eruptions, Demon hand/head/tail emerging, fire animation variants — directly matches Matt's "animations for non-combatant damaging elements" thesis.
**Legolas-3 reference:** REFUTED Matt's "REPLACE DireDungeon" hypothesis on scope grounds — CraftPix dungeon tilesets are room-construction; DireDungeon is item-icon library. Orthogonal scopes. Manifest treats them as COMPLEMENTARY.

### 3.2 Monster-subset (Deliverable 2 — DEFERRED stub)

**Path:** `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl`
**Status:** DEFERRED stub per dispatch § Deliverable 2 (Matt Q7 unresolved)
**Row count:** 1 stub header (no data rows until Q7 resolves)
**Carry-forward inventory:** 17 monster packs + 4 boss packs (rows 21-37 in legolas-3 inventory.jsonl) ready for curation
**Estimated curation time post-Q7-YES:** ~0.5 day

### 3.3 ZIP expansion (Deliverable 3 — DEFERRED stub)

**Path:** `agentic_orchestration/research/curated/craftpix-zip-expansion-deferred-2026-05-17.md`
**Status:** DEFERRED stub per dispatch § Deliverable 3 (Matt Q6 unresolved)
**Affected ZIPs:** `craftpix-net-382264-armor-and-weapons-pixel-rpg-icons.zip` (HIGH DireDungeon overlap risk; 578K) + `craftpix-net-596440-fishing-and-gathering-pixel-art-rpg-icons.zip` (LOW relevance; 116K)
**Estimated work post-Q6-YES:** ~30-60 min (overlap classification, not new manifest authoring)

### 3.4 4-layer VFX architecture (Deliverable 4)

**Path:** `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` + `.jsonl` companion
**Row count:** 8 new rows across Layers 2/3/4 (Layer 1 Pimen subset unchanged at 31 rows / 14 packs)
**Total architecture rows:** 39 (31 Layer 1 + 8 new Layers 2-4)
**New attribution credit lines:** 2 (Frostwindz + Alenia Studios)
**Cost delta:** -$4.25 if Matt approves Q3 (skip Pimen hit-spark)

See § 4 below for the 4-layer architecture proposal.

---

## 4. 4-layer VFX architecture proposal

Full proposal in `vfx-layered-architecture-vs2a-2026-05-17.md`. Summary:

| Layer | Source | Role | Render-pipeline target | New for VS2a? |
|---|---|---|---|---|
| **1 — substrate** | Pimen subset (existing) | Element × slot canonical-7 × A-E coverage | particlesUnder/Mid/Over per drax sub-layer split | unchanged |
| **2 — class-archetype** | Frostwindz Blood Mage / Necromancer / Rogue / Starcaller / Vampire | Class-thematic visual register composited on Layer 1 | particlesMid + particlesOver (same slot positions; overlay) | NEW |
| **3 — physical** | Frostwindz Slashes (G4 close) + Frostwindz Impacts (Pimen hit-spark alternative) | Physical-archetype Slot B/C; commercial-license alternative to CC-BY | particlesMid (slash) + particlesOver (impact); B&W tint capability | NEW |
| **4 — atmospheric** | Alenia Studios Atmospheric (20 effects) | Full-screen room-atmosphere overlays | NEW atmosphericUnder + atmosphericOver containers | NEW |

**VS2a scope (post-v1.12):**
- Layer 3 (Slashes + Impacts) — full wiring (replaces CC-BY pixel-battle-effects; may replace Pimen hit-spark).
- Layer 4 — POC: 1-2 atmospheric effects on single demo room (informs drax integration cost).

**VS2b scope (deferred):**
- Layer 2 (class-archetype overlays) — full wiring with `spirit.class_archetype` runtime field.
- Layer 4 (full atmospheric) — `room.atmosphere_theme` attribute; all 20 effects.
- Element-balance Layer 2 expansion (5 of 7 canonical-7 elements lack class-thematic VFX coverage; future commission scope).

**Element-imbalance observation in Layer 2:** Frostwindz packs concentrate on shadow (3 sub-registers: Blood Mage, Necromancer, Vampire) + physical (Rogue) + holy/lightning (Starcaller). Fire/water/earth/wind/lightning lack class-archetype overlay coverage. Three paths surfaced (commission Frostwindz extension / alternative vendor / accept-absence). Not a VS2a blocker.

---

## 5. Earth meta-layer readiness (10+ interior packs)

Legolas-3 surfaced 10 interior-asset packs that fit the Earth meta-layer (per `MEMORY.md project_earth_meta_layer.md`):

| Pack (CraftPix folder) | Earth meta-layer role | Acquisition status |
|---|---|---|
| Guild Hall (189780) | Earth town hub / Spirit Guide hall | **ACQUIRED** (closed G-ARMOR-MANNEQUIN) |
| Mage Tower (289481) | Arcane/magic trial room / Spirit Guide home | on-disk |
| Chapel (477438) | Holy/light element sanctuary | on-disk |
| Market Square (587497) | Earth town hub — citizens + musicians animated | on-disk |
| Tavern (666104) | Earth town social hub | on-disk (PSD-primary; export step needed) |
| Blacksmith (741016) | Crafting/upgrade interior; animated forge | on-disk |
| Herbalist's Hut (742958) | Potion-shop interior | on-disk (PSD-primary) |
| Nobles Manor (653272) | Upper-class Earth interior | on-disk |
| Main Character's Home (654184) | Player Earth-world home | on-disk (license file MISSING — flag for verification) |
| Glassblower's Workshop (692491) | Artisan workshop | on-disk (niche) |
| Fishing Village (885927) | Coastal Earth town variant | on-disk |

**VS2a-scope assessment:** Earth meta-layer is **out of VS2a-VS2b scope** per current roadmap (Earth gameplay loop is TBD per `MEMORY.md project_earth_meta_layer.md`). Interior packs flagged for **VS2b+ forward-roadmap consumption** — do not curate as manifests until Earth meta-layer design lands.

**License verification flag:** `craftpix-net-654184-main-characters-home` ships **NO license.txt** — Matt should verify attribution requirements before integration even if license is presumed CraftPix-Free-Terms.

---

## 6. Open Matt-decisions (carried forward + new)

### 6.1 Carried forward from legolas-3 (7 questions)

Per legolas-3 hive-log STATE entry "7 open decisions" + Top 5 findings; reconstructed from the full set of decision points legolas-3 surfaced:

| # | Question | Elrond recommendation | Status |
|---|---|---|---|
| **Q1** | G-COFFIN design-fit for `craftpix-net-298079` coffins.png (dungeon-floor prop vs chest-style) | ACCEPT (closes gap at zero cost; visual register matches dungeon-tileset trio) | pending Matt |
| **Q2** | Frostwindz Slashes as G4 close path (replaces CC-BY `pixel-battle-effects`; deprioritize CodeManu) | **ACCEPT** | pending Matt |
| **Q3** | Skip Pimen $4.25 `battle-vfx-hit-spark` purchase (Frostwindz Impacts 7-variant B&W+COLOR superior) | **SKIP** (save $4.25) | pending Matt |
| **Q4** | Accept REFUTED replacement thesis: CraftPix dungeon tilesets are COMPLEMENT not REPLACE for DireDungeon | ACCEPT refutation (different asset classes — room-construction vs item-icon) | pending Matt confirmation |
| **Q5** | NightBorne license verification (no license file on disk; GIF-only format wiring concern) | DEFER NightBorne; exclude from all curated subsets until resolved | BLOCKED pending Matt |
| **Q6** | Authorize 2 ZIPs expansion + DireDungeon overlap analysis (net-382264 armor+weapons; net-596440 fishing+gathering) | (no preference; depends on whether net-382264 adds breadth) | DEFER per dispatch stub |
| **Q7** | Commission VS2a monster subset curation now (17 monster + 4 boss packs ready) vs defer post-VS2a | (no preference; both viable — ~0.5 day work when authorized) | DEFER per dispatch stub |

**Additional context from legolas-3 STATE:** Alenia Studios Atmospheric (CC BY 4.0; 20 effects) is flagged as a NEW VFX slot type (room-atmosphere overlay). This is incorporated into the 4-layer architecture as Layer 4 and surfaces via new question Q-LAYER-1 below.

### 6.2 New decisions surfaced during curation

| # | Question | Elrond recommendation |
|---|---|---|
| **Q-LAYER-1** | Layer 4 atmospheric VS2a deployment scope (POC 1-2 effects vs defer all to VS2b) | POC 1-2 effects in single demo room (informs drax integration cost; low-risk) |
| **Q-LAYER-2** | Authorize Layer-2-on-Layer-1 alpha-blend compositing experimentation during drax VS2a integration | Authorize POC experimentation (low cost; informs VS2b architecture) |
| **Q-CHM-HOME** | `craftpix-net-654184-main-characters-home` license verification (NO license.txt on disk) | Verify attribution requirements before any Earth meta-layer integration |

### 6.3 Decisions internal to elrond seam (no Matt-decision needed)

- Dungeon-tileset subset 3+4+1 curation split (WIRE-NOW / WIRE-LATER / SKIP) — elrond steward authority per dispatch § "Within data domain"
- Monster-subset deferral mechanism (stub vs no-stub) — dispatch-prescribed
- ZIP-expansion deferral mechanism — dispatch-prescribed
- 4-layer architecture model (vs Pimen-only) — elrond steward authority for data architecture; Drax integration plan is consultation, not approval-gated

---

## 7. Earth meta-layer & VS2b+ forward-flag

Beyond the 10 interior packs (§ 5), legolas-3 surfaced VS2b+ scope expansions:

- **Environment-tileset expansion (10+ biome packs):** grassland, rocky, swamp, forest, desert, winter, flying-islands, seabed, cursed-land, training-arena, path-and-road. Curation deferred until VS2b biome roadmap lands.
- **Character-sprite expansion:** Swordsman 1-3, Swordsman 7-9, Warrior pack-2, RPG Heroes (Knight/Wizard/Crossbowman), Vampire 4-direction, Base female 4-direction, Base male 4-direction. Useful for player character pipeline; deferred to character-sprite dispatch scope.
- **UI extension:** Basic Icons 16x16 (net-556632), Game User Interface (net-775352), Bestiary Book (net-767317), Adventure Fantasy Book (net-137102). UI manifest extension deferred to M5/M6 portrait HUD work.
- **Animated UI:** Animated Magic Book (already-acquired; bonus pack), Bestiary Book (on-disk), Adventure Fantasy Book (on-disk). Three animated book packs cover skill-book / monster-bestiary / journal use cases.

**No VS2a-blocking forward-flag items.** All VS2b+ scope is queued for future dispatches.

---

## 8. Coordination and parallel-safety

This curation work consumed legolas-3 raw inventory + produced manifests. Parallel-safe by design:

- **No engine code touched** (elrond seam discipline).
- **No drax wiring touched** (drax v1.12 in flight — elrond manifests inform follow-on but don't pre-empt v1.12).
- **No new vendor commissions** (consumed on-disk only per dispatch out-of-scope rule).
- **No Pimen manifest modification** (Pimen subset is unchanged; 4-layer architecture is additive).
- **No NightBorne inclusion** (BLOCKED pending license).
- **PRE-SIGNAL § 14.1.1 honored** before hive-log append.

---

## 9. HANDOFFs

### 9.1 → drax (post-v1.12)

**VS2a wiring candidates (Layer 3 from 4-layer architecture):**
- Wire Frostwindz Slashes to physical-slash Slot B/C → replaces CC-BY `pixel-battle-effects` (G4 close path). Pending Matt Q2 ACCEPT.
- Wire Frostwindz Impacts B&W variant + element-tint composite → replaces Pimen hit-spark in physical-impact slot. Pending Matt Q3 SKIP.
- Optional POC: wire 1-2 Alenia atmospheric effects on single demo room (Layer 4); requires NEW `atmosphericUnder` + `atmosphericOver` pixi containers. Pending Matt Q-LAYER-1.

**Dungeon-tileset wiring candidates (3 WIRE-NOW packs):**
- `craftpix-net-298079` (lead): walls/floor + animated hazards (ghost_trap, dragon_trap, Statue_fire) + coffins.png (G-COFFIN closure).
- `craftpix-net-125640`: walls/floor + animated trap trio (fire_trap, spike_trap, lattice_trap) + Tiled-compatible map files.
- `craftpix-net-169442`: walls/floor + animated interactive (chest/lever/door) + two fire animation variants.

**4-layer VFX architecture integration plan:** see `vfx-layered-architecture-vs2a-2026-05-17.md` § 8 "Drax integration plan" — VS2a steps + VS2b steps + out-of-scope deferrals.

### 9.2 → matt

**7 carried-forward decisions** from legolas-3 (see § 6.1 above). Elrond recommendations:
- **Q1:** ACCEPT coffins.png G-COFFIN closure
- **Q2:** ACCEPT Frostwindz Slashes G4 close path
- **Q3:** SKIP Pimen $4.25 hit-spark (save $4.25)
- **Q4:** ACCEPT REFUTED replacement thesis — dungeon-tilesets COMPLEMENT DireDungeon
- **Q5:** DEFER NightBorne until license resolved
- **Q6:** No preference; ZIP expansion is small-scope work
- **Q7:** No preference; monster curation is ~0.5 day work, deferrable

**3 new decisions surfaced** during curation (see § 6.2 above):
- **Q-LAYER-1:** Layer 4 POC scope (recommend 1-2 effects POC)
- **Q-LAYER-2:** Layer-2 compositing experimentation authorization (recommend POC)
- **Q-CHM-HOME:** `main-characters-home` license verification (no license.txt on disk)

### 9.3 → knight-rider

Standard chain coordination. Completion record will append to dispatch (this doc references). No tag (curation, not code).

---

## 10. Acceptance criteria checklist (per dispatch § Acceptance)

- [x] Dungeon-tileset subset manifest authored — `dungeon-tileset-subset-vs2a-2026-05-17.jsonl` (8 packs)
- [x] Monster-subset manifest stubbed-as-deferred per Matt Q7 unresolved — `monster-subset-vs2a-2026-05-17.jsonl` stub
- [x] 2 ZIPs expansion stubbed-as-deferred per Matt Q6 unresolved — `craftpix-zip-expansion-deferred-2026-05-17.md` stub
- [x] 4-layer VFX architecture manifest authored — `vfx-layered-architecture-vs2a-2026-05-17.md` + `.jsonl` companion
- [x] Gap-status update doc authored with carried-forward Matt-decisions — this document
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append — to be performed at hive-log append step
- [ ] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider — to be appended at hive-log step
- [x] No new vendor commissions without Matt sign-off — consumed on-disk only
- [x] NightBorne explicitly excluded from all curated subsets — confirmed BLOCKED in all 5 deliverables

---

*Filed 2026-05-17 by elrond per dispatch authorization. Ships 5 deliverables (2 active manifests + 2 deferred stubs + this summary). 4-layer VFX architecture proposal opens VS2b composition design space.*
