# Stage A2 Closeout Scope of Work — continuation from VS2b closure

**Authored:** 2026-05-19 by knight-rider per Matt directive 2026-05-19 ("approved, proceed all the way through Stage A2").
**Authority:** Matt directive (autonomous-operation + pre-approval-batch mode extended through Stage A2 + Playtest Cycle 1).
**Status:** **Pre-approved executable plan.** Specialists pick up dispatches at activation gates per coordination matrix DAG.
**Estimated duration:** ~6–10 weeks wall (per roadmap "~6–10 weeks after VS2a/VS2b close").
**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9.
**Companion artifacts:** `coordination-matrix-stage-a2.md` + `stage-a2-pre-approval-batch-2026-05-19.md`.
**Predecessor:** `scope-of-work-vs2b.md` (VS2b; CLOSES at V6 ship → Stage A2 activates).

---

## § 0 — TL;DR

Stage A2 closeout completes the engine's ARPG-rebalance design queue (`canonical/28-engine-arpg-rebalance-design.md`) — the B-series items deferred while VS2a + VS2b shipped. ~70% of original Stage A2 is already in flight or shipped (B10.1/B10.2/B10.4/B11/B14.5 V1 + B6 main in VS2a). Stage A2 CLOSEOUT covers the remaining ~30%:

- **B7** gear-percentile variance gate
- **B12** full audit (boots/gloves/belt + +% MS affixes + hard-cap)
- **B13** post-narrow-slice (5 defensive mobility geometries + escape AI + observability + role-tagging + trait-pool; ~75% of original B13)
- **B14** multi-band convergence sim
- **B16** loot drop architecture (Drift-12 candidate filing)

**Plus Stage A2 design watch-items** (gandalf-stewarded; visual/UX axes):
- B12 visual/UX (boots/gloves/belt UI; +% MS VFX; cap UX)
- B13 telegraph-art convention
- B16 loot visual presentation layer

**Plus Playtest Cycle 1** post-Stage-A2 closeout (~1-2 weeks).

**7 dispatches total** (A1–A7).

---

## § 1 — Items in scope

### § 1.1 — A1 — B7 gear-percentile variance gate

- **Owner:** gamora (sim seam — engine-only)
- **Origin:** `canonical/28-engine-arpg-rebalance-design.md` B7 + co-design with B10 (gauntlet structure)
- **Deliverables:**
  - Per-class gear variance simulation (multiple roll percentiles vs balance loop)
  - Gate criterion: variance across gear rolls stays within tolerance band (specific threshold per B7 spec)
  - Per-class telemetry capture: gear-variance distribution
  - MIGRATION.md if telemetry surface extends
- **Effort:** ~2–3 days
- **Activation gate:** VS2b ships → Stage A2 kickoff
- **Tag:** `stage-a2/v0.1-b7-gear-variance-gate`

### § 1.2 — A2 — B12 full audit

- **Owner:** rocket (catalogue + schema) + gamora (sim consumer) + drax (UI consumer per A6 design watch-item)
- **Origin:** `canonical/28-engine-arpg-rebalance-design.md` B12 + VS2a partial coverage
- **Deliverables:**
  - Boots/gloves/belt slot additions to gear catalogue (per B12 spec)
  - +% MS affixes added per spec
  - Hard-cap on MS modifier per Discipline conventions
  - Sim consumption updated for new slots + affixes
  - drax UI: boots/gloves/belt slot display + +% MS visualization + cap UX (per A6 design watch-item framework)
  - MIGRATION.md at generation + sim + demo seams
  - Round-trip smoke per Principle 6
- **Effort:** ~1.5–2 weeks (rocket schema + sim consumer + drax UI)
- **Activation gate:** Stage A2 kickoff + A6 design watch-item framework lands (for UI/UX axes)
- **Tag:** `stage-a2/v0.2-b12-full-audit-complete`

### § 1.3 — A3 — B13 post-narrow-slice

