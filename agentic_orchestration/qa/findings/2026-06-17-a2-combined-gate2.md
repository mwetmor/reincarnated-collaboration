# Finding — 2026-06-17 — A2 combined (proxy-commander Set #6 forward-work)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** `548c881` (tag `rocket/v-proxy-add-gen-1`) + `4e13afb` (tag `gamora/v-proxy-add-sim-1`) — reviewed as one integrated wave
**Developers:** rocket (generation half) + gamora (simulation half)
**Principles applied:** Review Principles #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #5 (severity); Disciplines #1/#1.2 (math-note-first + code-citation), #2 (smoke-before-full), #9 (schema/attribution clarity), #11/#12 (substrate-led / brownfield non-shift); ADR-002, ADR-004, ADR-006

## What I found

Both halves of Wave A2 are clean, additive, and integrated correctly. I verified empirically (did not trust the completion summaries) against all 8 Gate-2 scope items. Both smokes PASS at the asserted counts when I ran them myself: generation 8/8, simulation 11/11, plus the D4 count regression 6/6 (the additive contribution accumulator did not break the count instrument). The contribution-ratio math note is math-before-code and its code-citations point at real lines that do what they claim: the accumulator at `spatial_engine.py:1724-1729` computes `Σ damage_multiplier × tick_size` over the same per-tick active set the count instrument walks (gated by the identical `track_proxy_population` flag at :1713), and the ratio at :1873 is exactly `proxy_damage_unit_seconds / (elapsed + proxy_damage_unit_seconds)` — the scale-invariant form the note derives by cancelling `owner_dps_mean`. The 0.5 selector boundary is real and shared by construction, not asserted: the sim does NOT redefine a threshold — `proxy_commander.classify_kit_membership` delegates entirely to rocket's `classify_proxy_primary`, which owns `PROXY_PRIMARY_THRESHOLD = 0.5` (inclusive `>=`; verified 0.5→True, 0.4999→False). The 6b circularity guard RAISES on `measured_at_6b_instrument=False` on BOTH halves (gen selector and sim wrapper). Clause B `s` is strictly in (0,1) in measured behavior (calibrated `S_BASELINE = 0.35`), the rocket emit guard re-fires on s∈{1.0, 1.5, 0.0, -0.1}, AND the sim carries a defensive re-check at `proxy_commander.py:123`. Set-applied contribution rises 0.7500→0.8684 and stays <1.0 (player still matters); `proxy_max_active` remains the hard count wall (Δcount capped). Production defaults are unchanged — `apply_max_profile_investment=False` (combatant.py:486, untouched) and `track_proxy_population=False` (spatial_engine.py:1195/2125); flag-OFF path returns 0.0 (brownfield-safe). CapabilityCategory 6→7 has all in-seam count-asserts updated (partition_schema, gear_instance_generator, tests) and there are ZERO out-of-seam consumers of the enum (grep across simulation/export/output/telemetry/spirit_guide returned nothing) — no exhaustiveness assumption is violated. The smoke writes nothing to the archive (ADR-006 read-only honored). Both commits are pure-additive (548c881; 4e13afb is 553 insertions / 0 deletions).

The one INFO observation: the simulation MIGRATION.md entry for this wave (line 11) is labeled **v1.73**, but v1.73 is already taken at line 7797 (the 2026-06-16 KPM-band Stage-1 entry). That prior entry's own note (line 7804) already flagged a v1.72→v1.73 numbering collision pending Stage-2 reconciliation. The new Wave A2 entry inherits/re-uses the same disputed number. This is a documentation-attribution-surface duplicate, not a behavioral defect or principle violation.

## Rationale

