# 2026-05-18 — drax — Galadriel-workaround capture pipeline + state-matched DoE-comparison captures (Track C; deferred-agent-creation posture)

> ⛔ **SUPERSEDED 2026-05-18 morning by Matt L3 reroute.** Galadriel agent file approved + dropped in (`.claude/agents/galadriel.md` commit `85a4629`). Track C work returns to its native owner. **Drax: DO NOT EXECUTE this dispatch.** New owner: galadriel. New dispatch: `2026-05-18-galadriel-capture-pipeline-and-state-matched-captures.md` — identical scope, galadriel-primary authorship, same destination paths (`agentic_orchestration/galadriel/pipeline/` + `captures/`). Drax's Track A + Track B work continues unchanged.

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track C § 2.3 deliverables 11 + 11.5 (already in drax-D11.5 dispatch) + capture-pipeline portion of deliverable 11; pre-authorization matrix § 6 rows 8, 9, 10.
**Type:** Pattern B; ~2-2.5 hours (includes Playwright install + pipeline + state-matched captures).
**Predecessor:** drax-debug-state-url-hook-D11-5 dispatch must land first (D11.5 hook must exist so captures can be state-matched).
**Status:** 🟡 **QUEUED — fires AFTER drax-D11.5 dispatch lands. Drax may interleave: D11.5 first (smaller), pipeline second.**
**Tag intent:** none (tooling under `agentic_orchestration/galadriel/pipeline/`; not engine/demo code).

---

## Why drax owns this tonight

Per morning-briefing L3-1 in `agentic_orchestration/hive-mind/morning-briefing-2026-05-19.md`: the `.claude/agents/galadriel.md` write was denied at sprint activation. Galadriel agent identity cannot be spawned as a subagent tonight. The work the agent would have done is preserved — drax has demo expertise + Node tooling experience + access to the demo dev server, so drax produces the capture pipeline tonight under the deferred-agent-creation workaround. Once Matt approves the agent file on morning, galadriel inherits the pipeline drax built and runs from there.

This is **galadriel's pipeline tools**, not drax's. Drax builds and runs tonight; galadriel (or galadriel-stand-in) owns it going forward. Pipeline code lives under `agentic_orchestration/galadriel/pipeline/`, not under `~/Games/reincarnated-demo/`.

---

## Required reading

1. The full invocation (above) — Track C § 2.3 entire section, especially deliverables 11 + 11.5 + 12
2. `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — the 7 DoE reference frames and their states
3. `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE feel-target canon; combat-state reading
4. `agentic_orchestration/galadriel/AGENT-DRAFT.md` — galadriel's intended methodology (the agent that should have built this pipeline; drax follows the same methodology as a stand-in)
5. drax-D11.5 dispatch completion record (must be present) — confirms `?debug-state=combat-midfight` works deterministically

---

## Deliverables

### Deliverable 1 — Playwright (or Puppeteer) headless capture pipeline

Lives at `agentic_orchestration/galadriel/pipeline/`. Structure:

```
agentic_orchestration/galadriel/pipeline/
  package.json              # local node deps; not committed to .gitignore-protected paths
  capture.mjs               # main headless capture harness
  states.json               # named demo-state configurations (URL param sets)
  README.md                 # how to run; what's parameterized; troubleshooting
  .gitignore                # node_modules
```

**`states.json`** example structure:
```json
{
  "combat-midfight": {
    "url_path": "/?debug=true&debug-state=combat-midfight",
    "viewports": ["mobile-portrait-1290x2796", "mobile-portrait-390x844", "mobile-portrait-375x667", "desktop-1920x1080"],
    "wait_for": "[debug-state] activated=combat-midfight",
    "warmup_ms": 2000,
    "doe_reference": "DOE-combat-whisper-rift-2-2026-05-17.png"
  },
  "combat-empty-room": {
    "url_path": "/?debug=true&debug-state=combat-empty-room",
    "viewports": ["mobile-portrait-1290x2796", "mobile-portrait-390x844"],
    "wait_for": "[debug-state] activated=combat-empty-room",
    "warmup_ms": 2000,
    "doe_reference": null
  },
  "inventory-open": { ... }
}
```

**`capture.mjs`** accepts:
- `--state <name>` (from states.json)
- `--viewport <name>` (from per-state viewports list; default: all)
- `--out-dir <path>` (default: `agentic_orchestration/galadriel/captures/<date>/<state>/<viewport>/`)
- `--dev-url <url>` (default: `http://localhost:5173`)
- `--all-states` (loop)