- **Owner:** rocket (catalogue + generator role-tagging) + gamora (sim AI + observability)
- **Origin:** `canonical/28-engine-arpg-rebalance-design.md` B13 + `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 narrow-slice + `canonical/32-progression-design.md` § 12.5 Amendment 2026-05-17
- **Narrow-slice already-shipped (Phase-1 P1 Deliverable 28):**
  - Universal dodge mechanic ✓
  - Enemy-AOE telegraph indicators ✓
  - Elite-tier reactive escape AI ✓
  - Cross-doc updates ✓
- **A3 deliverables (post-narrow-slice; ~75% remaining):**
  - 5 defensive mobility geometries as kit-pool additions: `roll` / `defensive_dash` / `strafe_mode` / `blink` / `dodge_stance`
  - Mini-boss + boss strategic/anticipatory/substrate-coherent escape AI (extends elite-tier reactive AI)
  - Archetype-emergence observability (telemetry surface)
  - Mobility role-tagging in generator
  - Full B13 trait-pool extension surface
  - drax UI: telegraph-art convention applied per A6 design watch-item framework
- **Effort:** ~2.5–3 weeks (down from original 3–4 weeks per narrow-slice reduction)
- **Activation gate:** Stage A2 kickoff + A6 design watch-item framework lands (for telegraph-art convention)
- **Tag:** `stage-a2/v0.3-b13-post-narrow-slice-complete`

### § 1.4 — A4 — B14 multi-band convergence sim

- **Owner:** gamora (sim seam — engine-only)
- **Origin:** `canonical/28-engine-arpg-rebalance-design.md` B14 (extends B14.5 V1 already-shipped)
- **Risk note:** "B14 is the riskiest piece but operates on existing primitives" (per roadmap § "Track A landing rhythm"). B14.5 V1 architecture is the canonical balance-loop pattern; B14 multi-band extends without replacing.
- **Deliverables:**
  - Multi-band convergence (e.g., 0/16/32/50 tier-band convergence simulation)
  - Telemetry surface for per-band convergence metrics
  - MIGRATION.md if sim seam extends contracts
- **Effort:** ~2–3 weeks
- **Activation gate:** Stage A2 kickoff
- **Tag:** `stage-a2/v0.4-b14-multi-band-convergence`

### § 1.5 — A5 — B16 loot drop architecture

- **Owner:** rocket (catalogue + drop rules) + drax (visual presentation per A6 framework)
- **Origin:** `canonical/28-engine-arpg-rebalance-design.md` B16
- **Drift-12 candidate filing:** "Loot visual presentation layer (drop animation; loot beams; rarity colors; tooltips; auto-pickup feedback)" — implicit-deferred axis per p6-forward-audit; filed as Drift-12 candidate in drift-audit at A5 closure
- **Deliverables:**
  - Drop rules engine: per-tier loot drop rates + rarity distribution
  - Auto-pickup architecture per mobile-first standard
  - drax visual presentation per A6 design framework: drop animation + loot beams + rarity colors + tooltips + auto-pickup feedback
  - MIGRATION.md at generation + demo seams
- **Effort:** ~1.5–2 weeks
- **Activation gate:** Stage A2 kickoff + A6 design watch-item framework lands (for loot visual layer)
- **Tag:** `stage-a2/v0.5-b16-loot-drop-architecture`

### § 1.6 — A6 — Gandalf Stage A2 design watch-items framework

- **Owner:** gandalf (design-steward — single framework for all three visual/UX axes)
- **Origin:** `canonical/16-project-roadmap.md` § "Stage A2 forward-audit (gandalf) watch-items" + `canonical/story/p6-forward-audit-2026-05-16.md`
- **Deliverables:**
  - **B12 visual/UX framework** — boots/gloves/belt UI conventions; +% MS VFX; cap UX
  - **B13 telegraph-art convention decision** — primitive-rendered (circle/cone/line; locked color/opacity in HD-2D-pixel register) vs vendor-sourced; per roadmap recommendation: primitive-rendered with PoE precedent
  - **B16 loot visual presentation layer framework** — drop animation; loot beams; rarity colors; tooltips; auto-pickup feedback
  - Drift-12 candidate filing in `canonical/story/drift-audit.md`
- **Effort:** ~1 day gandalf (single framework doc covering three axes)
- **Activation gate:** Stage A2 kickoff (autonomous; fires immediately)
- **Tag:** `stage-a2/v0.6-design-watch-items-framework`

### § 1.7 — A7 — Playtest Cycle 1 prep + execution

- **Owner:** gandalf (design-steward — rubric + observation framework) + knight-rider (coordination) + Matt (playtester at execution step; partial Matt-gating)
- **Origin:** `canonical/16-project-roadmap.md` § "Playtest Cycle 1"
- **Deliverables:**
  - **Prep phase (autonomous):** gandalf authors playtest rubric + observation framework + capture cadence per existing playtest conventions
  - **Execution phase (Matt-gated; HELD for wind-down):** Matt plays through the regenerated seasons (VS2a regen season_001003 + VS2b regen season_001005) + Stage A2 additions; observation captured per rubric
  - **Disposition phase (autonomous post-Matt-playtest):** gandalf authors playtest cycle report + recommendations; routes to roadmap for Stage A3 sequencing
- **Coverage:** skill tree UI comprehensibility + gauntlet density feel + mobility geometries + telegraphs + mobile-first auto-pickup + loot drop density
- **Effort:** prep ~2 days gandalf; execution ~1 day Matt; disposition ~2-3 days gandalf
- **Activation gate:** A1 + A2 + A3 + A4 + A5 + A6 land
- **Matt-gated step:** execution phase HELD for wind-down (Matt's playtest session)
- **Tag:** `stage-a2/v1.0-stage-a2-ship` (closeout tag at execution + disposition complete)

---

## § 2 — Already-shipped (reference only; no re-dispatch)

Per `canonical/16a-roadmap-shipped-log.md` + dispatch completion records:

| Item | Status |
|---|---|
| B10.1 — Gauntlet density (~80-100 monsters/min) | ✅ Shipped |
| B10.2 — Composition (~70% trash + ~20% magic + ~10% elite) | ✅ Shipped |
| B10.4 — Pack-scale (5-15 mobs per encounter) | ✅ Shipped |
| B11 — Geometry palette expansion (16 → 25 active types) | ✅ Shipped (VS2a) |
| B14.5 V1 — Primary loop architecture | ✅ Shipped (`v1.3-b14-5-primary-loop` 2026-05-12) |
| B6 — Class kit composition + Hierarchical Skill Tree | ✅ Shipping in VS2a (S2 + F4) |
| B13 narrow-slice (~25%) | ✅ Shipped Phase-1 P1 Deliverable 28 |

---

## § 3 — Matt-gated items

| # | Item | Owner | Trigger |
|---|---|---|---|
| **A7 execution** | Playtest Cycle 1 Matt-playtest session | Matt | A6 framework + A1-A5 dispatches land → wind-down |

Carry-over from VS2a/VS2b:
- **M1** Drift-15 environment-pack selection (HELD)
- **M2** engine-rebuild playtest tag firings (HELD)

Stage A2 ship (A7 disposition phase) does NOT require additional Matt-gate beyond the playtest session itself.

---

## § 4 — Sequencing summary

```
VS2b ship (vs2b/v1.0-vs2b-ship) ──► Stage A2 kickoff
                              │
              ┌───────────────┼───────────────┬──────────────┐
              ▼               ▼               ▼              ▼
             A1              A6              A4         (M1+M2 HELD)
       (gamora B7)       (gandalf design   (gamora
                          watch-items       B14 multi-band)
                          framework)
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
             A2              A3               A5
       (rocket+gamora+   (rocket+gamora;  (rocket+drax;
        drax B12 full)    B13 post-       B16 loot drop
                          narrow-slice)    architecture)
              │               │                │
              └───────────────┼────────────────┘
                              │
                              ▼
                            A7 prep
                       (gandalf playtest
                        rubric + framework)
                              │
                              ▼
                    (Matt-gated: A7 execution)
                              │
                              ▼
                            A7 disposition
                       (gandalf playtest report)
                              │
                              ▼
                    stage-a2/v1.0-stage-a2-ship
                              │
                              ▼
                    (Stage A3 — B9 series; pre-approval
                     decision deferred to Matt)
