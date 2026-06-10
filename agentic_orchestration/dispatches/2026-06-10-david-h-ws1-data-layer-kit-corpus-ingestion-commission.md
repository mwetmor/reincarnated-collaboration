# David-H WS1 Commission — UE Data Layer Port (Kit Corpus + Substrate Ingestion via db-lyon)

**STATUS:** ACTIVE (commission ready to fire post Niagara verification close)
**Date:** 2026-06-10
**Author:** gandalf
**Authority:** Matt 2026-06-10 — "fire A then prompt B via KR then prompt C via DH" + § 12 canonical lock (commit 861403d) + canonical Branch A architecture
**Audience:** david-h (PC orchestrator); mantis (executor); sam (Gate-2 PASS-WITH-WARN baseline)
**Companion docs (read first):**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 1-§ 12 (foundational architecture; § 12 LOCKED 2026-06-10)
- `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` (db-lyon empirically validated for data layer)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A operational)
- `agentic_orchestration/elrond/notes/2026-06-09-kit-to-star-sign-mvp-assignment-close.md` (Phase 1 kit-to-star-sign MVP)
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/synthesis.md` (423-entry zodiac corpus)

---

## 0. TL;DR

**Mission:** Port engine-pregenerated kit corpus + substrate-trace + Phase 2 elrond kit-to-star-sign assignments + Legolas zodiac corpus into UE DataTables via db-lyon `fill_datatable_from_json` action per MCP bridge spike PASS-WITH-WARN.

**Empirical trigger:** MCP bridge spike GREEN at db-lyon `7 Sequencer actions PASS / 26 tool tests PASS / DataTable CRUD 7/7 PASS`; Branch A canonical lock (Tal Rasha + § 10 + § 11 + § 12); kit-to-star-sign Phase 2 MVP shipped (37 kits × star_sign_id sidecar).

**Substrate consumed:**
- 1000-kit substrate-trace (current /forge baseline)
- Engine kit corpus (current cycle-14 output; reincarnated-engine seasons dir)
- Phase 2 elrond kit_star_sign_assignments.json sidecar (loadout repo)
- 423-entry Legolas zodiac corpus
- 20-family atomic-substrate-registry primitives

**Estimated wall-clock:** 1-3 weeks UE mantis work per Mantis convention.

---

## 1. WS1 scope per § 12 + Branch A architecture

### 1.1 DataTable schemas needed (mantis authors C++ struct definitions)

| DataTable | Source JSON | Used by |
|---|---|---|
| **DT_Kit** | Engine kit corpus per cycle-14 output | WS2 cosmograph rendering + WS3 materialization cinematic |
| **DT_KitStarSign** | Phase 2 elrond `kit_star_sign_assignments.json` | WS2 constellation overlay; vertical-slice spike Tier 1 commit display |
| **DT_StarSign** | Legolas `corpus.yaml` (423 entries) | WS2 cosmograph constellation anchors; cluster-rune-sky integration |
| **DT_PrimitiveFamily** | Atomic-substrate-registry Layer 0 (20 families) | WS2 sky cluster spatial layout; § 12 Tier 1 anchor mapping |
| **DT_ExperientialAxis** | Hypothesis-flow § 1.8 multi-axis architecture | § 12 Tier 1 anchors 5-7 (Power/Style/Harvest/Horizon) |

### 1.2 Ingestion path

Per db-lyon validated capability:
1. mantis authors UE C++ structs matching JSON schemas (one per DataTable)
2. mantis registers structs in UE project; compiles
3. mantis creates empty DataTable assets in Content Browser
4. mantis invokes db-lyon `fill_datatable_from_json` per DataTable with source JSON path
5. mantis verifies row counts + sample row inspection
6. mantis commits + pushes per PC-seam standing wave-close pattern

### 1.3 Source JSON staging

JSON sources live at Mac-side meta-repo + engine-repo + loadout-repo paths. PC-side requires:
- Mac → PC sync via git (already operational per CLAUDE.md addendum)
- OR direct fetch via Pi middleware (deferred per Pi infrastructure architecture)

Default: git-tracked JSON sources flow Mac → origin → PC per existing pull discipline.

---

## 2. Acceptance criteria

| # | Criterion |
|---|---|
| 1 | 5 DataTables defined with C++ struct backing |
| 2 | All 5 DataTables ingest source JSON via db-lyon `fill_datatable_from_json` |
| 3 | Row counts match source JSON entry counts (kit corpus / 37 kit-sign assignments / 423 star-signs / 20 primitive families / experiential axes) |
| 4 | Sample row inspection passes (data integrity verified per DataTable) |
| 5 | DataTable assets persist post-save (Editor close + reopen + verify) |
| 6 | Cross-DataTable foreign keys resolvable (kit_id ↔ star_sign_id ↔ primitive_family_id) |
| 7 | Sam Gate-2 review PASS or PASS-WITH-WARN |
| 8 | David-H wave-close memo authored + committed + pushed per PC-seam standing pattern |

---

## 3. Discipline citations

- **Discipline #46 (db-streaming + anti-materialization)** — DataTables are materialized JSON ingest; respect db-streaming discipline for downstream consumers (don't materialize sub-tables at runtime)
- **Sam WARN-002 Blueprint-mutation pre-fire gate** — exercise Blueprint mutation BEFORE MCP-driven scene authoring (separate gate; vertical-slice spike scope)
- **D7 AI-tell line** — JSON ingestion is engine-output pre-generated; no runtime LLM
- **ADR-006** — read-only-by-default external systems; db-lyon BUSL-1.1 base evaluation grant covers WS1
- **Recognition-validate-commit** — WS1 is empirical validation of db-lyon tooling at production scope

---

## 4. Out of scope

- ❌ Niagara VFX rendering (WS2 commission)
- ❌ Materialization cinematic (WS3 commission)
- ❌ Vertical-slice spike assembly (separate commission amendment)
- ❌ Spirit form 3D model + rigging (deferred to Meshy + Control Rig pipeline; per asset-pipeline canonical)
- ❌ AAA fidelity visuals (deferred per WS2 + asset pipeline)

---

## 5. Composition with prior work

- MCP bridge spike GREEN (db-lyon validated; commit `aaaeb85` + Sam `3eaf178`)
- Branch A canonical (cosmograph-pivot § 10 + Earth-Avatar § 11 + § 12)
- Phase 2 elrond MVP (commit `5552c9a` loadout repo + `e195390` meta-repo)
- Legolas zodiac corpus (N=423; `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/`)
- Atomic-substrate-registry CANONICAL

---

## 6. Sign-off

**Authored:** gandalf 2026-06-10 per Matt directive ("fire A").
**Authority:** gandalf cross-cutting commission authority + Matt direct authorization.
**Routing:** david-h orchestrates PC-side execution per federated PC team architecture; mantis executes; sam Gate-2.
**Empirical-evidence triggers:** WS1 GREEN → WS2 (Niagara rendering against ingested data) + WS3 (Sequencer materialization against ingested data) unblocked; vertical-slice spike assembly composes WS1 + WS2 + WS3.
**Composition:** all prior canonical commitments preserved.
**End of commission.**
