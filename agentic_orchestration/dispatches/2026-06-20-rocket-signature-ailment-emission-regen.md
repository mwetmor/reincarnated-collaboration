# Dispatch — rocket: signature-ailment emission regen (is_control != hard cut)

**Type:** Pattern B (multi-step: generation fix + regen + MIGRATION.md + decisions-log). Dedicated session.
**Author:** knight-rider, 2026-06-20. Matt-authorized (three decisions, 2026-06-20): (1) regime-wide ailment-emission fix APPROVED; (2) emission breadth = the **`is_control != hard` cut**; (3) boss/mini-boss armor-nerf rides the single downstream gamora refit.
**Seam:** generation (`reincarnated-engine/src/reincarnated/generation/`). rocket owns.
**Gate-1:** jack-ryan DESIGN-MODE before this publishes / before rocket tags.
**Gate-2:** jack-ryan DEV-MODE on the resulting commit(s).

---

## 0. Why this regen (the premise this closes)

The DoT/mitigation-symmetry Arm B run (gamora, `e537b29`, Gate-2 PASS-WITH-INFO `7099e49`) measured that the season-001 faithful-power population carries **0 of 66 DoT sources** — STR-tagged kits carry zero `tick_damage`. The bleed lever STR was designed to carry **does not exist on the population**. rocket's diagnosis (`generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md`) pins this as a **wiring bug, not a mapping gap**: the active per-skill-emitter generation path never calls the (intact) ailment-emission machinery.

This regen restores signature-ailment emission so the population carries the ailments the substrate already assigns by element. It is the **generation-side counterpart** to gamora's already-committed F1 DoT-activation (sim-side). It is the gating predecessor to the deferred **Arm C** re-fire (the bleed-as-lever test, gandalf pre-reg `df1023b`) and to the **single gamora refit** (band refit + boss/mini-boss armor-nerf).

## 1. The fix (surgical, recompose-first — NO new mechanic)

Teach `per_skill_emitter.emit_skills_for_kit()` to emit the element's signature ailment **alongside** `damage` on **primary-attack-chain skills**, using the existing `ELEMENT_AILMENT[config.element]` map and the existing `_make_ailment`-equivalent param shape (`tick_damage` + `duration_seconds` for dot ailments). **Re-confirm all anchors first-hand** — they may have drifted since the 2026-06-20 diagnosis.

**Anchors (diagnosis-cited; re-verify):**
- `per_skill_emitter.py:389-497` — `emit_skills_for_kit()`, the season-001 skill generator
- `per_skill_emitter.py:464-469` — the one-effect-per-skill site to extend
- `element_biases.py:70` — `"physical" → "bleed"` (wiring correct, intact)
- `ELEMENT_AILMENT` / `_make_ailment` (`ability_grammar.py:556-595, 649-744`) — the existing param shapes to mirror (do NOT re-route generation through the unused `ability_grammar` path; mirror its ailment-param shape inside the emitter)
- `foundation/ailment_loader.py:342` — `get_hard_control_ailments()`, the cut predicate (gandalf-confirmed)
- `season_generation_pipeline.py:192` — `STAT_ELEMENT_POOLS`; `:484-507` — `_draw_cell_elements`
- **Breadth (which skills carry the emit) is `a9cd243`'s ruling, ORTHOGONAL to the cut: `chain_A` primary-attack, all 4 tiers.** The cut decides WHICH ailments; `a9cd243` decides WHICH skills. Emit on primary-attack-chain only — **NOT** on `secondary_attack`, even though `per_skill_emitter.py:464-469` names BOTH "damage."

### The cut: `is_control != hard` (gandalf-classified, `gandalf/notes/2026-06-20-is-control-cut-classification-and-signature-assignment.md`)

Implement as a **rule against the engine's own `is_control` field**, NOT a hand-maintained list:
> emit `ELEMENT_AILMENT[config.element]` on primary-attack skills **UNLESS** that ailment is in `get_hard_control_ailments()`.

