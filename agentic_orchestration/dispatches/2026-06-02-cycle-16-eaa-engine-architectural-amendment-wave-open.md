# Dispatch — 2026-06-02 — cycle-16 — Engine Architectural Amendment (EAA) chain wave-open

**From:** knight-rider (orchestrator)
**To:** all wave participants (informational); Phase 1 routes to rocket / star-lord / elrond / gandalf-as-subagent in parallel after Gate-1 PASS
**Authority:** Matt 2026-06-02 Pattern B substantive design session ratification ("Realm Expansion confirmed, path α, draft the canonical record") + gandalf transmission with Locks A-P pre-commitment package
**Wave tag:** `EAA-engine-architectural-amendment`
**Cycle directory:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/`
**State file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
**Estimated horizon:** ~10-20 sessions wall-clock per canonical record § 7.1
**Wave-close criterion:** EAA-8 wave-close record PASS (canonical write at `canonical/story/2026-06-XX-eaa-chain-wave-close-record.md` + Matt strategic re-engagement signal)

---

## 1. Authoritative reading (READ IN ORDER before any phase action)

1. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** — THE architectural commitment; load-bearing; § 3 specifies what's NEW; § 7 specifies triggered workstreams (THIS is the binding directive)
2. `canonical/00-ground-state.md` § 1 — current truth (entry at top reflects 2026-06-02 season-archival)
3. `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` — Q18 lock; per-skill flavor pool source; consumed by EAA-1 WS1A.4-lite
4. `agentic_orchestration/gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md` — prior IA-chain close-out; Locks A-J pre-commitment package preserved
5. `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` — Q18 PG-3 ratification artifact
6. `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` — Q18 lock state v1.1; load-bearing for WS1A.4-lite implementation
7. `~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` — current R8 inverted-mode pipeline; to be retired (Stage 1 skip-flag pattern per LOCK M)
8. `~/Games/reincarnated-engine/src/reincarnated/foundation/elements.py` — canonical-7+1 catalog; PRESERVED

---

## 2. Authority chain

**Matt 2026-06-02 verbatim ratifications:**
- "season = archived. We have lost the concept of season with the introduction of the 'chernoff celestial body'"
- "we may periodically look to add additional kits by expanding the scope of the engine's parameters to generate further feature points within space"
- "future content will be a substrate engagement: New Maps, New Acts, New Game Modes. We can specifically tailor these to fit the under-played character kits"
- "Player driven is better than dev driven here I feel"
- "Realm Expansion confirmed, path α"
- "We can leave prior seasonal data as historical content"
- Economic-veteran question EXPLICITLY DEFERRED ("I would like to think further before deciding")

**Matt stated chain-close goal (verbatim):** "20+ characters, similar to Cycle 14 output but also with LLM named skills and with those skill having names influenced by flavor elements where appropriate. The new engine gen should also have the modern caster weapon population fix."

**Decision routing per hive-mind directive Matt 2026-05-23:**
- Seam-owners decide in-scope per their seam authority
- Matt is LAST-resort escalation for: decisions exceeding seam authority per ADR-002, push-to-remote (default), scope-amendment
- Locks A-P pre-commitment scope expanded (see § 3 below); no per-step Matt re-asking within Lock scope

---

## 3. Pre-commitment package (Locks A-P)

### Locks A-J (PRESERVED from IA chain)

- **LOCK A** rocket+star-lord engine readiness autonomy
- **LOCK B** elrond audit autonomy
- **LOCK C** gandalf-as-subagent substrate-curation authority
- **LOCK D** gandalf canonical authoring authority
- **LOCK E** elrond ingest autonomy
- **LOCK F** drax MVP-discipline (load JSON + existing component layouts; no UI redesign)
- **LOCK G** Vercel auto-deploy on drax push
- **LOCK H** standard gandalf design-quality audit at workstream close (note-only)
- **LOCK I** seam-owner authority for cross-cycle scope amendments
- **LOCK J** bounded-scope architectural amendment authority (ADDITIVE-ONLY discipline)

### Locks K-P (NEW for EAA chain — see wave-state file § 1 for full detail)

- **LOCK K** engine schema design authority (rocket + elrond + star-lord; ADR-004 MIGRATION per cross-seam touch)
- **LOCK L** WS1A.4-lite LLM prompt design authority (gandalf-as-subagent; escape clause = 2+ Gate-2 BLOCKs → Matt aesthetic judgment)
- **LOCK M** R8 + cosmological_vocabulary retirement scope (Stage 1 skip-flag pattern immediate; Stage 2 code removal deferred)
- **LOCK N** first kit-space-expansion generation parameters (n_kits=20-30; no Matt-touch required)
- **LOCK O** drax + engine page reframe MVP-discipline (NO new UI components; NO chernoff celestial body UI)
- **LOCK P** MM-P1-independence (EAA chain proceeds independently of MM-P1 design session)

### Escape clause (7 items)

KR escalates to Matt for: (1) engine architectural changes BEYOND § 3 scope, (2) WS1A.4-lite prompt BLOCK after 2+ iterations, (3) generation output quality substantively below expectations (>10% non-grammatical), (4) MM-P1 surfacing engine-architecture-impacting decisions, (5) ADR-002 architectural-commitment-tier scope changes, (6) cross-seam contract SEMANTIC changes, (7) strategic direction questions OUTSIDE EAA chain scope.

---

## 4. Wave purpose

Operationalize the Season-Archive Realm-Expansion canonical commitment at the engine + drax layer. The kit-space-expansion infrastructure replaces per-season class generation as the engine's content-emission unit. Each kit emerges from substrate inputs (primary + cultural-tradition + period + chain composition + T4 + WS1A.4-lite per-skill flavor judgment) and lands in the continuous kit space.

**Architectural shifts:**

1. **R8 inverted-mode theme coalescence + cosmological_vocabulary slot-fill** — retire via Stage 1 skip-flag pattern (LOCK M); old code preserved for legacy needs; deferred-cleanup workstream removes later
2. **Per-skill LLM flavor-or-canonical naming** — WS1A.4-lite (LOCK L); Q18 vocabulary consumed at per-skill flavor decision; replaces per-season cosmological vocabulary slot-fill
3. **Kit-space output schema** — per-kit JSON entry (NOT per-season manifest); additive schema extensions per LOCK K; backward-compatible
4. **Kit-space chronicle** — parameter expansion event records per canonical record § 3.4
5. **Cross-seam contract amendments** — ADR-004 MIGRATION.md per cross-seam touch
6. **First kit-space-expansion generation fire** — 20-30 kits per LOCK N
7. **Drax + engine page MVP reframe** — consume kit-space output via existing components per LOCK O

**Substrate preserved:** WS1A.Q18 Architecture A LOCK unchanged; Q18 vocabulary IMMUTABLE; BC axes unchanged; canonical-7+1 catalog unchanged; substrate composition policy semantic unchanged.

---

## 5. Phase-by-phase scope summary

### Phase 1 — Engine architectural amendment (parallel fire)

**EAA-1** WS1A.4-lite implementation — star-lord (LLM prompt + per-skill judgment integration) + rocket (engine skill-naming pipeline integration) + gandalf-as-subagent (prompt template authoring per LOCK L) — ~3-5 sessions

**EAA-2** Engine skip-flag pattern for R8 + cosmological_vocabulary retirement — rocket + star-lord per LOCK M Stage 1 — ~1-2 sessions

**EAA-3** Kit-space output schema (additive) — rocket + elrond + star-lord per LOCK K; ADR-004 MIGRATION.md per cross-seam touch — ~2-3 sessions

**EAA-4** Kit-space chronicle infrastructure — elrond + star-lord per LOCK K — ~1-2 sessions

Phase 1 PASS criterion: EAA-1 + EAA-2 + EAA-3 + EAA-4 all jack-ryan Gate-2 PASS.

### Phase 2 — First kit-space-expansion generation fire (sequential)

**EAA-5** First kit-space-expansion generation fire — KR + rocket + star-lord per LOCK N; 20-30 kits; WS1A.4-lite + skip flags + modern caster weapons in substrate — ~1-3 sessions

Phase 2 PASS criterion: EAA-5 Gate-2 PASS (generation output quality acceptable per LOCK L iteration discipline).

### Phase 3 — Drax + engine page MVP reframe (parallel)

**EAA-6** Drax MVP reframe (consume kit-space) — drax per LOCK O — ~2-4 sessions

**EAA-7** Engine page MVP reframe (chronicle kit-space-expansion) — drax + reincarnated-loadout per LOCK O — ~2-3 sessions (can parallel EAA-6)

Phase 3 PASS criterion: EAA-6 + EAA-7 Gate-2 PASS + Vercel preview deployed per LOCK G.

### Phase 4 — Wave-close

**EAA-8** Wave-close discipline — KR + gandalf design-quality audit + jack-ryan Gate-2 wave-close — ~1-2 sessions

EAA-8 = wave-close criterion; canonical record + ground-state § 1 update + strategic re-engagement signal to Matt.

---

## 6. Critique-pair coverage (jack-ryan)

**Gate-1 (DESIGN-MODE pre-fire review of KR-authored dispatches):**
- This wave-open dispatch — routed AT wave-open before Phase 1 fires
- Each EAA-N dispatch (EAA-1, EAA-2, EAA-3, EAA-4) — routed before respective phase fires
- Each subsequent EAA-N dispatch in Phase 2, 3, 4

**Gate-2 (DEV-MODE post-output review with BLOCK authority):**
- EAA-1 prompt iteration reviews (per LOCK L iteration discipline; 2+ BLOCK = Matt escape)
- EAA-2 skip-flag implementation post-PR
- EAA-3 kit-space schema spec
- EAA-4 chronicle implementation
- EAA-5 generation output quality (per LOCK N + LOCK L)
- EAA-6 + EAA-7 drax MVP outputs
- EAA-8 wave-close canonical write

Standard INFO / WARN / BLOCK verdicts apply per critique-pair-gate-protocol.

---

## 7. Cross-seam contract change? (Principle 6 gate)

**Answer:** YES — additive cross-seam contract changes per ADR-004 MIGRATION discipline.

**Cross-seam touches anticipated:**
- EAA-3 kit-space output schema (rocket → elrond → star-lord; engine-emit → ingest → output pipeline) — MIGRATION.md required
- EAA-4 kit-space chronicle (engine-emit → elrond-ingest) — MIGRATION.md required
- EAA-6 / EAA-7 drax consume kit-space output (star-lord output → drax consume) — MIGRATION.md required at drax-side consumption shape change

**Discipline:** all cross-seam contract changes are ADDITIVE per LOCK J + LOCK K; backward-compatibility preserved where possible. Semantic changes escalate per escape clause § 6.

**Round-trip:** each cross-seam contract change carries MIGRATION.md documenting old/new contract + backward-compat handling + consumer-side amendments.

---

## 8. Scope checklist (KR self-audit at wave-open)

- [x] Wave-state file initialized at `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- [x] Wave-open dispatch authored (this file)
- [ ] Jack-ryan Gate-1 routed pre-fire on wave-open
- [ ] Phase 1 EAA-N dispatches authored after wave-open Gate-1 PASS (in parallel)
- [ ] Phase 1 EAA-N Gate-1 reviews routed
- [ ] Phase 1 fire (parallel: EAA-1 + EAA-2 + EAA-3 + EAA-4)
- [ ] Auto-commit per established cycle-push pattern; auto-push per Matt 2026-06-02 explicit authorization

