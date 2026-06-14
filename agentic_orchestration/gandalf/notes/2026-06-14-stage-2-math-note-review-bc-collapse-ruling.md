# §7.5 review — gamora Stage-2 math note (AI bin-keying) + the Type-D bc-collapse adjudication

**Type:** §7.5 design review (gandalf seam) — Stage 2 of the three-stage BC-coordinate-identity cutover.
**Date:** 2026-06-14
**Author:** gandalf
**Verdict:** **PASS-WITH-AMENDMENTS** (one amendment, load-bearing — §A1 below; the bc-collapse ruling itself is ACCEPTED).
**Reviewed:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/bc-coordinate-cutover-stage-2-ai-bin-keying-2026-06-14.md` (commit `c29599b`).
**Against:** my §7 ruling (`2026-06-14-class-generator-bc-target-cutover-ruling.md`) — §7.5 (Component 5, discrimination-law-at-the-instrument), §7.6 (staging), §7.8 (one-variable / behavior-preserving), §7.9 (the two labels).
**Dispatch:** `agentic_orchestration/dispatches/2026-06-14-gamora-bc-coordinate-cutover-stage-2.md`.
**Empirical grounding (not ruled blind, §7.8):** verified at source 2026-06-14 — the lever (`ai_strategies.py:45/52/160/204/237/292/331`), the legacy orderings (`:61/62/96/99/100/101`), and the bc-collapse itself (ran `bc_target_from_generation_params` over water/earth/holy × damage × long × mana → byte-identical 8-tuple).

---

## 0. TL;DR

The note is faithful to §7.5. The smuggling trap is genuinely closed, the tri-state is sound design, and the outcome-equivalence criterion is the right bar. The bc-collapse of `water_mage`/`earth_caster`/`holy_caster` to one canonical damage-core ordering is **ACCEPTED behavior — the element-flavor deferral working as designed**, consistent with §7.8 (diversification + element-agnosticism are separate gated changes) and the Phase-5 element-skin deferral.

**ONE amendment gamora must fold before implementation:** the collapse is NOT pure element-flavor across all three. `earth_caster` legacy ordering leads with `control` (`control, area_damage, burst_damage, primary_attack`), but its Stage-1 coordinate is `ctrl_bin=damage-pure`. Control-vs-damage is a DISCRIMINATING axis (§2.3.1), not a flavor sub-ordering. So the earth member of the trio is a **mixed case**: its DoT/area/burst rotation flavor is correctly-deferred Type-D, but its control-LEAD is either (a) a Stage-1 source mis-bin (a real Type-M, earth-damage-caster should arguably be `mixed`/`control-pure`), or (b) a legacy-label OVER-claim (the `earth_caster` label asserted a control identity the kit's actual skills can't honor). gamora must classify which BEFORE the equivalence run, because the answer changes whether the canonical collapse ordering is allowed to drop control entirely. This is the §7.5 "the label was carrying information the coordinate does not" case bifurcating into its two legitimate sub-cases — and only ONE of them is a clean accept.

---

## 1. The bc-collapse ruling (the item gamora flagged for my adjudication, §2.6)

**RULING: collapsing the three to one canonical bin-derived damage-core ordering is the ACCEPTED behavior — for the FLAVOR component of the divergence. The element-flavor deferral is working as designed.**

The three legacy orderings diverge two ways, and the two ways are NOT the same kind of thing:

**(a) The damage-core flavor rotation — DoT-first (water) vs area-first (holy) — is PURE element-flavor. ACCEPTED.**
The coordinate is `(ranged-slow, large-AOE, solo, damage-pure, medium, flat, mitigator, overflow)` for all three. The DoT-lean of water and the area-lean of holy are exactly the "element-FLAVOR rotation identity" my §7.5 named: information the legacy label carried that the coordinate intentionally does not. The Stage-1 source (rocket §2.4) nudged element only into `var_bin`/`def_bin`/`geo_bin` — it did NOT mint a "rotation-flavor" axis, by design. This is the substrate-deferral (§7.2, §7.8): element is SKIN (Phase-5 cohesion-judge), the coordinate is pure mechanics, a "water" kit and a "holy" kit at the same coordinate ARE the same build. The legacy label was the only carrier of that flavor; binning it away is the deferral landing exactly where I ruled it should. **A single canonical damage-core ordering for this group is correct** — and the genre precedent is direct: a Frozen-Orb Sorc and a Fireball Sorc occupy the same build-region; the engine should pilot the build-region, and the element-skin distinction is presentation, not rotation. This is build-space-region identity (§3 of the ruling), not set-dungeon rigidity.

**(b) The earth control-LEAD is NOT flavor — it is a discriminating-axis claim. NOT auto-accepted — see §A1.**
`earth_caster` legacy = `[control, area_damage, burst_damage, primary_attack]`. Control-first. But `ctrl_bin=damage-pure`. The §2.3.1 map is unambiguous: `damage-pure → no control gate`. So the bin-derived ordering will NOT fire control first for the earth member — and that is a deviation on the CONTROL axis, which gamora's own taxonomy (§3.2) classifies as **Type-M (discriminating-axis mismatch — a behavior-preservation FAILURE), not Type-D.** gamora folded earth into the Type-D group implicitly. It is not cleanly Type-D. The control-lead must be resolved (§A1).

**Why this is the right call and not a different resolution.** The alternative — adding a rotation-flavor axis to the coordinate so the three stay distinct — is exactly the thing §7.8 forbids in this stage. It would (1) re-mint the element-as-mechanics coupling the lock retires, (2) bundle a content change (more axes) into the pipe change (this is the cert-wave one-variable error — a regression couldn't be attributed), and (3) pre-empt the Phase-5 cohesion-judge, which is the designated owner of element-skin re-cohesion. The flavor collapse is not a loss; it is the deferral. Phase-5 re-skins; until then, one build-region pilots one way. Hold the line.

---

## 2. The three confirmations gamora asked for

### 2.1 Is the smuggling-trap genuinely closed? — YES.

§2.1 names the forbidden path verbatim (`bins → label → ARCHETYPE_ROLE_PRIORITY[label]`) and §2.5 names the second smuggling vector (element/substrate keying — `CombatantState.substrate` is available at the keying site and the map MUST NOT read it). Both are the right traps. The map is `bc_target_role_priority(bc_target) -> list[str]`, a pure function of `ctrl_bin/eng_bin/tempo_bin/geo_bin/var_bin/def_bin` — never `archetype`, never element (§2.3, §6.3). I verified the lever is genuinely non-label: `get_priority_roles(archetype, preferred_behavior=...)` short-circuits and never reads `archetype` when `preferred_behavior` is set (`ai_strategies.py:230-240`). Promoting that monster-only override to the primary player mechanism is exactly §7.5. **Trap closed on both vectors (label AND substrate).**

One reinforcement for implementation (not a blocker): §2.2's rejection of the 6-value `_PREFERRED_BEHAVIOR_ROLES` enum is correct AND it independently strengthens the trap — routing the player space through the 6 monster buckets would have lost per-axis discrimination AND risked re-quantizing to a fixed enum. The direct bins→ordering map is both finer-grained and trap-cleaner. Endorsed.

### 2.2 Is the demote-to-fallback tri-state sound design (not hidden re-coupling)? — YES.

The §4 tri-state is correct and is NOT a hidden re-coupling:
- **PRIMARY** (`bc_target` present) → bin-keying; tables not consulted.
- **FALLBACK** (`bc_target` absent, known label) → `ARCHETYPE_ROLE_PRIORITY[archetype]` UNCHANGED.
- **LOUD-DEFAULT** (`bc_target` absent, unknown) → `log.warning` + registry default. No silent convergence (Disc #39 / P7).

This is sound for the reason the dispatch demanded it: physical kits ride the legacy path through Stage 3 (Matt directive — demote, do not retire). The fallback is not the disease re-entering because it fires ONLY when `bc_target` is genuinely absent — i.e. for kits that were never coordinate-composed. A `bc_target`-present kit NEVER touches the table. The tri-state keeps the two populations cleanly partitioned by the PRESENCE of the coordinate, not by any label inspection. The §4 Disc-#12 semantic-shift framing (the keying SOURCE shifts for present-kits; ZERO change for absent-kits) is exactly the honesty I want surfaced in the commit + decisions-log. **Sound. Not a re-coupling.** The one watch-item is purely operational and gamora already flagged it: the LOUD-DEFAULT branch must actually be loud — verify in implementation that the `bc_target`-absent-AND-unknown path hits the existing `:331`-style `log.warning`, not a silent registry fall-through.

### 2.3 Is outcome-equivalence the right behavior-preservation bar? — YES.

The §3.1 criterion (fight-engine outcome-equivalence: win-rate ±3pp, TTK ±5%, role-frequency L1 ≤ 0.10, bc-collapse groups evaluated as a GROUP against the envelope spanned by their three label orderings) is the correct bar, and it is correct SPECIFICALLY because of the collapse and the constant `tempo_bin`:

- **List-equality is the wrong bar by construction.** The collapse guarantees the bin ordering can't list-match all three members; demanding it would fail a thing that is working as designed. The instrument is the fight engine; the fight engine defines equivalence. A role-priority list is an INPUT to `choose_action`; "behavior" is the EMITTED fight. Two lists that produce statistically indistinguishable fights ARE piloting-equivalent. This is the same logic as the M1.3.5 discrimination-law work — measure the output, not the knob.
- **The envelope framing is the right handling for the collapse.** The three legacy orderings ALREADY produce three different fights; requiring the single bin ordering to match any ONE of them would privilege an arbitrary member. Requiring it to land WITHIN the envelope the three span is the principled bar — the collapsed group's outcome must be a member of the band its constituents already occupy. Correct.
- **The constant `tempo_bin=medium` across the mana set makes outcome-equivalence MORE necessary, not less.** Because tempo doesn't discriminate within the 16 (all mana → medium, verified at source `_ENERGY_TEMPO`), the rotation cadence axis carries zero information for this set — so list-level reasoning about cadence is meaningless and only the emitted-fight comparison can certify preservation. gamora correctly recorded this as a behavior-preservation LIMIT (§2.3.3, §2.5) rather than papering over it. **Outcome-equivalence is the right bar; the constant tempo is the reason it MUST be the bar.**

The proposed tolerances (±3pp / ±5% / L1 ≤ 0.10) are reasonable defaults; I do not adjudicate the numbers (jack-ryan Gate-2's seam — they must compose with the recompose band). I endorse the SHAPE.

---

## 3. Faithfulness to the rest of the §7 contract

- **§7.6 staging:** correct. Stage 2 adds `bc_target` to `CombatantState`, migrates the instrument, and FREES (does not remove) the internal legacy-format bridge. §6/§7.10 hold deletion for Stage 3. The note never reaches into generation (compose_kit/source/adapter untouched — confirmed against the dispatch out-of-scope list). Good.
- **§7.8 one-variable:** correct. The ONLY variable is the keying mechanism. Diversification explicitly out of scope (§0). The note resists the temptation to "fix" the collapse by tuning — it adjudicates it as deferral instead. This is the discipline holding.
- **§7.9 two labels:** correct. The note keys off the coordinate, never the start-of-pipe `archetype_tag`; the fallback table is the demoted legacy label, fired only on coordinate-absence; nothing is made player-facing. No conflation of the start-of-pipe disease with the end-of-pipe LLM `PlayerClass.name`.
- **§5 A3-separate ruling:** I endorse gamora keeping A3 (composition-fidelity, generation/shim seam) OFF the Stage-2 piloting run (AI-keying seam). They are orthogonal one-variable axes; bundling would break attribution. A3 closes on the generation side per §7.7. Shared harness, separate experiments — correct, and a KR coordination note, not a blocker.

---

## A1. THE AMENDMENT gamora must fold before implementation (load-bearing)

**Resolve the `earth_caster` control-lead BEFORE the equivalence run; do not ship it inside the Type-D group unexamined.**

The note's §2.6 enumerates the trio's orderings but its §3.2 taxonomy says control-axis deviations are Type-M (failures), not Type-D (accepted). `earth_caster` legacy LEADS WITH CONTROL yet its coordinate is `ctrl_bin=damage-pure`. That is a control-axis deviation by gamora's own definition. The bc-collapse ruling in §1(a) accepts the DoT/area FLAVOR collapse cleanly; it does NOT auto-accept dropping a control LEAD. gamora must classify which of two it is:

1. **Stage-1 source mis-bin (true Type-M, generation-side).** If `earth_caster`'s actual composed skills are control-meaningful (it really does want to fire CC first), then `bc_target_from_generation_params(role='damage', element='earth', ...)` emitting `ctrl_bin=damage-pure` is a Stage-1 bin error — earth-damage-caster should bin `mixed` (control in-rotation, not forced-first, per §2.3.1) or the role input should be control-orientation-aware. **This is NOT gamora's to fix** (generation seam, frozen Stage-1) — it is a finding gamora ROUTES to rocket + KR as a Stage-1 source-calibration item, and the earth member is held OUT of the clean-accept collapse until resolved.

2. **Legacy-label over-claim (clean Type-D, accept).** If `earth_caster`'s composed skills do NOT actually contain a control-dominant kit (the `control`-lead in the table was the LABEL asserting an identity the kit's skills never honored — the exact form-bias pathology: the flat label claiming more than the mechanics deliver), then dropping the control-lead is CORRECT and is the §7.5 "the label was carrying information the coordinate does not — and shouldn't have" case. Accept, and document that the legacy `earth_caster` table over-claimed control.

**How to decide:** the §3.1 outcome-equivalence run already produces the evidence — the role-frequency distribution for `earth_caster` under label-keyed piloting. If the label-keyed earth_caster fires control with meaningful frequency AND that control firing materially shapes its fights, it's case 1 (route to rocket). If control fires rarely / inconsequentially (the lead was aspirational), it's case 2 (accept). So the amendment is: **add `earth_caster` (and audit `shadow_controller`/`holy_controller` and any other `*_caster`/`*_controller` whose legacy table leads with control but whose Stage-1 coordinate bins `damage-pure`) as a NAMED pre-classification step in §3.2 — split the control-axis members out of the Type-D flavor group and adjudicate each as case-1-route-to-rocket or case-2-accept, using the role-frequency evidence, BEFORE the envelope test absorbs them.** The flavor collapse (DoT vs area) stays clean Type-D; the control-axis members get individually certified.

This is not a rejection of the bc-collapse ruling — it is tightening its boundary so a genuine discriminating-axis deviation cannot ride into production wearing a Type-D label. The whole cut exists to stop labels from carrying mechanical claims the coordinate doesn't; the review must not let one slip through in the equivalence harness.

---

## B. Disposition

- **VERDICT: PASS-WITH-AMENDMENTS.** The note is faithful to §7.5/§7.6/§7.8/§7.9. The smuggling trap is closed on both vectors (label + substrate); the tri-state is sound design, not a re-coupling; outcome-equivalence is the right bar and the constant `tempo_bin` is the reason it must be.
- **bc-collapse RULING: ACCEPTED as the element-flavor deferral working as designed** — for the damage-core FLAVOR divergence (DoT-first water vs area-first holy). A single canonical bin-derived damage-core ordering for the collapse group is correct; this is build-space-region identity, and Phase-5 owns the re-skin. Hold the line against re-minting a rotation-flavor axis (§7.8 violation).
- **AMENDMENT A1 (fold before implementation):** split control-axis members out of the Type-D group. `earth_caster` leads with control but bins `damage-pure` — that is a control-axis (discriminating) deviation, not a flavor sub-ordering. Classify each such member (audit `*_caster`/`*_controller` with control-lead + `damage-pure` coordinate) as either Stage-1 source mis-bin (route to rocket + KR; hold out of clean-accept) or legacy-label over-claim (accept + document). Use the §3.1 role-frequency evidence to decide. The envelope test must not absorb a control-axis deviation as flavor.
- **No other amendments.** §2.2 (direct map over 6-enum), §4 (tri-state), §5 (A3-separate) all endorsed as written.
- **Gate sequence preserved:** jack-ryan Gate-2 on the math note before any code; gamora folds A1; gandalf re-confirms A1 resolution at implementation review (the equivalence-run artifact §3.3 will carry the per-member control-axis classification).
- **Push gate (standing, Matt-gated):** this review note is push-ready pending Matt authorization; not pushed.

---

**Signed:** gandalf, 2026-06-14
**For:** the Stage-2 AI-bin-keying math note review — the simulator must MEASURE the kit it is given, not the label it once wore; the bc-collapse is the element-flavor deferral landing exactly where §7.5 ruled it should, and the one amendment guards the boundary between deferred flavor (accept) and a discriminating-axis claim the legacy label over-asserted (do not let it ride into the instrument as flavor).
