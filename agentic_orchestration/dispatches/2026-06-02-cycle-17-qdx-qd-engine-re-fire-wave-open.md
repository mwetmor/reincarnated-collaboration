# Dispatch — 2026-06-02 — cycle-17 — QDX QD-Engine Workflow Re-Fire with WS1A.4-lite Integration — wave-open

**From:** knight-rider (orchestrator)
**To:** all wave participants (informational); Phase 1 routes to rocket / star-lord in parallel after Gate-1 PASS
**Authority:** Matt 2026-06-02 Pattern B substantive design session → gandalf transmission with QDX chain routing (Locks A-P preserved from EAA chain; Locks Q-T NEW for QDX scope)
**Wave tag:** `QDX-qd-engine-re-fire`
**Cycle directory:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/`
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Estimated horizon:** 5-10 sessions wall-clock
**Wave-close criterion:** QDX-8 wave-close record PASS (canonical write at `canonical/story/2026-06-XX-qdx-chain-wave-close-record.md` + Matt strategic re-engagement signal)

---

## 1. Authoritative reading (READ IN ORDER before any phase action)

1. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** — QD-engine workflow Phase 1-8 architecture; THE pipeline this chain integrates WS1A.4-lite into
2. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** — architectural commitment; preserves continuous kit space + kit-space output schema + Realm Expansion content rhythm
3. **`canonical/00-ground-state.md`** § 1 (current truth)
4. **`canonical/story/2026-06-02-eaa-chain-wave-close-record.md`** — EAA chain wave-close record; documents what was delivered (legacy ClassGenerator path); lists what remains gap
5. **`canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`** — Q18 vocabulary lock; consumed by WS1A.4-lite
6. **`agentic_orchestration/gandalf/notes/2026-06-02-eaa-chain-wave-close-design-quality-audit.md`** — gandalf design-quality audit; flags Cycle 14-equivalent scope gap (the audit that motivates THIS chain)
7. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py`** — current Phase 5 skill naming; WS1A.4-lite must wire INTO this
8. **`~/Games/reincarnated-engine/src/reincarnated/llm/ws1a4_lite_flavor_judgment.py`** — the WS1A.4-lite module to integrate
9. **`~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py`** — the kit-space emitter the QD-engine workflow output emits to
10. **`~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py`** — Cycle 13 wave 5 lineage; reference for fire-script architecture
11. **`~/Games/reincarnated-loadout/public/engine-state/season-001/`** — Cycle 14 wave-5 historical output for richness reference (Pareto + faction clusters + Wave B identity)

---

## 2. Authority chain

**Matt 2026-06-02 Pattern B substantive design session** (gandalf transmission verbatim):

> The EAA chain delivered INFRASTRUCTURE but used legacy ClassGenerator. The result: 25 kits with rich per-skill flavor naming but only 8 distinct kit identity types (3-4 generic per primary), no T4 selection, no faction emergence, no Pareto-from-large-pool richness.
>
> **Matt's actual session-scope goal:** "Cycle 14 wave-5-equivalent output" — i.e., the QD-engine workflow output per canonical 39 (Pareto-from-large-pool + cohesion clustering faction emergence + Wave A/B identity LLM + multi-T4 selection per kit) PLUS WS1A.4-lite per-skill flavor naming applied throughout.
>
> THIS CHAIN delivers that. Wires WS1A.4-lite into QD-engine workflow's skill-naming phase + composes the full pipeline + fires it + emits to kit-space output schema (preserves Season-Archive Realm-Expansion pivot architectural commitment).

**Decision routing per hive-mind directive Matt 2026-05-23:**
- Seam-owners decide in-scope per their seam authority
- Matt is LAST-resort escalation for: decisions exceeding seam authority per ADR-002, push-to-remote (default; here CYCLE-PUSH-PATTERN ESTABLISHED per Matt 2026-06-02), scope-amendment

