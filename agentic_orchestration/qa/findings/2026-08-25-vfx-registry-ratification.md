# Finding — 2026-08-25 — VFX feature-registry ratification + the KR-seal record reconciliation

**Reviewer:** jack-ryan (RATIFIER, inside the Matt-authorized VFX-DEPTH autonomous run; conductor: gandalf RUN-CONDUCTOR)
**Severity:** **WARN** overall — 12 rows ratified, **0 rejected**, 1 promoted, 2 laws amended, 1 I-4 boundary re-cut, 3 defects flagged. **No BLOCK.** One item carries **ESCALATE** weight (Item 2's Matt-facing record).
**Target:** `agentic_orchestration/gandalf/vfx-feature-registry.md` (FF-01..FF-12 + § 1 rules + § 3 candidate) · collab seal commit `950f6656`
**Developer/proposer:** gandalf (registry rows, I-4 proposal) · galadriel (W-E1 matrix, the measured under-fire) · knight-rider (the seal) · drax (the W2 F-2 retraction that occasioned Item 2)
**Principles applied:** Review Principles **#1** (math before code), **#3** (cross-seam impact), **#4** (the record is the truth), **#5** (severity matters). Disciplines **#63** (unmeasured is not zero), **#64** (a name is not a referent), **#75 cl. 1** (bind the instrument to the artifact that ships), **#75 cl. 6** (a remedy does not inherit its predecessor's instrument). Governance: **ADR-002** tiered approval; `canonical-doc-format.md § 6.7`.
**Session note:** the ratification pass was executed across local midnight. It is stamped **2026-08-25** throughout because that is the run-date of every artifact it rules on; it was filed in the early hours of 2026-08-26.

---

## ITEM 1 — the registry bundle

### 1(a) — the eight founding rows

| row | disposition | reasoning |
|---|---|---|
| **FF-01** Leading-edge intensity apex | ✅ **RATIFIED — ESTABLISHED** stands | I-2 clause (b), Matt's eye. galadriel's F1 carrier is control-clean (comet 0.539 vs bar 0.000). Route caveat pulled into the cell: refuses below elongation 2.0 / 20 % of frames, and the absolute predicate `V>0.80 AND S<0.30` is a synthetic's idealisation — **the gradient, not the absolute level, is what is unambiguous on real footage.** |
| **FF-02** Intensity gradient along extent | ✅ **RATIFIED — ESTABLISHED** stands | I-2 clause (b). Control-clean on both `val_slope` and Δsat. |
| **FF-03** Cross-section variation | ✅ **family RATIFIED** · ⛔ **route NOT ratified (I-7)** | The family is Matt's eye and is not in doubt. `cv_width` is **DISQUALIFIED by its own null (backwards: comet 0.283 vs bar 0.305)**; the survivor holds 0.20 of margin, which is galadriel's own *"every F3 call is low-confidence."* **Cell now says INSPECT ONLY, MAY NOT CARRY A BAR.** |
| **FF-04** Particulate shedding | ✅ **family RATIFIED** · ⛔ **route NOT ratified (I-7)** | `sat_dist_norm` DISQUALIFIED; `sat_count` **caps at 400 and the whirlwind reference sits AT the cap**; on a reference leg the novelty mask contains enemies, gore, decals and HUD with no fx-off control available. |
| **FF-05** Volumetric embedding | ✅ **family RATIFIED** · ⛔ **route NOT ratified (I-7)** | `halo_softness` DISQUALIFIED; `halo_area_ratio` **cannot separate smoke from bloom — the scar arm, which contains no smoke at all, reads HIGHEST in the set (5.14).** A present/absent call is simply not available from this route. |
| **FF-06** Environment response | ✅ **RATIFIED — ESTABLISHED** stands | The only row satisfying **both** I-2 clauses (2 archetypes **and** Matt's eye). Its boundary against FF-10 is re-cut — see 1(c). |
| **FF-07** Camera somatic response | ⚑ **AMENDED — PROMOTED to ESTABLISHED** | **This is the pass's one status change and it is a consistency repair, not new evidence.** FF-07's promotion route is I-2 clause (b), Matt's eye (*"We cannot miss these elements!"*) — **identical to the route that carried FF-01..FF-05 to ESTABLISHED.** One evidence route cannot yield two statuses. Lap-1's 2/2 **TRUE NEGATIVE is corroborating, not contrary**: the dimension fired and correctly reported absence; **a family is not demoted by an exemplar that lacks it.** Second-archetype work (Demonic Leap) is re-classed from *status gate* to *route calibration* — and it is genuinely wanted, because the F7 null is a **rigid** pan while a 3-D tracking camera manufactures HF the null cannot model. |
| **FF-08** Temporal texture | ✅ **family RATIFIED — ESTABLISHED** · **route AMENDED** | See 1(b). Family status is the strongest in the registry: I-2 clause (a) satisfied by **26 reference legs across 24 archetypes and 5 classes**, plus an independent re-measurement through a separate code path on a separately re-fetched file (CV 1.107 both times). |

**Governance amendment landed with this pass — `I-2`:** the OR is disjunctive **and the Status cell must now NAME the promoting clause.** The FF-01..FF-05 / FF-07 divergence was invisible for exactly as long as no cell had to say which clause it used. *One evidence route, two statuses, is not a rule; it is a habit.*

**New rule landed — `I-7 ROUTE ≠ FAMILY`:** a family's status is a claim about a **phenomenon**; a detection route is a separate claim about an **instrument**, carrying its own validity. **A route disqualified by its own control may inspect, but may not carry a bar.** Cited: **#75 cl. 1** (bind the instrument to the artifact that ships) and **#75 cl. 6** (a remedy does not inherit its predecessor's instrument).

> ⚑ **DEFECT (WARN) — why I-7 was necessary rather than tidy.** The disqualifications were correctly and honestly recorded — in **§ 3**, as a caveat on the dataset. The **route cells in § 2 said nothing.** A consumer who reads the family table and never the dataset section is not a careless consumer; **he is the normal consumer, and the SPEC step is exactly that consumer.** A caveat that does not travel with the number is not a caveat. Fixed in-place by pulling the disqualifications down into the three affected cells. *(Same shape as this session's recurring finding: an instrument returning cleanly after it stopped answering the question.)*

### 1(b) — the FF-08 detection-route amendment: **UNDER-FIRE CONFIRMED · AMENDED, NOT AS PROPOSED**

**The under-fire is real and galadriel measured it correctly.** `OURS_blink`, CV **exactly 0.000**, dominant tone 945× — **missed the >1000× conjunct by 5.5 % and did not trip.** A metronome escaped a metronome detector.

**Proposed:** `CV == 0.000` exactly trips alone.
**RULED:** ⛔ **rejected as drafted** · ✅ **`CV < 0.25` TRIPS ALONE**; the spectral tone is **demoted from trip-condition to corroborating diagnostic.** *Inspect, never auto-pass* is unchanged.

**Why the broader form, from the tabled data and not from taste:**

1. **The proposal leaves a second escape standing.** `OURS_teleport` = CV 0.021, tone 473× — **under both bars.** galadriel inspected it anyway, *"on the CV alone."* The candidate rescues `blink` and still not `teleport`.
2. **It is a knife-edge predicate on a rounded display.** A metronome with one jittered interval reads 0.004 and escapes again. **A law one float-equality wide will be re-amended by the next row that misses it by a rounding digit.**
3. ⚑ **The conjunct never once ADDED a trip. It only ever subtracted.** Measured record of the tone term across the entire matrix: **2 trips, 2 escapes — and both escapes overridden by the instrument's own operator in the same table.** A condition whose whole observed effect is to suppress calls its owner then makes by hand is not a gate; it is friction with a spreadsheet. **The law should ratify the behaviour the instrument's owner already found necessary.**

**The arithmetic the new bar rests on:** 26 reference legs span **CV 0.449 – 1.149; not one falls below 0.449.** A sole-trip bar at 0.25 has **zero false-positive exposure across the entire measured reference corpus, with 0.199 of margin** below the lowest reference and a 0.346-wide empty band (0.103 – 0.448) containing no row of any kind. **That is a measured bar. `CV == 0.000` is a bar fitted to one row.** (Review Principle **#1**.)

**Carried caveats, binding on consumers:** CV inherits event-detection validity and 30 fps caps observable intermittency at 14.985 Hz · **a row below the minimum interval count records INDETERMINATE, never PASS** (`OURS_ground_slam` trips on six events) — **Discipline #63**, and the threshold itself is **galadriel's to set: it is an instrument parameter inside her seam and this ruling does not invent one** · the finding stays an **AUTHORING** finding, since `leap_strike` (0.668) and `dash_attack` (0.955) sit inside the reference band from the same seam on the same day.

**Not an I-6 item:** the trip law is a MEASURE-layer route, not a Layer-1 attention dimension. It stays audit-key-side; its CV outputs are content-free and remain legal at MEASURE and SPEC per the matrix's own quarantine stamp. Reading the quarantined matrix from this informed-side seat was legal and is recorded here as exercised.

> ⚑ **DEFECT (INFO) — flagged, not corrected; the audit doc is not mine to write.** `lap1-coverage-audit.md § 1`, FF-08 row, calls the blind passes *"independent supporting evidence for the FF-08 detection-route amendment."* **They are not.** The passes corroborate the **phenomenon** — 2/2, qualitatively, and that is a genuinely strong result. **An eye cannot corroborate a spectral-tone threshold's conjunct structure**, which is the only thing the amendment is about. Real evidence pointed at the neighbouring question.

### 1(c) — FF-09..FF-12 against I-3, and the I-4 split ruling

All four **PASS the I-3 phrasing law on all three litmus skills**, and all four **stay PROVISIONAL correctly**: both blind passes are the *same* skill, so I-2 clause (a) is not met and clause (b) has not fired. **The status column was right; I ratify as entered and add three binding notes plus one boundary ruling.**

| row | disposition | ruling |
|---|---|---|
| **FF-09** Recipient state response | ✅ **RATIFIED — PROVISIONAL** | Strongest I-1 entry in the set: **both passes ranked it #1 independently, and the registry was silent.** ⚑ **Scope note added:** the family names an **OBSERVABLE, not a seam.** A recipient reaction authored by the animation system is still FF-09; the SPEC routes implementation to whichever seam owns it and **must not reject the family as "not VFX."** X-1 self-caveats this boundary already (audit § 5.3), so it will be argued if it is not pre-ruled. |
| **FF-10** Effect transfer & attached persistence | ✅ **RATIFIED — PROVISIONAL** · ⚑ **I-4: SPLIT UPHELD, BOUNDARY RE-CUT** | See below. |
| **FF-11** Lifecycle phase structure | ✅ **RATIFIED — PROVISIONAL** | Distinctness holds both ways: against **FF-08** (interval irregularity vs macro state-sequence) and against **FF-02** (temporal sequence vs spatial gradient). ⚑ **Phrasing note added, binding on the SPEC: the five named phases are ILLUSTRATIVE, NOT A REQUIRED INVENTORY. A two-phase effect satisfies the family.** Graded as a five-item checklist, this row becomes EXPECTED CONTENT — **the exact failure I-6 forbids one layer down**, arriving at the layer I-6 does not cover. |
| **FF-12** Effect-driven illumination | ✅ **RATIFIED AS UNIFIED — PROVISIONAL**, with a pre-named split trigger | The definition carries **two separable claims** — self-luminance above ambient, and light **cast** onto neighbours — and they dissociate in practice (an emissive-only particle that lights nothing is a standard engine shortcut). **Kept unified**, because both passes named them together (X-1 #6 luminance, X-2 dim 4 cast) and **I-1's bar on theory-only ENTRY applies equally to theory-only SPLITS.** ⚑ **Trigger recorded in advance:** it splits into FF-12a / FF-12b **the first time a measured skill shows one without the other** — so the split is *executed* rather than re-argued. |

#### ⚑ The I-4 ruling — FF-10 vs FF-06: **the conductor's proposal is ACCEPTED and its DISCRIMINANT is REPLACED**

**Split upheld.** They are two phenomena, and both blind passes distinguished them without being told to.

**But the proposed axis does not survive its own definition.** The note proposes *world-surface (FF-06) vs actor-attached (FF-10)* — while **the FF-10 definition reads "transfers … to recipients/surfaces," re-entering FF-06's territory in the same sentence.** The carrier axis also cannot classify the ordinary case of ground-fire still burning after the cast ends.

**Re-cut on the EMISSION axis:**

- **FF-06** — the world is left **ALTERED**: residue, a state change, a scorch, a crack, a dust settle. *Nothing is still running.*
- **FF-10** — the effect's **OWN EMISSION CONTINUES** from a transferred origin, on a carrier (**actor or surface**), under its own lifecycle, outliving the delivery form. *It is still running, somewhere new.*

**Every lap-1 datum classifies without ambiguity under it:** X-2 #1 *"the effect is ON THE VICTIMS"* → FF-10 · X-1's ember-orb still emitting ~5 s post-flame → FF-10 · X-1 dim-5 blood pools, scorch, char → FF-06. **Both passes already drew this line. The ruling names the axis they used rather than imposing one they did not.** Detection route updated to per-**region** tracking that discriminates continuing emission from static residue **by temporal variance, not by carrier identity**.

Three-skill litmus, run on the re-cut pair: healing aura → FF-06 nothing / FF-10 lingering regen glow on the ally · laser → FF-06 scorch line on the wall / FF-10 the molten point still glowing · ground slam → FF-06 cracks and settled dust / FF-10 burning debris riding the struck targets. **Both families read sensibly on all three. I-3 holds after the re-cut.**

---

## ITEM 2 — the KR seal `950f6656` · **RULING: RECONCILIATION IS NEEDED, AND IT IS LARGER THAN A LINE**

**Filed** as a stamped ratifier block at the head of the seal's record-of-record, `qa/pending/2026-08-25-my-ww7-miscitation-…-under-a-different-name.md` (my queue; **KR's text struck nowhere, nothing rewritten** — the run's own strike-not-edit discipline, which drax modelled at W2 F-2).

**What stands, and it is most of the seal:** `WW-7` **is** an SB-1 run-ledger cell id and not a whirlwind label — **the mis-citation retraction is correct and I do not disturb it.** The surviving measurement (81.88 vs 43.64 px/m → **0.979 octaves**), its re-label to *SB-1 `ww7-gate2` at `player_lock` k=0.665*, and the HALT are **all unaffected** — none of them ever depended on the archetype label. **No decision is reopened by this ruling.**

**What is false:** the seal's **title** — *"WW-7 was never a whirlwind"* — and the claim propagated from it, *"the clip holds no whirlwind archetype."*

**The instrument, and it returned cleanly while answering a different question.** `grep -c -i whirlwind run_ww7_gate2_clip.sh → 0`. **I re-ran it. Still 0. TRUE — and NON-PROBATIVE.** That file is a **camera wrapper**: it does not contain the content, it *renders* it, at its own line 282 — `scenes/kc2_cpb_clip.tscn`. ⚑ **And the wrapper's header cites `kc2_cpb_clip.gd` four times (lines 24, 32, 47, 60): the file that answers the question was named inside the file that was grepped.** The scene script, `scripts/kc2_cpb_clip.gd:119-120`, verbatim:

> *"It exists to answer ONE question — does the **whirlwind** read, now that the man has a head, a hammer, and a rate Matt chose?"*

Four `whirlwind` hits in that file, including `"aim_is": "the WHIRLWIND STATION"` at :1080. **The grep's DOMAIN never contained the question — Discipline #63's clause-shape, #75 cl. 1 at the instrument, and precisely the line KR conceded to drax in this same session: *a correct mechanism tested against an assumed object agrees with itself.* The seal states that clause, and its own title is felled by it.**

**galadriel's pixel verification STANDS — and it is the fifth word-collision, on the word "whirlwind" itself.** *"A tiled arena, an altar, ~5 actors, a smoke volume and one thin melee arc"* is an **accurate frame description** and it is **not evidence against a whirlwind.** The referent is a **spin-attack archetype** (Undead Knight, warhammer, cut/spark arcs at `CUT_PER_REV 17`), not a **vortex phenomenon**. *One thin melee arc is what this whirlwind looks like.* **Discipline #64.** The seal catalogues four word-collisions this session (`census` · `terminal` · `WW-7` · `totem`); **the fifth was inside the seal, and it is the only one to reach a Matt-facing document.**

### ⚑ The consequence that is not record hygiene — a live design question INVERTS

The wave record's closing line: *"the A/B is **cross-archetype** — our whirlwind against a melee-cadence clip. As a depth-treatment reference that may be better than like-for-like; as a like-for-like comparison it is not one."*

**Under the correct label that caveat is VOID. Both arms are whirlwind casts. The A/B is LIKE-FOR-LIKE, and it is a stronger test than the record credits it with being** — the depth-treatment value the resolved to-do identified is **not replaced, it is joined by archetype match.** A design question **dissolving in our favour**, sitting unclaimed because a label was wrong. (Review Principle **#3**.)

### Where the correction is still owed — **ESCALATE**, flagged not written (not my files)

| record | owner | still says |
|---|---|---|
| `agentic_orchestration/step2-vfx-archetype-mint-wave-record.md` ≈ L399, L414-415 | knight-rider | *"holds no whirlwind archetype … galadriel's pixel verification stands with it"* + the cross-archetype caveat |
| `canonical/matt_to_do/2026-08-25-where-does-your-hitl-whirlwind-run-live.md` (CLOSED) | canon steward | *"The clip contains no whirlwind archetype — that part stands"* ⚑ **highest consequence: this is the copy MATT reads, and it is marked RESOLVED** |
| commit `950f6656` title | immutable | reconciled by the filed block; git messages cannot be edited and the pending filing is the record-of-record they point at |

**Also noted (INFO):** drax cites the source at `kc2_cpb_clip.gd:111-112`; the lines are **119-120**. **The quote is verbatim-correct** — citation drift only, almost certainly file movement. Named because this run's whole subject is citations that stop pointing at their object.

---

## Action

- [ ] **gandalf (conductor):** two audit-doc defects — § 1 FF-08 over-claim (an eye cannot corroborate a conjunct threshold); § 3 FF-10 definition said *"recipients/surfaces"* while proposing a carrier-axis split (**resolved by the I-4 ruling**; the audit text still carries the old phrasing). Registry is ratified — **the SPEC step may consume FF-01..FF-12 now**, subject to the three I-7 INSPECT-ONLY routes and FF-11's illustrative-phases note.
- [ ] **galadriel:** adopt `CV < 0.25` sole-trip; keep spectral tone as a recorded diagnostic. **Set the minimum-interval-count threshold below which a row is INDETERMINATE** — yours, deliberately not invented here. FF-03/04/05 route rehabilitation is wanted but is not gating.
- [ ] **knight-rider:** reconciliation line into `step2-vfx-archetype-mint-wave-record.md`, and **claim the like-for-like upgrade** — it improves the A/B you own.
- [ ] **canon steward:** the Matt-facing `matt_to_do` correction. It is CLOSED and wrong on one clause; a closed record is the one nobody re-reads.
- [ ] **Matt (veto-open, not blocking):** FF-07's promotion to ESTABLISHED and the FF-08 sole-trip bar are the two rulings a reasonable person could rule differently. Both are reversible; neither has yet been built on.

**Approval basis (ADR-002):** documentation-and-governance-only changes within the ratifier's own authority per `canonical-doc-format.md § 6.7`. **No code, no schema, no seam API touched.** Item 2's Matt-facing row is raised as ESCALATE rather than actioned, because the file is not mine.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/vfx-feature-registry.md` (ratified in place)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/vfx-depth-run/lap1-coverage-audit.md` §§ 1, 3, 5 (read; not edited)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/2026-08-25-vfx-depth-feature-matrix-ta.md` §§ 1.1–1.5, 3.3, trip-flag disposition table
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-25-vfx-depth-w1-playerlock-camera-and-4a-completion-record.md` § "Clip 1's LABEL, corrected in the record"
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-25-vfx-depth-w2-cathedral-venue-completion-record.md` § 4c, F-2
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-08-25-my-ww7-miscitation-propagated-into-a-measurement-and-the-number-survives-under-a-different-name.md` (reconciliation block filed at head)
- `/Users/admin/Games/reincarnated-godot/scripts/run_ww7_gate2_clip.sh` (the wrapper that was grepped; its line 282 and its own header cite the scene)
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_cpb_clip.gd` lines 119-120, 1080 (the file that settles it)
- Charter ledger rows **R-14, R-17a, R-18(b), R-19b, R-20**: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-25-vfx-depth-run-charter.md` (read; not edited)
