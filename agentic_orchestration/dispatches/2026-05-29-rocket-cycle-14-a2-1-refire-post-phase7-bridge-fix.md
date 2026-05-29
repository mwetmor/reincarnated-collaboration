# DISPATCH — Rocket Cycle 14 A2-1 RE-FIRE (Phase A2 Dispatch 1 Re-Attempt; post A2-1-FIX)

**Authored:** 2026-05-29 (Mode A Phase A2 unattended cascade A2-1 re-fire; post gamora A2-1-FIX close)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** rocket (content generation seam; re-fire of original A2-1 season_001 production cascade)
**Pattern:** Pattern B sustained-execution (full LLM production cascade re-fire); same shape as original A2-1; expected ~10-60 min wall-clock based on INTERIM A2-1 (45.5s pipeline wall + LLM phase 5 + phase 7 acceptance)
**Expected effort:** ~10-60 min wall-clock (interim A2-1 ran in 45.5s sans phase 5 LLM; phase 5 cohesion judge LLM expected to add wall-clock + first real LLM cost spend toward $50 soft cap)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 Phase A2 cascade authorization + hive-mind decision-routing (Matt 2026-05-23 verbatim — in-scope re-fire after seam-owner bug fix) + R48.4 single-seam (gamora released; rocket firing alone)

---

## 0. CONTEXT (read first — 3 min)

### 0.1 A2-1 lineage (INTERIM FAIL → A2-1-FIX → RE-FIRE this dispatch)

| # | Dispatch | Status |
|---|---|---|
| A2-1 (INTERIM) | `2026-05-29-rocket-cycle-14-wave-5-season-001-production-fire.md` | ❌ INTERIM FAIL (0/18 emit; cross-seam import bug blocked Phase 7) — completion record appended; collab `26d4baa` + engine `7701096` |
| A2-1-FIX | `2026-05-29-gamora-cycle-14-a2-1-fix-phase7-bridge-import.md` | ✅ CLOSED (2-line absolute-import fix + bundled quality-vector ID fix; verification PASS) — engine `b0ed9fd` (fix + MIGRATION.md §v1.55) + `c08352f` (AGENT_STATE); collab `1313d79` (completion record); tag `gamora/v2.12-a2-1-fix-phase7-bridge-imports-1` |
| **A2-1 RE-FIRE (THIS DISPATCH)** | this dispatch | ⏳ PENDING — re-fire of season_001 PRODUCTION cascade with both fixes landed |

### 0.2 What A2-1-FIX landed (KR-verified per Disc #42a meta-observation 5)

**Primary fix** — `simulation/phase7_bridge.py` lines 196-197 changed from relative imports `.ability_schema` + `.skill_schema` to absolute `reincarnated.generation.ability_schema` + `reincarnated.generation.skill_schema`. Deferred-inside-function-body pattern preserved (no circular-import re-emergence; KR verified by reading file at lines 193-200). `Phase7SyntheticKit` now constructs `kit.skills=[primary_attack]` with magnitude=3000 + energy_cost=0.0.

**Bundled fix (Option B-1 per A2-1-FIX dispatch § 2)** — `simulation/wave5_season_orchestrator.py` `_derive_quality_vector()` strips `S1_` prefix from `kit_id` before `startswith()` filter. Root cause: `kit.character_id = "S1_{bc_cell_id}"` but gauntlet `legendary_id = "{bc_cell_id}_{chain_id}"`. Fix produces 57 encounter results matched per kit (vs 0 pre-fix). Quality vectors on A2-1 re-fire will be empirically meaningful, not uniform 0.5.

**Verification (gamora-attested + KR spot-check):**
- Static import `from reincarnated.simulation.phase7_bridge import Phase7SyntheticKit` resolves
- Skill construction smoke: kit.skills len=1 role=primary_attack PASS
- 9/9 `test_phase7_bridge.py` tests PASS
- Disc #11 grep `synthetic_mode` in `src/reincarnated/simulation/` = ZERO functional code
- Quality-vector fix verified against actual A2-1 gauntlet JSON (57 encounter results matched)

### 0.3 What this dispatch fires

