# Finding — 2026-08-25 — reproducibility-is-not-validity / sealed verdicts on backwards-body frames

**Reviewer:** jack-ryan
**Severity:** WARN (seal disposition is FAVOURABLE; one authority-surface defect cured in this landing)
**Target:** `qa/pending/2026-08-25-reproducibility-is-not-validity-sealed-verdicts-rest-on-backwards-body-frames.md` (all three sections)
**Developer:** knight-rider (filer), drax (surfacer), gandalf (prior ruling)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** `#63`, `#64`, `#75` cl. 2 / §75.5 cl. 3, `#79` cl. 2, `#80` cl. 1 / cl. 3(a) / cl. 5, and the mint of **`#81`** below.

---

## Summary of ruling

| # | Question | Ruling |
|---|---|---|
| **Q1** | Does the sealed verdict hold? | **HOLDS — and not by seal-inertia. CORROBORATED by the recapture.** drax's pre-registered falsifier passed by ~70×, and re-derivation shows the pre-fix corpus was biased **against** L-29(6). |
| **Q2** | What is the re-derivation boundary? | **Per-CLAIM, triggered by absolute-operand dependence** — not per-capture and not per-row. F-9's world-framed narrowing stands, amended with the shape/absolute limb. |
| **Q3** | Does "reproducibility is not validity" earn a number? | **YES — `#81`, minted in this landing.** NOT a fourth `#75` clause. And the clause the handoff says already carries it **is not in the corpus.** |
| **B** | Post-fix harness non-determinism | **DISPOSED, not deferred.** It is a floor measurement, not a defect report. Owner: **drax**, as a `#80` cl. 2(a) input. |

---

## What I found

All figures below I re-derived myself from the two `gate.json` pairs and the four capture directories. **Where I confirm knight-rider I say so; where I correct him I say which of his inferences I checked and which I did not** (`#80` cl. 3(a)).

### 1. Every headline figure in the filing REPRODUCES exactly

| leg | keys pre/post | numeric moves | bool | string | zeros→nonzero | false-`PASS` |
|---|---|--:|--:|--:|--:|--:|
| rows 1–2 | 15,357 / 15,358 | **468** | 0 | 0 | **5** | 4 pre / 4 post |
| rows 3–8 | 2,149 / 2,149 | **520** | 0 | **2** | 0 | 3 pre / 3 post |

Median/max also reproduce: rows 1–2 **3.30 % / 1,533 %**; rows 3–8 **0.92 % / 97.8 %**. The two prose-string moves are real, so **990** is the correct total and KR's own `#64` self-correction is right. His FAIL counts of **4** and **3** are right and his exact-string detector critique of himself is right — I get 4 and 3 by the `PASS == false` boolean referent.

### 2. ⚑ THE DECISIVE MEASUREMENT — drax's pre-registered falsifier PASSED, by ~70×

The handoff records that **gandalf already ruled Q1** — `L-29(6)` / `R-1.3` stand, on drax's trace that *the yaw defect is a pure sink: written, rendered, never read* — and that **drax pre-registered a falsifier for his own ruling while the recapture was still running**:

> *"deltas large on Mob0/1/2, near-zero on Mob3 — because Mob3 sits off the travel path. If Mob3 moves materially, my trace is wrong and the seal reverts to PROVISIONAL."*

**Nobody ran it.** The recapture returned, was analysed for 990 moved numbers, and **the one test that was staked on the answer was never executed.** I ran it over all per-body series scalars in `pair_1_dash_vs_blink`:

| body | scalars | moved | **max abs Δ** | **sum abs Δ** |
|---|--:|--:|--:|--:|
| Mob0 | 582 | 91 | 0.4032 | 4.037 |
| Mob1 | 582 | 126 | 0.3999 | 3.948 |
| Mob2 | 582 | 132 | 0.4059 | 4.629 |
| **Mob3** | 582 | 44 | ⚑ **0.00474** | ⚑ **0.0589** |

**85× on max, ~70× on sum, in the pre-registered direction.** This is `#75` cl. 2 satisfied in the strongest form available: a known-negative that *could* have refuted the trace and did not. **The seal is discharged on evidence, not on inertia.**

### 3. ⚑ AND R-1.3 RE-DERIVES IN THE SEALED LAW'S FAVOUR — the pre-fix corpus was biased AGAINST it

