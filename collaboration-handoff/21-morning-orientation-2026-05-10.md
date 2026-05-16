# Morning Orientation — Resume 2026-05-10

This file is intended to be the first thing read when resuming the collaboration-side Claude session. It's a pointer index, not a re-explanation. Read this; then go to the specific docs and memory only as needed.

## Context in 30 seconds

- **Project:** Reincarnated engine. Procedurally-generated body-swap ARPG; side project with shipping ambitions; collaborator is the user's 11-year-old son (gameplay/art).
- **Working directory for this session:** `/Users/admin/Games/reincarnated-collaboration/`. The engine code lives separately at `/Users/admin/Games/reincarnated-engine/`; this session does NOT write engine code — it works on architecture, design, and CLI prompt drafting.
- **Mode:** architectural advisor to the engine-side CLI. The CLI implements; this session reasons about decisions, surfaces architectural concerns, drafts prompts and revisions.

## Current state (as of end of 2026-05-09)

- **Dimensional refactor (Phases 1–3) merged.** Phase 4 + 5 deferred to medium-term, post-UI/VFX.
- **Priority 02 (gear) in progress** on engine-repo branch `work/priority-02-gear`. CP1 ✓, CP2 ✓, CP2b ✓. Currently between CP2b and CP3. 669 tests passing. 13-CP plan total.
- **Primary design doc:** `canonical/17-gear-and-spirit-guide-design.md`. Updated extensively 2026-05-08/09 — including option C (stat-threshold equip gating), affix coherence dual-layer, off-hand mechanics, handedness, block mechanic, greatsword + wand, color integration.

## Decisions locked — do NOT reopen unless the user explicitly raises them

These were arrived at through extended discussion. Treat them as settled:

| Decision | Summary |
|---|---|
| **Option C (gear gating)** | Stat thresholds gate equipment (concrete, intelligible: "Requires STR 100"). `class_fit_profile` drives Spirit Guide marginal-value math + affix coherence. Two layers, each playing to its strength. |
| **Block fires before crit** | Resolver: hit → block → (if blocked: reduce by block_value, skip crit) → (else: crit → armor → apply). Tank with shield is durable against crit-heavy attackers. |
| **Single absolute marginal-value threshold** | Not dynamic per class state. Refined from earlier "dynamic" framing because dynamic was reverse-engineerable as patronizing-adaptive-difficulty. Initial value ~0.05–0.10 power_score units. |
| **Convergence calibrates against average gear** | Not max gear. Players "break the meta" structurally by accumulating above-average drops. Load-bearing for the player-experience design. |
| **Trait infrastructure shared with Priority 14** | Gear builds it (Priority 02 scope expansion); Priority 14 inherits. |
| **AGI stat is dead/reserved** | Confirmed in `migrations.py:110` ("reserved; current model has no agility"). No code change planned. One-line note in CP plan. |
| **AffixSpec vs EffectPoolEntry** | Open question for CP5c — extend existing pool with tags vs. parallel schema. CLI to investigate before duplicating. |

## Active CLI workstream

- **Just landed (CP2b):** wand + greatsword in weapon roster; 6 off-hand types; handedness on BaseItemType + GearInstance; block_chance/block_value on GearStats; Loadout → 4 slots with conditional off-hand; fit profile overrides for 8 new base types; migration 1.6 has handedness column.
- **Up next (CP3):** dead-field audit; gear stat wiring into combat sim; block resolver branch (locked: before crit).
- **CP3 prompt is paste-ready** in `20-cli-priority-02-cp3-prompt.md` § "CP3 instruction (paste into CLI when resuming)".

## Files to skim (priority order)

If the user's first message is a CP3 result, read these in order:

1. `collaboration-handoff/20-cli-priority-02-cp3-prompt.md` — yesterday's notes + CP3 prompt + carried-over decisions
2. `canonical/17-gear-and-spirit-guide-design.md` — gear architecture reference (skim "Equip-time stat thresholds", "Affix coherence", "Handedness and off-hand mechanics", "Block mechanic" if memory of these is fuzzy)
3. `canonical/16-project-roadmap.md` — phase/priority positioning if needed

If the user's first message is something new (a different design concern, off-topic question, etc.):

- The auto-loaded memory should give enough background. Don't over-read; respond to the actual ask.

## Auto-memory state (for awareness; auto-loads — don't manually read)

The MEMORY.md index includes:
- `project_reincarnated_engine.md` — current state, architectural direction (updated end-of-day 2026-05-09 to reflect CP2b)
- `project_gear_and_spirit_guide.md` — gear design summary
- `project_engine_state_findings.md` — empirical findings, accumulating concerns
- `project_role_orientation_taxonomy.md`, `project_geometry_palette.md`, `project_progression_concept.md` — phase/priority specifics
- `user_role.md` — user context (engine owner, side project, son collaborator)

If memory and current files conflict, trust the files (memory may be stale by a day).

## Probable user requests

In rough order of likelihood:

1. **CP3 result review.** User pastes a CP3 report from the CLI; respond like CP1/CP2/CP2b reviews — acknowledge what's good, surface architectural surprises, lock open design questions, draft the CP4 follow-up.
2. **CP3 prompt refinement.** User wants to adjust the prompt before pasting it. The prompt is in `20-cli-priority-02-cp3-prompt.md` § "CP3 instruction" — modify there.
3. **New design concern.** User surfaces something new (genre intuition, balance worry, UI consideration). Engage; if it touches gear architecture, fold into file 17 with the standard pattern (discuss → decide → edit doc → batch into next CLI revision).
4. **Status check / "where are we."** Use this orientation file plus file 16's roadmap to summarize concisely.

## Working agreement reminder

Per `00-working-agreement.md`: this session is for discussion and design artifacts only — no code in the working repos. The engine-repo CLI handles code. If something architectural emerges that needs implementation, route into a CLI prompt revision rather than implementing here.

## Mode-specific tone

The user has been collaborating closely on architectural decisions over the past two days. They expect:
- Substantive responses with structured trade-offs (tables, ordered lists), not just bullet-point summaries
- Honest pushback when an idea has flaws (e.g., the equalization "patronizing" critique was load-bearing)
- Concision in low-stakes responses; detail in architectural ones
- Recommendations with reasoning, not just options
- No emojis in code; use them sparingly in conversation only when they aid clarity
