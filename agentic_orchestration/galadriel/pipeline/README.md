# Galadriel capture pipeline

**Owner:** galadriel (visual-perception steward).
**Status:** v0.1 — single-night sprint scaffold; iterates as needed.
**Purpose:** headless Chromium capture harness for state-matched demo captures + cross-viewport regression checks against the canonical DoE reference set at `../reference-images/`.

The Mirror does not score what the picture has not shown plainly. The pipeline is the apparatus that makes the picture sit still long enough to be looked at.

---

## What this is

A small Node/Playwright harness that:

1. Launches headless Chromium at a named viewport (per `states.json` `_viewports`)
2. Navigates to a named demo state (per `states.json` `states`, which encodes the `?debug=true&debug-state=<name>` URL pattern shipped by drax-D11.5)
3. Waits for the demo to emit a known console signal confirming the state is active
4. Lets atmospheric layers + pixi tickers settle for `warmup_ms`
5. Saves a viewport-sized PNG + a JSON sidecar with full provenance (demo git SHA, console log tail, URL, viewport, timestamps)

Captures land under `agentic_orchestration/galadriel/captures/<YYYY-MM-DD>/<state>/<viewport>/capture.png` plus `capture.json` alongside.

## Dependencies

Local-install only — never global.

- `playwright@1.49.0` (Apache-2.0, Microsoft) — headless Chromium driver

Install:

```bash
cd agentic_orchestration/galadriel/pipeline
npm install
npx playwright install chromium   # downloads Chromium browser binary (~150-200MB) locally
```

The `node_modules/` + Playwright browser cache stay local; not committed (see `.gitignore`).

## Quick start (assumes demo dev server is running)

```bash
# 1. In one terminal — start the demo dev server
cd ~/Games/reincarnated-demo
npm run dev   # serves at http://localhost:5173

# 2. In another terminal — run the harness
cd ~/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline

# Smoke-test: 1 state × 1 viewport
node capture.mjs --smoke

# Primary capture — comparison-grade combat-midfight (REQUIRES drax-D11.5 hook)
node capture.mjs --state combat-midfight --viewport mobile-portrait-1290x2796

# Full sweep — all states × all listed viewports
node capture.mjs --all-states
```

## Args

| Flag | Meaning | Default |
|---|---|---|
| `--smoke` | shorthand for `--state landing --viewport mobile-portrait-390x844` | — |
| `--state <name>` | state name from `states.json` | — |
| `--viewport <name>` | viewport name from `states.json _viewports`; defaults to all listed for state | all listed |
| `--out-dir <path>` | base output dir | `../captures` |
| `--dev-url <url>` | dev server URL | `http://localhost:5173` |
| `--all-states` | loop all states × all listed viewports | off |

## States

See `states.json`. Current set (2026-05-18):

| State | DoE ref | D11.5 required? | Purpose |
|---|---|---|---|
| `landing` | none | no | Pre-D11.5 fallback / smoke baseline / cross-viewport regression check on whatever-state default |
| `combat-midfight` | `DOE-combat-whisper-rift-2-2026-05-17.png` | YES | PRIMARY comparison-grade |
| `combat-empty-room` | none | YES | HUD-only inspection (typography + UI register axis) |
| `inventory-open` | none | YES | Inventory-UI inspection (no DoE inventory ref in current set) |

The wait_for signal each state expects matches drax-D11.5 dispatch spec: `[debug-state] activated=<name>`. If drax ships a different log signature, update `states.json` `wait_for` fields accordingly — the harness records `wait_for_satisfied: false` in the sidecar and notes the friction; the capture still produces a PNG so the failure is visible, not silent.

## Viewports