```

---

## § 5 — Roadmap continuation (post-Stage-A2)

Per `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b":

- **Stage A3** — B9 series (traits + skill points + reset + Spirit Guide build coach); ~4–6 weeks; design fully resolved 2026-05-12 in file 32
- **Playtest Cycle 2** — post-A3; ~1–2 weeks
- **Stage A4** — B5 (legendary gear abilities) + B15 (Seasonal Sets); ~2–4 weeks engine + 1 wk demo
- **Playtest Cycle 3** — post-A4; ~1 week
- **Stage A5** — B1, B2 small balance items; ~2-3 hrs combined
- **Stage A6** — Category C deep-cuts; DEFERRED unless playtest demands
- **Stage A7** — Progression system implementation; ~5-7 weeks; design fully resolved 2026-05-12 in file 32 + 33
- **Playtest Cycle 4** — post-A7; ~2 weeks; Phase 0 ship-readiness assessment

**Pre-approval-batch decision for Stage A3+ DEFERRED to Matt at next wind-down session** — knight-rider stands ready to extend batch authoring if Matt requests.

---

## § 6 — Mission discipline

| Pressure | Default |
|---|---|
| B13 escape AI surfaces deeper than narrow-slice predicted | Surface to gandalf for re-disposition; may need separate dispatch for boss-specific AI |
| B16 visual layer surfaces complexity beyond A6 framework | gandalf amends framework; drax stays within seam |
| B7 gear-variance gate fails → catalogue gap surface | Surface to rocket via hive log; potentially blocks A5 (loot architecture) |
| B14 multi-band convergence surfaces architectural extension need | gamora L1 within seam per B14.5 V1 canonical pattern |
| Playtest Cycle 1 reveals VS2a/VS2b regression | gandalf re-disposition; surface to Matt at wind-down |
| Matt returns mid-Stage-A2 with redirection | wind-down trigger; pause; respect |