- Scope items 1-8 all verified empirically (Review Principle #2 smoke-gate; Discipline #1.2 code-citation). The math note is math-before-code and the cancellation derivation is real in the code, not narrated (Discipline #1; Review Principle #1).
- Cross-seam coherence (item 8) is structural, not coincidental: the sim consumes rocket's pure selector and never redefines the boundary or the contribution definition (Review Principle #3; ADR-004 — the MIGRATION names `classify_proxy_primary` as the single interface).
- The s<1 non-negotiable is double-guarded (emit + defensive re-check) and the 6b circularity contract is enforced on both halves — the capstone §6 anti-bootstrap discipline is encoded, not just documented.
- The MIGRATION version collision is Discipline #9 (attribution clarity — version monotonicity is the traceability surface). INFO, not WARN: it does not affect behavior, schema correctness, or the wave's pass; it muddies future migration-log traceability and should be reconciled when the pre-existing v1.72/v1.73 collision is reconciled (Stage-2, already banked).

## §2.2 ENDORSE criterion (pre-registered) — SATISFIED; wave TERMINATES without waking gandalf

All four §2.2 ENDORSE conditions hold against the combined evidence:
1. **Sensible membership** — genuine proxy-commander caster (contribution 0.7500) FLAGS; **Beast-Taming hunter (0.3750) does NOT flag** (the named negative case, in-sim via real integrated contribution); solo (0.0) does NOT flag.
2. **2pc + 4pc Clause A within the parity books** — no clause exceeds its band-share (smoke check [3] PASS); `proxy_max_active` stays the hard wall.
3. **Clause B s < 1** — coefficient `s_baseline = 0.35` strictly in (0,1), verified on the emitted bonus, not just the guard.
4. **Measured at the neutral 6b instrument** — selector path applies NO Set #6 terms; circularity guard enforced.

**No §2.2 PARK exception fires:** command-amplification (`s_command` / `effective_s(t)`) is held LIVE-ONLY by construction on both halves — never read into the sim parity path — so it is NOT promoted into the parity books (no Tier-3 production-semantic-shift). No membership surprise — the only flag is the genuine proxy-commander; beast-taming and solo are correctly sub-threshold. The wave terminates on clean pass per the pre-registered criterion.

## Action

- [x] jack-ryan: APPROVE the combined wave (ADR-002 — both halves are flag-gated additive within-seam builds with passing smokes; no cross-seam schema break; no decisions-log conflict). PASS-WITH-INFO.
- [ ] gamora (INFO, non-blocking): reconcile the simulation MIGRATION.md v1.73 label collision (line 11 vs line 7797) when the pre-existing v1.72/v1.73 numbering collision is reconciled (the Stage-2 item already banked at line 7804). Until then, traceability for the proxy-contribution entry is by title, not number.
- [ ] No Matt action required — no BLOCK, no §2.2 PARK, no Tier-3 trigger. Production flag-flips (the eventual live-integration of `apply_max_profile_investment` / `track_proxy_population`) remain a separate Tier-2/Tier-3 step outside this build-and-measure wave.

## References

- `src/reincarnated/generation/kit_architecture.py:326,329-370` — `PROXY_PRIMARY_THRESHOLD = 0.5`; `classify_proxy_primary` (pure; 6b guard; inclusive `>=`)
- `src/reincarnated/generation/partition_roller.py:314,317-354` — `PROXY_OFFENSE_INHERITANCE_SHARE_DEFAULT`; `make_proxy_commander_set_bonus`; `0 < s < 1` emit guard
- `src/reincarnated/generation/partition_schema.py:391,396` — `PROXY_ADJUSTING` 7th member + `len == 7` assert
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:1713,1724-1729,1873` — contribution accumulator (flag-gated) + scale-invariant ratio
- `src/reincarnated/simulation/spatial_gauntlet/proxy_commander.py:70,117,123,199-201` — `S_BASELINE=0.35`; defensive s-recheck; delegation to rocket's selector
- `src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` — additive `mean_proxy_contribution_pct` field
- Math notes: `src/reincarnated/generation/math/proxy-commander-set6-forward-work-2026-06-17.md`; `src/reincarnated/simulation/math/proxy-contribution-measure-and-set6-calibration-2026-06-17.md`
- Smokes (run + verified): `scripts/gamora_proxy_contribution_set6_smoke_2026_06_17.py` (11/11), `src/reincarnated/generation/notes/proxy_commander_set6_forward_work_proof_2026_06_17.py` (8/8), `scripts/gamora_d4_proxy_port_smoke_2026_06_16.py` (6/6 regression)
- `src/reincarnated/simulation/MIGRATION.md:11` (v1.73 — collision with :7797); `src/reincarnated/generation/MIGRATION.md:19` (CapabilityCategory 6→7)
- Charter: `reincarnated-collaboration/canonical/story/2026-06-17-autonomous-run-plan-v2.md` §2.2
