# Dispatch — 2026-07-03 — rocket → gamora — W2 pairing layer (DEMO-READINESS UNATTENDED RUN)

**From:** knight-rider
**To:** rocket (Phase 1: strategy classes + wiring) → gamora (Phase 2: cert), serial
**Approved by:** Matt 2026-07-03 (G1a: pairing layer rides the run) — design-OPEN, no Matt gate; **Gate-1 critique-pair on THIS dispatch required before fire** (MASTER protocol)
**Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** — §2 G1, §3 W2, §7 degrade row. Phase-3 authority: `canonical/reap-die-rise-engine/proxy-pairing-q6-q7-2026-07-02.md` **v2 (RATIFIED)** — partition · 65-pair matrix · 14×3 pools · P1–P7 · derivation rules i–vi.
**Estimated effort:** two serial sessions (rocket, then gamora)
**gates-on:** `W0.classifier · W0.2-type-decl-check · W0.fixture · Gate-1-pair-CLEAR`
**Failure policy (§7, load-bearing):** W2 stall → **degrade, never halt the emission**: W3 fires singleton-only (Phase-1 η members live; CONVERGENCE + DUAL_PROXY η-gated 0.0 — that config is smoke-gated green in W0 regardless of your state). CONVERGENCE/DUAL land as a named follow-up if you stall.

## Context

Phase 3 of the proxy-T4 program: CONVERGENCE + DUAL_PROXY enter the shipping family. Phase-1/2 precondition MET (B1-REBASE closed: `40e351e` + `67fc0a9`). The ratified pairing spec is the complete design authority — this dispatch adds no design; it wires + certifies.

## Required reading before starting

- Pairing spec v2 (FULL authority: partition, matrix, pools, P1–P7, rules i–vi — incl. (v) labeled inheritance + (vi) single visual identity)
- Proxy-T4 spec v3 (family membership + gates) · B1-REBASE completion records (both phases)
- Run spec v1.1 §3 W2 + §7 · decisions-log `a10a695` (Q6/Q7 six exception rows registered)
- W0 returns: rocket's classifier + 2-type-decl evidence + CONVERGENCE fixture

## Math-before-code

