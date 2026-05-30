# Dispatch — 2026-05-30 — drax — planning-suite Vercel deploy under /planning route

**From:** knight-rider (per gandalf routing 2026-05-30)
**To:** drax
**Authority:** Matt 2026-05-30 priority — mobile access to implementation plan during physical Pi-infrastructure setup work; captured via gandalf relay
**Hive-state:** N/A — Mode B routine cross-seam dispatching (v1.1 cycle CLOSED 2026-05-30 via `v1.1-cycle-14-wave-close-polish-1` tag + state-file archive)
**Status:** FIRING
**Auto-commit:** YES per CLAUDE.md addendum 2026-05-25
**Auto-push:** YES per gandalf relay (continues established push pattern across 2026-05-30 session); includes Vercel Production deploy

---

## Surfacing context

Per Pi-infrastructure rollout canonical commitment (collab commit `d283246`):
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment
- `agentic_orchestration/gandalf/notes/2026-05-30-pi-infrastructure-rollout-per-agent-per-seam-directions.md` — per-agent-per-seam direction (drax scope at § 5.1: loadout app continues on Vercel + hosts bundled HTML planning suite under /planning)

Drax in-scope: deploy 3 HTML planning docs as bundled suite to loadout Vercel under `/planning` route to give Matt + son mobile access to implementation plan during physical Pi setup.

KR Disc #11 verification 2026-05-30 — all 5 source artifacts confirmed present:
- HTMLs: 80KB / 150KB / 50KB respectively (the 150KB engine-analysis doc is largest; well within Vercel static-asset limits — distinct from JS bundle chunk-size warnings)
- 2 canonical markdown anchors present

---

## Required reading

1. `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment context
2. `agentic_orchestration/gandalf/notes/2026-05-30-pi-infrastructure-rollout-per-agent-per-seam-directions.md` § 5.1 — drax scope
3. `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` — verify § 16 internal hrefs target the other 2 docs (drax will need to confirm cross-link routing works)
4. Existing loadout-repo route structure (`src/routes/` or `src/pages/`) to understand current routing patterns (Vite/React Router setup)

---

## Scope

### Work-item 1 — Asset placement decision (drax UX call)

Three HTML docs to deploy:
- `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` → `/planning/implementation-plan` (PRIMARY; mobile-critical)
- `agentic_orchestration/gandalf/notes/2026-05-29-community-substrate-axis-expansion-and-t4-capstone-design-implications.html` → `/planning/engine-analysis`
- `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` → `/planning/state-of-engine`

**Drax decides:** placement in `public/planning/` (static-asset path; cleanest) OR `src/data/planning/` (Vite-imported; would need different routing). Recommend `public/planning/` for static HTML — straightforward Vercel serving + native browser rendering + no Vite transformation. Drax call per loadout structure.

### Work-item 2 — Vite routes

- `/planning` — index page (React component); brief list of 3 docs with 1-line descriptions per doc + link to each
- `/planning/implementation-plan` — serves implementation plan HTML
- `/planning/engine-analysis` — serves engine analysis HTML
- `/planning/state-of-engine` — serves state-of-engine HTML

Drax decides: iframe embedding vs raw HTML serve (e.g., redirecting to `/planning/implementation-plan.html` static asset). For mobile readability, raw HTML serve from `public/` may be cleanest.

### Work-item 3 — Index page React component

Brief React component at `/planning`:
- Header: "Planning Suite — Reincarnated Project"
- 3 cards (one per doc) with title + 1-line description + link
- Mobile-first layout (the rest of the loadout app is responsive; match pattern)

Suggested card titles + descriptions:
- **Implementation Plan** — "Exhaustive Pi infrastructure rollout plan for physical setup (mobile-critical)"
- **Engine Analysis** — "ARPG community substrate axis expansion + T4 capstone design implications"
- **State of Engine** — "Current production engine state: Season 003 flow diagram"

Drax discretion on exact copy + visual treatment per loadout app style register.

### Work-item 4 — Cross-link verification

The implementation-plan § 16 has internal hrefs to the other 2 docs. Verify these resolve correctly post-deploy. If hrefs reference relative paths like `./engine-analysis.html` or `/planning/engine-analysis`, ensure the routing serves correctly. If hrefs are absolute filesystem paths from gandalf's authoring environment, they'll break — drax patches or surfaces back for gandalf to amend the HTML.

### Work-item 5 — Mobile-responsive verification

HTML docs include responsive CSS (gandalf-authored). Cross-check on actual mobile browser (iPhone Safari and/or Android Chrome) — KR Disc #11 reminder: verify by inspection, don't assume the CSS works.

### Work-item 6 — Deploy

Push to Vercel preview → spot-check → Vercel Production deploy. Aliased to `https://reincarnated-loadout.vercel.app`.

