# 2026-05-18 — gandalf + drax — Visual benchmark report (Track C.13; rubric + first-pass scoring)

> ⛔ **SUPERSEDED 2026-05-18 morning by Matt L3 reroute.** Galadriel agent file approved + dropped in (`.claude/agents/galadriel.md` commit `85a4629`). Track C work returns to its native owner. **Drax: DO NOT EXECUTE this dispatch.** New owners: galadriel (primary author — rubric design + scoring application + report) + gandalf (critique-pair — design-interpretation review + Mirror voice). New dispatch: `2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md` — identical scope + same destination `canonical/story/visual-benchmark-vs2a-2026-05-18.md`. Drax's Track A + Track B work continues unchanged.

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track C § 2.3 deliverables 12 + 13; pre-authorization matrix § 6 row 11.
**Type:** Pattern B; ~3-5 hours total (rubric authoring + scoring + report co-authoring).
**Predecessor:** drax-galadriel-workaround-capture-pipeline-and-state-matched-captures dispatch completed; primary + secondary captures exist at `agentic_orchestration/galadriel/captures/2026-05-18/`.
**Status:** 🟡 **QUEUED — fires after capture pipeline produces captures.**
**Tag intent:** none (canonical-story doc; gandalf + drax co-authored).

---

## Why gandalf + drax as the co-authors

Galadriel is the natural author of this report. The agent file write was denied at sprint activation (see morning-briefing L3-1). Under deferred-agent-creation workaround:
- **Gandalf** owns rubric design + dissonance interpretation + Mirror-voice synthesis (gandalf has the design judgment; gandalf has been the canonical-story author of the DoE feel-target lock and the audio register canon)
- **Drax** owns evidence sections + scoring application + capture cross-link (drax produced the capture pipeline and the captures; drax can apply a rubric to evidence without making design judgments)

This pairing produces a benchmark report that's structurally equivalent to what galadriel would have authored, with gandalf adding the design-interpretation layer galadriel's persona spec explicitly delegates to gandalf anyway (see AGENT-DRAFT.md "with gandalf: tight critique-pair").

---

## Required reading

