# Finding — 2026-08-24 — Step-2 first landings (T-A tranche 1 + WW-AB clean-room)

**Reviewer:** jack-ryan
**Severity:** **PASS-WITH-FINDINGS** (2 WARN · 4 INFO · 1 ESCALATE · 0 BLOCK)
**Target:** `drax/v0.1-s2a-mint-tranche-1` (godot `c6eede0`) · `drax/v0.1-s2-whirlwind-cleanroom-1` (godot `1692d6e`)
**Developer:** drax (presentation seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity matters)
**Disciplines cited:** #1, #10, #19.1(b), #63, #70, #73, #75, #76

---

## Scope, and what this gate is NOT

This is **process and discipline conformance** on four minted T-A rows. It is not a visual-quality verdict — galadriel holds that gate and returned it (`galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`, three rows PASS-WITH-FINDINGS, L-19 PASS on all three, no HALT). Her gate scores the **frame**; this one scores the **record**. Neither subsumes the other and they did not overlap.

## Correction to the tasking premise (stated first, because it changes the ledger)

The dispatch that produced this review states *"four T-A rows are minted and none has a Gate-2 record in `agentic_orchestration/qa/`."* **The directory claim is true. The work claim is not.**

Gate-2 review of these landings **already happened** and is on the record — it is where **Disciplines #75 and #76** got their founding instances (engine `9307b46b`, the STEP-2/RULING-BATCH, 2026-08-24 21:00:30). Specifically: #75 instance 4 is galadriel's `telegraph_precedence_ok` finding, #75 instance 5 is a jack-ryan re-derivation error self-disclosed while auditing her gate, #76 instance 2 is the clean-room quarantine leak, #76 instance 3 is the C-8 census.

**What did not exist is a VERDICT on the tags** — a PASS/BLOCK disposition on `c6eede0` and `1692d6e`. Lessons were harvested into canon; the rows were never dispositioned. This file supplies that.

The mis-read is itself **#19.1(b)**: a directory listing is a *summary*; the ruling batch is the *record*. Recorded without prejudice — the conclusion ("jack-ryan owes a Gate-2 here") was correct, and acting on it was right.

---

## What I found

### ✅ VERIFIED — the math-before-code ordering receipt (Discipline #1, Principle 1)

Verified by re-deriving the timeline rather than accepting the claim. **Both rows hold.**

**Tranche 1:**

| Time (EDT) | Event | Instrument |
|---|---|---|
| 19:07:24 | mint note §§ 0–8 committed | collab `40d22e99`, 668 lines, single file |
| 19:15:24 | earliest effect script `s2a_aura.gd` | filesystem mtime |
| 19:27:48 → 19:42:32 | `s2a_census.gd`, `s2a_melee_strike.gd`, `s2a_ground_circle.gd` | mtimes, strictly monotone |
| 19:44:45 | `render.txt` — the render itself | mtime |
| 19:48:00 | mint commit | godot `c6eede0` |
| 19:49:14 | § 9 RESULTS appended | collab `c4b3f84b` |

**WW-AB:** note `78cdc3d6` @ 18:35:44 → mint `1692d6e` @ 18:52:40 → § 9 results `3acffa79` @ 18:52:52. Same shape, 17-minute lead.