For each (state × viewport):
1. Launch headless Chromium at viewport
2. Navigate to `<dev-url><url_path>`
3. Wait for `wait_for` console log
4. Wait `warmup_ms` for atmospheric layers + animations to settle
5. Screenshot full page; save PNG with deterministic filename
6. Emit metadata JSON sidecar (timestamp, demo git SHA via subprocess, state, viewport, console_log_tail)

**`README.md`** documents how to run, install deps, and troubleshoot.

### Deliverable 2 — Primary captures (state-matched DoE comparison)

Run the pipeline against the live local dev server. Capture:

**Combat surface (matches DoE refs #1):**
- Viewport: mobile-portrait-1290×2796 (DoE's exact aspect)
- State: combat-midfight
- Output: `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/capture.png` + sidecar JSON

**Town surface (matches DoE refs #2-7):**
- The demo today is dungeon-only; **there is no town**. This is a Track C finding, not a capture.
- Drax does NOT produce a forced comparison.
- Drax notes in pipeline README + capture-set summary that town-surface is unaddressed in demo (consistent with invocation § 2.3 expected disposition).

### Deliverable 3 — Secondary captures (cross-viewport regression check)

Same primary `combat-midfight` state, but at:
- mobile-portrait-390×844 (iPhone 14)
- mobile-portrait-375×667 (iPhone SE)
- desktop-1920×1080

Plus `combat-empty-room` at mobile-portrait-1290×2796 (HUD-only inspection — useful for the rubric's typography + UI register axis without combat noise).

### Deliverable 4 — Capture-set summary

A `agentic_orchestration/galadriel/captures/2026-05-18/CAPTURE-SET-SUMMARY.md` listing:
- Every capture produced (state × viewport)
- Demo git SHA at capture time (for reproducibility)
- Any captures that FAILED (with FRICTION notes — e.g., "headless launched OK but `?debug-state=combat-midfight` produced empty render at SHA xyz; surface for morning review")
- Reference image cross-link per primary capture (which DoE ref pairs to which demo capture)
- Town-surface gap statement (one paragraph; consistent with invocation § 2.3 town-feel-gap framing)

---

## Methodology

**Discipline #1 (math-before-code):** State enumeration + state determinism math already done in drax-D11.5 dispatch. Pipeline reuses that math. No new pre-implementation math required here, but document any spawn-state seed values that the pipeline RELIES ON (e.g., "pipeline expects combat-midfight to spawn ≥3 monsters in viewable area; if fewer, OBSERVATION should be surfaced").

**Discipline #2 (smoke-test):** Before producing the full capture set, smoke-test the pipeline on one state × one viewport. Confirm:
- Headless launches without browser-install errors
- URL loads
- `wait_for` log emits
- Screenshot file saves
- Metadata sidecar saves
- File renders openable (drax visual-inspects locally; no broken PNG)

Only after smoke passes do the full captures run.

**Discipline #11 (attribution):** Pipeline README documents Playwright/Puppeteer choice + version pin; sharp version pin; any other deps.

**Reproducibility-first:** Captures include metadata sidecars with git SHA + timestamp + state + viewport. Another agent (or galadriel-on-morning) can re-run the pipeline against the same SHA and reproduce the captures within rendering variance.

---

## Out of scope

- Similarity scoring or rubric application (that's a separate dispatch / co-authored work with gandalf)
- Benchmark report authorship (separate; gandalf co-authors)
- Modifying demo or engine code (drax stays in `agentic_orchestration/galadriel/pipeline/`)
- Loadout analytics screenshots (separate iteration; happens after drax-loadout-analytics ships)
- Animation cadence comparison (stills only tonight; cadence is best-effort Phase-2)
- OCR for HUD text comparison (Phase-2)
- pHash / dHash / HSV histogram extraction (Phase-2 unless trivially included; not required for tonight's rubric)

## HARD NOs (per invocation § 6)

- No `git push --force`
- No Vercel demo deployment
- No vendor acquisitions (Playwright/Puppeteer are MIT-licensed open source; npm install is allowed per § 6 row 8)
- No CLAUDE.md or AGENTS.md modifications

## Completion handoff

1. Append completion record to this dispatch
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline)
3. Pipeline code + captures + summary all live under `agentic_orchestration/galadriel/`
4. Knight-rider then queues:
   - Rubric authorship (gandalf review of draft → drax-or-knight-rider applies → benchmark report)
   - Co-authored benchmark report at `canonical/story/visual-benchmark-vs2a-2026-05-18.md`

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track C § 2.3 (capture-pipeline portion). Single-night sprint cadence. Drax operates as galadriel-stand-in under deferred-agent-creation workaround; see morning-briefing L3-1.*
