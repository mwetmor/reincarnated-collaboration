# Dispatch — 2026-07-11 — rocket (lead) + star-lord (attribution spine) — E3 Element-Application binder (v1 partitions)

**From:** knight-rider
**To:** rocket (LEAD — binder + generation), star-lord (attribution spine — v1-BLOCKING, rides this dispatch)
**Co-signers:** gamora (resolver-consumption contract only — co-signs the math note; NO gamora build this dispatch)
**Approved by:** Matt 2026-07-11 (transmission: *"draft + fire the E3 element-application dispatch (rocket + star-lord)"*; all design RULED — zero design elicitation)
**Estimated effort:** multi-day (Pattern B — dedicated session)
**Acceptance:** `chain_partition` + `geometry_partition` ship, honestly certified; the binder is born; the Option C tuple is deleted; the attribution spine measures realized elemental output-share; SPINE untouched; round-trip GREEN.

---

## §0 — Context (why this, why now)

E3 is the fourth axis of the full-spec main line (E1→E2→E4→**E3**). All design landed and is Matt-ruled — this dispatch operationalizes ruled intent, it does NOT re-open design. The canonized authority is `canonical/reap-die-rise-engine/engine-doctrine-and-element-application-2026-07-11.md` **Part C**; the mechanical surface + binding resolver is `canonical/current-to-end-state/mechanical-reality.md` **§4/§5/§9**.

**The headline (scaffolding audit, Matt-confirmed):** v1 partitions block on NOTHING new. `chain_partition` is LIVE (Amendment 7a per-chain elements, `per_skill_emitter.py`); `geometry_partition` is runtime-free pipeline logic. The two families that ship here need no new capability layer — they BIND to machinery that already exists. This is why E3 is the build-ladder item #1 and the hook layer (ladder #2), component accounting (#3), phase axis (#4), and emission primitive (#5) all queue BEHIND it.

**The binder law (Part C-1, do-not-regress C-10):** the element block is a *binder over existing machinery, never new machinery.* Structure creates capability only in kernel/chain/emission layers; element application binds to capability slots that already exist. **Generation-time law:** the binder stamps concrete fields at generation; the sim reads only resolved fields; the gauntlet certifies the RESOLVED kit; presentation rides the same resolved fields. NO sim-time element decisions — grep-provable.

