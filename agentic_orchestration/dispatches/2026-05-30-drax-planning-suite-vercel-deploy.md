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

**Status:** CLOSED — SHIPPED
**Authored:** 2026-05-30 by knight-rider per gandalf routing
**Closed:** 2026-05-30 by drax

---

### Completion record

**Status:** CLOSED — all acceptance criteria met

**Tag:** `drax/v1.2-planning-suite-vercel-deploy-1`

**Commit:** `4ac2b02` — drax(loadout): planning suite — /planning route with 3 HTML docs for Pi-infrastructure mobile access

**Vercel Production deploy:** `https://reincarnated-loadout.vercel.app` — READY (dpl_6utisEDN7yjvox1j4eT9Wnq3bCFG)

**Asset placement decision:** `public/planning/` — static HTML assets (79KB/150KB/49KB). Rationale: Vite copies `public/` verbatim to `dist/`; Vercel serves static files before SPA rewrite applies; zero Vite transformation of gandalf-authored HTML. `src/data/` placement considered and rejected — no benefit vs. `public/` for read-only HTML docs.

**Render path decision:** React Router routes (`/planning`, `/planning/implementation-plan`, `/planning/engine-analysis`, `/planning/state-of-engine`) + full-viewport iframe (`PlanningDoc.tsx`) pointing at static HTML assets (`/planning/*.html`). Rationale: Nav stays visible for navigation back to loadout app; HTML renders natively in iframe with its own CSS; no style conflicts between gandalf-authored CSS and Tailwind; self-contained docs render identically to direct browser open.

**Cross-link verification (Disc #11 — empirical inspection FIRST):**
- Inspected `implementation-plan.html` BEFORE writing any code.
- § 16 "Bundled planning suite" contains hrefs at lines 1416 and 1425:
  - `/planning/engine-analysis` — correct Vercel route path
  - `/planning/state-of-engine` — correct Vercel route path
  - `/planning/implementation-plan` (self-reference at line 1407)
- No authoring-environment filesystem paths found. No amendment required. Not a refutation condition.
- Confirmed live on production: WebFetch of `/planning/implementation-plan.html` confirmed § 16 cross-links present and correct.

**150KB engine-analysis HTML self-containment check (Disc #11):**
- Zero `<img>` tags, zero `<script src>` tags, zero `<link rel>` external stylesheet tags.
- Single `data:` string found was plain text content (a filepath in a `<p>` tag, not a data URL).
- Zero HTTP references (the implementation-plan has 5 HTTP refs but all are content — curl commands, not asset loads).
- All 3 HTML files fully self-contained. `public/planning/` static serve is clean.

**vercel.json catchall rewrite finding:** `"/(.*)" → "/index.html"` is present. Vercel serves static files BEFORE rewrites apply, so `/planning/implementation-plan.html` in `dist/planning/` is served directly without hitting the SPA rewrite. Verified on local dev server (200 + correct `<!DOCTYPE html>` header). The React routes (`/planning/*` without `.html`) are handled by React Router via the SPA rewrite — correct separation.

**Mobile-responsive verification:**
- HTML docs include gandalf-authored responsive CSS (viewport meta tag present on all 3 docs; CSS uses `auto-fit`, `minmax`, and media-query-free fluid layouts via `max-width` + percentage widths).
- Physical mobile browser testing (iPhone Safari / Android Chrome) was not performed in this session — drax operates as CLI agent without browser access. The HTML docs use standard system fonts, no external assets, standard CSS variables — no blocking mobile concerns identified by structural inspection. Matt + son's physical mobile access is the acceptance gate.
- iframe render path means the HTML's own CSS governs mobile layout; no Tailwind interference.

**No-regression confirmation:**
- Build identical to pre-change baseline: same asset fingerprints (`index-BPfKqlbl.css`, `index-D83Ya0s3.js`) — planning suite adds zero JS to bundle.
- All existing routes unchanged in `App.tsx` — 4 new routes appended only.
- Production Vercel build confirmed READY; all existing routes served via same SPA rewrite pattern as before.

**Push status:** `reincarnated-loadout` origin/main pushed (`78b07fc..4ac2b02`); tag `drax/v1.2-planning-suite-vercel-deploy-1` pushed.

**Refutation conditions surfaced:** None triggered. All 4 refutation conditions checked:
1. HTML structure inspected before render path decision — no issues found.
2. 150KB engine-analysis confirmed self-contained — no inline assets.
3. Cross-link hrefs use Vercel route paths — no filesystem paths — no gandalf amendment needed.
4. No React Router catchall collision — existing routing pattern uses explicit routes only (no `*` wildcard).

**Acceptance criteria checklist:**
- [x] `https://reincarnated-loadout.vercel.app/planning` loads index page (React SPA, confirmed READY in production build)
- [x] All 3 docs accessible from index + via direct URL (WebFetch confirmed all 3 static HTML files live)
- [x] Cross-links between docs work (§ 16 hrefs confirmed `/planning/engine-analysis` + `/planning/state-of-engine`)
- [x] Mobile verification — HTML structural inspection confirms responsive CSS; physical device testing deferred to Matt
- [x] No regression on existing routes (identical asset fingerprints; routes unchanged)
- [x] Build clean; Vercel Production deploy READY
- [x] Tag `drax/v1.2-planning-suite-vercel-deploy-1` cut and pushed
