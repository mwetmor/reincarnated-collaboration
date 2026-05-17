# 2026-05-17 — rocket — Narrow-slice engine schema fields (windup_duration_seconds + indicator_color_hex)

**Authority:** Gandalf L3 § 7 binding decision (PARTIAL Phase-1 P1 extension; narrow slice per § 5.1) per Matt standing delegation 2026-05-17.
**Type:** Pattern B (long task) — ~1 day.
**Predecessor:** gandalf L3 briefing (`gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` @ `3ec108f`).
**Seam:** generation + foundation (rocket; substrate identity loader + schema extensions). No simulation work (gamora consumes later); no demo work (drax consumes later).

---

## Why this matters

Narrow-slice Phase-1 P1 extension lands telegraphed combat + engine-coupled dodge. Two new engine schema fields are required as **inputs to both gamora's reactive escape AI work AND drax's enemy-AOE ground-indicator rendering**. Schema fields must land FIRST so the downstream simulation + render work can consume them.

These are simple additive schema extensions to `substrate_identities/*.yaml` + the substrate identity loader. No mass-rewrite; no migration of existing data.

---

## Required reading (in order)

1. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — full briefing; § 3 (Telegraphed AOE windup system) authoritative for per-substrate defaults; § 5.1 (this work in scope)
2. `canonical/story/substrate-identity-declarations-2026-05-17.md` — all 7 substrate declarations; you'll extend each
3. `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` — your existing loader; 10 fail-loud validation rules
4. `reincarnated-engine/config/substrate_identities/*.yaml` — all 7 YAMLs in scope for extension
5. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — most recent gandalf STATE entry on the L3 briefing

---

## Scope

### Item 1 — Engine schema field additions

Add 2 new fields to substrate identity declarations:

- **`windup_duration_seconds`** (float) — default AOE windup time for this substrate's skills (per-substrate cosmological character)
- **`indicator_color_hex`** (string, format `#RRGGBB`) — ground-indicator color for this substrate's AOEs

**Per-substrate defaults per gandalf briefing § 3.2 (cosmological character):**

| Substrate | windup_duration_seconds | indicator_color_hex | Rationale |
|---|---|---|---|
| fire | 0.6 | `#E85D24` | Escalation = building-up windup; player reads charge |
| water | 0.7 | `#3B8EE0` | Pervading presence = tide-rise from center over time |
| earth | 0.4 | `#8B5A2B` | Positional refusal = anchor + persist (shorter windup; longer duration handled separately) |
| wind | 0.5 | `#A3D9E0` | Kinetic rearrangement = telegraphs direction (medium windup) |
| lightning | 0.5 | `#F2D027` | Instant arc + chain windup (medium windup; chain re-telegraph elsewhere) |
| holy | 0.7 | `#F5D061` | Slow radiant build-up = bright cosmological accumulation |
| shadow | 0.2 | `#3D2C4E` | Hidden-until-commit = late-telegraph (gandalf judgment: 0.2s; still telegraphed but smallest reactive window) |

