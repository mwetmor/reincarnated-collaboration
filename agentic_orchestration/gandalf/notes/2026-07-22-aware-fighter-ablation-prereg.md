# Aware-Fighter Ablation Gate — Preregistration Sheet

**Author:** gandalf `RUN-CONDUCTOR` (SPEC-AUTHOR beat), 2026-07-22.
**Status:** **FROZEN VERBATIM (2026-07-22)** — Matt ruled all four pins (ledger **L-27**, verbatim:
*"P1 - Full 6-entry set / P2 - 10% / P3 - k=2 × seed-to-seed SD of the blind encounter-arm
aggregate intake / P4 - Both"*). Pins filled inline; struck alternatives retained for audit.
jack-ryan prereg check **PASS-WITH-CONCERNS** (`a9bb1886`) → C1+C2 WARN pins **folded** (§6
precedence rule; §2 auditable seal artifact; W3′ folding convention — no bar-parameter moves) →
freeze-beat re-verify **clean PASS** (`57d18520`: both pins PRESENT / MECHANICAL / CONSISTENT).
**POST-FREEZE EDITS VOID THE GATE.** Execution: named-gamora charter
(`2026-07-22-aware-fighter-ablation-execution-charter.md`). **Gate engine hash: `2f43045`**
(Gate-2 delta PASS `3f26b00b`; pushed).
**Lineage:** L-21 (*"It lands, let's test out the geometry aware fighter"*) → L-22 charter
(`2026-07-22-aware-fighter-build-charter.md` §4) → L-23 (*"Adopt both leans — C3 and D2 with the D3
floor"*) → BW-1 Gate-2 PASS-WITH-CONCERNS → L-25 BW-1.1 coherence slice (verified; light Gate-2
delta check in flight) → this prereg. **Discipline #18 methodology consult DISCHARGED:**
`agentic_orchestration/legolas/notes/2026-07-22-ablation-bar-calibration-modeA.md` + conductor
extraction `…/gandalf/notes/2026-07-22-blackdarken-extraction-bar-calibration-addendum.md`.

---

## §1 — The question and the arms

**Question:** does geometry awareness — the Reader stack's exposure-map considerations — measurably
improve the fighter's defensive outcome on the authored encounter frame, beyond the proven-equivalent
nearest-first baseline?

- **BLIND arm:** `BLIND_CONFIG = PolicyConfig(name="blind", weighted=(("distance", 1.0),))` — proven
  behaviorally ≡ the legacy fighter (BW-1 + BW-1.1 batteries: 256/256 bit-equal, triple + trace).
- **AWARE arm:** the gate consideration set (P1 below), same code path, config-only difference —
  the L-22 §1.4 ablation property is the no-confound guarantee. **Any engine-code difference between
  arms voids the gate.** Both arms run at ONE frozen engine commit: **`2f43045`** (Gate-2 delta PASS
  `3f26b00b`; pushed `a9e2bc7..2f43045`).

## §2 — Frame and seal

- **Frame:** the W3′ 32-cell set × 4 seeds {20260722, 20260723, 20260724, 20260725}, compositions
  reproduced via the battery harness cell/seed/parity logic
  (`…/gamora/notes/2026-07-22-aware-fighter-bw1-equivalence-battery.py` lineage).
- **[P4 — RULED: BOTH (Matt 2026-07-22, L-27)] Arm composition.**
  - **(a) BOTH compositions — ADOPTED.** matched-baseline AND encounter arms, 256 fights per
    policy arm (512 total). The encounter arm is the margin substrate; the matched-baseline arm is a
    built-in **specificity control** (geometry-sparse — AWARE should show ≈no margin there; a large
    baseline-arm margin signals a confound, not geometry value). Cost is trivial (~1 min compute).
  - ~~(b) Encounter-only~~ — struck at pin.
- **C2 seal (carried device; AUDITABLE-ARTIFACT PIN folded at prereg-check C2, jack-ryan
  2026-07-22 — W3′ §8 C2 lineage; no bar-parameter move):** the BLIND arm runs FIRST, complete.
  Its 256 per-fight records + the derived encounter-arm aggregate-per-seed means + `SD_seed` are
  written to a **seal-JSON, flushed to disk BEFORE the first aware fight fires** (W3′ precedent:
  `…-tier3-w3prime-pregate-seal.json`). The final **verdict JSON embeds that seal's md5**; any
  post-seal mutation of the blind record ⇒ **red-flag HALT, no verdict**. This makes
  "sealed before aware" a hash-checkable INVARIANT (DRIFT-CRITIC-confirmable independent of the
  aware outcome), not a sequence assertion. No peeking, no re-rolls.

## §3 — [P1 — RULED: FULL 6-ENTRY SET (Matt 2026-07-22, L-27)] The AWARE gate consideration set

Registry (BW-1/BW-1.1 as-built): `distance` (raw, BLIND-only) · `distance_normalized` · five
geometry reads: `exposure_incoming_threat_density`, `cluster_density`, `crossfire_overlap`,
`lane_pressure`, `escape_gradient`. Proposal config as-built (equal weights 1.0):

```
AWARE_CANDIDATE_CONFIG = (distance_normalized, exposure_incoming_threat_density,
                          cluster_density, crossfire_overlap, lane_pressure,
                          escape_gradient) — all 1.0
```

- **(a) FULL SET (all 6 entries, equal weights) — ADOPTED.** Rationale: the gate prices the
  geometry DIAL, and a null must be decisive. A lean-set null is ambiguous (maybe the one read was
  weak, not geometry per se); a full-set null closes the question. The F8 cost flag (5.47× BLIND,
  unmitigated 40-mob worst case) is a **batch-economics** number: ~93 ms/fight × 256 aware fights
  ≈ 24 s — irrelevant at gate scale, and the shipped-config pruning lap (which reads earn their
  keep, weight tuning, map-cache mitigations) is the FOLLOW-UP lap if the gate passes. Honest note:
  gamora's build report expected the pin "won't be all 5" against the ~3–4× runtime target; the
  conductor overrides for gate purposes — the runtime target binds the SHIPPED config, not the
  instrument.
- ~~(b) LEAN SET~~ · ~~(c) other subset~~ — struck at pin. The shipped-config pruning lap
  (post-gate, if PASS) owns the lean/runtime question.

**PINNED AWARE config = `AWARE_CANDIDATE_CONFIG` verbatim (6 entries, all weights 1.0). Weights
frozen; no tuning between seal and verdict.**

## §4 — Metrics (F3 — RULED at L-23; formalized here)

- **PRIMARY — player damage INTAKE** (`SpatialFightResult` damage-taken field, BW-1 §2.4; mirror of
  `player_damage_total`, self-inflicted LC HP costs excluded). Lower is better.
- **SECONDARY — time-to-clear** (fight duration in ticks). Report-only + directional flag: AWARE
  slower by >5% on encounter aggregate ⇒ flagged for investigation (not auto-fail).
- **GUARD — differential clear-rate.** Per (cell, seed): clear outcome (all-mobs-killed boolean)
  must MATCH between arms. Any mismatch ⇒ that cell's intake comparison is void (intake on a
  non-clear is incommensurable) and the gate verdict is PARTIAL-investigate regardless of margins —
  in EITHER direction (aware clearing MORE is a real finding but a different claim than the
  preregistered one; it re-opens the frame, not the bar).
