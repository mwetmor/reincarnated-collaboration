# Dispatch — 2026-06-01 — cycle-15 — WS1A.Q18 flavor-pool research-and-lock wave-open

**From:** knight-rider (orchestrator)
**To:** all wave participants (informational); Phase 0 routes to elrond as the operational opener
**Approved by:** Matt 2026-06-01 verbatim "hand to KR to fire the wave"
**Wave tag:** `WS1A.Q18-flavor-pool-research`
**Cycle directory:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/`
**State file:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
**Estimated effort:** single wave; 5 phases internally gated; ~13-19 sub-agent invocations total per operational sequence § 5
**Acceptance:** PG-4 PASS on canonical write at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` = wave CLOSED

---

## 1. Authoritative operational sequence

**Read FIRST and IN FULL before any phase action:**
`agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (554 lines)

This document is authoritative for:
- Wave shape (single hive-mind wave; 5 phases gated internally per § 2)
- Per-phase owner + sub-agent fan-out + output artifacts per § 2
- Phase-gate responsibilities matrix per § 3
- Sub-agent fan-out patterns per § 4 (Phase 1 parallel 3 samplers; Phase 3 parallel ≤6 expansion)
- Sub-agent prompt drafts per § 9 Appendix A (KR consumes + finalizes per elrond's PG-0 medium decision)
- Risk register + failure modes per § 7
- Artifact path index per § 8
- Hive-mind composition (state file + critique-pair + wave-close discipline) per § 6

This wave-open dispatch SUMMARIZES the operational sequence for routing; the operational sequence is the canonical reference.

---

## 2. Authority chain

**Matt 2026-06-01 ratifications (verbatim):**
- "ratify hive-mind path; author the operational sequence"
- "Can we not have this made into one long hive mind wave? This would be my leaning to do so (wave with all sessions as gated phases if needed)" — wave-shape framing
- "hand to KR to fire the wave" — current authorization

**Q-shape ratifications (Pattern B session 2026-06-01):**
- Q-shape-1: legolas as commissioner + analyzer; samplers as parallel sub-agents
- Q-shape-2: pre-Phase-1 elrond consultation on data medium
- Q-shape-3: soft cap at 6 expansion sub-agents
- Q-shape-4: existing-pool audit integrated into Phase 5

**Decision routing per hive-mind directive Matt 2026-05-23:**
- Seam-owners decide in-scope per their seam authority
- Matt is LAST-resort escalation for: decisions exceeding seam authority per ADR-002, push-to-remote (default), scope-amendment
- PG-3 (architectural-commitment lock) IS Matt-decision per ADR-002 architectural-commitment scope (vocabulary-lock IS architectural)

---

## 3. Wave purpose

For each of the 8 canonical primary elements (fire / water / earth / wind / lightning / holy / shadow / physical), produce a research-grounded locked sub-element / flavor-element allow-list that represents the kit-identity vocabulary that WS1A.3 (per-kit sub-element selection) and WS1A.4 (per-skill bounded LLM flavor judgment) consume.

**Empirical state at wave-open:** existing `data/seasonal_elements/pool.json` (156 entries; 60 allow-list) covers only 4 primaries (earth/fire/water/wind) at asymmetric cardinality (22/20/11/7); lightning/holy/shadow have ZERO flavor entries; physical absent by design (open 7-vs-8 empirical question).

**Methodology principle (substrate-led applied to vocabulary; Discipline #41):** the locked allow-list per primary emerges from genre-precedent vote count + statistical analysis + design curation. Prior pool authoring was exploratory; this cycle grounds the lock empirically.

**Locked-artifact shape at wave-close** (per operational sequence § 0):
- 7-vs-8 empirical decision (does physical have a sub-element allow-list, or not?)
- Per-primary curated allow-list (target floor ~12-15 entries per rotating primary)
- Q18.a-e structural decisions (primary scope; source of authority; flex semantics; d1_status filter; cardinality target)
- Research provenance trail (3 tracks × 8 primaries empirical inventory)
- Operational-migration dispatch hook for extending `data/seasonal_elements/pool.json`

---

## 4. Phase-by-phase scope summary

Per operational sequence § 2 (full detail there; summary here for routing):

### Phase 0 — Pre-wave elrond data-medium consultation (FIRING at wave-open)

**Owner:** elrond
**Pattern:** single-question consultation; in-wave sub-agent invocation
**Output:** `agentic_orchestration/elrond/consultations/2026-06-XX-q18-flavor-pool-data-medium.md` naming medium choice (E.α Python notebook + Parquet/CSV / E.β substrate DB extension / E.γ flat JSON + pandas-numpy) and format spec
**Phase-gate:** PG-0 — elrond's medium decision binds before Phase 1 fires
**Dispatch:** `agentic_orchestration/dispatches/2026-06-01-elrond-q18-flavor-pool-data-medium-consultation.md`

### Phase 1 — Parallel sample (3 sub-agents fan-out from legolas)

**Owner:** legolas (Mode A commissioner + coordinator)
**Sub-agents:** Sampler-A (ARPG canon) + Sampler-B (JRPG / isekai / anime) + Sampler-C (tabletop + mythological + alchemical); concurrent invocation
**Output:** sample-A/B/C.md (or to elrond-named medium) per § 8 artifact path index
**Phase-gate:** none formal at Phase 1 close; Phase 2 fires automatically once 3 samplers return

### Phase 2 — In-seam triage (legolas analyzer)

**Owner:** legolas
**Output:** sample-triage.md per § 8
**Phase-gate:** PG-1 — gandalf ratifies Phase-3 scope (EXPAND/TERMINATE/NARROW per 8 × 3 viability matrix); soft cap ≤6 expansion sub-agents

### Phase 3 — Adaptive-scope full research (≤6 expansion sub-agents fan-out)

**Owner:** legolas
**Sub-agents:** ≤6 (PG-1-bounded); deeper-research per cell ratified at PG-1
**Output:** full-<track>-<primary>.md per § 8
**Phase-gate:** PG-1.5 (in-flight amendment; conditional) — gandalf re-ratifies if over-cap or NARROW→EXPAND mid-research

### Phase 4 — Elrond statistical analysis

**Owner:** elrond (Phase 4 IS the math hotspot per Discipline #18)
**Output:** stats verdict at `elrond/analysis/element-flavor-mapping-stats-2026-06-XX.md` + raw data
**Phase-gate:** PG-2 — gandalf ratifies dataset sufficient to proceed to synthesis OR routes back to Phase 3 amendment loop

### Phase 5 — Gandalf synthesis + Matt-ratification + canonical write (wave terminus)

**Sub-phases:**
- **5a** — gandalf synthesis draft at `gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md`
- **5b** — Pattern B substantive design call (gandalf + Matt; PG-3 = architectural-commitment lock)
- **5c** — final canonical write at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` + 00-ground-state.md § 1 update + 02-roadmap.md update
- **5d** — jack-ryan Gate-2 wave-close review (PG-4 = wave-close criterion; BLOCK authority)
- **5e** — KR wave-close record + gandalf design-quality audit per OP § 4.6
- **5f (POST-WAVE)** — operational migration dispatch extending `data/seasonal_elements/pool.json`