**Line-citation note (source-verified 2026-07-11, supersede any stale doc cites):**
- `HYBRID_RATE = 0.175` — definition `season_generation_pipeline.py:233`; roll site `:662` (mechanical-reality.md §3 says `:664` — use `:662`).
- Kit-level scaling stamp (the site that flips to per-chain): `damage_scaling_type = _BC_ATTRIBUTE_TO_SCALING_TYPE.get(...)` at `per_skill_emitter.py:1114`; `scaling_attribute = _BC_ATTRIBUTE_TO_SCALING_ATTR.get(...)` at `:1115`. Downstream stamps at `:1234`, `:1303`, `:1315`, `:1470` (summon path). Confirm the full set at math-note time.
- Option C tuple lives across THREE files: `bc_target_substrate_engine.py` (`allow_cross_attribute` param `:479`, use `:519`), `bc_target_subspace_generator.py` (`:342-343`, `:479`, `:534-535`), `bc_target_cell_sampler.py` (`allow_cross_attribute`/`option_c_cross_attribute` fields `:62-63` + every CellDef literal). Deletion touches all three. **Non-routing reference (JR-1):** `bc_target_player_class.py:102` docstring names `option_c`/`allow_cross_attribute` — scrub to keep grep-clean post-deletion (no live consumer there; routing stays the three files; Discipline #10).
- Amendment 7a per-chain elements: `per_skill_emitter.py` (`:864/:1136/:1279` per mechanical-reality §3); `chain_partition` walker = `chain_B := secondary`.
- **`HYBRID_RATE` roll-site `:662` vs the `:664` in mechanical-reality §3 + canon C-5/B.1 (GD-4):** the roll is source-verified at `:662`; the two Matt-facing living surfaces cite `:664`. rocket confirms at math-note time; **SAME-COMMIT maintenance law — update the `:664` cites in `mechanical-reality.md` §3 and `engine-doctrine-and-element-application-2026-07-11.md` C-5/B.1 to the confirmed line at math-note close** so the surfaces don't drift.

---

## §1 — Target seams & serialization

- **rocket (LEAD):** owns `generation/` — the NEW binder, the `element_application` block, the two v1 walkers, the tuple deletion, the `naming_flavor_element` split, the scaling-unification T4, masks/pins, the `HYBRID_RATE` dial promotion.
- **star-lord (v1-BLOCKING, same dispatch):** owns the attribution spine — kill-attribution-by-element + realized-share telemetry columns. **The rate-band law is unenforceable without it** (Part C-5 realized-share semantics: the cert measures output-share, which requires per-element attribution). This is not a follow-up; it ships in this dispatch.
- **gamora (co-sign only):** co-signs the math note's **resolver-consumption contract** — confirms the sim reads resolved fields exactly as the binder stamps them (generation-time law), and that realized-share is measurable on the existing damage-event stream. **NO gamora BUILD this dispatch.** (gamora's build energy is reserved: E4 PHASE-2 queued behind the pilot; hook layer ladder #2 behind this one.)

**Serialization law (unchanged, restated):** the **gamora seam is the serialization point, not the sessions.** Do NOT interrupt / re-task / close the open pilot KR session. Its completion-build + Gate-2 + post-2026-07-10 git signal is the E4-PHASE-2 unblock — checked via git, never by asking it. This E3 dispatch does not touch the pilot's work.

---

## §2 — Math note FIRST (Discipline #1) — NO code before it closes

**File:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/element-application-binder-2026-07.md`
**Lead:** rocket. **Co-sign:** star-lord (attribution columns) + gamora (resolver-consumption contract). ONE conversation, ONE note.

Must derive / pin before any code:

1. **Per-chain scaling law.** `scales_with` (element → stat) flips BOTH `damage_scaling_type` AND `scaling_attribute` at the existing per-chain derivation site (`per_skill_emitter.py:1114-1115` adjacency), REPLACING the kit-level stamp. Derive: for each chain's element, the (type, attribute) pair; the physical-chain-on-magical-kit case (K15 Spellsword: one physical chain + magical chains — the blade is physically typed, mitigation branches to dodge/block/armor per `damage_resolver.py:439+`). **Baseline law (R-6):** every chain's element scales off *its own element's* stat by default — the scaling-unification T4 (item 4) is the OVERRIDE. **(JR-5) The note MUST enumerate the FULL downstream-stamp set** — which of `:1234/:1303/:1315/:1470` (summon path) flip to per-chain vs stay kit-level BY DESIGN — and resolve it before code, not defer it to build. No scaling-derivation hole left under the code.
2. **rate_band → realized-share arithmetic.** `splash` = 10–25%, `co_equal` = 40–60% of **gauntlet-measured elemental OUTPUT share** (NOT slot count — Part C-5 load-bearing sentence: slot count lies; a spender owns most output). Derive the mapping from band enum to the certifiable output-share target, and the < 100% ceiling (full supersession is a reskin, not hybridity).
3. **Scaling-unification T4 override math.** "All elements scale off primary stat" — overrides scaling **STAT only** (type / geometry / mitigation stay per-chain). The T4 slot IS the price of co_equal (splash rides free). Derive: how the capstone catalog entry stamps the override; rollable + pinnable; the un-T4'd co_equal decay it prevents (the GD Battlemage disease).
4. **Geometry-partition rule.** The kernel-geometry-class → element map (e.g. {flies → frost, pools → fire}); the mask `hard_constraint` (kit spans ≥2 geometry classes to be eligible). Runtime-free — pure pipeline assignment.
5. **`HYBRID_RATE` governed-dial promotion.** From buried constant (`:233`) to config-surfaced governed dial. Derive the config surface + default (0.175 preserved).

**Resolver-consumption contract (gamora co-sign):** the exact resolved-field set the binder stamps (per-skill element, per-chain type/attribute) and the guarantee the sim reads ONLY those — no sim-time element branch. Realized-share is measured on the resolved output.

**Attribution-column contract (star-lord co-sign):** the per-element attribution columns (kill-attribution-by-element + realized-share) — schema, what a "damage event" carries, DoT-tick coverage (later: components/emissions/proxy attacks).

---

## §3 — rocket scope (build, AFTER the note closes)

- [ ] **NEW `generation/element_application_binder.py`** — the four addresses (Part C-1 / mechanical-reality §4): capability slots (element-blind) · `element_application` block · the ~7-walker rulebook (only `chain_partition` + `geometry_partition` LIVE this dispatch; the other five are stubbed data-map entries that ship WITH their capability layer, never ahead — do NOT build them). Sited at the emitter stage where Amendment 7a chain-element resolution already runs. **Generation-time law grep-provable.**
- [ ] **`element_application` block** in the ONE versioned kit packet: `{primary, secondary (HARD CAP one), structures [x1..2], rate_band}`. (Composes with the E4 versioned packet contract — same packet, new block.)
- [ ] **`chain_partition` walker:** `chain_B := secondary` (Amendment 7a already live — wire it under the binder's rulebook, don't reinvent).
- [ ] **`geometry_partition` walker + mask:** geometry-class → element map; `hard_constraint` (≥2 geometry classes). Pipeline assignment.
- [ ] **Option C tuple DELETION:** remove `allow_cross_attribute` / `option_c_cross_attribute` + all consumer sites across `bc_target_substrate_engine.py`, `bc_target_subspace_generator.py`, `bc_target_cell_sampler.py` + the `bc_target_player_class.py:102` docstring reference. (`attribute_coupling` / StatDistributionV2 SURVIVE — general Layer-4 sheet machinery, unrelated to the retired cross-attribute tuple. Do NOT delete those.) **(JR-2) Grep-clean acceptance:** post-deletion `grep -rn 'allow_cross_attribute\|option_c_cross_attribute' src/reincarnated/generation/` returns ONLY surviving `attribute_coupling`/StatDistributionV2 sites — zero references to the retired tuple, docstrings included.
- [ ] **`secondary_element` → `naming_flavor_element` split:** mechanical role → `element_application.secondary`; flavor directive → `naming_flavor_element` (naming-only, Do-Not-Regress C-10 — no mechanical consumption, ever). **Open question flagged (§11):** `t4_category_schema.py select_secondary_element()` / `DUAL_ELEMENT_ADDITION` is a SEPARATE pre-existing T4 mechanic — the split must NOT conflate the flavor field with that capstone category. Resolve at math-note time.
- [ ] **Scaling-unification T4** into the capstone catalog — rollable + pinnable; stat-only override.
- [ ] **Masks + ruled pins:** K15 = `chain_partition` + `co_equal` + scaling-T4 · K20/K23 = splash. (H5 → `flat_split` at v2 — NOT this dispatch.) Masked sampling with pin-capable anchors (Part C-6). **This dissolves the batch-2 sample-vs-pin fork operationally — anchors PIN, variations SAMPLE under masks** (but the fork stays a named KR+Matt decision; do NOT resolve it here).
- [ ] **`HYBRID_RATE = 0.175` → governed dial** (config-surfaced).

## §4 — star-lord scope (v1-BLOCKING, same dispatch)

- [ ] **Attribution spine:** kill-attribution-by-element + realized-elemental-output-share telemetry columns. Covers DoT ticks at v1 (later: components / emissions / proxy attacks — noted, not built).
- [ ] Joins the fingerprint columns (Part B.3 / C-5) — the realized-share cert reads these. Without this, the rate-band law cannot be certified — this is the gating dependency for §6.

---

## §5 — Cross-seam contract change? (Principle 6 gate — KR completes at authoring)

**YES.** This dispatch adds the `element_application` block to the kit packet, adds per-element attribution columns to the telemetry schema (star-lord), and changes per-chain scaling field derivation. Cross-seam boundaries touched: generation→sim (resolved-field contract), generation→telemetry (attribution columns), packet shape.

**Therefore ADR-004 MIGRATION.md REQUIRED** at the seam boundary — rocket-authored (packet + resolved-field contract), star-lord co-authors the attribution-column section. Note downstream consumers in it: **the hook layer** (ladder #2 — its fourth walker family `rider_on_hit`/`proc_trigger` → HookEntry emission is DESIGNED at `gandalf/notes/2026-07-11-hook-layer-design-note.md` but BUILDS behind this dispatch; note as downstream consumer, do NOT draft) · **B12 spin-channel re-cert** (downstream consumer note only) · **Presentation/VFX seam (drax, Godot) (GD-3)** — downstream consumer of the resolved per-skill `element` field + `naming_flavor_element`; note the C-8 legibility contract (per-button palette purity for partitions; secondary palette on emitted entities for carriers-later). Note as consumer, do NOT draft · component accounting / phase axis / emission primitive (later ladder items).

**Acceptance MUST include the round-trip clause (§9).**

---

## §6 — Certification protocol (FLAG — executes at cert stage, not build)

Breadth price is **SIM-MEASURED, never assumed** (Matt ⑧-entry ruling, verbatim: *"let the balance sim speak… It's not obvious to me that 10%–15% will be correct"*). At cert:
- Run the pinned four + a mono control through the gauntlet with a **counter-breadth matrix** + **mono-resist / mixed-defense / armor-heavy** regimes.
- Band the breadth price to neutralize MEASURED advantage. **10–15% is a demoted PRIOR, not a target.**
- Registered prediction (record it, test it): advantage concentrates in mono-resist + armor-heavy, near-zero neutral; residual after the T4-slot cost may be < 10%.
- Standard gauntlet + realized-share check against the declared band (Part C-7). Pre-registered degenerates to hunt: partition relocating a control/DoT rule-package onto a high-frequency chain role (perma-slow / stacking exploit — the chain-role × rule-package matrix is the exploiter's hunting ground).

This is a FLAG for the cert stage — the build lands first, cert measures. Note it in the MIGRATION/AGENT_STATE so the cert run is not skipped.

---

## §7 — Round-trip smoke (MANDATORY, Principle 6)

- [ ] **Round-trip smoke:** emit a hybrid kit (chain_partition, co_equal — use the K15 pin) through the production emission path → resolved packet carries the `element_application` block + per-chain type/attribute stamped → sim reads resolved fields → telemetry attribution columns populate with per-element output share → field-presence + realized-share-nonzero check at the consumer boundary. Reproducible artifact committed (E4 precedent: `eb4be4c` — a commit asserting "PASS" without the runnable instrument is a Gate-2 BLOCK).
- [ ] **(JR-3) DoT-tick attribution:** the round-trip fixture MUST include at least one DoT-emitting chain so per-element attribution is exercised over a tick stream, not only direct hits — field-presence on the DoT path is v1-BLOCKING per §4. (Smoke can otherwise go GREEN with the DoT attribution path untested — a Gate-2 gap.)
- [ ] **(GD-1) Legibility-field check (C-8):** verify the resolved per-skill `element` field is the SAME field presentation consumes — assert per-button palette purity for `chain_partition`/`geometry_partition` kits (each skill wears one element's palette). No separate presentation rules-engine (mechanical-reality §4 generation-time law). **Field-presence / field-contract check ONLY** — VFX build is downstream; this asserts the field contract is legibility-ready.
- [ ] **SPINE SACRED:** zero diffs to the tier/damage/energy/cooldown spine tables — element application is a binder LAYER, not a spine change. SHA-256 zero-diff verification in the smoke (E4 precedent).
- [ ] Geometry-partition round-trip: emit a ≥2-geometry-class kit → verify the geometry→element map stamps per-skill elements correctly.

---

## §8 — Verdict instrument (#2-FF — for Gate-2 jack-ryan)

- **Verdict instrument named:** the round-trip smoke artifact (§7) + the per-chain scaling unit path + the tuple-deletion test sweep + `pytest` full suite (no new failures) + grep-provable generation-time-law audit.
- **One-command path (JR-4):** the exact command that reproduces the smoke AND the reproducible-artifact path are recorded in **AGENT_STATE.md**, not solely the commit message (E4 `eb4be4c` precedent — a PASS assertion without the runnable instrument is a Gate-2 BLOCK).
- **Precondition state:** math note CLOSED (rocket + star-lord + gamora co-signs) before any code; MIGRATION.md present at seam; attribution columns live before the realized-share cert can run.

---

## §9 — Acceptance criteria

- [ ] Math note `element-application-binder-2026-07.md` CLOSED (rocket-led; star-lord + gamora co-signs).
- [ ] `element_application_binder.py` born; four addresses present; generation-time law grep-provable.
- [ ] `chain_partition` + `geometry_partition` walkers LIVE; other five structures stubbed-not-built.
- [ ] Per-chain scaling: `scales_with` flips BOTH fields at ONE site; kit-level stamp replaced; K15 physical-chain case correct (mitigation branches).
- [ ] Scaling-unification T4 in capstone catalog, rollable + pinnable, stat-only override.
- [ ] Option C tuple DELETED across all three files; `attribute_coupling`/StatDistributionV2 preserved.
- [ ] `secondary_element` → `naming_flavor_element` split; naming-only Do-Not-Regress; no conflation with `t4_category_schema` DUAL_ELEMENT_ADDITION.
- [ ] `HYBRID_RATE` promoted to governed dial.
- [ ] Masks + ruled pins (K15 / K20 / K23) wired.
- [ ] **star-lord attribution spine LIVE** — per-element kill + realized-share columns.
- [ ] SPINE SACRED: SHA-256 zero-diff on spine tables.
- [ ] **Round-trip smoke:** production-path hybrid-kit emission → resolved packet `element_application` block + per-chain stamps → sim resolved-field read → telemetry per-element output-share populated + nonzero; reproducible artifact committed.
- [ ] **Legibility law (C-8) field contract honored (GD-2):** `naming_flavor_element` carries the Emberfrost proportional-rename directive; per-skill resolved element is the palette-driving field; per-family VFX legibility is not foreclosed (partitions = per-button purity). Field contract only — VFX build downstream.
- [ ] MIGRATION.md at seam (rocket + star-lord sections; downstream consumers noted).
- [ ] `pytest` full suite: no new failures.
- [ ] AGENT_STATE.md updated (rocket + star-lord); cert-protocol FLAG (§6) recorded so it is not skipped.
- [ ] Tags: rocket `rocket/v<X.Y>-element-application-3`; star-lord `star-lord/v<X.Y>-attribution-spine-1` (or per seam convention).

## §10 — Out of scope (explicit non-goals)

- **The other five structures** (`flat_split`, `rider_on_hit`, `proc_trigger`, `phase_partition`, `emission_carrier`) — stubbed data-map entries only; each ships with its capability layer later. Building any is scope creep.
- **The hook layer** (ladder #2) — design note is authority; queues BEHIND this dispatch; do NOT draft or build.
- **H5** → `flat_split` at v2 — not this dispatch.
- **gamora BUILD** — co-sign only; no sim build here.
- **The ninth-axis arity stress-test** — slotted separately (see the ninth-axis note); rocket archive plumbing may ride alongside per KR's sequencing, but the arity MEASUREMENT is gamora-gated behind E4 PHASE-2.
- **batch-2 fire / bench-promotion elicitation / B12 re-cert / phase axis / emission primitive / Q14 ONE band re-anchor.**
- **Resolving the batch-2 sample-vs-pin fork** — stays a named KR+Matt decision.

## §11 — Open questions for the agent to resolve (document in the note)

- The `secondary_element` vs `t4_category_schema.DUAL_ELEMENT_ADDITION` vs `element_application.secondary` three-way disambiguation — which consumers repoint where. (Flavor field renames; mechanical role moves to the block; the T4 category is a separate pre-existing mechanic.)
- The full set of downstream scaling-stamp sites (`:1234/:1303/:1315/:1470` summon path) — confirm the per-chain flip covers all, or document which stay kit-level by design (e.g. summon skill scaling).
- Geometry-class → element map's exact class taxonomy (which of the 24 `geometry_type` / 6 `spatial_geometry_type` classes map to which elements) — the doctrine gives the pattern ({flies→frost, pools→fire}); the concrete map is the agent's to derive and pin in the note.
- Attribution-column granularity for DoT ticks vs direct hits at v1.

## §12 — References

- `canonical/reap-die-rise-engine/engine-doctrine-and-element-application-2026-07-11.md` — **Part C** (C-0…C-10), Appendix A audit, R-5/R-6/R-8/R-9 reconciliation rows.
- `canonical/current-to-end-state/mechanical-reality.md` — §4 binding resolver (four addresses + walker table), §5 surfaces register (rows 1/2/S), §9 build ladder item 1.
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` — 2026-07-10 seventh + eighth entries (E3 design + rump rulings); 2026-07-11 second entry (K15/H5 ruling, ninth-axis priority).
- `agentic_orchestration/gandalf/notes/2026-07-11-hybridity-mechanical-scaffolding-audit.md` — the binding-surface audit (register of record for gaps).
- `agentic_orchestration/gandalf/notes/2026-07-11-hook-layer-design-note.md` — downstream consumer (ladder #2); note in MIGRATION, do NOT build.
- E4 precedents: `dispatches/2026-07-10-rocket-commitment-axis-E4.md` (versioned packet + round-trip + #2-FF pattern); reproducible-smoke lesson (`eb4be4c`).

---

*Gate-1 status: **CLEAR — FIRE-READY.** Critique pair ran in parallel 2026-07-11. jack-ryan DESIGN-MODE **PASS-WITH-AMENDMENTS** (5: JR-1 docstring-scrub `bc_target_player_class.py:102`; JR-2 §3 grep-clean acceptance; JR-3 §7 DoT-tick attribution; JR-4 §8 one-command path→AGENT_STATE; JR-5 §2 downstream-stamp enumeration). gandalf **CONCUR-WITH-AMENDMENTS** (4: GD-1 §7 legibility-field check C-8; GD-2 §9 legibility-law acceptance checkbox; GD-3 §5 MIGRATION presentation/VFX seam→drax; GD-4 §0 `HYBRID_RATE` :664→:662 SAME-COMMIT). All 9 folded. No blocker raised by either critic. gandalf's one genuine fidelity gap (C-8 Legibility Law dropped in translation) closed by GD-1/2/3.*
