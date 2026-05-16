# Dispatch — elrond viability-gate structural review (Pimen sample)

**Status:** COMPLETE — 2026-05-16 (Completion section appended)
**Target:** elrond (structural-track reviewer per AGENTS.md § Viability-gate workflow)
**Branch:** main (collaboration repo — verdict lands here)
**Tag intent:** No tags — verdict file is the deliverable.

## Context

Legolas completed his Pimen Mode-B sample crawl (`research/catalogue/pimen/sample-2026-05-16.json` — 20 rows, ~30 KB, captured per the released commission). Per AGENTS.md § Viability-gate workflow, three parallel reviewers must verdict on the sample before Pimen full crawl is released:

- **Structural track (this dispatch)** — you (elrond)
- **Wiring track** — drax (separate dispatch)
- **Design track** — gandalf (separate dispatch)

Your three verdicts collectively determine: PASS → full Pimen crawl released; CONDITIONAL → re-sample with adjustments; FAIL → skip Pimen, document rejection rationale.

This is **distinct from your earlier catalogue-rubric-schema work** (which drax reviewed for wireability and you closed-out today). This dispatch is sample-data review — does the actual Pimen data the schema describes work for the project?

## Your review focuses on

Per AGENTS.md § Viability-gate workflow structural-track criteria + your own elrond.md § viability-gate role:

1. **Metadata completeness across required fields.** Per Legolas Mode-B spec, each row should have: asset_id, source, url, name, category, dimensionality, style_register, style_tags, decomposition, file_format, license, cost, crawl_date, pimen_element + the six rubric axes (resolution_band, palette_size, shading_technique, linework_style, animation_frame_density, derived stylistic register). Scan the 20 rows. Which fields are universally populated? Which are flagged "unknown" and is that operationally tolerable at full-crawl scale or a problem?
2. **Schema-fit.** Do the rows insert cleanly into `catalogue_assets` per your schema (`research/curated/catalogue-schema.md`) without type-coercion gymnastics? Test if needed by attempting an insert into the empty catalogue.db.
3. **License clarity.** Sample row 1 shows `license: "commercial-royalty-free"` — is this unambiguous in your license enum, or does Pimen's actual license text need closer mapping?
4. **Decomposition signal coherence.** Sample shows `decomposition: "not-applicable"` for VFX — does this map cleanly to your schema's decomposition enum (was it `monolithic / decomposed / partial / unknown` per Legolas spec)? If "not-applicable" isn't a current enum value, propose a schema adjustment or a tagging-guide refinement.
5. **Style-register inferability.** The six rubric axes (resolution_band, palette_size, etc.) are marked "unknown" in some sample rows. This is expected without download access — Legolas can't inspect frames directly. **What's the resolution path?** Curators inspect assets manually post-acquisition? Defer rubric tagging to post-purchase? This is a real operational question for full-crawl scaling.

## What you do NOT review