---

## 5. Critique-pair coverage (jack-ryan)

Per operational sequence § 6:

**Gate-1 (DESIGN-MODE pre-fire review of KR-authored dispatches):**
- This wave-open dispatch + Phase-0 elrond consultation dispatch — routed AT wave-open before Phase 0 fires
- Phase-1 sampler dispatches — KR routes to jack-ryan for Gate-1 after PG-0 (elrond medium decision binds output-format-instructions)
- Phase-3 expansion sub-agent dispatches — KR routes for Gate-1 after PG-1
- Phase-4 elrond stats dispatch — KR routes for Gate-1 after PG-1 close

**Gate-2 (DEV-MODE post-output review with BLOCK authority):**
- Phase 5c canonical write at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md`
- PG-4 = wave-close criterion; BLOCK authority on drift / math-before-code violations / cross-seam impact unaddressed
- Gate-2 PASS = wave closes; Gate-2 BLOCK = amendment cycle re-fires sub-phase 5c

Standard INFO / WARN / BLOCK verdicts apply per critique-pair-gate-protocol.

---

## 6. Wave-close criterion

**PG-4 PASS = wave CLOSED.** PG-4 BLOCK = amendment cycle re-fires sub-phase 5c; wave remains OPEN until PG-4 PASS.

Wave-close discipline (sub-phase 5e):
- KR wave-close record authored at `canonical/story/2026-06-XX-ws1a-q18-flavor-pool-wave-close-record.md`
- Gandalf design-quality audit at `gandalf/notes/2026-06-XX-ws1a-q18-wave-close-design-quality-audit.md` per OP § 4.6 (Discipline #43 candidate; A1-A5 questions; PASS / PASS-with-design-concerns / DRIFT-DETECTED)
- Wave-state file marked CLOSED; pattern-set captured for Q16/Q17/Q19 composition

---

## 7. Pattern-setting note (cross-wave composition)

This wave **PATTERN-SETS** the structure for the remaining WS1A hard-blocker Q-waves:
- WS1A.Q16 (per-skill flavor judgment LLM prompt design)
- WS1A.Q17 (hybrid kit element pair selection)
- WS1A.Q19 (emergent kit concept naming consistency)

Clean execution at Q18 reduces orchestration overhead for subsequent Q waves. Pattern composition success is a Phase 5e wave-close design-quality audit signal.

---

## 8. Cross-seam contract change? (Principle 6 gate)

**Answer:** NO contract change in this wave-open dispatch itself.

Sub-phase 5f (POST-WAVE operational migration dispatch extending `data/seasonal_elements/pool.json`) WILL be a cross-seam contract change touching elrond + star-lord; that dispatch is OUT-OF-SCOPE for the WS1A.Q18 wave per operational sequence § 2 sub-phase 5f. POST-WAVE migration follows standard MIGRATION.md cross-seam discipline per ADR-004.

**Round-trip:** not applicable — no cross-seam contract change in this dispatch (wave-open is orchestration-only; vocabulary lock is design-side architecture; pool migration is POST-WAVE).

---

## 9. Scope checklist (KR self-audit at wave-open)

- [x] Wave-state file initialized at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- [x] Wave-open dispatch authored (this file)
- [x] Phase-0 elrond consultation dispatch authored
- [ ] Jack-ryan Gate-1 routed pre-fire on wave-open + Phase-0 dispatches
- [ ] Phase-0 elrond consultation FIRED (after Gate-1 PASS)
- [ ] Single commit of work-products (Action 5 per gandalf handoff; auto-commit per CLAUDE.md addendum 2026-05-25)
- [ ] Foreground report-back to gandalf (Action 6)

---

## 10. Out of scope (explicit non-goals for THIS wave)

- Pool migration to `data/seasonal_elements/pool.json` — POST-WAVE sub-phase 5f
- WS1A.Q16 / Q17 / Q19 waves — pattern-set but execute as separate downstream waves
- WS1A.3 / WS1A.4 implementation — consumes locked pool downstream of this wave
- Canonical-7+1 element catalog changes — substrate; preserved as-is per operational sequence § 10.4

---

## 11. Sustained-background-process discipline

Per hive-mind protocol § 3.2 + operational sequence § 6:
- Long-running sub-agents (Phase 1 samplers + Phase 3 expansion sub-agents) fire in-background where supported
- KR monitors completion notifications without polling
- Wave proceeds phase-by-phase as sub-agents complete and phase-gates ratify

---

## 12. References

- **Authoritative operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md`
- **Wave-state file:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- **Parent canonical doc:** `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 + § 8b Q18 (parent question) + § 5.2 (WS1A gate sequence)
- **WS1A active-workstream registration:** `canonical/00-ground-state.md` § 1
- **Hive-mind protocol:** `agentic_orchestration/operating-procedures/hive-mind-protocol.md`
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led) + § 42 (framing-audit) + § 18 (math-hotspot methodology consultation)
- **Substrate to extend:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing 156-entry pool — POST-WAVE migration target)
- **Canonical element catalog (substrate):** `~/Games/reincarnated-engine/config/elements.yaml`

---

## Completion record (appended at wave-close)

To be authored at Phase 5e wave-close. Will carry:
- Wave-close timestamp
- PG-4 verdict
- All artifact paths landed
- Wave-state file CLOSED marker
- Pattern-set capture for Q16/Q17/Q19
- Cross-references to KR wave-close record + gandalf design-quality audit + canonical write

---

**End of wave-open dispatch.**
