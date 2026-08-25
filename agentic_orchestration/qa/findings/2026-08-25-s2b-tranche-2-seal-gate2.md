# Finding — 2026-08-25 — S2B tranche-2 seal

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-CONDITIONS (one condition is tag-blocking)
**Target:** `drax/v0.1-s2b-receipts-a2-complete` · `drax/v0.1-s2b-rows-1-2` · rows 3–7 `d9e908c` · stage 4 `f29f12b`
**Developer:** drax (rows/receipts), galadriel (R-6 acceptance, occlusion audit), knight-rider (E-1)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 4 (decisions-log as truth), 5 (severity matters)
**Disciplines cited:** #80 (headline, cl. 1, cl. 2(a), cl. 4), #75 cl. 2, #78, #19.1(b), #76 cl. 1
**ADRs:** ADR-002 (tiered approval)

---

## 0. Verdict summary

| item | disposition |
|---|---|
| **My pre-declared Gate-2 BLOCK** (rows 3–7 minted without A-2's seven sensitivity receipts) | **DOES NOT FIRE — terms satisfied.** All seven verified at source, both legs where I demanded both legs. |
| **`melee_arc` sensitivity deferral** (KR item 1) | **Deferral of the WORK is LEGITIMATE. Banking of the CLAIM is not.** → **C1, tag-blocking.** |
| **Whirlwind occlusion gate** (KR item 2) | **NOT a tranche-2 seal blocker.** KR's handoff statement is inaccurate — and so is his proposed self-correction. → **C3.** |
| **ww `post` mark** (KR item 3) | **Correctly handled. No action.** drax's decline ratified for the second time. |
| **E-1 GLF "no verdict flips" claim** | **CHECKS OUT.** No bar exists to flip. → forward hazard only, **C2**. |

**Seal may proceed on C1.**

---

## 1. What I found — the pre-declared BLOCK does not fire

I did not take the completion record's word for this. I read the receipt artifacts at
`reincarnated-godot/harness_logs/s2b_receipts_2026-08-24/`.

`sensitivity.json` carries `proofs` with exactly seven keys, matching my A-2 table 1:1 —
`banked_at_E1: [ii_structured_content, i_stage, iii_ciede2000]`,
`banked_now: [iv_c2_yaw, v_cross_row_separation, fix_a_c8_declaration_key, fix_b_probe_delta_coverage]`.
`ALL_PASS: true`.

Where my clause demanded **both legs**, both legs are present and non-trivial:

- **(iii) CIEDE2000** — known-identical (`gtc fire descend | gtc fire erupt`, byte-identical, dE2000 **0.0**) *and* known-different (`melee fire | water`, dE2000 **18.70**). My clause said "both legs, or the metric change is unproven." Both are there, and the identical leg is a **pipeline-produced** negative, not a subtraction artifact — stronger than what I asked for.
- **(ii) structured content** — reproduces **0.3038** against galadriel's **0.304** target, operator named in full (3×3 Sobel, unnormalised, ITU-R 601-2 luma, `|∇| > 10`). The divisor sweep is the part that earns it: `/4` returns **0.2699**, which is plausible and matches *neither* published operator — and it is what was shipped before the proof existed.
- **(i) cathedral stage** — six arms, ON-vs-OFF max delta **0.6027 pp** against stage ratios of **77–149×**. Both my conditions (stage dominates; differs from bare) discharged.
- **(iv) yaw** — known-negatives at 10°/45° **FAIL**, correct arms 0.034–0.969° against a 2.907° bar, and it publishes its own **10° detection floor** rather than claiming unconditional sensitivity.

**Contamination check I ran unprompted:** receipt (i)'s known-negative is an *effect-off* measurement, and the E-1 gate was just found to have been scoring a superseded `_fxoff_` control. I checked whether receipt (i) inherited that defect. It did not — `s2b_e1_gate.py:284/290` scopes the `_fxoff`/`_fxctl` suffix with `if row == "ww"`, and receipt (i)'s arms are `melee`/`gtc`/`aura` only. **Receipt (i) is clean, and the reason is structural rather than lucky.**

**Form note (INFO, no action):** my clause said "in `gate.json`"; the receipts live in a sibling `*.json` set under the same tagged commit. Substance met; I am not enforcing the container.

---

## 2. ⚑ C1 — TAG-BLOCKING — `melee_arc`'s caster-retention criterion cannot go red, and the summary banks it as met

**This is the answer to KR's item 1, and it is not the answer he framed.**

`harness_logs/s2b_rows37_2026-08-24/gate.json`, `melee_arc@arena` and `melee_arc@cathedral`:

```
"A5_CASTER_RETENTION": {
  "structured_px_in_region": 1143,      "structured_px_retained": 1143,
  "retention_frac": 1.0,                 "caster_region_px": 1610,
  "authored_px_inside_caster_region": 0,
  "authored_frac_of_caster_region": 0.0,
  "why_by_construction_too": "the crescent's INNER radius is 2.34-2.62 m, so it
     cannot overlap the caster's footprint. The pixels are the check on the
     construction, not a substitute for it."
}
```

The authored mask and the caster region are **disjoint by construction**. `retention_frac` is therefore arithmetically forced to ≈1.0 **independent of the artifact**. It reads 1.0000 / 0.9993 not because the crescent preserves caster legibility but because the crescent never reaches the caster region at all.

**That is #80's founding shape, on a tranche-2 row, inside the tag being sealed** — and #80's own text is *"a gate that cannot fail is emitting a claim about itself."* **cl. 2(a) is directly on point: a gate that cannot compute its own floor returns UNEVALUABLE, not PASS.** This criterion cannot distinguish *"not occluded"* from *"no overlap was possible,"* which is the same inability the 99.6 %-sky denominator had.

**Three things I am careful to say, because the fairness of this finding depends on them:**

1. **drax disclosed it.** `authored_px_inside_caster_region: 0` and `why_by_construction_too` are his own fields, in his own words. Nothing was hidden and nothing needs excavating — I found this by reading what he published. **Self-disclosure converts a BLOCK into a WARN and never converts a defect into a non-defect** (this dispatch, line 414, my own composition rule). It is why C1 is a record correction and not a re-mint.
2. **The underlying design claim is sound, and on better evidence than the pixels.** Inner radius 2.34–2.62 m against a 22.6 px caster footprint is a *geometric* guarantee, which is stronger than a retention fraction. The row is not in doubt. **The artifact is fine; the record over-claims.**
3. **cl. 1 is NOT breached and my own cl. 4 ratification survives.** I checked, because cl. 4 asserts `s2b_rows12`/`rows37` already comply. `region_basis` here is *"the rig's foot and head unprojected through the CAPTURE camera by the engine"* — engine geometry, not a frame-relative box — and the denominator (`caster_region_px: 1610`) **is** printed. **The region derivation is exemplary. The defect is the criterion's inertness on this population, which is a different clause.** My cl. 4 stands.

**⚑ The sharpest evidence that this is a real defect and not my pedantry: the same agent, in the same run, handled the identical question correctly in the opposite direction.** On ww's `post` mark drax **declined to turn an N/A into a PASS** because it moved favourably and was not pre-registered. On `melee_arc` caster-retention a structurally-N/A criterion **is** reported as one of *"all three A-5 re-anchored criteria met."* **Same question, same run, opposite handling.** The receipt is honest; the summary line elevates a consistency check into an acceptance test.

**This is the fifth summary-count defect of this run** (L-47 INFO-8 logged the fourth and accepted *"derived-summary discipline"* as a run-close governance candidate, R-L47-2). It is the same class: **the measured record is right and the sentence written on top of it is not.**

### C1 — required before the tranche-2 tag

- [ ] **drax:** amend the row-5 claim. Caster-legibility is satisfied **BY CONSTRUCTION** (inner radius 2.34–2.62 m vs caster footprint); its pixel leg returns **UNEVALUABLE on this population** per #80 cl. 2(a), `authored ∩ caster_region = ∅`. **Row 5 seals on two measured A-5 criteria plus one construction argument — not three measured criteria.** Background retention (0.5618 / 0.6982) and C5 are unaffected and genuinely measured; background retention demonstrates real dynamic range **across stages**, which is what makes it non-degenerate.
- [ ] **knight-rider:** carry the same correction into any Matt-facing summary that repeats "all three met."

**No re-mint. No re-render. No re-capture. This is a sentence.**

---

## 3. The deferral itself — LEGITIMATE, with its scope stated

KR asked to be corrected rather than ratified by silence. **The deferral is legitimate and I am ratifying it explicitly, on stated grounds rather than by omission.**

- **A-2's seven receipts were tranche-wide INSTRUMENT proofs.** The `melee_arc` row-level sensitivity proof was **never one of the seven**. Deferring it does not touch my pre-declared BLOCK, whose terms are independently satisfied (§ 1).
- **The rule is: defer the WORK, do not bank the CLAIM.** Post-seal scheduling of a proof that costs arms and no re-render is ordinary sequencing. Sealing a *claim* that the deferred proof exists to underwrite is not. C1 separates them.
- **Row 7's 5°/7° fill-in is already handled honestly.** Row 7 reports **1.185° / 0.935°** against the 2.907° bar while *"carrying its declared 10° floor, not reading as unconditional."* The gap between bar and demonstrated detection floor is **published rather than papered over**. That is #80-compliant as it stands; the fill-in refines a known bound, it does not repair a false claim. **No condition.**
- **KR's "worst-replicating row" point cuts the other way from how he framed it.** `melee_arc` replicating at 76.4 % is a fact about **A-6's retired null leg**, not about row 5's acceptance criteria. A-6 is retired on three independent grounds; its non-replication is the *reason* for the retirement, not a residual doubt about the row. **Row 5's own criteria are separately evidenced.**

---

## 4. ⚑ KR item 2 — the whirlwind premise. Plain answer: NO, the statement is not accurate

`skill_handoff_2026-08-25.md` § 3 states: *"The one genuine open blocker: the whirlwind occlusion gate."*

**That is inaccurate, and KR's proposed correction — "but `whirlwind` is a TRANCHE-1 row" — is also inaccurate.** Whirlwind is **neither**:

- **Tranche 1** = `melee_strike`, `ground_targeted_circle`, `aura` — three rows, § 3.1.1 / 3.1.2 / 3.1.8 (`2026-08-24-drax-s2a-mint-tranche-1.md:21–27`). That dispatch's own out-of-scope block, line 172: ***"`whirlwind` — separate dispatch, clean-room protocol, RT-4-gated. Do not touch it here."***
- **Tranche 2** = `self_buff`, `totem`, `circle`, `single_target`, `melee_arc`, `multi_projectile`, `line`. Whirlwind is absent.
- **KR recorded the correct fact himself**, in this very dispatch at line 83, quoting galadriel: *"her tranche-1 gate covers `melee`/`gtc`/`aura` only, and `whirlwind` is in the **not-started set**."* He logged that as *"my fourth premise error of this run."*

**So the handoff statement is the same premise error recurring a fifth time, in the document Matt reads, after its own correction was written 1,250 lines earlier in the file KR was summarising.**

**Two further facts that settle it independently of row rosters:**

1. **The redispatch's own § Out of scope, line 128, excludes *"re-opening the WW-AB seal or the enemy-leg leg of § 9.2."*** The occlusion gate's moving verdict **is** the enemy leg. An item this dispatch explicitly placed out of scope cannot be that dispatch's blocking item.
2. **`wwcr_occlusion_gate.py` is the whirlwind clean-room gate, not `s2b_e1_gate.py`.** Whirlwind does appear inside tranche-2 work as an **E-1 stage-metrics arm** (`row == "ww"`) — so it is not wholly foreign to the dispatch, and I want that stated rather than glossed. But the E-1 ww arm and the clean-room occlusion gate are different instruments, and the occlusion gate scores nothing tranche 2 seals.

**Corrected characterisation, offered so the fix is one edit:** the occlusion-gate item is a **genuine open item on the WW-AB / whirlwind clean-room workstream**, carrying a real newly-known finding (**~27 % of true enemy-silhouette pixels change at `05-sustain` on both corpora** — the exact failure that row exists to correct, invisible to the gate as scored). **It is not a tranche-2 seal blocker, and tranche 2 does not wait on it.**

### C3 — record correction, not tag-blocking

- [ ] **knight-rider:** correct `skill_handoff_2026-08-25.md` § 3. Whirlwind is neither tranche-1 nor tranche-2; it is the separate clean-room dispatch, in the not-started set. The occlusion gate is a WW-AB open item.
- [ ] **jack-ryan (me), carried forward:** the occlusion-gate bar re-derivation is routed to me and I am **not** discharging it in this finding. **It is pre-registration work and #80 cl. 2(a) already names its safe construction** (`bar := floor_mean + k·floor_sd` on the region actually scored, `k` fixed a priori, which re-scales automatically when the denominator is repaired). **A-11.4 binds the sequencing: the bar is derived before the repaired number is looked at again.** Separate work item, WW-AB workstream.

---

## 5. KR item 3 — ww `post` mark. Correctly handled, no action

drax declined to switch `post` on because turning an N/A into a PASS **moves favourably and was not pre-registered**, despite the stated 3,973 px scuff reason not reproducing (diffs to exactly 0 against the rendered control). KR ratified. **I concur, and it is the second ratification.**

This is **#80 operating as intended and paying for itself**: a verdict improvement discovered mid-run is exactly what the discipline exists to make you pay for in advance. **It is un-registered, not failing.** It gets its own pre-registration or it stays N/A. **No condition.**

**And it is the correct-direction control against which C1's over-claim is legible** — see § 2, point 3.

---

## 6. E-1 / GLF — KR's claim checks out, with a forward hazard

**KR asked me to check "no verdict flips — GLF has no threshold." It holds.** Verified two ways:

1. `2026-08-24-drax-s2b-mint-tranche-2.md:521` states it in the corrected table itself.
2. **Independently:** the redispatch § Out of scope, line 126 — ***"Setting GLF-enrichment bars. galadriel's, after the sweep. Do not propose numbers."*** The bars **do not yet exist**. A quantity with no threshold cannot carry a verdict, so no verdict can flip. **The claim is structurally true, not merely observed to be true.**

**The forward hazard, which the claim's correctness does not dispose of:** `authored_px` was inflated **6,452 → 1,869** and **5,773 → 1,842** — a **~3.45×** correction. The GLF table's entire purpose is to be the **input to galadriel's future bar-setting**. So the correction's value is **wholly forward**: it flips nothing today and determines everything about the bars set tomorrow. **A stale copy reaching her would set enrichment bars ~3.45× off with no verdict ever appearing to flip** — which is precisely the failure mode that "no threshold" makes invisible.

**Credit where it is due, and it is the substantive part:** the E-1 work **retired an open defect rather than adding one** (`00-pre` arena 83 → 0, cathedral 265 → 0, `PASS_exactly_zero` false → true), and the `superseded_excluded` publication with all twenty filenames is **better than the MOVE that was ordered** — an exclusion that publishes its own membership list cannot drift from the directory it describes.

### C2 — routing, not tag-blocking

- [ ] **knight-rider:** carry the **corrected** E-0 GLF table to galadriel explicitly, flagged as superseding, **before** she runs the enrichment sweep or proposes bars. Do not rely on her re-reading the dispatch.

---

## 7. Approval authority (ADR-002)

Within my tier and **APPROVED directly**: the receipt-completeness ruling (§ 1), the deferral ruling (§ 3), the `post`-mark concurrence (§ 5), and conditions C1–C3, all of which are documentation/record corrections.

**ESCALATE to Matt — one item only:** `reincarnated-godot` push covering `f29f12b`, `7dc58d3`, `0c38b79`, `0d26021`. Outside the standing Step-2 push pattern **by that pattern's own scope boundary** (CLAUDE.md: the pattern covers `reincarnated-collaboration` and `reincarnated-engine` only). **Fresh ask owed. Unchanged by this finding.**

**Not escalated:** nothing here conflicts with a locked decisions-log entry, and no cross-seam schema changes.

---

## 8. Inferences I did NOT check — stated per #80 cl. 3(a)

*(cl. 3(a) requires a review that re-derives numbers to state which inferences it did and did not check. Silence is read downstream as ratification.)*

**Checked at source:** all seven A-2 receipts and both legs of each · the `_fxoff_`/`_fxctl_` row-scoping in `s2b_e1_gate.py` · `melee_arc` gate records at both stages · tranche-1 and tranche-2 row rosters · the GLF no-threshold claim (two independent routes) · #80's own cl. 4 ratification against `rows37`.

**NOT checked, and the seal does not rest on my having checked them:**

- **The other four tranche-2 rows' criteria were not swept for the C1 defect class.** I found it on `melee_arc` because KR pointed me at that row. **A gate whose region is disjoint from its artifact prints the same green everywhere** — I have no basis to say rows 3/4/6/7 are clean of it, only that I did not look. **Recommend the same `authored ∩ region` emptiness check across all rows as a mechanical sweep** (#76 — derive, don't enumerate; this is exactly the "derive-don't-hand-list" standing instruction from L-47 WARN-5).
- **A-6's three retirement grounds** are carried from my own prior instance-4 close at `aa332c6a`; not re-derived here.
- **galadriel's R-6 acceptance condition** (0/0/0, determinism 60/60 then 20/20) is taken from her acceptance and drax's receipt; I did not re-run it.
- **The 7.41× `line`/`single_target` boundary and the RT-2 `fire|earth` result** are reported, not verified by me.
- **`single_target`'s 709 px against a 535 px floor (1.32×)** — drax flagged it himself as the thinnest coverage in T-A and the Javelin low-contrast risk. **I did not evaluate whether 1.32× is adequate margin. That is galadriel's axis, and it is an open question, not a finding.**

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-24-drax-s2b-rows-redispatch.md` (§ 4, § 5 L107, L128, L83, § A-11.6)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-24-drax-s2b-mint-tranche-2.md` (A-2 L391–403, A-5 L418, pre-declared BLOCK L451–453, GLF L521)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-24-drax-s2a-mint-tranche-1.md` (L21–27 roster, L172 whirlwind scope)
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2b_receipts_2026-08-24/{sensitivity,xrow,yaw,c8key,probedelta_fixb}.json`
- `/Users/admin/Games/reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/gate.json`
- `/Users/admin/Games/reincarnated-godot/scripts/s2b_e1_gate.py:284,290`
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#80, minted `1cc2c5f8`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/knight-rider/rulings/2026-08-25-e1-gate-scores-the-control-mode-its-own-harness-was-fixed-to-stop-using.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/skill_handoff_2026-08-25.md` § 3 (subject of C3)