**Stated limit, so this receipt is not over-read (#19.1(b) applied to my own verdict).** Commit ordering proves *commit* ordering. mtime is last-modification, not creation, so it cannot prove a file did not exist at 19:07 — it can only fail to support it. What the receipt does establish: every effect script was **added** at `c6eede0` with no prior commit anywhere in the tree; the mtimes are monotone in a plausible authoring order; and the **render** — which cannot run before the effect nodes exist — postdates the note by 37 minutes. No evidence contradicts the claim and three independent instruments support it. **The strongest available post-hoc receipt, and it verifies.** A session-level read/write audit log would be stronger; none exists.

**Positive note (INFO-1):** galadriel independently ran the same discipline on her own gate — skeleton committed `f9ed153a` @ 20:06:19, verdict `5a8b738f` @ 20:22:54. Three agents, one wave, unprompted. That is #1 becoming reflexive rather than instructed.

### ✅ VERIFIED — C-8 as a derived declaration (Discipline #76 clause 2, Principle 1)

Derived from `harness_logs/s2a_2026-08-24-final/render.txt`, not accepted from the completion record:

- **21** `C8_DECLARATION` lines. **21/21** report `non_authored_emitter_count: 0`. **21/21** report `non_authored_emitters_in_frame: []`. Zero non-empty. KR's handed number reproduces **exactly**.
- **21** `stage ready` lines, **21 distinct** arm keys — no arm double-counted, no arm missing a declaration.
- **C-3 albedo 0.085 on 21/21 arms**, derived from the same lines. Dispatch watch-item verifies.
- `s2a_census.gd` decides AUTHORED by **ancestry** (`r.is_ancestor_of(n)`), not by name, and its own docstring states why: *"Name matching is what breaks silently the day somebody renames a node."*
- The third emitter is real and is declared in-band: `neutralised_found_by: "s2a_census.gd, not by hand — it was NOT on my C-8 list"`, naming `KingRig.Greatsword` blade self-illumination — an emissive material on the very blade the weapon trail is generated from. Present on all 21 arms.

**The declaration is not laundered.** `non_authored_emitter_count: 0` is achieved *after* an intervention, and the same JSON carries `stripped` (2 nodes, identical across 21 arms), `neutralised` (1, identical across 21), and `strip_mechanism: "declarative export, not name-matching"`. The count and the interventions that produced it travel together. **This is #76 clause 2 executed correctly against a defective brief that I authored, and it holds.**

### ⚠ WARN-1 — the C-8 declaration is not uniquely keyed to its arm (Discipline #10)

The `C8_DECLARATION` payload carries `row / element / vector / valence / scale`. The run varies **two further axes it does not carry**: `fx` (`on` / `novfx`) and `rt` (readthrough: `off` / `on` / `trailoff` / `control` / `ctrloff`).

Derived collision set: **8 of 21 declarations collapse onto 2 keys** — `(melee, neutral, descend, hostile, nominal)` ×2 and `(aura, fire, descend, hostile, nominal)` ×6.

**Nothing is currently mis-attributed** — all 21 counts are zero, and each declaration sits immediately below its own `stage ready` line in the same log, so position resolves it. The defect is **latent, not active**, which is why this is WARN and not BLOCK.

Why it matters anyway: drax's own docstring establishes that *"the declaration is the control on [galadriel's] measurement, and a control produced from memory is not a control."* A control that cannot be uniquely bound to its treatment arm is under-specified — **#10, change one thing and measure one thing**, where `fx` and `rt` *are* the one thing changed. The moment the declaration is lifted out of log-position into a per-arm record — the natural next step, with 20 more T-A rows queued — position stops resolving it and a non-zero count could attach to the wrong arm.

**One-line fix:** add `fx` and `rt` to the `C8_DECLARATION` payload.

### ⚠ WARN-2 — `vfx_probe_delta.py` emits two comparisons at different coverage and names neither

Carried here from the X-6 ruling because it is a live artifact in this seam. `byte_identical` is computed by `sha_set()` over **every** frame; `samples` is computed over `idxs`, **at most 14 entries**; `frames_a` / `frames_b` describe **neither**. No field in the record names either comparison's `N`. **The artifact invites the exact inference that produced the L-31 correction.**

**Owner: drax. Obligation: emit a per-comparison coverage field.** Full rationale and the binding clause at `engineering-disciplines.md` § 75.5 clause 5.4.

### ✅ VERIFIED — the WW-AB clean-room declaration is COMPLETE; it is only PARTIALLY CHECKABLE, and that is the honest finding

Against my dispatch lane (*"whether the declaration is complete and checkable, not whether the effect is pretty"*):