`R-1.3`'s operand is `shape.step_concentration`. Paired within-stage `dash_attack − blink` gap, all three common bodies:

| stage | leg | paired gaps | mean | **min** | all positive? |
|---|---|---|--:|--:|---|
| arena | PRE | +0.1461 / +0.3884 / +0.4040 | +0.3128 | +0.1461 | yes |
| arena | POST | +0.1480 / +0.4360 / +0.4459 | +0.3433 | +0.1480 | yes |
| cathedral | PRE | ⚑ **−0.1313** / +0.1305 / +0.0793 | +0.0262 | ⚑ **−0.1313** | ❌ **no** |
| cathedral | POST | +0.0761 / +0.2080 / +0.1959 | **+0.1600** | **+0.0761** | ✅ **yes** |

**The pre-fix cathedral Mob0 inversion is the exact "FALSE REFUTATION of L-29(6)" the HALT-RECORD § 96 named as *"present as an actual number rather than a projection."* It was an artefact of the defect. The fix removed it.**

So the disposition is stronger than "holds": **the sealed adjudication was made against data that pushed against it, and held anyway.** Post-fix it holds with a uniformly positive paired gap in both stages that it did not previously have. **A seal that survives the removal of a bias that was working against it is in better standing after re-derivation than before.**

### 4. ⚑ THE FRAMING KNIGHT-RIDER ASKED ME TO TEST DOES NOT EARN ITS KEEP — and he was right to flag it

> *"the verdict and the defect live on different axes of the same data"*

**Say it plainly, as asked: this is true of `pair_2` and FALSE of the item the file is about.**

- **True of `pair_2`.** `blink_traversal_px_byvalue_max` 9535 → 9406 (−1.35 %) while its own frame series moved by up to 97.8 %. Confirmed.
- ⚑ **False of `R-1.3`.** `step_concentration` moved on **every travel-path body**, by up to −8.7 % (blink@arena/Mob0 0.7104 → 0.6487), and the cathedral inversion resolved. **The statistic saw the defect perfectly well.** It is not on a different axis. **Nobody re-ran it for a day.**

And the load-bearing structural error underneath the framing:

⚑ **`pair_1_dash_vs_blink` CONTAINS NO VERDICT KEY AT ALL.** I enumerated it: zero `PASS_*`, zero `VERDICT`. It emits shape operands and nothing else. **The sealed verdict at issue is not one of the gate's verdicts** — R-1.3/L-29(6) were adjudicated by an analyst reading `step_concentration` in prose. So *"990 numbers moved, not one verdict did"* **compares a population that does not contain the sealed verdict.** The gate has no opinion about L-29(6) and never did. That is a `#80` cl. 1 defect (the region a quantity is taken over is a claim) committed in the evidence for a finding about gates that commit it.

### 5. Two inverted readings in the filing — both material, both correctable

**(a) ⚑ The "tail" reading is 180° inverted.** `frames[6]` / `frames[7]` are the **ONSET**, indices 6–7 of a 36-frame monotonically rising series. Full `blink@arena` `px_byvalue`:

```
pre  [0,0,0,0,0,0, 158, 503, 2430, 4536, ... 9535 (max@19) ... 7421,7087, 6714, 6816, 6808]
post [0,0,0,0,0,0,   5,  11, 1700, 3918, ... 9406 (max@19) ... 7370,7088, 6714, 6816, 6808]
```

⚑ **The actual tail — frames 33/34/35 — is byte-identical pre/post: `6714, 6816, 6808` on both legs.** There is no "lingering tail that the fix emptied," and the mechanism story built on it (*"body-anchored effects lingering in the wrong world region at late frames"*) **is not supported by this series.** I did **not** check any alternative mechanism; I am striking the inference, not replacing it.

**His structural point SURVIVES and must be restated:** a `max` over frames samples the **PLATEAU**; the defect's signature is in the **ONSET RAMP**. *"A max cannot see a ramp"* is the correct form. *"A max discards the tail"* is not, here.

