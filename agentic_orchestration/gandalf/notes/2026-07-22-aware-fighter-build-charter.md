# Aware-Fighter Run — BW-1 Build Charter (Reader stack upstream)

**Author:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat), 2026-07-22 — under Matt's verbatim ruling
**"Yes, push the reader stack upstream"** (ledger **L-22**; run-authorization lineage **L-21**, Matt
verbatim *"It lands, let's test out the geometry aware fighter"*).
**Decision substrate:** conductor architecture synthesis + legolas Mode A confirmatory sweep
(`agentic_orchestration/legolas/notes/2026-07-22-game-combat-ai-landscape-modeA.md`, commit `14fc8539`).
**Executor:** named-**gamora** (seam owner, `simulation/`). **Reviewer:** jack-ryan **Gate-2** on the
engine delta — this wave is PRODUCTION ENGINE CODE, full build discipline (unlike the W3/W3′
notes-side runners).
**Relationship to Tier-3:** Tier-3 run COMPLETE (L-20). BW-1 is the aware-fighter run's build wave;
the ablation GATE is NOT this wave (it follows Gate-2 via prereg → check → freeze → execute).

---

## §1 — The architecture (pinned)

1. **Decision layer = utility-scored considerations** feeding exactly two decisions: **target choice**
   and **movement intent**. Considerations are DATA (a scored, weighted list, config-selectable
   per-run), not code branches — the consideration set must be swappable without touching the
   decision code path.
2. **Exposure/influence map** — a lightweight geometry read computed from readable mob state
   (`x, y, threat_tier, archetype_tag, preferred_behavior`); feeds the geometry considerations.
   Per-decision computation is acceptable (per-tick only if cheap); batch economics baseline is
   ~17 ms/fight — the map must not blow this up by more than a small integer factor.
3. **Execution = existing movement/steering intents** (approach / hold / reposition). No pathfinding
   rewrite, no navmesh work.
4. **THE ABLATION PROPERTY (load-bearing — the reason this architecture was chosen):** the
   formation-**BLIND** policy is the SAME code path with the consideration set reduced to
   `{distance}` — nearest-first as a degenerate utility function. Aware-vs-blind must differ ONLY in
   consideration-set contents. **No dual code paths, no legacy branch kept alive behind a flag.**
5. **Out of scope this wave:** behavior trees (boss-phase future) · any learned policy · mob-AI
   changes · formation-builder changes (homogeneous COMMON-4 stands for lap 1) · role-heterogeneity
   in packs (lap 2, formation-side) · time-series/texture metrics (fork-(a) territory).

## §2 — Deliverables

1. **Policy seam.** Extract target selection (`spatial_engine.py:1338` —
   `min(targets, key=lambda t: attacker.distance_to(t))`) and movement intent (~lines 3500–3920)
   into the decision layer. **Skill selection (`_select_player_skill_v2`, line 2036) stays OUTSIDE
   the policy seam this wave** — energy-type branching untouched; red-flag if entanglement forces
   otherwise (stop-and-report, do not improvise a wider refactor).
2. **Considerations architecture.** Scored considerations with weights; BLIND set = `{distance}`
   reproducing current behavior; AWARE **candidate** set = geometry reads computable from the
   substrate (candidates: exposure/incoming-threat density, crossfire/arc overlap, cluster density,
   lane/corridor pressure, escape-gradient). **Gamora PROPOSES the computable candidate list in the
   math note; the GATE set is pinned at prereg by conductor + Matt — not in this wave.**
3. **Equivalence battery — THE WAVE'S HARD GATE.**
   - **BEFORE any refactor:** rerun the W3′ 256-fight set (32 cells × {matched-baseline, encounter}
     × 4 seeds {20260722–25}) at current engine HEAD via the legacy path; record per-fight metric
     triple (mobs_killed / total_aoe_hits / player_damage_total) + a per-decision trace (tick,
     chosen target id, movement intent). The W3′ runner + seal encode the exact compositions:
     `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-gate.py` + `…-pregate-seal.json`
     + `…-gate-output.json` — reuse their cell/seed/parity logic to reproduce the fights exactly.
   - **AFTER the refactor:** same 256 fights via the policy seam running BLIND (`{distance}`).
   - **Standard:** bit-equal metric triples per fight AND decision-trace equality. **Any mismatch ⇒
     red-flag STOP + report** (including RNG-stream divergence with provably identical decisions —
     report it as its own class; conductor rules on the substitute standard). No tolerance bands,
     no silent acceptance. This battery is the no-confound guarantee: blind ≡ current fighter,
     behaviorally proven, so the future gate's margin is purely the value of the added reads.
4. **Damage-intake metric.** Add player damage-TAKEN capture to `SpatialFightResult`
   (`spatial_telemetry.py:191–340` — field currently absent; the 1D `FightResult.a_damage_taken` is
   the precedent) and wire it through the batch runner. Scalar per fight; no per-tick series this
   wave.
5. **Tests.** Unit tests for the policy seam, considerations scoring, exposure map, and intake
   metric + the equivalence battery packaged as a repeatable test artifact.
6. **Build report.** `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw1-build-report.md`
   — as-built vs THIS charter, section by section, DRIFT-CRITIC-consumable; battery results included.

## §3 — Pins + discipline

- `player_gather_primitive` OFF in both blind and aware configurations (carried conductor pin).
- **Discipline #1 math-before-code:** exposure-map + utility-scoring math note lands at
  `agentic_orchestration/gamora/notes/` BEFORE decision-layer code.
- **#2 smoke** (small battery slice first) · **#3 no parallel regens** (sequential fights, one seed
  set) · **#11 empirical inspection** (verify, never assume — especially battery bit-equality).
- Engine writes confined to the gamora seam (`simulation/`); `corpus.db` untouched; no telemetry
  schema changes beyond the intake field.
- **Commit-never-push** (engine repo AND collaboration repo); stage ONLY own files by explicit path;
  verify `git diff --cached --stat` before each commit. Conductor holds the engine push until
  **Gate-2 PASS**.
- Red-flag semantics: stop-and-record, never improvise.

## §4 — What follows (NOT this wave)

Gate-2 PASS ⇒ prereg sheet for the ablation gate (gate consideration set + F3 metric + F4 bar
pinned; the Discipline #18 methodology/temperature consult feeds the bar; ARCHITECT open-questions
pass fires at that boundary) ⇒ jack-ryan check ⇒ freeze ⇒ named-gamora ablation execution
(aware-vs-blind on the 32-cell frame; the C2 seal device carries — blind arm sealed before any
aware fight) ⇒ verdict ⇒ review book.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22 — L-22, veto-open.