| Name | WxH | DPR | Mobile? | Notes |
|---|---|---|---|---|
| `mobile-portrait-1290x2796` | 1290×2796 | 3 | yes | iPhone 14 Pro Max class — DoE references exactly match this aspect |
| `mobile-portrait-390x844` | 390×844 | 3 | yes | iPhone 14 class — common-phone regression check |
| `mobile-portrait-375x667` | 375×667 | 2 | yes | iPhone SE class — small-phone regression check |
| `desktop-1920x1080` | 1920×1080 | 1 | no | canonical PC resolution; non-DoE comparison |

## Sidecar metadata

Every capture writes a JSON sidecar (`capture.json`) alongside the PNG with:

- `state`, `state_purpose`, `viewport`, `viewport_spec`
- `dev_url`, `full_url`, `doe_reference` (cross-link to the canonical DoE comparison image)
- `demo_git_sha`, `demo_git_short_sha` (reproducibility anchor)
- `captured_at_utc`, `ok`, `error`
- `wait_for`, `wait_for_satisfied`, `warmup_ms`
- `friction_notes` (e.g., "wait_for signal not observed within 15s — D11.5 hook unshipped")
- `console_log_tail` (last 200 console messages — useful for diagnosing render or state-setup failures)
- `capture_png` (relative path to the PNG)
- `pipeline_version`

## Discipline

- **Reproducibility-first.** Sidecar records everything an independent re-run needs.
- **No silent transformation.** Captures are raw PNGs. Any later crop / histogram / pHash computation is a separate script with its own provenance.
- **State-determinism is upstream.** The pipeline does not seed game state; drax-D11.5 owns that. If determinism fails, the friction is recorded in the sidecar; the capture is not silently discarded.
- **Smoke before full.** Always `node capture.mjs --smoke` first when (a) the dev server has just restarted, (b) the demo SHA has changed, or (c) the pipeline code has changed.
- **Attribution.** `package.json:attribution` records Playwright provenance (Apache-2.0). See `package.json:author` for galadriel ownership.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Permission denied` on `npx playwright install` | first-run browser-download permissions | run with elevated permissions OR install Chromium globally and point Playwright at it via `PLAYWRIGHT_BROWSERS_PATH` |
| `wait_for signal "[debug-state] activated=…" not observed within 15s` | drax-D11.5 hook not shipped at demo SHA OR demo emits a different log signature | check `capture.json:console_log_tail` for what the demo actually emits; update `states.json:wait_for` accordingly OR wait for drax-D11.5 to land |
| Captured PNG is all-black or all-white | demo failed to render at headless viewport size; pixi context might not have initialized | (a) increase `warmup_ms` in states.json; (b) check `console_log_tail` for pixi or asset-load errors; (c) try the `desktop-1920x1080` viewport to isolate whether it's mobile-specific |
| Captured PNG is white-with-letterbox | demo loaded but didn't paint its canvas; possibly orientation-overlay covering the scene at this viewport | check whether the demo's portrait orientation overlay is triggered (`mobile.ts` logic); the harness may need to set additional viewport hints |
| Dev server returns 404 on `?debug=true&debug-state=…` | demo's index.html doesn't read URL params for debug routes (pre-D11.5) | wait for drax-D11.5 to land |
| `Error: Browser closed unexpectedly` | flaky headless Chromium boot | re-run; if persistent, `npx playwright install chromium` to refresh browser binary |

## Future work (Phase-2+)

- pHash / dHash perceptual-hash extraction for low-frequency structural similarity vs reference set
- HSV histogram extraction + cosine-similarity scoring per region (color register axis)
- Canny edge density per region (visual-busyness axis)
- OCR sweep on captures for HUD text inventory comparison
- Sprite-pose detection for animation cadence (multi-frame captures + diff)
- CLIP image embedding for "structurally similar" similarity at higher abstraction
- Reference-set extension (Matt-captured DoE additions: character-select, inventory, mid-rift transition, boss-fight, death screen)

These iterate as the rubric matures; pipeline v0.1 is the apparatus, not the analysis.

---

*Authored 2026-05-18 by galadriel. The Mirror's pipeline. May the captures reveal what the surfaces actually show.*