**Complete — yes, and beyond the brief.** § 6.2 is an affirmative exhaustive read-list with line ranges, not a summary. § 6.3 carries the quarantine, the incidental encounters (`ls` output — names, not content), **five self-quarantined path classes not on the list** with the cost-asymmetry reasoning stated, and a volunteered disclosure of one read drax had intended not to make (`tail -c 2000 AGENT_STATE.md`), including what was in it, what was not, his assessment, and the explicit hand-off *"that assessment is mine, and it is gandalf's to overturn."* § 6.4 is the declaration proper. Node prefix `wwcr_` chosen for collision-isolation. § 8 pre-registers the falsifying pixel test **before** § 9 reports it.

**Checkable — only partly, and this bounds the experiment's conclusion.** A read-list is **self-reported**; no session-level read audit exists. The independently verifiable parts are (a) the `wwcr_` prefix isolation, verifiable from the commit's file list — **12/12 new files carry it or are `wwcr_`-scoped scenes**, confirmed; and (b) gandalf's DRIFT-CRITIC lineage audit of the *output*. **The clean-room control therefore rests on drax's attestation plus an output-side audit, not on an input-side proof.** That is not a defect in drax's execution — it is the ceiling of the method as designed, and WW-AB's verdict must be read at that confidence, not above it. **Recorded so the comparison is not over-read at seal (#70: declare the population you do NOT cover).**

**INFO-2 — the quarantine leak is already ruled.** drax's § 7.1 routes `scripts/run_ww*.sh` and `scenes/rigs/pilots/rig_poe1_cyclone.tscn` as a Gate-1 escape in a list I authored. That is **#76 founding instance 2**, already banked. **No further action; it is closed.** Noted here only so the WW-AB reader does not re-open it.

### ✅ RULED — galadriel vs drax, three contradictions

Two agents disagree on record about one artifact. Ruling: **galadriel is right in all three, and in none of them is drax wrong on his own evidence.** Every one resolves the same way — *which instrument has standing for this claim type* — and in all three the claim is a **rendered-appearance** claim, where render truth governs authoring truth.

| # | drax's claim | galadriel's refutation | Ruling |
|---|---|---|---|
| 1 | RT-2 minimum pair, hue-angle degrees; `fire\|earth` absent from the matrix | ΔE2000: true minimum is `fire\|earth` @ **7.38**, tighter than `neutral\|wind` @ 9.58 | **galadriel.** Not a factual contradiction — an **instrument** contradiction. She states her ΔE2000 "reproduces drax's degrees closely." Hue-angle is not a perceptual metric and ranked the pair out of view. She has already filed it as a standing instrument correction (her finding #1) + a WARN to rocket (#2). Correct disposition; I add nothing. |
| 2 | `payload_vector` a "qualified yes"; gate reported 10-vs-0 visible-payload frames | Byte-identical PNGs at **7 of 8** marks; `telegraph_precedence_ok` is scene-graph truth, not render truth | **galadriel — and this is a genuine instrument defect**, already canonized as **#75 instance 4**. A scene-graph reading cannot adjudicate a rendered-appearance claim. |
| 3 | Aura's 11.5 % lit-px element spread is "a threshold artifact" | The ratio does **not decay as the threshold rises**; a pure threshold artifact lives in the faint tail and would | **galadriel, with a named falsifier.** This one *is* a #19 defect on drax's side: the mint note (line 867) asserts the artifact explanation parenthetically, as settled, with **no cheapest-refuting-test named** — and the refuting test was cheap and available. A forensic hypothesis stamped as a conclusion. **INFO-3**, not WARN: it is confined to an aside, the substantive contract claim beside it (ring-radius spread 0.5 px) is independently measured and holds, and galadriel caught it one gate later — the sequence worked. |

**The generalizable ruling, and it is not about either agent.** In all three the mint note adjudicated a **rendered** claim on the **authoring-side** instrument, because that is the instrument the author has. The gate is where the render-side instrument lives. **The correction belongs to the sequence, not to drax** — and the sequence produced it, on schedule, which is the wave working. Banked as a new per-claim-type row in **#19.1**: *only pixels refute pixels.*

**INFO-4 — drax's numbers were refutable, which is why they were refuted.** All three claims were published in derived form with their instruments named. That is the precondition for galadriel's gate having anything to bite on. Worth stating because the raw count "three contradictions" reads as a quality problem and is closer to the opposite.

### ⚠ ESCALATE — the push discrepancy, RESOLVED on evidence; a governance question remains

**Both records are true and they do not conflict.** Derived:

- drax's WW-AB note § 7.6: *"My dispatching instruction for this wave is COMMIT, DO NOT PUSH. I followed the narrower, more recent instruction and pushed nothing."* — correct at the time, and he **flagged the charter L-2 conflict rather than resolving it unilaterally.** That is the right call and it is worth saying so.
- godot `AGENT_STATE.md` line 13, tranche-1 (a **later, separate** drax session): *"Tag `drax/v0.1-s2a-mint-tranche-1`. **Pushed** (charter L-2 push-as-you-go, **KR-confirmed for this wave**)."*
- `origin/main` = `c6eede0`. `1692d6e` is its **ancestor**. Annotated tag `drax/v0.1-s2-whirlwind-cleanroom-1` (object `9a980a4`, tagger date 18:52:40) is reachable from `c6eede0` and is on origin.

**Mechanism: the WW-AB commit and its annotated tag reached origin as ancestors of the tranche-1 push, which was separately KR-confirmed.** No unrecorded actor. No unilateral push. Nothing to invent.

**What remains open is governance, not forensics: drax raised an escalation and it was never answered — it was mooted.** He flagged a conflict between charter L-2 (*push as you go*) and his dispatch (*commit, do not push*), resolved conservatively, and routed it. The next session then received the opposite instruction and pushed, carrying his commit out with it. **The flag was overtaken by events and closed by nobody.** An escalation that dies by supersession rather than by ruling is the same failure shape as **#73** one level up — the state changed and the record did not follow.

**To Matt or KR:** state whether charter L-2 or the per-dispatch push clause governs when they conflict, and record it. Two drax sessions eight hours apart received opposite instructions on the same repo in the same wave.

### ℹ INFO-5 — #73 is being applied inconsistently *inside the wave that ruled it*

Derived from `agentic_orchestration/dispatches/`:

| Dispatch | `**Status:**` header | Ground truth |
|---|---|---|
| `2026-08-24-drax-s2a-mint-tranche-1.md` | **COMPLETE (2026-08-24)** ✅ | correct |
| `2026-08-24-drax-s2-whirlwind-cleanroom-wwab.md` | **PENDING** ❌ | completion record present (line 190); tag + commit on origin |
| `2026-08-24-galadriel-s2-minted-gate.md` | **PENDING — blocked until drax lands tranche-1** ❌ | tranche-1 landed; galadriel's verdict delivered at `5a8b738f` |
| `2026-08-24-jack-ryan-u4-router-x5-x6-gate2-standing.md` | **PENDING** ❌ | U-4 ratified `58d22432`; X-5 adopted as #19.1(b); **mine** |

**#73 was adopted 2026-08-24 at `ef7cfc82` — 18:39:47 — which is BEFORE all four of these landed.** Three of four headers are stale, and one of the three is my own. Recorded as INFO because the completion records themselves are sound and #73 already governs the remedy; the finding is that the rule's *adoption* did not propagate to the same-day corpus. **The two whose owner is me or drax are flipped in this session.** galadriel's is hers to flip.

---

## Rationale

- **Discipline #1 / Principle 1** — ordering receipt verified by re-derivation across three independent instruments, with the receipt's own limit stated rather than the claim over-read.
- **Discipline #76 clause 2 / Principle 1** — C-8 derived, delta reported in both directions (list said 2, world had 3), nil-delta on the count stated rather than omitted (#63).
- **Discipline #10** — WARN-1: a control that cannot be uniquely bound to its treatment arm is under-specified on the axes actually varied.
- **Discipline #75 § 75.5 / #70 / #19.1** — WARN-2 and the three-contradictions ruling: render-side claims need render-side instruments, and every comparison names its own coverage.
- **Discipline #70** — the clean-room declaration's checkability ceiling is declared so the WW-AB comparison is not read above its confidence.
- **Discipline #73 / #19.1(b)** — INFO-5 and the tasking-premise correction.
- **Principle 3 (cross-seam impact)** — **no MIGRATION.md owed.** Both landings are `reincarnated-godot/` presentation-internal: new `s2a_*` / `wwcr_*` scripts and scenes plus one modification to `scripts/king_rig.gd` (the C-8 blade neutralisation, gated behind the existing `stock_vfx_enabled` declarative export). No consumer contract changed; no engine, loadout, or demo surface touched. drax's own § 7.2 correctly routes the one *potential* cross-seam coupling (`R_ENGAGE` vs a future engine whirlwind hit radius) as a TODO with the engine's number declared to win, rather than asserting a value across the seam. Correct handling.

## Action

- [ ] **drax** — WARN-1: add `fx` and `rt` to the `C8_DECLARATION` payload before tranche 2. One line; do not re-render tranche 1 for it.
- [ ] **drax** — WARN-2: emit a per-comparison coverage field in `vfx_probe_delta.py` per § 75.5 clause 5.4.
- [x] **jack-ryan** — flip `**Status:**` on my own standing dispatch (#73). Done this session.
- [ ] **galadriel** — flip `**Status:**` on `2026-08-24-galadriel-s2-minted-gate.md` (#73). Hers, not mine to write.
- [ ] **knight-rider / Matt** — ESCALATE: rule the charter-L-2-vs-per-dispatch-push-clause precedence and record it. Two sessions, opposite instructions, same repo, same wave.
- [ ] **gandalf (DRIFT-CRITIC)** — carry the clean-room checkability ceiling into the WW-AB verdict: the input-side control is attestation-based, so your output-side lineage audit is the only independent leg. Read the comparison at that confidence.
- **No action required of drax on the three contradictions.** galadriel's findings #1/#2/#4 already route them; #75 instance 4 already canonizes the instrument defect. Do not re-open.

## Verdict

**`drax/v0.1-s2a-mint-tranche-1` — PASS-WITH-FINDINGS.** Ordering receipt verifies. C-8 derived, not enumerated, and it found a hazard the brief missed. C-3 at 0.085 on 21/21. Two WARNs, neither blocking, both one-line fixes forward.

**`drax/v0.1-s2-whirlwind-cleanroom-1` — PASS-WITH-FINDINGS.** Ordering receipt verifies. Clean-room declaration complete, self-widened, and volunteering its own escape. Its checkability ceiling is declared, not concealed. The push discrepancy resolves cleanly on evidence.

**Nothing here is a BLOCK, and nothing here goes to Matt as a design question.** The single ESCALATE is an operational precedence call, not architectural.

**Pattern-setting note (the dispatch's own quality criterion).** These are the first landings of a wave that binds 1,134 skills to 24 authored effects. The pattern they set is: **derive the declaration from the live artifact, publish claims in refutable form, flag your own escapes, and pre-register the falsifier before you report the result.** All four held on both rows. The defects found are in *record keying* and *instrument coverage* — not in the bindings. **Cheap to fix now, expensive at row 20**, which is exactly the leverage this gate exists to catch.

## References

- `/Users/admin/Games/reincarnated-godot/harness_logs/s2a_2026-08-24-final/render.txt` — the C-8 / albedo derivation source (21 `C8_DECLARATION` + 21 `stage ready`)
- `/Users/admin/Games/reincarnated-godot/scripts/s2a_census.gd` — ancestry-based census
- `/Users/admin/Games/reincarnated-godot/scripts/vfx_probe_delta.py` — WARN-2
- `/Users/admin/Games/reincarnated-godot/scripts/sa_gate.py` — `determinism_assert`, the § 75.5 exemplar
- `/Users/admin/Games/reincarnated-godot/AGENT_STATE.md` line 13 — the push record
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-24-s2a-mint-note.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-24-s2-whirlwind-cleanroom-mint-note.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1, #10, #19.1, #63, #70, #73, #75 (+ § 75.5), #76
