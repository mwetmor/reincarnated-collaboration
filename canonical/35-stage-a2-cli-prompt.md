# 35 — Stage A2 Claude CLI Agent Prompt

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Captured:** 2026-05-12
**Purpose:** Copy-paste-ready prompt for the Claude CLI agent at the start of Stage A2 work. Primes the agent with the architectural context, constraints, and engineering disciplines needed to execute the ARPG-genre coordinated sprint without breaking existing systems.

## How to use

1. Confirm Stage A1 (pre-sprint design + small fixes) has landed
2. Capture the regression baseline:
   ```bash
   cd /Users/admin/Games/reincarnated-engine
   python3 scripts/capture-regression-baseline.py
   # Inspect: ls baseline/v1.2-pre-stage-a2/ ; less baseline/v1.2-pre-stage-a2/balance_summary.json
   git add baseline/v1.2-pre-stage-a2/
   git commit -m "Capture pre-Stage-A2 regression baseline"
   ```
3. Tag both repos at the restore point:
   ```bash
   bash /Users/admin/Games/reincarnated-engine/scripts/tag-pre-stage-a2.sh
   # Review tag output; then push:
   PUSH_TAGS=1 bash /Users/admin/Games/reincarnated-engine/scripts/tag-pre-stage-a2.sh
   ```
4. Create `stage-a2` branch on both repos
5. Open Claude CLI in the `reincarnated-engine` repo
6. Paste the prompt block below as your opening message
7. Let the agent orient itself BEFORE engineering begins

---

## Copy-paste prompt block

