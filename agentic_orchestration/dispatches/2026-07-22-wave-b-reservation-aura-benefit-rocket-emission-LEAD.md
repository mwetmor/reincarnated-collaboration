# Dispatch — rocket — Wave-B Reservation/Aura BENEFIT round: emission LEAD

**Status:** PENDING
**Seam:** rocket (generation / config / emission)
**Conductor:** knight-rider (Wave-B Reservation/Aura build lane; run-state `agentic_orchestration/knight-rider/wave-b-reservation-aura-run-state.md`)
**Date authored:** 2026-07-22
**Pattern:** B (engine emission slice; dedicated session)
**Ruling that spawned this:** Matt ruled **R2 = (B) BENEFIT-BEARING** on 2026-07-22 + ratified a **FIVE-family** scope amendment. Input of record: `agentic_orchestration/gandalf/design-inputs/2026-07-22-aura-benefit-model-design-read.md` (gandalf SPEC-AUTHOR, DRIFT-CRITIC PASS). This carries the read's §3 emission spec + the SCOPE AMENDMENT (pulse-damage into v1). No open Matt-gates remain in the read — build to it.

---

## Position in the round
You are the **LEAD** again. The MVP round's S6 cert surfaced that the aura BENEFIT-side was unwired (only the reservation TAX was live). Matt ruled (B): wire it. You emit the ONE new field pair that sources a benefit magnitude; gamora's sim reads it into resolution. **Land + push your slice, then gamora starts (she reads engine HEAD after your push). Do NOT run in parallel with the gamora session on the same tree (Discipline #62).** You go first; you finish; you push; gamora follows.

## What this extends — READ FIRST (governance)
This EXTENDS your own MVP-round emission slice (`rocket/v2.13-wave-b-reservation-aura-emission-1`, module `generation/aura_geometry.py`, `AURA_GEOMETRY_KEYS` tuple, `aura_geometry` block on `PlayerClassV2.to_dict()` + `KitCandidate.to_character_dict()`). You add TWO sibling keys to the SAME block, same contract. **REMOTE TRUTH `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (`b850800`) stays untouched.** The MVP-round positional/ramp fields (`aura_radius_m`, `aura_reattune_ramp_s`) are inherited unchanged. FORBIDDEN fields (`aura_polarity`, `aura_target_cap`, `exclusive_aura_class`) stay absent (§15-R). This is purely additive (Disc #12).

## Required reading
1. `agentic_orchestration/gandalf/design-inputs/2026-07-22-aura-benefit-model-design-read.md` — **§3 (emission field spec — LEAN (a) scalar + discriminator), §2 (per-family scaffold bands), §1 (family set), and the bottom SCOPE AMENDMENT (pulse-damage into v1 = FIVE families).** Source of record.
2. Your own MVP-round dispatch + completion record: `dispatches/2026-07-22-wave-b-reservation-aura-rocket-emission-LEAD.md` — the `aura_geometry` module pattern you established.
3. `agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md` — §15-R (rulings), §6/§10-C1 (benefit = stat-mod on beneficiaries in radius).
4. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #8 (schema-validation-at-boundaries), #12 (semantic-shifting/additive), #40 (scaffold-declaration), #41 (no fantasy-archetype taxonomy — the enum names STAT AXES, not archetypes).
5. Read primitives from engine HEAD by symbol/grep, NOT stale line refs.

## Acceptance criteria (this dispatch)
1. **`aura_benefit_mod`** — new optional `float | None` field on the `aura_geometry` block. The benefit MAGNITUDE. `None` = inert (⇒ `full_benefit` stays 1.0 downstream ⇒ reservation-only aura = prior fork-A behavior byte-identical). Additive.
2. **`aura_benefit_kind`** — new optional `str | None` enum field on the `aura_geometry` block. Values ∈ **`{damage, defense, regen, speed, pulse_damage}`** (FIVE — pulse-damage amended in). Names the sink axis. Disc #41-clean: these are MECHANICAL stat axes (mirror the engine's `buff_damage/buff_defense/buff_dodge/buff_mana_regen` vocabulary + the pulse emission axis), NOT archetype/class labels. `None` = inert.
3. **Inert corner `None/None`** = byte-identical to your MVP-round emission (additive-identity theorem: absent benefit ⇒ prior behavior). A benefit-bearing kit sets BOTH fields (mod + kind); assert a validator error if exactly one is set (mod-without-kind or kind-without-mod is malformed — Disc #8).
4. **Band-guard (Disc #8 + #40, per read §2):** `_validate_aura_geometry` rejects `aura_benefit_mod` outside the per-KIND scaffold band. Because the band is kind-dependent, the validator reads `aura_benefit_kind` first to select the band. Scaffold bands (SCAFFOLD — gamora S6 cert finalizes; tag with Disc #40 scaffold-declaration, party=gamora, gate=S6 cert):
   | kind | band (scaffold) | mid |
   |---|---|---|
   | `damage` | [0.08, 0.20] | 0.14 |
   | `defense` | [0.08, 0.20] | 0.14 |
   | `regen` | [0.10, 0.30] | 0.20 |
   | `speed` | [0.05, 0.15] | 0.10 |
   | `pulse_damage` | [0.15, 0.35] | 0.25 |
5. **Enum-guard:** `_validate_aura_geometry` rejects any `aura_benefit_kind` outside the five-value set; the extra-key drift guard still raises on any injected key beyond `AURA_GEOMETRY_KEYS`.
6. **Forbidden fields still absent (Disc-check):** grep confirms NO `aura_polarity`, NO `aura_target_cap`, NO `exclusive_aura_class`, and NO fantasy-archetype enum (`aura_class ∈ {paladin,…}` is forbidden — `aura_benefit_kind` is the stat-axis enum, not that).
7. **Pulse cadence is NOT a kit field** (read amendment): `pulse_interval_s = 2.0` is an ENGINE constant on gamora's seam, NOT emitted here. Kits emit magnitude (`aura_benefit_mod`) only for `pulse_damage`; radius reuses the existing `aura_radius_m`. Do NOT mint a cadence field or a pulse-radius field.

## Discipline requirements
- **#1 math-before-code:** these are additive field declarations + a band-selector validator (no new fight arithmetic). A full math-note is N/A — but state the additive-identity claim explicitly in the MIGRATION entry (absent `aura_benefit_mod` ⇒ byte-identical prior behavior; `full_benefit` default 1.0 preserved).
- **#12 semantic-shifting:** frame both fields as ADDITIVE siblings on the existing `aura_geometry` block. Mirror the MVP-round additive-widen precedent.
- **#8 schema-validation-at-boundaries:** the mod-without-kind malformed check + kind-dependent band-guard + enum-guard all land at `_validate_aura_geometry`.
- **#40 scaffold-declaration:** the five bands ship with the SCAFFOLD tag (gamora S6 cert finalizes) so they are not silent hardcodes.
- **#41 no fantasy-archetype taxonomy:** the enum names stat axes only.
- **MIGRATION.md owed (ADR-004):** the two new fields cross the rocket→gamora seam (rocket emits, gamora consumes into resolution). Append a 1-line-class entry: two NEW OPTIONAL consumed fields, no removal, no retype, additive; gamora reader contract = `full_benefit ← aura_benefit_mod`, sink axis ← `aura_benefit_kind`.
- **#2 smoke-test:** round-trip smoke through the export boundary (`to_dict()` → JSON → read) asserting: both new fields serialize; `None/None` inert-corner defaults hold; all five enum values accepted; each band-guard rejects out-of-band per kind; mod-without-kind rejected; forbidden fields absent. Smoke, not full-regen. Re-run Wave-B + Wave-C regression.

## Out of scope (explicit)
- Any edit to `resource_economy.py` / `bc_target_composer` (REMOTE TRUTH).
- The gamora sink wiring — sourcing `full_benefit`, the four stat-mod paths, the pulse-damage AoE emission path, `pulse_interval_s`, AC-9a/b/c/d cert — ALL gamora's seam.
- `aura_polarity` / `aura_target_cap` / `exclusive_aura_class` (ruled out).
- The §7 capstone surface (Fork 4c) — DEFERRED behind MVP certs AND Q35.
- Off-hand `off_hand_contract.BannerContract.aura_radius_m` (a DIFFERENT serialized path — leave it; gamora consumes the economy `aura_geometry` block).

## Commit / push
Auto-commit in-scope work-products (CLAUDE.md team discipline). **PUSH authorized "as you go"** (Matt 2026-07-22 per-cycle push pattern). Tag `rocket/v<next>-wave-b-reservation-aura-benefit-emission-1` (increment from your last aura tag; check for series collisions with any Wave-D tags as before). Append a completion record: fields added, malformed-check + band-guard behavior, enum values, MIGRATION entry, smoke result, forbidden-field confirm, and the explicit go-token for gamora:
`BENEFIT-EMISSION-READY: aura_benefit_mod + aura_benefit_kind (5-value incl pulse_damage) emitted + pushed`

---

## Completion record

**Status:** DELIVERED — rocket, 2026-07-22.

**Fields added (2 sibling keys on the existing `aura_geometry` block, contract now 4 keys):**
- `aura_benefit_mod` (`float | None`) — the benefit MAGNITUDE sourced into gamora's `full_benefit` slot. `None` = inert (`full_benefit` stays 1.0).
- `aura_benefit_kind` (`str | None`) — stat-axis sink enum, FIVE values `{damage, defense, regen, speed, pulse_damage}` (pulse_damage per SCOPE AMENDMENT). Disc #41-clean (mechanical stat axes, not archetypes). `None` = inert.

**Inert corner:** `None/None` is byte-identical to the MVP-round emission (additive-identity, Disc #12) — `full_benefit` keeps its 1.0 default downstream ⇒ reservation-only aura = fork-A behavior. `None` (not 0.0) is the inert sentinel.

**Validator behavior (`_validate_aura_geometry`, Disc #8 schema-at-boundary):**
- **Enum-guard:** rejects any `aura_benefit_kind` outside the 5-value set (checked FIRST so band-selection reads a validated kind).
- **Malformed-pair check:** rejects exactly-one-set — mod-without-kind OR kind-without-mod — as malformed. Both must be set for a benefit-bearing aura.
- **Kind-dependent band-guard (Disc #8 + #40, SCAFFOLD — gamora S6 cert finalizes):** reads `aura_benefit_kind` to select the band, rejects `aura_benefit_mod` outside it. Bands: `damage` [0.08,0.20] · `defense` [0.08,0.20] · `regen` [0.10,0.30] · `speed` [0.05,0.15] · `pulse_damage` [0.15,0.35]. (`AURA_BENEFIT_BANDS` dict.)
- **Extra-key drift guard:** still raises on any injected key beyond `AURA_GEOMETRY_KEYS` (now 4).

**Forbidden fields confirmed absent:** `aura_polarity`, `aura_target_cap`, `exclusive_aura_class`, and no fantasy-archetype enum. Pulse cadence NOT minted — `pulse_interval_s` is an engine constant on gamora's seam (SCOPE AMENDMENT); kits emit magnitude only, radius reuses `aura_radius_m`. REMOTE-TRUTH `resource_economy.py` untouched.

**MIGRATION (ADR-004):** 1-line-class entry appended to `src/reincarnated/generation/MIGRATION.md` — two NEW OPTIONAL consumed fields, no removal/retype, additive; gamora reader contract = `full_benefit ← aura_benefit_mod`, sink axis ← `aura_benefit_kind`.

**Smoke (Disc #2):** `src/reincarnated/generation/notes/wave_b_reservation_aura_emit_smoke_2026_07_22.py` — **84/84 PASS** (extended with benefit enum-guard, malformed-pair, kind-dependent band-guards, pulse-cadence-not-a-field, benefit-bearing round-trip). Regression: Wave-B **65/65 PASS**, Wave-C **ALL PASS** — no regression.

**Tag / push:** `rocket/v2.14-wave-b-reservation-aura-benefit-emission-1` (v2.13 was the MVP round; no Wave-D collision). Pushed: `bcbe001..138999f` on `main` + tag. Tree is clean and non-broken (Disc #62) — gamora may run.

**GO-TOKEN for gamora:**
`BENEFIT-EMISSION-READY: aura_benefit_mod + aura_benefit_kind (5-value incl pulse_damage) emitted + pushed`

---

## Status pass — 2026-08-24 (rocket, dispatch-triage sweep)

**VERDICT: `ALREADY-LANDED`.** The `**Status:** PENDING` header at line 3 is **STALE** — never flipped after delivery. Nothing owed. The full chain (this dispatch → gamora benefit-sim → Gate-2) completed the same day it was authored.

**Evidence (all independently re-verified today):**
1. **Commit + tag on remote:** `138999ff… refs/tags/rocket/v2.14-wave-b-reservation-aura-benefit-emission-1`, commit `138999ff rocket(v2.14-…): aura BENEFIT field pair (R2=B, 5-family)`, and `git branch -r --contains 138999ff` → `origin/main`.
2. **Both fields in the frozen contract:** `src/reincarnated/generation/aura_geometry.py` `AURA_GEOMETRY_KEYS` (line 55) is now **4 keys** — `aura_radius_m`, `aura_reattune_ramp_s`, `aura_benefit_mod`, `aura_benefit_kind`. `AURA_BENEFIT_KINDS` (line 79) holds the FIVE stat axes; the per-kind `AURA_BENEFIT_BANDS` carry the Disc #40 SCAFFOLD tag.
3. **AC-6 forbidden-field check holds today:** grep for `aura_polarity` / `aura_target_cap` / `exclusive_aura_class` returns only doc-comments + the smoke's negative assertions. No fantasy-archetype enum exists; `aura_benefit_kind` remains stat-axis-only (Disc #41-clean).
4. **AC-7 holds:** no cadence field and no pulse-radius field was ever minted — `pulse_interval_s` stayed an engine constant on gamora's seam.
5. **MIGRATION.md entry present:** `src/reincarnated/generation/MIGRATION.md` § `[2026-07-22] WAVE-B RESERVATION/AURA BENEFIT round (R2=B)` (line 8 ff.), carrying the gamora reader contract `full_benefit ← aura_benefit_mod` and the per-kind band table.
6. **Downstream consumed + certified:** gamora `a0cb754d` / tag `gamora/v1.13-wave-b-reservation-aura-benefit-sim-1` (both on origin), S6 cert GREEN 8/8.
7. **Lane closed in tracker:** `canonical/current-to-end-state/current-to-end-state-engine.md:120` names this exact range — *"rocket `bcbe001..138999f` benefit-emission + gamora `138999f..d3a3e8d` benefit-sim; falsification dead (monotonic sweep); AC-9a–d pass; Gate-2 PASS."*

**§ 15-R supersession check — NEGATIVE.** No decisions-log entry after 2026-07-22 touches auras (post-07-22 set = 07-31 WR3-KITE-COMMIT, 07-31 WR3 W-2, 08-08 ×3 corpus/edition-pin). The R2=(B) BENEFIT-BEARING ruling and the FIVE-family scope amendment (pulse_damage in v1) both stand unamended; Forks 1b/2b/3a/6b/7a stand as built.

**Residual (NOT mine):** the Matt-authorized milestone tag `v<X.Y>-wave-b-reservation-aura` is still **unapplied** — `git tag -l "v*wave-b*"` is empty. KR action; it is the only unclosed item in this lane.
