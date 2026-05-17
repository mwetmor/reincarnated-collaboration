# 2026-05-17 — rocket — earth.yaml AVOID declarations + roles.yaml DPS-floor audit

**Authority:** Phase-1 P1 hive-mind L1 (rocket in-seam; substrate identity loader + role registry are rocket-owned).
**Type:** Pattern A (short task) — micro-task; ~1-2 hours total.
**Trigger:** Gamora D3 ship (tag `gamora/v1.4-d3-path-a-impl-1` @ `048611a`) surfaced two upstream issues during WP-9 smoke + Discipline #12 audit.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — gamora D3 SHIP STATE + HANDOFF entries (most recent; 6-item HANDOFF → jack-ryan; rocket micro-task surfaced inline)
2. `reincarnated-engine/src/reincarnated/generation/math/d3-path-a-archetype-composition-phase-1-p1.md` § 5 (multi-stat-to-floor) + § 8 (smoke baseline + WP-9 expectations)
3. `reincarnated-engine/config/substrate_identities/earth.yaml` — current declaration (in scope for amendment)
4. `reincarnated-engine/config/roles.yaml` — current declaration (in scope for audit)
5. `reincarnated-engine/src/reincarnated/generation/archetype_composer.py` — gamora's composition algebra (read-only for context); particularly `_check_constraint_tag_affinities` if present

---

## Issue 1 (PRIMARY) — earth.yaml missing AVOID declarations

**Symptom:** WP-9 smoke regression: earth_caster substrate-affinity score dropped from 0.525 (pre-D3) → 0.1688 (post-D3).

**Root cause (per gamora analysis):** earth.yaml is missing two `forbidden_mechanics` AVOID declarations:
- `fork: AVOID`
- `ricochet_bounce: AVOID`

Composition algebra is correct. The substrate identity declaration is incomplete — when the composer queries `earth.forbidden_mechanics` it returns a partial set, and the resulting AVOID set under-represents earth's cosmological identity. The smoke score correctly drops because the kit-shape vector that should land at "positional refusal / unyielding" instead allows projectile-fork and projectile-ricochet patterns that contradict that identity.

**Cosmological framing (per substrate-identity-declarations-2026-05-17.md § 3 earth):** earth is positional refusal; *the substrate of can-I-be-here being answered yes-and-so-can-what-stands-with-me.* Forking and ricocheting patterns are explicitly anti-earth — they spread the engagement laterally rather than holding the position. Adding these to AVOID brings the declaration into alignment with the cosmology the rest of earth's fields already describe.

**Actions:**
- Edit `config/substrate_identities/earth.yaml`:
  - Add `fork: AVOID` to `forbidden_mechanics`
  - Add `ricochet_bounce: AVOID` to `forbidden_mechanics`
- Validate via substrate_identity_loader (your existing 10 fail-loud rules)
- Re-run WP-9 smoke against earth_caster — expectation: score returns to 0.525 range (pre-D3 baseline)
- If smoke still doesn't recover, surface as QUESTION → gamora in hive log (algebra issue beyond substrate declaration); do NOT defer-resolve yourself.

---

## Issue 2 (SECONDARY) — roles.yaml DPS-floor tag placement audit

