# Finding — 2026-06-22 — proxy-gen-prereqs-G1-G2-gate2

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-CONCERNS (no BLOCK; one WARN, two INFO)
**Target:** engine commit `795f24a`, tag `rocket/v-proxy-gen-prereqs-1` (push held)
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #2, #11, #12; ADR-004, ADR-006

## Verdict

**PASS-WITH-CONCERNS. The `proxies` surface IS cleared for gamora W2 to consume.** All seven gate
teeth verified first-hand (Discipline #11 — nothing taken on rocket's faith). The surface is genuinely
always-empty on current kits (solo-safe) and genuinely consumable by the real sim consumer
`entity_from_proxy_dict`. Concerns are forward-looking notes for W2, not blockers.

## What I found

Every load-bearing claim holds under first-hand verification.

**Tooth 1 — G-SOLO byte-identical (the load-bearing one).** CLEARED. I built a real `PlayerClassV2`
via the test fixture and called `to_dict()`: `"proxies"` is present, is a list, is `[]`, and the dict
JSON-round-trips clean. The mechanism is sound: `build_proxies_surface(self.skills)` returns `[]` when
`skills is None`, and `skills` is `None` on every current kit (pre-Layer-3). Even post-Layer-3, the
`_summon_proxy_fields` discriminator (`proxy_geometry`/`proxy_acquisition` both None → skip) keeps a
non-summon skill from emitting a decl. No current path can emit a populated `proxies`. Empty list →
sim `proxy_decls=[]` → solo path byte-identical (sim §6 criterion #1). NOT a content-emission breach.

**Tooth 2 — no bin un-deferred.** CLEARED. `_DEFERRED_PROXY_BINS = {"proxy-light","proxy-heavy"}`
(`bc_target_composer.py:97`) is UNTOUCHED — `git show 795f24a -- bc_target_composer.py` is an empty diff;
the file is not in the commit's 6-file set at all. `grep -rl '"proxies"' exports/` = 0. Machinery only.

**Tooth 3 — consumable by the REAL sim consumer.** CLEARED. The smoke round-trips all five bands
(melee/ranged/aura/capture/circle) through the actual `entity_from_proxy_dict` — not a mock — with no
raise; aggro_fraction resolves correctly (taunt→0.6). I confirmed the emitted decl keys are exactly the
set `entity_from_proxy_dict` reads off the dict. The bridge imports `PROXY_TYPE_TIER` and
`DEFAULT_ATTACK_INTERVAL_S` from the sim module (not duplicated), so it stays in lock-step with the
consumer's authoritative type set.

**Tooth 4 — SCAFFOLD-vs-FINAL boundary.** CLEARED. MIGRATION.md (lines 76-80) names the four magnitude
fields gamora calibrates in W3 (`damage_multiplier`, `base_hp`, `proxy_max_active`, `attack_interval_s`)
vs the six rocket-final identity/translation fields. Boundary is explicit and correct; W2/W3 will not
re-derive the wrong half.

**Tooth 5 — proxy_type always-valid-or-RAISES.** CLEARED. `select_proxy_type` has an explicit valid
default branch (`passive_fighter`), so it cannot return an unknown type; `proxy_decl_from_summon` then
re-checks membership in `PROXY_TYPE_TIER` and RAISES `ValueError` if violated (defense-in-depth mirroring
the consumer's P7 fail-loud). I verified all 14 entries of `PROXY_TYPE_TARGETING` are members of
`PROXY_TYPE_TIER` (zero orphans) — so no derived targeting can reference a type the sim would reject.

**Tooth 6 — G3 NOT built.** CLEARED. The bridge carries the `acquisition="capture"` label and selects a
valid `proxy_type` (`passive_fighter`) plus the `max_active=1` trophy override, but builds NO mob-side
capturable tag and NO stat-inheritance rule. No G3 leaked in.

**Tooth 7 — tests/smoke.** CLEARED. Smoke ALL-PASS (40 checks). `pytest -k "bc_target_subspace or proxy"`
= 39 passed, 0 failed. The 45 `test_cycle12_layer4/6` failures are genuinely PRE-EXISTING and unrelated:
I read the traceback — they fail in the retired `SkillTreeGenerator.generate()` (a dead b6-era construct),
not in any proxy path. The `proxies` key is net-new vs the parent commit (`795f24a~1` had 0 references to
`build_proxies_surface`), so this commit introduced no regression into those suites.

## Rationale

Discipline #1 satisfied — math note authored before code, §§ keyed to the gen addendum, all magnitudes
declared SCAFFOLD with the bound each helper enforces. Discipline #2 — smoke exercises the real consumer.
Discipline #11 — every rocket claim re-verified first-hand, not accepted on report. Discipline #12 — the
semantic-shift declaration is honest (purely additive; one new key; no existing field changes meaning).
ADR-004 cross-seam contract (MIGRATION.md) is present and complete. ADR-006 push correctly held.

## Concerns (non-blocking)

**WARN-1 — spawner-side fields are not yet round-trip-validated.** The smoke round-trips the
`ProxyCombatant`-constructor half (`proxy_type`/`base_hp`/`damage_multiplier`/`range_m`/`targeting`/
`attack_interval_s`). It does NOT validate the six decl-LEVEL population fields (`geometry`,
`proxy_max_active`, `count`, `duration_s`, `spawn_cadence_s`, `acquisition`) against a real consumer,
because the population spawner that reads them is gamora's W2 code and does not exist yet. The decl
carries them correctly (verified by inspection), but their consumption contract is asserted by MIGRATION,
not yet exercised. This is by design per the dispatch (the population-spawner round-trip is explicitly
W2's job) — flagging so W2 owns validating its half of the seam rather than assuming it's pre-tested.

**INFO-1 — `aura` range asymmetry is intentional but a foot-gun.** `geometry_to_range_m("aura")` returns
`5.0`, NOT `0.0`, because `aura` is in BOTH `_SUPPORT_GEOMETRIES` and `PROXY_GEOMETRY_RANGE_M`, and the
line-195 guard (`and geometry not in PROXY_GEOMETRY_RANGE_M`) deliberately keeps the radial reach. Only
true no-attack-shape geometries (`none`, `totem`, `self_buff`) hit the `0.0` path — verified empirically.
This is correct (an aura has a radius), but the math-note phrasing "no-attack-shape → 0.0" reads as if
`aura` would be 0.0. Worth a one-line clarification if rocket touches the note again; not blocking.

**INFO-2 — `geometry` and `behavioral_tier` are redundant-but-explicit.** The sim defaults
`behavioral_tier` from `PROXY_TYPE_TIER[proxy_type]` and never reads `geometry` in
`entity_from_proxy_dict`. The bridge emits both explicitly for round-trip clarity / spawner use. Harmless;
noted only so W2 knows `geometry` is informational at the constructor level.

## Action
- [x] jack-ryan: Gate-2 review complete; surface CLEARED for gamora W2 consumption.
- [ ] gamora (W2): consume the `proxies` SHAPE; the surface is `[]` on every current kit until Matt lifts
      the bin (consume shape, not populated data). Validate the six decl-LEVEL spawner fields against your
      population-tracker code — that half of the seam is not yet round-trip-tested (WARN-1).
- [ ] gamora (W3): calibrate ONLY the four SCAFFOLD magnitude fields (`damage_multiplier`, `base_hp`,
      `proxy_max_active`, `attack_interval_s`); do NOT touch the rocket-final translation/identity fields.
- [ ] rocket (optional, non-blocking): clarify the math-note §3 "no-attack-shape → 0.0" line so it does
      not read as applying to `aura` (which correctly returns 5.0).

## References
- `src/reincarnated/generation/proxy_vocabulary_bridge.py` (G1+G2)
- `src/reincarnated/generation/bc_target_player_class.py:409-415` (`to_dict()` wire-in)
- `src/reincarnated/generation/math/proxy-gen-prereqs-G1-G2-math-2026-06-22.md`
- `src/reincarnated/generation/MIGRATION.md` (2026-06-22 entry — cross-seam contract)
- `src/reincarnated/simulation/spatial_gauntlet/proxy_population.py:259-324` (consumer `entity_from_proxy_dict`)
- `src/reincarnated/generation/bc_target_composer.py:97` (`_DEFERRED_PROXY_BINS` — verified untouched)
- `scripts/rocket_proxy_gen_prereqs_smoke_2026_06_22.py` (smoke — ALL-PASS, 40 checks)
- `agentic_orchestration/dispatches/2026-06-22-rocket-proxy-gen-prereqs-G1-G2.md` (acceptance)
