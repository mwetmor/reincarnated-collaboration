# Finding — 2026-07-07 — rocket leg-3 STEP-1: summoner emission-wire design + resource/LLM-cost projection

**Reviewer:** jack-ryan (Gate-1, DESIGN-MODE — pre-fire peer collaborator)
**Verdict:** PASS-WITH-CONDITIONS
**Target:** math note `leg3-summoner-emission-wire-and-projection-2026-07-07.md` (engine `0384dbb`; verified HEAD)
**Developer:** rocket (generation seam)
**Mode:** DESIGN + PROJECTION only — NO code landed, NO run fired. STEP-2 (wire + run) gated on THIS PASS + Matt run-auth.
**Principles applied:** 1 (math-before-code), 3 (cross-seam impact), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #1.1, #8, #11, #12, #23

---

## What I found

Every load-bearing claim in the note was verified against source at `0384dbb` (I did not trust the note). The routing correction is CORRECT and it is the finding that matters most: the dispatch's cited wire site `season_generation_pipeline.py:404-412` is a dataclass field-def + comment (`primary_t4: Optional[dict] = None` at `:409`) — `grep '\.primary_t4\s*='` returns zero hits in the pipeline (exit 1). The real DDA stamp is `cycle14_wave5_emitter.py:546` (`primary_t4 = PRIMARY_T4`), in star-lord's export seam. The `PRIMARY_T4` constant (`:394-402`) matches the note's transcription exactly. The emit-wire design is sound: the widened validator (`:795-841`) does a full field-by-field `_PRIMARY_T4_DDA_REQUIRED` match on the DDA branch (so Clause D emitting `dict(PRIMARY_T4)` is provably byte-identical), and the proxy branch requires `discipline_anchor` + a `ACCEPTED_PROXY_PRIMARY_T4` member + truthy `scope`, with an explicit reject on non-proxy-bearing kits carrying a proxy strategy. `route_primary_t4` returns an `AlterationOutput` dataclass with `strategy_type` (not a validator dict with `strategy`), so the adapter is genuinely net-new and necessary. `build_proxies_surface` returns `[]` for solo kits (`proxy_vocabulary_bridge.py:294`), and empty decls fall through to DDA — the freeze proof holds. The §8-A1 bands are correctly framed as a MEASURED outcome reported at STEP-2, not a pass/fail threshold. The W3-smoke root-cause is confirmed orthogonal: the `w3_emission_driver.py:688` assertion hard-codes `== 300 and == 400` reading only `identity_glyph` (grep of the assertion body for `primary_t4`/`proxy` returns zero hits), yet it WILL halt a proxy-inclusive pilot because that run breaks the 300/400 population invariant regardless of the emit path. The cost envelope is honestly bounded and traceable to the W3 pilot-beat sizing note (`export/math/w3-pilot-beat-sizing-2026-07-03.md:128`, "400 survivors ≈ $10-20"), the flavor pass is genuinely per-skill with per-item resumable skip (`one_realm_bundle_assembler.py:925` — `for skill in kit.get("skills", [])`), and the $0 dry-run levers are real (`w3_emission_driver.py:703/792` — `if not dry_run_flavor and not smoke:`).

## Verdict on the five verification asks

1. **Routing correction (load-bearing) — RATIFIED.** `:404-412` is field-def only; real stamp is `cycle14_wave5_emitter.py:546`. The dispatch's single-seam framing does not match the code.
2. **Emit-wiring design — SOUND.** Adapter Clause D → byte-identical solo; Clause P → proxy activation; §8-A1 correctly framed as measured.
3. **Cost projection — SOUND + HONESTLY BOUNDED.** Envelope ≤$10 flavor / $0 dry-run, anchored on empirical W3 precedent. Call-count math checks (200 survivors × 12 skills = 2,400 kit-flavor calls). Dry-run-first is the correct risk posture.
4. **W3-smoke — ORTHOGONAL to emit path but GATES the pilot; CONFIRMED.** Fix belongs in STEP-2, star-lord's file.
5. **Disc #23 framing — HONEST.** Refutation conditions are cheapest-refuting and mostly already empirically closed.

## STEP-2 co-dispatch touch-point inventory — CONFIRMED + seam-attributed (for KR routing)

This is the routing consequence KR needs. STEP-2 is a **rocket+star-lord co-dispatch**, NOT a solo rocket landing. Four touch-points, verified against source:

| # | Touch-point | Seam / owner | File:site (verified) |
|---|---|---|---|
| 1 | Emit-assignment wire + net-new adapter `_primary_t4_to_emit_dict` | **star-lord** (export) | `cycle14_wave5_emitter.py:546` |
| 2 | Driver proxy-inclusive drive | **star-lord** (export) | `w3_emission_driver.py` |
| 3 | Identity-glyph assertion → population-aware | **star-lord** (export) | `w3_emission_driver.py:688` |
| 4 | Proxy-bin un-gate (`_DEFERRED_PROXY_BINS` lift for pilot) | **rocket** (generation) | `bc_target_composer.py:97` (gate at `:318`) |