**Cycle-push authorization:** auto-commit + auto-push per established pattern (Matt 2026-06-02 verbatim "auto-push to remote on standard cycle-push cadence" extending EAA + IA chain precedent).

---

## 3. Pre-commitment package (Locks A-T)

### Locks A-P (PRESERVED from IA + EAA chain — see wave-state file § 1 for full detail)

A-J operational + design + critique-pair authority. K-P engine schema + WS1A.4-lite prompt + skip-flag + n_kits + drax MVP + MM-P1 independence.

### Locks Q-T (NEW for QDX chain — see wave-state file § 1 for full detail)

- **LOCK Q** — QD-engine workflow integration authority (rocket + star-lord; ADDITIVE-ONLY)
- **LOCK R** — QDX-5 fire parameters (KR + rocket + star-lord; n_candidates bounded; cost $5-30)
- **LOCK S** — Integration-smoke-gate per Discipline #54 (single-kit smoke before full fire)
- **LOCK T** — Drax MVP refresh per LOCK O pattern (existing components only)

### Updated escape clause (9 items)

KR escalates to Matt for: (1) engine architectural changes BEYOND QDX integration scope; (2) LLM cost substantially exceeds projection (>2× upper bound ie >$60); (3) kit count substantially below expectations (<20 surviving Pareto); (4) 2+ Gate-2 BLOCKs on QDX-5; (5) Wave B identity LLM template-repeat; (6) MM-P1 surfacing engine-arch-impacting decisions; (7) ADR-002 architectural-commitment-tier scope changes; (8) cross-seam contract semantic changes; (9) strategic direction questions OUTSIDE QDX chain scope.

---

## 4. Wave purpose

Operationalize Matt's actual chain-close goal — Cycle 14 wave-5-equivalent output composed with WS1A.4-lite per-skill flavor naming throughout. Where EAA delivered 25 kits via legacy ClassGenerator (8 identity types; no T4; no Pareto), QDX delivers ~30-40 kits via the canonical QD-engine workflow with full identity emergence + faction clustering + multi-T4 selection + per-skill flavor LLM judgment.

**Architectural shifts (all ADDITIVE per LOCK Q):**

