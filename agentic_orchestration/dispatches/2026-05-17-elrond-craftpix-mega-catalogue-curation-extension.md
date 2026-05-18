# 2026-05-17 — elrond — CraftPix mega-catalogue curation extension (post-legolas-3)

**Authority:** Matt L3 2026-05-17 evening — legolas-3 catalogue crawl shipped completion record with 67 CraftPix rows + 9 free_characters_and_vfx rows + 5 gap-status changes + 7 Matt-parked questions. This dispatch consumes legolas-3's raw inventory and produces curated subset manifests + VFX-layer-architecture proposal + gap-status updates.
**Type:** Pattern B — curation + manifest extension (~0.5-1 day; data-steward work in elrond's seam).
**Predecessor:** legolas-3 CraftPix mega-catalogue crawl completion (`agentic_orchestration/dispatches/2026-05-17-legolas-craftpix-mega-catalogue-and-character-vfx-crawl.md` § completion record).

---

## Why this matters

Legolas-3 produced raw inventory. Your job: turn it into actionable manifests for downstream consumption. Five gap-status changes need elrond-curation work to formalize:

1. **G-COFFIN CLOSED** (pending Matt Q1 design-fit) — craftpix-net-298079 coffins.png is the candidate; verify size register + add to ambient-props manifest
2. **G4 close path** (pending Matt Q2) — Frostwindz Slashes retires CodeManu CC-BY dependency; VFX manifest schema needs Frostwindz class-archetype layer
3. **G3 substantially CLOSED** — 17 monster packs on disk; needs curated monster-subset manifest if Matt authorizes (Q7)
4. **Pimen hit-spark redundancy** (pending Matt Q3) — Frostwindz Impacts superior; manifest update
5. **NightBorne BLOCKED** (pending Matt Q5) — flag in manifests, do not include in any curated subset until license resolved

Plus: legolas-3 proposes a **4-layer VFX architecture** (Pimen substrate / Frostwindz class-archetypes / Frostwindz physical / Alenia atmospheric). Your VFX manifest schema needs to extend to support these layers cleanly.

---

## Required reading

1. **Legolas-3 completion record** — `agentic_orchestration/dispatches/2026-05-17-legolas-craftpix-mega-catalogue-and-character-vfx-crawl.md` § completion record (your authoritative input)
2. **Legolas-3 raw inventory** — `agentic_orchestration/research/catalogue/craftpix-mega-catalogue-2026-05-17/inventory.jsonl` + `free-characters-and-vfx-inventory.jsonl` + `summary.md`
3. **Your prior Pimen subset** — `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` (template + integration with Pimen substrate layer)
4. **Your prior icons-and-props subsets** — `floor-loot-subset-vs2a-2026-05-17.jsonl`, `ambient-props-subset-vs2a-2026-05-17.jsonl`, `ui-icons-subset-vs2a-2026-05-17.jsonl` (acquired-pack manifests — extend with CraftPix complements)
5. **Your acquisition registration completion** — `agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-acquisition-registration.md` § completion record (current acquired-pack status)
6. **Gandalf sizing canon** — `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (size-register-fit criterion)

---

## Scope — five deliverables

### Deliverable 1 — Dungeon-tileset subset manifest

Author `agentic_orchestration/research/curated/dungeon-tileset-subset-vs2a-2026-05-17.jsonl`.

Curate from legolas-3's 8 dungeon-tileset packs (stone + cave + sewer + undead):
- Per-tier subset (which packs primarily ship room tiles vs animated hazards vs both)
- Animated-hazard inventory (ghost trap, dragon-head fire trap, fire statue, spiked floor, fountain, etc.) — these are the "non-combatant damaging elements" Matt flagged
- Size register check (gandalf canon; pixel grain matching demo)
- License posture per pack (CraftPix-Free-Terms; one attribution credit)
- Recommendation per pack: WIRE-NOW (VS2a room construction); WIRE-LATER (VS2b biome expansion); SKIP (off-tone)

### Deliverable 2 — Monster-subset manifest (CONDITIONAL on Matt Q7)

If Matt authorizes (Q7 = YES, "commission now"): author `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl`.

Curate from legolas-3's 17 monster packs + 4 boss packs:
- Per-substrate mapping (which monster fits which canonical-7 substrate; e.g., zombie → shadow, dragon → fire, golem → earth, ent → earth/wind, etc.)
- Per-archetype mapping (trash / elite / boss role)
- Animation state coverage (idle / walk / attack / hurt / die)
- VS2a slot priorities (which 8-12 enemies cover the gauntlet bestiary)
- Per-pack license check

If Matt-Q7 = DEFER: stub this manifest with "DEFERRED post-VS2a per Matt L3" and move on.

### Deliverable 3 — Expand 2 ZIPs + classify (CONDITIONAL on Matt Q6)

If Matt authorizes (Q6 = YES): expand `craftpix-net-382264` (armor+weapons icons) + `craftpix-net-596440` (fishing-and-gathering icons). Add rows to existing UI-icons + floor-loot manifests for any DireDungeon overlap analysis.

If Matt-Q6 = DEFER: stub with "DEFERRED" and note in completion record.

### Deliverable 4 — VFX manifest schema extension (4-layer architecture)

Extend existing Pimen subset manifest (or author a new companion manifest) to support legolas-3's proposed 4-layer architecture:

| Layer | Source | Role | Examples |
|---|---|---|---|
| 1 — substrate | Pimen | Element × slot wiring | fire-cast / water-projectile / lightning-impact |
| 2 — class-archetype | Frostwindz Blood Mage / Necromancer / Rogue / Starcaller / Vampire | Active spirit visual register | Composited on Layer 1 |
| 3 — physical | Frostwindz Slashes + Impacts | Physical-archetype Slot B/C | CC-BY-free alternative to Pimen physical |
| 4 — atmospheric | Alenia Studios Atmospheric | Full-screen room-atmosphere overlays | tornado / fractal-lightning / creeping-frost / fire-embers / phantom-fog |

Author or extend manifest at `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` + JSONL companion.

Include per-layer:
- Element/archetype/class-coverage matrix
- File path (acquired_path)
- License posture
- Render-pipeline placement (which Pixi layer; particlesUnder/Mid/Over)
- Drax integration notes (which existing module extends; or new module needed)

### Deliverable 5 — Gap-status update + summary doc

Author `agentic_orchestration/research/curated/craftpix-mega-curation-summary-2026-05-17.md`:

1. Executive summary
2. Gap-status changes (with Matt-decision dependencies):
   - G-COFFIN: status pending Matt Q1
   - G4: status pending Matt Q2 (elrond-recommended ACCEPT Frostwindz)
   - G3: substantially closed; pending Q7 for VS2a curation
   - Pimen Impacts purchase: pending Matt Q3 (elrond-recommended SKIP, save $4.25)
   - NightBorne: BLOCKED until license resolved (Q5)
3. Curated subset manifest references (paths + row counts)
4. 4-layer VFX architecture proposal
5. Earth meta-layer readiness (10 interior packs; VS2b+ scope flag)
6. Open Matt-decisions (carry forward legolas-3's 7 questions; add any new ones surfaced during curation)
7. HANDOFFs:
   - → drax: dungeon-tileset wiring candidates (post-v1.12 if Matt approves); monster subset (if Q7 YES); 4-layer VFX architecture integration plan
   - → matt: 7 carried-forward decisions + any new ones
   - → knight-rider: standard chain coordination

---

## Out of scope (DO NOT)

- ❌ DO NOT commission new vendor acquisitions without Matt sign-off (consume on-disk only)
- ❌ DO NOT modify legolas-3 raw inventory (consume only; flag any data-quality issues for legolas-4 follow-on if needed)
- ❌ DO NOT touch drax's ingest pipeline or wiring code (manifests only; drax integration follows separate dispatches)
- ❌ DO NOT pre-empt drax v1.12 loot-pipeline wiring (in flight; your curation may inform follow-on but doesn't redirect v1.12)
- ❌ DO NOT pre-empt Matt-decisions — your manifests can recommend, but final acquisition/scope calls are Matt's L3
- ❌ DO NOT include NightBorne in any curated subset until license is resolved

---

## Acceptance criteria

- [ ] Dungeon-tileset subset manifest authored
- [ ] Monster-subset manifest authored OR stubbed-as-deferred per Matt Q7
- [ ] 2 ZIPs expanded + classified OR stubbed-as-deferred per Matt Q6
- [ ] 4-layer VFX architecture manifest authored
- [ ] Gap-status update doc authored with carried-forward Matt-decisions
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider
- [ ] No new vendor commissions without Matt sign-off
- [ ] NightBorne explicitly excluded from all curated subsets until license resolved

---

## Coordination

- **Parallel-safe with**: drax v1.12 loot-pipeline wiring (in flight); drax hotfix v1.12.0 (just shipped); rocket hotfix v1.12.1 (in flight); gamora D11 math note (in flight); gandalf DoE doc cascade (in flight); D11 sprint queue
- **PRE-SIGNAL § 14.1.1** before hive-log appends (many writers; race-condition risk highest of any day)
- **No tag** (curation; not code)

---

## Why this is important now

Legolas-3 surfaces meaningful cost-savings (skip Pimen $4.25; potentially retire CodeManu CC-BY risk) AND meaningful scope expansions (17 monster packs; Earth-meta-layer 10 interior packs; 4-layer VFX architecture). Your curation work formalizes these into manifests drax can consume; otherwise the value stays trapped in raw catalogue form.

This is the standard legolas → elrond → drax chain working as designed: scout → curate → wire.

---

*Dispatched 2026-05-17 by knight-rider per legolas-3 completion + Matt L3 standard chain. ~0.5-1 day. Append completion record when done.*

---

## Completion record — elrond — 2026-05-17

**Status:** COMPLETE.
**PRE-SIGNAL § 14.1.1:** honored — `git fetch origin` ran before hive-log append; last remote commit `9fee2ce` (docs(drax): hive-log STATE entry — v1.12 loot-pipeline wiring DireDungeon current-state eval); local hive-log already modified with jack-ryan D11 Gate-1 advisory entry — append to local working tree without rebase to preserve concurrent local entries.
**Tag:** none (curation; not code; standard discipline).
**Type:** Pattern B — data-steward curation; consumed legolas-3 raw inventory; produced manifests + 4-layer VFX architecture proposal.

### Deliverables shipped

| # | Deliverable | Path | Status |
|---|---|---|---|
| 1 | Dungeon-tileset subset manifest | `agentic_orchestration/research/curated/dungeon-tileset-subset-vs2a-2026-05-17.jsonl` | **AUTHORED** — 8 packs (3 WIRE-NOW / 4 WIRE-LATER / 1 SKIP); 1 header + 8 data rows |
| 2 | Monster-subset manifest | `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` | **DEFERRED stub** per Matt Q7 unresolved; 1 stub-header row carrying forward inventory pointers |
| 3 | 2 ZIPs expansion + DireDungeon overlap analysis | `agentic_orchestration/research/curated/craftpix-zip-expansion-deferred-2026-05-17.md` | **DEFERRED stub** per Matt Q6 unresolved; work plan documented |
| 4 | 4-layer VFX architecture manifest | `agentic_orchestration/research/curated/vfx-layered-architecture-vs2a-2026-05-17.md` + `.jsonl` | **AUTHORED** — 8 new rows across Layers 2/3/4 (Layer 1 Pimen unchanged); architecture doc + JSONL companion |
| 5 | Gap-status + summary doc with carry-forward Matt-decisions | `agentic_orchestration/research/curated/craftpix-mega-curation-summary-2026-05-17.md` | **AUTHORED** — 10 sections per dispatch spec |

### Acceptance criteria

- [x] Dungeon-tileset subset manifest authored — 8 packs curated (legolas-3 dungeon-tileset inventory rows 2-9)
- [x] Monster-subset manifest stubbed-as-deferred per Matt Q7 unresolved
- [x] 2 ZIPs expansion stubbed-as-deferred per Matt Q6 unresolved
- [x] 4-layer VFX architecture manifest authored (Pimen substrate / Frostwindz class-archetype / Frostwindz physical / Alenia atmospheric)
- [x] Gap-status update doc authored with 7 carried-forward + 3 new Matt-decisions
- [x] PRE-SIGNAL § 14.1.1 before hive-log append
- [x] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider — appended
- [x] No new vendor commissions without Matt sign-off — consumed on-disk only throughout
- [x] NightBorne explicitly excluded from all curated subsets — confirmed BLOCKED in all 5 deliverables

### Gap-status changes formalized

| Gap | Pre-curation | Post-curation | Matt-decision dependency |
|---|---|---|---|
| **G-COFFIN** | OPEN | **CLOSED** via `craftpix-net-298079` coffins.png (zero cost) | Q1 design-fit confirmation |
| **G4 — physical-slash CC-BY risk** | PARKED Matt-decision | **CLOSE-PATH on disk** via Frostwindz Slashes (Layer 3) | Q2 (elrond-recommended ACCEPT) |
| **G3 — non-humanoid embodiment** | OPEN-deferred | **SUBSTANTIALLY CLOSED** — 17 monster + 4 boss packs ready for curation | Q7 (no preference) |
| **Pimen `battle-vfx-hit-spark` $4.25** | Planned acquisition | **MAY BE REDUNDANT** — Frostwindz Impacts superior | Q3 (elrond-recommended SKIP — save $4.25) |
| **NightBorne** | Unverified license | **BLOCKED** — no license file on disk | Q5 (DEFER until resolved) |

### Cost impact

If Matt approves Q3 SKIP: revised VS2a Pimen acquisition $26.35 → $22.10 (savings $4.25). CC-BY attribution surface from `pixel-battle-effects` eliminated (G4 close path on disk via Frostwindz Slashes). CodeManu acquisition deferred indefinitely (Stage A2+ if Frostwindz quality issues surface at drax integration).

### Top 5 findings for Matt

1. **G-COFFIN closure available at zero cost** — `craftpix-net-298079` coffins.png is design-fit-compatible with stone-dungeon trio (net-125640 + net-169442 + net-298079 form coherent set). Pending Q1.
2. **G4 close path on disk via Frostwindz Slashes** — eliminates CC-BY attribution surface from `pixel-battle-effects`; no CodeManu acquisition needed. Pending Q2 (elrond-recommended ACCEPT).
3. **$4.25 savings opportunity** — Frostwindz Impacts (7 effects × B&W + COLOR variants) is superior wiring architecture to single-pack Pimen hit-spark. B&W variants match drax's runtime tint-composition strategy. Pending Q3 (elrond-recommended SKIP).
4. **4-layer VFX architecture proposed** — Pimen substrate (Layer 1, unchanged) + Frostwindz class-archetype overlays (Layer 2, 5 packs) + Frostwindz physical (Layer 3, Slashes + Impacts) + Alenia atmospheric (Layer 4, 20 effects). Opens VS2b composition design space.
5. **Layer 2 element-imbalance observed** — Frostwindz class packs concentrate on shadow + physical + holy/lightning. Fire/water/earth/wind/lightning lack class-archetype overlay coverage. Path C (accept absence for VS2a-VS2b) workable; future Frostwindz commission or alternative vendor for under-covered elements is a forward-flag, not VS2a-blocker.

### HANDOFFs

**→ drax (post-v1.12):** see summary § 9.1 + 4-layer architecture § 8 for full integration plan:
- Wire Frostwindz Slashes to physical-slash Slot B/C (replaces CC-BY pixel-battle-effects) — pending Matt Q2 ACCEPT
- Wire Frostwindz Impacts B&W variant + element-tint composite (replaces Pimen hit-spark) — pending Matt Q3 SKIP
- Optional Layer 4 POC: 1-2 atmospheric effects on single demo room; requires NEW `atmosphericUnder` + `atmosphericOver` pixi containers — pending Matt Q-LAYER-1
- Dungeon-tileset wiring: 3 WIRE-NOW packs (net-298079 lead, net-125640, net-169442) form stone-dungeon trio; animated hazards (ghost_trap, dragon_trap, Statue_fire, fire_trap, spike_trap, lattice_trap) are non-combatant damaging element library

**→ matt:** 7 carried-forward decisions (Q1-Q7) per summary § 6.1 + 3 new decisions surfaced during curation (Q-LAYER-1, Q-LAYER-2, Q-CHM-HOME) per summary § 6.2. Elrond recommendations consolidated in summary § 9.2.

**→ knight-rider:** standard chain coordination complete. Curation deliverables ready for downstream wiring dispatches (drax) and acquisition decisions (matt). No tag (curation, not code).

### Parallel-safety report

- No engine code touched
- No drax wiring touched (v1.12 in flight — manifests inform follow-on but don't pre-empt v1.12)
- No new vendor commissions (consumed on-disk only)
- Pimen subset manifest unchanged (4-layer architecture is additive)
- NightBorne excluded (BLOCKED Q5)
- PRE-SIGNAL § 14.1.1 honored before hive-log append

*Completed 2026-05-17 by elrond. ~0.5-1 day curation work per dispatch target. 5 deliverables shipped (2 active manifests + 2 deferred stubs + summary doc + 4-layer architecture proposal).*
