# Yomi (season_002328) — provenance audit

**Author:** elrond
**Date:** 2026-05-16
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-elrond-B-yomi-provenance-audit.md`
**Mode:** Read-only investigation across all four repos.
**Status of investigation:** COMPLETE

---

## 0. Executive verdict

**Yomi (season_002328) is a single point of failure on data we have been actively building against — and the failure mode is worse than the audit § 3.6 suggested.** The canonical Yomi season data lives ONLY in `reincarnated-loadout/data/season_002328/` (556 KB total — 10 class JSONs + manifest + gear_pool.json). The loadout repo has **no origin remote** (25 local commits, never pushed). If the loadout working directory is lost, Yomi is lost.

The audit § 3.6 hypothesized: *"Yomi must be in a separate telemetry pass or has been generated against a different telemetry instance."* The truth is more pedestrian and more concerning: **Yomi was generated against the canonical engine on 2026-05-13, the engine produced full `seasons/season_002328/` and telemetry rows at that time, and BOTH have since been deleted from the engine repo.** The commit message that brought Yomi into loadout uses the phrase "from engine side-seed" — meaning the run was framed as a deliberate side-experiment outside the canonical 001xxx-numbered series, and its engine-side artifacts were not preserved.

**Reproducibility status:** the seed (2328) and anchor (myth-014-yomi) are known and the engine is deterministic from seed. However, the engine code has changed substantially between 2026-05-13 and now (B10.2, B10.4, telemetry tier-1, etc.). A re-run from seed=2328 today would produce **a different Yomi** — same anchor, similar themes, but different per-class stats, different convergence outcomes, different gear pool. **THIS Yomi cannot be byte-recovered from seed alone.**

Recommendation: **option 3 (archive current Yomi into elrond's archive/ NOW) plus option 2 (Matt sets up loadout origin remote)**, sequenced as immediate (option 3) + Matt's convenience (option 2). Option 1 (regenerate from seed) is a separate, longer-cost dispatch for a *different* purpose (re-converging Yomi back into canonical engine telemetry) and is not the remediation for the SPOF.

---

## 1. Provenance timeline (reconstructed from git + manifest + telemetry)

All times below in EDT (UTC-4) for legibility; UTC equivalents in parentheses where surfaced from raw timestamps.

| Time (EDT) | Event | Evidence |
|---|---|---|
| **2026-05-12 ~20:32** | Last canonical-series season generated — season_001007, theme=fire, anchor=library-005-memory-archive | `data/telemetry.db.seasons` row: `generated_at = 2026-05-13T03:25:47.478799+00:00` (= 23:25 EDT 2026-05-12) — wait, EDT is UTC-4, so 03:25 UTC = 23:25 prior-day EDT. Refined below. Actually the listing showed `2026-05-13T03:22:50` and `2026-05-13T03:25:47` UTC for 001006/001007 — these are 23:22/23:25 EDT 2026-05-12, matching the seasons/ directory mtime of `2026-05-12 20:30` / `2026-05-12 20:32`. The hour discrepancy is the UTC-vs-EDT offset; treat the seasons/ dir mtime as authoritative for "when the canonical 001xxx series last wrote." |
| **2026-05-13 ~00:32** | Yomi generation begins (computed: 01:13:51 EDT − 2498.6s duration ≈ 00:32:14 EDT) | Derived from manifest `generated_at` and `summary.generation_duration_seconds = 2498.6` |
| **2026-05-13 01:13:51** | Yomi generation completes; manifest.json written at `seasons/season_002328/manifest.json` (engine internal shape, `manifest_version: 1.3`) | `data/season_002328/manifest.json` field `generated_at: 2026-05-13T05:13:51.927556+00:00` |
| **2026-05-13 01:46:16** | Loadout commit `61fd526` — "Phase 2: Page 1 loadout — Yomi data swap + full implementation". 10 class JSONs + manifest.json copied from engine `seasons/season_002328/` into loadout `data/season_002328/`. (gear_pool not yet copied — Phase 2 included it via the analytics layer, not gear catalog.) | Loadout git history, commit body cites "Yomi season_002328 (10 named classes, all 4 elements new: lantern/miasma/brine/bone); Anchor class: Lantern-Keeper of Yomi's Winds (hybrid_mage, 52.6% WR)" |
| **2026-05-13 → 2026-05-14 ~01:32** | (Window during which the canonical engine `seasons/season_002328/` and telemetry rows for it must have still existed, since they were needed for the gear_pool export to follow) | Logical reconstruction from c1f02ca's documented dependency on `seasons/<id>/gear/catalog.json` + telemetry-DB gear records |
| **2026-05-14 01:32:45** | Loadout commit `11596f7` — "Export Yomi (season_002328) gear_pool.json from engine side-seed. 200 items, 40 per tier (legendary/epic/rare/uncommon/common). Required by drax for v0.5-real-gear." | Loadout git history |
| **2026-05-14 23:58:18** | Engine commit `c1f02ca` — "export: add per-item GearStats + rolled_effects to gear_pool export (v1.1)". Documents the deterministic-replay mechanism: re-runs `generate_season_gear_pool()` with `seed + 999` against the season's `gear/catalog.json` from `seasons/<id>/`. | Engine git history |
| **2026-05-14 23:58:36** | Loadout commit `7693af9` — "data(season_002328): re-export gear_pool with per-item stats (v1.1 schema). File grows from 196 KB to 350 KB." Cited source: "engine star-lord seam, commit c1f02ca". | Loadout git history |
| **2026-05-14 ~23:59 → 2026-05-16 (unknown precise time)** | Engine `seasons/season_002328/` directory deleted, and telemetry rows for `season_002328` removed from `data/telemetry.db.seasons` | No git evidence (gitignored); inferred from current absence. The deletion necessarily post-dates the v1.1 re-export (which depended on the catalog.json) and pre-dates 2026-05-16 (this audit). |
| **2026-05-16 (this session)** | Audit confirms Yomi absent from engine seasons/, exports/, telemetry, all baselines, all caches | Filesystem + SQL queries documented below |

### 1.1 — The "side-seed" terminology

Commit `11596f7` (2026-05-14 01:32 EDT) says "from engine side-seed". This phrase appears nowhere else in the engine or loadout codebases (verified via `grep`). The most plausible interpretation: an ad-hoc seed value chosen outside the canonical 001xxx numbering scheme (which appears to mirror season_number sequentially), used for a one-off generation pass meant to produce realistic gear data for drax's v0.5-real-gear work without polluting the canonical season-number series. The seed value `2328` itself is opaque — no observed semantic significance — likely chosen ad hoc for uniqueness.

This framing (side-experiment, not canonical) plausibly explains why the engine-side artifacts (seasons/ directory + telemetry rows) were deleted at some point — they were treated as disposable scaffolding for the loadout data export. **The unanticipated consequence**: the loadout repo became the canonical home of a real season.

---

## 2. Where Yomi exists today — comprehensive inventory

### 2.1 Engine repo (`~/Games/reincarnated-engine/`) — ABSENT

| Path | Status | Evidence |
|---|---|---|
| `seasons/season_002328/` | ABSENT | `ls seasons/` lists 23 dirs from `season_000001` to `season_001007`; no 002328 |
| `exports/season_002328/` | ABSENT | `ls exports/` lists 5 dirs `season_001001`–`season_001005`; no 002328 |
| `data/telemetry.db.seasons` row for season_002328 | ABSENT | `SELECT … WHERE season_id LIKE '%2328%' OR seed = 2328 OR anchor_id LIKE '%yomi%'` returns 0 rows. Telemetry max `generated_at` is `2026-05-15T03:56:50`; no 002328 in the time-ordered series |
| `data/telemetry.db.*` other tables (classes, monsters, gear, abilities, …) | ABSENT (transitively) | Run_id-keyed; no 002328 run_id → no rows of any kind |
| `data/seasonal_elements/` | UNAFFECTED | Element pool is global, not per-season; lantern/miasma/brine/bone names are entries here but selection was per-season metadata, now only preserved in the loadout manifest |
| `data/seasonal_anchors/` | INDIRECTLY PRESENT | The anchor `myth-014-yomi` is a row in `seasonal_anchors/library.json` (verified — the library is still intact); but the *fact that Yomi season selected it* lives only in the loadout manifest |
| `baseline/v1.2-pre-stage-a2/` | ABSENT | Snapshot dated 2026-05-12; predates Yomi by 1 day |
| `cache/llm/` | NO YOMI CONTENT | A few SHA-named files contain "2328" as a substring coincidentally; grep on file *content* for `"002328"`, `"Yomi"`, `"season_002328"` returns no matches |
| Source code | NO YOMI HARDCODES | `grep -r "002328|[Yy]omi|side[_-]seed" src/ scripts/ cli.py config/` returns only generic mentions in star-lord MIGRATION.md + AGENT_STATE.md as historical references; no special-casing |
| Engine git history | One commit-message mention | `baa3bed` (telemetry tier-1 v2.0 migration) — body says "Drax v0.7 picks up these fields via fresh Yomi regen" — this is a forward-looking reference, not data preservation |

### 2.2 Loadout repo (`~/Games/reincarnated-loadout/`) — SOLE CANONICAL HOME

| Path | Status | Detail |
|---|---|---|
| `data/season_002328/manifest.json` | PRESENT | 72 lines; `manifest_version: 1.3` (engine internal shape — confirms the audit § 3.3 shape-leak finding); contains seed=2328, anchor metadata, element selections (lantern/miasma/brine/bone), summary (10 classes / 40 monsters / 0.508 trial defeat rate / 0 convergence failures / 2498.6 sec generation duration) |
| `data/season_002328/classes/class_0001..0010.json` | PRESENT | 10 class JSON files (one short of the audit's "11 classes" claim — Yomi actually generated 10, not 11; manifest summary confirms `classes_generated: 10`) |
| `data/season_002328/gear_pool.json` | PRESENT | 350 KB, v1.1 schema (per-item stats + rolled_effects + ability_modifiers); 200 items, 40 per tier |
| **Total disk footprint** | **556 KB** | `du -sh data/season_002328/` |
| Loadout git history | 3 commits scoped to `data/season_002328/` | `61fd526` (Phase 2 add, 2026-05-13); `11596f7` (gear_pool first export, 2026-05-14); `7693af9` (gear_pool v1.1 re-export, 2026-05-14) |
| **Origin remote** | **NONE** | `git remote -v` returns empty. 25 local commits exist; no push target configured. |

### 2.3 Demo repo (`~/Games/reincarnated-demo/`) — ABSENT

| Path | Status | Evidence |
|---|---|---|
| Any reference to season_002328 / Yomi | ABSENT | `grep -rln "002328\|[Yy]omi" reincarnated-demo/` (excluding .git and node_modules) returns 0 matches; `git log --all --grep="002328\|[Yy]omi"` returns 0 commits |

The demo pipeline consumes seasons 001001–001005 (per audit § 1A). Yomi was never demo-targeted.

### 2.4 Collaboration repo (`~/Games/reincarnated-collaboration/`) — REFERENTIAL ONLY

Yomi appears as illustrative reference in 13+ canonical/story design docs (`cosmology-reincarnated.md`, `trial-moment-ritual.md`, `season-feel-rubric.md`, `court-of-forms.md`, `naming-triad.md`, `drift-audit.md`, `engine-generic-meta-structure.md`, `enemy-visual-legibility.md`, `embodiment-narrative-layer.md`, `ascension-moment-ritual.md`, `passage-moment-ritual.md`, `spirit-guide-voice.md`, `gandalf-phase2-bullet-points.md`); in all skill_handoff docs (`skill_handoff_2026-05-13/14/15.md`); in `CHANGELOG.md`; in my own audit (`data-architecture-audit-2026-05-16.md`); and in catalogue-rubric work. These are **prose references** — they cite Yomi as design example (Pomegranate, Izanami Passage, Lantern-Keeper) but do not carry the data. **Loss of Yomi data would not break the prose; loss would break re-running gameplay against the design vocabulary the prose has built.**

### 2.5 Anywhere else — checked, nothing found

- Engine `cache/llm/` content: no matches.
- Engine baseline snapshot `v1.2-pre-stage-a2`: predates Yomi.
- Other backup locations: none observed in repo trees.

---

## 3. Single-point-of-failure assessment

**Original status (pre-option-2): CONFIRMED SPOF, severity high.**
**Status as of 2026-05-16 post-option-2 execution: REPO-LEVEL SPOF CLOSED.** Loadout now lives at `https://github.com/mwetmor/reincarnated-loadout` with `main` pushed and tracking. The three-deep redundancy (working tree + local git + remote) is restored. The risk modes below describe the **pre-option-2** state, retained for the historical record.

