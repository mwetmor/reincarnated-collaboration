# Dispatch — 2026-05-30 — drax — planning-suite refresh: PC spec report integration

**From:** knight-rider (per gandalf routing 2026-05-30 follow-on to prior planning-suite deploy)
**To:** drax
**Authority:** Matt 2026-05-30 PC spec report integration; captured via gandalf relay
**Hive-state:** N/A — Mode B routine follow-on (initial planning-suite dispatch CLOSED at `drax/v1.2-planning-suite-vercel-deploy-1` 2026-05-30)
**Status:** FIRING
**Auto-commit:** YES per CLAUDE.md addendum 2026-05-25
**Auto-push:** YES per established 2026-05-30 session pattern; includes Vercel Production deploy

---

## Surfacing context

PC procurement closed per Matt 2026-05-30 `SYSTEM_SPECS_FOR_PIPELINE.md` report (collab repo root). Implementation plan HTML § 9 (PC) + § 10 (Unreal install) updated to reflect:
- PC already in hand (MSI MAG Codex R2; specs documented)
- Unreal 5.4 + 5.5 + full toolchain already installed (skip install steps; pivot to configuration)
- 3 immediate hardware actions surfaced (XMP/EXPO BIOS enable + BIOS update for Intel 13/14th gen voltage-stability microcode + wired ethernet connection)
- 2 upgrade recommendations (64GB RAM; secondary NVMe; not blockers)
- VRAM management strategy for Reincarnated workflow
- UE 5.4 vs 5.5 version recommendation

Source HTML refreshed by gandalf at `8fce404` (collab); file size grew from ~79KB → ~92KB confirming content landed. KR Disc #11 grep confirmed 7 references to MSI MAG Codex / XMP / EXPO / Intel 13/14 inside the HTML.

Canonical doc `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` § 5 also amended (PC procurement closed; rollout sequencing impact noted).

---

## Required reading

1. `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` § 9 + § 10 — verify update structure (collapse details for original procurement discussion expected)
2. `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` § 5 — canonical context (PC procurement closed amendment)
3. `SYSTEM_SPECS_FOR_PIPELINE.md` (collab repo root) — Matt's PC spec report (anchor source)
4. Your prior dispatch close record at `agentic_orchestration/dispatches/2026-05-30-drax-planning-suite-vercel-deploy.md` — render path decisions you made (public/planning/ + full-viewport iframe; commit `aebcdf7`)

---

## Scope

### Work-item 1 — Re-copy updated implementation-plan HTML

Re-copy `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` → loadout repo `public/planning/implementation-plan.html` (the path you chose in initial dispatch; stick with it per gandalf "if drax already deployed initial dispatch with one path choice, stick with that for the amendment").

### Work-item 2 — Other 2 docs unchanged

`engine-analysis.html` + `state-of-engine.html` unchanged. No re-copy needed unless you want single-commit consistency refresh — drax call.

### Work-item 3 — Mobile-responsive verification of updated § 9-10

The new `<details>` collapse for original procurement discussion should render correctly on mobile browsers. Verify via inspection (Disc #11 — continuing the W2/W4/initial-planning-suite empirical pattern).

### Work-item 4 — Re-build + re-deploy

Same `/planning` routing as established by initial dispatch — no route changes. Push to Vercel preview → spot-check → Vercel Production deploy.

---

## Quality criterion

**Operational-quality goal this dispatch serves:** Matt + son have current mobile-accessible implementation plan reflecting actual PC state + 3 immediate hardware actions (XMP/EXPO BIOS enable + BIOS update for Intel 13/14th gen voltage stability + wired ethernet) needed before sustained Pi infrastructure work. Configuration framing replaces procurement framing throughout § 9-10. Pattern: documentation surface MUST track reality once Matt closes a procurement decision; staleness would mis-route the physical-setup workstream.

**Refutation conditions** (drax sub-agent surfaces if any apply BEFORE executing):
- Source HTML at `8fce404` is somehow not in fact updated (Disc #11 spot-check inspection of § 9-10 content before copy)
- `<details>` collapse element renders poorly on mobile (gandalf-authored; surface back to gandalf if browser-incompatible, don't drax-patch)
- File size growth (~92KB; was ~80KB) somehow affects Vercel static-serve performance — verify on actual mobile network if concern surfaces
- Existing /planning routing somehow regresses on the refresh — verify other 2 doc routes still serve post-deploy

**Sub-agent action if refutation triggers:** halt before deploy; return triage finding to KR. KR routes to gandalf for HTML amendment OR to Matt for scope-amendment.

---

## Acceptance criteria

- [ ] `https://reincarnated-loadout.vercel.app/planning/implementation-plan` reflects updated § 9 (actual PC profile + 3 immediate actions) and § 10 (Unreal already installed status)
- [ ] `<details>` collapse for original procurement discussion expands cleanly on click
- [ ] Other bundled docs unaffected (`/planning/engine-analysis` + `/planning/state-of-engine` continue rendering at their routes)
- [ ] No regression on existing loadout app routes
- [ ] Build clean; tests pass; Vercel Production deploy Ready
- [ ] Tag: `drax/v1.X-planning-suite-refresh-pc-spec-1` (you choose version)

---

## Out of scope (explicit guard)

- HTML doc content changes (gandalf-authored; surface back if issue found)
- Other loadout app features
- Pi/PC physical infrastructure work itself (doc-deployment only)
- Engine seam touches (none required)
- /planning routing changes (initial dispatch's routing stays; this is content-refresh only)

---

## Cross-seam impact

- **gandalf:** owns HTML content; drax surfaces back if mobile-render issue with `<details>` collapse or any content-amendment need
- **engine seam:** no impact

---

## Completion record (to be appended on close)

**Status:** FIRING
**Authored:** 2026-05-30 by knight-rider per gandalf follow-on routing
