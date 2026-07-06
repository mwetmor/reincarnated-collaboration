# Skill handoff — 2026-07-06 (Matt-facing)

> Authored by knight-rider at GLANCE v1 BUILD closeout. Collab repo pushed through `87a5fd9`; tree clean, synced with `origin/main`.

## Headline — Glance v1 is LIVE

**https://reincarnated-glance.vercel.app** — the derived project dashboard. One URL, DERIVED from canon on every push, authored by no one. No DB, no server, **no LLM in the truth path**. Tiers 0-2 shipped; Tier 3 + RUN-STATE staged (see below).

All five dispatch steps closed:
- **Step 0 (jack-ryan RATIFY):** §7 "the five legislated shapes" folded into `canonical-doc-format.md` + skill twin (same commit `d88ba87`, §6.8-compliant); Discipline **#60** "parse-contract CI-fail-loud" landed in `engineering-disciplines.md` (`a75e97e`, engine repo). The LOCK-O candidate never landed, so #60 was claimed by Glance; a future LOCK-O escape-clause takes #61.
- **Step 1 (KR fold):** run-close deltas folded (`b3d943c`); then reconciled the parallel-session race — the summoner ruling had RESOLVED (Option 1) mid-work, so my ⚖-OPEN prose was stale. Superseded it with verified facts (`f189444`): ruling RESOLVED (`541c4ca`), gen-path Leg-1 landed (`306a917`, Gate-2 `a49ccd4`), criterion-C hygiene struck. D.1 #7 → IN-FLIGHT, `gates-on: gen-path-pilot-leg3`.
- **Step 2 (drax build):** `glance/` app in this collab repo, own Vercel project (`34bdc44`, `1c8129b`). Deterministic ~parser → `state.json` (gitignored, regenerated every build) → Vite/React/Tailwind static SPA. CI severity split live: MALFORMED = build FAIL file+line; dangling `gates-on:` = warning badge; absence never an error.
- **Step 3 (first-parse reconciliation):** exactly ONE MALFORMED across all four trackers + both Matt queues — duplicate `III.8` row ID in the engine tracker's MVP-TAG PASS table. Routed to gandalf (author); fixed → `III.8b` (`99093c4`, taxonomically honest child of the III.8 section, since III.7/III.9 are occupied section headers). Re-parse: **MALFORMED 0, exit 0**.
- **Step 4 (deploy):** live + smoke-verified (`db9fb6d`, `87a5fd9`). Tier 0 renders correct against canon: your-move pixel **5** (Q2/Q3/Q4/Q7/Q8), matt_to_do **2**, dangling **1** (`gen-path-pilot-leg3`, the legal in-flight gate), four tracker cards with STATUS + newest-first latest delta, watermark 2026-07-06.
- **Post-closeout (continuous deploy wired + freshness-signal fix):** the Vercel Git integration was NOT connected at closeout — the live site was a one-time CLI deploy, so pushes did not refresh it. Matt authorized the Vercel GitHub App on the repo; `vercel git connect` linked it (prod branch `main`, root `glance/app`). **Proven end-to-end:** pushed `f3bbd40` → webhook auto-build → READY in ~24s → production alias promoted. Canon-change path confirmed (a `canonical/**` edit rebuilds despite living outside the root dir; `commandForIgnoringBuildStep: None`). Vercel runs the parser in its build, so a red parse blocks the deploy — the fail-loud contract holds through the deploy path. Then fixed a freshness-signal defect: `last_commit`/`repo_sha` came back null on Vercel builds (parser shelled out to `git log`, which Vercel's build container doesn't expose). drax patched it (`a3594e7`) to read `VERCEL_GIT_COMMIT_SHA`/`_MESSAGE`/`_AUTHOR_NAME` env vars (git-log fallback for local builds); Vercel injects no commit-*date*, so the timestamp is a build-time proxy, flagged `date_is_build_time_proxy` and honestly labeled **"Last build"** in the UI (never claims a commit-time it doesn't have). Verified live: `last_commit` fully populated, invariants unchanged (5/2/1, four trackers).

## One Matt-decision surfaced by the deploy

- **Glance URL is currently PUBLIC.** drax disabled Vercel SSO-protection so the standalone URL is shareable (consistent with the standalone-shareable-app ruling; Glance is team tooling, not player-facing per spec §8, so the style/G2 gate doesn't apply). If you'd prefer it gated behind Vercel login, say so and drax re-enables `ssoProtection`. **Default kept: public.**

## Staged, NOT built (v1 = Tiers 0-2 only, Matt scope law)

- **Tier 3 (dependency graph)** — the `gates_on[]` edges + `dangling_gates[]` are already in `state.json`; it's a pure render layer when its criterion hits (one full board cycle with token adoption + dangling < ~10%). Seam left clean.
- **RUN-STATE pane** — **entry criterion is ALREADY MET** (the W1 #8 run registry exists with ≥1 registered run — the demo-readiness run produced exactly that, `cbeb9471`→`2d32195d`). Named the **first fast-follow**, but deliberately not built into v1 per scope law. A second `View` variant alongside glance/drill/source.

## Queued for jack-ryan's next governance touch (from the 2026-07-03 handoff ops-lessons)

Three candidate discipline entries surfaced during the demo-readiness run, not yet ratified:
1. Sub-agent-spawned long processes die with the sub-agent session (KR now launches detached).
2. Production-path smoke registration must be guard-tested.
3. Recovery claims must cite an existing code path (the "no re-fight required" claim shipped without one).

## Still-open Matt queue (unchanged by this session; the Tier-0 pixel = 5)

Q2, Q3, Q4, Q7, Q8 open in `canonical/matt_decision_needed/`. The summoner-emission item (2026-07-03) is ✓ RESOLVED (Option 1). matt_to_do: T1, T2.

## Next-session pickup

1. If token adoption is a priority: agents emit `gates-on:` on queue-row writes (law now, fork-4). Once a full board cycle carries them at < ~10% dangling → Tier 3 unlocks.
2. RUN-STATE pane is the named first fast-follow whenever Matt wants it (criterion already met).
3. Variation pilot: rocket reports READY FOR LEG 3 (`rocket/v-pilot-leg1-summon-int-variation-1`); batch-2 summoner emission `gates-on: gen-path-pilot-leg3`.
4. Flavor-scope ⚖ (shortlist-first vs all-700) remains OPEN from the prior handoff — 35/35 shortlist finalists flavored, 665 parked, $0 spent on the rest.