**Re-fire the SAME Wave 5 season_001 PRODUCTION cascade as original A2-1, with both A2-1-FIX commits applied.** Engine HEAD at `c08352f` (post-fix); production pipeline now functional through Phase 7.

Pipeline (engine `~/Games/reincarnated-engine/`; same as original A2-1):

1. **Phase 2** — kit candidate generation (12 skills × 3 chains × 4 tiers; substrate weapon binding per SC-6b enrichment)
2. **Phase 3** — gauntlet simulation (R3-prime band lower-bound + T1 base-context amendment active; post-Phase-A1 state) — **quality-vector derivation NOW MEANINGFUL** (per bundled fix; not uniform 0.5)
3. **Phase 4** — archive insertion to `kit_archive.db`
4. **Phase 5** — **cohesion judge LLM calls FOR REAL THIS TIME** (SC-3 PRIMARY Pattern B Structured Output with Layer Tags; star-lord cost guard enforces $50 soft cap PROJECTION) — original A2-1 short-circuited at Phase 7 before this layer fired meaningfully
5. **Phase 7** — acceptance gate (≥12/18 kits emit threshold; **synthetic_kit skill construction NOW WORKS** per phase7_bridge fix)

### 0.4 Disc #42a framing-audit applied at dispatch consumption

KR's authoring already applied Q1-Q6 to this dispatch. Rocket should re-apply at consumption:

- **Q1 — load-bearing framing assumption:** "A2-1-FIX repairs the Phase 7 short-circuit + quality-vector signal; pipeline now produces meaningful Phase 7 emit count + Phase 5 LLM judge can exercise real cohesion-vs-AI-tell tradeoff"
- **Q2 — refutation evidence in scope:** gamora attestation + KR spot-check (engine file verified; tag landed; 9/9 phase7_bridge tests PASS); additional verification = the pipeline fires
- **Q3 — refutation surface-able cheaply:** yes — fire the pipeline; observe Phase 7 emit count
- **Q4 — measurement context match:** Phase 7 acceptance threshold is calibrated against D9 ratified close-criterion; same context as original A2-1
- **Q5 — calibration scope match:** ≥12/18 threshold per-season is D9 RATIFIED; scope-match
- **Q6 — semantic stability of "≥12/18 emit" + "Path α validated":** Path α is empirically validated at Phase 3 gauntlet sim layer (13/18 WR-bracket PASS at original A2-1). Phase 7 ≥12/18 = Path α validated at acceptance layer (post LLM cohesion judge). These ARE distinct measurements; rocket's attestation must cite Phase 7 (NOT Phase 3 proxy) for the architectural validation claim. This is the KR Disc #42a vigilance flag forward from original A2-1 interim.

If any framing refutes, SURFACE TO KR before pipeline fire.

### 0.5 Disc #42a vigilance flag forward (load-bearing for re-fire attestation)

Rocket's original A2-1 interim attestation conflated "Phase 3 13/18 WR-bracket PASS = Path α validated" with the architectural claim. Phase 3 is a proxy, not the full signal. Phase 7 acceptance — post-LLM-cohesion-judge — is the full architectural validation gate.

**Required attestation forward (re-fire completion record):**
- Cite Phase 7 emit count explicitly (e.g., "11/18 acceptance PASS" or "13/18 acceptance PASS")
- Cite cohesion judge LLM exclusion count separately (e.g., "Phase 5 LLM excluded N kits as low-cohesion or high-AI-tell")
- Cite Phase 3 WR-bracket PASS as gauntlet-sim layer proxy (informational; not the architectural claim)

The architectural claim "Path α v1 validated at Phase 7 acceptance layer" is established ONLY when Phase 7 emit ≥12/18 AFTER LLM exclusions.

---

## 1. THE TASK

**Re-fire Wave 5 season_001 PRODUCTION cascade end-to-end against current engine state (HEAD at `c08352f`).**

### 1.1 Pre-flight (REQUIRED before pipeline fire)