Failure modes:

| Mode | Probability | Impact | Recovery path today |
|---|---|---|---|
| Loadout working dir wiped (accidental rm, disk failure, dotfile mishap) | Low but non-zero | All Yomi data lost; loadout app loses its working season; design vocabulary loses its anchor example | None — no other copy exists |
| `data/season_002328/` selectively deleted (e.g., dev refactor) | Low (gitignored content not currently in `.gitignore` per spot-check; tracked via git, so `git restore` would recover) | All Yomi data lost from working tree; recoverable from loadout local git history | **Loadout local git history** — but if loadout `.git` is corrupted/wiped, gone |
| Loadout `.git` corruption (rare but possible) | Very low | All Yomi data lost from history; recoverable from working tree IF working tree is intact | Working tree only |
| Both working tree AND `.git` lost together (e.g., laptop failure with no backup) | Low overall (per-event probability low, but probability-over-time accrues) | Yomi lost permanently | None |
| The session that holds the loadout repo state (e.g., this laptop) is replaced or destroyed | Variable; not bounded by typical software risk | Yomi lost permanently | None — there is no off-machine copy of any kind |

The lattice of "data exists in working tree + git history + remote" that protects most files reduces here to "data exists in working tree + loadout's local git only." That removes one redundancy layer compared to remote-backed repos.