---

## 9. Out of scope (explicit non-goals for THIS chain)

- **MM-P1 specific UX** — chernoff celestial body Stages A-D; 3d art deck; sound dimension; VFX surfaces 1+2 (defer to MM-P1 design session per LOCK P)
- **Economic-veteran problem resolution** — deferred per canonical record § 5; gates on materials/trading scope
- **Realm Expansion content design** — gates on first Realm Expansion content design session
- **Underplayed-kit telemetry instrumentation** — gates on first kit-space-expansion telemetry data
- **Stage 2 R8 + cosmological_vocabulary code removal** — deferred to later cleanup workstream per LOCK M Stage 2
- **Existing season migration to kit space** — per canonical record § 6 Path α; existing seasons preserved as historical
- **WS1A.3 per-kit sub-element selection** — RETIRED per canonical record § 3.2 (per-skill flavor-or-canonical decision REPLACES per-kit sub-element framing)

---

## 10. Sustained-background-process discipline

Per hive-mind protocol § 3.2:
- Long-running sub-agents (EAA-1 prompt iteration, EAA-3 schema spec authoring, EAA-5 generation fire) fire in-background where supported
- KR monitors completion notifications without polling
- Chain proceeds phase-by-phase as workstreams complete and gates ratify

---

## 11. References

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`
- **Wave-state file:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- **Q18 vocabulary lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Ground-state oracle:** `canonical/00-ground-state.md` § 1
- **IA chain close-out resume framing:** `agentic_orchestration/gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md`
- **Pool.json v1.1 substrate:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
- **R8 inverted-mode pipeline (to retire):** `~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py`
- **canonical-7+1 catalog (preserved):** `~/Games/reincarnated-engine/src/reincarnated/foundation/elements.py`
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **GOVERNANCE / ADRs:** `agentic_orchestration/GOVERNANCE.md`
- **Critique-pair gate protocol:** `agentic_orchestration/operating-procedures/` + `reincarnated-critique-pair-gate-protocol` skill

---

## Completion record (appended at wave-close)

To be authored at EAA-8 wave-close. Will carry:
- Wave-close timestamp
- Each EAA-N PASS verdict
- All artifact paths landed
- Wave-state file CLOSED marker
- Pattern-set capture for downstream parameter-expansion cycles
- Cross-references to KR wave-close record + gandalf design-quality audit + canonical write
- Strategic re-engagement signal to Matt with state summary

---

**End of EAA chain wave-open dispatch. Awaiting jack-ryan Gate-1 PASS before Phase 1 fire.**
