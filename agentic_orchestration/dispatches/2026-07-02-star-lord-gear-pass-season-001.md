# Dispatch — 2026-07-02 — star-lord — gear pass against LOCKED season-001 (B2, Lane B)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-07-02 (serial-emission ledger D.1 #5; KR relay `gandalf/notes/2026-07-02-kr-relay-two-lane-fire-order.md` §3.2 + Lane B; gear-source RULED = generation pass against season-001, NOT a different season)
**Estimated effort:** 1–2 days
**Acceptance:** the demo bundle carries a **populated gear pool** generated against the LOCKED season-001 (the same season the two designated summoners live in), and the `main_weapon`≈`main_hand` 11-slot vocab divergence drax flagged is reconciled.
**Status:** 🔥 FIRING — **Gate-1 CLEARED (jack-ryan DESIGN-MODE, ENDORSE-WITH-FOLDS ×4; folds B2-1…B2-4 applied)**. B1-REBASE closed → engine tree free (Lane B serial). Feeds Lane A D8 (core DONE; UI Q7-blocked) via non-blocking data swap into drax's shipped D4 loader.

## Context

Matt ruled the gear source (relay §3.2): **generation pass against the LOCKED season-001** — NOT a different season. Swapping seasons would orphan the two designated summoner host-kits (`...int_none_s2` / `...int_none_s1`) and invalidate the D4 round-trip. The bundle currently ships `gear_pool=0` (season-001's telemetry.db has no `gear_instances` table; ledger D.1 #5). The 200-item gear writer "works when called" (ledger PART B) — this dispatch calls it against season-001 and folds in the vocab reconcile drax surfaced at D4 close.

**The vocab reconcile:** drax's loader consumes the 11-slot `gear_representative` non-fatally (deduped WARN) but flagged the divergence — the emit ships `main_weapon`/`secondary_item`/extra `legs` where canonical is `main_hand`/`off_hand`. Confirm whether the 11-slot generation vocab is canonical (then drax trims his loader's slot list) OR reconcile toward the 10-slot canonical. Your call as schema author; document it in MIGRATION and hand the ruling to drax.

## Required reading before starting

- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` D.1 #5 (gear pool gap) + PART B (the gear writer state) + PART D.1 #4 (weapon descriptor — rides B3)
- `agentic_orchestration/dispatches/2026-07-02-drax-godot-bundle-loader.md` (drax's D4 CLOSE record — the 11-slot gear-vocab flag, "For knight-rider to route")
- `src/reincarnated/export/one_realm_bundle_assembler.py` (`_load_gear_pool()` + the gear_representative passthrough) + the 200-item gear writer
- `src/reincarnated/export/MIGRATION.md` §v1.83 (the LOCKED schema you extend)

## Cross-seam contract change? (Principle 6 gate — YES)

The gear pool populates a bundle field drax consumes; the vocab reconcile changes a schema drax reads.
- `Round-trip: MIGRATION.md entry (v1.84) documenting the populated gear-pool shape + the gear_representative vocab ruling; drax re-runs bundle_roundtrip_smoke.gd against the re-emitted bundle to confirm the populated pool loads. Cross-seam contract → MIGRATION before tag (ADR-004).`

## Scope

- [ ] Drive the 200-item gear writer / `_load_gear_pool()` against the LOCKED season-001 → populate the bundle `gear_pool`
- [ ] **Vocab reconcile (jack-ryan Gate-1 fold B2-2 — two disposition classes, different authority):** rule on the 11-slot `gear_representative` vs 10-slot canonical divergence. **(a) 11-slot declared canonical → drax trims his loader slot list:** pure documentation, star-lord-owns as schema author (ADR-002 within-seam) — document in MIGRATION, hand to drax, fire it. **(b) reconcile TO 10-slot:** this touches the generation-side `gear_representative` — a cross-seam schema change to a LOCKED emit (v1.83) — which is **ESCALATE-to-Matt via KR**, NOT a silent star-lord ruling (ADR-002 tiered; Principle 4 — LOCKED-state is truth). Do not self-serve path (b)
- [ ] **jack-ryan Gate-1 fold B2-1 (RESCOPED — the D8-in-flight hazard is stale):** D8's *core* is already DONE (`drax/v-godot-grimoire-scouting-ui-1` @ `300d07b`); only its on-screen UI layer is Q7-rig-blocked — there is NO live concurrent build against the 11-slot schema for your ruling to change out from under. The real consumer at risk is **drax's SHIPPED D4 loader** (`bundle_loader.gd`, deduped-WARN gear-slot handling). A **10-slot** ruling still needs the **KR flag** (it changes a schema drax's landed loader reads), but the collision is with the shipped loader, not an in-flight D8 build. Ruling toward 11-slot-canonical (drax trims) is collision-free. Cite: Principle 6 (cross-seam impact); Discipline #42 (framing-audit — the original B2-1 framing was refuted by MASTER line 27, D8 core done)
- [ ] Re-emit the bundle (schema_status stays LOCKED; season-001; the two designated summoners' proxies preserved — do NOT drop them) with the populated gear pool
- [ ] `validate_bundle()` passes (gear records carry all required fields; III.7 clean; no telemetry keys)
- [ ] MIGRATION.md v1.84 entry (populated gear pool + vocab ruling)
- [ ] Empirically verify (Discipline #11): `gear_count > 0`; **the two summoner kits' proxy blocks are pre/post-re-emit DIFFED — byte-identical OR an explicitly-ruled delta (jack-ryan Gate-1 fold B2-4)** — a presence-only "STILL non-empty" check misses mutation; re-emit could preserve *a* proxy while changing it; gravecaller still absent
- [ ] AGENT_STATE updated
- [ ] Tag: `star-lord/v-gear-pass-season-001-1`

## Acceptance criteria

- [ ] Bundle `gear_pool` populated from season-001 (`gear_count > 0`) **AND each gear record carries a `scaffold`/provenance flag until B3 names it (jack-ryan Gate-1 fold B2-3, Discipline #40)** — populated gear values entering the LOCKED production bundle are scaffold-in-production-path; un-flagged gear values BLOCK (B3 must be able to tell generated-placeholder from ratified)
- [ ] The gear_representative vocab divergence ruled + documented (MIGRATION) + handed to drax
- [ ] Re-emit preserves the LOCKED summoner proxies + gravecaller-absent invariants (no regression on the D4-proven content)
- [ ] MIGRATION v1.84 + validate_bundle passes

## Out of scope (explicit non-goals)

- **LLM gear NAMING** — rides B3 (the flavor-completion pass); B2 populates the pool, B3 names it
- Monster/skill/faction flavor completion (B3)
- The demo emission run (B4) — this is a gear pass on the EXISTING season-001, not a new emission
- Changing the two summoner designations or the season (Matt ruled season-001 held)

## Quality criterion

**Game-quality goal:** Lane A D8 (and the demo loadout) builds against a REAL engine-emitted gear pool, not `gear_count=0` — the six-type demo bundle (Matt-ruled all-six-types 2026-07-02) gets its gear leg, honestly pipeline-emitted.

**Refutation conditions (surface if any apply):**
- The gear writer requires a different season to populate (would orphan the summoners — surface to Matt, do NOT swap seasons)
- The vocab reconcile forces a schema change that breaks drax's D4-proven loader (coordinate at MIGRATION before tagging)
- Re-emit drops or mutates the two summoner proxies (regression on the D4 close — the invariant check must catch this)
- Gear items ship without required fields (validate_bundle must fail closed, not paper over)

## Open questions for the agent to resolve (document; escalate schema conflicts to KR)

- Whether the 11-slot generation vocab is declared canonical (drax trims) or reconciled to 10-slot canonical (which touches the generation-side gear_representative) — your ruling, documented
- Whether LLM gear naming is cheap enough to fold into THIS pass or genuinely belongs in B3 (default: B3 per the relay; note if you'd combine)

## References

- serial-emission ledger D.1 #5/#4 · drax D4 CLOSE record (vocab flag) · one-realm §5 ask 1 (all-six-types)
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` (Lane B)
