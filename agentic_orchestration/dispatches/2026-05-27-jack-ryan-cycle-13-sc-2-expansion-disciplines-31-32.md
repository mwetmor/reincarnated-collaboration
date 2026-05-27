# Dispatch — 2026-05-27 — jack-ryan — Cycle 13 SC-2 Expansion (Disciplines #31 + #32)

**From:** knight-rider
**To:** jack-ryan
**Approved by:** Matt 2026-05-27 — Cycle 13 handoff doc § 4.1.5 (SC-2 discipline candidates expansion) + framing brief § 4.1 KR autonomous (sidecar dispatching) + Matt verbatim "Resume Wave 0 → Wave 1 dispatch sequencing"
**Estimated effort:** 1-2 hrs canonical authoring (2 new disciplines + cross-updates)
**Acceptance:** 2 new disciplines (#31 + #32) landed in `engineering-disciplines.md` per existing format + wrapper skill cross-update + ground-state row update; tagged commit

## Context

Matt + gandalf Pattern-B session 2026-05-27 surfaced 2 NEW engineering-discipline candidates beyond the 5 ratified via prior SC-2 (which became #26-#30). Per closeout § 7 + handoff § 4.1.5:

- **#31 Dual-effect separability discipline** (D76 amendment) — Category A (character-wide) and Category B/C (chain-specific) effects must be INDEPENDENTLY COHERENT; removing one should leave the other as a genuine standalone mechanic. Failure mode: T4s where chain effect is just "consequences of character-wide effect spelled out in chain terms." [Founding instance: corrected Blood Magic example 2026-05-27 — original framing had chain effect that was just spelled-out consequence of character-wide effect; corrected to genuinely independent mechanics]

- **#32 First-do-no-harm discipline for algorithmically-generated T4 keystones** — Synergy detection must include downstream-tension-creation check (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve). Net synergy score balances both passes. Failure mode: T4s that solve a stated problem by introducing an equally-bad new problem.

This is async / non-blocking — does not gate any Cycle 13 wave fire, but ratification is needed before these disciplines can be cited downstream (notably Wave 2 T4 algorithm implementation per closeout § 2.5).

## Required reading before starting

1. `canonical/00-ground-state.md` (current epoch + canon-status table)
2. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (current 30 disciplines authoritative source; adopt format / numbering / when-to-cite trigger / R-prescriptions pattern; verify #31 + #32 numbers unoccupied)
3. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 7 (founding-instance source for both candidates)
4. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 2.4-2.5 (substantive context — T4 algorithm 3-category taxonomy + compositional synergy scan)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 D76 (parent decision for #31 amendment)
6. `agentic_orchestration/operating-procedures/jack-ryan.md` (DESIGN-MODE for canonical-write decisions)
7. `agentic_orchestration/operating-procedures/engineering-disciplines.md` (cross-cutting wrapper skill; needs cross-update post-authoring)

## Math-before-code (canonical-authoring; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Disciplines referenced by other agents at execution time; no schema / fixture / boundary mutation.

## Scope

### SC-2 expansion — Disciplines #31 + #32

- [ ] **#31 Dual-effect separability discipline** (D76 amendment) — author canonical entry per existing format:
  - Summary statement (load-bearing)
  - When-to-cite trigger (Wave 2 T4 algorithm implementation; T4 design-spec authoring; jack-ryan Gate-1 on any T4 architecture proposal)
  - Failure mode example (Blood Magic original framing — chain effect was spelled-out consequence; not independently coherent)
  - Corrected example (per closeout § 2.5 + § 7 — Blood Magic re-architected with genuinely independent character-wide vs chain-specific effects)
  - Composes with: #27 dual-effect capstone discipline (parent); #29 commitment-to-consequence (separability commits)
  - Source-of-record: D76 amendment from closeout § 7 + § 2.4 T4 algorithm 3-category taxonomy

- [ ] **#32 First-do-no-harm discipline for algorithmically-generated T4 keystones** — author canonical entry per existing format:
  - Summary statement: synergy detection must check downstream-tension-creation (Pass 2 preserve), not just upstream-tension-resolution (Pass 1 resolve); net synergy score = resolve-score − create-score
  - When-to-cite trigger (Wave 2 T4 algorithm compositional synergy scan implementation; legendary added-skill generation at consumption time; any algorithmic synergy detection)
  - Failure mode example (T4 that solves HP-cost-without-regen via life-steal-from-bleed → bleed-immune bosses leave mechanism with no fuel → solved one problem by creating equally-bad new problem)
  - Composes with: #18 methodology-before-execution (algorithmic synergy detection is a math hotspot); #29 commitment-to-consequence (Pass 2 commits to consequence of synergy)
  - Source-of-record: closeout § 2.5 compositional synergy scan + § 7 candidate #7

- [ ] **Discipline numbering protocol** — assign #31 + #32 per source-of-truth verification; if numbering collision with concurrent jack-ryan work, adjust + flag in completion record

### Cross-updates

- [ ] `agentic_orchestration/operating-procedures/engineering-disciplines.md` wrapper skill — update IS-statement from 30 to 32 disciplines; add new rows for #31 + #32 with one-line summary + when-to-cite trigger
- [ ] `canonical/00-ground-state.md` § 1 row for engineering-disciplines.md — update count from 30 to 32; add #31 + #32 names; reference SC-2 expansion + Cycle 13 source
- [ ] Tag intent: `jack-ryan: engineering-disciplines amendment — Cycle 13 SC-2 expansion (#31 + #32 from 2026-05-27 Pattern-B session)`

## Acceptance criteria

- [ ] Both disciplines authored in `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` per existing format
- [ ] Each carries its source citation + when-to-cite trigger + failure-mode example + composition references
- [ ] Wrapper skill updated 30 → 32
- [ ] Ground-state row updated 30 → 32
- [ ] Tagged commit per jack-ryan convention
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Authoring NEW disciplines beyond #31 + #32 (any additional candidates surfaced during read should be FLAGGED, not authored)
- Modifying existing disciplines #1-#30 (only #31 + #32 additions; D76 amendment composes via #31 reference, not D76 rewrite)
- decisions-log entries (separate jack-ryan work; if surfaced, capture as flag only)
- Production code modifications

## Open questions for the agent to resolve

- Numbering — confirm #31 + #32 are next available; adjust if concurrent jack-ryan work consumed
- Format depth — #31 is a sub-discipline / amendment of #27 (dual-effect capstone); decide whether to author as #31 standalone OR #27.1 sub-discipline (#27.1 may be cleaner; your seam-owner call)
- #32 R-prescription association — if any (composes with #18 methodology-before-execution at math hotspot; algorithmic synergy detection is a math hotspot)

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 7 (candidate source) + § 2.4-2.5 (substantive context)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 D76 (parent decision)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (current state — 30 disciplines)
- `agentic_orchestration/operating-procedures/jack-ryan.md` (DESIGN-MODE canonical-write authority)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-handoff-to-knight-rider.md` § 4.1.5 (this dispatch's authority basis)

---

**Cycle:** 13
**Wave:** 0 / Sidecar (async / non-blocking)
**Gates:** none directly; ratification unblocks downstream citation of #31 + #32 in Wave 2 T4 algorithm implementation
**Priority:** P2 — fire parallel with Wave 1 + SC-4 expansion + SC-6 audit

---

## Completion record — 2026-05-27

**Completed by:** jack-ryan
**Status:** DONE — both disciplines landed; cross-updates applied

### Disciplines landed

- **#31 (standalone, not #27.1)** — Dual-effect separability discipline; D76 amendment composing with #27 as quality criterion. Numbering rationale: #27 tests presence (dual-effect exists); #31 tests coherence (each layer survives removal of the other). Orthogonal checks; standalone is cleaner. Founding instance: corrected Blood Magic Blood Magic example with two-gate separability test table.
- **#32** — First-do-no-harm discipline for algorithmically-generated T4 keystones; two-pass synergy scan (Pass 1 resolve + Pass 2 preserve); net = resolve − create. Founding instance: life-steal-from-bleed against bleed-immune bosses case.

### Cross-updates applied

| File | Change |
|---|---|
| `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` | Scope note updated (30 → 32); #31 + #32 entries inserted before R-prescriptions; Anatomy section updated |
| `agentic_orchestration/operating-procedures/engineering-disciplines.md` | IS statement updated (30 → 32); table header updated; #31 + #32 rows added |
| `canonical/00-ground-state.md` § 1 engineering-disciplines row | Updated count 30 → 32; #31 + #32 names and sources added; 2026-05-27 SC-2 expansion noted |
| `.claude/skills/reincarnated-engineering-disciplines/SKILL.md` | NOT updated — write permission denied for `.claude/skills/`; that file is a packaging artifact under Stream 3 (gandalf) authority; operating-procedures version is authoritative; flag to gandalf for next skill-sync pass |

### Commit

See tagged commit: `jack-ryan: engineering-disciplines amendment — Cycle 13 SC-2 expansion (#31 + #32 from 2026-05-27 Pattern-B session)`
