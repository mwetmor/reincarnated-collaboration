# Dispatch — rocket — Wave-B Reservation/Aura MVP: emission LEAD

**Status:** PENDING
**Seam:** rocket (generation / config / emission)
**Conductor:** knight-rider (Wave-B Reservation/Aura build lane; run-state `agentic_orchestration/knight-rider/wave-b-reservation-aura-run-state.md`)
**Date authored:** 2026-07-22
**Pattern:** B (multi-slice engine work; dedicated session)
**Gates cleared:** gandalf DRIFT-CRITIC PASS-WITH-FLAGS · jack-ryan Gate-1 DESIGN-MODE PASS-WITH-AMENDMENTS (2026-07-22). This dispatch carries the ruled amendments — build to them.

---

## Position in the wave
You are the **LEAD**. You emit the new aura fields FIRST; gamora's sim consumers read them. Land + push your slice, then gamora starts (she reads engine HEAD after your push). **Do NOT run in parallel with the gamora session on the same tree** (Discipline #62 — the Wave-C two-agents-one-tree collision that orphaned a commit). You go first; you finish; you push; gamora follows.

## What this extends — READ FIRST (governance)
This is the **Reservation/Aura DESIGN + FIDELITY EXTENSION**, and it EXTENDS an already-BUILT spec. **`canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` is REMOTE TRUTH — Gate-2-passed 2026-07-16, pushed `b850800`. DO NOT re-open it.** You do NOT re-touch `bc_target_composer._ECON_BIN_COST_TYPE_MAP` (reservation entry) or the `resource_economy.py` reservation fields (`reservation_percent`/`reservation_flat`/`reservation_resource`). Those are inherited unchanged. This dispatch adds NEW emission fields on the aura carrier only — additive (Discipline #12).

## Required reading
1. `agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md` — §6 (radius model, ruled 2b), §8 (swap-tax, ruled 6b + 7a), §14 (rocket routing bullet), §15-R (Matt's rulings). **Source of record.**
2. `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` — the REMOTE-TRUTH boundary (do not reopen). Note ERRATA 12/13/14.
3. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code), #2 (smoke-test), #12 (semantic-shifting / additive), #40 (scaffold-declaration).
4. Your `generation/MIGRATION.md` recent entries (Wave-A A3 additive-widen precedent) + the Wave-A completion records in `dispatches/2026-07-13-rocket-wave-a-summon-economy-config.md`.

## Ruled fork set (Matt 2026-07-21, §15-R — BINDING, do not re-litigate)
Fork 1 = **(1b) stackable-reserved** (bound by built Σ<0.90; **NO new exclusivity tag** — `exclusive_aura_class` does NOT ship) · Fork 2 = **(2b) radius-gated hard-edge** (`aura_radius_m` ships) · Fork 3 = **(3a) no-cap** (**NO `aura_polarity`, NO `aura_target_cap`**) · Fork 6 = **(6b) re-attunement ramp** (`aura_reattune_ramp_s` ships) · Fork 7 = **(7a) instant refund** at carrier-END.

## Acceptance criteria (this dispatch)
1. **`aura_radius_m`** — new optional float field on the aura carrier (meters). Band `[2.0, 12.0]` LOCKED-scaffold (gamora tunes at S6; D2 aura radii ~2.6–8yd, PoE ~2.2m base). Absent ⇒ prior behavior (no radius gate). Additive (Disc #12).
2. **`aura_reattune_ramp_s`** — new optional float field on the aura carrier (seconds). **Ship a scaffold default `1.0`, band `[0.5, 1.5]`, tagged with a Discipline #40 scaffold-declaration** (`SCAFFOLD — gamora S6 cert finalizes band`) so it is not a silent hardcode. Absent ⇒ no ramp. Additive.
3. **Forbidden fields absent (Disc-check):** grep the emission surface confirms NO `aura_polarity`, NO `aura_target_cap`, NO `exclusive_aura_class` — the §15-R rulings (3a no-cap, 1b needs no tag) mean these must NOT be emitted.
4. **C3 carrier-set widening is descriptive-only on your seam** — carriers A (radius aura) / B (self-buff) feed the SAME built `reservation_percent`/`reservation_flat` fields; you emit no new reservation-arithmetic type. Confirm the aura carrier's reservation rides the existing built fields.
5. **Banner reservation (prep for gamora Slice 2, Fork-8=8a):** confirm banners (carrier D) reuse the EXISTING `reservation_flat`/`reservation_percent` fields (§9 — "banners reserve the same regen-cap tax as other carriers"). Expected: **no new field, no MIGRATION for banner reservation.** If your read finds a banner-specific reservation field is genuinely required, **STOP and escalate to KR** (do not mint a new reservation field unilaterally — it touches the REMOTE-TRUTH surface's neighborhood).

## Discipline requirements
- **#1 math-before-code:** a short note is owed only if any field introduces non-trivial arithmetic. These are additive field declarations (no new arithmetic), so a full math-note is likely N/A — but state the additive-identity claim (absent field ⇒ byte-identical prior behavior) explicitly in the MIGRATION entry.
- **#12 semantic-shifting:** frame both new fields + the C3 carrier-set widening as ADDITIVE. Mirror the Wave-A `PROXY_TYPE_TARGETING → PROXY_TYPE_BEHAVIOR` additive-widen precedent.
- **MIGRATION.md owed (ADR-004):** the new fields `aura_radius_m` + `aura_reattune_ramp_s` cross the rocket→gamora seam (rocket emits, gamora consumes). Author a 1-line-class MIGRATION entry: new OPTIONAL consumed fields, no removal, no retype, additive. This is the cross-seam contract gamora reads.
- **#2 smoke-test:** a round-trip smoke through the export boundary (`to_dict()` → JSON → read) asserting the two new fields serialize + absent-field defaults hold + forbidden fields absent. Smoke, not full-regen.
- **#62 parallel-tree hygiene:** you own the tree alone for this slice. Read primitives by symbol/grep at HEAD `8d8bd26`, NOT by draft §16 stale line refs.

## Out of scope (explicit)
- Any edit to `resource_economy.py` reservation fields or `bc_target_composer._ECON_BIN_COST_TYPE_MAP` (REMOTE TRUTH).
- `aura_polarity` / `aura_target_cap` / `exclusive_aura_class` (ruled out by 3a / 1b).
- The §7 capstone surface (Fork 4c) — DEFERRED behind MVP certs AND Q35 (Fork-5 vehicle parked). Do NOT emit `aura_transform_id` or capstone 6-set/T4 entries now.
- The sim consumers (C1 radius gate, C4 ramp state, AC-7-SIM guard) — all gamora's seam.

## Commit / push
Auto-commit in-scope work-products (CLAUDE.md team discipline — do not re-ask per-commit). **PUSH authorized "as you go"** (Matt 2026-07-22 — per-cycle push pattern established for this wave). Tag `rocket/v<next>-wave-b-reservation-aura-emission-1`. Append a completion record to this file (fields added, MIGRATION entry, smoke result, tag, banner-reservation confirm outcome, and the explicit go-token for gamora: `EMISSION-READY: aura_radius_m + aura_reattune_ramp_s emitted + pushed`).

---

## Completion record

**Status:** COMPLETE — SHIPPED + PUSHED. rocket, 2026-07-22.
**Tag:** `rocket/v2.13-wave-b-reservation-aura-emission-1` (v2.12 series was consumed by the prior Wave-D slice-0 `rocket/v2.12-waved-1`; incremented to v2.13 to avoid collision).

### Fields added (both generation paths — parity)
- **`aura_radius_m`** — `float | None` (meters). INERT default `None` (no radius gate ⇒ prior behavior). Band `[2.0, 12.0]` LOCKED-scaffold (gamora S6 cert finalizes). Fork-2b radius-gated hard-edge. Additive (Disc #12).
- **`aura_reattune_ramp_s`** — `float | None` (seconds). INERT corner default `None` (no ramp); builder-default `1.0` (`AURA_REATTUNE_RAMP_S_DEFAULT`). Band `[0.5, 1.5]`, tagged Discipline #40 scaffold-declaration (`SCAFFOLD — gamora S6 cert finalizes band`; party=gamora; gate=S6 cert). Fork-6b re-attunement ramp (Fork-7a instant refund). Additive.
- Home: NEW sibling config module `src/reincarnated/generation/aura_geometry.py` (parallel to `summon_economy.py`/`resource_economy.py`). NOT in `resource_economy.py` (REMOTE TRUTH — untouched). Emitted as always-present `aura_geometry` block on `PlayerClassV2.to_dict()` + `KitCandidate.to_character_dict()`.

### Forbidden fields (§15-R) — confirmed ABSENT
`aura_polarity` (Fork-3b), `aura_target_cap` (Fork-3a no-cap), `exclusive_aura_class` (Fork-1b no tag) — absent from `AURA_GEOMETRY_KEYS` + emitted block; smoke Disc-checks their absence; extra-key guard raises on injection.

### MIGRATION entry
`src/reincarnated/generation/MIGRATION.md` [2026-07-22] — 1-line-class cross-seam contract: two NEW OPTIONAL consumed fields (rocket emits → gamora consumes), no removal, no retype, additive-only. Additive-identity theorem stated (absent fields ⇒ byte-identical HEAD `8d8bd26`). Includes gamora reader contract (C1 radius gate + C4 ramp) + banner-reservation confirm + forbidden-field ruling.

### Smoke result (Disc #2, round-trip through export boundary)
`notes/wave_b_reservation_aura_emit_smoke_2026_07_22.py` — **35/35 PASS** (inert corner, forbidden-field Disc-check, active kit, band guards, JSON export round-trip, PlayerClassV2 field presence). Regression: Wave-B **65/65 PASS**, Wave-C **ALL PASS**. All touched files `py_compile` clean.

### Banner-reservation confirm (AC-5) — outcome
NO new field, NO MIGRATION for banner reservation, NO escalation. Carrier D (banner) reserves via the EXISTING built `resource_economy.reservation_flat`/`reservation_percent` (spec §9); plant-point radius reuses `aura_radius_m` (center-choice is gamora's sim consumer, not a new emission field). C3 carrier-set widening (carriers A/B/D → same built reservation fields) confirmed descriptive-only on the rocket seam (AC-4).

### Surprises / flags
- **Naming-collision noted (not a problem):** `off_hand_contract.BannerContract.aura_radius_m` (default 8.0) already exists — but that is the OFF-HAND ITEM cosmetic contract blob (`off_hand_item` serialized surface), a DIFFERENT dict path from the economy `aura_geometry` block. No runtime collision. Off-hand banner contract untouched.
- **Tag series bump v2.12 → v2.13** to avoid collision with the prior Wave-D slice-0 tag.

### go-token (gamora waits on this)
`EMISSION-READY: aura_radius_m + aura_reattune_ramp_s emitted + pushed`
