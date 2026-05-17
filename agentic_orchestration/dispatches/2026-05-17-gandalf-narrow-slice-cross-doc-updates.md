# 2026-05-17 — gandalf — Narrow-slice cross-doc updates (canonical-32 § 12.5 + substrate-identity-declarations § 9 + decisions-log draft)

**Authority:** Self-authored extension of your L3 briefing (per § 5.1 + § 6.5 of `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md`).
**Type:** Pattern B (long task) — ~1 day (mostly absorbed by briefing per § 5.1).
**Predecessor:** Your L3 briefing (`gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` @ `3ec108f`).

---

## Why this matters

Your briefing § 7 recommendation (PARTIAL Phase-1 P1 extension; narrow slice) is binding per Matt's standing delegation. Phase A of execution now spawns: rocket schema fields (separate dispatch) + your cross-doc updates (this dispatch). Both land in parallel to enable Phase B (drax narrow-slice work) + Phase C (gamora narrow-slice AI).

The cross-doc updates per briefing § 6.5:

1. `canonical/32-progression-design.md` § 12.5 amendment — items #2/#3/#4/#6 reflect narrow-slice locks; #1/#5 stay open for B13-proper
2. `canonical/16-project-roadmap.md` — B13 scope-reduction note (narrow slice ~25% of B13; ~2.5-3 weeks remaining at Stage A2 closeout)
3. `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9 — amendment-note acknowledging narrow-slice spatial-combat substrate underwrites the declarations
4. Decisions-log entry (you draft; jack-ryan reviews; knight-rider sequences final accept)

---

## Required reading (in order)

1. Your L3 briefing — `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 5.1 + § 6.5 + § 7 (all your own; refresh)
2. `canonical/32-progression-design.md` § 12.5 — current state; identify items #2/#3/#4/#6 for amendment
3. `canonical/16-project-roadmap.md` — B-series state; B13 entry in particular
4. `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9 — current amendment-history section
5. `reincarnated-engine/design/decisions/decisions-log.md` — latest format + recent entry conventions

---

## Scope

### Item 1 — canonical-32 § 12.5 amendment

Amend canonical 32 § 12.5 to reflect narrow-slice locks per briefing § 6.5:

- **Item #2 (i-frame durations)** — lock per narrow-slice spec (0.3-0.4s with substrate variation; gandalf-recommended numerical asymmetry per § 2.2 of briefing)
- **Item #3 (player-cast telegraphs)** — lock per § 3.6 recommendation (NO player-AOE telegraph in solo; player kit-self-discipline is via cooldown not visual telegraph)
- **Item #4 (indicator hitbox)** — lock per § 3.3 (geometry-painter reuse; indicator covers exactly the AOE hit-region)
- **Item #6 (cadence)** — lock per § 3.2 per-substrate windup table; cite the rocket schema fields landing

- **Items #1 (5-geometry roster) + #5 (mobility role-tagging)** — keep open / defer to B13-proper; explicitly note "STAY OPEN; B13-proper at Stage A2 closeout"

### Item 2 — canonical-16 B13 scope-reduction note

Add a note to `canonical/16-project-roadmap.md` B13 section explaining:
- B13 reduced ~25% by narrow-slice Phase-1 P1 extension landing
- Remaining B13 scope: ~2.5-3 weeks at Stage A2 closeout (down from ~3-4 weeks)
- Cross-reference your briefing as the source of the scope-reduction

### Item 3 — substrate-identity-declarations § 9 amendment

Add an amendment-note to `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9 documenting:
- Narrow-slice spatial-combat substrate underwrites the declarations
- The Layer-1 identity declarations are conditional on a Layer-0 spatial-combat substrate (per § 1 of your briefing)
- Cross-reference your briefing tag (`gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1`)

### Item 4 — Decisions-log draft entry

Author a draft decisions-log entry capturing the L3 decision:
- Title (suggested): "L3 — Narrow-slice telegraphed-combat extension for Phase-1 P1 (2026-05-17)"
- Decision: PARTIAL Phase-1 P1 extension per briefing § 7
- Rationale: brief (3-5 bullets) summarizing the cosmological + pragmatic case
- Cross-reference: briefing tag + briefing path + rocket schema dispatch + gamora narrow-slice (queued) + drax narrow-slice (queued)
- **Note:** Per protocol § 5.3 (decisions-log is jack-ryan-owned), this is a DRAFT for jack-ryan to review + accept. Don't directly commit to the decisions-log; knight-rider routes draft → jack-ryan → final.

