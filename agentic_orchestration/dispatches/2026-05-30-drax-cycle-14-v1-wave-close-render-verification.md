# Dispatch — 2026-05-30 — drax — Cycle 14 v1 wave-close render verification

**From:** knight-rider (per gandalf surface 2026-05-30; routing recommendation Item 2)
**To:** drax
**Authority:** Matt (PENDING fire-signal; gated on star-lord companion dispatch completion)
**Hive-state:** ACTIVE candidate — wave-close scope-extension downstream verification
**Status:** PENDING (blocked on star-lord companion dispatch close)
**Auto-commit:** YES upon fire (per CLAUDE.md addendum 2026-05-25)
**Auto-push:** PENDING per-workstream-pattern re-establishment

---

## Blocking dependency

This dispatch is GATED on completion of:
- `agentic_orchestration/dispatches/2026-05-30-star-lord-cycle-14-v1-wave-close-emit-pipeline-extension.md`

When star-lord completes (158 class files re-emitted with 12 skills + 11 gear slots + non-fabricated stat_distribution; manifest `placeholder_skill_content: false`), this dispatch fires.

---

## Surfacing context

Same surface as star-lord companion dispatch — gandalf 2026-05-30 surface: /loadout + /sample pages render blank skills + blank gear + 100/10/10/10 stats for Cycle 14 wave-5 seasons. Star-lord companion dispatch closes the engine-side data plumbing; this dispatch verifies player-surface render.

---

## Required reading

1. `~/Games/reincarnated-collaboration/canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1.1 (Rank-0 amendment) + § 1.2 (Sample tab Cycle 15+ scope)
2. `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` § 4 — stat distribution rendering
3. `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.68 (star-lord-authored as part of companion dispatch)
4. `~/Games/reincarnated-loadout/src/pages/Loadout.tsx` — current render path
5. `~/Games/reincarnated-loadout/src/pages/Sample.tsx` — current render path (scope-bounded; see below)

---

## Scope

### Work-item 1 — Loadout tab render verification (PRIMARY)

Verify `/loadout` page renders:
- All 12 skills per kit (not 1 placeholder)
- Skills present as **rank-0 uninvested** per doc 49 § 1.1.1 Rank-0 amendment (e.g., skill cards greyed/dimmed with "Rank 0 — Uninvested" callout; rank pip = 0 of N)
- Gear catalog renders 11 slots per kit with rarity + modifiers + substrate_binding
- Stat distribution renders per doc 47 § 4 — primary attribute callout + scaling ratios (if star-lord chose Option A) OR live-calc placeholder (if Option B)
- No console errors on load
- Build still clean (1035 modules; zero TypeScript errors)
- 81/81 tests PASS (no regression)

### Work-item 2 — Sample tab scope boundary enforcement (CRITICAL)

**Sample tab stays placeholder for Cycle 14 v1** per gandalf surface confirmation + doc 49 § 1.2.

Sample tab requires AS-gauntlet-passed investment commit which is Cycle 15+ scope. Even though star-lord emits 12 real skills, Sample tab must NOT render them as if they were investment-committed. Sample tab continues to show "Cycle 15+ refresh pending" or equivalent placeholder state.

**Implementation discretion (drax decides):** Either:
(a) Sample tab reads the new 12-skill data but renders them in a "preview-only" mode with a banner ("Sample preview — investment commits land Cycle 15+")
(b) Sample tab continues current placeholder state (no change from drax cascade-r4 cleanup); only Loadout tab consumes the new data

Drax decides per Sample tab UX vision. Gandalf available for Pattern A-light consult if drax wants alignment check.

### Work-item 3 — Banner text update

Amber placeholder banner currently reads (per cascade-r4 cleanup commit `d97462f`):
> "Skills are substrate-derived placeholders — Kit identities, faction clusters, and balance metadata (win rates, quality vectors, cohort) are real engine output."

With star-lord companion dispatch landed (`placeholder_skill_content: false`), banner text must update OR banner removes entirely from Loadout tab. Drax decides:
(a) Banner removes for Loadout tab (skills now real)
(b) Banner stays with updated text reflecting "rank-0 uninvested — investment commits land Cycle 15+"

**Sample tab banner:** if Work-item 2 (a) chosen, Sample tab banner stays with "preview-only" text. If Work-item 2 (b), banner stays with original text on Sample tab only.

### Work-item 4 — Analytics + Encounters tabs no-op verification

Analytics tab is unaffected (consumes balance_metadata which §v1.67 already populated). Verify no regression.

Encounters tab is unaffected (gamora Cycle 15+ scope). Verify Cycle14EncountersNote substrate placeholder still renders.

### Work-item 5 — Vercel production deploy

Trigger Vercel deploy. Verify Production Ready status. Aliased to `https://reincarnated-loadout.vercel.app`. Spot-check 1 Cycle 14 season URL in browser to confirm render.

---

## Cross-seam impact

- Engine seam (star-lord): consumed via companion dispatch — no further engine work
- Demo seam: no impact (this is loadout-only)

---

## Smoke-test expectation (Discipline #2)

Before full verification:
1. `npm run build` — verify clean (zero TypeScript errors)
2. Local dev server: load Cycle 14 season-001 → /loadout → verify 1 kit's skill list shows 12 entries
3. Spot-check 1 kit's gear catalog shows 11 populated slots
4. If smoke PASS, proceed to Vercel deploy + remaining verification

---

## Acceptance criteria

- [ ] /loadout: 12 skills per kit render as rank-0 uninvested (doc 49 § 1.1.1)
- [ ] /loadout: 11 gear slots populated with rarity + modifiers + substrate_binding
- [ ] /loadout: stat distribution renders per chosen star-lord option (no 100/10/10/10 fabrication on player surface)
- [ ] /sample: scope boundary held (Cycle 15+ scope respected; no investment-committed render)
- [ ] Banner text updated OR removed per Work-item 3 decision
- [ ] /analytics: no regression
- [ ] /encounters: no regression
- [ ] Build clean (1035-ish modules; zero TypeScript errors)
- [ ] 81/81 tests PASS
- [ ] Vercel Production Ready
- [ ] Tag: `drax/v1.X-cycle-14-v1-wave-close-render-verification-1`

---

## Out of scope

- AS-gauntlet-passed investment commit Sample tab full surface (Cycle 15+)
- Encounters tab encounter sim (gamora Cycle 15+ scope)
- New gear pool UI (gear data lands via emit; render uses existing gear UI)
- Skill investment UI controls (Cycle 15+ — rank-0 is read-only render)

---

## Pattern A-light verdict request (post-completion, optional)

Drax may request gandalf Pattern A-light verdict on Loadout rank-0 uninvested rendering pattern (doc 49 § 1.1.1 operationalization quality check). Not blocking close.

---

## Completion record (to be appended on close)

**Status:** PENDING (gated on star-lord companion dispatch)
**Authored:** 2026-05-30 by knight-rider
