# Cert-wave 2D — W-D close + D1–D6 wave-decision record

**Author:** knight-rider, 2026-06-13. Matt-ratified dispositions on the D1–D6 queue.
**Phase:** W-D (six-axis MEASURE) — gamora delivered (engine `5ec33bb`, tag `gamora/v-wd-six-axis-measure-1`, not pushed).
**Critique pair:** jack-ryan Gate-2 = WARN (doc-only); gandalf design = ENDORSE (b). They converge.
**Standing pattern note:** orchestrator session is now **event-driven** (no self-scheduled heartbeat) per Matt 2026-06-13.

---

## D1 — cond.4 = PASS (gate-read), but it does NOT close §6.4

**RATIFIED PASS.** jack-ryan's verbatim read of oracle §6.2 cond.4 (line 263: *every axis assigned-from-spatial + wired-not-default (Bucket-A) + `CommitGradeVerdict` mint*) is correct precedence; gamora meets it. The Gate-2 WARN is **documentation-only** and clears WARN→PASS once gamora writes two annotation lines (math-note "§8 was stricter than the oracle" reconciliation line; JSON `measure_cond4_pass:true` annotated beside `prereg_pass:false`/`ablation_pass:false`) — both within jack-ryan's ADR-002 approve authority.

**HARD CONSTRAINT (load-bearing — KR enforces downstream):** cond.4 PASS **does NOT** establish §6.4's *"the archive measures the current kit = measured fact."* **wired-not-default ≠ discriminates.** Per oracle §6.4: *only when RESOLVE AND MEASURE (cond.4 W-D + cond.5 W-F) pass* does "measures the current kit" stop being a claim — and only then does the 1D engine delete. **§6.4 stays OPEN; it closes at W-F.** No downstream artifact or agent may read "8 axes wired" as "the archive measures the kit."

