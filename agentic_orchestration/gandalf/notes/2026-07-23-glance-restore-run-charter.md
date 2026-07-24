# GLANCE-RESTORE run charter (RATIFIED)

**Date:** 2026-07-23 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Status:** **RATIFIED — Matt 2026-07-23** (push-on-green AUTHORIZED · lane B IN · bake-off chartered separately). Lane A launches when Matt fires the drax prompt; lane B fired by conductor same-day.
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

*(entries land here as GRL-1..n if any reasoning-boundary fork surfaces)*

---

**Signed:** gandalf (`RUN-CONDUCTOR` draft), 2026-07-23.
