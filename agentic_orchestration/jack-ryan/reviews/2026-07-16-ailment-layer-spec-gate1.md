# Finding — 2026-07-16 — ailment-layer engine spec Gate-1

**Reviewer:** jack-ryan (DESIGN-MODE, critique-pair with gandalf-prime)
**Severity:** PASS-WITH-AMENDMENTS
**Target:** `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (drafted by gandalf SPEC-AUTHOR unit, autonomous atlas-parity run)
**Author:** gandalf-prime (SPEC-AUTHOR); five §10 rulings under Matt autonomous-run delegated authority
**Principles applied:** Review Principle #1 (math-before-code), #2 (smoke-gate discipline), #3 (cross-seam impact), #5 (severity matters); Disciplines #1 (math-before-code), #11 (two-seam interaction), #12 (semantic-shift declaration)

## What I found

Spec is architecturally sound, evidence-anchored, correctly identifies all seam sites, and its five §10 rulings each carry principled grounds. Reviewed against post-Wave-A engine reality (commits 4a70547 / 7aeb2a6 / 4fdd314 / 43fa149) — no drift with landed proxy layer. Three real defects and five precision gaps: (1) sunder §2.6 stacking law contradicts itself (single-instance vs summed-cap — math-consistency BLOCK if unaddressed); (2) taunt-annex §6.5 misnames `PROXY_TYPE_BEHAVIOR` (actual map is `PROXY_TYPE_TARGETING`, string-valued, would break existing consumers if extended to dict); (3) §7 interaction table missing hard_control × sunder family (the tentpole "unload while locked" pattern §10-b explicitly names). Applied 8 text-level amendments inline; no rulings challenged.

## Per-focus-area results

1. **Resolution-site correctness (§2.8/§3.6):** PASS with precision amendment. Sunder → `damage_resolver.resolve_skill` composition point (verified line 322-324 buff composition seam). Shatter → `effect_resolver.tick_effects` expiry path, but shatter check must fire BETWEEN duration-decrement (line 59) and expiry-cull (line 95) — amended §3.6 to make placement explicit.

2. **ailment_loader schema fit (§2.3/§2.4/§3.3/§4.3/§5.3):** PASS. `VALID_CATEGORY_VALUES` at `ailment_loader.py:69-75` confirms `"debuff"` reserved; `param_ranges` structure with min/max/default matches R8 validation at line 259-289; `is_control ∈ {hard, soft, none}` matches R6 at line 230. Loader R3 uses `CANONICAL_AILMENT_NAMES - seen_names` which passes when new names ADD to seen — new ailments extend cleanly. R10 checks specifically for the 3 Phase-1 P1 new names — untouched. Note for build phase: rocket must extend `CANONICAL_AILMENT_NAMES` in `ailment_loader.py:38` to include the 4 new names, else R3 passes but code intent drifts.

3. **Refresh-law consistency (§2.6/§3.5/§5.5):** PASS with §2.6 defect resolved. F3 DoT-refresh law at `damage_resolver.py:1075-1087` (max(existing, incoming) duration + max tick_damage for DoTs). Poison's independent-stack model correctly requires a NEW `_add_poison_stack` path per §5.6 — cannot reuse `_add_or_refresh`, spec acknowledges this. Freeze/stun single-instance refresh compose with the existing law. Sunder §2.6 defect: original wording proposed BOTH single-instance-per-target AND cross-source `min(cap, sum_of_active_amps)`. Contradiction — if single-instance, sum has one term. Amended to (option 2): single-instance + max-magnitude refresh + cap as parameter-drift invariant.

4. **DPS-composition guards (§7):** PASS with clarification amendment. Sunder cap semantics resolved via §2.6 amendment (max-magnitude, not sum). consecrate×sunder claim of "triple-multiplicative" in original §7 was DOUBLE-multiplicative on precise read (consecrate DoT tick × sunder amp; the shadow-target rule is inside consecrate's own valenced logic, not a separate multiplier) — amended. poison×sunder multi-tick amp is correctly identified as watch-item under §5.8 stack-cap guard.

5. **§11 toxic_cloud DL-03 flag:** PASS with rocket-binding amendment. `substrate_templates.py` has an established `tags=["placed"]` convention for zone effects (`bomb_mine`, `turret`, `totem`, `zone_teleport_shadow`, `sentinel`, `wall`, `wind_cyclone_zone`, `holy_sanctify_zone`) distinct from `tags=["channel"]` caster-held family (`hp_cost_channel_*`). Amended §5.9 to bind rocket to `tags=["placed"]` explicitly — no ambiguity for build.

6. **Taunt annex vs landed Wave-A reality (§6.5):** PASS with rename amendment. `proxy_vocabulary_bridge.py` actual maps are `PROXY_TYPE_TIER: dict[str, int]` and `PROXY_TYPE_TARGETING: dict[str, str]` with values in `{nearest, player_target, taunt, intercept, positional, proximity, none}`. `golem_construct` already has `targeting_behavior="taunt"`. There is NO `PROXY_TYPE_BEHAVIOR` map. Amended §6.3 and §6.5.1 to specify a NEW parallel map `PROXY_TAUNT_PRIORITY: dict[str, float]` — do NOT mutate `PROXY_TYPE_TARGETING` to dict-valued (would break string-consumers of the existing shape). spatial_engine.py exists at 4313 lines (Wave-A landing confirmed by size) — nav-selection consumer touchpoint per §6.5.2 remains valid.

7. **Interaction table completeness (§7):** WARN → resolved by amendment. Original table missed the hard_control × sunder family (freeze/stun/root/shock × sunder). §10 ruling (b) rationale explicitly names this pattern ("unload while locked; the burst is earned by pushing the target under threshold during the freeze") as the design purpose of freeze — but §7 only showed freeze × shatter and sunder × sunder. Added freeze × sunder (tentpole), stun × sunder, root × sunder, shock × sunder, plus poison × freeze (referenced §5.10 but missing from table).

8. **Emission-surface realism (§2.5/§2.9):** PASS. `element_biases.py` is only 117 lines; ELEMENT_AILMENT is a single-value map (single ailment per element). No existing `SECONDARY_AILMENT_MAP` — clean addition. `geometry_derivation.py` `_control_effects` at line 238 and `_damage_effects` at line 239 are the correct seams; drain-in-control-set is a pre-existing inconsistency (drain is category=dot, is_control=none but appears in `_control_effects` for filter-disqualify purposes). Amended §5.7 to explicitly guard rocket against replicating the drain pattern for poison.

## Amendments applied (8 total, all in `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md`)

1. **§2.6 Sunder stacking law** — resolved single-instance-vs-summed-cap contradiction. Single-instance + max-magnitude refresh + cap-as-invariant. Cited `damage_resolver.py:1075-1087` for F3 lineage.
2. **§3.6 Shatter placement precision** — added between-decrement-and-cull placement rule (between `effect_resolver.py:59` and `:95`).
3. **§5.7 Poison geometry** — added guard against putting poison in `_control_effects` (drain's pre-existing inconsistency does not propagate).
4. **§5.9 Toxic_cloud DL-03 binding** — bound rocket to `tags=["placed"]` per existing zone-template precedent.
5. **§6.3 Taunt Representation A** — corrected `PROXY_TYPE_BEHAVIOR` → NEW parallel `PROXY_TAUNT_PRIORITY: dict[str, float]` map. Verified against `proxy_vocabulary_bridge.py:83-86` post-Wave-A.
6. **§6.5.1 Taunt rocket authorship** — matched §6.3 correction.
7. **§7 Interaction table** — added freeze × sunder (tentpole), stun × sunder, root × sunder, shock × sunder, poison × freeze; corrected sunder × sunder line to REFRESHES single-instance; corrected consecrate × sunder from triple- to double-multiplicative.
8. **§11 DL-03 conformance note** — marked toxic_cloud RESOLVED at §5.9.

Additional: STATUS stamp updated from "draft-for-Gate-1" to "Gate-1 PASS-WITH-AMENDMENTS" with jack-ryan attribution + 2026-07-16 date + amendment section anchors.

## Rulings challenged

**None.** Reviewed all five §10 rulings:
- (a) `debuff` category — correct; reserved slot exists precisely for this class; new category duplicates concept space.
- (b) expiry-under-threshold shatter — grounds are strong (verb-collision with sunder if on-hit; execute-setup pattern preserves PoE2 Ice Strike two-phase loop). Concur.
- (c) hybrid stun DR — solo-ARPG-shape (D3 elite CC-reduction / LE boss resist) is the right precedent set, not MMO stack-DR. Concur.
- (d) independent-stack poison — matches PoE1 build-craft the closest. Concur.
- (e) proxy-AI directive taunt — 10/11 gap kits are proxy-hosted; Thorns-class self-taunt is a player build-modifier on the SAME nav consumer. Concur (with §6.3/§6.5.1 correction on target map).

No evidence supports overturning any ruling. Any of them may still be reversed by Matt on read; that is the veto-open condition, not a Gate-1 defect.

## Action

- [x] Amendments applied inline to spec.
- [x] STATUS stamp updated.
- [ ] rocket: extend `ailment_loader.CANONICAL_AILMENT_NAMES` at build-time to include 4 new names (spec §1 build phase); loader currently passes R3 but frozenset intent drifts if not extended.
- [ ] rocket: use `tags=["placed"]` for `toxic_cloud` template per §5.9 binding.
- [ ] rocket: add NEW `PROXY_TAUNT_PRIORITY` map per §6.3/§6.5.1 (do NOT mutate `PROXY_TYPE_TARGETING`).
- [ ] gamora: sunder cap enforced as invariant on single ActiveEffect, not summed across actives (§2.6 amended).
- [ ] gamora: shatter check placed between `effect_resolver.py:59` decrement and `:95` cull (§3.6 amended).
- [ ] Matt: five §10 rulings remain veto-open per autonomous-run authority; one-word overturn on any is preserved.

## References

- Spec (amended): `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md`
- `/Users/admin/Games/reincarnated-engine/config/ailments.yaml` (registry state)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/foundation/ailment_loader.py:38,69-75,308,317` (schema)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:322-324,996-1053,1056-1092` (sunder site, apply, refresh)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py:39,42-96` (tick + expiry)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:65-74,89-102,105-117` (emission surface)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/geometry_derivation.py:238-239` (effect sets)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/proxy_vocabulary_bridge.py:83-86` (Wave-A taunt shape)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/substrate_templates.py` (`tags=["placed"]` precedent)
- Wave-A DEV-MODE finding: decisions-log lines 5751-5813
- Wave-A commits: 4a70547, 7aeb2a6, 4fdd314, 43fa149; pushed 4929c6c
