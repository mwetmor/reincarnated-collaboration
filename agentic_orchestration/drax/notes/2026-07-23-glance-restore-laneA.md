# GLANCE-RESTORE — Lane A completion note (drax)

**Date:** 2026-07-23 (executed) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-23-glance-restore-run-charter.md` (RATIFIED, Matt 2026-07-23) · **Conductor:** gandalf · **Executor:** drax

## Verdict

**Lane A GREEN through push + Actions.** Prod-truth gate (G4b) deferred to Matt's one-look — Vercel deploy commit not machine-verifiable from this session (no CLI, on-disk token expired, and the sidecar refresh is output-invisible so served bundle is byte-identical).

## What happened (the freeze)

Glance prod was frozen at `e5ea8584` (2026-07-22 15:41 UTC). The checked-in
`glance/app/scripts/atlas/kit-provenance-sidecar.json` went stale vs `corpus.db` (curation
added rows). The atlas BUILD-FAIL GUARD correctly halted every build; Vercel's own
`npm run build` (which runs the parser) also failed, so the deploy chain stalled and prod
served the last green (~34h stale).

## Gate ledger

| Gate | Result | Evidence |
|---|---|---|
| **G1** — re-export sidecar | ✓ exit 0 | `node scripts/atlas/export-kit-provenance-sidecar.mjs` → rows 590, folk_name 590/590 non-null. **Row-delta +5** (stale 585 → 590). |
| **G2** — guard verify | ✓ exit 0 | `verify-build-fail-guard.mjs` — all 11 doctored cases HALTED + clean source builds. GUARD VERIFY: ALL PASS. |
| **G3** — build | ✓ exit 0 | `npm run build` green (stage-assets Edition-IV + stage-kits + parser + tsc + vite; built in ~933ms). Only tracked change = the sidecar; dist/public artifacts gitignored. |
| **Commit + push** | ✓ | `ea660a00` on `main` (push-on-green pre-authorized at ratification). |
| **G4a** — Actions green | ✓ | run `30060749928` GREEN — "Build (parser + tsc + vite)" pass, build job 26s. https://github.com/mwetmor/reincarnated-collaboration/actions/runs/30060749928 |
| **G4b** — Vercel prod truth | ⏳ MATT ONE-LOOK | prod `https://reincarnated-glance.vercel.app` responds 200, serving my green build's exact asset hashes (`index-Iv_cRUd4.js` / `index-P6tX_gsz.css`). Deploy **commit** not self-verifiable: Vercel CLI not installed; on-disk CLI token returned `invalidToken`; sidecar refresh is guard-gating only (output byte-identical), so client-observable output can't distinguish deploy commits. Vercel git-integration deploys on a now-green build (the freeze was "red parse stops deploy" — now green), so prod is virtually certain to serve `ea660a00`, but that is circumstantial, not machine-verified. |

## G4b — what Matt confirms in one look

On the Vercel dashboard (project `reincarnated-glance`, `prj_R6SCwuSmezW19HPOLWKoJfMCxeYx`):
the production deployment for commit `ea660a00` is **READY** and aliased to prod (newer than
the frozen `e5ea8584`). If the on-session token were live I'd have closed this myself — flagging
`matt_to_do`: refresh the local Vercel CLI auth token so future GLANCE-RESTORE-class runs can
self-close G4b.

## Constraints honored

- `corpus.db` READ-ONLY — never written (export reads only).
- Touched nothing outside `glance/` + this note + `glance/AGENT_STATE.md`.
- No secondary-cause chasing: G2 + G3 went green on the fresh sidecar (staleness WAS the sole
  cause) — no fallback-HALT needed.

## Findings (not fixes)

1. **G4b self-closure gap:** the local Vercel CLI is uninstalled and the on-disk token is expired.
   Any run whose exit predicate includes "prod serves commit X" cannot self-verify from-session
   without one of them. Charter's fallback covered it, but it's a recurring tax → `matt_to_do`.
2. **glance.yml Actions** still forced onto Node 24 (checkout@v4 / setup-node@v4 target the
   deprecated Node 20). Non-blocking annotation only; noted for a future action-version bump.

**Signed:** drax, 2026-07-23.