---

## 4. Reproducibility-from-seed analysis

The engine is deterministic from seed + code state. Same `seed=2328` + same code + same data files = byte-identical output. **However**, the code has changed substantially between 2026-05-13 (Yomi gen) and 2026-05-16 (now):

| Date | Engine commit | Substance |
|---|---|---|
| 2026-05-13 (Yomi gen) | (commit at or before `128654f` — last pre-Yomi commit not surfaced, but B10.2 PackProxy work was already happening per commit `128654f` 2026-05-12) | The math model that Yomi was generated against |
| 2026-05-13 → 2026-05-14 | `2caf949` (B10.2 fixup), `097281f` (B10.2 closure), `4b6782f` (AGENT_STATE) | Recompose gauntlet isolation; test counter stability |
| 2026-05-14 → 2026-05-15 | `18e45ef` (B10.4 swarm eff_attr calibration), `6653666` (B10.4 docs), `d6002bf` (B10.4 AGENT_STATE), **`c1f02ca` (gear_pool stats)**, `4897023` (AGENT_STATE), `4d159d6` (B10.4 full regen findings) | B10.4 swarm calibration (eff_attr 0→7) — *changes effective attack stat per pack-proxy combat* → changes balance modifier convergence → changes final per-class stats |
| 2026-05-15 → 2026-05-16 | `baa3bed` (telemetry tier-1 v2.0 — schema addition; does not change behavior) | Telemetry schema only; behavior preserved |