**Single-season-per-playtest rule** (LOCKED 2026-05-12): Stage A2 closeout does NOT regen new season; uses VS2a regen (season_001003) + VS2b regen (season_001005) as playtest substrate. No new regen for A1-A6 closure; Playtest Cycle 1 walks the same player through both regen seasons + Stage A2 additions.

---

## § 7 — Cross-references

- Predecessor: `agentic_orchestration/hive-mind/scope-of-work-vs2b.md`
- Sibling pre-approval batches: `vs2a-pre-approval-batch-2026-05-19.md` + `vs2b-pre-approval-batch-2026-05-19.md`
- B-spec source: `canonical/28-engine-arpg-rebalance-design.md`
- B13 narrow-slice: `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 + `canonical/32-progression-design.md` § 12.5 Amendment
- B14.5 V1 architecture: per `v1.3-b14-5-primary-loop` (2026-05-12) — canonical balance-loop pattern
- p6-forward-audit (watch-items source): `canonical/story/p6-forward-audit-2026-05-16.md`
- Drift-12 candidate (loot visual layer): file at drift-audit.md per A5 + A6
- Roadmap: `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b"
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## § 8 — Tag milestone plan (Stage A2 namespace)

| Tag | Trigger |
|---|---|
| `stage-a2/v0.0-vs2b-baseline` | At Stage A2 kickoff (fires when VS2b V6 ships) |
| `stage-a2/v0.1-b7-gear-variance-gate` | A1 lands |
| `stage-a2/v0.2-b12-full-audit-complete` | A2 lands |
| `stage-a2/v0.3-b13-post-narrow-slice-complete` | A3 lands |
| `stage-a2/v0.4-b14-multi-band-convergence` | A4 lands |
| `stage-a2/v0.5-b16-loot-drop-architecture` | A5 lands |
| `stage-a2/v0.6-design-watch-items-framework` | A6 lands |
| `stage-a2/v0.7-playtest-cycle-1-prep-complete` | A7 prep phase lands |
| `stage-a2/v1.0-stage-a2-ship` | A7 disposition lands; Stage A2 CLOSED |

Notional `stage-a2/v1.1-stage-a2-validated` fires post-playtest-cycle-1 validated.

---

*Filed 2026-05-19 by knight-rider per Matt directive (VS2A → VS2B → Stage A2 pre-approval extension). Seven dispatches close the engine's ARPG-rebalance design queue; the playtest follows; the road continues toward Stage A3.*