- Pixi.js consumption viability (drax's track)
- Thematic/style-register design fit (gandalf's track)
- Whether to buy specific Pimen packs (Matt's decision; downstream of all three verdicts)

## Verdict format

Write your verdict to: `agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md`

Structure:

```markdown
# Finding — 2026-05-16 — elrond structural-track Pimen sample review

**Reviewer:** elrond
**Severity:** PASS | PASS WITH FLAGS | NEEDS REWORK
**Target:** Legolas Pimen sample (20 rows)
**Track:** structural (viability-gate of three)

## Verdict (one line)

## Per-criterion assessment
### 1. Metadata completeness
### 2. Schema-fit
### 3. License clarity
### 4. Decomposition signal coherence
### 5. Style-register inferability + resolution path

## Schema or pipeline refinements recommended (if any)

## What this unblocks (if PASS)
Full Pimen crawl release; expanded source crawls.

## What this blocks (if NEEDS REWORK)
Specifically what re-sampling adjustments are needed.
```

## Authority boundary

You don't have veto on the sample itself (that's a downstream-of-three-verdicts gate decision). Your verdict is **structural quality assessment**. Genuine schema-vs-data mismatches are your call to surface and recommend fixes for. Cross-track conflicts (e.g., your structural verdict differs from drax wiring or gandalf design) get synthesized by knight-rider into the gate decision; if architectural, escalate to Matt.

## Sequencing within your session

This dispatch sits alongside two others in your queue: A (research.db retirement) and B (Yomi provenance audit) — both 2026-05-16 dispatches. Pick the order that serves the work. My suggested order: A (small, ~30-60 min) → this structural review (~30-60 min) → B (investigative, 1-2 hours). But your call.

## Required reading

- Legolas Pimen sample: `research/catalogue/pimen/sample-2026-05-16.json`
- Your own schema: `research/curated/catalogue-schema.md` + `catalogue-rubric-schema.md`
- Your own AGENT_STATE.md (left state from last session)
- AGENTS.md § Viability-gate workflow (the three-track protocol)
- `~/.claude/agents/elrond.md` § viability-gate role

## Completion — elrond, 2026-05-16

### Verdict

**PASS WITH FLAGS.** Full verdict file: `agentic_orchestration/qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md`.

The sample fits the v1.0 catalogue schema cleanly — empirically validated by three representative-row insertion tests (one per category: paid clean VFX, free monolithic enemy, free rubric-ambiguous VFX) and two counter-tests confirming CHECK constraints reject raw vendor-prose values. No blocking schema mismatches; four flags describe curation-pipeline pre-processor rules needed before live curation, not schema rework.

### Three-track convergence

| Track | Reviewer | Verdict | File |
|---|---|---|---|
| Wiring | drax | PASS WITH FLAGS | `qa/findings/2026-05-16-drax-pimen-sample-wiring-review.md` |
| Design | gandalf | PASS | `qa/findings/2026-05-16-gandalf-pimen-sample-design-review.md` |
| **Structural** | **elrond** | **PASS WITH FLAGS** | **`qa/findings/2026-05-16-elrond-pimen-sample-structural-review.md`** |

All three tracks converge on operational pipeline rules; **no schema or content rework required**. Pimen full-crawl is greenlit at the viability-gate level — knight-rider's call to release.

### Flags filed (curation-pipeline, not schema)

1. **`file_format` parser** — Pimen ships prose strings ("PNG, RAR archive (11 kB)"); CHECK constraint rejects raw. Curator-side 15-line parser maps to closed enum.
2. **`style_register: "pixel-art"` derivation rule** — parent value doesn't map directly to axis-6 enum; sub-register tag (`hand-drawn-pixel` / `sub-register-uncertain`) drives derivation; conservative default routes to `manual-review` queue.
3. **`pimen_element` convention** — vendor-specific element tag → preserve in `source_metadata_raw` + emit `asset_style_tags.tag = 'pimen-element:<value>'` for queryability.
4. **Multi-category pack split** — packs containing assets across `category` enum boundary (`earth-spell-effect-03` VFX+enemy; Mega Pack VFX+UI) emit multiple `catalogue_assets` rows with same `pack_id`, distinct `source_asset_id` suffix.

Plus operational discipline:

5. **Post-acquisition visual-inspection workflow** — `palette_size` / `shading_technique` / `linework_style` are universally `unknown` from vendor metadata (no vendor will supply these without frame access). Curator post-purchase pass backfills observed values; ~2 min per asset; ~3 hours for full Pimen crawl of ~100 assets. Document in `curation-pipeline.md`.

### What this unblocks

Pimen full-crawl release (knight-rider sequences with Legolas). Order can be either:

- **(a) Crawl-then-pipeline:** Legolas crawl now; elrond implements `curate_catalogue.py` with flag rules after raw output arrives. (~1-2 days curation script implementation.)
- **(b) Pipeline-then-crawl:** elrond implements `curate_catalogue.py` against the 20-row sample first; validates pipeline behavior; then full crawl is mechanical. (~Same total effort, different sequencing.)

Knight-rider's call. My slight preference is (b) — validates pipeline rules against the smaller sample before scaling — but (a) is fine too.

### What this blocks

**Nothing.** Pipeline-implementation work is the natural next dispatch in my queue regardless of crawl timing.

### Optional follow-on if knight-rider wants

If knight-rider wants the four pipeline rules formalized in `curation-pipeline.md` + `curator-tagging-guide.md` BEFORE crawl release, that's a ~30 min deliverable. Otherwise the rules land naturally during pipeline implementation.

### Schema state

`catalogue.db` returned to empty post-test (verified). No artifact left from the schema-fit test. Schema lock v1.0 unchanged.

— elrond, 2026-05-16
