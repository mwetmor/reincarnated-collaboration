# Gate-1 Finding — Wave-C Engine Spec (trigger + mark-consume · ailment-wave-c+ · small-adds)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1 peer collaborator; BLOCK authority available)
**Date:** 2026-07-17
**Target:** `canonical/reap-die-rise-engine/wave-c-trigger-mark-engine-spec.md` @ commit `f2511469` (post-DRIFT-CRITIC PASS-WITH-CORRECTIONS)
**Prior gate:** gandalf-prime DRIFT-CRITIC `PASS-WITH-CORRECTIONS` — 4 corrections applied + rulings WC-13..WC-21 stamped veto-open (`f2511469`).
**Verdict:** **PASS-WITH-AMENDMENTS.** Three MAJOR amendments, four MINOR amendments, three NOTE-level observations. No BLOCK. Spec is buildable; amendments are contract-tightening + touchpoint-completion, not structural. Corrections are locus/enumeration-level; no ruling reversal.

**Principles applied:** #1 (math-before-code — §13 formulas verified), #8 (schema-at-boundary — cost_type resolver contract), #11 (empirical inspection — read composer code, verified 972-assert live, verified `_ROLE_COST_TYPE_PRIORITY` state, grep'd support-strike touchpoints), #12 (semantic-shift = additive-widening — enum widenings audited), #13 (drift-check — cross-section consistency). Review Principles #2 (smoke-gate — S6 required per §12.5), #3 (cross-seam impact — 5 MIGRATION docs verified), #4 (decisions-log as truth).

---

## Verdict summary

**PASS-WITH-AMENDMENTS.** Rocket and gamora may build against this spec as written, PROVIDED the three MAJOR amendments below are folded before rocket lands the resolver-contract widen. The MINOR amendments are documentation-quality; the NOTES are for the record. All 8 DRIFT-CRITIC rulings (WC-13..WC-21) are technically sound and I concur — one carries a knock-on scope-adequacy finding (WC-21 STRIKE → Finding 2 blast-radius).

**Mandate coverage:**

| Mandate item | Status |
|---|---|
| 1. Internal consistency (cross-section) | PASS w/ 3 MINORs (cross-refs · matrix-wording) |
| 2. Consumer-contract soundness | PASS w/ 1 MAJOR (cost_type resolver contract) |
| 3. Byte-neutrality claims (§9) | PASS — table auditable; RNG discipline clean |
| 4. Lattice discipline | PASS — 972-assert live @ `bc_target_cell_sampler.py:395`; Wave-C rides `persistent_trigger` (verified `skill_schema.py:224`); no widen |
| 5. Interaction-matrix soundness (§4.8, blind+weaken locus) | PASS — clamp locus consistent doc-wide; DRIFT-CRITIC correction #1 landed cleanly |
| 6. LOCKED invariants (§13) | PASS — all six formulas + LOCKs mathematically sound |
| 7. Seam-routing completeness (§12) | PASS w/ 2 MAJORs (rocket surface misses resolver-contract widen; support-strike blast-radius under-scoped) + 1 MINOR (elrond rendezvous absent from §12) |
| 8. Escalation rulings WC-13..WC-21 | CONCUR on all 8; no dissent-notes; per-ruling notes in decisions-log entries |
| 9. §10 strike-plan blast-radius | See Finding 2 MAJOR — 2 additional composer touchpoints missed |

**Blind+weaken sim-side clamp locus explicit statement (per return-report requirement):** **CONSISTENT doc-wide.** §4.8 canonical matrix row (line 766) states "ADDITIVE-CAPPED; cap at `1 - min(blind + weaken_magnitude, 0.80)`"; §13.2 (line 1492) states "Enforced SIM-side at ailment aggregation — the effect resolver clamps the composite when both are active on one defender"; DRIFT-CRITIC correction #1 explicitly retargets from "emission composition" to "SIM-side clamp at ailment aggregation." Only softness: §4.2 (line 536) `curse:weaken × blind` sub-matrix row uses "ADDITIVE ... compose multiplicatively" without citing the 0.80 cap — see MINOR-5 for polish. Contract is sim-consumer-clear.

---

## MAJOR findings (fold before rocket build)

