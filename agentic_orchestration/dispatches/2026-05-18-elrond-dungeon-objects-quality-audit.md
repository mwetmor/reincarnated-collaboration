# 2026-05-18 — elrond — Dungeon-objects quality audit (stairs prioritized; all dungeon objects)

**Authority:** Matt L3 playtest 2026-05-18: *"the stairs sprite is a really bad choice. Generally all of the dungeon objects are poor."*
**Type:** Pattern A — quality audit + swap-candidate scout; ~45-60 min.
**Status:** 🟢 **ACTIVE — fire immediately. No-spend scout; uses already-acquired catalogues.**

---

## Why this matters

VS2a Final Sprint (drax v1.13) wired CraftPix dungeon tileset + ambient props (magic book / coffin / candles). The tileset includes stairs + chests + pots + decorations + floor-tiles + wall-deco. Matt's playtest verdict: quality is poor across the board — stairs called out specifically; everything else by inference.

Demo experience is materially degraded by low-quality static dungeon assets. The Reincarnated visual register is HYBRID a3 (per gandalf canon); dungeon objects need to fit Cluster A retro-pixel for register coherence. Goal: identify higher-quality alternatives from already-acquired packs, or flag specific acquisitions if no acceptable alternative exists.

---

## Required reading

1. **Drax v1.13 completion** — `agentic_orchestration/dispatches/2026-05-17-drax-vs2a-final-sprint-comprehensive-wiring.md` § completion (which CraftPix dungeon tileset was wired; ambient-prop pack origin)
2. **CraftPix mega-catalogue** — `agentic_orchestration/research/catalogue/craftpix-mega-catalogue-2026-05-17/` (legolas-3 crawl; full inventory of available CraftPix dungeon-object packs)
3. **CraftPix free-characters catalogue** — `agentic_orchestration/research/catalogue/free_characters_and_vfx/` (if applicable for dungeon objects)
4. **Icon + prop catalogue** — `agentic_orchestration/research/catalogue/icon-prop-2026-05-XX/` (legolas-1 + elrond curation; 79 rows; includes dungeon-relevant props)
5. **Gandalf register canon** — `canonical/story/audio-register-canon-2026-05-17.md` style register guide (visual cluster A retro-pixel for dungeon)
6. **Gandalf v1.10 VFX scene-needs spec** — `canonical/story/vs2a-vfx-scene-needs.md` (register-fence rule; per-UI-surface authoring)

---

## Scope — five deliverables

### Deliverable 1 — Current state audit