**Validation:**
- Add fail-loud rule (rule #11): `windup_duration_seconds` MUST be present + float in [0.0, 5.0] range
- Add fail-loud rule (rule #12): `indicator_color_hex` MUST be present + match regex `^#[A-Fa-f0-9]{6}$`
- Cross-check: indicator_color_hex per substrate should match (or be cosmologically coherent with) the drax-loadout vfx-manifest grouping-vocab color palette (per drax v0.28 hotbar overhaul work)

### Item 2 — Substrate identity loader extension

- Extend the `SubstrateIdentity` dataclass / model with the 2 new fields
- Update loader to populate them from YAML
- Add the 2 new fail-loud validation rules per above
- Update export `__init__.py` if needed so the fields are accessible to consumers

### Item 3 — Tests

- Add unit tests for the 2 new fields
- Add unit tests for the 2 new fail-loud rules (missing field; out-of-range value; invalid hex format)
- Run full substrate_identity_loader test suite — confirm 12 rules pass (was 10; now 12)

### Item 4 — MIGRATION.md

- Author `generation/MIGRATION.md` §v3.2 entry documenting:
  - Schema additions (Discipline #12 semantic shift)
  - Per-substrate default values + cosmological rationale
  - Consumer obligations (gamora narrow-slice escape AI + drax narrow-slice indicator rendering both consume these fields)
  - Discipline #1 (math-before-code): N/A; this is schema extension, not new mechanic

---

## Out of scope (DO NOT)

- ❌ DO NOT implement i-frame mechanics or dodge engine-coupling — that's drax + rocket joint later
- ❌ DO NOT implement AOE windup mechanics in simulation — that's gamora later
- ❌ DO NOT modify simulation, demo, or loadout files
- ❌ DO NOT modify D8/D9 trait pools, role definitions, or ailment registry
- ❌ DO NOT extend scope to other schema fields (per-substrate-dodge-tweak fields per § 6.7 briefing note are LATER; this dispatch is just the 2 indicator-related fields)
- ❌ DO NOT touch gamora's archetype_composer.py or any simulation code

---

## Acceptance criteria

- [ ] All 7 substrate_identities YAMLs extended with `windup_duration_seconds` + `indicator_color_hex` per the table above
- [ ] `SubstrateIdentity` dataclass extended; loader populates new fields
- [ ] 2 new fail-loud validation rules (rule #11 windup + rule #12 hex) added; existing 10 rules continue to pass
- [ ] Unit tests added for new fields + new rules
- [ ] Full test suite passes (substrate_identity_loader + cross-seam D3 composer + everything else)
- [ ] `generation/MIGRATION.md` §v3.2 entry authored
- [ ] Hive-log STATE entry appended
- [ ] Tag `rocket/v1.7-narrow-slice-engine-schema-fields-1`

---

## Smoke test expectation

- `python -c "from reincarnated.foundation import load_substrate_identities; ...print field values"` for all 7 substrates returns sensible defaults
- Validation rules fail correctly when test YAML is malformed
- D3 composer + class generator continue working (additive change should not break them)

---

## Cross-seam impact

- **Gamora narrow-slice escape AI work** consumes `windup_duration_seconds` per substrate when computing AOE timing for player-AOE → reactive-escape detection. Schema must land first.
- **Drax narrow-slice indicator rendering** consumes `indicator_color_hex` + `windup_duration_seconds` per substrate when rendering ground indicators. Schema must land first.
- **Drax v0.28 hotbar overhaul** (in flight) may also consume `indicator_color_hex` for substrate-colored skill frames if not yet derived from D20 grouping vocab. Either source works; drax may want to standardize on one path post-this-dispatch.

---

## Math-before-code requirements

N/A — schema extension; no new mechanic math. Discipline #1 not triggered.

---

## Tag intent

`rocket/v1.7-narrow-slice-engine-schema-fields-1` — seam-prefixed; single commit per ADR-006.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Dispatched 2026-05-17 by knight-rider per gandalf § 7 binding L3 decision + Matt standing authority. Estimated 1 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `rocket/v1.7-narrow-slice-engine-schema-fields-1 @ 7bcfb0a`
**Agent:** rocket (Claude Sonnet 4.6)

### Acceptance criteria — ALL MET

- [x] All 7 substrate_identities YAMLs extended with `windup_duration_seconds` + `indicator_color_hex` per the dispatch table
- [x] `SubstrateIdentity` dataclass extended; loader populates new fields from YAML at root level
- [x] 2 new fail-loud validation rules (rule #11 windup + rule #12 hex) added; existing 10 rules continue to pass (146/146 tests green)
- [x] Unit tests added for new fields + new rules (25 new tests: `TestWindupDurationSeconds` + `TestIndicatorColorHex`)
- [x] Full test suite passes (substrate_identity_loader 146/146 + cross-seam targeted suite 398/398)
- [x] `generation/MIGRATION.md` §v3.2 entry authored (consumer obligations for gamora + drax; design invariants; deferred forward-work)
- [x] Hive-log PRE-SIGNAL + STATE + TAG entries appended
- [x] Tag `rocket/v1.7-narrow-slice-engine-schema-fields-1` cut (local; push on Matt authorization)

### Canonical values per gandalf briefing § 3.2

| Substrate | windup_duration_seconds | indicator_color_hex |
|---|---|---|
| fire | 0.6 | `#E85D24` |
| water | 0.7 | `#3B8EE0` |
| earth | 0.4 | `#8B5A2B` |
| wind | 0.5 | `#A3D9E0` |
| lightning | 0.5 | `#F2D027` |
| holy | 0.7 | `#F5D061` |
| shadow | 0.2 | `#3D2C4E` |

### Notes

**Consumer readiness:** Gamora and drax can now consume the new fields. See `generation/MIGRATION.md` § v3.2 for access patterns and consumer obligations.

**Pre-existing working-tree observation:** `color_spectrum.py` had an in-flight modification by another seam that added lightning/holy/shadow to `ELEMENT_COLOR_RANGES`. This caused one pre-existing test (`test_unknown_element_raises`) to fail against the working-tree state. NOT a regression from this dispatch — the test passes against git HEAD. Flagged in hive log for jack-ryan + gamora awareness.