1. **WS1A.4-lite → Phase 5 skill naming integration** — `phase5_skill_naming.py` gains optional `ws1a4_active=True` pre-pass; when active, fires per-skill flavor-or-canonical judgment BEFORE cohesion-judge naming
2. **kit_space_emitter → QD-engine workflow terminal** — `season_generation_pipeline.py` (or successor entry) terminal phase routes to `kit_space_emitter.emit_kit_space_expansion_event()` when skip_* flags True (Realm Expansion path)
3. **Single-entry-point fire script** — `scripts/qdx_qd_engine_re_fire_*.py` composes Phase 2 → 4 → 5 → naming → Wave A/B → T4 → emit in single invocation
4. **Integration-smoke-gate** (Discipline #54) — single-kit smoke before full Pareto-pool fire
5. **Full fire** (QDX-5) — ~30-40 kits, multi-hour wall-clock, $5-30 LLM cost
6. **jack-ryan Gate-2 acceptance verification** (QDX-6) — 7-criteria checklist
7. **Drax MVP refresh** (QDX-7) — loadout + engine page render new output

**Substrate preserved:** WS1A.Q18 Architecture A LOCK unchanged; Q18 vocabulary IMMUTABLE; BC axes unchanged; canonical-7+1 catalog unchanged; substrate composition policy semantic unchanged. EAA chain engine work preserved (WS1A.4-lite + skip flags + kit_space infrastructure all consumed by QDX chain; nothing thrown away).

---

## 5. Phase-by-phase scope summary

### Phase 1 — Integration (parallel fire)

**QDX-1** WS1A.4-lite into Phase 5 skill naming — rocket + star-lord per LOCK Q — ~1-2 sessions
**QDX-2** kit_space_emitter into QD-engine workflow terminal — star-lord + rocket per LOCK Q — ~1 session
**QDX-3** Single-entry-point fire script — rocket per LOCK Q — ~1-2 sessions

Phase 1 PASS criterion: QDX-1 + QDX-2 + QDX-3 all jack-ryan Gate-2 PASS.

### Phase 2 — Integration smoke-gate (sequential)

**QDX-4** Integration-smoke-gate — KR + rocket + star-lord + jack-ryan per LOCK S; single-kit smoke; verifies WS1A.4-lite + emitter + Wave A/B identity + T4 — ~0.5-1 session

Phase 2 PASS criterion: QDX-4 Gate-2 PASS (per 7-criteria smoke checklist; see § 6 below).

### Phase 3 — Full fire + verification (sequential)

**QDX-5** Full QD-engine workflow fire — KR + rocket + star-lord per LOCK R; ~30-40 kits; multi-hour; $5-30 LLM — ~1-3 sessions
**QDX-6** Gate-2 acceptance verification — jack-ryan per LOCK L pattern; 7-criteria acceptance checklist — ~0.5-1 session

Phase 3 PASS criterion: QDX-5 + QDX-6 PASS (verification PASS / PASS-with-INFO; BLOCK invokes LOCK L iteration).

### Phase 4 — Drax MVP refresh (sequential)

**QDX-7** Drax MVP refresh (loadout + engine page) — drax per LOCK T; existing components only — ~2-4 sessions

Phase 4 PASS criterion: QDX-7 Gate-2 PASS + Vercel preview deployed per LOCK G.

### Phase 5 — Wave-close

**QDX-8** Wave-close discipline — KR + gandalf design-quality audit + jack-ryan engineering-disciplines.md amendments — ~1-2 sessions

QDX-8 = wave-close criterion; canonical record + ground-state § 1 update + strategic re-engagement signal to Matt.

---

## 6. Quality criterion

**Game-quality goal this wave serves:** deliver to Matt the **Cycle 14 wave-5-equivalent kit-richness experience** within the Season-Archive Realm-Expansion architectural commitment. Players browsing the kit space encounter distinct emergent kit identities (not template-repeats), grouped into emergent factions, with per-skill thematic flavor naming. The "Necromancer kit" feels uniquely a Necromancer; the "Tempest Caller" feels uniquely a Tempest Caller; Bone Spear coexists with Shadow Bolt on the same kit's skill bar.

**Refutation conditions** (sub-agent surfaces if any apply):
- This wave contradicts canonical 39 architecture (alters QD-engine workflow phase semantics non-additively)
- Alternative execution (e.g., re-firing EAA-5 v2 ClassGenerator with parameters tweaked) would deliver the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., 30+ kits emitted but all template-repeat names)
- Wave framing pre-commits to a decision Matt has not ratified
- Wave introduces a pre-authored taxonomy without justification (#41 candidate)
- Wave introduces a scaffold value not flagged as pending-decision (#40)

**Acceptance criteria** (mechanical completion):
- QDX-1 + QDX-2 + QDX-3 Gate-2 PASS
- QDX-4 smoke verifies pipeline composition (7-criteria checklist)
- QDX-5 produces ~30-40 kits in `data/kit_space/` with full identity emergence
- QDX-6 7-criteria verification PASS / PASS-with-INFO
- QDX-7 drax MVP Vercel deploy
- QDX-8 wave-close canonical record + ground-state § 1 update

**7-criteria QDX-6 acceptance verification (also reused for QDX-4 smoke):**
1. Kit count in 30-40 range (relaxed to ≥1 for smoke; ≥20 for full fire; ≥3 distinct elements for smoke; ≥6 for full)
2. Distinct emergent kit identities (no template-repeat across kits sharing primary element)
3. Faction emergence ≥3 named clusters (full fire; ≥1 for smoke)
4. Multi-T4 selection populated on all kits (`t4_selection` not null)
5. `ws1a4_flavor_rate > 0`; per-skill `ws1a4_*` metadata present on non-physical kits
6. Substrate-led element distribution (not round-robin; reflects substrate substrate composition)
7. Per-skill flavor decisions thematically coherent (sample inspection: flavor words match expected pool; canonical naming reads as canonical)

---

## 7. Critique-pair coverage (jack-ryan)

**Gate-1 (DESIGN-MODE pre-fire review of KR-authored dispatches):**
- This wave-open dispatch — routed AT wave-open before Phase 1 fires
- Each QDX-N dispatch (QDX-1, QDX-2, QDX-3) — routed before respective Phase 1 sub-agent fires
- Each subsequent QDX-N dispatch in Phase 2-5

**Gate-2 (DEV-MODE post-output review with BLOCK authority):**
- QDX-1 + QDX-2 + QDX-3 post-output review
- QDX-4 smoke-gate review (per Discipline #54)
- QDX-5 fire post-output (acceptance criteria check)
- QDX-6 7-criteria acceptance verification (Gate-2 with BLOCK authority for substantive failures)
- QDX-7 drax MVP outputs
- QDX-8 wave-close canonical write

Standard INFO / WARN / BLOCK verdicts per critique-pair-gate-protocol skill.

**LOCK L iteration discipline:** first BLOCK on prompt/integration design → seam re-fire within authority (no Matt-touch); 2+ BLOCKs → Matt escalation.

---

## 8. Cross-references

### Canonical authority
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (architecture)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (commitment preserved)
- `canonical/story/2026-06-02-eaa-chain-wave-close-record.md` (preceding chain; preserves engine infrastructure)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary)
- `canonical/00-ground-state.md` § 1 (current truth)

### Engineering disciplines (relevant)
- Discipline #54 — Integration-smoke-gate before full-fire (consumed by QDX-4)
- Discipline #11 — Empirical inspection (consumed by QDX-6 verification)
- Discipline #53 — LOCK J ADDITIVE-ONLY discipline (consumed by LOCK Q)
- Discipline #1 / #1.1 — Math-before-code + resource-bounds projection (consumed by QDX-3 + QDX-5)
- Discipline #19 — Agent-tool-not-for-waiting (KR fires Phase 1 in parallel)
- Discipline #18 — Methodology-before-execution (consumed at Pareto reduction + cohesion clustering hotspots)

### ADR composition
- ADR-002 tiered approval (LOCK escape clauses compose with tiered authority)
- ADR-004 cross-seam MIGRATION (QDX-1 + QDX-2 may trigger MIGRATION.md updates)
- ADR-006 read-only-by-default (push pattern explicitly authorized by Matt per cycle-push convention)

### Anticipates downstream (when QDX-8 closes)
- MM-P1 substantive design session (composes with QDX-5 kit_space output as empirical backdrop)
- Future kit-space-expansion events (QDX-9+; engine parameter scope expansions)
- Realm Expansion content design (when first Realm content workstream opens)
- Economic-veteran problem resolution (gates on materials/trading scope)

---

## 9. Next moves (KR immediately after this dispatch lands)

1. ✅ Author QDX wave-state file (`cycle-17-qdx-qd-engine-re-fire/wave-state.md`)
2. ✅ Author this wave-open dispatch
3. ✅ Author QDX-1 + QDX-2 + QDX-3 dispatches
4. 🟢 Route jack-ryan Gate-1 review on wave-open + Phase 1 dispatches
5. 🟢 PARALLEL fire QDX-1 + QDX-2 + QDX-3 (rocket + star-lord) via Agent tool with `run_in_background=true` per Discipline #19
6. Auto-commit + auto-push wave-open artifacts per cycle-push pattern
7. On Phase 1 PASS → route QDX-4 smoke-gate
8. On QDX-4 PASS → route QDX-5 + QDX-6
9. On QDX-5 + QDX-6 PASS → route QDX-7 (drax MVP)
10. On QDX-7 PASS → route QDX-8 wave-close + signal Matt for strategic re-engagement

---

**End of QDX wave-open dispatch.**
