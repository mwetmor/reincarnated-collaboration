# Dispatch — elrond catalogue rubric + DB schema + curation pipeline (2026-05-16, revised)

**Status:** COMPLETE — 2026-05-16
**Target:** elrond (data steward — Tier C+ with steward authority within data domain)
**Branch:** main (collaboration repo — Elrond's work lands here)
**Tag intent:** No code tags — this dispatch produces schema docs + rubric design + empty DB + curation pipeline. The DB file is gitignored; design docs are committed.

**Supersedes:** Earlier draft of this same dispatch focused purely on catalogue DB schema. Revised 2026-05-16 to incorporate gandalf's catalogue-rubric commission (`agentic_orchestration/gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md`).

## Context

Two work streams converge in this single dispatch:

1. **Catalogue rubric design** — gandalf has filed a commission request to operationalize the locked style-register decision (`canonical/story/style-register.md`). The locked register categories are design-conversation-precise but operationally vague — two curators tagging the same asset can land in different categories. The rubric must provide axis-based precision sufficient for curator-tagging consistency, consumption-time filtering reliability, and pivot-insurance compatibility per AGENTS.md § score-don't-filter.
2. **Catalogue DB schema + curation pipeline** — independent of the rubric, the broader catalogue layer needs schema definition, empty DB creation, curation pipeline plan, and MIGRATION.md. These two pieces are deeply intertwined — the rubric IS part of the DB schema — so they're combined into one dispatch.

Per Matt's 2026-05-16 directive, this is **Option B (gandalf-direct dialogue)** — Elrond invokes gandalf directly via Pattern A subagent or Pattern B sustained dialogue (your call which serves the work better) rather than routing all coordination through knight-rider. Five specific topics worth dialoguing on are listed below.

**Priority:** Not urgent. Catalogue work is multi-week+; no operational blocker. Land when you have capacity to engage.

## Gandalf's input — proposed rubric axes

Treat these as **gandalf's starting proposal**, not as locked spec. If curation experience surfaces gaps or refinements, amend in dialogue.

| Axis | Suggested checkable values | What it distinguishes |
|---|---|---|
| **Sprite resolution range** | 16-32px / 32-64px / 48-128px / 96-256px / 256+px | Retro tends lower; HD-2D pixel tends middle; raster tends higher |
| **Palette size** | ≤16 / 17-64 / 65-256 / 256+ (truecolor) | Retro restricted; hand-drawn pixel expansive; raster truecolor |
| **Shading technique** | flat-fill / single-step / dithered / gradient-ramp / painterly | Retro flat-or-single-step; hand-drawn pixel dithered/ramped; raster painterly |
| **Linework style** | hard-1px-outline / soft-outline / variable-width / no-outline | Retro hard 1px; hand-drawn pixel variable-or-absent; vector hard-clean |
| **Animation frame density** | 2-4 / 5-8 / 9-12 / 13+ per cycle | Retro lower-frame; hand-drawn pixel 6-12; cinematic higher |
| **Stylistic register** (derived) | retro-16bit / hand-drawn-illustration / clean-vector / painterly-raster / anime-cel | Qualitative aesthetic tag, derived from axes 1-5 plus subjective check |

The first five are **mechanically checkable** (look at asset; vendor metadata; direct inspection). The sixth is the **derived classification**, computable deterministically from the others plus a final aesthetic-pattern check.

**Reincarnated's locked register, expressed against these axes** (per gandalf's commission):

| Layer | Resolution | Palette | Shading | Linework | Animation | Derived register |
|---|---|---|---|---|---|---|
| Combat tier | 32-128px | 32-256 | dithered or gradient-ramp | variable-width or no-outline | 6-12 frames | hand-drawn-illustration |
| Narrative-moment tier | 96-512px | 64-256 | gradient-ramp or painterly | no-outline | static or 12+ frames | hand-drawn-illustration |

The consumption-time filter for Drax / Star-lord becomes a multi-axis query returning assets matching this tag profile.

## Deliverables (five — combined from gandalf's commission + broader catalogue DB needs)

### 1. Schema definition

Two parts:

**(a) Style-register rubric schema** — table or column structure implementing the six axes above. Lives in `agentic_orchestration/research/curated/catalogue-rubric-schema.md` as a design doc, AND as columns in the catalogue DB.

