# David-H WS2 Commission — Niagara Cluster-Rune Rendering at Celestial-Sphere Geometry

**STATUS:** ACTIVE (commission ready to fire post Niagara verification PASS; gates on Option A/B Matt + gandalf decision per David-H consultation memo)
**Date:** 2026-06-10
**Author:** gandalf
**Authority:** Matt 2026-06-10 — "fire A then prompt B via KR then prompt C via DH" + § 12 canonical lock + Tal Rasha § 4.5 (WS2 commission scope expansion per Branch A operational)
**Audience:** david-h (PC orchestrator); mantis (executor); sam (Gate-2)
**Companion docs (read first):**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 12 (CANONICAL lock 2026-06-10 — 7 cluster regions; cycling-preview UX; sky-runes-only)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 11 (Tal Rasha § 4.2 — rune visual register: large + atmospheric + light-edge brush-stroke + no color + drawn by light only)
- `agentic_orchestration/david-h/notes/2026-06-10-consultation-mac-kr-niagara-verification-and-ws2-routing.md` (Option A/B routing trade-off matrix; PENDING Matt + gandalf decision)
- `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` (Sam WARN-001 windowed-mode Niagara verification gate)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` § 4.5

---

## 0. TL;DR

**Mission:** Render the 7 sky cluster regions per § 12.3 + 7 cluster-runes per § 11.2 visual register using Niagara VFX at AAA fidelity. Implement cycling-preview cosmograph response animation (highlighted cluster illuminates / others dim; smooth ~0.3-0.5 sec transitions per § 12.4). Compose with spherical-shell celestial-sphere geometry per § 2.6.

**Empirical trigger:** Mantis windowed-mode Niagara verification PASS per Option A or Option B routing (queued for Matt + gandalf decision); Branch A canonical operational per § 12.

**Substrate consumed:**
- Niagara API (windowed-mode validated per Option A/B routing)
- DataTables ingested per WS1 commission (cluster spatial layout per § 12 + per-cluster rune designation)
- Phase 5 amended /forge findings (cluster spatial layout 2D web prototype + cycling-preview animation timing reference)
- Style-register Tal Rasha § 4.2 visual register specs

**Estimated wall-clock:** 2-4 weeks UE mantis work per Mantis convention.

**Critical gate:** Sam WARN-001 windowed-mode Niagara verification PASS (Option A or B routing per Matt + gandalf decision). WS2 execution does NOT begin until verification PASSes.

---

## 1. Visual register per § 11.2 + § 12.2 CANONICAL

| Property | Specification |
|---|---|
| **Scale** | Large + atmospheric — looms behind primitive cluster (per § 11.2 Matt verbatim) |
| **Edge effect** | Light-edge brush-stroke — glowing light highlights rune edges |
| **Color** | NO COLOR — runes drawn by light only; monochromatic luminous brush strokes |
| **Distinctness** | Categorical readability — runes recognizable as "signs" against cosmograph background; distinct from kit-cluster dots + figurative-nebula clusters |
| **LOD** | Visible at 1× zoom as atmospheric presence; details emerge at 2×+ per Phase 3 LOD pattern |

---

## 2. 7 sky cluster regions (per § 12.3)

| # | Cluster region | Rune assignment (canonical TBD via Pattern B; drax-discretion baseline per Phase 5 amendment) |
|---|---|---|
| 1 | Race / ancestry | TBD |
| 2 | Element / flow | TBD (Phase 4 amended deployment used I Ching trigram for Elements) |
| 3 | Weapon / craft | TBD |
| 4 | Power / mastery | TBD |
| 5 | Style / way | TBD |
| 6 | Harvest / rewards | TBD |
| 7 | Horizon / goal | TBD |

**Canonical rune-per-cluster assignment** deferred to Pattern B per § 12.13 + cross-language rune selection per locked pattern (substrate-led; per-meaning match across Cuneiform / Norse Runes / I Ching / Enochian / etc.).

WS2 implementation absorbs canonical rune assignments when Pattern B locks. Mantis can implement against placeholder rune-glyphs initially + swap to canonical when locked.

---

## 3. Niagara implementation scope per sub-phase

### Phase WS2.1 — Niagara nebula rendering at celestial-sphere geometry
- Render 7 cluster region nebula structures volumetrically on spherical-shell celestial sphere interior
- Composes with § 2.6 spherical-shell geometry lock
- Per-cluster atmospheric depth + 3D context per Earth-Avatar canonical
- Acceptance: 7 distinct cluster regions volumetrically rendered

### Phase WS2.2 — Rune-anchor light-edge brush-stroke rendering
- Each cluster region carries its assigned rune (Phase 5 amended baseline or canonical post-Pattern B)
- Rune rendered per § 11.2 visual register (large + atmospheric + light-edge + no color + drawn by light only)
- Looms behind primitive cluster (per Matt verbatim)
- Acceptance: 7 runes rendered atmospherically; visual register matches canonical spec

### Phase WS2.3 — Cycling-preview response animation
- Highlighted cluster (from iPad cycling input) illuminates + camera focuses
- Other clusters dim
- Smooth ~0.3-0.5 sec transitions per § 12.4
- Camera fly-through between clusters as cycling progresses
- Acceptance: cycling produces cosmograph response; animation smooth

### Phase WS2.4 — Constellation overlay (kit-as-constellation per cosmograph-pivot § 10)
- 423-entry zodiac corpus constellations rendered as star-figure overlay within celestial sphere
- Each kit binds 1:1 to constellation per Phase 2 elrond MVP assignments
- Constellation layer composes with cluster-region nebula layer (distinct visual layers per § 12.2 split)
- Acceptance: 423 constellations renderable; kit-as-constellation visible

### Phase WS2.5 — WS2 close report
- Per-acceptance-criterion verdict
- Performance metrics at AAA fidelity (60 FPS target per § 12.4 implied)
- Cycling animation timing observations
- Cluster spatial layout final + tradeoff observations
- Methodology hotspots flagged
- Gap notes for vertical-slice spike integration

---

## 4. Acceptance criteria

| # | Criterion |
|---|---|
| 1 | Sam WARN-001 windowed-mode Niagara verification PASS (Option A or B per Matt + gandalf decision) |
| 2 | 7 cluster region nebula structures rendered volumetrically on spherical-shell celestial sphere |
| 3 | 7 cluster-runes rendered per § 11.2 visual register (large + atmospheric + light-edge brush-stroke + no color) |
| 4 | Cycling-preview cosmograph response animation operational (highlighted cluster illuminates; others dim) |
| 5 | Camera fly-through smooth at ~0.3-0.5 sec transitions per § 12.4 |
| 6 | 423-entry constellation overlay renderable |
| 7 | Kit-as-constellation visible (per Phase 2 elrond MVP assignments) |
| 8 | Performance: 60 FPS at AAA fidelity per TSR+TAA per mantis 3.6 criterion |
| 9 | Composition with WS1 (DataTables ingested per WS1 commission) operational |
| 10 | Sam Gate-2 review PASS or PASS-WITH-WARN |
| 11 | David-H wave-close memo authored + committed + pushed per PC-seam standing pattern |
| 12 | No raw LLM player-facing content (D7) |

---

## 5. Discipline citations

- **Discipline #18.2 (methodology consultation timing at extension hotspots)** — Niagara cluster-rune rendering is extension of MCP bridge spike capability; methodology consultation fires AFTER baseline cluster rendering attempt
- **D7 AI-tell line** — rune visual register hand-curated; no runtime LLM
- **D8 mobile-friendly** — UE rendering optimized for iPad-class hardware per Earth-Avatar architecture
- **Tal Rasha § 4.5 commission scope expansion** — WS2 fires per Branch A operational
- **Sam WARN-001 windowed-mode verification gate** — load-bearing pre-fire criterion; WS2 does NOT execute until verification PASSes per Option A or B
- **Discipline #46 (db-streaming + anti-materialization)** — Niagara constellation rendering streams from DataTables; doesn't materialize all 423 constellations at once

---

## 6. Out of scope

- ❌ Per-primitive iconography rendering (RETIRED per § 12.10; cosmograph carries cluster-runes only)
- ❌ Tier 2 selection UI (iPad-side; drax Phase 5 amendment scope)
- ❌ Materialization cinematic (WS3 commission)
- ❌ Spirit form 3D model rendering (deferred to Meshy + Control Rig pipeline)
- ❌ Earth avatar + grassy knoll scene assembly (vertical-slice spike scope)

---

## 7. Composition with prior work

- WS1 (data layer ingestion) — WS2 consumes ingested DataTables
- MCP bridge spike GREEN (db-lyon validated) — WS2 fires per same tooling
- Tal Rasha § 4.5 commission scope expansion — WS2 IS that scope expansion
- § 12 canonical lock — WS2 operationalizes § 12.2 sky surface
- Phase 4 amended /forge GREEN — 2D web prototype informs spatial layout intent
- Phase 5 amended /forge (post-close) — cycling-preview animation timing reference

---

## 8. Sign-off

**Authored:** gandalf 2026-06-10 per Matt directive ("fire A") + § 12 canonical lock + Tal Rasha § 4.5.
**Authority:** gandalf cross-cutting commission authority + Matt direct authorization.
**Routing:** david-h orchestrates PC-side execution; mantis executes; sam Gate-2.
**Gates on:** Sam WARN-001 windowed-mode Niagara verification PASS per Option A or B (queued Matt + gandalf decision per David-H consultation memo `2026-06-10-consultation-mac-kr-niagara-verification-and-ws2-routing.md`).
**Empirical-evidence triggers:** WS2 GREEN → vertical-slice spike assembly unblocked (composes WS1 + WS2 + WS3).
**Composition:** all prior canonical commitments preserved.
**End of commission.**
