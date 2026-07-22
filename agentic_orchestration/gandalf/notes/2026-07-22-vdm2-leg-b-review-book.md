# VDM-2 → Edition-next Lap — Leg-B Review Book

**For:** Matt. **From:** gandalf (`RUN-CONDUCTOR`).
**What this is:** the Matt-interface deliverable at Leg B's close — the R-8(b) precedent (charter §6 / V-3: "review book per leg + red-flag pings only"). This is your account of what Leg B did and the one strategic fork it surfaces for your ruling. Nothing here blocks; Leg B has already landed on its pre-registered honorable fallback. **This book also closes the RUN** (both legs complete; the Tier-3 encounter-geometry run is a separate sequel).

**Spine:** `2026-07-22-vdm2-edition-next-lap-run-state.md` (scoreboard + ledger V-1..V-26 + review-book log RB-1..RB-9). **Prereg (BINDING):** `gandalf/design-inputs/2026-07-22-leg-b-edition-next-preregistration.md`. **elrond's execution:** `research/curated/atlas/2026-07-22-legb-gate-report.md` + `research/scripts/atlas_legb_refit_2026_07_22.py` (commit `78b7dc6b`). **Leg-A book (predecessor):** `2026-07-22-vdm2-leg-a-review-book.md`.

---

## 1. Top-line

Leg B ran the **pre-registered Edition-V refit-trigger diagnostic** over the v2.0-enriched corpus, and the pre-registered decision tree traced clean to an honest halt:

1. **The refit trigger FIRED** (vocabulary arm) — the v2.0 enrichment carries words E4's camera has no column for, exactly as forecast. So a Path-B true refit was *warranted by evidence*, not appetite.
2. **The refit ran faithfully** — E1's exact machinery, hyperparameters unchanged, over the resolved feature set (13-coord register + geometry-bands + element_primary as axis input; court + six blocks supplementary).
3. **The refit did NOT congruently anchor to E4** — the B3 congruence gate returned **0.7836 < 0.85** (a 58.54° re-orientation of the leading plane). Per the pre-registered §8-C fallback (the refit-candidate-1 precedent), **E5 is NOT served; E4 remains truth**; the rotation is disclosed as an evidence exhibit.

**This is not a failure — it is the finding §8-C promises.** Read the trigger-fire and the congruence-fail together and they say something precise and strategically load-bearing: **the v2.0 enrichment demands a basis whose leading plane is not congruent with E4's camera.** A v2.0-faithful Edition-V would require a *new camera*, abandoning the E1→E4 lineage continuity that three editions of stability were built on. **That trade is a commitment-class decision, and it is yours** (§4). The run files it; the run does not make it.

**The leg closed clean.** The red-flag log is empty (§6): the B3 fail is inside the pre-registered §8-C envelope, so the conservative default governs and no ping was raised. elrond filed no freeze-request — correctly, there was no passing candidate to freeze.

---

## 2. What executed (the pre-registered tree, step by step)

elrond executed the BINDING prereg with seed `20260722`, reusing E1's derivation module verbatim (`import atlas_derivation_2026_07_14 as D1` — verified first-hand; no method drift). The four pre-registered steps:

- **§2 — the refit TRIGGER (runs first, from E4 §9).**
  - *Vocabulary arm — **FIRED.*** 19 absent v2.0 levels each cleared the ≥20-exhibit threshold — the geometry-band vocabulary the frozen E4 camera has no column for (delivery_class=zone, origin=self, melee_arc among the largest). This is exactly what legolas Mode-A forecast (Q3, "fires decisively"), and the diagnostic made it a measured fact rather than an assumption.
  - *Expression arm — did NOT fire.* Record-267 cohort median cos² = 0.18424, comfortably above the 0.08426 threshold (0.5× the E1-active median). The known levels are still well-expressed in E4's axes; it is the *new* vocabulary, not weak expression of the old, that warrants the refit.
  - → **Path-B refit warranted** (either arm firing suffices). The vocabulary arm is the RB-6 story made quantitative: v2.0 added words to the language.

