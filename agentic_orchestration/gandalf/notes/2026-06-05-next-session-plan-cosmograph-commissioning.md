# Next-Session Plan — Cosmograph Pre-Milestone Commissioning

**STATUS:** CURRENT (next-session plan; load-bearing for resume after wind-down)
**Date:** 2026-06-05
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-05 directive: "plan for next session as a doc and then let's wind down for the day"
**Companion:** `canonical/story/2026-06-05-cosmograph-pivot.md` (architectural commitment); ground-state entry as immediate-predecessor canonical

---

## 0. TL;DR

Next session resumes at the **cosmograph pre-milestone commissioning** phase. Pattern B scoping landed DP1-DP5 in the 2026-06-05 session; the next moves are operational commissions to elrond (substrate-trace extraction) and drax (cosmograph web build), composed in parallel. No new design calls required before commissioning unless a specific question surfaces. The wind-down state is clean: no in-flight Veo generations, no pending Matt-questions, no half-written canonical docs.

---

## 1. Where we left off (session-end state 2026-06-05)

### 1.1 Architectural commitments locked

- **Cosmograph pivot ratified.** Recognition record at `canonical/story/2026-06-05-cosmograph-pivot.md` (amended with engine-pre-generates / game-selects clarification).
- **Pre-milestone scoping DP1-DP5 locked:**
  - **DP1 — Data source:** combined QDX-5 + EAA-5 v2 corpus substrate-traces (~62 BC cells from `kit_archive.db`)
  - **DP2 — Embedding axes:** Tier 1 (element_primary, archetype, role_orientation, engagement_type, range_profile, mitigation_profile) + Tier 2 (survivability_tier, damage_focus, mobility_tier) substrate-primitive axes from the kit corpus
  - **DP3 — Visual encoding:** BC cell nodes color-tinted by element_primary; categorical anchors (BOSS-KILLER / SHADOW PRIMARY / etc.) as larger derived anchor nodes; no edges in minimum
  - **DP4 — Spirit-preview:** lasso → game-side compute centroid → lookup nearest pre-generated character in JSON packet → side panel displays matched kit's pre-computed identity (categorical labels, Q18 flavor identity, T4 selection)
  - **DP5 — Hosting:** sub-route on existing loadout app, likely `/forge`
- **T4 vocabulary amendment:** Duskweaver's T4 selection name **Penumbral Inversion Shell → Twilight Inversion Shell** per Matt 2026-06-05 directive. Captured in `2026-06-02-mm-p1-top-1-rename-duskweaver.md` § 6.
- **MM-P1 video production playbook PARKED.** Recontextualized as post-confirm cinematic-payoff playbook (not main self-validation surface). Status updated in `2026-06-02-mm-p1-self-validation-video-production-playbook.md` header.

### 1.2 Tooling state

- **Veo harness operational** at `~/Games/reincarnated-collaboration/duskweaver-mm-p1/veo_runner.py` (~140 lines Python). Tested + working against Gemini Developer API (`veo-3.1-generate-preview` model). 4 Clip 1 cosmos iterations executed (v1-v4) during the cosmograph-pivot recognition path; all output preserved in `duskweaver-mm-p1/clips/` as research evidence. Harness is parked but functional for post-confirm cinematic work.
- **API key stored** in `duskweaver-mm-p1/.env` (gitignored).
- **No in-flight Veo generations.** Background tasks all completed; nothing polling.

### 1.3 Doc state

- **Cosmograph recognition record:** authored + amended (engine-pre-generates / game-selects boundary).
- **Ground state (`canonical/00-ground-state.md`):** updated with cosmograph entry at top of CURRENT TRUTH table + Last-Updated note + epoch-shift indicator.
- **Season-archive-realm-expansion-pivot doc:** amended with 2026-06-05 cosmograph cross-reference note.
- **MM-P1 video playbook:** header PARKED-status note added.
- **Duskweaver rename doc:** T4 vocabulary amendment landed (Penumbral → Twilight).
- **QDX-5 governance lapse note:** urgency-elevation note added (cosmograph rendering quality gates on substrate richness).

### 1.4 Open work-tracks queued for next session

| Track | Owner | Scope | Status |
|---|---|---|---|
| Cycle-18 recovery-2 wave-close | knight-rider | Author wave-close record OR amendment for the recovery-2 delivery (page rewrite + new /kits route + sample nav deprecation); ratify recovery-2 as delivered → clean cycle close | NOT YET CLOSED — Matt 2026-06-05 ratification confirmed; KR to formalize |
| Substrate-trace extraction | elrond | Combined QDX-5 + EAA-5 v2 corpus → cleaned cell-coordinate vectors as `.csv` or `.parquet` for cosmograph ingestion | NOT YET COMMISSIONED |
| Page restore + cosmograph build (combined dispatch) | drax | Workstream A: restore `/loadout` to cycle-18 grid+featured+faction view, dissolve `/kits` route, extract rich-character-view component for reuse. Workstream B: build cosmograph at `/forge` using extracted component as side-panel preview. Combined dispatch to avoid double deploys. | NOT YET COMMISSIONED — gated on (a) recovery-2 KR close, (b) elrond substrate-trace delivery |
| Cinematic payoff design (parked) | gandalf + Matt | Re-engage Veo prompt design for post-confirm materialization moment when cosmograph milestone lands | PARKED — empirical-evidence trigger is cosmograph lasso→confirm flow operational |

