# 2026-05-17 — gamora — Standard-demo fresh 5-season regen (post-D3, pre-D10)

**Authority:** Matt L3 standing disposition (Path C sequencing per knight-rider auto-dispatch authority 2026-05-17).
**Type:** Pattern B (long task) — ~1-2 days (5 full-season regens; not perception-test-specific generation).
**Seam:** generation + simulation (gamora-owned; engine-side regen using current generation rules).
**Predecessor:** gamora D3 ship (`gamora/v1.4-d3-path-a-impl-1 @ 048611a`) + rocket earth.yaml fix + jack-ryan post-D3 APPROVE.
**Trigger:** Drax-demo Item 5 audit confirmed all 5 public seasons in `reincarnated-demo/public/seasons/` were generated 2026-05-09/10 (~8 days pre-D3); zero post-D3 archetype tags present. Matt needs eyes on canonical-7 substrates for focused playtest.

---

## Why this regen matters

Matt is preparing to play the build with the v0.25 polish landed. The current 5-season set predates the canonical-7 substrate expansion (D3 ship) by ~8 days. Playing on these seasons would surface zero new substrate content — Matt would only see fire/water/earth/wind canonical-four classes + preserved hybrid_mage + physicals.

The fresh regen produces 5 standard-demo seasons from the **post-D3 engine**. They will include:
- 21 substrate-role compositions (7 substrates × 3 roles)
- 18 distinct archetype tags (after burst/area alias collapse)
- 11 new archetype tags introduced by D3: `earth_burst`, `wind_burst`, `lightning_mage`, `lightning_caster`, `lightning_controller`, `holy_mage`, `holy_caster`, `holy_controller`, `shadow_mage`, `shadow_caster`, `shadow_controller`
- Preserved: `hybrid_mage` + 5 physical archetypes (`rogue`, etc.) per D3 design