**(b) Broader catalogue DB schema** — `agentic_orchestration/research/curated/catalogue-schema.md`. Covers:
- `catalogue_assets` table — per-asset rows with all 12+ fields from Legolas Mode B specification + the six-axis rubric columns from (a) above
- Normalization tables if appropriate (`catalogue_sources`, `catalogue_style_tags`, etc.)
- Types, constraints, indexes
- Source-anchoring (every row traces to origin)
- Versioning (parallel to engine's `schema_meta` pattern)

### 2. Curator-tagging guidance document

`agentic_orchestration/research/curated/curator-tagging-guide.md` — for each rubric axis, **how a curator determines the value** when looking at an asset. Includes worked examples per axis showing which Pipoya / CreativeKind / Foozle / CraftPix / pimen / etc. assets land in which value bucket per the empirical asset landscape file (`research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`).

Critical objective: **two different curators tagging the same asset should arrive at the same register classification.**

### 3. Deterministic classification rule for derived stylistic register (axis 6)

Given values on axes 1-5, what's the rule that returns the register classification? May admit `manual-review` as an output for genuinely ambiguous cases.

Document the rule explicitly — flowchart, decision table, or pseudocode — in the curator-tagging guide or a sibling file.

### 4. Validation pass on existing research

Re-classify the listed vendors / packs in `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` against the proposed axes. Surface any cases where the categorization is unstable (e.g., a vendor that scores between hand-drawn-pixel and retro depending on how axes are interpreted). Refine axes if needed before locking.

Output: a structured validation report — could be a sibling markdown doc, could be inline in the curator-tagging guide, your call.

### 5. MIGRATION.md + empty DB created

- `agentic_orchestration/research/curated/MIGRATION.md` — v1.0 entry documenting the initial schema
- `agentic_orchestration/research/curated/catalogue.db` — empty SQLite file with schema applied; gitignored
- `agentic_orchestration/research/curated/curation-pipeline.md` — operational doc covering input contract (Legolas raw output), curation steps (deduplication, normalization, quality filtering, axis tagging, license-clarity flagging), rejection criteria, provenance preservation, schema migration policy

## Direct-dialogue protocol with gandalf — REQUIRED

Matt's explicit instruction (relayed via gandalf's commission): **invoke gandalf directly** to discuss this rubric work. Pattern A (subagent invocation from your session) OR Pattern B (sustained terminal session) — your call which serves the work better.

**Five specific topics worth dialoguing on:**

1. **Is the derived stylistic-register classification (axis 6) genuinely deterministic from axes 1-5, or does it need additional axes?** Gandalf has design instinct on this; you have schema-rigor lens. Surface friction.
2. **Vendors who ship across registers** — e.g., CraftPix has both pixel AND vector packs. Does the rubric tag at the vendor level, the pack level, or the per-asset level? What's the right granularity?
3. **Assets that score "between" categories on multiple axes** — what's the resolution path? `manual-review` flag? Force a primary register and tag the secondary? Dialogue-worthy.
4. **Non-humanoid-monster-sprite coverage** (per `canonical/story/enemy-visual-legibility.md` § Cross-references) — does this need its own sub-rubric or integrate cleanly into the proposed six axes?
5. **License / cost metadata structure** — mentioned in AGENTS.md viability-gate structural track but not detailed in gandalf's commission. Worth dialoguing on the right structure (per-asset / per-pack / per-vendor with override).

**How to wire:** open the dialogue at your session start (or after initial schema sketch — your call on timing). Capture outcomes in the rubric deliverables AND surface back to knight-rider for cross-team awareness.

Knight-rider does NOT need to be present during the dialogue. Direct gandalf-elrond coordination is the explicit Matt-approved pattern here.

## Cross-seam coordination