### Item 5 — Hive-log STATE + HANDOFF entries

- STATE entry: cross-doc updates shipped; specifies amendment summary per doc
- HANDOFF → jack-ryan: decisions-log draft ready for review
- HANDOFF → rocket: schema field consumer obligations now formally documented (rocket sees this when consuming your amendment)

---

## Out of scope (DO NOT)

- ❌ DO NOT write engine code, simulation code, or demo code
- ❌ DO NOT amend D8 / D9 trait pools (briefing § 3.4 already noted no amendment needed)
- ❌ DO NOT amend hive-mind protocol or substrate-expansion-decision docs
- ❌ DO NOT commit directly to decisions-log (jack-ryan owns; you draft only)
- ❌ DO NOT respond to your own 7 open questions in briefing § 9 (those are for Matt at leisure; knight-rider surfaces if needed)
- ❌ DO NOT extend scope to other canonical doc updates

---

## Acceptance criteria

- [ ] `canonical/32-progression-design.md` § 12.5 amended per Item 1 above
- [ ] `canonical/16-project-roadmap.md` B13 scope-reduction note added per Item 2
- [ ] `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9 amendment-note added per Item 3
- [ ] Decisions-log DRAFT entry authored (path: per your convention; suggest a `drafts/` subdirectory or as a separate file referenced for jack-ryan review)
- [ ] Hive-log STATE + 2 HANDOFF entries (jack-ryan + rocket)
- [ ] Tag `gandalf/v1.3-narrow-slice-cross-doc-updates-1`

---

## Smoke test expectation

- No engine code changes; no test suite impact
- Doc updates render cleanly + cross-reference resolves
- Decisions-log draft is jack-ryan-reviewable

---

## Math-before-code requirements

N/A — doc updates.

---

## Tag intent

`gandalf/v1.3-narrow-slice-cross-doc-updates-1` — seam-prefixed.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 you authored). `git fetch origin` first.

---

## Continuous-availability ramp

Stay LIVE for Matt L3 follow-up Q&A on briefing § 9 (your 7 open questions) — knight-rider surfaces if needed; you respond at leisure.

---

*Dispatched 2026-05-17 by knight-rider per Phase A parallel-start. Estimated 1 day. Append completion record when done.*

---

## Completion record — 2026-05-17 gandalf

**Status:** COMPLETE.
**Tag intent:** `gandalf/v1.3-narrow-slice-cross-doc-updates-1` (cut at commit landing).

### Acceptance criteria — all met

- [x] `canonical/32-progression-design.md` § 12.5 amended per Item 1 (items #2/#3/#4/#6 locked per narrow-slice; items #1/#5 STAY OPEN for B13-proper; new "Amendment 2026-05-17 — Narrow-slice Phase-1 P1 extension (L3 binding decision)" subsection appended)
- [x] `canonical/16-project-roadmap.md` B13 scope-reduction note added per Item 2 (Stage A2 closeout paragraph + new green-highlighted note; ~25% scope reduction; ~2.5-3 weeks remaining)
- [x] `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.1 amendment-note added per Item 3 (Layer-0 spatial-combat substrate underwriting Layer-1 declarations; per-substrate dependency examples; narrow-slice resolution; Layer-1 unchanged)
- [x] Decisions-log DRAFT entry authored at `reincarnated-engine/design/decisions/drafts/2026-05-17-narrow-slice-telegraphed-combat-extension-DRAFT.md` (jack-ryan owns final accept; knight-rider routes commit)
- [x] Hive-log STATE + 2 HANDOFFs (jack-ryan + rocket) appended per Item 5 (PRE-SIGNAL per § 14.1.1 prefixed)
- [x] Tag intent `gandalf/v1.3-narrow-slice-cross-doc-updates-1` declared

### Out-of-scope honored

- No engine code, simulation code, or demo code touched
- No D8/D9 amendments
- No hive-mind protocol amendments
- No direct decisions-log commits (draft only; jack-ryan owns accept; knight-rider routes)
- No response to briefing § 9 open questions (those are for Matt at leisure)
- No scope extension to other canonical doc updates

### Smoke test expectation

- No engine code changes; no test suite impact ✓
- Doc updates render cleanly + cross-references resolve ✓
- Decisions-log draft is jack-ryan-reviewable ✓

### Continuous-availability ramp

Gandalf stays LIVE for Matt L3 follow-up Q&A on briefing § 9's 7 open questions. Knight-rider surfaces if/when needed.

*Completion recorded 2026-05-17 by gandalf.*
