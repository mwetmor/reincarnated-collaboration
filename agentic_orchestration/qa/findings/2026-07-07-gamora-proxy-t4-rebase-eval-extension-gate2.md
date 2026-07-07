# Finding — 2026-07-07 — gamora-proxy-t4-rebase-eval-extension

**Reviewer:** jack-ryan (DEV-MODE Gate-2, BLOCK authority)
**Severity:** PASS (INFO)
**Verdict:** PASS
**Target:** tag `gamora/v-proxy-t4-rebase-eval-extension-1` @ engine `8a29009` (= HEAD)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam MIGRATION), 6 (cross-seam round-trip), Disc #11 (empirical inspection), Disc #12 (semantic-shift framed-not-buried), ADR-004, ADR-008

## What I found

The extension certifies the ratified four-family PROXY suite against the LANDED rebased source in one pass, and every claim in the completion record reproduces under independent verification. Tag `8a29009` equals HEAD; the commit touches only instrument surface (`scripts/gamora_proxy_t4_suite_eval_2026_07_02.py`, `tests/test_proxy_t4_suite_eval.py`, math note §9, artifact JSON, `simulation/MIGRATION.md`, `simulation/AGENT_STATE.md`) — I confirmed by diffstat that it touches ZERO generation/production code (no `mechanic_alteration.py`, `t4_catalog_v2.py`, `proxy_commander.py`, `demo_summoner_kits.py`). I re-ran the pin suite myself (20/20 pass, 0.11s — matches the claimed 0.12s) and the full-pass harness myself (EXIT=0, all_pass=True). A2: all 12 member cells OK, every A2 number in the record reproduced exactly on my run — FISSION crypt 60.1s→9.7s (army_dps 500→3300), SOVEREIGNTY 500→1000, ASCENSION 500→550 (heavy) / 575 (light), `proxy_dmg>0` / `player_dmg==0` on every row (R1 by construction), WR held at 1.0, caster-alone WR 0 under baseline AND T4-noop. A3: reproduced bone→FISSION / crypt→SOVEREIGNTY on landed non-mana `focus`; the SOVEREIGNTY `energy≠mana` gate at `mechanic_alteration.py:1069` is exactly as cited; F-d pair separated (bone sep 0.15, crypt sep 0.275). I independently ran the F-f AST probe — it returns False; no live `FAMILY_MAX_ONE` consumer exists in the generation package (excluding the definer `t4_catalog_v2.py`), so the eval-side invariant HOLD is honest and no inert guard was wired on the frozen surface. Hard-guards all clear: scaffold bands byte-match the record (ASCENSION 0.15/0.10, SOVEREIGNTY pool 10 / resummon 20.0, FISSION split 0.60 / cap 4, ZONE amp 0.15), no `2.3384` chassis-fossil reference in the diff (chassis FROZEN), D3 baseline asserted byte-unchanged by construction (`_assert_cert_baseline_intact` fires after every apply) and holds on my run.

## Rationale

- **Principle 1 (math-before-code):** the §0–§6 pre-registration (certify-or-PUSH rule, A3 two-branch, F-f two-branch) was authored before the cert run; §9 is the completion record against the landed source. Math note is thorough and honest about which branch fired.
- **Principle 2 (smoke-gate):** smoke + full-pass GREEN; I reproduced both independently. Commit carries the smoke line.
- **Principle 3 / Principle 6 / ADR-004 (cross-seam):** the new `energy_type` read is a CONSUMER-side dependency on rocket's DoF-A field (`demo_summoner_kits.py`, tag `rocket/v-batch2-dof-a-focus-field-1` @ `1af6889`). The MIGRATION note is a consumer-read note that correctly cross-refs rocket's producer contract; there is NO producer/schema change on gamora's side (no `SpatialFightResult` field, no SQLite column, no `_INSERT_SQL` widening) — star-lord owes nothing, as claimed. Round-trip is not-applicable in the Principle-6 sense because gamora emits no cross-seam field here; the read is over an already-landed generation field on a read-only instrument. Justification is explicit, not silent.
- **Disc #11:** all landed-source facts I spot-checked (scaffold bands `:938`, family `:1466`, SOVEREIGNTY gate `:1069`, `energy_type` default `focus`) are as the record states — inspected, not assumed.
- **Disc #12:** the semantic shift (retiring the `charge_stack` eval-side hard-code in BOTH harness and tests, now reading the landed field) is framed in the commit body and the MIGRATION note, not buried. No live production behavior is reinterpreted — the change is eval-instrument-only.
- **F-f (Disc #12 restraint):** the record does NOT promote the F-f check to a live-consumer assertion because rocket determined the leg-2 route does not make the GEOMETRY co-draw reachable (B4-scoped) and no live consumer exists. The eval-side invariant stands as the catch; `enforce_family_max_one` live-wiring is correctly re-surfaced to KR rather than papered over with an inert guard on a frozen surface.

This is within jack-ryan tier authority (ADR-002): the change is test additions + within-seam instrument (harness/math note/artifact) + a documentation-side consumer MIGRATION note, with NO production API or schema change. No Matt escalation required.

## Action

- [x] Developer: none required — cert is clean and reproduces.
- [ ] KR: carry forward the two open items the extension correctly RE-SURFACED (not gamora-owed): (1) rocket owes the `enforce_family_max_one` live-wiring before B4 wires the emission pipeline; (2) the F-f live-consumer probe should flip to True at that point, at which time the F-f test can be promoted to a live-consumer assertion (gamora's §3 sub-case-1). These are B4-scoped, not blockers on this cert.
- [ ] Matt: no decision needed. Milestone tagging (drop of seam prefix) remains Matt-gated per ADR-003 when this rolls into a milestone; push remains Matt-gated.

## References

- `reincarnated-engine/scripts/gamora_proxy_t4_suite_eval_2026_07_02.py`
- `reincarnated-engine/tests/test_proxy_t4_suite_eval.py` (20/20 pins, re-run by reviewer)
- `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-suite-rebase-eval-extension-2026-07-07.md` (§9 completion record)
- `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-rebase-eval-extension-full.json` (artifact; all_pass=True, 14 rows)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-07 consumer-read note)
- `reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (`:938` scaffold bands, `:1069` SOVEREIGNTY gate, `:1466` PROXY_T4_FAMILY — inspected, unchanged by this tag)
- `reincarnated-engine/src/reincarnated/generation/demo_summoner_kits.py` (rocket DoF-A field consumed; unchanged by this tag)
- Independent verification artifact: `/tmp/jr-verify-proxy-t4-ext.json` (reviewer's own full-pass, reproduces record)