- **Empirical basis for intake-primary (battery preview, conductor-computed 2026-07-22):**
  damage-DEALT is near-degenerate under full-clear — seed-SD = 0 in 29/32 baseline and 21/32
  encounter cells (dealt ≈ Σ mob HP when everything dies; the W3/W3′ convergence lesson in
  miniature). Intake has no such ceiling. Time proxy (trace length): encounter aggregate seed-CV
  1.30%, baseline 0.53% — tight secondary channel.

## §5 — The bar (F4 — D2 + D3, form RULED at L-23; numbers pin here)

**Margin definition:** `M_rel = (Ī_blind − Ī_aware) / Ī_blind`, where Ī = mean per-fight intake
across the ENCOUNTER arm (32 cells × 4 seeds). Positive = aware takes less damage.

- **[P2 — RULED: D2 = 10% (Matt 2026-07-22, L-27)] D2 — relative bar.** Calibration window
  **5–15%** (legolas bifurcation: regime-shift cluster >100% [Uriarte kiting, Black & Darken +476%]
  vs trained-agent subtle cluster 3–17 pp [HRL-IM, Multi-UAV, HoK]; ours predicted subtle by the
  W3/W3′ competent-play-convergence lesson). ~~8%~~ / **10% PINNED** / ~~12%~~.
  **`PASS requires M_rel ≥ 0.10`.**
- **[P3 — RULED: k=2 × blind-arm aggregate seed-SD (Matt 2026-07-22, L-27)] D3 — noise floor.**
  Form (ruled L-23): absolute margin ≥ k × noise-estimate, computed from the SEALED BLIND ARM at
  execution (B&D Figure-8 margin-÷-reference-σ precedent).
  - **Estimator PINNED: (i) seed-to-seed SD of the blind encounter-arm aggregate mean intake** —
    exactly "how much does the headline number move if I reseed"; honest 3 df; matches the ruled
    form. ~~(ii) pooled per-cell seed-SD as estimator~~ struck — stays a REPORTED DIAGNOSTIC (the
    substrate is largely deterministic per-cell: 21/32 encounter cells had zero dealt-noise;
    per-cell floors are ill-posed). ~~(iii) bootstrap CI half-width~~ struck (overkill at n=4).
  - **k PINNED: 2** (rliable 95%-CI-non-overlap ≈ k=2; primary protection is D2, D3 is the floor
    against noise-driven pass). ~~3~~ struck.
  - **D3 as executable predicate: `(Ī_blind − Ī_aware) ≥ 2 × SD_seed(blind encounter-arm
    aggregate mean intake)`.**
  - **Degenerate guard:** if the estimator = 0 (fully deterministic blind arm), D3 auto-satisfies;
    D2 + clear-guard still bind.
- **Reporting (regardless of pins):** per-cell intake deltas + sign counts + pooled sd + both-arm
  aggregates — the B&D/legolas reporting-discipline shape. Sign counts are REPORTED, not gated.