**EMIT (5/8):**
| ailment | element | signature | tick scaling attr |
|---|---|---|---|
| bleed | physical | DoT `tick_damage` from `base_mag` | str/dex (originating skill's scaling attr) |
| burn | fire | DoT `tick_damage` | int/wis |
| drain | shadow | DoT `tick_damage` | int/wis |
| chill | water | **slow-only, NO damage tick** (signature IS `slow_percent`; zero DPS-band contribution) | n/a |
| consecrate | holy | shadow-target-only DoT + heal-amp (near-zero DPS vs non-shadow synthetic mob) | int/wis |

**EXCLUDE (3/8) — `is_control: hard`:** root (earth), knockback (wind), shock (lightning). These carry NO damage signature this regen (keeps CC-soup hazard out; this is what retires gandalf's diminishing-returns guardrail as a dependency).

**Scaling-attr routing must mirror `damage_resolver.py:312`** (direct-damage scaling-stat lookup) so emitted DoTs compose with gamora's committed F2 source-attribute tick-scaling fix (`e537b29`). bleed on a STR kit must tick on str, not int/wis.

### Math-note-first (Discipline #1 — REQUIRED before code)

rocket authors a math note BEFORE wiring, estimating:
- expected per-affected-skill effect-count delta (1 → 2 on primary-attack-chain skills that carry an emitting element)
- expected fraction of the 66-config population that gains an ailment, by attribute (STR→bleed on all mono-physical; casters→burn/drain/chill/consecrate by element pool; DEX→per-element)
- expected per-tick and full-fight DoT contribution at the EXISTING `0.003` tick coefficient (sanity-check the power injection against current bands — this sizes the downstream refit, it does NOT re-tune anything here)

## 2. Discipline — recompose-first, NO magnitude re-tune

Implement faithfully with the EXISTING ailment param shapes and the EXISTING `0.003` tick coefficient. Do **NOT** re-tune DoT magnitude, ailment_chance, or band values in this regen. The emitter is deterministic, so the `ability_grammar` probabilistic `constraint.ailment_chance` does NOT port — emission is a deterministic "yes, on primary-attack-chain skills." The PURPOSE is to make the substrate's existing intent function and MEASURE the shift (Arm C + refit), not to guess magnitudes.

**Chill is the recompose-first trapdoor — branch on ailment category.** Chill routes through the `soft_control` param shape (`slow_percent` + `duration_seconds`), NOT the `dot` shape. Do **NOT** synthesize a `tick_damage` for chill to fit a uniform emit path — that *invents* a mechanic the substrate never declared (gandalf §3a). The emit path must branch on ailment category (`dot` vs `soft_control` vs `amplification`), mirroring the three registry param shapes — not force all five through the dot shape.

## 3. Regen + acceptance

- **Regen:** YES — regenerate season-001 (`cycle-14-wave-5-season-001`) so the population carries signature ailments. Use the established regen path; tag the regen artifact.
- **Acceptance criteria:**
  1. STR-tagged mono-physical kits carry `bleed` with nonzero `tick_damage` on primary-attack-chain skills.
  2. Caster kits carry their element's emitting ailment (burn/drain/chill/consecrate per element); chill carries `slow_percent` and NO damage tick.
  3. NO kit carries root/knockback/shock as an emitted damage signature (hard-control excluded).
  4. Population ailment-source count rises from 0/66 to the math-note-predicted fraction; spot-verify against the prediction (Discipline #10 empirical inspection).
  5. Effect-list growth is additive (existing `damage` effect retained; ailment appended) — no existing effect dropped.
- **Smoke-test (Discipline #2):** small-N regen first (a handful of kits across STR + each caster element + one hard-control element), verify the emit/exclude split and tick-scaling attr first-hand BEFORE full regen. Resource-scaling rehearsal per #2.1. The hard-control smoke kit must **AFFIRMATIVELY show zero emitted ailment effect** (criterion 3's negative assertion is spot-checked in smoke, NOT deferred to full regen) — confirm `get_hard_control_ailments()` returns the populated `{root, knockback, shock}` frozenset first-hand before trusting the exclude.

## 4. Cross-seam — MIGRATION.md REQUIRED (ADR-004)

Kit-dict effect-lists gain entries → downstream contract shift for every consumer enumerating `skill.effects`:
- **gamora (sim):** already iterates effects and has `_DOT_AILMENT_NAMES`/`_make_ailment` tick handling + the committed F2 scaling fix → consumes new effects WITHOUT sim schema change. (The whole point of sequencing gen after sim's F1/F2.)
- **star-lord (telemetry/export):** any consumer assuming **one-effect-per-skill** sees a longer list per affected skill. NO new schema field (a population/value shift), but the per-skill effect-count coordination with star-lord is a **HARD pre-tag gate**: rocket confirms with star-lord that no telemetry/export path enumerates effects positionally or asserts single-effect BEFORE tagging. If such a path exists, it is a **BLOCK surfaced to knight-rider**, not a self-resolved item. The §9 hand-back "coordination result" must read **CONFIRMED-CLEAR or ESCALATED**.
- **drax (loadout/demo):** if loadout renders skill effects, the longer list surfaces there — note in MIGRATION for awareness (not a blocker this regen).

Author `MIGRATION.md` documenting: the effect-list contract change, the consumers, and that no schema field is added.

## 5. decisions-log (architectural commitment)

This is a generation-architecture commitment worth recording (jack-ryan canonical-writes the entry, not rocket): *"season-001 generation path emits signature ailments per element on the primary-attack chain, gated by the `is_control != hard` cut."* Include: the cut rule, the EMIT/EXCLUDE split, the primary-attack-chain which-skills ruling, the deterministic-emit (no ailment_chance port), and the band-shift/refit dependency. The EMIT-set cardinality (**5 with consecrate IN / 4 with consecrate OUT**) reflects Matt's consecrate disposition locked at launch — jack-ryan writes the **as-launched** set, not the as-authored set. rocket flags the entry need at hand-back; jack-ryan writes it at Gate-2.

## 6. Band-shift dependency (NOT this dispatch)

Emitting the DoT trio = a power injection → bands shift. This regen CREATES the population; it does **NOT** refit bands or touch the production gate. The refit is the **single downstream gamora pass** (band refit + boss/mini-boss armor-nerf, sized on Arm C + Q3 data). Generation-side (this) and sim-side (gamora refit) must be **sequenced together** — do not refit until this regen lands and Arm C re-fires. Net DPS-band injection is **DoT-trio-driven only** (chill = slow-only, consecrate = shadow-only near-zero vs synthetic mob), per gandalf.

## 7. Out of scope (do NOT pull in)

- Magnitude / ailment_chance / band re-tuning (downstream, data-driven).
- The deferred control-ailment-damage-signatures proposal (thorny-root / cut-bleed / cold-burn) — gandalf confirmed NOT needed; it was for hard-control ailments, which the cut excludes.
- Re-routing generation through the unused `ability_grammar` path — mirror its ailment-param shape inside the emitter; do not redirect the pipeline.
- The Arm C re-fire and the gamora refit (separate downstream gamora dispatches).
- Hard-control damage signatures + the diminishing-returns guardrail (retired as a dependency by the cut; re-opens only if hard-control signatures are ever added).

## 8. Tag intent

Seam-prefixed: `rocket/v<X.Y>-ailment-emission-regen-<n>`. Milestone (de-prefixed) only on Matt approval.

## 9. Hand-back (§ rocket → knight-rider)

- math note (effect-count delta + population fraction + expected DoT contribution at 0.003)
- the emitter change + regenerated season-001 artifact (tagged)
- MIGRATION.md (effect-list contract; consumers; star-lord effect-count coordination result)
- decisions-log entry NEED flagged for jack-ryan canonical-write
- spot-verification of acceptance criteria 1-5 against the math-note prediction
- explicit confirmation the EXCLUDE(3) hard-control ailments carry no damage signature

Then: jack-ryan Gate-2 → gamora Arm C re-fire (df1023b) → gamora single refit (band + boss/mini-boss nerf).

---

**Open confirm (knight-rider → Matt, pending at authoring):** `consecrate` is `is_control: none` (amplification), so the literal `is_control != hard` cut INCLUDES it. Authored with **consecrate IN** per gandalf's recommendation (holy parity; shadow-only DoT self-limiting → negligible band impact). If Matt's intent was "DoT trio + chill only," cut consecrate → emitting set becomes 4/8 (one-line amendment to § 1).