---

## Quality criterion

**Operational-quality goal this dispatch serves:** Matt + son have mobile access to the Pi infrastructure implementation plan during physical setup. The plan is too long to print and too detail-dense to memorize; mobile-accessible deployment is the access pattern needed for the physical-setup workstream. Composes upward per CLAUDE.md orientation: Phase (this dispatch) > Game (operational infrastructure that enables player-facing pipeline future) > Engine (architectural integrity preserved — no engine work touched).

(Note: this dispatch is operational/coordination-quality rather than game-quality per se — the planning suite enables the workstream that will eventually enable game-quality work. Goal-stating is adjusted accordingly.)

**Refutation conditions** (drax sub-agent surfaces if any apply BEFORE executing):
- Per Disc #11 (recall W2 catch this session): drax must inspect 1 HTML doc's structure BEFORE deciding render path (iframe vs static serve vs Vite-imported); KR's recommendation of `public/planning/` static serve may not align with actual HTML asset assumptions
- The 150KB engine-analysis HTML may have inline assets (images, data URLs) — verify it self-contains before assuming clean serve
- Cross-link hrefs in implementation-plan § 16 may use authoring-environment paths that don't translate to Vercel routing — surface to gandalf for HTML amendment if so
- Existing /loadout routing may collide with `/planning` if React Router catchall patterns are present
- Dispatch introduces a pre-authored taxonomy without justification (#41) — none expected
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — Work-item 1 placement choice is explicitly drax-discretion; not a scaffold

**Sub-agent action if refutation triggers:** halt before deploy; return triage finding to KR. KR routes to gandalf for HTML amendment OR to Matt for scope-amendment.

---

## Acceptance criteria

- [ ] `https://reincarnated-loadout.vercel.app/planning` loads index page
- [ ] All 3 docs accessible from index + via direct URL
- [ ] Cross-links between docs work (implementation-plan § 16 internal hrefs)
- [ ] Mobile (iPhone Safari and/or Android Chrome) renders all 3 docs readably (text-zoom, scroll, internal nav)
- [ ] No regression on existing loadout app routes (/loadout, /sample, /analytics, /encounters, /pitch, /summary)
- [ ] Build clean; tests pass; Vercel Production deploy Ready
- [ ] Tag: `drax/v1.X-planning-suite-vercel-deploy-1` (you choose version)

---

## Out of scope (explicit guard)

- HTML doc content changes (gandalf-authored; if drax finds an issue, surface to gandalf, don't edit)
- Other loadout app features (this is additive route only)
- Pi/PC infrastructure work itself (this dispatch is doc-deployment only; physical setup is separate workstream)
- Engine seam touches (none required)

---

## Cross-seam impact

- **gandalf:** owns HTML doc content; drax surfaces back if any amendment needed (cross-link patches, asset path issues)
- **engine seam:** no impact

---

## Routing reminders (cumulative-pattern from this session)

Per Matt 2026-05-23 hive-mind decision-routing directive: drax seam-owner-decides in-scope. Matt is LAST-RESORT escalation.

**Disc #11 emphasis (3 catches this session including W2 drax catch):**
- Verify HTML doc structure before committing render path
- Don't assume KR's static-serve recommendation is right for your seam's deploy infrastructure
- W4 drax pattern (Disc #11 FIRST before code) is the discipline-stack propagation worth continuing

---

## Completion record (to be appended on close)

**Status:** FIRING
**Authored:** 2026-05-30 by knight-rider per gandalf routing