### MAJOR-1 — cost_type resolver contract not extended to accept `"hp"` return
**Where:** §1 table row for `bc_target_composer.resolve_cost_type` (line 92); §6.5 line 972 (`_ECON_BIN_COST_TYPE_MAP["damage-taken-converts"] = ["hp"]`); §7.3 line 1073 (`_ECON_BIN_COST_TYPE_MAP["HP-economy"] = ["hp"]`).
**Empirical grounds:** `bc_target_composer.py:267` docstring for `resolve_cost_type`: `Returns: one of mana | rage | combo | focus | stamina-as-resource` — closed enum. `_ROLE_COST_TYPE_PRIORITY` (lines 236-241) maps for damage/control/support/hybrid roles contain no `"hp"` entry. `EconomyObjective.cost_type: str` (line 216) is downstream-typed against this return set. The line 742 site `cost_type = resolve_cost_type(econ_bin, role, rng)` feeds downstream cost-carrier fields (mana/rage etc.); `"hp"` as return value is contract-new and cascades.
**Mechanical trace:** with spec-authored `_ECON_BIN_COST_TYPE_MAP["HP-economy"] = ["hp"]`, `resolve_cost_type("HP-economy", "damage", rng)` executes: `feasible=["hp"]` → filter role_priority → `ordered=[]` → fallback `ordered=feasible[:]=["hp"]` → returns `"hp"`. The resolver mechanically works, BUT: (a) docstring lies (post-fold contract); (b) `_ROLE_COST_TYPE_PRIORITY[<any role>]` lists carry no `"hp"` so the role-tie-break path is unreachable for hp; (c) any downstream reader that dispatches on cost_type membership needs the widened enum.
**Recommendation:** §12.1 rocket-slice table row for §6 TH and §7 LC should EXPLICITLY name three sub-changes: (i) `_ECON_BIN_COST_TYPE_MAP` map entries; (ii) `resolve_cost_type` docstring/return-type widen to `mana | rage | combo | focus | stamina-as-resource | hp`; (iii) any consumer that dispatches on cost_type accepts `"hp"` (grep-check owed). Add math-note-linked cross-reference: this is the resolver-contract-widen precedent Wave-B set at its `charge-stack` LIFT — the same discipline governs.
**Severity:** MAJOR — the resolver contract is a schema-at-boundary (Discipline #8); silent widen risks the exact Wave-B AC-1 field-count-off-by-N pattern. Non-BLOCKing because the widen is deterministic + reversible; but rocket needs the touchpoint enumerated before authoring.

### MAJOR-2 — §10 support-strike blast-radius under-scopes composer + canonical-enum sites
**Where:** §10.2 touchpoint inventory (lines 1252-1261); §10.3 sweep plan (lines 1265-1275).
**Empirical grounds (grep-verified `mhwetmore@Mac ~/Games/reincarnated-engine`):**
- `src/reincarnated/generation/bc_target_composer.py:238` — `_ROLE_COST_TYPE_PRIORITY["support"]` first-class entry: `["mana", "stamina-as-resource", "focus", "combo", "rage"]`.
- `src/reincarnated/generation/gear_generation.py:606` — `_ALL_ROLE_ORIENTATIONS = ["damage", "control", "hybrid", "support"]` — the canonical role_orientation enum. §10.2 lists gear_generation.py role_orientation maps but does not name this line as the enum-of-record.
**Consequence:** WC-21 STRIKE ruling ("Discipline #13 drift-by-residue" grounds are sound) implies these two sites must be swept OR the strike is admittedly-incomplete. Currently §10.3 lists only 4 touchpoint classes; two additional CODE sites carrying live `"support"` semantics are absent. If build proceeds against §10.3 as-is, `_ROLE_COST_TYPE_PRIORITY["support"]` remains post-STRIKE — Discipline #13 drift-by-residue survives the sweep the ruling was meant to close.
**Consequence-2 (byte-neutrality):** the spec's §9.1 support-hygiene row states "Behavior changes only where explicitly stated" (implicit byte-neutrality for non-touched sites). If STRIKE removes `_ROLE_COST_TYPE_PRIORITY["support"]`, kits currently emitted with `role="support"` (there are entries in `output/one_realm_demo_bundle.json` — regenerated output surface — plus any live corpus kit whose `role` field is "support") would fall through to the `_ROLE_COST_TYPE_PRIORITY.get(role, _ROLE_COST_TYPE_PRIORITY["damage"])` default at composer line 270 — changing cost_type distribution. That's byte-DIFFERENT for those kits, contradicting the §9.1 default-corner claim. The spec must ALSO name: (a) whether any live corpus kit carries `role="support"` today (elrond query owed); (b) if yes, whether STRIKE re-emission of those kits is scoped as an expected regression or handled by a role remap step.
**Recommendation:** §10.3 sweep-scope adds bullets 5 and 6:
- 5. `src/reincarnated/generation/bc_target_composer.py:238` — remove `_ROLE_COST_TYPE_PRIORITY["support"]` key OR keep-as-legacy-with-note (LEAN: remove per STRIKE consistency; document that composer default-fallback catches any orphan).
- 6. `src/reincarnated/generation/gear_generation.py:606` — `_ALL_ROLE_ORIENTATIONS` enum reduces from 4→3 (support removed). Downstream `_normalise` / defaultdict-role_orientation paths (lines 854, 908) reduce keyspace accordingly.
Plus a LOUD-FLAG in §10.5 for elrond: query DB for kits with `role="support"`, list count; if >0, scope re-emission or role-remap. Sample query lane, not spec-scoped.
**Severity:** MAJOR — the STRIKE ruling's own grounds (drift-by-residue) are directly implicated by the missed sites. Non-BLOCKing because the discovery is scoped-additive (2 code lines + 1 elrond check), and rocket can catch this at authoring pass; but Gate-1 should not clear the spec's §10.3 scope claim without recording the additions.

### MAJOR-3 — §12.1 rocket surface under-enumerates LC/TH consumer-contract touch
**Where:** §12.1 rocket slice table (lines 1364-1377); §9.1 byte-neutrality §7 LC row (line 1189).
**Empirical grounds:** `bc_target_composer.py:742` — `cost_type = resolve_cost_type(econ_bin, role, rng)` fires unconditionally when econ_bin is any active (non-DEFERRED) value. Once §6/§7 lift `damage-taken-converts` and `HP-economy` from `_DEFERRED_ECON_BINS`, ANY kit whose `econ_bin` field takes those values will route through resolve_cost_type at emission time. The byte-neutrality claim in §9.1 §7 row ("existing kits' `hp_cost_scale=0.0` means no HP-cost payment path fires") is SIM-side neutral but is silent on EMISSION-side: whether existing kits' `econ_bin` field takes the newly-lifted values by default.
**Consequence:** the byte-neutrality theorem needs an explicit clause: **"No existing kit's `econ_bin` field defaults to `HP-economy` or `damage-taken-converts` post-Wave-C landing; those bin values are opt-in for LC-signature and TH-signature kits per rocket authoring rule."** Absent this clause, a rocket implementer might presume the bin-lift auto-routes existing kits, breaking byte-neutrality on the emission side even while sim-side is inert.
**Recommendation:** §9.1 §6 row + §7 row extend text: "and no existing kit's `econ_bin` field takes the newly-lifted `damage-taken-converts` or `HP-economy` value at Wave-C landing — those bin values are opt-in per rocket authoring on the 3 LC + 3 TH rosters." §12.1 rocket-slice table for §6 and §7 explicitly notes: "rocket authoring rule: set econ_bin only for the 3-kit / 3-kit rosters named in §6.3 / §7.2; no default-shift for other kits."
**Severity:** MAJOR — byte-neutrality is a Discipline #12/Wave-B house-model invariant; silent emission-side neutrality violates the theorem's default-corner clause. Fixable in the spec text without design change; must be explicit before rocket authors.

---

## MINOR findings (folded at STATUS-BUILT time)

### MINOR-4 — §1 line-92 cross-reference typo
"§7.4 — the sole active bin whose taxed pool IS the HP pool" — §7.4 is the poe2-grim-feast composite kit section. The `["hp"]` cost_type map for `damage-taken-converts` is authored at §6.5 (line 972); the `["hp"]` map for `HP-economy` is at §7.3 (line 1073). Recommend: "per §6.5 for TH; §7.3 for LC HP-economy."

### MINOR-5 — §4.2 matrix row wording drift from §4.8 canonical
Line 536 `curse:weaken × blind` row uses "ADDITIVE ... compose multiplicatively" without citing the 0.80 clamp. The §4.8 canonical row (line 766) is precise ("ADDITIVE-CAPPED at 0.80"). Readers hitting §4.2 first see just "ADDITIVE"; the resolver-contract clamp is elsewhere. Recommend §4.2 row: "ADDITIVE-CAPPED (per §4.8 canonical row — SIM-side resolver clamps composite to 0.80 max)."

### MINOR-6 — §12 sequencing missing elrond corpus re-classify rendezvous
§5.2 flags `le-frost-wall-rm` totem → placed-lane corpus re-classify at Wave-C landing (elrond lane); §6.3 flags 3 TH kits UNKNOWN → TH re-classify; §4.6 flags di-spiritform-druid-pvp re-crawl. Tracker-delta lists these as LOUD-FLAGS. §12.3 sequencing dependency graph does not include an elrond step. Recommend §12.3 add a post-`gamora geometries` step: "[elrond: corpus-align] le-frost-wall-rm re-classify + TH bucket-tag + V10 census update — single-writer discipline preserved."

### MINOR-7 — §5.1 orbit_projectile_count = 4 default vs D2/D4 typical N
`d3-inarius-bonestorm` narrative says "4 bone shards"; `poe1-poison-bv` canonical PoE1 is 6 blade projectiles at 20-quality unbuffed. Default `orbit_projectile_count=4` is D3-canonical but low for poison-BV lineage. Non-blocking (gamora tunes within band 1-8), but a math-note in §13.5 stating "N default is D3-canonical; PoE1 BV uses N=6 typical — gamora may re-default per S6 gauntlet response" would preserve the discipline.

---

## NOTE-level (record, no action owed)

### NOTE-8 — §2.5 mark-of-a-mark corpus-inspection claim uncorroborated
§2.5 line 221 states "raw_json inspection of the 20 ailment kits — no `mark-of-a-mark` construct present." Claim is anchored to gandalf's inspection but no separate audit trail (DB query, script output). For a LOCKED invariant (MAX_CHAIN_DEPTH=1), the empirical grounds should have a reproducible artifact. For the record; not a defect.

### NOTE-9 — DRIFT-CRITIC WC-13..WC-21 concurrence sound
All 8 rulings concur with SPEC-AUTHOR LEANs on cited grounds. WC-21 STRIKE grounds (Discipline #13 drift-by-residue) are technically sound but the ruling exposes MAJOR-2 blast-radius scope. WC-13..WC-20 grounds are technically sound with no knock-on scope issues. No dissent-notes to record; per-ruling concur-with-grounds notes carried in the decisions-log entries drafted alongside this finding.

### NOTE-10 — §12.7 census-delta arithmetic verified
V9 baseline `509/565 = 90.1%` ✓. Gate-lift math `8+4+4+2+1+8+6+3+3+3 = 42` ✓. Floor `509+40=549 / 565 = 0.9717 = 97.2%` ✓. Ceiling `509+42=551 / 565 = 0.9752 = 97.5%` ✓. DRIFT-CRITIC correction #4 (naming the floor + the two contingent kits d2-smiter/d2-zealot) is arithmetically clean and improves projection honesty per Discipline #11 (empirical inspection).

---

## References
- Spec under review: `canonical/reap-die-rise-engine/wave-c-trigger-mark-engine-spec.md` @ `f2511469`
- Companion specs verified: `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (house model), `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (§7 matrix pattern)
- Census verified: `agentic_orchestration/research/curated/atlas/s2-readiness-census-v9-2026-07-16.md` (blind 8 / curse-hex 4 / fear 4 / deflect 2 / instant-kill 1 / unknown-ailment 1 / BT 8 / orbit 6 / walls 3 / LC 3 / DR 2 / TH 3 all match)
- Engine code (read-only): `bc_target_cell_sampler.py:391-395` (972-assert LIVE); `bc_target_composer.py:238-287` (resolver contract); `bc_target_composer.py:248-260` (map); `skill_schema.py:222-227` (persistent_toggle + persistent_trigger commitment_bins live post-Wave-B); `gear_generation.py:606` (`_ALL_ROLE_ORIENTATIONS`)
- decisions-log entries drafted: `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — WC-13 through WC-21 + DRIFT-CRITIC gate stamp + Gate-1 verdict entries appended.

---

**Signed:** jack-ryan (Gate-1 DESIGN-MODE) — spec is buildable with 3 MAJOR fold-in amendments (contract widen, blast-radius, byte-neutrality clause); 4 MINOR text polish; 3 NOTE-level record-only. No BLOCK. DRIFT-CRITIC rulings WC-13..WC-21 concur.
