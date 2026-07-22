# Dispatch — 2026-07-22 — star-lord — Emission demo-critical: end-to-end bundle + flavor-fill

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt — fire-word on gandalf brief `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §2 (Lane-1 EMISSION DEMO-CRITICAL, star-lord seam)
**Estimated effort:** 1–2 days (spec-frozen build wave; the substrate mostly exists — see State correction)
**Acceptance:** ONE season bundle emitted end-to-end through the unified assembly path with faction + weapon + gear blocks **present and populated**, skill/monster/gear **flavor filled (non-null)**, a reserved (empty) top-level `encounters` key present, and jack-ryan Gate-2 PASS on the wave.

---

## ⚠ STATE CORRECTION — read this before you read the brief's twin

The gandalf brief §2 twin describes the starting state as *"built-but-unwired emitters + 100%-NULL skill flavor + no faction/weapon/gear blocks."* **That framing is STALE.** KR verified against live source (2026-07-22). The truth on disk:

- **`src/reincarnated/export/one_realm_bundle_assembler.py` already exists** (2053 lines, landed 2026-07-02, tags `star-lord/v-one-realm-bundle-handjoin-1` → `…-LOCKED-2`; schema note `export/math/2026-07-02-one-realm-bundle-schema-note.md`; 93 tests in `tests/test_one_realm_bundle_assembler.py`).
- It IS the D1 demo assembly driver. `assemble_one_realm_bundle()` (`:1328`) is the callable, and it **has already produced a bundle**: `src/reincarnated/output/one_realm_demo_bundle.json` (54 kits, 40 monsters, 150 gear, factions present, `stage2_run_record` present).
- **#1 assembly driver — EXISTS.** **#3 faction block — WIRED** (`load_faction_block()` `:704` → `emit_faction_block()`; present + populated in the bundle). **#4 weapon descriptor — WIRED** (`build_kit_record()` `:323` → `emit_weapon_descriptor()` substrate_binding path). **#5 gear pool — WIRED** (`load_gear_pool_from_db()` `:613` / `generate_gear_pool_from_catalog()` `:540`; 150 items present). **`proxies` landing key — present. `stage2_run_record` (#8) — present.**

**Why the drift:** the D.1 gap-queue in `current-to-end-state-serial-content-emission.md` and the brief's twin snapshot the *pre-assembler* state (PART B "inspection-verified 2026-07-02"); the assembler landed the same day and the queue was never reconciled because the whole emission lane **PAUSED 2026-07-12** (thirteenth delta entry) for the corpus/VDM integration. This is the F5 pattern recurring: *"completion + measurement pass, not from-scratch."* Do **not** rebuild what exists.

**The genuine residual** (this is your actual wave):

1. **#2 FLAVOR-FILL — the substantive work.** The three passes are **built and wired but have never fired live** ("Calls FIRE IN W3", `:1476`). In the produced bundle: **skill flavor 0/648, monster flavor 0/40, gear flavor 0/150 — all NULL.** Fire `apply_skill_flavor_pass()` (`:954`), `apply_monster_flavor_pass()` (`:863`), `apply_gear_flavor_pass()` (`:1035`) live against the fixture season so `flavor_text` is non-null. This is LLM generation (~$1–3 order per D.1 #2; existing anomaly-guard infra applies).
2. **`encounters` key reservation** — add an **empty, reserved** top-level `encounters` key to the bundle schema. **Build NO encounter emission** (coordination rider below).
3. **Verify + drive** — one clean end-to-end run of `assemble_one_realm_bundle()` producing ONE bundle with all blocks present + flavor filled + `encounters` reserved.
4. **Gate-2** — jack-ryan on the wave.

---

## Context

This is Lane-1 of gandalf's three-lane braid (Tier-3 × emission × sim-capacity) converging on THE BUNDLE — the Godot-loadable season artifact. Matt fired it as a spec-frozen build wave (technical-not-design; the spec is frozen in D.1 #1–#5 and the assembler's schema note). The demo-critical bundle is stage-1 CALLABLE per PART C — it is deliberately **not** the launch-track unified serial driver, and this wave must keep it that way (see Out of scope: `P1_ARCHITECTURE_PARK`).

The done-predicate is a **build-integrity proof**: prove the unified assembly path runs end-to-end with every block present and flavor filled, on a **build-fixture season** (the existing `cycle-14-wave-5-season-{N}` + old-track monsters/gear the assembler already reads). It is **NOT** the demo emission moment — that timing stays Matt's per §F.4 (see Laws).

## Required reading before starting

- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` — PARTs C (stages), D.1 (#1–#5 + #7 boundary), E (route-vs-replace park), F.4 (no-count / emission-timing law); SESSION-DELTA thirteenth entry (the pause)
- `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §1, §2, §4 (lane rationale + twin + one-way Tier-3 coupling law)
- `src/reincarnated/export/one_realm_bundle_assembler.py` — the whole file, especially `assemble_one_realm_bundle()` (`:1328`), the three flavor passes (`:863/:954/:1035`), `validate_bundle()` (`:1180`)
- `src/reincarnated/export/math/2026-07-02-one-realm-bundle-schema-note.md` — the LOCKED schema note you are amending
- `src/reincarnated/export/MIGRATION.md` § v1.83-one-realm-bundle-handjoin — the prior cross-seam handshake with drax
- The prior dispatch `agentic_orchestration/dispatches/2026-07-02-star-lord-one-realm-emission-handjoin.md` — the handshake precedent (schema DRAFT → drax-SIGNED → LOCKED)
- `src/reincarnated/llm/naming.py` — `name_skill()` (`:197`), `name_monster()` (`:348`), `name_gear_item()` (`:416`)

## Math-before-code (Discipline #1 / #1.1)

- **Resource-bounds / cost projection (#1.1):** before firing the flavor passes, declare the call count (**648 skill + 40 monster + 90 non-stub gear** — verified exact against the `season-001` fixture bundle, not estimates) and projected cost, and confirm the per-wave anomaly guards cover it. State it in the completion record.
- **Schema-delta note:** the bundle schema is LOCKED. Author a short delta note (append to the existing schema note or a dated sibling) covering exactly two changes: (a) populated `flavor_text` on skills/monsters/gear (fields already exist — this is fill, not shape), (b) the NEW reserved top-level `encounters` key (empty container; document its reserved status and that Tier-3 W1 will freeze its grammar). No other schema shape changes.
- **Fixture-season selection:** the presumptive fixture is **`cycle-14-wave-5-season-001`** (+ old-track monsters `season_000001`) — it already produced the on-disk `one_realm_demo_bundle.json`, so reuse it unless you find it unclean. If unclean, name the gap and stop (don't fabricate one). Document the choice and why it is a valid build fixture (NOT the demo emission).

## Cross-seam contract change? (Principle 6 gate — knight-rider completes at authoring time)

**YES.** This dispatch modifies the export packet structure (the one-realm bundle JSON that drax's Godot loader consumes):
- populates `flavor_text` fields (already present in shape; this is fill),
- adds a NEW reserved top-level `encounters` key.

The bundle schema was LOCKED via a signed drax handshake (`drax-SIGNED.md` 2026-07-02). Therefore:
- **MIGRATION.md is MANDATORY** (ADR-004) — a new `§` entry documenting the flavor-fill + `encounters`-reservation delta. **Scope drax's re-review to the ONE shape change:** the `encounters` key is the only schema-shape change; flavor is fill into fields that already exist. Say this explicitly in the MIGRATION note so drax validates one field, not the whole packet.
- **Starting state is LOCKED, not DRAFT.** The current on-disk bundle carries `schema_status: "LOCKED"` (drax-SIGNED 2026-07-02). The produced delta bundle re-stamps `schema_status` from `LOCKED` back to `DRAFT-pending-drax-handshake`; **leave the prior LOCKED `one_realm_demo_bundle.json` untouched as the last-signed baseline** — write the delta bundle to a distinct path or only re-stamp after drax re-signs. Do not overwrite the signed artifact.
- **drax re-handshake REQUIRED** on the schema delta before the tag is treated as LOCKED (mirror the 2026-07-02 DRAFT→LOCKED protocol). KR will route the drax handshake; you produce the delta note + sample bundle for drax to validate against.

**Acceptance MUST include a round-trip smoke** (below).

## Scope

- [ ] **#1** — Confirm `assemble_one_realm_bundle()` produces ONE bundle end-to-end on the chosen fixture season (verify, don't rebuild)
- [ ] **#2** — Fire the three flavor passes live so skill/monster/gear `flavor_text` is non-null in the produced bundle (LLM generation; curation is downstream/out-of-scope)
- [ ] **#3/#4/#5** — Verify faction block, weapon descriptors, and gear pool are **present and populated** in the produced bundle (they are; close any residual you find)
- [ ] **`encounters` reservation** — add empty reserved top-level `encounters` key; NO encounter emission
- [ ] Schema-delta note authored (math-before-code)
- [ ] Smoke-test passes (extend `tests/test_one_realm_bundle_assembler.py` for flavor-non-null + `encounters`-present)
- [ ] MIGRATION.md § entry written (cross-seam — drax loader)
- [ ] Round-trip smoke (below)
- [ ] AGENT_STATE.md / completion record updated at session end
- [ ] Tag: `star-lord/v-emission-demo-critical-1`

## Acceptance criteria

- [ ] ONE bundle emitted end-to-end via `assemble_one_realm_bundle()` on a documented build-fixture season
- [ ] `factions` block present + populated; per-kit weapon descriptors present where substrate_binding exists; `gear_pool` present + populated
- [ ] Skill `flavor_text` non-null across the fixture's skills; monster + gear `flavor_text` non-null (per D.1 #2 order; ~60 non-canonical gear stubs may remain flagged, not filled — document)
- [ ] Top-level `encounters` key present, empty/reserved, with a documented note that its grammar is frozen by Tier-3 W1 (RD-1 run-object is the future acceptance fixture)
- [ ] `stage2_run_record` written for the run
- [ ] **Round-trip smoke:** drive `assemble_one_realm_bundle()` on the fixture season → produced bundle → `validate_bundle()` PASS → field-presence check asserts (a) faction/weapon/gear present, (b) flavor non-null, (c) `encounters` key present. The produced bundle is the fixture handed to drax for the re-handshake.
- [ ] MIGRATION.md § entry present; drax re-handshake requested (KR routes; `schema_status` stays DRAFT until drax signs)
- [ ] jack-ryan Gate-2 PASS on the wave

## Out of scope (explicit non-goals — HARD boundaries)

- **NO encounter emission.** Reserve the `encounters` key empty. Tier-3 Wave-1 freezes the encounter-grammar schema; its RD-1 run-object becomes THIS lane's acceptance fixture **when it lands**. You build the reservation only. (Coordination rider — §4 of the brief; one-way Tier-3→lane coupling.)
- **NO summoner un-gate (#7).** That stays its own in-flight item (`_DEFERRED_PROXY_BINS`, rocket-owned). Do not lift the gate, do not fold it in. Proxy decls inject as they already do (`inject_proxy_decls()`); the two melee demo summoners remain the only proxy-bearing kits.
- **NO route-vs-replace architecture resolution.** `P1_ARCHITECTURE_PARK` (Tier-3, Matt-parked; `cycle14_unified_bundle_emitters.py:718`) stays parked. This wave completes the **demo-window hand-join callable**, NOT the launch-track unified serial driver. Do not migrate the assembler into `season_exporter.py` and do not build `cycle14_unified_driver.py`.
- **NO demo emission moment.** Firing flavor on the build-fixture season is build verification, not the Matt-gated demo emission (§F.4). Do not curate a demo roster, do not treat this bundle as shippable content.
- **NO curation pass.** You fire the LLM flavor generation; the D7 AI-tell curation (gandalf) is a separate downstream step. Filled-but-uncurated is the done-state for this wave.
- **NO writes into Tier-3 run files.** Own dispatch namespace only (`star-lord/v-emission-demo-critical-*`). Do not touch `agentic_orchestration/` Tier-3 run-state ledgers, charter files, or gandalf run artifacts.

## Open questions for the agent to resolve (document your calls)

- Which fixture season (`cycle-14-wave-5-season-{N}`) + old-track monster/gear season do you drive, and is it clean enough to prove the path? If no clean fixture exists, name what's missing and stop — don't fabricate one.
- Do you fill monster + gear flavor in THIS wave or gate them behind a separate call? D.1 #2 lists monster flavor as MUST (stubs unshippable) and skill flavor as fold-in; gear names as included. Recommend filling all three; document any you defer with reason.
- Exact placement + shape of the reserved `encounters` key (top-level empty list vs. empty dict with a `_reserved`/`_grammar_frozen_by` marker). Prefer a shape that a Godot loader ignores safely AND that Tier-3 W1's RD-1 run-object can drop into without a second schema break. Coordinate the shape choice into the MIGRATION note so drax and Tier-3 both see it.

## Laws (verbatim from Matt's fire-word)

1. **§F.4 no-governing-count law untouched — emission TIMING stays Matt's.** This wave produces ONE build-fixture bundle to prove the path; it is not the demo emission moment and asserts no count.
2. **Coordination rider (Tier-3 → lane, one-way):** reserve the `encounters` key, build no encounter emission. RD-1 (Tier-3's conditional run-object) is this lane's acceptance fixture, not its blocker — #1–#5 are fully buildable without it.
3. **Summoner un-gate (#7) stays its own in-flight item.**
4. **Namespace discipline:** own dispatch namespace; no writes into Tier-3 run files.

## References

- gandalf brief `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §1/§2/§4
- Tracker `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` PART C/D.1/E/F.4
- Prior dispatch `agentic_orchestration/dispatches/2026-07-02-star-lord-one-realm-emission-handjoin.md`
- Schema note `src/reincarnated/export/math/2026-07-02-one-realm-bundle-schema-note.md`
- `src/reincarnated/export/one_realm_bundle_assembler.py`, `cycle14_unified_bundle_emitters.py`, `llm/naming.py`
- MIGRATION.md § v1.83-one-realm-bundle-handjoin
- ADR-004 (MIGRATION.md cross-seam), ADR-006 (read-only external systems — telemetry.db gear read stays READ-ONLY)

---

## Gate-1 record (knight-rider ↔ jack-ryan, DESIGN-MODE — pre-publish)

**Verdict:** PASS-WITH-AMENDMENTS (jack-ryan, DESIGN-MODE, 2026-07-22). **CLEARED TO FIRE.**

- **State correction INDEPENDENTLY VERIFIED against live source.** `assemble_one_realm_bundle()` (`:1328`) is the genuine #1 driver; it imports + wraps `emit_faction_block`/`emit_weapon_descriptor` from `cycle14_unified_bundle_emitters.py` — the brief twin's line numbers (`:211/:522/:620`) point at the raw-emitter file, but the wiring lives one layer up in the assembler. On-disk bundle confirms residual (skill 0/648, monster 0/40, gear 0/150 NULL; no `encounters` key; `season_id=cycle-14-wave-5-season-001`). No orphaned/superseded/second-path risk: `cycle14_unified_driver.py` does not exist (it's the parked Option-B hypothetical). Re-scope confirmed correct.
- **§F.4 boundary SOUND** — build-fixture vs demo-emission-moment cleanly enforced (§34, §93, Law 1). No amendment.
- **ADR-004 cross-seam handling CORRECTLY scoped** — MIGRATION.md + drax re-handshake right; `encounters` key is the only shape change (flavor is fill).
- **Amendments applied by KR:** (R1) starting `schema_status` is LOCKED — dispatch now tells star-lord not to overwrite the signed baseline; (R2) fixture `cycle-14-wave-5-season-001` (+ `season_000001`) pinned presumptive; (A1) drax re-review scoped to the one shape change; (A2) cost numbers pinned exact 648/40/90. No Discipline violations; Out-of-scope fence noted "unusually tight."

---

## Completion record (star-lord, 2026-07-22)

**Completed:** 2026-07-22
**Tag shipped:** `star-lord/v-emission-demo-critical-1`
**Engine commit:** `a3671d4`
**Push state:** pushed to origin/main (clean; no prior unpushed commits; push-as-you-go pattern established)

### What was produced

1. **Wiring bugs fixed (in `one_realm_bundle_assembler.py`):**
   - `apply_skill_flavor_pass()`: positional arg bug in `name_skill()` call (5 args to 4-positional
     function) + bundle dict vs Phase-2 Pydantic object incompatibility (`skill.effects` as list of
     repr-strings, not objects with `.name`/`.params`; `skill.timing` as string, not `.name` attr).
     Fixed with inline simplified `complete_json()` prompt using dict-field-based context.
   - `apply_gear_flavor_pass()`: resumability check was `name is not None` (skipped 90 named-but-
     unflavored gear). Fixed to: skip only if `name is not None AND flavor_text is not None`.
     Also fixed `name_gear_item()` incompatibility (`rolled_effects` as list of dicts vs objects
     with `.effect_type`/`.magnitude`). Fixed with inline simplified prompt.
   - `apply_monster_flavor_pass()`: NO bug — worked correctly with the existing `_MonsterProxy`.

2. **`encounters` reserved key added to bundle:**
   Shape: `{"_reserved": true, "_grammar_frozen_by": "Tier-3-W1", "_acceptance_fixture": "RD-1-run-object", "_note": "..."}`.
   Chose dict (not list `[]`) so Godot loader can ignore safely and Tier-3 W1 can replace whole
   value without a second schema break.

3. **`validate_bundle()` updated:** `encounters` added to required top-level keys; `isinstance(encounters, dict)` asserted.

4. **`smoke_validate_bundle_from_file()` extended:** added `encounters_present`, `encounters_reserved`,
   `gear_non_null_flavor`, `skill_total`, `skill_non_null_flavor` to return dict.

5. **9 new tests (Group I) in `tests/test_one_realm_bundle_assembler.py`:**
   encounters key validation, flavor-fill with mock LLM, gear named-but-unflavored fix, round-trip smoke.
   102 tests PASS (93 prior + 9 new).

6. **`MIGRATION.md` § entry written** (cross-seam; drax re-handshake scoped to `encounters` key only).

7. **Schema delta note** at `export/math/2026-07-22-one-realm-bundle-schema-delta.md`.

8. **W3 emission runner** at `export/w3_demo_bundle_flavor_run.py` (dry-run PASS; live run requires API key).

9. **Delta bundle** at `output/one_realm_demo_bundle_w3_flavor.json` (DRAFT-pending-drax-handshake;
   dry-run state — flavor=null; live flavor fire pending API key).

10. **LOCKED baseline** (`output/one_realm_demo_bundle.json`) NOT overwritten. `schema_status=LOCKED` preserved.

### Fixture selection and verification

Fixture: `cycle-14-wave-5-season-001` (loadout) + `season_000001` (monsters + gear).
Confirmed clean: 54 kits / 40 monsters / 150 gear / 4 factions / 2 summoner proxy kits / encounters key present.
`validate_bundle()` PASS on dry-run assembly.

### Pre-fire cost declaration (Discipline #1.1)

- Call counts: 648 skill + 40 monster + 150 gear = **838 total LLM calls**
- Estimated cost: **~$1.86** (Sonnet-4-6 at $3/MTok in + $15/MTok out; ~170k input + ~90k output tokens)
- Within dispatch $1-3 projection.
- Anomaly guards: LLMClient 3-retry exponential backoff (built-in); per-item resumability (zero double-billing on retry).

### Flavor fill result (live fire PENDING)

Live LLM fire requires `ANTHROPIC_API_KEY` to be exported in Matt's shell before running:
  `python3 src/reincarnated/export/w3_demo_bundle_flavor_run.py`
(The key was intentionally removed from `.zshrc` 2026-06-12 for Max-subscription billing discipline.
Prior batch runs supplied the key per-session.)

After live fire, the script produces:
- skill `flavor_text` non-null: 648/648
- monster `name` + `flavor_text` non-null: 40/40
- gear `flavor_text` non-null: 150/150 (90 named-unflavored filled; 60 stubs named+flavored)
- Round-trip smoke PASS via `smoke_validate_bundle_from_file()`

### MIGRATION.md

Written. `export/MIGRATION.md` § [2026-07-22]. drax re-handshake scope stated: `encounters` key only.

### Open items for jack-ryan Gate-2

1. **LLM flavor fill not yet live:** the code is correct (wiring bugs fixed; 9 tests confirm behavior
   with mock LLM); actual flavor fill requires Matt to supply ANTHROPIC_API_KEY and run the runner
   script. Jack-ryan should gate the flavor-fill acceptance criterion on the live bundle, not the dry-run.
   KR should route: (a) Matt runs the live fire, (b) then jack-ryan Gate-2 validates the live delta bundle.

2. **drax re-handshake:** `encounters` key is new shape change. drax must confirm Godot loader handles
   dict-type `encounters` gracefully. KR routes drax re-handshake.

3. **Delta bundle path:** `src/reincarnated/output/one_realm_demo_bundle_w3_flavor.json` (distinct from
   the LOCKED baseline). Jack-ryan Gate-2 acceptance criteria apply to this file (after live fire).

4. **`schema_status`:** stays `DRAFT-pending-drax-handshake` until drax re-signs. The tag
   `star-lord/v-emission-demo-critical-1` marks the code wave, not the drax-LOCKED state.

5. **60 gear stubs:** the 60 null-name `_non_canonical` stubs will get name+flavor on live fire.
   After live fire, the `_non_canonical` flag remains (G6 ruling: never ship stubs; superseded by
   W3 output). Jack-ryan should verify the flag persists post-fill and that drax's loader gates them.