The B10.4 swarm calibration is the load-bearing concern: pack combat math changed, and convergence outcomes for any class that fights packs would shift. A Yomi re-run from seed=2328 today would converge to *different* balance modifiers than the 2026-05-13 run did → different per-class final stats → different gear pool (gear is generated from class profile + seed+999) → different anchor-class identity (e.g., the "Lantern-Keeper of Yomi's Winds, hybrid_mage, 52.6% WR" might land at 49% WR with different stats).

**Implication:** "regenerate from seed=2328" can produce **A Yomi**, but not **THIS Yomi**. THIS Yomi is what design docs, drax's loadout app, gandalf's narrative work, and the existing Pomegranate / Izanami Passage vocabulary all reference. The two would coexist confusingly if both were named "season_002328"; the canonical regeneration would be a *replacement*, not a *recovery*.

**Practical recovery path for THIS Yomi: file-level archive of the loadout `data/season_002328/` content. There is no engine-state pathway.**

---

## 5. Remediation options (ranked)

### Option 3 — Archive current Yomi into elrond's archive/ (RECOMMENDED, IMMEDIATE)

**Action:** copy `reincarnated-loadout/data/season_002328/` into `agentic_orchestration/research/curated/archive/yomi-season_002328-2026-05-13/` (preserves directory structure, manifest, classes, gear_pool). Add an `archive/yomi-season_002328-2026-05-13.md` companion documenting provenance per the v1.1 archive convention established in MIGRATION.md.

