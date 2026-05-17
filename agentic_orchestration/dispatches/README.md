# Dispatches — no-paste handoff pattern

**Purpose:** Minimize Matt's prompt-pasting friction when launching specialist sessions for multi-day work.

## How it works

1. **knight-rider** (after Matt's approval) authors a dispatch brief as a file here:
   `<YYYY-MM-DD>-<agent-name>-<task-slug>.md`

   Example: `2026-05-14-gamora-b10-2-pack-proxy.md`

2. **Matt** opens a terminal:
   ```bash
   cd ~/Games/reincarnated-engine        # or reincarnated-loadout for drax
   claude --agent gamora                 # or rocket, star-lord, drax
   ```
   That's it. One command. No paste.

3. **The agent** reads `agentic_orchestration/dispatches/` at session start, finds the latest undated-as-complete dispatch matching its name, and begins execution.

4. **Completion** — when the agent finishes, it appends a completion record to the dispatch file:
   ```markdown

   ---

   ## Completion record
   **Completed:** 2026-05-14 14:30
   **Tags shipped:** gamora/v1.3-b10-2-pack-proxy
   **Smoke results:** <path or inline>
   **MIGRATION.md written:** yes — affects star-lord telemetry
   **Notes for jack-ryan review:** <bullets>
   ```

## Dispatch brief format

```markdown
# Dispatch — <date> — <agent> — <task>

**From:** knight-rider
**To:** <agent name>
**Approved by:** Matt at <time>
**Estimated effort:** <hours / days>
**Acceptance:** <how to know when done>

## Context (1-2 paragraphs)
<why this work matters, what triggered it>

## Required reading before starting
- <files / docs to read first>

## Math-before-code (if applicable)
<specific math/decisions to document before implementation>

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

Does this dispatch add, modify, rename, or remove any field on:
- A telemetry schema table (class_fight_loadouts, class_balance_results, etc.)
- A fight_log dict key (gamora → star-lord boundary)
- A loadout dict key (rocket/gamora → star-lord/drax boundary)
- An export packet structure (season JSON shape; season_writer.py output)
- Any other inter-seam fixture dict

**If YES:** the Acceptance criteria below MUST include one of:
  - `Round-trip smoke: <description of production-path fixture used + consumer boundary exercised + field-presence check>`
  - `Round-trip: not applicable because <explicit reason>`

**If NO:** state `Round-trip: not applicable — no cross-seam contract change in this dispatch.`

Silence on this field is a Gate-1 BLOCK per REVIEW_PROCESS.md Principle 6.

## Scope
- [ ] <concrete deliverable 1>
- [ ] <concrete deliverable 2>
- [ ] Smoke-test passes
- [ ] MIGRATION.md if cross-seam impact
- [ ] Round-trip smoke (or not-applicable justification) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: <expected tag name>

## Acceptance criteria
<!-- List each acceptance item explicitly. Cross-seam dispatches must include the round-trip clause here. -->
- [ ] <criterion 1>
- [ ] Round-trip smoke: <fixture + boundary + check> OR Round-trip: not applicable because <reason>

## Out of scope (explicit non-goals)
- <thing 1 to not do>
- <thing 2 to not do>

## Open questions for the agent to resolve
- <decisions the agent must make and document>

## References
- <links to relevant decisions-log entries, ADRs, prior tags>
```

## Naming rules

- Filename: `<YYYY-MM-DD>-<agent-name>-<task-slug>.md`
- Agent name lowercase, hyphenated (gamora, rocket, star-lord, drax, jack-ryan)
- Task slug lowercase, hyphenated, ≤4 words

## Cleanup

After 30 days OR after the work has been merged to main, dispatches can be moved to `dispatches/archive/<year>/` to keep the active folder readable. knight-rider handles this periodically.
