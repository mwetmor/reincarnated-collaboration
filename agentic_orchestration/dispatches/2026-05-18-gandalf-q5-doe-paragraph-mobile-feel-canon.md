# 2026-05-18 — gandalf — Q5 DoE paragraph addition to mobile-feel-target canonical doc

**Authority:** Matt L3 yes-batch 2026-05-18 Tier 1.5 — Q5 APPROVED.
**Type:** Pattern A — small doc addition; ~20-30 min.
**Status:** 🟢 **ACTIVE — fire immediately. Gandalf idle.**

---

## Why this matters

Tier 1.5 Q5: DoE (Dungeon of Exile) is the locked reference experience for VS2a + VS2b mobile-feel target per Matt L3 (Path A authorization earlier in session). Captured in `canonical/story/mobile-feel-target-doe-2026-05-17.md`. Q5 is a small canonical-doc addition codifying DoE as the genre reference so future agents anchor mobile-UX decisions against a concrete experience-target.

---

## Required reading

1. **DoE mobile-feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (your prior; the canon Matt locked Path A against)
2. **Mobile-vs-PC pixel sizing canon** — `canonical/story/mobile-vs-pc-pixel-sizing-2026-05-XX.md` (gandalf v1.7; 3 locks + parked Q1/Q2/Q4/Q5)
3. **DoE Path A doc cascade** — canonical-17 + canonical-32 portrait amendments (your prior; mobile-plan-amendment-portrait-primary)

---

## Scope — one deliverable

Add a paragraph (or short section) to `canonical/story/mobile-feel-target-doe-2026-05-17.md` (or equivalent canon doc) capturing:

- **DoE as canonical reference experience for Reincarnated mobile**: Dungeon of Exile (mobile-first ARPG) is the validated reference for player-feel + UX patterns. Matt L3 locked Path A 2026-05-17.
- **What DoE establishes for Reincarnated**:
  - Portrait-primary orientation
  - Cooldown-based heal (10s CD; 35% max-HP; 50 HP floor; 0s cast; no invuln)
  - Auto-cast skill rotation with manual target override (Reincarnated Option A locked 2026-05-18)
  - Cooldown-based potions (15s; mirrors DoE pattern)
  - Touch-first input design
  - HUD density appropriate for portrait + finger-touch precision (88-125px touch targets)
- **When to depart from DoE canon**: any deviation requires explicit canonical-doc note + Matt L3 sign-off (e.g., feature-parity differs because of Reincarnated-specific design elements like Spirit Guide + Earth-Self meta-layer + 6-archetype kit shape).
- **Forward-looking**: DoE remains the canon reference through VS2a + VS2b; revisit canonical reference selection if Reincarnated-specific mechanics push the demo away from DoE-pattern fidelity (e.g., if PVP/PVE rift events + Earth meta-layer require fundamentally different UX paradigm)

Cross-references:
- canonical/17-gear-and-spirit-guide-design.md (portrait amendments)
- canonical/32-progression-design.md (portrait amendments)
- mobile-vs-pc-pixel-sizing canon (gandalf v1.7)
- decisions-log.md DoE Path A entry (jack-ryan)

---

## Acceptance criteria

- [ ] Paragraph/section authored in canon doc
- [ ] DoE reference + locked Path A clearly cited
- [ ] Departure rule defined (when to deviate from DoE)
- [ ] Forward-looking trigger condition for canon reselection
- [ ] Cross-references to relevant canonical docs
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `gandalf/v1.12-q5-doe-paragraph-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT amend DoE-related canon docs beyond the paragraph addition
- ❌ DO NOT touch implementation code
- ❌ DO NOT re-litigate DoE reference (Matt L3 locked)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** rocket new-season regen; drax v1.18.5 hotfix; elrond Tier 5.1/5.2 (all different seams)
- **Triggers downstream:** none — terminal doc-canon polish item
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 Tier 1.5 yes-batch. ~20-30 min. Append completion record when done.*

---

## Completion record — 2026-05-18 gandalf

**Status:** ✅ **COMPLETE.**

**Tag:** `gandalf/v1.12-q5-doe-paragraph-1` (local; ADR-006 — no push).

### What landed

`canonical/story/mobile-feel-target-doe-2026-05-17.md` § 12 (new section) — *DoE as canonical reference experience (Matt L3 Path A lock 2026-05-17; codified Q5 2026-05-18).*

Five subsections:

- **§ 12.1** — DoE named as the validated reference experience for Reincarnated mobile (not inspiration, not one influence — the reference). Provenance traced to Matt L3 Path A authorization 2026-05-17 and the doc-cascade that followed.
- **§ 12.2** — Single-glance reference list of what DoE establishes: portrait-primary; cooldown heal (10s / 35% / 50 floor / 0s cast); auto-cast skill rotation with manual target override (Option A locked 2026-05-18); cooldown potions (15s); touch-first input; HUD density 88-125px.
- **§ 12.3** — Departure rule: (1) any deviation requires explicit canon-doc note, (2) Matt L3 sign-off required, (3) default is fidelity. Cautionary tale: Diablo Immortal's pre-launch beta drift toward D3-PC patterns.
- **§ 12.4** — Forward-looking canon-reselection triggers: Earth meta-layer UX paradigm shift, PVP/PVE rift multi-actor demands, Spirit Guide during-combat depth, substrate-readability UX needs, visual-register divergence. Default absent trigger: DoE remains canon.
- **§ 12.5** — Cross-references (canonical-17, canonical-32, mobile-pc-pixel-sizing v1.7, decisions-log 2026-05-17 entry, this dispatch).

### Acceptance criteria

- [x] Paragraph / section authored in canon doc (§ 12, ~5 subsections)
- [x] DoE reference + locked Path A clearly cited (§ 12.1)
- [x] Departure rule defined (§ 12.3 — 3 clauses)
- [x] Forward-looking trigger condition for canon reselection (§ 12.4 — 5 triggers)
- [x] Cross-references to relevant canonical docs (§ 12.5 + back-reference added in § 11)
- [x] PRE-SIGNAL § 14.1.1 — N/A for canon-doc-only edit; no hive-log append performed this session (Pattern A small doc dispatch; terminal item with no downstream triggers per dispatch)
- [x] AGENT_STATE STATE entry — N/A (gandalf has no AGENT_STATE.md in agentic_orchestration/gandalf/; ledger lives in dispatch completion records + git tags per established pattern)
- [x] Tag `gandalf/v1.12-q5-doe-paragraph-1` applied locally (no push per ADR-006)

### Out of scope honored

- ❌ No DoE-related canon docs amended beyond this paragraph (canonical-17, canonical-32, mobile-pc-pixel-sizing, mobile-ux-execution-plan all untouched; § 12 only references them)
- ❌ No implementation code touched
- ❌ No re-litigation of DoE reference (Matt L3 Path A lock stands; this section codifies, does not re-open)
- ❌ No tag push (ADR-006)

### Coordination notes

- Parallel-safe with rocket new-season regen, drax v1.18.5 hotfix, elrond Tier 5.1/5.2 — confirmed; different repos / different seams; this is a canon-doc-only edit in collaboration repo.
- No downstream triggers; terminal doc-canon polish item per dispatch.

### Time

~25 min wall-clock — within dispatch estimate.

*Completion appended 2026-05-18 by gandalf.*