3 of 4 land in star-lord's `export/`; rocket's clean-owned STEP-2 work is the composer un-gate only. Per role rules ("do not patch across seams; raise to knight-rider"), STEP-2 must co-fire. Inventory is complete and correctly attributed.

## Conditions to fold before STEP-2 (all minor; none block PASS)

- [ ] **C1 (rocket, doc-only):** the note cites `t4_scope` vocab at `cycle14_wave5_emitter.py:451` — that line is `MULTI_ACTIVE`. The `chain_wide_own`/`CHAIN_WIDE_OWN` label IS existing t4_scope vocabulary, but it's documented at `:67-68` (module docstring valid-values list), not `:451`. Correct the line-ref in the STEP-2 wire note. Substantive claim (existing label, not a new magnitude) is unaffected.
- [ ] **C2 (STEP-2 rehearsal):** the "≤7 proxy entities/fight" bound (max_active 3 + FISSION cap 4) is directionally sound — FISSION hard-cap=4 confirmed (gamora AGENT_STATE + `b1-rebase-proxy-t4-suite-eval` JSON); `max_active` is a gamora-calibrated balance constant. The note already flags peak-entity as a STEP-2 rehearsal-confirm item. Keep that as an explicit STEP-2 acceptance line; do not treat ≤7 as proven until the rehearsal measures it.
- [ ] **C3 (STEP-2 measurement):** the §2.5 `t4_candidates` family-membership A1-coverage question stays OPEN and is an explicit STEP-2 acceptance line (does the phase-2 scan already emit a family member into `t4_candidates`, or does leg-3 owe it?). Correctly deferred; carry it forward, do not let it silently drop.
- [ ] **C4 (star-lord, STEP-2):** §4.4 fix option (b) (non-empty + all-glyphs-valid, no exact split pinned) is the safer disposition — it stops encoding a batch-1 population invariant into a driver leg-3 re-populates. Recommend (b); leave final call to star-lord as file-owner per the note.

## Run-auth cost posture (for KR → Matt relay)

The envelope is sound and I endorse the dry-run-first framing. Recommended authorization ask to Matt:

- **Authorize the $0 dry-run pilot unconditionally** — it is the wire-proof + band measurement + A1 coverage check at ZERO LLM cost (`dry_run_flavor=True` skips all flavor passes). This carries no ADR-006 spend risk; the only cost is ~23-36 min compute on the local host (well within an unattended window, no overnight).
- **Authorize a ≤$10 flavor ceiling as a SEPARATE, optional follow-on** — fired only if Matt wants named pilot-ready kits. Expected ~$6.50 (130 survivors × ~$0.05, amortized on empirical W3 precedent); monster/gear flavor is shared + largely already-flavored from prior W3 runs, so resumable-skip drops actual calls well below the 2,800 ceiling. Key has ~$50 remaining; $10 is 20% — no exhaustion risk.

This two-tier ask (compute-only $0 first, bounded-$ flavor second) is the right posture: it de-risks the wire proof entirely and defers the only real spend to a decision Matt can make AFTER seeing dry-run band results.

## Action

- [ ] rocket: fold C1 (line-ref), carry C2/C3 as STEP-2 acceptance lines.
- [ ] star-lord: STEP-2 owns touch-points 1-3; recommend §4.4 fix (b) per C4.
- [ ] knight-rider: author STEP-2 as a **rocket+star-lord co-dispatch** per the confirmed touch-point inventory; relay the two-tier run-auth ask ($0 dry-run first + optional ≤$10 flavor) to Matt.
- [ ] Matt (run-auth, ADR-006): authorize $0 dry-run pilot; separately rule on the ≤$10 flavor ceiling.

## References

- Note under review: `reincarnated-engine/src/reincarnated/generation/math/leg3-summoner-emission-wire-and-projection-2026-07-07.md`
- Wire site: `src/reincarnated/export/cycle14_wave5_emitter.py:546` (stamp), `:394-402` (PRIMARY_T4), `:795-841` (validator), `:67-68` (t4_scope vocab)
- Pipeline field-def (NOT a populate site): `src/reincarnated/generation/season_generation_pipeline.py:404-412`
- Route fn: `src/reincarnated/generation/mechanic_alteration.py:1972` (`route_primary_t4`), `:136-163` (`AlterationOutput`)
- Proxy family: `src/reincarnated/generation/t4_catalog_v2.py:150` (`ACCEPTED_PROXY_PRIMARY_T4`)
- Un-gate: `src/reincarnated/generation/bc_target_composer.py:97` / `:318`
- W3 assertion: `src/reincarnated/export/w3_emission_driver.py:688`; $0 levers `:703`/`:792`
- Flavor pass: `src/reincarnated/export/one_realm_bundle_assembler.py:925`
- Cost anchor: `src/reincarnated/export/math/w3-pilot-beat-sizing-2026-07-03.md:128`
- Predecessor: `qa/findings/2026-07-07-leg2-summoner-emission-route-coordinated-gate2.md` (`3bae44a`)
- Governing dispatch: `dispatches/2026-07-07-rocket-leg3-summoner-emission-wire-and-run.md`
