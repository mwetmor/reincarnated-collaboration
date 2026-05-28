# Dispatch — 2026-05-27 — per-agent OP amendments (Move 2+3+5 delivery; 9 OP files; parallel fan-out)

**From:** knight-rider
**To:** EACH AGENT (jack-ryan / gandalf / gamora / rocket / star-lord / drax / elrond / legolas / galadriel) — applies amendment to OWN OP file
**Approved by:** Matt 2026-05-27 (Matt-gate Path (1) ratification + "Per-agent OP amendments (Move 2+3+5; 10 files) can fire in parallel")
**Estimated effort:** ~5-15 min per agent (mechanical amendment per standardized template; ~1-2 hr total wall-time across parallel fires)
**Acceptance:** each of 9 non-KR agent OP files amended per standardized template (Move 2 Discipline #42 framing-audit + Move 3 Discipline #44 framing-refusal authority + Move 5 orientation phrase preamble); KR OP already amended (Move 1 + Move 5 portion at `8a1ee9a`)

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** propagate the 5-moves discipline-stack across all per-agent operating-procedures so the team operates under coherent quality discipline. Without Move 2+3+5 propagation, agents fire dispatches without framing-audit + refusal-authority + orientation preamble — discipline-stack remains partial. Composes "Engine first. Game second. Phase third." orientation.

**Refutation conditions** (per agent surfaces if any apply):
- Standard amendment template conflicts with existing OP structure (warrant agent judgment on placement, NOT contradiction)
- Discipline #42 framing-audit conflicts with existing per-agent self-discipline (e.g., gandalf already has Pattern A-deep three-question protocol; surface composition note)
- Discipline #44 framing-refusal template doesn't fit agent's actual seam scope (e.g., star-lord refusal pattern differs from gandalf refusal pattern)
- Orientation phrase preamble already implicit via other OP language (cross-reference rather than duplicate)

## Context

**Authority chain:**
- Disciplines #42 + #43 + #44 ratified at engine `e93d9ad` (jack-ryan canonical-write 2026-05-27)
- Move 5 orientation phrase ratified: "Engine first. Game second. Phase third." (canonical at AGENTS.md + KR OP)
- Move 1 KR OP quality-criterion template ratified (KR OP § 3.11)
- Each agent owns their own OP file per AGENTS.md convention (self-authored from observed practice)

**Standardized amendment template (3 sections per OP):**

### Template Section A — Move 2: Discipline #42 framing-audit at sub-agent dispatch consumption

```markdown
## Framing-audit at sub-agent dispatch consumption (Discipline #42)

When invoked as sub-agent via Pattern-A or Pattern-B dispatch, apply framing-audit before executing:

- **Q1 — Load-bearing assumptions:** what does this dispatch assume to be true such that if those assumptions fail, the work doesn't compose? Enumerate.
- **Q2 — Refutation evidence:** what empirical evidence would refute Q1 assumptions? Seek it before executing.
- **Q3 — Outcome trigger:** if Q1 OR Q2 surfaces contradiction with seam-owned authority, invoke Discipline #44 framing-refusal + surface back to KR for re-routing.

Apply framing-audit at:
- Sub-agent dispatch consumption entry
- Math hotspot ratification (Discipline #18 composition)
- Pattern A-deep / verdict authoring (per role-specific OP)
- Cross-seam routing (Discipline #25 semantic-layer rep-audit composition)
```

### Template Section B — Move 3: Discipline #44 framing-refusal authority

```markdown
## Framing-refusal authority (Discipline #44)

Refusal IS NOT failure. When dispatch framing exceeds seam authority OR violates seam discipline, refuse and surface back:

- **Refusal templates** (per seam) at `agentic_orchestration/<agent>/refusals/` (.gitkeep present)
- **4 refusal patterns:**
  - Pattern R-1: Framing assumes seam authority the agent doesn't own (re-route to correct seam owner)
  - Pattern R-2: Framing violates seam discipline (e.g., synthetic-stub-as-permanent-fallback for content seams)
  - Pattern R-3: Framing imposes pre-authored taxonomy under no-classes architecture (Discipline #41 violation)
  - Pattern R-4: Framing requires methodology depth exceeding transcription scope (route to legolas Mode A methodology consultation)
- **Refusal output**: surface back via completion record; KR routes to re-author OR re-route

Refusing protects the work-product; carrying mis-framed work pollutes downstream.
```

### Template Section C — Move 5: Orientation phrase preamble

```markdown
## Orientation phrase (Move 5; team-wide)

> **Engine first. Game second. Phase third.**

Apply this orientation at every dispatch consumption + every design decision:

1. **Engine first** — engine-layer infrastructure integrity is the foundation; cannot be papered over by game-layer or phase-layer fixes
2. **Game second** — game-quality flows from engine-layer integrity; never sacrifice engine integrity for short-term game-layer convenience
3. **Phase third** — current-phase scope is bounded by engine-first + game-second commitments; if phase scope conflicts with engine integrity, defer phase work or invoke framing-refusal

The orientation is composition-with not replacement-of seam-owned discipline.
```

## Per-agent OP target files (9)

| Agent | OP file path |
|---|---|
| jack-ryan | `agentic_orchestration/operating-procedures/jack-ryan.md` |
| gandalf | `agentic_orchestration/operating-procedures/gandalf.md` |
| gamora | `agentic_orchestration/operating-procedures/gamora.md` |
| rocket | `agentic_orchestration/operating-procedures/rocket.md` |
| star-lord | `agentic_orchestration/operating-procedures/star-lord.md` |
| drax | `agentic_orchestration/operating-procedures/drax.md` |
| elrond | `agentic_orchestration/operating-procedures/elrond.md` |
| legolas | `agentic_orchestration/operating-procedures/legolas.md` |
| galadriel | `agentic_orchestration/operating-procedures/galadriel.md` |

If the OP file doesn't yet exist for any agent, create it per the gandalf OP prototype structure (`.claude/skills/reincarnated-<agent>-operating-procedure/SKILL.md` mirror).

## Required reading

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #42 (canonical text for Move 2 template)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #43 (composes with Move 4 at wave-close)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #44 (canonical text for Move 3 template)
- `agentic_orchestration/AGENTS.md` (Move 5 orientation phrase block; canonical authority)
- `agentic_orchestration/operating-procedures/knight-rider.md` § 3.11 (KR Move 1 template; pattern reference)
- This dispatch (your seam's amendment instruction)

## Discipline #46 compliance

- N/A — OP documentation amendment; no DB queries

## Discipline #42 framing-audit (this dispatch)

- **Q1 load-bearing assumptions:** (1) standardized template applies across all 9 OPs without per-agent customization beyond placement judgment; (2) each agent has authority to amend their own OP per AGENTS.md convention; (3) per-agent OP file exists OR can be created per prototype
- **Q2 refutation evidence to seek:** verify template doesn't contradict existing per-agent OP structure (especially gandalf with Pattern A-deep three-question protocol composition); verify orientation phrase placement at OP top doesn't displace existing § 0 or § 1 content
- **Q3 outcome trigger:** if template doesn't compose cleanly with existing OP, invoke Discipline #44 framing-refusal + surface to KR for re-template

## Scope (each agent on own OP)

- [ ] Read your OP file at the target path
- [ ] Read the 3 template sections above (Move 2 / Move 3 / Move 5)
- [ ] Choose placement for each section:
  - **Move 2 (framing-audit):** in disposition-related section (e.g., "Decision-loop discipline"); composes with any per-agent verdict-authoring protocol
  - **Move 3 (framing-refusal):** in mode-selection or scope-management section; cross-reference per-seam refusal directory at `agentic_orchestration/<your-agent>/refusals/`
  - **Move 5 (orientation phrase):** at OP top preamble OR § 0 introduction; cross-reference AGENTS.md authority
- [ ] Apply template to OP file (verbatim or with per-agent context adaptation per your judgment)
- [ ] Verify Discipline #42 framing-audit Q1/Q2/Q3 holds for your specific OP composition
- [ ] If Q3 triggers, invoke Discipline #44 framing-refusal + surface back to KR (DO NOT force template if it contradicts your seam discipline)

### Closure (per agent)

- [ ] Update your own OP file
- [ ] Append per-agent completion record to THIS dispatch (single dispatch file collects all 9 completion records)
- [ ] Per-agent commit: `<agent>: OP amendment per Move 2+3+5 (Disciplines #42 + #44 + orientation phrase)`
- [ ] Push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria (per agent)

- [ ] OP file amended with Move 2 + Move 3 + Move 5 sections
- [ ] No conflict with existing OP structure (or surfaced via #44 refusal)
- [ ] Per-agent completion record appended
- [ ] Commit + push per agent

## Out of scope

- Do NOT amend KR OP (already amended at `8a1ee9a`)
- Do NOT amend canonical-discipline-authority text at engineering-disciplines.md (jack-ryan owns; canonical text is already at `e93d9ad`)
- Do NOT amend AGENTS.md (already has Move 5 orientation phrase block)
- Do NOT touch other agents' OPs (each owns own)

## Open questions (per agent surfaces if applicable)

- **Q-OP-<agent>-1:** does standard template placement work for your OP, or does per-agent context warrant adaptation? Surface in completion record
- **Q-OP-<agent>-2:** any pre-existing per-agent discipline that composes-with vs replaces template (e.g., gandalf Pattern A-deep)?

## References

- Disciplines #42 / #43 / #44 ratified at engine `e93d9ad` (jack-ryan canonical-write)
- AGENTS.md (Move 5 orientation phrase canonical)
- KR OP § 3.11 (Move 1 template pattern reference)
- Matt 2026-05-27 Matt-gate Path (1) ratification routing

---

## Per-agent completion records

(each agent appends own section below on completion)

### jack-ryan

**Completed:** 2026-05-27
**Agent:** jack-ryan
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1: Template assumes clean composition across all 9 OPs; jack-ryan OP already has Discipline #23 (Pattern A-deep framing-audit) at § 3.10 — potential duplication risk
- Q2: Verified Discipline #23 and Discipline #42 operate at different workflow points (#42 = dispatch-entry; #23 = within verdict authoring). No duplication. `agentic_orchestration/jack-ryan/refusals/` directory confirmed present. Orientation phrase placement at OP top verified no § 0 structural displacement.
- Q3: No contradiction surfaced. Template composes cleanly. Proceeding.

**Placement decisions:**
- Move 5 (orientation phrase): inserted as standalone section BEFORE § 0 (top of OP preamble), with cross-reference to AGENTS.md canonical authority
- Move 3 (framing-refusal § 2.7): inserted after Mode F in § 2 (mode-selection section), with explicit composition note distinguishing #44 refusal from Mode F invocation-gating
- Move 2 (framing-audit § 3.12): inserted as § 3.12 in decision-loop section, after existing § 3.10 Discipline #23 cross-reference, with explicit composes-with note

**Composition notes:**
- Q-OP-jack-ryan-1: Standard placement worked cleanly. No structural conflicts.
- Q-OP-jack-ryan-2: Discipline #23 (§ 3.10) pre-exists and addresses Pattern A-deep framing-audit within verdict authoring. Discipline #42 (§ 3.12) addresses dispatch-entry framing-audit before execution. The compose-with note in § 3.12 makes the distinction explicit — these are complementary, not redundant.

**Files amended:**
- `agentic_orchestration/operating-procedures/jack-ryan.md`

### gandalf

**Completed:** 2026-05-27
**Agent:** gandalf
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1 load-bearing assumptions: (1) three template sections compose cleanly with existing gandalf OP, particularly with pre-existing § 4.1 Pattern A-deep three-question protocol (which IS the precursor to Discipline #42); (2) gandalf owns own OP per AGENTS.md; (3) `agentic_orchestration/gandalf/refusals/` directory present (.gitkeep confirmed, dated 2026-05-27 18:03); (4) Move 5 preamble at top doesn't displace existing STATUS block; (5) Pattern R-3 (no-classes architecture) is particularly load-bearing for gandalf per Stage 3+4 mid-grep redaction precedent (smith-monk → smith-ascetic, assassin → walker variants).
- Q2 refutation evidence sought: verified refusals dir present with seam-specific .gitkeep note; verified § 4.1 Pattern A-deep three-question protocol is the precursor of #42 (same Q1/Q2/Q3 shape) — they operate at different scopes (§ 4.1 at Pattern A-deep verdict authoring; § 3.7/#42 at ANY dispatch consumption entry), composing-with rather than replacing; verified no existing Move 5 preamble; verified Disciplines #41/#42/#43/#44/#45 ratified at engine `e93d9ad` per jack-ryan canonical-write 2026-05-27 (engineering-disciplines.md grep confirmed all 5 disciplines present); verified § 3.1 push-back-hard authority is content-level (composes-with not duplicates framing-level refusal at Discipline #44).
- Q3 outcome: no contradiction with seam-owned authority. Template composes cleanly with explicit composes-with annotations matching the jack-ryan/rocket/gamora/star-lord precedent. No Discipline #44 framing-refusal warranted. Proceeded.

**Placement decisions:**
- **Move 5 (orientation phrase):** inserted at TOP of OP as standalone `## Orientation phrase (Move 5; team-wide)` section, BEFORE the STATUS block — matches jack-ryan/rocket/gamora/star-lord/drax/elrond/galadriel precedent. Gandalf-specific "Engine first" expansion explicitly names canonical-narrative integrity context (THEMATIC_REGISTRY foundation, PM-2 D-Sharpened invariance, Path III G-B math spec at canonical doc § 13, design-spec-as-math handoffs that respect engine-layer architecture per Discipline #41 no-classes + substrate-led discipline). Composes naturally with the just-embedded engine-first canonical-narrative integrity work (THEMATIC_REGISTRY all 4 stages at meta `da56926`; PM-2 § 13 G-B amendment at engine `768a68d` + meta `6d1d5c0`). "Game second" instantiated with story coherence + player-experience design + thematic resonance + class-fantasy fidelity. "Phase third" instantiated with Cycle 14 wave cadence + Phase E-N work + Pattern-X recovery work. STATUS block amended with "Move 2+3+5 amendments 2026-05-27" provenance note. Canonical authority cross-referenced to AGENTS.md § Move 5 block.
- **Move 3 (framing-refusal authority, Discipline #44):** inserted as `### Framing-refusal authority (Discipline #44 — Move 3)` subsection at END of § 2 mode-selection, after "Design call with specialist" — preserves mode-selection as the complete "what kind of work + what can be refused" block per gamora/star-lord/elrond precedent. All 4 R-patterns instantiated with gandalf-resident examples: R-1 (mis-routed authority — simulation math route to gamora, decisions-log entries route to jack-ryan, dispatch firing routes to KR, engineering-disciplines.md canonical text routes to jack-ryan); R-2 (seam-discipline violation — § 3.4 recognition-validate-commit violations, § 3.3 AI-tell-line violations, § 3.5/§ 3.6 editorialization violations); R-3 (no-classes architecture — PARTICULARLY LOAD-BEARING for gandalf per Stage 3+4 mid-grep redaction precedent; cross-reference to refusals directory for future smith-monk → smith-ascetic / assassin → walker-variants record; composes with Discipline #45 vocabulary lock); R-4 (methodology depth route to legolas Mode A). Explicit composition note distinguishing § 3.1 content-level push-back from Discipline #44 framing-level refusal. Matt 2026-05-27 quote on stagnant-vestigial-logic cost cited as authority anchor.
- **Move 2 (framing-audit at dispatch consumption, Discipline #42):** inserted as new § 3.7 in decision-loop discipline section, AFTER § 3.6 timezone-agnosticism and BEFORE the `---` separator into § 4. Gandalf-specific apply-points named: sub-agent dispatch consumption entry (Pattern A-light + A-deep + Pattern-B inbound), math hotspot ratification (P2/P3/P5), Pattern A-deep verdict authoring entry, cross-seam routing (design-spec-as-math handoffs), canonical-narrative integrity gates (THEMATIC_REGISTRY work, PM-2 invariance, Path III G-B math spec). Two explicit composition notes added: (a) with § 4.1 Pattern A-deep three-question protocol — § 4.1 is the PRECURSOR of #42, generalized at dispatch consumption (§ 3.7) vs. Pattern A-deep verdict authoring (§ 4.1), with the first-canonical-example (§ 4.5 gamora ~120-sec Pattern-A query) demonstrating both at once; (b) with § 3.4 recognition-validate-commit — Q2 IS empirical-evidence inspection at dispatch consumption; Q3=YES triggers framing-refusal; recognition-validate-commit handles deferred architectural commitments downstream. § 4.7 composition table updated with the new § 3.7 ↔ § 4.1 relationship + new § 4.6 ↔ § 3.7 temporal-complement relationship (#42 catches framing BEFORE execution; #43 catches drift AFTER).

**Composition notes:**
- **Q-OP-gandalf-1 (placement adaptation):** standard template placement worked with gandalf-specific adaptation. Three adaptations of note: (i) Move 5 preamble expanded to name gandalf-specific Engine/Game/Phase semantics where "Engine first" = canonical-narrative integrity at engine-substrate seam (THEMATIC_REGISTRY foundation, PM-2 D-Sharpened invariance, Path III G-B math spec) — load-bearing because gandalf's "engine layer" is the canonical-narrative substrate, not the runtime engine seam; (ii) Move 3 refusal patterns contextualized with gandalf-resident routing examples and explicit R-3 flag for the Stage 3+4 mid-grep redaction precedent; (iii) Move 2 framing-audit composition note explicitly anchors to § 4.1 first-canonical-example (§ 4.5) demonstrating both Pattern A-deep verdict-authoring framing-audit AND wider dispatch-consumption framing-audit catching the same pre-imposed-assumption failure at ~120-sec latency. Adaptation is composition-with not modification-of canonical template.
- **Q-OP-gandalf-2 (pre-existing per-agent discipline composition):** Two pre-existing disciplines compose-with template:
  - **§ 4.1 Pattern A-deep three-question protocol** (established 2026-05-23) IS the precursor of Discipline #42. Same Q1/Q2/Q3 shape. #42 (ratified 2026-05-27 at engine `e93d9ad`) generalizes § 4.1's three-question protocol to ALL sub-agent dispatch consumption — not just Pattern A-deep verdict authoring. Section § 3.7 makes the relationship explicit; § 4.7 composition table now anchors § 4.1 as the precursor. Complementary, not redundant.
  - **§ 3.1 push-back-hard authority** is content-level (object-level disagreement with a proposed design move, lore choice, mechanic decision); **Discipline #44 framing-refusal** is framing-level (the dispatch itself is structurally mis-framed). Move 3 Framing-refusal authority subsection makes the distinction explicit. Push back when content is wrong; refuse when framing is wrong. They compose without overlap.

**Files amended:**
- `agentic_orchestration/operating-procedures/gandalf.md`

### gamora

**Completed:** 2026-05-27
**Agent:** gamora
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1: (1) template sections compose cleanly with existing OP structure; (2) gamora has self-amendment authority per AGENTS.md convention; (3) refusals directory confirmed present at `agentic_orchestration/gamora/refusals/`; (4) existing Discipline #23 cross-reference at § 3.5b and Mode 1 extension discipline address framing-audit at verdict-authoring depth — distinct from Discipline #42 dispatch-entry gate
- Q2: refutation evidence sought — read gamora OP in full; verified no existing Move 5 orientation phrase; verified Discipline #23 is cross-referenced at § 3.5b (operational cross-reference) and in Mode 1 extension discipline (verdict-authoring trigger) — these operate at a different trigger point than Discipline #42 (dispatch-entry); confirmed `.gitkeep`-pattern refusals directory present; no contradiction found
- Q3: no contradiction surfaced. Template composes cleanly. Proceeding.

**Placement decisions:**
- Move 5 (orientation phrase): inserted as standalone `## Orientation phrase (Move 5; team-wide)` section at OP top preamble, after metadata block and before `---` separator and `## 0`. Includes gamora-specific expansion: Engine first = simulation integrity (fight engine, balance loop, convergence algorithm, doppelganger gate); Game second = fight quality + spirit-guide output downstream of simulation integrity; Phase third = current-phase scope bounded by engine-first + game-second. Canonical authority cross-referenced to AGENTS.md Move 5 block.
- Move 3 (framing-refusal authority Discipline #44): inserted as `### Framing-refusal authority (Discipline #44)` in `## 2` mode-selection section, after Mode 4 and before Canonical capture. All 4 R-patterns instantiated with gamora-specific examples. R-4 particularly named per dispatch brief (HDBSCAN § 4.6 fallback precedent; fight-engine spatial-distribution math and doppelganger calibration sweep methodology as named hotspots per § 3.3).
- Move 2 (framing-audit at dispatch consumption Discipline #42): inserted as `### 3.8` in `## 3` decision-loop discipline section, after § 3.7 file-write constraint. Q1/Q2/Q3 instantiated with gamora-specific examples (AGENT_STATE.md checkpoint verification, math note existence check, smoke-test result verification before treating as given). Explicit composition note with Discipline #23: #42 = entry-gate (fires before execution); #23 = deep-protocol (fires within verdict authoring). Complementary, not duplicate.

**Composition notes:**
- Q-OP-gamora-1: Standard template placement worked cleanly. No structural conflicts. Move 5 preamble placement natural (between metadata block and § 0 — no existing preamble to displace). Move 3 placed in § 2 mode-selection (after Mode 4, before Canonical capture) — preserves mode-selection as the complete "what kind of work + what can be refused" block. Move 2 placed as § 3.8 in decision-loop (natural extension of pushback discipline at § 3.1 through § 3.7).
- Q-OP-gamora-2: Two pre-existing discipline cross-references compose-with rather than conflict-with the template. Discipline #23 (§ 3.5b + Mode 1 extension discipline) is the deep-protocol framing-audit at verdict-authoring depth — it pre-existed and names gamora-specific framing-commitment points (convergence-gate verdicts, doppelganger calibration verdicts, fight-engine spatial-distribution math verdicts). Discipline #42 (new § 3.8) is the dispatch-entry framing-audit — fires earlier, wider scope (any dispatch consumption), same Q1/Q2/Q3 shape. The composition note in § 3.8 makes the distinction explicit.

**Files amended:**
- `agentic_orchestration/operating-procedures/gamora.md`

### rocket

**Completed:** 2026-05-27
**Agent:** rocket
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1: (1) three template sections compose cleanly with existing OP without contradiction; (2) rocket has self-amendment authority per AGENTS.md; (3) `agentic_orchestration/rocket/refusals/` directory confirmed present; (4) Move 5 orientation phrase at top preamble does not displace existing § 0 STATUS block; (5) Pattern R-3 (no-classes architecture) is particularly load-bearing for rocket given Stage 3 Option α recommitment at engine `2dce2fa`
- Q2: (a) existing OP has no orientation phrase — Move 5 is net-new addition; (b) existing § 3.7 cross-references Discipline #23 framing-audit — #42 operates at dispatch-entry BEFORE execution; #23 operates within Pattern A-deep verdict authoring; these are different workflow points, not duplicates; (c) refusals directory confirmed present; (d) Move 3 framing-refusal authority fits naturally at end of § 2 mode-selection block; (e) Move 5 preamble before STATUS block confirmed structurally sound
- Q3: No contradiction with seam-owned authority. All three templates compose cleanly. No Discipline #44 framing-refusal warranted. Proceeded.

**Placement decisions:**
- Move 5 (orientation phrase): inserted at TOP of file before STATUS block, as standalone preamble section; expanded with rocket-specific "Engine first" context anchoring to no-classes architecture (Discipline #41) + Stage 3 Option α recommitment; cross-references AGENTS.md as canonical authority; STATUS block amended with 2026-05-27 amendment note for provenance
- Move 3 (framing-refusal authority, Discipline #44): inserted as new "Framing-refusal authority (Discipline #44 — Move 3)" subsection at END of § 2 mode-selection, after "Math hotspot execution" mode; all 4 R-patterns instantiated with rocket-specific examples; R-3 explicitly flagged as particularly load-bearing for rocket given Stage 3 Option α recommitment; composition note added distinguishing § 3.1 content-level push-back from Discipline #44 framing-level refusal
- Move 2 (framing-audit at dispatch consumption, Discipline #42): inserted as new § 3.10 in decision-loop discipline section, after § 3.9; rocket-specific Q1/Q2 empirical evidence sources named; apply-points enumerated including dispatch entry, math hotspot ratification, Pattern A-deep verdict authoring, cross-seam routing, gandalf design-spec-as-math handoff; composition note with Discipline #23 (§ 3.7) making gate-vs-deep-protocol distinction explicit

**Composition notes:**
- Q-OP-rocket-1: Standard template placement worked cleanly. No structural conflicts. Move 5 preamble placement before STATUS block is natural given no existing orientation phrase. Move 3 placement at end of § 2 mode-selection keeps the complete "what kind of work + what can be refused" contract in one section. Move 2 as § 3.10 follows existing § 3.x numbering sequence without displacement.
- Q-OP-rocket-2: Discipline #23 (§ 3.7 cross-reference) pre-exists for Pattern A-deep framing-audit within verdict authoring. Discipline #42 (§ 3.10) addresses dispatch-entry framing-audit before any execution begins. Composition note in § 3.10 makes #42-as-gate + #23-as-deep-protocol distinction explicit — complementary, not redundant.

**Files amended:**
- `agentic_orchestration/operating-procedures/rocket.md`

### star-lord

**Completed:** 2026-05-27
**Agent:** star-lord
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1: (1) template applies cleanly across star-lord OP thin-format; (2) star-lord has self-amendment authority per AGENTS.md; (3) `agentic_orchestration/star-lord/refusals/` confirmed present; (4) orientation phrase at OP top doesn't conflict with existing STATUS block; (5) Move 2 composes with existing Discipline #23 cross-reference at § 3.7 (different depth: #42 = dispatch-entry gate; #23 = Pattern A-deep verdict-authoring); (6) Move 3 adds formal framing-refusal authority — § 3.1 pushback is content-level; Discipline #44 is framing-level; no contradiction
- Q2: verified Discipline #23 in § 3.7 operates at verdict-authoring depth (Pattern A-deep), not dispatch-entry — Move 2 is complementary not duplicate; verified § 3.1 pushback is content-level (specific field/retry/DB-write violations) vs Discipline #44 framing-level (structurally mis-framed dispatch) — composition without conflict; confirmed refusals dir present; confirmed no existing Move 5 preamble
- Q3: no contradiction surfaced. Template composes cleanly. No framing-refusal invoked. Proceeding.

**Placement decisions:**
- Move 5 (orientation phrase): top preamble, BEFORE the STATUS block — matches drax/legolas/galadriel pattern; "Engine first" expanded to name star-lord's specific engine-layer meaning (export/output/telemetry/llm seam integrity: schema validation at write boundaries, cost-tracked LLM call-sites, durable telemetry, bounded retries); "Phase third" instantiated with ExportFactionCluster + Phase 5/7 placeholders per Dispatch 3B Seam 3 context; STATUS block updated with 2026-05-27 amendment note for provenance; canonical authority cross-referenced to AGENTS.md Move 5 block
- Move 2 (framing-audit § 3.9): new § 3.9 in decision-loop section, after existing § 3.8 (deferred-work gate); seam-specific Q1/Q2 content named (schema validators at write boundary, telemetry column existence, MIGRATION.md presence, LLM call-site ledger coverage); apply-points include dispatch-entry, P5 methodology lock, Pattern A-deep export schema decisions, cross-seam routing; composition note explicitly distinguishes #42 (dispatch-entry) from #23 (verdict-authoring depth)
- Move 3 (framing-refusal § 3.10): new § 3.10 immediately after § 3.9; cross-references `agentic_orchestration/star-lord/refusals/`; all 4 R-patterns instantiated with star-lord-resident examples; R-2 expanded per dispatch note (synthetic-stub-as-permanent-fallback for content-generation call-sites is load-bearing Pattern R-2 for LLM-call infra seam — test-only vs permanent-fallback boundary explicit); composition note distinguishes § 3.1 content-level pushback from § 3.10 framing-level refusal

**Composition notes:**
- Q-OP-star-lord-1: Standard template placement worked cleanly with seam-specific context adaptation (orientation block expanded to name star-lord-specific Engine/Game/Phase semantics; refusal patterns contextualized with export/telemetry/LLM resident examples; framing-audit Q1/Q2 surfaces seam-specific empirical checks). Adaptation is composition-with not modification-of canonical template.
- Q-OP-star-lord-2: Discipline #23 (§ 3.7 cross-reference — Pattern A-deep three-question protocol) pre-exists and fires at verdict-authoring depth. Discipline #42 (§ 3.9) fires at dispatch-entry, before execution begins. These are complementary gates at different workflow depths. § 3.1 pushback (content-level) and § 3.10 Discipline #44 (framing-level) are two separate enforcement layers that compose without overlap.

**Files amended:**
- `agentic_orchestration/operating-procedures/star-lord.md`

### drax

**Completed:** 2026-05-27
**Agent:** drax
**Status:** DONE

**Framing-audit (Discipline #42) applied at entry:**
- Q1: drax OP exists and is current; template applies without contradiction; drax has self-amendment authority; refusals directory confirmed present at `agentic_orchestration/drax/refusals/`
- Q2: refutation evidence sought — no placement conflict found; existing Discipline #23 cross-reference composes with Move 2 (different depth: #42 fires at dispatch consumption entry, #23 is deep verdict-authoring protocol)
- Q3: no contradiction surfaced; no framing-refusal invoked; proceeding

**Placement decisions:**
- Move 5 (orientation phrase): inserted at top preamble after metadata block, before `§ 0 What this skill IS and IS NOT`; canonical authority cross-referenced to AGENTS.md
- Move 3 (framing-refusal authority): inserted as `### Framing-refusal authority (Discipline #44)` in `§ 2` mode-selection section, after Pattern B entry; cross-references `agentic_orchestration/drax/refusals/`; R-2 pattern adapted for presentation-seam specificity (engine-side fix from presentation seam named explicitly)
- Move 2 (framing-audit at dispatch consumption): inserted as `§ 3.9` in `§ 3` decision-loop discipline section, after `§ 3.8`; includes composition note with Discipline #23 clarifying #42 fires at dispatch entry (#42 = gate, #23 = deep protocol); presentation-seam hotspots named (Vercel deploy decisions, demo-vs-loadout feature-placement)

**Composition notes:**
- Q-OP-drax-1: Template placement worked cleanly. Move 3 placed inside `§ 2` mode-selection (after Pattern B) rather than as a standalone section break — preserves mode-selection as the complete "what kind of work + what can be refused" block.
- Q-OP-drax-2: Discipline #23 (framing-audit checklist; Pattern A-deep three-question protocol) pre-existed in cross-references. Composes-with Move 2 rather than replacing. Documented in §3.9 composition note.

**Files amended:**
- `agentic_orchestration/operating-procedures/drax.md`

### elrond

**Status:** COMPLETE 2026-05-27

**OP file amended:** `agentic_orchestration/operating-procedures/elrond.md`

**Placement decisions:**

- **Move 5 (orientation phrase):** prepended above existing STATUS block as blockquote preamble; elrond-specific context added — "engine first" includes substrate-layer integrity (catalogue DB schema soundness, Phase D cleaning gates a/b/c/d, source-anchored reversibility) — substrate IS the data-steward seam's engine-layer; cross-references AGENTS.md Move 5 block as canonical authority
- **Move 2 (Discipline #42 framing-audit):** inserted as new § 3.13 after existing § 3.12 cross-references block; composes with § 3.3 Pattern A-deep adoption, § 3.4 math-hotspot routing, § 3.5 Discipline #11, § 3.6 Discipline #20; elrond-specific entry points enumerated (P2/P3 ratification, Pattern A-deep verdict authoring, Discipline #25 cross-seam routing, Phase D gate go/no-go calls, cross-source canonical merge schema decisions); composition note added for the bundled-methodology-consultation pattern (precedent commit `f8eb1a4` — Cycle 14 Path (1) 5-sub-query consultation) — framing-audit runs ONCE on the bundle's framing rather than per sub-query
- **Move 3 (Discipline #44 framing-refusal authority):** inserted as new § 3.14 after § 3.13; cross-references refusals directory at `agentic_orchestration/elrond/refusals/`; all 4 refusal patterns (R-1/R-2/R-3/R-4) instantiated with elrond-specific examples — R-1 (engine telemetry schema, design-meaning of cluster output, ADR-004 routing); R-2 (schema without source-anchoring, P2/P3 without methodology consultation, crawl-derived substrate without robots.txt verification per Discipline #20, density-based algorithm row-duplication per #20 second sense, silent value transformation); R-3 (pre-authored taxonomy where substrate should vote — Pattern 4-5-6 retirement spirit); R-4 (methodology depth requiring legolas Mode A consultation); composition note with § 3.1 pushback-within-data-domain — pushback ("fix and re-fire") vs refusal ("framing needs re-authoring") boundary clarified

**Discipline #42 framing-audit (this dispatch):**

- **Q1 load-bearing assumptions:** (a) standardized template composes cleanly with existing § 2 mode-selection and § 3 decision-loop structure; (b) Move 5 preamble doesn't conflict with existing § 0 STATUS header; (c) Move 2 composes with existing Pattern A-deep + bundled-methodology-consultation pattern rather than replacing; (d) Move 3 is genuinely new authority — § 3.1 covers pushback but not formal refusal
- **Q2 refutation evidence sought:** inspected existing OP (§ 3.3 Pattern A-deep adoption; § 3.12 cross-references to #25 + #18.1/2; § 3.1 data-domain pushback); inspected refusals directory (`.gitkeep` present); inspected engineering-disciplines.md (#42 + #43 + #44 ratified at jack-ryan canonical-write 2026-05-27); inspected bundled-methodology-consultation precedent (`f8eb1a4`). All inspections confirm template ADDS dispatch-consumption-time framing-audit + formal refusal authority; does NOT contradict
- **Q3 outcome:** no contradiction with seam-owned authority. Template applies with placement judgment. No Discipline #44 framing-refusal warranted; proceed with amendment

**Open questions surfaced:**

- **Q-OP-elrond-1:** standard template placement worked with elrond-specific adaptation — Move 5 preamble extended with substrate-as-engine-layer context (load-bearing because elrond's "engine layer" is the substrate, not the runtime engine seam); Move 2 § 3.13 composes with bundled-methodology-consultation pattern (composition note added; not contradiction); Move 3 § 3.14 instantiates all 4 R-patterns with elrond-resident examples (instantiation, not template-deviation). No structural conflict; no Move 4 KR surface required
- **Q-OP-elrond-2:** pre-existing per-agent discipline composes-with template — § 3.3 Pattern A-deep adoption (gandalf OP § 2 discriminator inheritance) extends naturally to § 3.13 Pattern A-deep verdict-authoring framing-audit entry point; § 3.1 pushback-within-data-domain composes-with § 3.14 framing-refusal authority (boundary clarified — pushback at content level; refusal at framing level)

**Files amended:**

- `agentic_orchestration/operating-procedures/elrond.md`

### legolas

**Status:** COMPLETE — 2026-05-27

**OP file amended:** `agentic_orchestration/operating-procedures/legolas.md`

**Placement decisions:**
- **Move 5 (orientation phrase):** inserted at OP top preamble — after the STATUS/skill-packaging block, before `**Authored:**` metadata line and § 0. Placement chosen so orientation phrase is the first substantive content encountered on every invocation.
- **Move 2 (framing-audit, Discipline #42):** new § 3.10 in decision-loop discipline section, following § 3.9 (empirical-evidence gate). Composes with existing Discipline #23 three-question protocol already cross-referenced in § 3 — noted explicitly as same discipline, Q1/Q2/Q3 structure is canonical form.
- **Move 3 (framing-refusal, Discipline #44):** new § 3.11 immediately following § 3.10. Cross-references `agentic_orchestration/legolas/refusals/`. Composition note with existing § 3.1 pushback authority added — § 3.1 is the operational form; Discipline #44 is canonical framing; pushback categories mapped to R-patterns explicitly.

**Q-OP-legolas-1 (template placement):** standard placement worked cleanly. No structural conflict. Move 5 preamble placement is natural given the thin-OP format (no § 0 heading to displace — it precedes the authored metadata block). Move 2 and Move 3 slot into decision-loop § 3 as §§ 3.10 and 3.11 without displacing any existing content.

**Q-OP-legolas-2 (pre-existing discipline composition):** two composition notes:
1. Discipline #23 (Pattern A-deep three-question protocol) already cross-referenced in § 3; Move 2 explicitly notes these are the same discipline at Q1/Q2/Q3 level — no duplication, just canonical anchoring.
2. Pattern R-4 in Move 3 template is asymmetric for legolas: legolas IS the route-target for R-4 from other agents (methodology depth exceeding transcription scope routes TO legolas Mode A). When legolas itself faces a downstream R-4 situation (consumer asking legolas to synthesize beyond seam scope), re-route to KR. Asymmetry explicitly called out in § 3.11.

**Discipline #42 framing-audit (Q1/Q2/Q3 for this amendment task):**
- Q1: (1) template applies across legolas OP without contradiction; (2) legolas owns its OP per AGENTS.md; (3) no orientation phrase yet present in OP
- Q2: read both OP and dispatch; verified no existing Move 5 preamble; verified § 3.1 pushback authority composes with (not duplicates) Discipline #44; verified no read-only constraint conflict (amendment is to legolas's own OP, which is in-seam-scope per seam authority)
- Q3: no contradiction found; proceeded

**Files amended:**
- `agentic_orchestration/operating-procedures/legolas.md`

### galadriel

**Status:** COMPLETE 2026-05-27

**Amendment applied to:** `agentic_orchestration/operating-procedures/galadriel.md`

**Placement choices (per dispatch § Scope step "Choose placement"):**
- **Move 5 (orientation phrase):** TOP preamble — new `> **Orientation: Engine first. Game second. Phase third.**` block immediately after title, with galadriel-contextualized Engine/Game/Phase expansions (Engine = reference-image provenance + rubric falsifiability; Game = visual coherence + style-register fidelity; Phase = benchmark cycles + PD Meshy gap-fill + P5 calibration sweeps + Pattern A dispatches). Preserved existing § 0 STATUS block immediately after; added 2026-05-27 amendment note to STATUS line per provenance discipline.
- **Move 3 (framing-refusal authority Discipline #44):** in § 2 mode-selection at end (after "Capture-pipeline tooling") as new "Framing-refusal authority (Discipline #44 — Move 3)" subsection. Galadriel-contextualized all 4 refusal patterns: R-1 (mis-routed authority — gandalf for design-meaning / drax for render-architecture); R-2 (seam-discipline violation — scoring-vs-findings, survey-mode, falsifiability, manifest-provenance); R-3 (pre-authored taxonomy under no-classes — composes with § 3.6 substrate-led + #41); R-4 (methodology depth exceeds transcription — composes with § 3.2 + § 3.8 surface-back). Explicit composition note: Pattern R-4 IS galadriel's seam-native refusal pattern (generalizes § 3.8 HARD NO from "no sub-agents" to "no carrying mis-framed methodology depth").
- **Move 2 (framing-audit Discipline #42):** in § 3 decision-loop discipline as new § 3.0 (entry-discipline) — composes ahead of every other § 3 sub-discipline; galadriel-contextualized Q1/Q2/Q3 surfaces with seam-specific examples (manifest-row state-matched references, calibration-sweep prior-fire check, surface-in-question reference existence). Apply-points include sub-agent entry, math hotspot ratification (P5), Pattern A-deep verdict authoring, cross-seam routing, benchmark report § 5 + § 6 authoring. Explicit composition note with § 3.11 #23 Pattern A-deep three-question protocol: #42 ratifies the same three-question shape as canonical AND widens applicability from Pattern A-deep specifically to ALL sub-agent dispatch consumption entries.

**Framing-audit Q1/Q2/Q3 at amendment entry (Discipline #42 self-application):**
- **Q1 load-bearing assumptions:** (a) templates compose cleanly with existing OP structure; (b) Move 2 composes with existing § 3.11 #23 (Pattern A-deep three-question protocol — same Q1/Q2/Q3 shape); (c) Move 3 composes with existing § 3.8 no-sub-agent-invocation HARD NO (the surface-back-to-KR pattern IS Pattern R-4); (d) Move 5 at preamble doesn't displace § 0 STATUS block.
- **Q2 refutation evidence:** verified — OP § 3.11 already cross-references #23 precursor; § 3.8 already encodes surface-back-to-KR-or-gandalf as galadriel's seam-native methodology-consultation pattern; refusals dir exists (.gitkeep present at `agentic_orchestration/galadriel/refusals/`). KR OP precedent (commit `8a1ee9a`) placed orientation in § 3.11 not at preamble; galadriel chose preamble placement per dispatch § Scope "at OP top preamble OR § 0 introduction" — both are sanctioned; preamble chosen because the orientation is composition-with not replacement-of seam-discipline AND galadriel's OP doesn't have a § 3.11-equivalent dispatch-authoring-template section where orientation would naturally sit (KR's § 3.11 is dispatch-authoring; galadriel doesn't author dispatches).
- **Q3 outcome trigger:** NO contradiction surfaced. Template composes. No #44 refusal required. Amendment proceeded as authored above.

**Open questions resolved (per dispatch § Open questions):**
- **Q-OP-galadriel-1 (placement adaptation):** standard template placement worked with per-agent context adaptation (orientation block expanded to name galadriel-specific Engine/Game/Phase semantics; refusal patterns contextualized to galadriel's 4 mis-routing patterns; framing-audit Q1/Q2 surfaces galadriel-specific empirical examples). Adaptation is composition-with not modification-of canonical template.
- **Q-OP-galadriel-2 (pre-existing per-agent discipline composition):** § 3.11 #23 Pattern A-deep three-question protocol is the precursor to Move 2 Discipline #42 (same Q1/Q2/Q3 shape). Composition explicit in new § 3.0: #42 supersedes/canonicalizes #23 AND widens applicability from Pattern A-deep to ALL sub-agent dispatch consumption. § 3.8 no-sub-agent-invocation HARD NO is the precursor to Move 3 Pattern R-4 (surface-back to KR/gandalf rather than self-spawn). Composition explicit in new Framing-refusal authority subsection.

**Acceptance criteria check:**
- [x] OP file amended with Move 2 + Move 3 + Move 5 sections
- [x] No conflict with existing OP structure (composition documented per § 3.0 #23-cross-reference + Framing-refusal § Pattern R-4 + § 3.8 composition + preamble + § 0 STATUS preservation)
- [x] Per-agent completion record appended (this entry)
- [ ] Commit + push per agent (firing next)

**Files amended:**
- `agentic_orchestration/operating-procedures/galadriel.md`
