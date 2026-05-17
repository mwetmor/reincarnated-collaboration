# 2026-05-17 — rocket — Narrow-slice i-frame schema fields (per-substrate dodge tuning)

**Status:** QUEUED — auto-spawn after rocket's current dispatch (`rocket/v1.7-narrow-slice-engine-schema-fields-1`) ships. (Rocket is single-track; spawn when free.)
**Authority:** Gandalf L3 § 7 binding decision + § 5.1 narrow-slice scope ("Promote drax v0.26 cosmetic dodge to engine-coupled — i-frame wiring + cooldown shared state + remove damage during i-frames — drax + rocket joint, 2-3 days; rocket portion is the schema field").
**Type:** Pattern A (short task) — ~0.5-1 day.
**Predecessor:** `rocket/v1.7-narrow-slice-engine-schema-fields-1` (windup + indicator hex; just shipped).
**Seam:** generation + foundation (rocket; substrate identity loader extension).

---

## Why this matters

Drax's narrow-slice work needs to promote v0.26 cosmetic dodge → engine-coupled dodge with i-frames. Per gandalf briefing § 2.2 substrate-coupling table, dodge i-frame durations have substrate variation:

- Earth dodge: slightly shorter dash, more i-frames (positional-refusal = "I brace here and become briefly untouchable")
- Wind dodge: slightly longer dash, fewer i-frames (kinetic-rearrangement = "I am where you didn't expect, but only for a moment")
- Other 5 substrates: medium baseline i-frames

The numerical asymmetry is small but cosmologically-coherent. Drax can't apply substrate-coupled i-frame logic without the data; this dispatch adds the schema field.

---

## Required reading (in order)

1. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 2.2 (Substrate coupling for dodge); § 5.1 (this work in scope)
2. `canonical/story/substrate-identity-declarations-2026-05-17.md` — all 7 substrate declarations
3. `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` — your v1.7 work; now extending again
4. `reincarnated-engine/config/substrate_identities/*.yaml` — all 7 YAMLs in scope

---

## Scope

### Item 1 — Add `dodge_iframes_seconds` field per substrate

Add 1 new field to substrate identity declarations:

- **`dodge_iframes_seconds`** (float) — duration of damage-immunity window during dodge for this substrate's player

**Per-substrate defaults per gandalf briefing § 2.2 (asymmetric per substrate-coupling):**

| Substrate | dodge_iframes_seconds | Rationale |
|---|---|---|
| fire | 0.35 | baseline ignition (medium) |
| water | 0.35 | baseline suffusion (medium) |
| earth | 0.45 | positional refusal — bracing into invulnerability (longest) |
| wind | 0.25 | kinetic rearrangement — quick reposition; less linger (shortest) |
| lightning | 0.30 | resonance — fast arc-step |
| holy | 0.35 | baseline radiance (medium) |
| shadow | 0.40 | penumbra — concealment-tinged second-longest |

**Validation:**
- Add fail-loud rule (rule #13): `dodge_iframes_seconds` MUST be present + float in [0.0, 2.0] range

### Item 2 — Loader extension

- Extend `SubstrateIdentity` dataclass with the new field
- Update loader to populate from YAML
- Add fail-loud validation rule
- Update exports if needed

### Item 3 — Tests

- Unit tests for new field (presence per substrate; range; cosmological invariants — earth longest, wind shortest)
- Run full test suite

### Item 4 — MIGRATION.md

- Update `generation/MIGRATION.md` §v3.3 entry documenting:
  - Field addition + per-substrate defaults
  - Consumer obligation (drax narrow-slice engine-coupled dodge consumes this)
  - Cosmological rationale per gandalf § 2.2

---

## Out of scope (DO NOT)

- ❌ DO NOT implement dodge engine-coupling logic (that's drax narrow-slice)
- ❌ DO NOT add other schema fields beyond `dodge_iframes_seconds`
- ❌ DO NOT touch simulation, demo, loadout files
- ❌ DO NOT modify v1.7's `windup_duration_seconds` or `indicator_color_hex` values

---

## Acceptance criteria

- [ ] All 7 substrate YAMLs extended with `dodge_iframes_seconds` per table
- [ ] `SubstrateIdentity` dataclass extended; loader populates field
- [ ] Rule #13 validation added; rules #1-#12 continue passing
- [ ] Unit tests added (presence + range + cosmological invariants)
- [ ] Full test suite passes
- [ ] `generation/MIGRATION.md` §v3.3 entry authored
- [ ] Hive-log STATE entry
- [ ] Tag `rocket/v1.8-narrow-slice-iframe-schema-field-1`

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. **Also apply pull-rebase before engine-repo commits** if other agents are concurrently committing there (per gandalf 2026-05-17 OBSERVATION about cross-repo race conditions).

---

## Tag intent

`rocket/v1.8-narrow-slice-iframe-schema-field-1` — seam-prefixed.

---

*Queued 2026-05-17 by knight-rider. Spawn after rocket's v1.7 ships. Estimated 0.5-1 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Commit:** `f3b80ac` (reincarnated-engine)
**Tag:** `rocket/v1.8-narrow-slice-iframe-schema-field-1`

**Acceptance criteria — all satisfied:**
- [x] All 7 substrate YAMLs extended with `dodge_iframes_seconds` per gandalf briefing § 2.2 table
- [x] `SubstrateIdentity` dataclass extended; loader populates field from YAML root block
- [x] Rule #13 validation added (float in [0.0, 2.0]; fail-loud on missing/non-numeric/out-of-range); rules #1-#12 continue passing
- [x] Unit tests added: `TestDodgeIframesSeconds` (14 tests) — field presence, type, range, canonical values for all 7 substrates, cosmological invariants (earth longest, wind shortest, shadow second-longest, baselines equal)
- [x] Full test suite: 146 → 160 tests; 480-test foundation smoke clean (substrate identity + D2 coupling + ailment + role registries)
- [x] `generation/MIGRATION.md` §v3.3 entry authored with consumer obligations
- [x] Hive-log STATE entry (`phase-1-p1-log.md` PRE-SIGNAL + TAG + STATE + HANDOFF → drax)
- [x] Tag `rocket/v1.8-narrow-slice-iframe-schema-field-1` cut

**Per-substrate values landed:**

| Substrate | dodge_iframes_seconds |
|---|---|
| earth | 0.45 (longest) |
| shadow | 0.40 (second-longest) |
| fire | 0.35 (baseline) |
| water | 0.35 (baseline) |
| holy | 0.35 (baseline) |
| lightning | 0.30 |
| wind | 0.25 (shortest) |

**Consumer handoff → drax:** `SubstrateIdentity.dodge_iframes_seconds` is populated.
Access: `foundation.get_element(player_substrate_name).identity.dodge_iframes_seconds`.
Drives the i-frame (damage-immunity) window for engine-coupled dodge (Deliverable 28).
Coordinates with drax v0.31 dodge cooldown fix; i-frame field is independent of cooldown.

— rocket