**[KR] action — TRIGGERED:** gamora to surface her per-axis discrimination decomposition from the W-D 4-part pre-reg (the PARTIAL/FAIL breakdown — which axes discriminate NOW, which don't, against the pre-registered bins). Routed to gandalf on completion.

**[gandalf] owed (routed):** (i) interpret gamora's decomposition against the known-deferred list — Axis-2A → D4 sustained-wave fixture (oracle line ~189/192); mobility-via-gather → default-off per the §5.2 ablation-negative. Every fail mapping to a deferred axis = clean; any fail on an axis that should discriminate NOW = a **live obligation**, surfaced as such (not a doc-line). (ii) the oracle discrimination fix — cond.4 gets a discrimination sub-clause (or §6.4 gets gated on the clean decomposition) so wired-not-default can't masquerade as measures-the-kit when §6.4 closes at W-F (the 1D-delete gate). Folds with §5.2.

## D2 — disposition (b) RATIFIED

Per-seed K4≥K2 margin **accepted as closing-time noise**; the K4≥K2 mechanism obligation is **discharged-NEGATIVE**. The Matt-sharpened with/without ablation returned a clean negative WITH a mechanical truth: **gather INVERTS the margin** (WITHOUT 6/9 +3.99 → WITH 1/9 −3.44) — it lifts the stationary nova K2 more than mobile K4, because **gather is a substitute for mobility, not where a mobile kit's identity lives.** Speed-gated gather **rejected as rule-shopping** (oracle §5.1). This reopens the deferral Matt personally ratified — done on the ablation evidence (recognition→validate→commit). Direction half (K4 IN 9/9 + mean ordering) stays CERTIFIED unchanged.

## D3 — gandalf commits the §5.2 amendment

**[gandalf] owed (routed, his seam, on Matt's nod).** Verify the drafted text against the agreed basis (concurrent-instance discipline) and commit: the ablation RESULT (gather-inverts), the (b)-close (mechanism discharged-NEGATIVE), the mobility-home reframe (mobile-kit identity = kite-survival under sustained pressure → existing W-F K4 SURV-via-kite ⚠C4, condition-5), the farming-mobility coverage-edge + margin-vs-parity fork (logged as an OPEN design-call, **not** a build), and the D1 cond.4/§6.4 discrimination fix. **KR does NOT write the oracle.**

## D4 — sequence the spatial-proxy-mechanic PORT (Axis-2A + §4.D)

**[KR] SEQUENCED** as a genuine new workstream (movement-AI-scale rework). It is the routed home for Axis-2A's real discrimination — the §4.D sustained-wave fixture (oracle line ~189: hard W-D prerequisite, fixture lands *before* Axis-2A wiring or wiring certifies against noise). Closes part of D1's known-deferred accounting once it lands.

**ARITY HELD for gandalf's Bucket-B ruling (D4 gate):** does proxy-density become a real **9th axis + a 7th §5 reference kit**? Per oracle §6.3, that is gandalf's Bucket-B design ruling, which he owes. **Workstream sequenced; arity question NOT presumed (not 8, not 9) — gated on the ruling.** Full dispatch authoring HELD until Bucket-B resolves the arity.

## D5 — rocket reference-kit follow-on — ENDORSED

**[KR] SEQUENCED.** rocket's resource/CC-differentiated reference kit, **arity=8 HELD** (no 7th kit until/unless Bucket-B promotes proxy-density). This is also the **instrument for testing Axis-5 resource-economy + Control discrimination** — flagged for the D1 decompose (the current hand-built set is uniform on Resource/Control, so those axes are wired-but-not-exercised; this kit exercises them). Dispatch authored: `dispatches/2026-06-13-rocket-reference-kit-coverage.md`.

## D6 — pytest-collection error — OWNER ASSIGNED: rocket

**[KR] ROUTED to rocket.** Root cause diagnosed: `src/reincarnated/foundation/grouping_vocabulary_loader.py:174` raises RuntimeError — cannot locate `canonical/story/grouping-layer-vocabulary.md`. The doc was **moved to `canonical/story/historical/grouping-layer-vocabulary.md` in commit `93b8427`** (docs structural-restructure), but the foundation loader's path candidates were not updated → **9 test modules fail at collection** (`test_b6_generator_wired`, `test_cosmological_vocabulary`, `test_cp8_gear_naming`, `test_gear_integration`, `test_integration`, `test_naming`, `test_no_canonical_four_in_llm_prompts`, `test_role_orientation`, `test_spirit_guide_orchestrator_wiring`). `foundation/` is rocket's seam → rocket fixes the loader path (or restores the doc to the expected path, or sets the fallback to `historical/`). Dispatch authored: `dispatches/2026-06-13-rocket-grouping-vocab-loader-fix.md`. Not gandalf's seam, not gamora's.

---

## W-D-export + onward

- **[KR]** W-D-export dispatch authored: `dispatches/2026-06-13-star-lord-wd-export.md` (star-lord, gated on gamora's MIGRATION v1.31 — won't fire before it). **CAVEAT folded:** the bins are **wired-not-yet-fully-discriminating** pending the D1 decompose → the export is **NOT stamped as "measures the kit."** Gate-1 (jack-ryan) in flight.
- **[KR]** W-E (throughput) queued. cond. 5 (defensive-bridge boss re-validation) stays at **W-F**.

## Ownership split (summary)

| Item | Owner | State |
|---|---|---|
| D1 cond.4=PASS ratify + WARN-clear | KR + jack-ryan | RATIFIED; WARN clears on gamora's 2 doc lines |
| D1 decompose surfacing | gamora (KR-triggered) | FIRED → hand to gandalf |
| D1 decompose interpretation + oracle discrimination fix | gandalf | ROUTED (needs decompose) |
| D2 disposition (b) | KR (record) | RATIFIED |
| D3 §5.2 amendment commit | gandalf | ROUTED (on nod) |
| D4 proxy-port workstream | KR (sequence) | SEQUENCED; arity held |
| D4 Bucket-B arity ruling | gandalf | OWED |
| D5 reference-kit follow-on | rocket (KR-dispatched) | SEQUENCED, arity=8 |
| D6 grouping-vocab loader fix | rocket (KR-dispatched) | ROUTED w/ diagnosis |
| W-D-export | star-lord (KR-dispatched) | AUTHORED, gated on MIGRATION v1.31 + D1 |
| Oracle amendments (§5.2 + cond.4/§6.4) + Bucket-B ruling | gandalf | his canon-write side |

**Push:** all 2026-06-13 commits remain unpushed; Matt gates the keystone-close push.