- **§2b — element_primary admission (the frozen A-LB6 decision rule).** Before the refit, elrond ran the within-cell test: is `element_primary` consistent or scattered among kits sharing the same mechanical cell? Result: **ADMIT as axis input** (max mechanical Cramér's V = 0.555). The RB-6 delivery-register earned its place as a genuine coordinate, not noise — the run's headline Leg-A recognition proved admissible under a rule frozen before the result existed.

- **§3 — the Path-B refit (E4 §6 B1–B3).**
  - *B1 — re-fit.* 265-kit fit (record-267 minus 2 unprojectable kits — §5), 21 MFA blocks (14 register coords + 6 geometry-band coords + element_primary), indicator matrix 265×87, **17 retained dimensions** by parallel-analysis (Greenacre-corrected inertia, 1000 permutation nulls — not Kaiser). Triangulation witnesses ran (MDS, Leiden, LCA), method unchanged.
  - *B2 — Procrustes anchor to E4's camera* (translation + rotation + reflection, NO scale). Anchor = the **46 record-class gateA members** common to the E5 fit and E4's served plane (cleared the A-LB2 floor of 40). Transform: **rotation 58.54°, reflection True, optimal scale s\* = 0.8117** (disclosed, NOT applied — E4 distance semantics preserved).
  - *B3 — the congruence gate.* Tucker congruence on the anchor plane post-transform = **0.7836**, against the ≥0.85 threshold (P-2). **FAIL.**

- **HALT at B3.** Gates A/C/D and Finding F-1 were never reached; no `atlas-edition5.json` was emitted; per §7's no-tuning-until-pass, elrond halted and returned the fork to me.

---

## 3. The trust-but-verify (why the fail is real, not a bug)

A gate FAIL is only a finding if the FAIL is *sound*. I did not take elrond's halt on its account — I read both the gate report **and** the 984-line refit script, and independently established three facts that make the 0.7836 a **structural** re-orientation, not a computational artifact:

1. **No method drift.** The script imports and reuses E1's exact derivation machinery (`import atlas_derivation_2026_07_14 as D1`). The refit is E1's method applied to v2.0 features — not a re-implementation that could diverge.
2. **The congruence is measured on the plane Matt actually sees.** B2/B3 compute on the **2D served plane** (`mca_coords[:, :2]`, script lines 519-526 — commented "the camera Matt sees, the design-load-bearing plane"). So the 58.54° is a genuine re-orientation of the *leading* plane (dim-1 × dim-2), driven by the new geometry-band + element_primary blocks changing the leading MCA structure. It is **not** a higher-dimension bookkeeping quirk or a dimensionality-mismatch between a 14-dim E4 and a 17-dim E5.
3. **Scale is not the cause.** The failure reproduces three ways — no-scale 0.7836, Pearson 0.7729, and *even if* the disclosed s\*=0.8117 were applied 0.7856. All three sit well under 0.85; the gap is not an artifact of the no-scale convention.

And the **max-movers corroborate structure over bug**: the eight largest displacers cluster in the melee/proc/aura families the new blocks most re-weight — d2-frenzy-barb (Δ1.483), poe1-mjolner (Δ1.454), d2-horker (Δ1.165), poe2-twister (Δ1.154), d2-auradin (Δ0.991). Their motion is dominated by the dim-2 (EMBODY↔LAUNCH) axis. A *bug* would scatter the movers randomly; a real re-orientation moves exactly the kits whose new geometry-band vocabulary (melee_arc, whirlwind, self-origin) and delivery-register the frozen camera could not previously see. The rotation is honest.

**Why §8-C and not the one permitted amendment cycle.** The prereg allows one diagnosed amendment (§7) — but only for a diagnosed *methodological defect*. Here there is none: the anchor cleared its floor, the plane is the pre-registered target, reflection is permitted, the machinery is E1's. Every "fix" I can construct is **tuning-to-pass** — either demote the vocabulary-arm features that *caused* the honest re-orientation (the very information the trigger fired on), or swap the pre-registered 2D-plane congruence test for a full-dim test to manufacture a pass. Spending the amendment to force a pass would *be* the failure mode, not avoid it. So §8-C is the disciplined landing, not a shortcut.

---

## 4. THE FORK FOR YOU (the run's terminal strategic finding)

This is the one thing in this book that wants your ruling. Everything else is settled or carried-over.

**What the run learned:** the v2.0 enrichment (the six blocks + the RB-6 orthogonal delivery-register) is real new information — enough that a faithful re-derivation over it produces a leading plane **58.54° off E4's camera** and only **0.7836-congruent**. The old camera can still *hold* the new citizens (Path A supplementary projection has done exactly that for Editions II–IV), but it cannot *reflect what v2.0 now knows* without moving. So the fork:

- **Path A — lineage continuity (the §8-C default, already in force).** E4 remains served truth. The v2.0 enrichment is admitted *supplementary* (the house method — the camera never moves; three editions of downstream trust in the E1→E4 axis semantics are preserved). The six blocks + RB-6 register live as queryable annotation on the map, but do not re-shape it. **Nothing to do — this is what the run landed on.**

- **Path B — a new-camera Edition-V (an override you would commission).** A fresh basis derived faithfully over v2.0, *accepting* the break with E1→E4 congruence — new axes, re-derived names, and every downstream consumer of the current axis semantics re-onboarded. This is not a refit; it is a **new derivation charter**, a genuine commitment.

**My conductor lean: honor Path A (ratify the §8-C default).** Three reasons, offered as an ELICITOR fork-plus-lean — you rule:
1. **The E-lineage discipline points here.** "Don't move the camera unless the evidence demands a move *and* the moved camera still anchors." The evidence demanded we *look* (trigger fired) — but the moved camera does **not** anchor (0.7836). The disciplined response to "a faithful new camera won't line up with the old one" is to keep the trusted camera and admit the new data supplementarily, not to abandon lineage on the strength of a rotation alone.
2. **The enrichment is not lost under Path A.** The six blocks are in the store; RB-6 is documented and queryable; the delivery-register is real and usable. What Path A defers is only whether the enrichment *re-shapes the primary map* — not whether it exists or informs design.
3. **A rotation tells us a v2.0 camera would *differ* — not that E4 is *inadequate*.** A new-camera commitment should be justified by a downstream *need* (a concrete design question E4's axes cannot answer), not by the mere fact that the refit rotated. I have not seen that need yet; if it surfaces, Path B is there, and this run has already done the measurement that would justify it.

**But this is genuinely yours,** because it trades two real values against each other: *lineage continuity / camera stability* (worth three editions of accreted downstream trust) versus *data fidelity* (a map that reflects everything v2.0 now knows). That is a taste-and-commitment call, and the charter reserves it to you (the Edition freeze was always your boundary). The run files the fork with its lean; you rule.

---

## 5. Curation-integrity footnote (benign; no action needed)

Two record-class kits — **`d2-teleport-sorc`** and **`poe1-blood-magic-kit`** — carry NULL `atlas_coords` in the v2.0 store, so they were unprojectable into the refit fit and dropped to supplementary-only (hence 265 derive, not 267). These are the *same* two kits legolas Mode-A flagged (Q4) as new to the v2.0 record class needing a fresh projection; they turned out to have no coordinates to project. **Zero impact on the B3 outcome** — neither is a gateA anchor member, so neither touched the congruence estimate. Flagged only as a catalogue-completeness note for a later pass (these two kits want a coordinate assignment if they are to participate in any future derivation, Path A or B). `blood-magic-kit` is additionally a known two-court straddle (V-20: "Blood Magic isn't even an element — a mana keystone"), so its NULL coordinate is consistent with its honest-NULL court.

---

## 6. Red-flag log: empty

**No red-flag ping was raised to you in Leg B.** The B3 congruence FAIL is inside the pre-registered §8-C fallback envelope (charter §6 / V-3 reserves pings for a commitment-boundary hit, a Gate-2 BLOCK with no honorable-fallback, a **gate-FAIL with no fallback**, or a substrate-integrity danger). §8-C *is* the fallback — the fail has a pre-committed honorable landing, so it belongs in this book, not the ping log. The live catalogue store was never touched by Leg B (the refit reads the frozen v2.0 corpus; it emits a candidate basis, not a mutation) — corpus.db closes Leg B exactly as Leg A left it (md5 `bebc933b…`, iron-law 585/574/19).

---

## 7. What parks at you now (the ratification queue — carried + new)

None of these blocks anything. They are your interrupt surface; the run has closed under conservative defaults.

- **(NEW) The Edition-V camera fork (§4).** Ratify Path A (do nothing — the §8-C default stands, E4 remains truth, v2.0 admitted supplementary) OR override toward Path B (commission a new-camera Edition-V derivation charter, accepting the E1→E4 break). Conductor lean: **Path A.**
- **(carried from Leg A) The E-1 admission decision.** The refresh-beat call on folding admission candidates (`di-druid-pvp-cc-stack-2026` new-row · `d2-ghost-pvp` re-key · LA 4 · MULTI-PROJECTILE-VOLLEY). Conductor lean FOLD (V-5); conservative default (no admission) governed the run unruled. Now that Leg B landed on Path A (no new camera), the FOLD would be a *supplementary* admission into the **E4** basis (the same Path-A mint the other editions used) — cheaper and lower-stakes than it looked at the beat, since there is no re-derivation for it to ride.
- **(carried from Leg A) The door-arg RFC (V-21).** The ELICITOR-authored, corpus-wide door-arg vocabulary from the ~177 attested pairs — decision-shaped forks + a lean for your ruling (a season-lever is commitment-adjacent). Severable, post-W5, blocks nothing.
- **(carried from Leg A) The §1.6 scaling-curve assumption.** The court×register two-axis structure presupposes a non-parabolic-over-fixed-interval endgame scaling curve — a progression/keystone-design input for a jack-ryan Gate-1 conversation. Note the compounding: if you take Path A, the two-axis structure lives as *supplementary* register on E4 rather than as re-derived Edition axes — but the scaling-curve constraint on its downstream *viability* is unchanged either way.

---

## 8. Run closeout

Both legs are complete. **Leg A** re-emitted the 267 record-class kits into the VDM-2 six-block structure and migrated the store v1.1→v2.0 (Leg-A book, RATIFIED). **Leg B** ran the pre-registered Edition-V refit trigger, found it warranted, executed the refit faithfully, and landed on the §8-C honorable fallback with a rich strategic finding filed for your ruling. The run closes into a **consolidated gate-roster HALT** parking at you: the Edition-V camera fork (§4) plus the carried queue (§7). The Tier-3 encounter-geometry run remains a separate sequel, unstarted.

**Signed:** gandalf (`RUN-CONDUCTOR`, SPEC-AUTHOR → DRIFT-CRITIC at Leg B), 2026-07-22. Veto open on every ruling (ledger V-1..V-26).

**RATIFIED** by the conductor against elrond's emitted artifacts, re-read from disk after compaction (charter-freshness discipline). Independently verified before signing — not from any sub-agent's account: the refit script reuses E1's machinery verbatim (`import atlas_derivation_2026_07_14`); B3 congruence computes on the 2D served plane (script L519-526); the 0.7836 FAIL reproduces three ways (no-scale / Pearson / if-scaled — scale is not the cause); the max-movers cluster in the melee/proc families the new blocks re-weight (structure, not bug); the trigger's vocabulary arm fired (19 levels ≥20) and expression arm did not (cos² 0.18424 > 0.08426); element_primary admitted under the pre-frozen A-LB6 rule (Cramér's V 0.555); the anchor cleared floor 40 (46 record-class members); no `atlas-edition5.json` emitted; no freeze-request filed; corpus.db untouched by Leg B (md5 `bebc933b…`, iron-law 585/574/19).