**Symptom (per gamora Discipline #12 finding):** During D3 implementation, gamora discovered that `min_4_dps_skills` and `min_1_dps_aoe` constraint tags appearing in `burst_damage` + `area_damage` `constraint_tag_affinities` blocks were propagating to **ALL DPS archetypes** when they should be **wind_controller-specific DPS floor guards.**

Gamora fixed the propagation in composition: DPS role affinities not propagated; control role mandatory tags include them explicitly. **But:** gamora left a note suggesting that `roles.yaml` itself may have these tags placed under the wrong role entries (the propagation source).

**Actions:**
- Inspect `config/roles.yaml`:
  - Find `min_4_dps_skills` and `min_1_dps_aoe` entries — confirm which role(s) they appear under
  - Cross-check against gandalf D8 trait-floor design + canonical/32-progression-design.md to determine which role(s) should legitimately own these tags
  - Expected outcome (per gamora hypothesis): these belong to `controller` role (or specifically to a control-role variant tied to wind), NOT to `burst_damage` or `area_damage` (DPS roles)
- If misplacement confirmed:
  - Move the tags to the correct role entries
  - Validate via role registry loader (your existing rules)
  - Surface the schema correction in MIGRATION.md (Discipline #12 semantic shift — DPS roles no longer carry these floor guards via affinity propagation)
- If placement is intentional (e.g., docs justify it):
  - Document the rationale in roles.yaml as a comment + surface to gamora in hive log as INFO; gamora may want to revisit composer affinity-propagation logic

---

## Cross-seam impact

- **Gamora D10 code phase** depends on these two issues being resolved. D10 substrate-coherent generation rules consume both substrate forbidden_mechanics + role constraint_tag_affinities. If either is malformed, D10 algorithm under-discriminates.
- **Jack-ryan checkpoint review** (separately dispatched) will examine the WP-9 closure after this micro-task lands. Coordinate timing if possible: rocket lands earth.yaml + roles.yaml fixes BEFORE jack-ryan re-runs WP-9 smoke.

---

## Out of scope (DO NOT)

- ❌ DO NOT modify `archetype_composer.py` (gamora-owned)
- ❌ DO NOT modify other substrate_identities/*.yaml (only earth.yaml is in scope for amendment)
- ❌ DO NOT modify gandalf D8 trait-floor pools or canonical-four pools (gandalf-owned)
- ❌ DO NOT extend scope to add other AVOID/PREFER declarations beyond fork + ricochet_bounce (additional cosmological tuning is separate work; surface as QUESTION if you notice other gaps)

---

## Acceptance criteria

- [ ] `config/substrate_identities/earth.yaml` updated with `fork: AVOID` + `ricochet_bounce: AVOID`
- [ ] WP-9 smoke against earth_caster: score in 0.45-0.55 range (pre-D3 baseline restoration)
- [ ] `config/roles.yaml` audited; `min_4_dps_skills` + `min_1_dps_aoe` placement either corrected or documented-rationale-preserved
- [ ] If schema correction made: MIGRATION.md entry authored per Discipline #12
- [ ] Hive-log STATE entry appended documenting both fixes
- [ ] Tag `rocket/v1.5-earth-yaml-amend-and-roles-dps-audit-1` (or similar seam-prefixed)

---

## Smoke test expectation

- All substrate_identity_loader fail-loud validation rules continue to pass (10 rules)
- All role registry loader rules continue to pass
- WP-9 smoke for earth_caster restored to pre-D3 baseline (0.45-0.55 range)
- Other 6 substrates: WP-9 smoke unchanged (you're only touching earth.yaml + roles.yaml)
- Full test suite passes (348 sim tests + 68 gamora D3 tests + 54 star-lord D15 tests + rocket existing tests)

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 race-condition discipline gandalf authored this session): `git fetch origin` first; conflict-check; pull-rebase if concurrent commits.

---

## Tag intent

`rocket/v1.5-earth-yaml-amend-and-roles-dps-audit-1` — seam-prefixed intermediate tag.

---

*Dispatched 2026-05-17 by knight-rider per auto-dispatch authority + gamora HANDOFF (post-D3 ship). Estimated 1-2 hours total. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `rocket/v1.5-earth-yaml-amend-and-roles-dps-audit-1` @ `cd9e913`
**Engine commits:** `cd9e913` (config fixes + MIGRATION.md), `c1639b1` (AGENT_STATE)
**Collab commit:** `cb6f468` (hive log STATE)

### Issue 1 (PRIMARY) — RESOLVED

`config/substrate_identities/earth.yaml`: Added `fork: AVOID` + `ricochet_bounce: AVOID` to `geometry_affinities`. Substrate_identity_loader validation passes (all 7 substrates). WP-9 smoke: earth_caster modifier restored 0.1688 → **0.5250** (acceptance range 0.45–0.55). CLOSED.

### Issue 2 (SECONDARY) — RESOLVED

`config/roles.yaml`: Removed `min_4_dps_skills` + `min_1_dps_aoe` from `burst_damage`, `area_damage`, `damage_over_time` affinities. Added to `control` affinities with inline documentation. Role_registry_loader validation passes (all 9 roles). Runtime behavior unchanged (gamora D3 composer already skips DPS role affinities). Jack-ryan post-D3 INFO item on roles.yaml cleanup CLOSED.

### Smoke results

- WP-9 earth_caster: **0.5250** (PASS)
- 312 substrate + role + D3 composer tests: **ALL PASS**
- MIGRATION.md §v3.1 entry authored

### Acceptance criteria

- [x] `config/substrate_identities/earth.yaml` updated with `fork: AVOID` + `ricochet_bounce: AVOID`
- [x] WP-9 smoke against earth_caster: score 0.5250 (in 0.45–0.55 range)
- [x] `config/roles.yaml` audited; `min_4_dps_skills` + `min_1_dps_aoe` moved to `control`
- [x] MIGRATION.md entry authored per Discipline #12
- [x] Hive-log STATE entry appended
- [x] Tag `rocket/v1.5-earth-yaml-amend-and-roles-dps-audit-1` cut and pushed