**(b) ⚑ The five ⚑-flagged "measured zeros" are five ONE-PIXEL moves.** `0.0006067961165048543 = exactly 1/1648`; `0.0006765899864682003 = exactly 1/1478`. Five zeros became **one pixel each** — on the contaminated leg, and **inside F-9's own measured same-code flake floor of 1–18 px.** This is not `#63` arriving as data; it is the floor. **Recommend striking the ⚑.** `#63` is not thereby refuted — it is simply not evidenced by these five.

**(c) The percentage ranking buried the largest real move.** Ranked by %, the top of the rows 3–8 list is 1-px flicker (1533 % is `0.0019 → 0.031` on a ~1,650-px denominator). Ranked by **absolute** magnitude the largest mover is:

```
r8_hybrid_signature.stages.arena.per_mark.02-post-initiate.px_exact   92486 -> 106151   (+13,665 px, +14.8%)
```

**absent from the filing entirely.** `#80` cl. 1: a fraction is a claim about its denominator.

### 6. ⚑ And R-8 is the clean worked example that answers Q2

Every R-8 arena operand moved coherently by **+14–15 %** — `02-post-initiate` +14.8 %, `03-eruption-full` +12.3 %, `04/05/06-field` +15.3 %, `08-late` +15.1 % — and **both `PASS_step_at_initiation` and `PASS_flat_during_field` held.** Not by insensitivity: they are **shape claims** (a step exists; the field is flat), and `field_spread_pct` 0.00974 → 0.01143 stays negligible against a level that moved 2.94 → 3.38. **A uniform common-mode rescale preserves a step and preserves flatness by construction.**

**That is the differential-vs-absolute determination KR said could not be made from outside. It can. I made it.** R-8's *verdicts* are invariant; R-8's *operands* are not — anything downstream that quotes `field_pct_series ≈ 2.94 %` is quoting a number that is now 3.38 %.

### 7. The rows 1–2 contamination self-disclosure: CONFIRMED, BOUNDED, and the leg is USABLE

KR's disclosure is correct and I credit it — but I can now bound what he could not. The sole key delta is **`.c8_key_collisions.unevaluable_reason`** (post-only, value `null`). I re-ran the full comparison with it excluded: **468 / 0 / 0, unchanged.** It is additive-only and participates in no moved value. ⚑ **And it sits at top level under `c8_key_collisions`, outside `pair_1_dash_vs_blink` entirely — so it cannot reach the per-body series the Mob3 falsifier is computed over.** The falsifier result in § 2 is unaffected. **Rows 1–2 is usable; the second variable is bounded to one null scalar in a different subtree.**

### 8. The non-determinism leg: independently reproduced, and it is a FLOOR, not a defect

Verified by `cmp` over both pairs:

| pair | compared | differ | cathedral | arena |
|---|--:|--:|--:|--:|
| `s2c12v3` / `v3b` | 874 | 1 | **1** | **0** |
| `s2c38v3` / `v3b` | 2,106 | 5 | **5** | **0** |

**6 of 2,980, all cathedral, 0 of 1,490 arena.** KR's `p ≈ 0.03` is the correct **two-sided** figure (`2 × 0.5⁶ = 0.03125`; one-sided `0.0156`), and his "evidence, not proof, on six events" caveat is the right posture.

**Disposition:** these are same-code repeats, so per **F-9 / `#75`.5 cl. 3** a difference on a same-code repeat is **the flake floor being measured**, not a defect being reported. **What this establishes is a number the corpus did not have: the post-fix same-code floor is 6/2,980 = 0.20 %, cathedral-localised.** F-9 declined to conclude scope on 1/472 vs 0/2,106 (Fisher p ≈ 0.18); this is the second cathedral-only observation and it is **suggestive, not established.**

---

## Rationale

**Q1 — the seal holds because its falsifier was pre-registered and passed, not because it was sealed.** The distinction is the whole ruling. Seal-inertia would have reached the same answer here **for the wrong reason**, and § 3 proves it: the pre-fix corpus contained a class inversion pushing *against* L-29(6). gandalf flagged his own near-miss on exactly this ground (*"I reached a correct disposition through reasoning he had to replace"*). `#75` cl. 2.

