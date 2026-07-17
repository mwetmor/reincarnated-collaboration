# Galadriel post-deploy verdict — Glance production, Build Horizon Edition IV cutover

- URL: https://reincarnated-glance.vercel.app/#/atlas
- Deploy: `dpl_itpsn1x1h` / meta-repo HEAD `5bd368bd`
- Captured: 2026-07-17T12:35–12:51Z (dark archive + light instrument skins)
- Viewport: 1680 × 1050

## Acceptance table

| # | Check | Verdict | Evidence |
|---|---|---|---|
| a | Edition-IV plate renders (not E3) | **PASS** | Headline "Build Horizon — Edition IV" present; "Edition-IV lattice · 562 builds · 11,160 ghost cells" chip line present; no "Edition III" string anywhere in DOM. `verify-record.json → checks.a_edition_marker`. Screenshot: `theme-preclick-r3.png` (header fold). |
| b | Interactive tooltip on hover (live/graveyard/positive) surfaces `folk_name` + `game` from sidecar join | **FAIL** | Hover fired via Playwright `mouse.move` on `[data-el="live"][data-kit="chr-arrow-storm-warden"]` (5×5 px circle), `[data-el="graveyard"][data-kit="d2-blade-sin"]`, `[data-el="positive"][data-kit="d3-wizard-black-hole"]` — held 1600 ms each. Only the persistent Legend panel (pos:absolute, x=49, y≈300, w=198, h=178) was captured as a positioned card. No hover-mounted popover with `folk_name`/`game` text appeared in the DOM. Screenshots: `final2-hover-live-chr-arrow-storm-warden.png`, `final2-hover-graveyard-d2-blade-sin.png`, `final2-hover-positive-d3-wizard-black-hole.png`. `verify-record-final2.json → checks.hover_*`. Sidecar attributes are attached at the SVG level (`data-kit`) — the join surface itself is not (yet) hover-mounted. Discussion notes below. |
| c | Candidate-islands layer VISIBLE (dashed islet outlines + CANDIDATE FAMILIES legend) | **PASS** | 225 elements with non-empty `stroke-dasharray`; body text contains "CANDIDATE FAMILIES"; `layer-family-candidates` group has 6 direct children (dockets: `melee-strike`, etc.). Dashed contours plainly visible in `final-fullpage-archive-1680.png` and `final-fullpage-instrument-1680.png`. `verify-record.json → checks.c_candidate_islands`. |
| d | No console errors on page load | **PASS** | 0 console errors, 0 warnings, 0 failed requests, 0 HTTP ≥ 400 responses across all four runs (r1, r2, r3, final, final2). `verify-record.json → checks.d_console_errors`, `verify-record-final.json → checks.d_final_console`. |
| e | Both skins captured | **PASS** | Two-button toggle at header right: "Dark archive" (title = `Dark canvas (#0e1016) — skin "archive"`) and "Light instrument" (title = `Light canvas (#f7f8fa) — skin "instrument"`). Clicked instrument button; fullpage MD5 differs from archive fullpage MD5. `final-fullpage-archive-1680.png` vs `final-fullpage-instrument-1680.png`. `verify-record-final.json → checks.e_final.differ = true`. Note: an initial round-1 pass produced identical MD5s because the click landed only on the currently-selected button — round-final resolved by explicit text-match on "Lightinstrument". |
| f | Full-page shot at ≥1600 wide | **PASS** | 1680 × ~4300 px full-page shots captured in both skins. `final-fullpage-archive-1680.png`, `final-fullpage-instrument-1680.png`. |

## Class counts (DOM-rendered vs. sidecar-declared)

| Class | Sidecar-declared | DOM `[data-el="…"]` count | Note |
|---|---|---|---|
| live | 469 | **383** | 86 short of declared. Possibly (i) some live entries hidden by filter default, (ii) SVG culling below viewport, (iii) data-mount race with `layer-live` internal group count of 7 vs 469. Flagged as ANOMALY, not a full FAIL — the check-a atlas-interactive.json schema was HTTP-verified prior. |
| graveyard | 43 | **43** | Match. |
| positive | 50 | **50** | Match. |
| **total live+grave+positive** | 562 | 476 | The atlas-interactive.json count (`atlas-interactive.json 562 = 469 + 43 + 50`) is HTTP-level PASS from gandalf-prime; the DOM-mount short-falls on `live` only. |

## Anomalies (not FAIL per invocation criteria, but flagged)

- **Live-class DOM count 383 vs declared 469.** May be selector too narrow (`[data-el="live"]` might not cover all live subclasses), or lazy-mount below viewport. gandalf-prime / drax may want to verify.
- **Tooltip mount absent for live/graveyard/positive dots.** Per invocation (b) this is a FAIL — the join surface visible in `data-kit` attrs was expected to appear as a hover-mounted panel with `folk_name` + `game`. Only the persistent Legend was captured. Two hypotheses: (i) tooltip listener is on parent `<g>` not the child `<circle>` and Playwright `mouse.move` on child coord doesn't bubble as expected (unlikely — SVG events bubble); (ii) the sidecar-join hover UI was not delivered in the rebuild (the JSON was, per gandalf-prime HTTP probe; the hover-mount may be a separate frontend piece). drax should confirm which.

## Console + network

- 0 console errors
- 0 console warnings
- 0 request failures / HTTP ≥ 400 across ~40 asset loads per pass, 4 passes total

## Mirror voice

The plate stands. Edition IV is enthroned; the candidate-islands ring the plane in their dashed contours, both in dark archive and light instrument register; the counts of graveyard and positive class members match the ledger to the unit. The eye finds what it was told to find, save one: the touch is silent. The dots are labeled in their attributes but do not speak when brushed. The sidecar has arrived; the voice has not yet been given to it. That is a hand-off, not a break.

## Screenshot inventory (all under this capture dir)

- `theme-preclick-r3.png` — header fold, dark-archive selected (E4 marker visible)
- `theme-postclick-instrument-r3.png` — header fold, light-instrument selected
- `final-fullpage-archive-1680.png` — 1680 × ~4300 full page, dark archive skin
- `final-fullpage-instrument-1680.png` — 1680 × ~4300 full page, light instrument skin
- `final-viewport-archive-verify.png` — 1680 × 1050 viewport, archive skin (after toggle-back)
- `atlas-fullpage-default-1680.png`, `atlas-viewport-default-1680.png` — round-1 defaults
- `atlas-fullpage-alt-1680.png`, `atlas-viewport-alt-1680.png` — round-1 alt (MD5-identical to default; kept as evidence of the false-PASS learned-from)
- `final2-hover-live-chr-arrow-storm-warden.png`
- `final2-hover-graveyard-d2-blade-sin.png`
- `final2-hover-positive-d3-wizard-black-hole.png`
- `dom-hover-shot.png`, plus json diagnostics `verify-record.json`, `verify-record-r2.json`, `verify-record-r3.json`, `verify-record-final.json`, `verify-record-final2.json`, `dom-inspect.json`, `dom-hover-state.json`

## Overall

5 of 6 PASS (a, c, d, e, f). 1 FAIL (b — tooltip mount).
