# Dispatch — 2026-05-27 — gandalf — Cycle 14 SC-2 doc 40 amendments

**From:** knight-rider
**To:** gandalf (story-and-design steward)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-2)
**Estimated effort:** ~3-6 hours
**Acceptance:** doc 40 amendments per doc 46 § 13 + doc 47 § 5 landed canonically; affected D-entries marked AMENDED with cross-references to doc 46 / doc 47 sections

## Context

Cycle 14 framing brief RATIFIED 2026-05-27 — Q1-Q11 in full. Sidecar SC-2 fires Wave 0 to land doc 40 amendments before downstream waves consume the architectural foundation. Doc 40 (`canonical/40-gear-balance-guide-architecture-2026-05-26.md`) is the Cycle 13 architectural foundation with D1-D86 entries; doc 46 (concentration architecture; 9 layers) and doc 47 (damage scaling architecture; physical/magical/hybrid routing) amend specific D-entries per their respective § 13 and § 5 amendment lists.

The amendments are inheritance work, not re-architecture — doc 40 entries that were superseded or refined by doc 46/47 architectural commitments need to be marked AMENDED in-place with cross-references so downstream readers (rocket, gamora, jack-ryan, future agents) hit the canonical superseding architecture at first read.

Without this amendment landing in Wave 0, Wave 1 (concentration architecture Layers 1-4+7) and Wave 0.5 (damage scaling routing) fire against a doc 40 that still presents the unamended Cycle-13-era D-entries as canonical — a discipline #1 (math-before-code) violation if rocket consumes unamended D-entries when implementing the new architecture.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — the doc being amended (D1-D86 entries)
- `canonical/46-concentration-architecture-2026-05-27.md` — particularly § 13 amendment list (D9 / D33 / D38 / D51 / D54 / D55 / D56)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — particularly § 5 amendment list
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` — RATIFIED authority basis
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` — Cycle 14 scope-doc
- `.claude/skills/reincarnated-canonical-doc-format` — canonical doc format spec (STATUS protocol + cross-reference protocol)

## Math-before-code (if applicable)

Not applicable — this is canonical doc amendment, not code emission. Math-before-code discipline applies to the consumers of doc 40 amendments (rocket Wave 0.5 + Waves 1-2 implementation), not to the amendment authoring itself.

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add, modify, rename, or remove any field on:
- A telemetry schema table — **NO**
- A fight_log dict key — **NO**
- A loadout dict key — **NO**
- An export packet structure — **NO**
- Any other inter-seam fixture dict — **NO**

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** (This is canonical doc amendment, not code emission. Cross-seam impact lands downstream when rocket + gamora implement against the amended architecture.)

## Scope

- [ ] Inspect doc 46 § 13 amendment list (D9 / D33 / D38 / D51 / D54 / D55 / D56 + any others gandalf surfaces in re-read); inspect doc 47 § 5 amendment list
- [ ] For each affected D-entry in doc 40:
  - [ ] Mark D-entry header as AMENDED with date 2026-05-27 + cross-reference to superseding doc 46 / doc 47 section
  - [ ] Preserve original D-entry content (per canonical/00-ground-state.md historical-preservation pattern) — amendment is additive cross-reference, not deletion
  - [ ] Where amendment substantively changes the D-entry's load-bearing claim (e.g., capability scope reduction in D54-D56), note the supersession explicitly in the entry body
- [ ] Author a top-of-doc-40 amendment-pass-record (anchor § 0.X or similar) summarizing all 2026-05-27 amendments with index of affected D-entries → superseding doc 46 / doc 47 sections
- [ ] Cross-reference back from doc 46 § 13 + doc 47 § 5 to the amended D-entries (bidirectional per canonical doc format § 4 cross-reference protocol)
- [ ] Update `canonical/00-ground-state.md` if doc 40's STATUS line warrants a CURRENT-with-amendment note (gandalf decides per canonical doc format judgment)
- [ ] AGENT_STATE.md not applicable (gandalf is canonical-doc steward; commits to collab repo)
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum since SC-2 is authorized cycle work)

## Acceptance criteria

- [ ] All D-entries listed in doc 46 § 13 + doc 47 § 5 amendment lists marked AMENDED in doc 40 with bidirectional cross-references
- [ ] Top-of-doc-40 amendment-pass-record anchor added summarizing the amendment pass
- [ ] No regression to D-entries not listed in amendment lists (preserve unaffected canonical content)
- [ ] Doc 46 § 13 + doc 47 § 5 cross-reference back to the amended D-entries (bidirectional)
- [ ] STATUS line in doc 40 reflects the 2026-05-27 amendment pass
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Do NOT re-author doc 40 from scratch — this is in-place amendment work, not restructure
- Do NOT amend D-entries not listed in doc 46 § 13 + doc 47 § 5 lists (unless gandalf surfaces a load-bearing inconsistency that warrants separate dispatch authoring)
- Do NOT touch doc 41 / doc 42 / doc 43 / doc 44 / doc 45 (those are Cycle 13 design-intent docs; their amendment cycle is separate and not in Wave 0 scope)
- Do NOT delete or move D-entries to historical/ — amendment preserves originals with supersession markers
- Do NOT touch the gauntlet sim representative loadout discipline (§ 6.5 amendment) — that's Wave 2 work, not SC-2 scope
- Do NOT author discipline-canonical-writes — that's jack-ryan's seam via SC-1

## Open questions for the agent to resolve

- **Q-SC2-1**: Doc 46 § 13 names D9 / D33 / D38 / D51 / D54 / D55 / D56 — is this list exhaustive or are there subordinate D-entries (e.g., D54.1 / D55.1) that warrant amendment companions? Gandalf decides per re-read of doc 46 layers 3 (capability scope reduction) + 5 (concentration probability) + 6 (cohesion layering) — author rationale into the amendment-pass-record anchor.
- **Q-SC2-2**: Doc 47 § 5 amendment list — gandalf inspects doc 47 § 5 in full + identifies the affected doc-40 D-entries (damage-scaling-path implications across D-entries that reference weapon damage scaling, skill damage formulas, sim methodology). Author rationale per amendment.
- **Q-SC2-3**: STATUS line on doc 40 — does this amendment pass demote doc 40 to "CURRENT-with-amendments" or preserve "CURRENT" with the amendment-pass-record anchor as the discriminator? Gandalf decides per canonical doc format judgment + records rationale.

## References

- `canonical/46-concentration-architecture-2026-05-27.md` § 13 (amendment list)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 5 (amendment list)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (the target doc)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 1 L1 (architectural foundation lock) + § 5 SC-2 entry
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-kr-kicker.md` § 4.1 (immediate actions — fire SC-2 to gandalf)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 3 (SC-2 entry) + § 2 Wave 0 outputs
- Canonical doc format skill — STATUS protocol + bidirectional cross-reference protocol