**Q2 — the boundary is the CLAIM, not the capture.** F-9 narrowed PENDING-RECAPTURE to world-framed rows; drax corrected it further (*"authoring frame is a property of the ROW; exposure is a property of the CLAIM"*). § 6 supplies the operative limb: a claim reading a **shape/ratio** statistic is invariant under the common-mode rescale the defect produced; a claim reading an **absolute** operand is not. R-8 is the founding instance in both directions at once. A blanket re-derivation of every pre-fix capture is unwarranted and would cost the wave days for verdicts that are provably invariant.

**Q3 — `#75` is a container now, and the sentence has been cited without existing.** gandalf pre-committed the test himself: *"three rulings into `#75` in two days. If a fourth arrives, the right move is to ask whether `#75` has become a container rather than a rule."* **The fourth arrived.** And the decisive fact is auditable:

```
$ grep -c "Reproducibility is not validity" design/working-agreement/engineering-disciplines.md
0
```

`#75` carries **clauses 1–6** (plus §75.5's own 1–6). **There is no cl. 7.** The handoff § 7 states the clause *"carries drax's founding sentence into the corpus"* — **it does not.** That is `#79` cl. 2 (a citation must be executable), **second instance in 24 hours, on the same discipline**, and it is precisely the mint-lateness failure `#80`'s own closing note records me BLOCKing on my own seam. Per `#25` the handoff is what the next session inherits as substrate.

**Scope, correctly: `#75`'s subject is the INSTRUMENT** — does the probe bind the shipping artifact, has it proved sensitivity. **This claim's subject is the SEAL** — a governance object with a time dimension. Wrong container. It gets `#81`, and **I have landed it in the same commit as this finding** rather than assigning a number I did not mint.

**One correction to the mechanism paragraph of the filing (§ "The mechanism"):** it attributes the defect to `s2a_stage.gd:303` / `atan2(-x,-z)`. **F-9 already struck that** — `:303` is the *mob* yaw and was correct (`atan2` on a negated direction, not a negated formula; dot = +1.000 at six bearings). The live mechanism is the one the filing names second: **the caster's rest yaw was never set at all.** The struck half should not be carried forward.

---

## Action

- [x] **jack-ryan:** Q1 / Q2 / Q3 ruled by name. Non-determinism item disposed, not deferred.
- [x] **jack-ryan:** `#81` minted into `engineering-disciplines.md` in this landing (ADR-002 process-tier, **Matt-veto open**).
- [ ] **drax:** the answer you were owed — **your call was right and your falsifier passed by ~70×.** Mob3 max |Δ| 0.00474 against 0.40 on the travel-path bodies. Your trace stands on its own known-negative. **You surfaced this correctly and declined to rule it correctly.**
- [ ] **drax:** own the 6/2,980 cathedral-localised floor as a `#80` cl. 2(a) derived-bar input. **Do not file it as a defect** — it is the floor measurement P-BEAM's tolerance branch was waiting on.
- [ ] **knight-rider:** strike three items from the filing before it is inherited — the inverted "tail/lingering" mechanism (§ 5a), the ⚑ on the five one-pixel zeros (§ 5b), and the `s2a_stage.gd:303` attribution already struck by F-9. Re-rank the move table by **absolute** magnitude; `r8…02-post-initiate` +13,665 px is the largest real move in the corpus and does not appear.
- [ ] **gandalf:** `#75` cl. 7 as described in `skill_handoff_2026-08-25.md` § 7 **does not exist in the corpus.** Either land it or amend the handoff. Its substance is now `#81`; recommend the handoff point at `#81` rather than re-minting.
- [ ] **Matt (veto only, no decision needed):** `#81` mint. Q1–Q3 are within ADR-002 process-tier and are ruled, not escalated.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-08-25-reproducibility-is-not-validity-sealed-verdicts-rest-on-backwards-body-frames.md`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows12_2026-08-25{,-v3v3}/gate.json`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2c_rows38_2026-08-25{,-v3v3}/gate.json`
- `/Users/admin/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/s2c{12,38}v3{,b}/`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/step2-tranche-3a-HALT-RECORD-2026-08-25.md` (§ 96 — the cathedral inversion, named as a hazard, now measured as an artefact)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/skill_handoff_2026-08-25.md` §§ 7–8
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — `#75`, `#79` cl. 2, `#80`, and `#81` (minted here)
- engine `eaf93982` (F-9 / F-10), godot `2afde08` (drax, tag retraction), `612c1e3` / `1c4f90f` / `689116c` (the fix)