**Cost:** ~15 minutes elrond work. 556 KB committed to collaboration repo (one-time).

**Value:** removes the SPOF immediately. Recovery becomes a `cp` rather than "lost forever." Aligns with the v1.1 archive convention.

**Tradeoffs:**
- Adds 556 KB to the (currently untracked) collaboration repo. No collaboration .git exists today (confirmed in Phase 1 work), so no git footprint impact — the archive is filesystem-only durability, which is the same robustness profile as the loadout repo's working tree. Net storage redundancy improves; net repo-git redundancy stays neutral until either repo gets a remote.
- Per ADR-006, reads from loadout (allowed) and writes to elrond's domain (allowed) — no authorization friction.

**Authorization needed:** none — read + write are both within elrond's permitted operations per ADR-006.

### Option 2 — Establish loadout repo origin remote and push — ✓ DONE 2026-05-16

**Action taken (Matt-authorized, elrond-executed as cross-seam exception for SPOF remediation):**

```
git -C reincarnated-loadout remote add origin https://github.com/mwetmor/reincarnated-loadout.git
git -C reincarnated-loadout push -u origin main
```

**Result:** all 25 commits + working tree state of loadout `main` now pushed to GitHub. `main` tracks `origin/main`. Future pushes via standard `git push`. The repo lives at `https://github.com/mwetmor/reincarnated-loadout`.

**Cross-seam-boundary note:** loadout is drax's seam; elrond is normally read-only there. Matt's explicit direct request + the SPOF-remediation context made this an authorized one-time exception. No code or content changed — only `git remote add` + `git push`. Working tree was clean (verified pre-push), so no commits were authored.

**Value delivered:** loadout repo now has the standard working-tree + local-git + remote redundancy lattice. SPOF for the *whole* loadout repo (not just Yomi) is now closed.

**Residual Yomi-specific consideration:** even with loadout pushed, Yomi still has only the loadout-repo home. If we want **four-deep** redundancy (working tree + local git + remote + elrond archive) — i.e., the same standard the rest of the project's data layer now operates at — option 3 below remains the closing action.

### Option 1 — Regenerate Yomi from canonical seed=2328 against current engine

**Action:** Launch engine with `--seed 2328 --season-id 002328 --anchor myth-014-yomi` (or however the side-seed flow was invoked), produce a fresh canonical season_002328, write to engine `seasons/`, populate telemetry, re-export gear_pool. Compare output to loadout's current data. **Outputs will differ** per § 4.

**Cost:** ~45-60 min generation runtime + dispatch authoring + drax wiring decision (does loadout consume the regenerated data or stay on the archived data?).

**Value:** converges Yomi back into canonical engine state, including telemetry analytics. Future drax work can rely on standard engine pipeline.

**Tradeoffs:**
- **Replaces THIS Yomi with A Yomi.** Existing design references, drax loadout state, and any other consumers either get re-aligned (lossy) or operate against archived-old Yomi while engine has new Yomi (forking).
- Should NOT be the SPOF remediation — should be a separate, intentional dispatch with its own scoping.
- If pursued, do so AFTER option 3 has archived the current Yomi (so the old version is preserved).

**Recommendation:** do not bundle with SPOF remediation. Queue as separate star-lord / rocket dispatch for "canonical-engine-state recovery of Yomi" when convenient.