---

## 2. Recommended next-session operational sequence

### Phase 1 — Session-start protocol (~15 min)

1. Read `canonical/00-ground-state.md` § 1 (current truth) and the cosmograph entry at top
2. Read `canonical/story/2026-06-05-cosmograph-pivot.md` (full record) — especially § 4.1 engine/game boundary and § 5 pre-milestone scoping
3. Read this next-session plan doc (you're here)
4. Skim `agentic_orchestration/gandalf/notes/2026-06-02-mm-p1-top-1-rename-duskweaver.md` § 6 (T4 vocabulary amendment)

### Phase 2 — Confirm scoping holds OR amend (~5-10 min Matt-check)

Short Matt-check: do DP1-DP5 still hold, or has further thinking surfaced amendments? If amendments, capture and update the recognition record before commissioning.

If scoping holds, proceed to Phase 3.

### Phase 3 — Commission elrond (substrate-trace extraction) [~30 min authoring]

Draft an elrond commission spec at `agentic_orchestration/gandalf/dispatches/2026-06-XX-elrond-substrate-trace-extraction.md` (or wherever the convention places dispatches; check knight-rider routing protocol).

Spec content:
- Source: combined QDX-5 + EAA-5 v2 corpus
- Required fields per row: kit_id, element_primary, archetype, role_orientation, engagement_type, range_profile, mitigation_profile, survivability_tier, damage_focus, mobility_tier, name (the LLM-renamed kit identity), t4_selection (with Twilight rename applied to kit_shadow_000007), categorical_labels (BOSS-KILLER / SHADOW PRIMARY / etc. — derived from coordinate position)
- Output format: `.csv` or `.parquet` consumable by drax frontend
- Field-cleanup notes: governance lapse on QDX-5 means cultural_tradition + period are NA; include these columns with NA values rather than omitting (drax may want to surface "substrate-thin" indicator)
- Acceptance criterion: file lands in agreed location with all 62 rows + agreed columns; drax can ingest without further data work
- Time budget: 1-2 hours elrond time
- Cost budget: ~$0 (no LLM calls; pure curation work)

### Phase 4 — Commission drax (combined: page-restore + cosmograph web build minimum) [~45 min authoring]

Matt 2026-06-05 directive: "bring back sample and loadout as they were" — `/loadout` should restore to cycle-18 original grid+featured+faction view; recovery-2's rich per-character view gets REPURPOSED as the cosmograph's side-panel character preview at `/forge` (work not lost; repositioned).

Draft a combined drax commission spec at `agentic_orchestration/gandalf/dispatches/2026-06-XX-drax-cosmograph-plus-page-restore.md` covering BOTH workstreams in one dispatch:

**Workstream A — Page restoration:**
- Restore `/loadout` to cycle-18 original: grid + featured picks + faction filter (currently at `/kits`)
- Move `/kits` content back to `/loadout`; delete `/kits` route; redirect `/kits` → `/loadout`
- Preserve `/sample` unchanged (already as it was)
- Recovery-2's rich per-character view code (`Loadout.tsx` cycle-18 recovery-2 state) extracted as a reusable component for re-use in Workstream B

**Workstream B — Cosmograph at `/forge` (minimum build):**
- Target: NEW `/forge` sub-route on existing loadout app
- Stack: React/Vite/Tailwind (matches existing loadout); add `@cosmograph/react` dependency
- Data ingest: load substrate-trace data from elrond's extracted `.csv`/`.parquet`; one BC cell per row
- Visualization:
  - Force-directed cosmograph rendering via @cosmograph/react WebGL canvas
  - Node color: by element_primary (shadow=#1a1a2e, fire=#c1392b, water=#2980b9, etc. — coordinate with elrond on canonical-7+1 color palette)
  - Node size: uniform for BC cells; larger for categorical-anchor nodes
  - Categorical anchors (BOSS-KILLER / SHADOW PRIMARY / etc.): derived in frontend logic from substrate-coordinate rules; rendered at the centroid of each anchor's region
  - Lasso interaction: built-in cosmograph feature; on lasso, returns set of selected BC cell IDs
- Side panel:
  - On lasso, compute centroid of selected cells' substrate vectors
  - Find nearest pre-generated kit (by Euclidean distance in substrate space)
  - Display matched kit's pre-computed identity via the rich-character-view component repurposed from Workstream A: name, element, archetype, categorical labels, T4 selection (with Twilight Inversion Shell rename applied to kit_shadow_000007), Q18 flavor identity
- Confirm button: stub for now (no cinematic firing yet); routes to placeholder "spirit confirmed" view

**Acceptance criteria (both workstreams):**
- `/loadout` restored to grid + featured + faction filter view
- `/kits` route returns 301/308 redirect to `/loadout`
- `/sample` unchanged
- `/forge` new route renders all 62 BC cells in cosmograph; lasso interaction works; side panel displays matched kit correctly using repurposed rich-character view
- Vercel preview deployment expected on completion

**Sequencing within dispatch:**
- Workstream A first (page restore + component extraction)
- Workstream B builds on A's extracted component
- Combined sequencing within one drax dispatch avoids double Vercel deploys

**Time budget:** 1-4 days drax time (combined workstreams)
**Cost budget:** $0 (no LLM calls; pure frontend build)

**Pre-commission dependency:** recovery-2 KR wave-close formalized first (so the rollback is clean — close cycle-18-recovery-2 → open new cycle for the page-restore + cosmograph combined dispatch).

### Phase 5 — Wave-close

Once both commissions complete (likely separate dispatch cycles):
- Author wave-close record at `canonical/story/2026-06-XX-cosmograph-minimum-wave-close.md`
- Capture: elrond data delivery; drax build delivery; Vercel preview URL; any discipline candidates surfaced; substrate-coverage observations
- Decision point for Matt: validate cosmograph as the chernoff-celestial-body surface OR iterate

---

## 3. Decision points still open (for next session)

| # | Decision | Why deferred |
|---|---|---|
| **DP6** | Post-confirm cinematic strategy: per-kit pre-rendered (62 cinematics) vs. runtime Veo-fired-per-confirm vs. single generic cinematic for all kits | Not in minimum scope; re-engage after cosmograph milestone validates |
| **DP7** | Categorical anchor derivation rules (BOSS-KILLER / SHADOW PRIMARY / etc.): coded in drax frontend OR pre-computed by elrond | Probably elrond pre-computes (substrate-led discipline); confirm in elrond dispatch |
| **DP8** | "Substrate-thin" indicator surfacing in cosmograph UI (showing which cells have NA cultural_tradition + period due to QDX-5 governance lapse) | Open — does the cosmograph honestly show data-quality issues, or hide them? Matt-question for Phase 2 |
| **DP9** | Vercel deployment routing: replace existing loadout's main page OR add `/forge` as separate route OR something else | Likely `/forge` per DP5 lock; confirm with drax during commission |

---

## 4. What to NOT do in next session

- **Don't fire Veo generations.** Iteration is parked. Re-engage only after cosmograph minimum validates the substrate-selection flow.
- **Don't re-open scoping DP1-DP5** unless Matt explicitly surfaces a question. They're locked.
- **Don't commission drax before elrond.** Drax needs elrond's data first.
- **Don't write extensive new canonical docs** before commissioning. The recognition record + next-session plan + ground-state entry are sufficient documentation for the commissioning phase. Wave-close record fires after delivery.
- **Don't re-engage the trait-palette / cursor / cinematic design from the prior cycle 18 / MM-P1 work.** That architecture is superseded by cosmograph.

---

## 5. Composition with broader project state

This next-session plan composes with:
- `canonical/story/2026-06-05-cosmograph-pivot.md` (architectural commitment)
- `canonical/00-ground-state.md` (current truth)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (Realm Expansion content rhythm)
- `agentic_orchestration/gandalf/notes/2026-06-02-mm-p1-top-1-rename-duskweaver.md` (Duskweaver identity + T4 Twilight amendment)
- `agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-governance-lapse-skill-tree-minimums.md` (substrate-thin urgency elevation)
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (existing loadout app architecture; cosmograph sub-route composes with this)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (engine workflow; pre-generation pipeline that feeds JSON packet)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (gear architecture; gear scope deferred to post-cosmograph)

---

## 6. Outstanding canonical-doc combing not yet done

The 2026-06-05 session focused doc-update efforts on the highest-impact targets (cosmograph record + Duskweaver T4 + MM-P1 playbook PARKED + season-archive cross-reference + ground-state entry + QDX-5 governance lapse urgency). The following docs are CORRECT AS-IS but may benefit from light cosmograph cross-references in a future combing pass:

- `canonical/29-design-overview.md` — strategic anchor; add cosmograph reference (if doc still exists; not surfaced during the 2026-06-05 survey)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D-series may want a new D-track for cosmograph
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine-to-game JSON-packet boundary may want explicit cosmograph callout
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` — player surface design; should reference cosmograph as next/forge sub-route
- `canonical/story/style-register.md` — style register decisions (likely unaffected; cosmograph is its own visual register)

These are low-priority. Address in a future combing pass if next-session capacity permits, or defer to when a specific doc's content needs amendment.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-05 per Matt directive to plan for next session + wind down
**Resume criterion:** next gandalf invocation; Phase 1 session-start protocol provides full context restoration
**Empirical-evidence trigger for cosmograph milestone success:** elrond delivers cleaned substrate-trace extraction; drax delivers Vercel-deployed cosmograph at `/forge` with working lasso → side-panel-character-lookup; Matt validates against the blank-canvas onboarding-problem criterion (does the substrate landscape engage; does lasso give legible compositional feedback)

**End of next-session plan.**