- **Legolas Pimen sample dispatch** is **held** until your rubric lands — so the sample is tagged against the locked rubric from the start (no rework). When your rubric is ready, knight-rider releases the Legolas dispatch.
- **Star-lord** — engine telemetry is his seam; the cross-store boundary is documented in your existing audit. Cross-DB queries (engine telemetry × catalogue) routed via SQL ATTACH conventions.
- **Drax** — eventual consumer at consumption time. The rubric becomes his filter query.
- **Gandalf** — direct dialogue per above; viability-gate design-track reviewer once samples land.
- **Knight-rider** — receives schema doc + DB + rubric; will draft decisions-log entry for the rubric lock (per gandalf's commission item 5) once your work lands and we have Matt's approval.

## Acceptance

- Schema docs committed at `research/curated/catalogue-rubric-schema.md` + `research/curated/catalogue-schema.md`
- Curator-tagging guide committed at `research/curated/curator-tagging-guide.md`
- Deterministic classification rule documented (separately or inline)
- Validation pass on existing research done; report committed
- Empty catalogue.db created with schema applied; visible via `sqlite3 catalogue.db .schema`
- MIGRATION.md committed with v1.0 entry
- Curation pipeline plan committed
- Catalogue.db added to appropriate .gitignore
- **Direct dialogue with gandalf documented** — at minimum, a summary of which axes were refined through dialogue and what was decided
- **Drax wiring-track schema review completed** — see new acceptance step below
- Knight-rider notified at completion with: schema doc paths, DB confirmation, rubric outcome (axes locked / refined / amended), key dialogue outcomes, drax wiring-track verdict, readiness signal for Legolas Pimen sample release

## Drax wiring-track schema review (new acceptance step added 2026-05-16)

Per Matt's 2026-05-16 directive, drax (demo + loadout owner) reviews the schema **before this dispatch is declared complete and before Legolas's Pimen sample is released for crawl**. The intent: catch schema-vs-consumption mismatches early — better to surface them now than discover them when samples are already tagged against a flawed schema.

**Process:**

1. When Elrond's deliverables (schema docs, rubric, curator-tagging guide, classification rule, validation report) are drafted, Elrond signals knight-rider that the schema is ready for drax review.
2. **Knight-rider invokes drax** (Pattern A subagent OR Pattern B terminal — knight-rider's call based on drax's session state) to perform a wiring-track schema review.
3. **Drax assesses** along the wiring-track criteria the viability gate uses for samples — but applied to the SCHEMA itself:
   - **Pixi.js consumption viability** — can the demo's existing pipeline consume assets tagged against this schema? Which fields are directly usable? Which require demo-side adaptation?
   - **Sprite-archetype registry compatibility** — does the schema support the registry pattern locked in `enemy-visual-legibility.md` § S1?
   - **Style-register filter query feasibility** — can drax write a filter query that returns the locked HD-2D-shaped register? What does the query look like?
   - **Loadout app consumption** — for assets reaching the loadout app (gear, character display), does the schema provide what the React/Vite consumer needs?
   - **Demo viability in current state vs demo update needed** — Matt's explicit framing: does the demo CONSUME this schema as-is, or does drax need a demo-side schema-adaptation patch before catalogue assets can flow through?
4. **Drax produces a verdict** at `agentic_orchestration/qa/findings/2026-05-16-drax-elrond-schema-wiring-review.md`:
   - PASS — schema is wireable in current demo/loadout state; no adaptation patch needed before catalogue rollout
   - PASS WITH FLAGS — wireable but specific adaptations recommended; lists them with priority
   - NEEDS REWORK — schema requires changes before drax can wire it; specifies which fields / structures / patterns block consumption
5. **Elrond responds** to drax's verdict in dialogue (Pattern A subagent OR direct conversation):
   - PASS: no action; dispatch proceeds to completion
   - PASS WITH FLAGS: Elrond decides whether to address flags in this dispatch or defer to a follow-on; documents the decision
   - NEEDS REWORK: schema iteration required; second drax review after rework

This step is **load-bearing** — the dispatch is NOT complete until drax PASSES (or PASSES WITH FLAGS with Elrond's documented response). This protects against scenarios where catalogue samples are crawled and tagged before drax discovers a consumption gap.

**Authority note:** drax does NOT have schema-design authority — that's Elrond's domain. Drax's verdict is a wiring-viability assessment, not a schema veto. If drax flags a wiring issue, Elrond and drax dialogue to resolve. Genuine conflicts escalate to knight-rider; if architectural, to Matt.

## Required reading

- `~/.claude/agents/elrond.md` — your own definition; especially "First major task" + "Schema design principles" + "Authority"
- `~/.claude/agents/legolas.md` — Mode B field specification (your DB needs to accept his output)
- `~/.claude/agents/gandalf.md` — his ownership of style-register + design-track viability gate role
- `agentic_orchestration/gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md` — gandalf's original commission (this dispatch consumes that)
- `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` — your own audit; especially recommended-architecture section
- `canonical/story/style-register.md` — the locked canonical reference + the new "Operational precision — deferred to Elrond's rubric design" subsection
- `canonical/story/enemy-visual-legibility.md` — informs whether monster-sprite-specific columns / sub-rubrics are warranted
- `canonical/story/embodiment-narrative-layer.md` (when authored) — non-humanoid-form sprite needs
- `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical landscape Elrond validates the rubric against (deliverable 4)
- `AGENTS.md` § viability-gate workflow + score-don't-filter principle + authority tiers

## Completion record

Append to this file under a "Completion" section: all deliverable paths; key axis decisions (locked or refined per dialogue); gandalf-dialogue summary; any open questions for the first Legolas sample to inform; readiness signal for sample release.

---

## Drax wiring-track review completion entry

**2026-05-16 — drax wiring-track schema review: PASS WITH FLAGS**

Verdict file: `agentic_orchestration/qa/findings/2026-05-16-drax-elrond-schema-wiring-review.md`

Schema is wireable against both `reincarnated-demo/` and `reincarnated-loadout/` in current state. No demo-side adaptation patch required before catalogue rollout. Three flags filed for Elrond's documented response: (1) `file_format` column needs a CHECK constraint with a closed enum before first crawl inserts — moderate priority; (2) confidence threshold convention for loadout tag display — low priority, defer to S1 registry dispatch; (3) `catalogue_sources.default_license` CHECK still carries `'itch-standard'` which was dropped from the per-asset license enum — fix in DDL before DB is created. Five missing artifacts identified (MIGRATION.md, .gitignore, catalogue.db, curation-pipeline.md, pivot-insurance-ledger.md, catalogue-rubric-validation doc) — dispatch-completion blockers per acceptance criteria but not wiring-track blockers. Legolas Pimen sample dispatch may proceed.

---

## Completion — elrond, 2026-05-16

### All deliverables committed

| # | Deliverable | Path |
|---|---|---|
| 1a | Style-register rubric schema (six-axis, v1.0 locked post-gandalf dialogue) | `agentic_orchestration/research/curated/catalogue-rubric-schema.md` |
| 1b | Broader catalogue DB schema (v1.0 design locked; pending Matt approval per ADR-002) | `agentic_orchestration/research/curated/catalogue-schema.md` |
| 2 | Curator-tagging guide with per-axis worked examples for all major vendors | `agentic_orchestration/research/curated/curator-tagging-guide.md` |
| 3 | Deterministic classification rule for axis 6 — decision table with rules R1-R8 + curator-override / manual-review escalation ladder | `agentic_orchestration/research/curated/catalogue-rubric-schema.md` § 3 (+ curator-guide § 11) |
| 4 | Validation pass — 22 vendor/pack patterns re-classified against the rubric | `agentic_orchestration/research/curated/catalogue-rubric-validation-2026-05-16.md` |
| 5a | MIGRATION.md v1.0 entry | `agentic_orchestration/research/curated/MIGRATION.md` |
| 5b | Empty catalogue.db with schema applied (gitignored) | `agentic_orchestration/research/curated/catalogue.db` |
| 5c | Curation pipeline operational contract | `agentic_orchestration/research/curated/curation-pipeline.md` |
| 5d | Pivot-insurance ledger (gandalf dialogue Topic 6 addition) | `agentic_orchestration/research/curated/pivot-insurance-ledger.md` |
| 5e | Schema migration script | `agentic_orchestration/research/scripts/catalogue_migrations/v1_0_initial.sql` |
| 5f | `.gitignore` for catalogue.db family | `agentic_orchestration/research/curated/.gitignore` |
| — | AGENT_STATE update | `agentic_orchestration/research/curated/AGENT_STATE.md` |

### Key axis decisions (post-gandalf-dialogue, locked v1.0)

| Topic | Status | Decision |
|---|---|---|
| Axis 6 determinism | REFINED | Rule-derived with documented exceptions R6 (CreativeKind hard-outlined hand-drawn-pixel) + R7 (Foozle boundary cluster with default-borderline). R6 side-effect: mandatory `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` tag — scene-level filters constrain to one profile per Octopath HD-2D precedent. |
| Per-asset vs per-pack vs per-vendor granularity | ACCEPTED+ | Per-asset is canonical. Addition: `catalogue_packs.pack_register_consistency` advisory column (`consistent / mixed / unknown`) populated post-curation. |
| Between-categories assets | REFINED | Three-step ladder: (a) exception rules in table; (b) curator-override with audit-trail (rule-bug threshold: >10% corpus OR >5 on single clause); (c) `manual-review` queue → `gandalf-call` only for register-genuinely-ambiguous cases. |
| Non-humanoid embodiment | PARTIALLY REJECTED | v1.0 enum = 8 starter embodiments + `pending-amendment` + `not-applicable` + `unknown`. New `pending_amendment_hint` column captures form-read; amendment-gated promotion to canonical via `embodiment-narrative-layer.md` amendment protocol. Pre-loading expansion slots was rejected — would let catalogue data define narrative canonicity. |
| License / cost structure | REFINED | `commercial-license` split into four narrower values (`commercial-royalty-free / commercial-per-project / commercial-royalty-bearing / commercial-license`). `itch-standard` DROPPED (forced read). >20% `unknown` license in a sample fails design-track viability gate on data-hygiene grounds. |
| Pivot-insurance ledger (gandalf-added) | ACCEPTED | Curation pipeline appends per-pass coverage summary; threshold flags surface silent pivot-insurance erosion. Asymmetric-stewardship analogue of Discipline #13. |

### Drax wiring-track flag responses

- **Flag 1 (file_format CHECK constraint):** RESOLVED IN v1.0. Closed enum added to `catalogue_assets.file_format` (17 values). DDL updated, DB recreated, smoke-tested.
- **Flag 2 (loadout confidence threshold):** DEFERRED per drax's own recommendation; defer to S1 registry dispatch.
- **Flag 3 (`catalogue_sources.default_license` itch-standard):** RESOLVED IN v1.0. Migration SQL was already correct; design doc had stale references (3 occurrences: `catalogue_sources` CHECK, `catalogue_packs.pack_license` CHECK, an example SQL query). All fixed. DB verified.

### Gandalf-dialogue summary

Pattern-A subagent dialogue 2026-05-16. Five named topics + one gandalf-added (pivot-insurance ledger). Strong design pushback on Topic 4 (embodiment expansion slots) and Topic 1 (R6 outline-profile sub-tag for scene coherence per Octopath HD-2D precedent). Full record in `catalogue-rubric-schema.md` § 9.

### Open questions for the first Legolas sample to inform

The first Pimen Mode B sample will be the first real curation pass against this rubric. Items the sample will surface or confirm:

1. **R6 prevalence.** How many Pimen assets land in R6 vs R5? If R5 dominates, R6 is the well-behaved exception. If R6 is common, scene-coherence outline-profile constraint becomes a load-bearing consumption pattern.
2. **R7 activation.** Does Pimen produce any R7-boundary assets? Probably no (Pimen is firmly `hand-drawn-pixel` register). Validates R7's narrow targeting.
3. **License clarity.** Pimen's commercial terms — `commercial-royalty-free`, `commercial-license`, or something else? Confirms the license-enum value set is right-sized for the predominant vendor pattern.
4. **Decomposition signal.** Spell-effect packs are typically `not-applicable` for decomposition. Confirms the schema's category-aware decomposition handling.
5. **Embodiment coverage.** Pimen is VFX-only — no character/enemy/embodiment assets. The first embodiment-bearing sample (LuizMelo? Elthen?) will exercise the `pending-amendment` pattern (LuizMelo Skeleton pack expected to trigger it).

### Readiness signal for Legolas Pimen sample release

**GREEN — ready for release.**

The rubric is locked. The DB schema is design-locked v1.0 with Drax wiring verdict PASS. The migration SQL applies cleanly to an empty DB. Drax's flags addressed. Curator-tagging guide is comprehensive for the named vendors. Validation pass demonstrates the rubric admits the empirical landscape.

Pending items that do NOT block sample release:
- Matt approval on the schema lock (per ADR-002) — required before live curation begins, but Legolas's Mode B sample crawl can start since the sample is raw output, not curated data
- Curation script implementation — deferred until sample lands (no point implementing without data)
- Decisions-log entry for the rubric lock — knight-rider drafts when convenient
- `embodiment-narrative-layer.md` cross-reference for `pending-amendment` pattern — gandalf owns; surfaced via this completion

Knight-rider: dispatch the Legolas Pimen sample when sequencing permits. Recommended explicit instruction to Legolas to populate the six rubric axes from vendor metadata where possible (axes 1-5 are largely vendor-metadata-derivable for Pimen); set `unknown` where not determinable; tag `category = 'vfx'` for all Pimen assets; tag `embodiment_tag = 'not-applicable'`.

— elrond, 2026-05-16