Inventory what dungeon objects are currently wired in the demo:
- Stairs sprite (currently from which pack? what's the visual register? quality assessment 1-5)
- Chests (Seliel chest already wired; verify quality)
- Pots (red/yellow; verify quality)
- Doors / gates
- Wall decorations (banners, torches, sconces)
- Floor decorations (rugs, stones, debris)
- Decorative props (magic book, coffin, candles, etc. from drax v1.13)
- Misc (barrels, crates, tables, chairs, bookshelves)

Rate each on 1-5 (5=high quality + fits register; 1=poor quality OR wrong register).

### Deliverable 2 — Swap-candidate scout

For every object rated 1-3, search already-acquired catalogues for higher-quality alternatives that fit Cluster A retro-pixel register. Prioritize:
- **Stairs** (Matt called out as worst; player sees it every level)
- **Then any 1-2 rated objects** (lowest quality wins priority)
- **Then 3-rated objects** (acceptable but room for improvement)

For each swap candidate:
- Source pack path
- License (must be permissive: CC0, CC-BY, OGA, Kenney, CraftPix free-terms, Seliel)
- Visual register fit (Cluster A retro-pixel ideally; flag any deviations)
- Frame count + dimensions
- Whether it's a drop-in swap or requires alpha-channel preprocessing / rescaling

### Deliverable 3 — Acquisition flag list (small)

If a critical gap exists with no acceptable already-acquired alternative, flag the gap as a Matt-acquisition candidate:
- Object type missing acceptable candidate
- Recommended pack (URL + cost)
- Why this matters (visibility / frequency in demo)

Recommendation: minimize flagged acquisitions for VS2a; defer non-critical gaps to post-VS2a.

### Deliverable 4 — Output document

Author `agentic_orchestration/research/curated/dungeon-objects-quality-audit-2026-05-18.md` with:
- Current state audit table (object × current pack × quality rating)
- Swap candidate table (object × swap pack × license × register fit × drop-in vs preprocess)
- Acquisition flag list (if any)
- Recommendation summary for drax v1.17 swap dispatch

### Deliverable 5 — Drax v1.17 handoff brief

Brief block at end of doc summarizing what drax needs to do in v1.17:
- Specific files to modify (atlas paths, tileset references)
- Object-by-object swap targets
- Any preprocessing required (PIL alpha; PNG re-export)
- Test plan: which encounters/rooms to spawn for visual verification

---

## Acceptance criteria

- [ ] Audit doc authored at named path
- [ ] Current-state audit table complete (all dungeon object categories)
- [ ] Swap candidates identified for all 1-3 rated objects
- [ ] Stairs has at least 2 swap candidates ranked by fit
- [ ] License verified for every swap candidate
- [ ] Acquisition flag list complete (small or empty)
- [ ] Drax v1.17 handoff brief included
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `elrond/v1.8-dungeon-objects-quality-audit-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT swap any sprites yourself (drax v1.17 seam; you provide candidates)
- ❌ DO NOT pre-empt Matt acquisition decisions (flag; do not authorize spend)
- ❌ DO NOT modify drax v1.13 code (research-only output)
- ❌ DO NOT touch hybrid_mage retire chain
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** gandalf canonical-6 doc; jack-ryan decisions-log + Discipline #17; rocket canonical-6 archetype removal; drax v1.16.2 audio + holy VFX
- **Triggers downstream:** drax v1.17 dungeon-objects swap (knight-rider fires post-your-audit + post-drax-v1.16.2-completion)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 dungeon-object quality feedback. ~45-60 min. Append completion record + audit doc path when done.*

---

## Completion record

**Completed:** 2026-05-18 by elrond
**Tag:** `elrond/v1.8-dungeon-objects-quality-audit-1` (local; not pushed per ADR-006)
**Output doc:** `agentic_orchestration/research/curated/dungeon-objects-quality-audit-2026-05-18.md`
**Result:** Audit complete; root cause identified; 5 priority swap targets for drax v1.17; acquisition flag list EMPTY for VS2a.

### Acceptance criteria status

- [x] Audit doc authored at `agentic_orchestration/research/curated/dungeon-objects-quality-audit-2026-05-18.md`
- [x] Current-state audit table complete (Section 1 — 21 dungeon object classes inventoried with quality + register-fit ratings 1-5)
- [x] Swap candidates identified for all 1-3 rated objects (Section 2 — covers floor tiles, wall tiles, stairs, animated props, prop variety)
- [x] Stairs has 3 swap candidates ranked by fit (Section 2.1 — 169442 Objects.png primary; 298079 stairs.png fallback; 169442 decorative_cracks_floor.png as hazard not stair)
- [x] License verified for every swap candidate (all CraftPix-Free-Terms; one credit line covers all packs)
- [x] Acquisition flag list complete (Section 3 — EMPTY for VS2a; informational VS2b candidates listed)
- [x] Drax v1.17 handoff brief included (Section 5 — files + preprocessing + test plan + failure-modes + acceptance criteria)
- [x] PRE-SIGNAL § 14.1.1 awareness noted (no hive-log append performed this session — audit-only Pattern A delivers via output doc + dispatch completion record per dispatch directive; if hive-log entry warranted post-handoff, fetch-before-stage discipline applies)
- [x] AGENT_STATE STATE entry updated
- [x] Tag created locally (no push per ADR-006)

### Root-cause finding (executive)

The CraftPix `walls_floor.png` sheets wired by drax v1.13 Area 1 are **composition reference atlases, NOT auto-tilable 16px tilesets**. Drax's slicer treats rows 4-8 as "floor tile candidates" and tiles them deterministically across room floors, producing **stair-fragments and wall-bar-fragments scattered across every room's floor**. The clean floor tile sheet (`plates.png`, 208×128, 13×8 grid) and dedicated stair sheet (`stairs.png`, 192×240) and high-quality dungeon object library (169442 `Objects.png`, 384×96) all exist on-disk but are unwired. Matt's "stairs sprite is really bad" verdict is the direct visible consequence of mis-interpreting the architecture-atlas as a tile-grid.

### Priority swap targets for drax v1.17

1. **P1 Floor tiles** — switch from `walls_floor.png` rows 4-8 to `plates.png` (208×128 13×8 clean grid). Quality 1→4.
2. **P2 Stairs** — wire 169442 `Objects.png` top-left stair piece at exit-door threshold; per-season variants. Quality 1→5.
3. **P3 Walls** — disable broken sprite walls; fall back to existing procedural 8px Graphics perimeter. Quality 1→3.
4. **P4 Animated props** — correct frame-count for candles (432×224), torches (224×288), fountain (288×64). Quality 2→4.
5. **P5 Prop variety** — wire 3-4 props from 169442 `Objects.png` + 298079 `other_objects.png` (ladder, crate, barrel, sack, vase, column, cage, rubble). Adds visible variety; closes Matt "generally poor" concern.

Estimated drax v1.17 effort: ~3-4 hours.

### Acquisition flag list

**EMPTY for VS2a.** All swap candidates already on disk under `reincarnated-demo/public/assets/craftpix_catalogue_large/`. License is CraftPix-Free-Terms; existing single credit line covers all wirings.

Informational VS2b candidates (no Matt decision needed VS2a): Mucho Pixels ($4.95; coffin/weapon-stand/pot states), Anokolisa free 500-sprite pack, Indie-Vova Dungeons & Pixels 32x32 ($5.99).

### Cross-seam coordination

- **Drax v1.17 dispatch ready** — Section 5 of audit doc is the handoff brief; files, preprocessing, test plan, failure-modes, acceptance criteria all specified
- **Schema observation surfaced** — recommend `usage_recommendation` field in future dungeon-tileset subset manifests to prevent slicer-shredding defect class (advisory; non-blocking for VS2b crawl scope)
- **Drift-audit candidate** — distillable discipline: "composite reference atlases are NOT auto-tilable tilesets; sprite-tile rendering must consume purpose-built tile-grid sheets only" — recommend Gandalf or jack-ryan note in decisions-log

### Out-of-scope honored

- DID NOT swap any sprites (drax v1.17 seam)
- DID NOT modify drax v1.13 code (audit-only)
- DID NOT touch hybrid_mage retire chain
- DID NOT push tag (ADR-006)
- DID NOT authorize spend (acquisition flag list empty for VS2a)
