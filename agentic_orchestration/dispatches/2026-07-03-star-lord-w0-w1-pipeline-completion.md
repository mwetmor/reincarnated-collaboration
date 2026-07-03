# Dispatch — 2026-07-03 — star-lord — W0 export widen + W1 pipeline completion (DEMO-READINESS UNATTENDED RUN)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-07-03 (run fire authorized; spec §1-C emission-exercise authorization — the export/MIGRATION v1.81-1.82 hold's first Matt-authorized exercise)
**Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** — §1 A/B/F, §2 G3/G6/G9, §3 W0+W1, §7. Cite it; do not re-derive.
**Estimated effort:** one long session
**gates-on:** — *(W1 fires parallel with W0 — EXCEPT the #8 registry writer, which gates on schema ratification: see sequencing below)*
**Failure policy:** §7 — wiring failure: one retry → halt the wave loud + park. A NULL-riddled bundle is NOT readiness.

## Context

W1 completes the pipeline so W3 (THE emission run) has one callable driver emitting all six content types into a single Godot-consumable bundle with zero hollow spots (criteria A + B). Your W0 item (export DDA-lock widen) is the KR scope-pin from the spec's "B4 prereq re-scope" row — the other half (F-f consumer) is pinned to rocket. **Necro-energy = RESOLVED no-op (G4: mana, caster-subset) — do not build anything for it.**

## Required reading before starting

- Spec v1.1 (whole; your seam owns most of it)
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` — PART B (your own inspection substrate) + D.1 rows #1/#2/#3/#4/#5/#8 (verbatim scope)
- Your B2 completion record (`a916632`) + export `MIGRATION.md` v1.84
- Engine decisions-log `a10a695` (G-rulings registration)

## Math-before-code

Not applicable — wiring + schema work. Disc #8 (schema validation at boundaries) governs instead.

## Cross-seam contract change? (Principle 6 gate)

**YES — heavily.** The bundle gains `proxies` landing key, faction block, weapon descriptors, gear pool, stage-2 run record, `proxy_scaling` contract flag (spec §6). Consumers: drax (Godot bundle loader), gamora (W4 tagging reads composition).
**Round-trip smoke REQUIRED:** production-path fixture bundle → assert key-present + non-NULL count per content type (the criterion-B checklist, inverted from PART B's hollow-spot list) at the consumer boundary. MIGRATION.md before tags (ADR-004).

## Scope — W0 item (fires first, unblocks nothing downstream of you but hard-gates W3)

- [ ] **Export DDA-lock widen** (KR scope-pin; MASTER B1 closeout provenance): `cycle14_wave5_emitter.py` hard-locks `primary_t4` to DDA (`_PRIMARY_T4_REQUIRED` :698; `PRIMARY_T4` :388) — a proxy-family `primary_t4` raises ValueError. Widen validator + emit shape so proxy-family primaries emit. `gates-on: —`

## Scope — W1 (serial D.1 rows, verbatim)

- [ ] **#1 Assembly driver**: cycle-14 kits + old-track monsters + `_load_gear_pool()` + proxy decls → ONE bundle; adds the missing **`proxies` landing key**; writes a **stage-2 run record**; carries the **`proxy_scaling` flag** (spec §6 emission contract). Supersedes the one-realm §5.1 hand-join (dead — do not execute the stale ask). `gates-on: —`
- [ ] **#3 Faction block wiring** — `emit_faction_block()` (built + validated) into the bundle. `gates-on: —`
- [ ] **#4 Weapon descriptor wiring** — `emit_weapon_descriptor()` into the bundle (substrate_binding path). `gates-on: —`
- [ ] **#5 Gear-pool writer** into the bundle (B2 landed gear_pool 0→150). `gates-on: —`
- [ ] **#2 Flavor-call WIRING** — `name_monster()` (MUST) · `name_skill()` flavor_text · `name_gear_item()`. **Wiring only in W1 — the calls FIRE in W3 per the Gate-1 #4 split**: kit-identity flavor on gauntlet SURVIVORS ONLY; monster/gear/faction flavor keys off bundle-membership (written once at assembly). **All calls per-item → resumable, no double-billing on retry** — verify + state this property explicitly in the completion record (spec §11 Q1-iii assigns this verification to you + KR). `gates-on: —`
- [ ] **#8a Registry schema DRAFT** (G9: you draft, jack-ryan ratifies — no Matt gate): run_id · timestamp · config hash · bundle path · gauntlet summary · cert status. **Draft FIRST in your session and flag it in your completion record** — KR routes it to jack-ryan for the W0/W1-boundary fast pass. `gates-on: —`
- [ ] **#8b Registry writer — DO NOT BUILD in this session.** `gates-on: registry-schema-ratified` (Gate-1 #5, Disc #8: ratify BEFORE the writer builds against it). KR re-dispatches the writer the moment ratification lands.
- [ ] **G6 supersession**: mark the ~60 null-name gear stubs + unapplied weapon descriptors **non-canonical** — never ship. `gates-on: —`
- [ ] Smoke-test passes · MIGRATION.md · AGENT_STATE.md updated
- [ ] Tag: `star-lord/v-demo-run-w1-1`

## Quality criterion (OP §3.11)

**Game-quality goal this dispatch serves:** criterion A+B — ONE callable driver, ZERO hollow spots. The demo's face (names, flavor, factions, gear, weapons) arrives complete because the pipeline emits it, not because anyone hand-patched it (§20d honesty: the engine is the product).

**Refutation conditions** (surface before executing if any apply):
- Any wiring path would require hand-authoring content (violates zero-hand-authored ruling)
- The driver shape conflicts with PART C stage-1/2 (callable → registered) direction
- Acceptance could pass with a bundle that has a present-but-empty content type (key exists, zero rows) — the criterion-B assertion must be key-present AND non-NULL count
- A flavor call is NOT per-item-resumable (double-billing risk) — surface loud, this is a load-bearing spec assumption (§11 Q1-iii)

## Acceptance criteria

- [ ] DDA-lock widened; proxy-family `primary_t4` emits in test
- [ ] Driver callable; six-type bundle emitted from a production-path fixture; `proxies` key present
- [ ] Round-trip smoke: key-present + non-NULL count per all six types at consumer boundary
- [ ] Registry schema draft flagged for jack-ryan; #8b writer NOT built
- [ ] ~60 stubs marked non-canonical
- [ ] Per-item flavor resumability verified + stated
- [ ] MIGRATION.md updated before tag

## Out of scope

- Firing the LLM flavor calls (W3) · the emission run itself (W3) · un-gating proxy bins (W3 step 1, rocket)
- The #8b registry writer (separate follow-up dispatch post-ratification)
- B3 backfill (SUPERSEDED, G6) — do not fill the 60 stubs
- Trigger layer / web tracker (PART C stages 3-4, post-demo)

## References

- Spec §1/§3/§11 · serial tracker PART B + D.1 · B2 record `a916632` · MIGRATION v1.84 · decisions-log `a10a695`
