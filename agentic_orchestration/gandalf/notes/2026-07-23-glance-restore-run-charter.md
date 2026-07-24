# GLANCE-RESTORE run charter (RATIFIED)

**Date:** 2026-07-23 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Status:** **DONE — 2026-07-23, exit predicate MET at verified prod truth (verdict: §6; G4b closed by conductor, GRL-1)**. Was RATIFIED — Matt 2026-07-23 (push-on-green AUTHORIZED · lane B IN · bake-off chartered separately); lane A executed by drax same-day, lane B by named `gandalf` sub-agent.
**Executes:** drax (lane A — all repo-touching work) · named `gandalf` sub-agent (lane B — pattern amendment)
**Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`) — fit test all-four-YES (§2)
**Commissioned:** Matt 2026-07-23 — "draft a run for the glance work, starting with (a) and if you can, layer in the rest. Would a KR run be appropriate here, or is it all Drax work?"

---

## §0 Intent (the owner's question, one sentence)

Glance prod has been frozen at `e5ea8584` (2026-07-22 15:41 UTC) by a stale checked-in `kit-provenance-sidecar.json` tripping the atlas BUILD-FAIL GUARD; restore the deploy chain so **prod serves current canon truth again** — corpus.db untouched (READ-ONLY law) — and absorb the failure's lesson into the desirable-run pattern.

**Rubric-law note (KFL-27 lesson #1, applied at charter time):** the owner's question here is fully machine-decidable — "prod serves a commit newer than the freeze, built from a fresh sidecar." No aesthetic surface → no owner-eye checkpoint needed. Predicate-diff against this §0 done at launch: **nothing fell out** — the intent IS the predicate (coverage = one sidecar, one build surface, one deploy).

## §1 Substrate (bounded, frozen at launch)

| Item | Role |
|---|---|
| `agentic_orchestration/research/curated/corpus.db` → `canon_corpus` | READ-ONLY source of truth (never written) |
| `glance/app/scripts/atlas/kit-provenance-sidecar.json` | THE stale artifact (regenerated in-run) |
| `glance/app/scripts/atlas/export-kit-provenance-sidecar.mjs` | regen instrument — repeatable by design (v1.13 E4 cutover, Matt-ruled 2026-07-17) |
| `glance/app/scripts/atlas/verify-build-fail-guard.mjs` | guard verifier (doctored cases HALT + clean source builds) |
| `glance/` build + `.github/workflows/glance.yml` + Vercel prod | the surface being restored |

## §2 Fit test (routes the conductor)

- **F1 enumerable:** YES — one sidecar, one build, one CI workflow, one deploy.
- **F2 decidable:** YES — G1–G4 all machine-checkable, no judgment-doneness.
- **F3 pre-drainable:** YES — the single commitment fork is push-to-main; drained at ratification via **push-on-green** authorization.
- **F4 authority-resident:** YES — gandalf authored/owns the atlas-interactive glance spec (D1-h); drax owns the executing presentation seam.

**→ gandalf conducts; KR NOT engaged.** Single-seam, zero cross-seam sequencing, no fork profile to manage — a KR wave here is apparatus without cargo. (Pattern §3: KR's spec-frozen build-wave shape is for multi-dispatch construction, not a one-commit restore.)

## §3 Lanes + pre-registered gates

**Lane A — restore (drax, all execution):**

1. Re-export: `node scripts/atlas/export-kit-provenance-sidecar.mjs` → **G1:** exit 0; `__provenance__.row_count > 0`; row-delta vs the stale sidecar reported (evidence line, not a gate).
2. **G2:** `node scripts/atlas/verify-build-fail-guard.mjs` exit 0 (all doctored cases HALT; clean source builds).
3. **G3:** `npm run build` green in `glance/app` (parser + tsc + vite).
4. Commit (auto-fire — authorized-work product) + **push on green** (pre-authorized at ratification; the one commitment boundary).
5. **G4 — the red-main tripwire, applied to ourselves:** post-push, `glance.yml` Actions run GREEN on the pushed commit AND Vercel prod serves a deployment newer than `e5ea8584`. The run is not done at push; it is done at **verified prod truth**.
6. drax `AGENT_STATE.md` reconcile.

**Lane B — pattern amendment (named `gandalf` sub-agent, per §2.1 conductor-economics):** amend `desirable-run-pattern.md` with a §6 "Pattern-observations from run failures," four observations:

1. **Coverage-gates before accuracy-gates** for fidelity runs (KFL-27 taxonomy #3).
2. **Owner-eye checkpoints pre-registered mid-run** for presentation-surface runs (KFL-27 taxonomy #4).
3. **Rubric law** — a VERIFIED claim names the owner's-question rubric, never a narrower proxy (KFL-27 taxonomy #1/#2).
4. **Red-main tripwire** — any run that pushes to a CI-gated surface carries a post-push pipeline-green + deploy-truth gate in its exit predicate. Born from this freeze: a push left glance red on main with prod silently frozen ~30h; nobody's exit predicate owned the deploy.

Gate: doc committed; jack-ryan ratification queued (governance rule-ownership routes to him per `canonical-doc-format.md § 6.7`).

**Fallback (honorable):** if G2 or G3 stays red AFTER a fresh sidecar — staleness was not the sole cause — HALT decision-shaped to Matt with the new failure surface named. No secondary-cause chasing in-lane.

## §4 Matt interface

- **At ratification — ✓ RULED (Matt 2026-07-23):** (i) push-on-green **AUTHORIZED**; (ii) lane B **IN**; (iii) MCP bake-off **chartered separately** (`2026-07-23-mcp-bakeoff-run-charter.md`, $15 approved → matt_to_do T5). KIT-FIDELITY docket §4 absorbed into the true-sources plan session (Matt-sequenced, after both runs are moving) — still NOT this run's scope.
- **In-run:** red-flag pings only.
- **At end:** one verdict line + evidence links (Actions run URL, prod deployment hash, row-delta).

## §5 Ruling ledger (veto-open) — empty at launch

- **GRL-1 (2026-07-23, conductor):** G4b closed on **deployment-header evidence** in lieu of a dashboard commit-SHA read — prod `last-modified: Fri, 24 Jul 2026 02:17:12 GMT` postdates the `ea660a00` push (02:06:09 UTC) by 11 min and the freeze (`e5ea8584`, 2026-07-22 15:41 UTC) by ~34.6h, while serving the green build's exact asset hashes (`index-Iv_cRUd4.js` → 200). Reasoning: the §3 predicate is "a deployment newer than `e5ea8584`" (deploy-recency, not SHA); only guard-passing builds deploy, and the serving deployment postdates the fresh-sidecar push. Drax's deferral (no CLI, token `invalidToken`, output byte-identical) was honorable and correct from his session. **Veto-open:** if Matt's dashboard shows prod aliased to an older deployment, this ruling is overturned and the run reopens.

## §6 Run verdict (conductor close-out, 2026-07-23)

**DONE — prod unfrozen; exit predicate MET at verified serving truth** (the red-main tripwire's own standard, applied to ourselves).

| Gate | Result | Evidence |
|---|---|---|
| G1 | ✓ | export exit 0; 590 rows, folk_name 590/590 non-null; **row-delta +5** (585→590) |
| G2 | ✓ | guard verify exit 0 — 11/11 doctored cases HALT + clean source builds |
| G3 | ✓ | `npm run build` green (~933ms) |
| push | ✓ | `ea660a00` on main (push-on-green, pre-authorized) |
| G4a | ✓ conductor-verified | `gh run view 30060749928` → conclusion `success`, headSha `ea660a00` — byte-match with drax's ledger |
| G4b | ✓ conductor-closed | GRL-1 (deployment headers: newer-than-freeze, serving green build's asset hashes). Rubric-law check vs §0: intent = "prod serves current canon truth again" — the serving deployment postdates the fresh-sidecar push and only guard-passing builds deploy; intent satisfied, no proxy-narrowing. |
| Lane B | ✓ | `desirable-run-pattern.md` §6 landed (`d04e85fb`, verified faithful); jack-ryan ratification queued (`qa/pending/2026-07-23-gandalf-desirable-run-pattern-s6-amendment.md`) |

**Findings routed:** (1) deploy-truth **self-closure gap** (Vercel CLI uninstalled; on-disk token expired) → matt_to_do **T6** — non-urgent, unblocks future red-main-tripwire self-closure. (2) `glance.yml` checkout@v4 / setup-node@v4 **Node-20 deprecation** — annotation-only; future action-version bump, drax seam.

**Freeze duration:** ~34.6h (2026-07-22 15:41 UTC → 2026-07-24 02:17 UTC). corpus.db READ-ONLY law held throughout; lane A touched nothing outside `glance/` + drax's note.

---

**Signed:** gandalf (`RUN-CONDUCTOR` draft), 2026-07-23. Run closed DONE by conductor same-date, §6.
