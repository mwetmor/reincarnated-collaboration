# Finding — 2026-06-13 — gamora-bc-measurement-pipeline-and-full-run

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** engine `3136fd7` + `60cce7a` (pipeline) and `edec4c6` + collab `286e373` (full run)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3/6 (cross-seam round-trip), 4 (decisions-log/lock truth); Disciplines #1, #3, #4, #8, #11, #17, #19.1

## Verdict: PASS-WITH-INFO

The MEASUREMENT is methodologically sound and the headline finding is REAL, independently
reproduced three ways. gandalf may consume the inversion as a trustworthy signal at Gate 1.
Two INFO items fold forward (one is a narrative-vs-artifact aggregation nuance gandalf should
read before designing around the damage-taken claim). Nothing BLOCK-grade; nothing locked changed.

## What I found

**1. The inversion is real substrate, not a measurement artifact — reproduced independently.**
I re-ran the full corpus driver: byte-identical output (md5 `63731e21…`, git diff empty, RUN
CLEAN, schema 96/96), so the run is deterministic and brownfield-safe. I then re-did the FK join
to PREDICTED targets from scratch and reproduced gamora's exact ordering: mean measured eHP_ratio
by PREDICTED bin = tank 0.982 < mitigator 1.029 < dodger 1.091 < glass 1.202. PREDICTED is a clean
24/24/24/24; MEASURED is glass 94 / mitigator 2 / tank 0 / dodger 0. The kits rocket intended as
glass do measure as the tankiest. I also re-derived raw signals: predicted-glass kits genuinely
carry the highest raw HP (mean 17,329 vs tank 14,985, +16%) — reproduced byte-for-byte against
gamora's stated number. The HP advantage is what drives the inversion; it dominates any
damage-taken difference. The inversion is substrate-intrinsic: rocket's `defensive_vitality_scale`
(1.8 tank → 0.55 glass) did not translate into differentiated simulated eHP, and in fact inverted.
This is the load-bearing signal for rocket Items 7/8, and it is sound.

**2. The panel decision (boss-only, fixed) is a legitimate Discipline #4 right-tool choice.**
gamora's empirical probe (math note §1) shows standard/elite opponents die to the kits' opening
burst before landing an attack → 0 incoming damage → every kit clamps to the tank ceiling →
Axis-4 meaningless. Only boss-tier survives to exercise the defensive surface. I confirmed in the
output that ZERO kits clamped to the tank-ceiling sentinel (ratio==10.0) and avoidance populated on
all 96 — so the panel achieved its stated purpose: it made the surface measurable. The production
KPM gauntlet is correctly rejected (math note §2.1) as the wrong tool — it's a band-calibration
harness, not a defensive-profile measurement. The bin-COLLAPSE magnitude is panel-strength-relative
(a softer panel lifts all ratios toward the 5.0/2.0 edges); gamora pre-registers this honestly
(§3) and reports-don't-forces (Discipline #11) — she did not re-tune edges to manufacture the
target. Correct.

**3. Locked-edge / schema / math-before-code integrity all clean.** Code edges
(0.40 / 5.0 / 2.0 / 0.3 / 0.7) match lock §§3.6/3.7 (lines 275-277, 329-333) exactly — nothing
locked changed. Math notes (3422be2 07:58, panel note) precede the run (edec4c6 11:07) and anchor
to the lock without re-deriving bins (Principle 1 / Discipline #1). star-lord's consume-side
migration (3da0400 08:32) landed before the run; producer validates 96/96 against
`ExportKitBCMeasuredBin` — confirmed on my rerun (Discipline #8, Principle 6 round-trip satisfied,
MIGRATION.md v1.68 present in the pipeline commit). Brownfield: gamora's "2 pre-existing failing
suites on clean HEAD (git-stash confirmed)" note + my byte-stable rerun confirm no perturbation of
existing sim behavior.

## INFO items (fold into gandalf Gate 1)

**INFO-1 — the damage-taken stat in the finding narrative is PHYSICAL-PANEL-ONLY, not the
all-8-fight basis the eHP_ratio actually pools.** The dispatch/completion-record reconciliation
states predicted-glass kits take the LOWEST damage (12,187 < tank 14,534). That number is correct
ONLY on the 4 physical fights. On the all-8-fight basis the eHP_ratio reduction actually uses
(`_ehp_ratio` sums across the full fight list, including the fire opponent), the ordering REVERSES:
glass takes the HIGHEST damage (24,172 > tank 22,755). The inversion CONCLUSION survives either way
because the +16% HP advantage dominates, so the headline is robust. But the supporting "lowest
damage taken" claim is surface-specific, and a reader who treats it as the eHP_ratio basis will
mis-model. gandalf should design Items 7/8 around "glass HP advantage dominates," NOT around
"glass takes less damage" as a general property — it does not, against the elemental opponent.

**INFO-2 — AGENT_STATE md5 mismatch (cosmetic).** gamora's AGENT_STATE cited the deterministic
output md5 as `a2bc98b5`; the actual file md5 is `63731e21…`. The file is byte-STABLE across my
rerun (the brownfield invariant that matters is satisfied), so this is a stale/typo'd checkpoint
value, not a determinism failure. Worth gamora correcting in the checkpoint for future joins.

## Rationale

Discipline #19.1 (cheapest refuting test per claim): I ran the three cheapest refuters — rerun for
determinism, independent FK join for the inversion, independent raw-HP/damage probe for
panel-scale-invariance. The first two confirm; the third confirms the HP half exactly and exposed
that the damage half is surface-conditional (INFO-1). Discipline #4 / #11 / #17 ground the panel
choice and report-don't-force posture. Principles 1/2/6 + Discipline #8 ground the
build-integrity checks. Nothing rises to WARN: the inversion is real, the methodology is sound,
the one narrative imprecision (INFO-1) does not corrupt the artifact (the records carry the
all-8-fight eHP_ratio correctly) — it only risks mis-reading at the design venue, which this INFO
forecloses.

## Action

- [ ] gandalf (Gate 1): treat INFO-1 as a modeling caveat — the inversion is driven by glass HP
      advantage, not by a general "glass takes less damage" property. Decide vestigial-label vs
      generation-fix on that corrected basis.
- [ ] gamora: correct the AGENT_STATE md5 (INFO-2) and, in future divergence narratives, label
      damage-taken stats by surface (physical-only vs all-panel) so the eHP_ratio basis is
      unambiguous.
- [ ] Matt: none required — PASS-WITH-INFO is within jack-ryan tier authority (test/measurement
      certification, ADR-002). The substrate decision is gandalf's Gate-1 lane, not mine.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/bc_measurement.py` (reduction; `_ehp_ratio` pools all 8 fights)
- `~/Games/reincarnated-engine/scripts/gamora_bc_measurement_full_corpus_2026_06_13.py` (run driver)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/bc_measured_bins.json` (96 records; md5 63731e21)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/bc-measurement-corpus-gauntlet-2026-06-13.md` (panel design)
- `~/Games/reincarnated-collaboration/canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` §§3.6/3.7 (locked edges — unchanged)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py:893` (`ExportKitBCMeasuredBin` consume schema — 96/96 valid)
