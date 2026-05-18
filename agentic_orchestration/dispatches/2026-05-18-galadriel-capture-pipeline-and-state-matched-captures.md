# 2026-05-18 — galadriel — Capture pipeline + state-matched DoE-comparison captures (Track C; primary owner)

**Authority:** Matt L3 morning 2026-05-18 verbatim "approve galadriel agent file" → `.claude/agents/galadriel.md` dropped in at commit `85a4629`. Track C reroute per Matt L3 morning verbatim "reroute Track C to galadriel."
**Type:** Pattern B; ~2-2.5 hours (Playwright install + pipeline + state-matched captures).
**Predecessor:** drax-debug-state-url-hook-D11-5 dispatch must land first (D11.5 hook must exist so captures can be state-matched). Open drax terminal is executing that.
**Status:** 🟡 **QUEUED — fires AFTER drax-D11.5 D11.5 hook lands. Galadriel session opens; D11.5 readiness is the gate.**
**Tag intent:** none (tooling under `agentic_orchestration/galadriel/pipeline/`; not engine/demo code).
**Supersedes:** `2026-05-18-drax-galadriel-workaround-capture-pipeline-and-state-matched-captures.md` (workaround under deferred-agent-creation; that dispatch is now ⛔ DO NOT EXECUTE).

---

## Native ownership returns

The original Track C dispatch routed this work to drax as a stand-in because galadriel agent file could not be created at sprint activation (overnight knight-rider Write-tool denial; bash `cp` succeeded on morning approval). Galadriel is the natural author — pipeline lives under `agentic_orchestration/galadriel/pipeline/`, captures under `agentic_orchestration/galadriel/captures/`, methodology per AGENT-DRAFT.md (now committed to `.claude/agents/galadriel.md`).

Drax retains Track A (mobile-render validation + D11.5 debug-state hook) + Track B (loadout analytics) work. The handoff: drax ships D11.5 → galadriel session reads `?debug-state=combat-midfight` is live → builds capture pipeline.

---

## Scope — UNCHANGED from superseded workaround dispatch

All deliverables, methodology, file paths, hard NOs identical to the superseded dispatch. Read the superseded dispatch in full for the detailed specification (kept in place for archival reference + content-mirror — it's not deleted, just marked DO NOT EXECUTE).

**Deliverables (capsule):**
1. Playwright (or Puppeteer) headless capture pipeline at `agentic_orchestration/galadriel/pipeline/{capture.mjs, states.json, package.json, README.md, .gitignore}`
2. Primary captures (combat-midfight @ mobile-portrait-1290×2796 vs `DOE-combat-whisper-rift-2-2026-05-17.png`)
3. Secondary captures (mobile-portrait-390×844 + 375×667 + desktop-1920×1080 + combat-empty-room state)
4. Capture-set summary at `agentic_orchestration/galadriel/captures/2026-05-18/CAPTURE-SET-SUMMARY.md`

**Town-surface gap statement:** demo is dungeon-only; DoE refs #2-7 town states have no demo counterpart. Document as structured finding, not forced capture.

**Methodology:** Discipline #1 math-before-code (state determinism done in D11.5 dispatch) + Discipline #2 smoke-test (1 state × 1 viewport smoke before full set) + Discipline #11 attribution (dep version pins + license notes).

---

## Required reading

1. Superseded dispatch — `2026-05-18-drax-galadriel-workaround-capture-pipeline-and-state-matched-captures.md` (read in full for detailed spec; ignore the SUPERSEDED banner)
2. Overnight sprint invocation Track C § 2.3 — `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md`
3. `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — 7 DoE reference frames
4. `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE feel-target canon
5. `.claude/agents/galadriel.md` (was AGENT-DRAFT.md) — your own methodology spec
6. drax-D11.5 dispatch completion record (must be present before pipeline runs)

---

## Coordination

- **Native owner now:** galadriel (was drax stand-in)
- **Predecessor blocker:** drax-D11.5 debug-state hook (drax executing in parallel; check his completion record before starting captures)
- **Triggers downstream:** rubric authorship + benchmark report (separate dispatch — galadriel + gandalf critique-pair; see `2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md`)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 morning by knight-rider per Matt L3 Track C reroute. Native ownership restored. Sprint Track C executes under galadriel's own identity.*