### Option 4 — Accept the gap; document and move on

**Action:** None.

**Cost:** 0 immediate.

**Value:** None.

**Tradeoffs:** SPOF persists. Future loss of loadout working dir = permanent Yomi loss. Given the small cost of option 3, accepting the gap is not defensible unless option 2 is being executed concurrently.

**Recommendation:** rejected.

---

## 6. Recommended sequencing — UPDATED 2026-05-16 post-option-2 execution

1. **✓ DONE 2026-05-16:** Option 2 — loadout origin remote (`https://github.com/mwetmor/reincarnated-loadout`) added; `main` pushed and tracking. Loadout SPOF is now closed.
2. **Open — Matt's call:** Execute option 3. Elrond archives `loadout/data/season_002328/` into `agentic_orchestration/research/curated/archive/yomi-season_002328-2026-05-13/` + companion markdown. ~15 min. Closes the residual Yomi-specific redundancy gap (the *whole-repo* SPOF is closed by option 2, but Yomi's data only lives in one repo — option 3 cross-replicates into elrond's archive for the same four-deep redundancy other historical artifacts now operate at).
3. **Deferred / optional:** Option 1 as a separate, scoped dispatch IF the project later wants Yomi back in canonical engine state (e.g., for analytics consistency, or for B-series rebalance pass to converge cleanly against Yomi). Not urgent. Not coupled to SPOF remediation.

After step 2 alone: SPOF for the loadout repo is closed (working tree + local git + remote = 3-deep redundancy). Yomi data exists in one repo's three-deep stack.

After step 2 + step 3: Yomi specifically lives in (a) loadout working tree, (b) loadout local git, (c) loadout remote, (d) elrond archive — 4-deep redundancy matching the discipline applied to the research.db cleanup.

---

## 7. Documentation follow-ons (knight-rider sequencing)

- **Audit § 3.6 update.** The current § 3.6 narrates the SPOF based on the audit's hypothesis. Replace its Yomi paragraph with a pointer to this audit and the corrected provenance reconstruction (engine `seasons/` directory + telemetry rows existed at generation time but were subsequently deleted; not a "different telemetry instance").
- **MIGRATION.md v1.2 entry** if option 3 is executed — elrond authors as part of option-3 execution.
- **Decisions-log entry** acknowledging the side-seed pattern as a recognized failure mode + the archive-on-import discipline if Matt wants to codify (knight-rider drafts; small ADR-equivalent or just a discipline entry). Optional.
- **Star-lord-side note**: the c1f02ca deterministic-replay mechanism documented in `export/MIGRATION.md` has a silent assumption (`seasons/<id>/gear/catalog.json` exists) that broke for Yomi between the v1.0 export (2026-05-14 01:32) and the v1.1 re-export (2026-05-14 23:58) — actually the re-export succeeded, so the catalog.json was present then; the assumption broke later when the directory was deleted post-2026-05-14 23:58. Worth noting in star-lord's MIGRATION.md as a known fragility of the side-seed pattern when re-exports are needed.

---

## 8. Verdict — recommended next action — UPDATED 2026-05-16 post-option-2

**Option 2 has executed.** Loadout SPOF is closed at the repo level.

The remaining open question: **does Matt want option 3 also?** It cross-replicates Yomi specifically into elrond's archive for the four-deep redundancy standard now in force across the rest of the data layer. The case for option 3 is *consistency-of-discipline*, not *immediate-risk-mitigation* (the latter is now neutralized).

- **In favor:** symmetry with the research.db archive convention; protects against a category of failure where the loadout repo is intact but Yomi-specific data within it is mutated by future work; gives gandalf/design a stable referent independent of loadout app evolution.
- **Against:** Yomi data is already in three places (loadout working tree, local git, remote); a fourth copy is incremental, not transformative; the data is small (556 KB) but the *discipline* of having multiple archived copies could spread to many files if generalized.

Recommendation: **execute option 3 if and only if Matt wants four-deep redundancy as a standing rule for design-vocabulary data.** Otherwise, option 2 alone is sufficient remediation.

— elrond, 2026-05-16