```
You are beginning Stage A2 of the Reincarnated engine refactor — the ARPG-genre
coordinated sprint. This is the single largest piece of work in Track A's queue
(~10-13 weeks of engineering). The sprint bundles:

  B6  Class kit composition + Hierarchical Skill Tree
  B7  Gear-percentile variance check
  B10 Gauntlet restructure (per-band; native swarm tier)
  B11 Geometry palette expansion (16 → 25 active types)
  B12 Movement speed + boots + 10-slot gear audit
  B13 Active mobility + telegraphs + evasion (25 → 30 palette)
  B14 Multi-band convergence simulator (3-band; 9 runs/class)
  + absorbed A1/A1b/A2/A4 bug fixes

DO NOT write any code yet. Your first job is ORIENTATION.

## Required reading (in order)

Read these docs cover-to-cover before proposing any implementation:

1. `29-design-overview.md`
   The strategic anchor — scope, two-engine architecture, four-track work model

2. `16-project-roadmap.md`
   Track A stage sequencing, single-season-per-playtest rule, refactor-not-rewrite
   lock, legacy-preservation approach. ALL operational guardrails for this work
   live here

3. `28-engine-arpg-rebalance-design.md`
   Full per-B-item scope. Each of B6/B7/B10/B11/B12/B13/B14 has detailed scope,
   cost estimate, co-dependency notes, demo follow-on notes. THIS IS THE
   ENGINEERING SPEC.

4. `33-progression-skeleton.md`
   Locked-only summary of all 12 progression-design sections. Quick reference for
   anything that needs to be true post-A2.

5. `32-progression-design.md`
   Full progression-design discussion (54 LOCKED entries across 12 sections).
   Reference when 33's summary needs unpacking.

6. `engine-repo/design/decisions/decisions-log.md`
   Recent entries (2026-05-08 through 2026-05-12). Especially:
   - 2026-05-08 dimensional generation Option C
   - 2026-05-11 B11 geometry palette expansion
   - 2026-05-11 B13 active mobility extension
   - 2026-05-11 progression philosophy
   - 2026-05-11 Earth meta-layer + body-swap pool correction
   - 2026-05-12 refactor-not-rewrite + legacy preservation + single-season rule

7. `30-engine-explainer-current.md`
   Current engine state — what's there to extend (don't replace)

8. `31-engine-explainer-future.md`
   Future engine state — what the engine should look like post-Stage-A2

9. `engine-repo/CLAUDE.md`
   Engine codebase orientation

## Critical constraints (DO NOT VIOLATE)

REFACTOR, NOT REWRITE. The engine's core systems (convergence loop, dimensional
generation, fit_for_class scoring, LLM call pipeline, telemetry, foundation
math) are proven through 5 production seasons + demo1 v1.2 family playtest.
Every B-item EXTENDS existing infrastructure. Do not throw existing code away
in favor of greenfield.

PRESERVE PRODUCTION SEASONS until intentional regen. The 5 seasons at
`engine-repo/exports/season_001001-005` (and mirrored in
`demo-repo/public/seasons/`) are baseline content. Regen happens deliberately
per stage landing rhythm, NOT incidentally during refactor work.

SINGLE-SEASON-PER-PLAYTEST. Default policy: regenerate AT MOST one season per
playtest cycle. Cost rises 6-10× through Stage A2 (~$5-10/season vs current
~$0.87). Multi-season regen requires explicit user authorization.

REGRESSION BASELINE EXISTS. Pre-Stage-A2 baseline lives at
`engine-repo/baseline/v1.2-pre-stage-a2/`. After each sub-stage ships, diff
against this baseline. Catches unintentional drift.

PARTIAL-TAG PROTOCOL. Each sub-stage tagged with `v*-partial` until verified by
user. Promote to full tag only after smoke tests pass. NEVER tag a release
without user confirmation.

SCHEMA-VERSION ON CHANGES. Schema additions (new fields like `tier`,
`chain_id`, `parent_skill_ids`, `cast_time`, `i_frame_window`, `set_id`,
per-band `convergence_report`) bump `season_manifest_version`. Old seasons
should remain interpretable (forward-compat).

CO-DEPENDENCY MATTERS. B6 + B7 + B10 + B11 + B14 are architecturally
co-dependent. Cannot ship one without the others. Plan integrated landing.

## Engineering disciplines (from prior phase learnings)

STALE BUILD FIRST. When something looks wrong, FIRST verify build state
(dependencies installed; latest code; tests fresh). Don't deep-dive
diagnostics on a stale build.

CIRCUMSTANTIAL → STRUCTURAL DIAGNOSIS. Don't jump from "this looks like X" to
"X is the root cause." Trace actual code paths. Past mistake: structural
diagnosis from circumstantial evidence led to wrong fixes.

EXPLICIT GIT STAGING. Use specific filenames, not `git add -u` or `git add .`.
Past mistake: implicit staging missed new directories during Vercel deploy.

EMPIRICAL INSPECTION OVER ASSUMPTION. For sprites/data/files, inspect actual
contents (PIL extraction, file reads, JSON dumps) before assuming structure.

TAG-BEFORE-VERIFY ANTI-PATTERN. Never tag a release without user verification.
Use `v*-partial` for intermediate states.

## Pending decisions (require user input before engineering)

Some Stage A2 sub-items have OPEN decisions that need confirmation:

A4 — shield magnitude scaling model (file 28):
  (a) heal-style WIS scaling
  (b) HoT-style damage_modifier scaling
  (c) generator-emits-tier-scaled

D1 — element-naming approach (file 28; technically Stage A1):
  (a) allow-list of vetted candidates
  (b) scoring function on free-associated candidates
  (c) hybrid (allow-list floor + scoring primary)
  Likely already resolved if Stage A1 D1 design session happened — verify with
  user.

B6 — specific kit composition templates per archetype (file 28 D2/B6 area):
  Per-archetype templates needed (fire_mage requires ≥3 fire, ≥1 AOE,
  ≥1 control...) — full per-archetype list needs to be drafted.

Surface these and request user decisions BEFORE writing implementation code.

## Your first response

DO NOT write code in your first response. Instead:

1. Confirm you have read the required docs (list which you actually read)
2. Confirm `v1.2-pre-stage-a2` tag exists on both engine + demo repos
3. Confirm regression baseline directory exists at
   `engine-repo/baseline/v1.2-pre-stage-a2/`
4. Identify the FIRST sub-item you propose to implement.
   Recommendation: start with B14 multi-band convergence simulator as a
   vertical slice that proves the architecture, OR B6 Hierarchical Skill Tree
   as the kit-composition foundation other items depend on. Justify your
   choice.
5. Surface the pending decisions above; ask the user to resolve them
6. Outline your implementation plan for the chosen first sub-item: what files
   you'll touch, what schema changes ship, how you'll verify against regression
   baseline, what `v*-partial` tag you'll create on success

DO NOT begin engineering until the user explicitly confirms:
  - Your chosen first sub-item
  - Resolution of pending decisions you flagged
  - The implementation plan

## Cross-references

If you need to look up specifics:

- Engine queue items: `28-engine-arpg-rebalance-design.md`
- Stage sequencing: `16-project-roadmap.md`
- Progression locks (canonical): `33-progression-skeleton.md`
- Progression discussion (depth): `32-progression-design.md`
- Hierarchical Skill Tree spec: `32-progression-design.md` § 4 (Q4.3)
- Multi-band sim spec: `32-progression-design.md` § 8
- Body-swap mechanics: `32-progression-design.md` § 9 + 11
- Earth meta-layer (far-future): `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_earth_meta_layer.md`
- Pet system intent: `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_pet_system.md`
- Decisions log: `engine-repo/design/decisions/decisions-log.md`

Acknowledge orientation. Ask questions. THEN we plan implementation.
```

---

## Notes on tuning this prompt

This is a deliberately long orientation prompt because Stage A2 is a high-risk,
high-scope refactor. The intent is to slow the agent down before engineering
begins — premature implementation in a refactor of this size is a real risk.

If the agent's first response shows it has NOT done the required reading, push
back. Confirm it reads each doc cover-to-cover. The locked design in file 32
is dense; skimming will produce wrong implementations.

After the user-confirmed first sub-item lands successfully:
- Tag a `v*-partial` release
- Diff against regression baseline
- Document what changed
- Then ask the agent: "ready for next sub-item — propose order + plan"

This iterative loop is how a 10-13 week sprint stays on track without losing
fidelity to the locked design.