This is the **pre-D10 interim regen** — it uses current generation rules (no D10 substrate-coherent enforcement yet). It serves as a qualitative signal for Matt + cheap eyes-on for the new substrates. A second regen will follow after D10 code phase lands to produce ship-target-quality content for the formal perception test.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — drax-demo Item 5 OBSERVATION (most recent; documents the path forward) + jack-ryan APPROVE STATE
2. `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` — § 1.3 and § 1.10 (D3 and D10 context)
3. `reincarnated-demo/public/seasons/` — current 5 season JSONs (the artifacts you're regenerating; inspect file naming + structure)
4. `reincarnated-demo/src/data/loader.ts` — `SEASON_IDS` constant (drax-demo will update this after your regen lands; inspect to understand what season-ID format the demo expects)
5. `reincarnated-engine/src/reincarnated/generation/archetype_composer.py` — your D3 ship; verify boot-time composition produces all 25 templates (incl. 11 new tags)
6. `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §v3.0 — your D3 cross-seam contract

---

## Scope

### Item 1 — Regen 5 standard-demo full seasons from post-D3 engine

Use whatever season-generation pipeline you normally run for full-season regens. The 5 seasons should be substantively different (not identical seeds) so Matt sees variety in his playtest.

**Actions:**
- Identify the season-generation entry-point (likely `season_orchestrator.py` or equivalent; you know your seam)
- Generate 5 standard-demo full seasons with the post-D3 engine
- Confirm each season's content includes:
  - At least one of `lightning_mage` / `lightning_caster` / `lightning_controller` archetype (lightning substrate must appear)
  - At least one of `holy_mage` / `holy_caster` / `holy_controller` archetype (holy substrate must appear)
  - At least one of `shadow_mage` / `shadow_caster` / `shadow_controller` archetype (shadow substrate must appear)
  - If random seed produces a season with zero of any substrate, re-roll or surface as OBSERVATION (substrate selection bias risk per project_b14_5_sidecar_analyses.md — fire over-representation noted historically)
- Author season metadata to include:
  - `engine_version` (e.g., `1.4-d3-path-a`) or
  - `engine_git_sha` (the SHA at regen time, e.g., the post-D3 SHA + any rocket micro-task SHA folded in)
  - `generated_at` (ISO 8601 timestamp)
  - This closes the Discipline #11 attribution gap drax-demo Item 5 audit surfaced
- Write the regen outputs to a staging path (not directly overwriting `reincarnated-demo/public/seasons/` — drax-demo handles the copy + pointer update as the follow-up micro-task)
  - Suggested staging path: `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_*.json` or your seam's conventional output directory
  - Document the staging path in your HANDOFF entry for drax-demo

### Item 2 — Verify regen content + author OBSERVATION

**Actions:**
- For each of the 5 regenerated seasons, run a quick sanity check:
  - Class roster includes substrates from canonical-7 (at minimum, all 7 substrates should be represented across the 5 seasons collectively; not necessarily each substrate in each season)
  - No obvious generation failures (empty kits, malformed JSON, broken schema)
  - Forbidden-mechanics rule is honored (e.g., no fire class with `water` ailment_signature applied; no water class with hybrid_with: fire)
  - WP-9 smoke modifier values are in expected range (no regression beyond what rocket earth.yaml fix restored)
- Author an OBSERVATION entry in the hive log summarizing:
  - 5-season substrate distribution (counts per substrate across 5 seasons)
  - Any anomalies that would distort Matt's qualitative playtest
  - File path of the staging output (so drax-demo knows where to find the JSONs)

### Item 3 — Hive log STATE + HANDOFF to drax-demo

**Actions:**
- Append STATE entry documenting the regen ship: tag name, staging path, 5-season substrate distribution, any anomalies
- Append HANDOFF → drax-demo block with:
  - Staging path to the 5 new season JSONs
  - File-name format the regen produced (so drax's SEASON_IDS update knows what to point at)
  - Any season-format schema changes if applicable (most likely no schema change; same format as pre-D3 seasons)

---

## Out of scope (DO NOT)

- ❌ DO NOT begin D10 code phase yet — that's the next gamora dispatch (separately staged). This regen is the pre-D10 interim only.
- ❌ DO NOT copy the regenerated JSONs into `reincarnated-demo/public/seasons/` directly (drax-demo handles that as a follow-up micro-task; you stage, they wire)
- ❌ DO NOT modify `reincarnated-demo/src/data/loader.ts:SEASON_IDS` (drax-demo seam)
- ❌ DO NOT generate the 12-class perception-test season here — that's a separate dispatch (task #32) targeting `d27-archetype-specs.md` kit-shape-vector constraints. This regen is 5 STANDARD-demo full seasons, not the perception-test season.
- ❌ DO NOT amend D3 implementation in this dispatch — D3 is APPROVED + locked; if you find issues during regen, surface as QUESTION → jack-ryan in hive log
- ❌ DO NOT extend scope to D10 generation-rule prototyping during this dispatch — keep it tight to "regen with current rules"

---

## Acceptance criteria

- [ ] 5 standard-demo full seasons regenerated from post-D3 engine
- [ ] Each season's metadata includes `engine_version` or `engine_git_sha` + `generated_at` (closes Discipline #11 attribution gap)
- [ ] Substrate distribution across 5 seasons collectively includes lightning + holy + shadow (canonical-7 fully exercised at the demo-content surface)
- [ ] No generation failures, malformed JSON, or schema breaks
- [ ] Forbidden-mechanics rule honored across 5 seasons (no contradictions of substrate identity declarations)
- [ ] Staging path documented in HANDOFF to drax-demo
- [ ] Tag `gamora/v1.4-standard-demo-regen-post-d3-pre-d10-1` at the regen-output commit
- [ ] Hive-log STATE + OBSERVATION + HANDOFF entries appended

---

## Smoke test expectation

- Regen completes without exceptions
- 5 season JSON files exist at staging path; each parses cleanly
- Per-season class roster contains at least one canonical-7 substrate (collectively all 7 represented across 5 seasons)
- Schema-validation rules continue to pass (whatever your existing season-validate pipeline produces)

---

## Math-before-code requirements

N/A — this is a regen using existing post-D3 generation pipeline; no new math contracts.

---

## Tag intent

`gamora/v1.4-standard-demo-regen-post-d3-pre-d10-1` — seam-prefixed intermediate tag. Single commit per ADR-006.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 race-condition discipline gandalf authored). `git fetch origin` first; conflict-check; pull-rebase if concurrent commits.

---

*Dispatched 2026-05-17 by knight-rider per Matt standing L3 authority + Path C sequencing decision. Estimated 1-2 days. Append completion record when done.*