1. The full invocation (above) — Track C § 2.3 (entire section) for rubric axes + scoring methodology
2. `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE feel-target canon; gameplay-pattern read of combat ref
3. `agentic_orchestration/galadriel/reference-images/MANIFEST.md` — the 7 DoE reference frames
4. `agentic_orchestration/galadriel/captures/2026-05-18/CAPTURE-SET-SUMMARY.md` — what the capture pipeline produced (including any FAILED captures with FRICTION notes)
5. Individual captures under `agentic_orchestration/galadriel/captures/2026-05-18/<state>/<viewport>/`
6. `agentic_orchestration/galadriel/AGENT-DRAFT.md` — the report-section structure galadriel would have authored under (gandalf + drax follow this template)
7. `canonical/story/audio-register-canon-2026-05-17.md` — adjacent register canon (informs the synthesis voice register)

---

## Deliverables

### Deliverable 1 — Rubric draft

Lives at `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1.md`.

**Authored by:** gandalf (rubric design); drax can comment but does not own the axis selection.

Per invocation § 2.3 deliverable 12, axes for **combat surface** (apply to DoE-combat-whisper-rift-2 + demo combat-midfight):
- Visual density (foreground/background sprite count per viewport area)
- Color register (palette saturation/hue distribution; HSV histogram comparison if drax can extract it; manual scoring otherwise)
- Lighting + atmosphere (atmospheric-layer presence; depth cues; ambient particle work)
- Typography + UI register (HUD module placement; font choices; iconography; bottom-bar layout; vendor naming convention — combat surface has minimap + objective + skull counter to score)
- Reading order + hierarchy (what does the eye land on first?)
- Animation cadence (best-effort from stills — floating numbers, telegraphed-attack rectangles, particle bursts)

Axes for **town surface** (DoE refs #2-7; demo has NO town — surface is a structured gap-finding):
- All combat axes (where applicable)
- NPC density + variety (town axis only)
- Service-surface clarity (town axis only)

**Scoring scale:** 1-5 per axis. Each score paired with one-sentence rationale citing specific visual evidence.

**Phase-2 axes (note for future iteration):** OCR for UI text comparison; sprite-pose detection for animation cadence; CLIP image embeddings for "structural similarity at high level."

### Deliverable 2 — Scoring application

**Authored by:** drax (applies the rubric to capture pairs).

Per invocation § 2.3:
- Score combat surface (demo combat-midfight at mobile-portrait-1290×2796 vs `DOE-combat-whisper-rift-2-2026-05-17.png`)
- Record town surface as **structured gap finding**, not a score (DoE has 6 town states; Reincarnated has 0)
- Per-axis "DoE delta" callout naming the most visible dissonance for drax-engineering (different drax-instance) to address in v1.22+ planning

Output lives in the benchmark report (deliverable 3) as a scorecard table.

### Deliverable 3 — Benchmark report

Lives at `canonical/story/visual-benchmark-vs2a-2026-05-18.md`.

**Co-authored:** gandalf (sections 1, 4-rubric-interp, 5, 7, 8); drax (sections 2, 3, 4-scoring-table, 6).

Sections (per AGENT-DRAFT.md template):

1. **Reference set** (gandalf) — which 7 images, which states, MANIFEST.md cross-link
2. **Demo capture set** (drax) — which captures produced, viewports, states, CAPTURE-SET-SUMMARY.md cross-link, any captures FAILED
3. **Rubric** (drax) — the rubric used; cross-link to `rubrics/2026-05-18-rubric-doe-comparison-v1.md`; per-axis criteria summarized
4. **Per-state scorecard** (drax fills table; gandalf interprets table) — axis-by-axis scores; deltas; evidence callouts; per-axis evidence cite
5. **Strongest dissonances** (gandalf) — top 3-5 with specific recommendations for v1.22+ design direction
6. **Gaps and absences** (drax) — surfaces present in reference but not in demo. **Town-feel gap statement** (one paragraph): DoE has 6 distinct town states with rich service-NPC + ambient-NPC + multi-player density; Reincarnated mobile has zero. This is a finding, not a score. Drax surfaces as evidence; gandalf interprets in section 7.
7. **Gandalf interpretation** (gandalf) — design-meaning of the evidence; what to do next, what to defer; town-feel-gap design-direction implications
8. **Mirror voice** (gandalf; optional, reserved) — if the picture is genuinely revealing, the Mirror may speak; brief, evocative, evidence-anchored. Otherwise omit.

---

## Methodology

**Rubric quality criteria (per AGENT-DRAFT.md):**
- Per-axis evidence basis (extractable measurement or stated 1-5 criteria)
- Per-axis falsifiability (a "5" is defensible by pointing to specific evidence)
- Per-state applicability (combat axes vs town axes)
- Delta callouts (per-axis "what's the biggest dissonance")

**Anti-patterns to avoid:**
- Axes that bundle multiple things — split
- Scoring without rationale — every score gets a one-sentence cite
- Genre-median triangulation when no reference exists — town surface gets a finding, not a score

**Honesty discipline:**
- If demo combat-midfight capture has FAILED states or rendering artifacts, the rubric scores ONLY what the capture actually shows; absences are surfaced as scoring caveats
- "First-pass" is in the title; do not over-promise depth or precision tonight
- Mark report as DRAFT in title for v1; iterate next sprint

---

## Out of scope

- Implementing fixes for dissonances surfaced (drax-engineering's v1.22+ work)
- Town-surface implementation (Phase-2; design-direction question)
- pHash / dHash / CLIP embedding scoring (Phase-2)
- OCR for HUD text (Phase-2)
- Sprite-pose detection for animation cadence (Phase-2)
- Modifying any source code in demo / engine / loadout
- Re-curating reference images

## HARD NOs (per invocation § 6)

- No `git push --force`
- No vendor acquisitions
- No CLAUDE.md or AGENTS.md modifications
- No load-bearing canonical-doc amendments (this is a NEW canonical-story doc; new docs are pre-authorized per § 6 row 11)

## Halt conditions (per invocation § 2.3)

- Capture pipeline produced no usable primary capture → rubric scoring deferred; report includes capture-failure context as primary finding; gandalf's Mirror voice may speak to the absence
- Rubric methodology produces incoherent scores (e.g., demo scores higher on visual density than DoE — likely measurement artifact) → surface as OBSERVATION in hive log; gandalf reviews rubric; mark report as v1-DRAFT with explicit caveats

## Completion handoff

1. Both authors append completion record to this dispatch
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline) — single entry, author = "gandalf + drax"
3. Rubric lives at `agentic_orchestration/galadriel/rubrics/`
4. Report lives at `canonical/story/visual-benchmark-vs2a-2026-05-18.md`
5. Morning state-of-hive surfaces report as Track C primary value artifact
6. Matt morning reading order: morning-briefing → state-of-hive → loadout preview URL → visual benchmark report

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track C § 2.3 deliverables 12 + 13. Single-night sprint cadence. Co-authored gandalf + drax under deferred-agent-creation workaround; report destination identical to galadriel's intended path.*