- **Specificity read (P4 = BOTH, so unconditional):** matched-baseline `M_rel` reported;
  expectation ≈ 0. If
  baseline-arm margin > ½ × encounter-arm margin, geometry-specificity is questionable ⇒
  PARTIAL-investigate.

## §6 — Verdict semantics

- **PASS** = D2 ∧ D3 ∧ clear-guard clean ∧ specificity clean (P4 = BOTH). Aware fighter VALIDATED as
  the batch-sim player proxy; unlocks: shipped-config pruning lap (weights/subset/cache), fork-(a)
  texture metrics, L-26 boss-garnish sequencing (the priced dial).
- **FAIL** = honorable fallback (pre-registered, no relitigating): BLIND remains the shipped
  fighter; the geometry reads archive as **boss-garnish candidates** (L-26 layer-2 has different
  economics — a boss reading the room is a config, not a rebuild); ZERO rip-out (ablation property
  = config-only, no code debt). The run still banks: policy seam, intake metric, battery harness.
- **PARTIAL-investigate** = clear-guard trip or specificity trip: no verdict until the confound is
  named; conductor rules on re-run vs re-frame with Matt.
- **Precedence rule (PIN folded at prereg-check C1, jack-ryan 2026-07-22; no bar-parameter move):**
  **PARTIAL triggers (clear-guard trip OR specificity trip) take precedence over the D2/D3
  verdict.** If either fires, the verdict is PARTIAL-investigate irrespective of whether D2/D3 were
  met or missed — **no confound-tainted run is scored PASS or FAIL.**
- **Result-read riders (prereg-check C3/C4/C5, INFO — travel into the verdict read):**
  (C3) DRIFT-CRITIC confirms the run's intake aggregate-per-seed + `SD_seed` use the SAME estimator
  verified on the dealt stand-in (sample SD, n−1, 3 df); (C4) REPORT the realized intake
  determinism profile alongside the verdict so a near-vacuous-D3 outcome (degenerate guard binding)
  is visible, not silent; (C5) AWARE includes `distance_normalized` alongside the five geometry
  reads — do not attribute a margin PURELY to the geometry reads; the post-gate pruning lap owns
  per-read contribution disentangling.

## §7 — Execution pins (carried + new)

1. `player_gather_primitive` OFF, both arms (carried conductor pin).
2. Sequential fights, no parallel regens (Discipline #3); smoke slice first (#2: 1 cell × both
   arms × 4 seeds before the full battery).
3. Decision-trace capture ON in both arms (post-hoc why-did-aware-differ analysis; harness already
   records it).
4. Seeds fixed {20260722–25}; no seed additions after seal (a wider-seed lap is a NEW prereg).
5. **Site-coverage attestation** (gamora, at execution): assert the policy seam is the ONLY
   target-choice source in the player path at the frozen commit (BW-1.1 tests already prove both E4
   sites + primary selection call the seam; attestation re-states it at the gate hash).
6. **Substrate deviation (disclosed, ARCHITECT item):** the exposure map reads runtime `max_hp`
   (tier-encoded: swarm/magic 150, elite/boss 2500) + `preferred_behavior` + `aggro_radius_m` — not
   the spawn-time-only `threat_tier`/`archetype_tag` labels named in L-22 §1.2. As-built reality
   per BW-1 report; carried as the map's substrate definition.
7. Runner extends the battery harness (same cell/seed/parity logic; adds intake + duration capture
   per arm); verdict JSON + seal JSON committed; full traces regenerable-not-committed (BW-1
   precedent).
8. corpus.db READ-ONLY; no telemetry-schema changes; engine diff between seal and verdict = ∅.
9. Commit-never-push (gamora); conductor pushes; `git -C <repo>` explicit, always.

## §8 — Process from here

1. ✓ Matt ruled P1–P4 in-session 2026-07-22 → **L-27** (all four = conductor leans,
   PRIME-CONCURRED).
2. ✓ Conductor PINNED this sheet (numbers filled, alternatives struck, engine hash recorded) —
   freeze confirms on check PASS; post-freeze edits void the gate.
3. ✓ jack-ryan prereg check returned **PASS-WITH-CONCERNS**
   (`…/qa/findings/2026-07-22-prereg-check-aware-fighter-ablation.md`, `a9bb1886`): C1 + C2 WARN
   pins **FOLDED** (§6 precedence rule; §2 auditable seal artifact); C3/C4/C5 INFO riders recorded
   in §6. All five re-derived numbers reproduced EXACTLY; no-confound verified in source at
   `2f43045`.
4. jack-ryan re-verify at the freeze beat (C1 + C2 only; PRESENT / MECHANICAL / CONSISTENT) →
   clean PASS → **FREEZE VERBATIM**.
5. Named-gamora execution charter (conductor-authored) → seal → run → verdict JSONs.
6. Verdict: conductor synthesis (DRIFT-CRITIC vs this frozen sheet) + Matt ruling; review book
   follows.

**Signed:** gandalf (`RUN-CONDUCTOR` / SPEC-AUTHOR), 2026-07-22 — veto-open.