gamora Phase 2: magnitude derivation math note per the B1-REBASE method (A2/A3/A5/A6 carry; seeds 53M+; Disc #18/#24 discipline — single-parameter isolation on any swept magnitude; #1.2 code citations).

## Cross-seam contract change? (Principle 6 gate)

CONVERGENCE/DUAL_PROXY kit emission shape (paired decls, labeled inheritance fields) reaches the bundle → drax-consumed.
**Round-trip smoke REQUIRED (rocket Phase 1):** a CONVERGENCE fixture kit through the emit path → assert paired-decl fields + inheritance labels present at the bundle boundary. MIGRATION.md before tags.

## Scope

**Phase 1 — rocket** (`gates-on: W0.classifier · W0.2-type-decl-check · W0.fixture · Gate-1-pair-CLEAR`):
- [ ] CONVERGENCE strategy class per matrix derivation (65 valid pairs; deterministic; rules i–vi)
- [ ] DUAL_PROXY strategy class per 14×3 pools + P1–P7 selection principles
- [ ] η wiring: both members offerable to eligible kits (family gates per proxy-T4 spec v3); FAMILY_MAX_ONE respected via the W0 F-f consumer
- [ ] Labeled inheritance (rule v) + single visual identity (rule vi) realized in emitted shape
- [ ] Round-trip smoke + MIGRATION.md · Tag: `rocket/v-demo-run-w2-pairing-1`

**Phase 2 — gamora** (`gates-on: W2.phase1`):
- [ ] Magnitude derivation + cert for both members (A2/A3/A5/A6 method carry; seeds 53M+)
- [ ] **E4 STRIKER×ECHO sim-cost assessment** (Gate-1 fold, jack-ryan #2; pairing spec §4/E4): price the sim cost FIRST; if deferred, the 2 affected pairs carry a **named prerequisite — not a silent skip**
- [ ] Fixture cert on the W0 CONVERGENCE fixture (fixture-only; never ships)
- [ ] Boundary assertions (F-series carry as applicable) · math note first
- [ ] Tag: `gamora/v-demo-run-w2-pairing-cert-1`

## Quality criterion (OP §3.11)

**Game-quality goal this dispatch serves:** G1 — CONVERGENCE kits exist in the demo roster pool (§8 mandates ≥1 if W2 lands); paired-proxy builds are legible (labeled inheritance, single silhouette) so the player reads WHAT merged and WHY it's strong.

**Refutation conditions** (surface before executing if any apply):
- The W0 2-type-decl check filed a gap (CONVERGENCE kits can't exist) — halt this dispatch, degrade path governs
- Any pair the matrix derivation produces that violates a Matt-ruled exception row (E0–E5)
- Acceptance could pass with η offering a pair no emitted kit can draw (vacuous wiring)
- Anything here requires re-opening the ratified pairing spec (design is CLOSED; wiring only)

## Acceptance criteria

- [ ] Both strategy classes live; matrix/pools byte-match the ratified spec tables
- [ ] Exception rows E0–E5 respected (test-pinned)
- [ ] gamora cert PASS both members (or halt-loud → degrade path + named follow-up)
- [ ] E4 sim-cost assessed OR the 2 affected pairs filed as a named prerequisite (never silent)
- [ ] Round-trip smoke at bundle boundary
- [ ] MIGRATION.md before tags

## Out of scope

- PROXY_INVERSION (deferred-by-ruling; η never offers it)
- Re-deriving or amending the pairing design (RATIFIED — wiring only)
- The emission run (W3) · singleton smoke (W0, rocket — already sequenced)

## References

- Pairing spec v2 · proxy-T4 spec v3 · run spec v1.1 §3 W2/§7 · B1-REBASE `40e351e`/`67fc0a9` · decisions-log `a10a695`

---

## Gate-1 record (critique-pair — CLEARED 2026-07-03)

**jack-ryan DESIGN-MODE: ENDORSE-WITH-FOLDS** (verdict relayed by KR, parallel read-only pass; attribution: jack-ryan):
- #1 [AMEND→affirmed] `Gate-1-pair-CLEAR` token is legitimate dependents-declare usage (this dispatch IS the Gate-1 target) — token retained.
- #2 [AMEND→FOLDED above] E4 STRIKER×ECHO sim-cost must be priced in Phase-2, or the 2 affected pairs carry a named prerequisite (pairing spec §4/E4; Disc #24). Folded into Phase-2 scope + acceptance.
- #3 [NOTE] byte-match + E0–E5 test-pin acceptance is non-vacuous — no change.
- Degrade path, ADR-004/Principle-6, framing-audit (#23): all endorsed clean. Batched registration `a10a695` confirmed on disk (decisions-log line 4723).

**gandalf design-track: ENDORSE** (5 findings, all [NOTE], no folds): wiring-only fidelity confirmed (every scope line traces to a ratified table); legibility rules v/vi carried first-class into the round-trip smoke (fails if labels absent); fixture never-ships fence intact; quality criterion matches run-spec §8's mandatory CONVERGENCE row; vacuous-wiring refutation condition is the sharpest guard. No thematic drift; loop-discipline preserved via matrix byte-match.

**KR disposition: Gate-1-pair-CLEAR ✓** — dispatch fires when the three W0 rocket returns (classifier · 2-type-decl-check · fixture) close.

---

## Completion record — Phase 1 (rocket) — PASS — 2026-07-03

**Tag:** `rocket/v-demo-run-w2-pairing-1` — engine commit **`6a7190b`** (push HELD; KR pushes at closeout). Built on W0 `e57b9d8`; engine main head was `87c47a6`.

**Both strategy classes: PASS.**
- **CONVERGENCE** (`mechanic_alteration.ProxyConvergenceStrategy`): gates on exactly-2-cross-family-valid-65 decls; emits the deterministically-derived merge (rules i–vi) with rule-v labeled inheritance + rule-vi single visual identity. Matrix in NEW `generation/proxy_pairing_layer.py`.
- **DUAL_PROXY** (`mechanic_alteration.DualProxyStrategy`): gates on exactly-1-pool-keyed type (entity-axis, T4_active only); emits `compatibility_pool` + `second_type` + `resummon_mode:single_action_both` (P7) + `independent_operation:true` (E3). 14×3 pools in `proxy_pairing_layer.py`.
- Both added to `PROXY_T4_FAMILY` → offerable via `select_proxy_t4` / `rank_proxy_t4_family` (spec §4 η wiring).

**Byte-match proof method:** the tables are TRANSCRIBED from the ratified spec, and the counts are DERIVED not hand-typed — `proxy_pairing_layer.py` import-time asserts: 15 merge classes over exactly C(6,2)=15 family-pairs; `VALID_CONVERGENCE_PAIRS` ENUMERATED (iterate C(14,2), strike same-family + E1/E2/E5) and asserted == 65; 14 pools each 3 members, each import-asserted cross-family vs its primary. A spec drift breaks import. Plus `tests/test_proxy_pairing_layer.py` (26 tests) pins name-templates, the six ratified examples legal, and the ratified pool rows order-preserved.

**E0–E5 pin evidence** (`tests/test_proxy_pairing_layer.py::TestExceptionRows` + `TestConvergenceMatrixByteMatch`): E0 partition (W0 asserts, reused); E1 golem/bodyguard×shadow INVALID; E2 ONLY terrain_anchor×shadow of ATTENDANT×ECHO (warcry/conduit×shadow struck); E3 passive_fighter×terrain_anchor ∈ CONVERGENCE-65 AND ∈ passive_fighter's DUAL pool (independence, not exclusion); E4 exactly-2 STRIKER×ECHO sim-cost pairs, flag carried in the merge; E5 every fragile_escort cross-family pair struck (loop over all cross-family others).

**η eligibility + non-vacuity:** CONVERGENCE offered only to exactly-2-cross-family-valid-65 kits; DUAL only to exactly-1-pool-keyed kits (T4_active). Non-vacuity SHOWN: the W0 fixture (golem_construct×autonomous_caster, valid-65 class-1 "Juggernaut") is drawable — CONVERGENCE η=0.679 competes (SOVEREIGNTY edges it at 0.704 on that full-body-singleton shape — both legitimate); a 1-type volatile_emitter kit draws DUAL (η=0.615, pool `[trap_mine, resource_conduit, delayed_position_shadow]`). Refutation guarded: an E1 pair (golem×shadow) NEVER draws CONVERGENCE (η=0.0, test-pinned); solo → None.

**Round-trip smoke:** `generation/notes/w2_pairing_roundtrip_smoke_2026_07_03.py` — **6/6 GREEN**. W0 CONVERGENCE fixture → `build_proxies_surface` → `select_proxy_t4` → bundle-shape dict (mirrors `PlayerClassV2.to_dict` `proxies` + `t4_alteration_output`); asserts paired-decl fields + rule-v/vi labels PRESENT at the boundary. Acceptance-grade confirmed by negative-mutation: stripping the labels FAILS the boundary assert (labels are load-bearing, not decoration).

**MIGRATION:** `generation/MIGRATION.md` — new [2026-07-03] W2 entry (bundle shape gains paired-decl sub-fields inside `t4_alteration_output.strategy_params`; ADDITIVE — drax renders `inherited_from_a/_b` + `single_visual_identity` for G1 legibility; star-lord no-action; gamora Phase-2 certs magnitudes + E4). MIGRATION written BEFORE the tag.

**Refutation conditions checked (Quality Criterion + math-note §5):** NONE fired. W0 2-type-decl check filed no gap; the matrix strikes all E1/E2/E5 pairs (test-pinned, cannot produce a struck pair); acceptance is non-vacuous (an emitted candidate draws each member); no ratified-spec re-open (transcription + ratified derivation rules only).

**Tests:** 95 PASS (pairing 26 + proxy-strategies 69 + catalog); two pre-existing strategy tests updated to the scan-gate ABC contract. two-layer/cycle13 t4 174 PASS. W0 smoke re-run 28/28 GREEN (6e/6f inverted from "η-gated 0.0" to "LIVE" — documented supersession, the singleton-only baseline is now W2-activated; solo/singleton invariance preserved by decl-shape gates). `test_cycle12_layer6_t4_wireup` 12-fail = PRE-EXISTING (SkillTreeGenerator retirement), confirmed identical on baseline via stash round-trip, NOT this work.

**Handoff to gamora Phase 2:** magnitude derivation + cert (A2/A3/A5/A6; seeds 53M+; PROVISIONAL anchors HP=avg×1.2 / damage=sum×0.8 / class-8=70/70); **E4 STRIKER×ECHO sim-cost assessment** (the 2 flagged pairs — price first, or file the named prerequisite); W0 CONVERGENCE fixture cert (AQ1). Symbols to consume: `proxy_pairing_layer.{VALID_CONVERGENCE_PAIRS, STRIKER_ECHO_SIM_COST_PAIRS, DUAL_POOLS, derive_convergence_merge}` + `mechanic_alteration.{ProxyConvergenceStrategy, DualProxyStrategy, select_proxy_t4}`. — rocket, 2026-07-03.