1. **Disc #48 R48.5 vm_stat check:** confirm > 1 GB free + reclaimable (KR pre-flight at session-start showed ~2.8 GB available; verify still holds post-A2-1 + A2-1-FIX work)
2. **Disc #48 R48.4 single-seam confirm:** gamora sub-agent released; only this dispatch's rocket is running
3. **Engine state confirm:** HEAD at `c08352f` (gamora A2-1-FIX AGENT_STATE); A2-1-FIX commit at `b0ed9fd`; tag `gamora/v2.12-a2-1-fix-phase7-bridge-imports-1` resolves
4. **Verify the fix landed:** `python -c "from reincarnated.simulation.phase7_bridge import Phase7SyntheticKit; k = Phase7SyntheticKit('test_kit', 'fire', 'bc_test'); assert len(k.skills) == 1"` should pass (rocket's smoke before pipeline fire)
5. **Star-lord LLM cost guard active:** verify cost-tracking wired + projects against $50 soft cap (this re-fire IS the first real LLM spend; pay attention)
6. **Prior INTERIM A2-1 phase outputs:** existing `phase2_*` / `phase3_*` / `phase4_*` / `phase5_*` / `phase7_*` JSONs in season-001 dir are from the INTERIM run (committed `26d4baa`). Rocket's call: archive to subdir (e.g., `a2-1-interim-pre-fix/`) for clarity, OR overwrite (interim is preserved in git history regardless)
7. **kit_archive.db:** present at `cycle-14-wave-5-season-001/kit_archive.db`. INTERIM run added 18 ACCEPTED kits. Rocket's call: clear and re-populate (recommended for clean re-fire) OR append (sequence the fresh kits alongside interim — but this complicates A2-2 Gate-2 review; recommend clear-and-re-populate)

### 1.2 Pipeline fire

Run the full season_001 production pipeline (same orchestration as original A2-1):
- Phase 2 → kit candidate gen
- Phase 3 → gauntlet sim (quality vectors NOW MEANINGFUL post bundled fix)
- Phase 4 → archive insert
- Phase 5 → **cohesion judge LLM calls (REAL LLM spend; star-lord cost guard projects + emits)**
- Phase 7 → acceptance gate (synthetic_kit skill construction NOW WORKS post primary fix)

**LLM cost guard surface conditions (star-lord in-process):**
- Track per-LLM-call cost cumulative across season_001
- Project cumulative cost for season_001 + extrapolate to 3-season cascade
- **If projected approach hits $50 across all 3 seasons → SURFACE TO KR via interim completion-record append** (cascade decision: continue / pause / Matt cap-extension)
- **Hard-halt threshold:** projected > $60 (20% overshoot) → halt cascade + surface IMMEDIATELY

This is the FIRST production fire that meaningfully spends LLM budget. The cost projection captured at A2-1 re-fire close becomes the EMPIRICAL baseline for 3-season cascade projection accuracy.

### 1.3 Output telemetry

Same shape as original A2-1 (per § 1.3 of original dispatch). Phase 5 cohesion-judge LLM telemetry per SC-3 PRIMARY (Structured Output with Layer Tags) — emit-prompt + response + per-layer cohesion verdicts + total LLM cost. Cross-Character Diversity Audit per SC-3 DETECTION (informational; not blocking A2-1 close).

### 1.4 Acceptance criterion (D9 ratified per-season)

- **≥12/18 kits emit** at phase 7 acceptance
- Phase 7 emit count explicitly cited (NOT Phase 3 13/18 proxy)
- Phase 5 cohesion judge LLM exclusion count explicitly cited
- LLM cost cumulative captured + extrapolation to 3-season projection
- Disc #11 grep `synthetic_mode` ZERO functional code (re-verify; bundled fix touched simulation/ — re-confirm regression-free)
- Cross-seam round-trip (production cascade IS the round-trip)
- Auto-commit per CLAUDE.md addendum
- Do NOT push — KR fires push after A2-2 Gate-2 PASS

### 1.5 Report format (Completion record append)

Append a `## Completion record` section to this dispatch with:

1. **VERDICT** — single line: "A2-1 re-fire season_001 production ≥12/18 emit at Phase 7 acceptance — PASS (Phase 7 emit count: X/18; LLM exclusions: Y)" OR "FAIL with diagnosis + framing-audit Q1/Q2/Q3 applied"
2. **Phase 7 emit count** — explicit X/18 figure
3. **Phase 5 LLM cohesion judge** — per-kit cohesion verdict (PASS / EXCLUDED + reasoning excerpts); total LLM cost; cost projection to 3-season
4. **Phase 3 gauntlet sim** — informational proxy (WR-bracket PASS count + quality-vector distribution NOW MEANINGFUL)
5. **AI-tell detection sub-audit** — Cross-Character Diversity per SC-3 DETECTION
6. **Disc #11 grep verification** — `synthetic_mode` ZERO functional code (re-confirm)
7. **Telemetry output paths** — all written JSON files
8. **Engine + collab commits + tag** — rocket commits + tag (`rocket/v?-season-001-re-fire-1` or seam convention)
9. **Disc #42a framing-audit self-verification** — Q1-Q6 enumerated at dispatch consumption + meta-observation 5 at attestation (verify artifact against report)
10. **Disc #42a Q6 vigilance forward** — confirm attestation cites Phase 7 result (not Phase 3 proxy) for architectural validation claim
11. **Any anomalies surfaced** during pipeline fire

---

## 2. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**No** — re-fire of existing pipeline; A2-1-FIX is intra-engine bug fix (no cross-seam contract change). Round-trip clause: production cascade IS the round-trip (rocket → gamora → star-lord → phase 7).

---

## 3. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal:** empirically validate Path α v1 architecture at the Phase 7 acceptance layer (post-LLM cohesion judge) by re-firing season_001 production with the import bug + quality-vector ID bug both repaired. This is the FIRST production fire that exercises the full cascade through LLM cohesion judge AND phase 7 emit acceptance — the architectural validation gate Path α was designed to satisfy.

**Refutation conditions:**
- Phase 7 emit < 12/18 — refute = full pipeline re-fire produces empirical signal; A2-1-FIX is verified clean per gamora attestation + KR spot-check
- Alternative execution Y serves the quality goal better — refute = re-firing same pipeline is the minimal-additional-work path to validation
- Acceptance criteria can pass without advancing the quality goal — refute = ≥12/18 emit at Phase 7 IS the architectural validation claim
- Dispatch framing pre-commits to a decision Matt has not ratified — NO (in-scope re-fire after seam-owner bug fix)
- Dispatch introduces pre-authored taxonomy without justification (#41 candidate) — N/A
- Dispatch introduces scaffold value not flagged as pending-decision (#40) — N/A

If any refutation condition triggers, SURFACE TO KR before pipeline fire.

---

## 4. OUT OF SCOPE

- ❌ Any engine code change (A2-1-FIX is closed; this is re-fire of fixed code)
- ❌ Path α architectural amendment (Path α architecture is what's being validated)
- ❌ Two-layer T4 architectural amendment
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Doc 48 class-roster A/B comparison execution (A2-5 scope; gandalf)
- ❌ Disciplines #41/#44/#45/#46 batched canonical-write (A2-6 scope; jack-ryan)
- ❌ Cross-season (A2-3/A2-4) production fire (this is season_001 only)
- ❌ Jack-ryan Gate-2 review (A2-2; fires after this dispatch closes)
- ❌ Matt v1 tag ratification (A2-7)
- ❌ Pushing without KR coordination
- ❌ Parallel sub-agent fan-out under R48.4

---

## 5. RISKS + COMPLICATIONS

- **LLM cost projection accuracy:** this is the first run that meaningfully spends LLM budget. The cost-per-season projection is OBSERVED here; extrapolation to 3-season may surface the $50 cap concern. If season_001 alone costs > $17 (1/3 of cap), 3-season is at risk.
- **Phase 5 LLM verdict-vs-AI-tell tradeoff (untested at production scale):** SC-3 PRIMARY Pattern B Structured Output with Layer Tags has been research-validated but NOT exercised at production scale in this seam. May surface LLM-call-failure modes or unexpected exclusion patterns.
- **Phase 7 emit < 12/18 even post-fix:** if LLM exclusions are aggressive (e.g., 7-8 exclusions), Phase 7 could fall below threshold. Surface IMMEDIATELY with diagnosis.
- **Phase 3 WR-bracket regression post bundled fix:** the `_derive_quality_vector()` fix changes downstream signal but NOT upstream gauntlet sim. WR-bracket count expected stable at 13/18. If it shifts, surface.
- **Disc #48 R48.5 mid-run RAM pressure:** if vm_stat < 500 MB available mid-run, pause + surface.
- **Disc #42a Q6 attestation discipline:** rocket MUST cite Phase 7 result (not Phase 3 proxy) for architectural validation claim. Self-audit at completion record authoring.

---

## 6. URGENCY + SEQUENCING

**Fires AFTER A2-1-FIX close; precedes A2-2 Gate-2.** R48.4 single-seam preserved (gamora released; rocket firing alone).

A2-1 RE-FIRE PASS → KR fires A2-2 (jack-ryan + gandalf critique-pair Gate-2 Pattern E autonomous-ratification).

A2-1 RE-FIRE FAIL → KR surfaces to Matt with framing-audit Q1/Q2/Q3 applied (FAIL-after-fix would be a MATERIAL architectural concern, not contained like the import bug).

---

## 7. SURFACING-TO-KR PROTOCOL

Append completion record (interim OR final) at any of:

- ✅ Season_001 ≥12/18 emit at Phase 7 + LLM cost within season-budget → normal close (KR fires A2-2)
- ⚠️ Phase 7 emit < 12/18 → SURFACE IMMEDIATELY with framing-audit Q1-Q3 applied (this would be a material architectural concern; routes to Matt)
- 🚨 LLM cost projection approach $50 cumulative across 3 seasons → SURFACE IMMEDIATELY (KR routes to Matt for cap-extension election)
- 🚨 LLM cost hard-halt $60 overshoot → SURFACE IMMEDIATELY + halt
- ⚠️ Disc #11 grep returns `synthetic_mode` functional code → SURFACE IMMEDIATELY (regression from A2-1-FIX)
- ⚠️ Disc #48 R48.5 mid-run RAM pressure (< 500 MB) → pause + SURFACE
- ⚠️ Disc #42a framing-audit refutes pre-imposed assumption → SURFACE IMMEDIATELY before pipeline fire
- 🚨 Substantial unexpected failure mode → SURFACE IMMEDIATELY

---

## 8. REFERENCES

- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-wave-5-season-001-production-fire.md` — original A2-1 dispatch + INTERIM FAIL completion record
- `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-fix-phase7-bridge-import.md` — A2-1-FIX dispatch + completion record (primary + bundled fix)
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Path α v1 engine readiness gate (validated at Phase 3 layer per A2-1 INTERIM; full validation pending this re-fire's Phase 7 result)
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Wave 5 state (A2-1 INTERIM RESULT + A2-1-FIX in-flight sections; this re-fire updates to A2-1 RE-FIRE)
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Disc #42a Q1-Q6 architectural argument
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md` — SC-3 PRIMARY pattern + DETECTION
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` — A2-1-FIX file (verified at lines 195-200)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — bundled fix file
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.55 — A2-1-FIX migration notes
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` line 3536 — amended close-criterion LOCKED
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11/#18/#21/#22/#39/#42a/#43/#48 active
- Engine HEAD: `c08352f` (gamora AGENT_STATE post-A2-1-FIX); tag `gamora/v2.12-a2-1-fix-phase7-bridge-imports-1`

---

**KR signature:** authored per Phase A2 unattended cascade authorization + R48.4 single-seam (gamora released; rocket alone) + Disc #42a meta-observation 5 self-vigilance (A2-1-FIX artifact verified against gamora attestation: phase7_bridge.py lines 196-197 absolute imports confirmed + tag landed + 9/9 tests PASS attested) + auto-commit per CLAUDE.md addendum + Disc #42a Q6 vigilance flag forward (attestation MUST cite Phase 7 result, not Phase 3 proxy).

This dispatch is the cheapest empirical refutation of "does A2-1-FIX deliver ≥12/18 emit at Phase 7 acceptance layer (with REAL LLM cohesion judge exercised)?" — re-fire of original A2-1 pipeline with both fixes landed.

A2-1 RE-FIRE PASS = Path α v1 architecturally validated at Phase 7 acceptance layer + unblocks A2-2 Gate-2 (Pattern E autonomous critique-pair) → cascade continues toward Cycle 14 v1 MVP D9 close.
