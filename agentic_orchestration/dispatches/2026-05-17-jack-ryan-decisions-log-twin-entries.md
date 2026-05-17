# 2026-05-17 — jack-ryan — Decisions-log twin entries (register-fence rule + 75% generative failure rate)

**Authority:** Matt L3 lock 2026-05-17 (~19:30 EDT) for both items; gandalf v1.10 follow-up flag for the register-fence rule.
**Type:** Pattern A — ~0.5 day; decisions-log authoring; no code.
**Predecessor:** Gandalf v1.10 advisory + VFX scene-needs spec authoring session.

---

## Why this matters

Two Matt-locked design constants from 2026-05-17 need formal decisions-log capture per ADR-002. Both have authority extending beyond their immediate scope — they're load-bearing for downstream design across multiple seams.

---

## Item 1 — Register-fence-per-UI-surface authoring rule

**Source:** Gandalf v1.10 VFX Sub-decision A advisory (`gandalf/v1.10-vfx-sub-decision-a-consult-1 @ 20e1adc`); lifted into VFX scene-needs spec top-level discipline; gandalf explicitly flagged: *"Register-fence rule deserves its own decisions-log entry per ADR-002 (authority extends beyond VFX-spec scope)."*

**The rule (binding for all VS2a+ content):**
> Within any single UI surface block, exactly one vocabulary register appears. Stats block = canonical-7 only. Flavor-text block = per-season vocabulary only (NEVER the canonical-7 substrate words). Item-label block = season-authored derived label (may echo per-season theme, never mixes canonical-7 substrate words). Skill-name block = canonical-7-derived for VS2a; per-season-derived deferred to Stage 3 (VS2b).

**Why it extends beyond VFX:** the rule applies to all rendered text on a UI surface — combat log, status effects, character sheet, inventory tooltips, gear flavor, NPC dialog UI, quest descriptions. It binds drax's typography work, rocket's LLM-generated content authoring, star-lord's output pipelines, and gandalf's future content commissions.

**Decisions-log entry should capture:**
- The rule itself (verbatim from gandalf v1.10 / VFX spec)
- Affected seams (drax / rocket / star-lord / gandalf authoring)
- Supersession context (replaces any implicit "mixed register OK" historical pattern)
- Genre canon citations (D2/D3/D4/PoE/Last Epoch postmortems — gandalf v1.10 references these)
- Forward consumer obligations (downstream content generation must respect the fence)

### Item 2 — ~75% expected generative-season failure rate (Matt design constant)

**Source:** Matt L3 2026-05-17 ~19:00 EDT: *"We will not plan to ship all generative seasons. Some will be failures (maybe 75% per our overarching game design)."*

**The constant:** ~75% of generative seasons are expected to be unshippable. This is **design-intended**, not a system failure mode. Curation step selects which seasons ship to playtest. Non-humanoid generation that doesn't pass curation is *expected*, not waste.

**Why it's load-bearing:**
- **Curation pipeline scope:** how curation work is sized (must process 4× more seasons than ship)
- **Gamora regen volume:** how many seasons per epoch are budgeted (must generate ~4× ship target)
- **Gandalf gating cadence:** how many seasons gandalf audits per checkpoint
- **Star-lord telemetry capacity:** per-season output growth at 4× ship-target
- **Elrond catalogue:** failure-flag schema field needed for tracking curation verdicts

**Decisions-log entry should capture:**
- The constant value (~75% failure rate; "approximately 3-in-4 seasons unshippable")
- Frame (feature, not bug — quotes Matt verbatim)
- Affected seams (gamora / gandalf / star-lord / elrond)
- Forward obligations: curation verdict telemetry; failure-flag schema; capacity planning

---

## Required reading

1. `agentic_orchestration/dispatches/2026-05-17-gandalf-vfx-sub-decision-a-cognition-and-register-consult.md` — gandalf's v1.10 advisory
2. `canonical/story/vs2a-vfx-scene-needs.md` § "Register-fence authoring rule" — the lifted top-level discipline
3. `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md` § "Micro-decision placeholders (RESOLVED)" — both items in context
4. `reincarnated-engine/design/decisions/decisions-log.md` — your authoring target; format-match recent entries
5. `agentic_orchestration/GOVERNANCE.md` ADR-002 — decisions-log authority

---

## Acceptance criteria

- [ ] Decisions-log entry 1 authored (register-fence rule)
- [ ] Decisions-log entry 2 authored (75% generative-season failure rate)
- [ ] Both entries cite source (gandalf v1.10 / Matt L3 2026-05-17)
- [ ] Both entries enumerate affected seams + forward obligations
- [ ] Format matches recent decisions-log entries
- [ ] Engine-side commit + push
- [ ] Hive-log STATE entry summarizing both
- [ ] Tag `jack-ryan/v1.3-decisions-log-twin-entries-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT amend the VFX scene-needs spec or gandalf v1.10 advisory (consume only)
- ❌ DO NOT propose changes to the register-fence rule (gandalf canon-locked)
- ❌ DO NOT propose changes to the 75% failure-rate constant (Matt-locked)
- ❌ DO NOT extend to other Matt-locked items (e.g., dual-stick mobile input was already hive-log captured; if you find others, surface as OBSERVATION but don't write entries unilaterally)

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append; pull-rebase before engine-side commit
- **Engine-repo state at dispatch time:** main at `81ff9ce` (rocket/v1.11)
- **Collab-repo state at dispatch time:** main at `43396bb` (spec doc shipped)

---

*Dispatched 2026-05-17 by knight-rider per autonomous-mode follow-up (Matt away). ~0.5 day. Append completion record when done.*
