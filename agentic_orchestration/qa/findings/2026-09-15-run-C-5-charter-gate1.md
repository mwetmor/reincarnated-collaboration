# Finding — 2026-09-15 — Run C-5 (VFX) charter (Gate-1, pre-GO)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Severity:** **BLOCK** — two items, both cheap, both pre-GO. Five of my six prior BLOCKs are **discharged**.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` v1.0 (`sha256[:12] d2bc7eb4f0ee`, 112 lines) · ledger `astra_test_01/burst/runs/C-5/ledger.json`
**Author under review:** gandalf (ARCHITECT → RUN-CONDUCTOR on GO)
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 4 (decisions-log as truth) · 5 (severity matters)
**Disciplines / ADRs cited:** #1, #41, #73, #75 cl. 2, #75 cl. 6, #80 · ADR-002, ADR-004, ADR-006

---

## 0. Verdict in one paragraph

This is a real charter. Against the six BLOCKs of `2026-09-15-vfx-architecture-gate1.md`, **five are discharged outright** and the sixth is discharged in substance and broken in its record. The document does what the last one did not: it names a run, opens its own ledger, restates all seven `mechanical-process.md § 1.6` HALT conditions with Matt's waiver attributed to Matt, gives a decidable exit predicate *and* an honourable fallback, prices the prerequisites as **two owned phases** rather than a £0 given, and — the item I have been carrying open since 2026-09-13 — lands **§ 5 TOOLING rows with acceptance clauses that can go RED** (#80: **DISCHARGED**). The remaining BLOCKs are not design objections and neither touches the architecture. **BLOCK-A: V2 is recorded as ruled by Matt in three places and in a `class: matt` ledger entry, while the project's own decision queue says, in the same commit series, "V2 OPEN — one word owed."** It is the load-bearing fork: it retires `pixel_scale`, sets the whole § 2 scale contract, and sets the brief rule every asset is painted under. **BLOCK-B: the V20 waiver is encoded as `images_cap: null`, and the launcher does integer arithmetic on that field — burst #1 raises `TypeError`, not a VOID.** One word from Matt and one guard clause clear both.

---

## 1. Disposition of the six prior BLOCKs

| Prior BLOCK | Disposition | Evidence |
|---|---|---|
| **1 — no charter; halted ledger; H-C3-2 undisposed** | **DISCHARGED** | Own ledger at `runs/C-5/ledger.json` (`run`, `charter`, `charter_sha256_12`, `bursts`, `experiments`, `milestones`, `halts`, `rulings`, `grok_calls`). § 1 authority table · § 3 forks ruled · § 4 phase sequence · § 5 TOOLING · § 8 HALTs · § 0 exit predicate + V18 fallback. C-3 ledger `halts[]` now carries `H-C3-2` with `status: DISCHARGED 2026-09-15` and a written disposition — the CLAUDE.md mooted-escalation corollary satisfied, not merely mooted. |
| **2 — gates not decidable** | **DISCHARGED** | Clock declared **once**, 03- § 2.0: *"every band and gate is in frames of 1/60 s"*, with the 24 fps consequence re-derived and pointed the right way. White gate: crop = **960×540 centred on impact**, **peak frame is the gate**, clip-mean reported, **synchronised** is the gate case, flash on/off both reported, **baseline measured in P-0 and recorded first**, attributable = total − baseline *"both printed, never silently subtracted"*. V2 = 1 collapses native ≡ screen, so the 1-px unit drift dissolves. VO/CO namespaces declared and *"never cited bare"* — T4d's RED clause enforces it (*"any bare `O1`-style name left in output"*). |
| **3 — scale contract is a function of `pixel_scale`** | **DISCHARGED in substance** — but see BLOCK-A; the contract is now a function of an **unruled** fork rather than an unstated one. Canvas-vs-extent is bound (§ 6 briefs carry *"canvas + occupied bounds + pivot + plane"*, extent in screen px); E0-p residue is resolved to **erosion** with piece scale held *"within ±15 %"*, so § 4's deformation tripwire is adjudicable. |
| **4 — § 4 measured by an instrument that cannot measure it** | **DISCHARGED** | 03- § 4 now marks BUILT / UNBUILT / UNAUTHORISED per gate, and the charter converts every UNBUILT one into a **P0-b TOOLING row that must go green before E0** (T4d = clean-plate differencing + baselines + VO3 re-point + event-trace comparator). § 7 states the BUILT set and labels `field_v1`/`aura_loop_v1` **PROVISIONAL** pending the frame-extraction sourcing class — the unauthorised lap is not walked. |
| **5 — prerequisites are the build and cost zero** | **DISCHARGED** | P0-a and P0-b are phases with owners, bursts, RED clauses and their own Matt checkpoints (Packets 84, 85). The false "£0" is gone: 03- states *"E0 is £0 in images; it is **not** £0 in bursts — P-0 is where the cost is."* The two-owners-one-directory collision is resolved the right way by **V10**: the component is exporter-emitted (Astra), drax assists, hand-edits *"handed back as exporter changes"* — so the next PACK cannot regenerate over hand-authored work. |
| **6 — two ruled decisions reversed uncited** | **DISCHARGED** | **V6:** R-C3-90(2) restored as the default's alternative, carried as a *hypothesis under test*, with **E0(a) rendering both presets and Matt ruling on sight** (§ 4, Packet 86). **V4:** no longer "dissolved" — § 3 and § 10 both read **conditional / GATED**, ruled at **Packet 87** with R-C3-120's precondition (*Matt wants to SEE a VFX built to the spec*) restored and cited, and `2026-09-15-hybrid-vfx-oracle.md` collapsed to point here as the single disposition. |

**#80 (my 2026-09-13 Gate-2 action, open since) — DISCHARGED.** § 5's five rows each carry a falsifiable acceptance clause with an explicit RED: Δ ≤ 1/255 on a synthetic 4-band texture with *index 0 opaque*; erosion 0/50±3/100 %; contact stamped ≤ 1 frame; **cold first cast registers** (the v17 defect, now a gate); byte-identical consecutive bakes; a synthetic known 4 % white reporting 4.0 ± 0.2 %; piece union = source ± 0.5 %. T4c is correctly written **report-not-stop** per V17. This is the first charter in this lane whose tooling can fail.

---

## 2. BLOCK findings

### BLOCK-A — V2 is recorded as a Matt ruling; the decision queue says it is open, and it is the fork everything else is built on

**What I found.** Four places assert it ruled:

- § 2: *"**V2 = 1: effects match the scene** … `pixel_scale` retired; **1 BH = 130 screen px; 3–6 BH burst envelope = 390–780 px**"*
- § 3, under the heading *"Forks ruled (Q79, Matt 2026-09-15) — **the substrate is fixed**"*: *"V2 **1 (match the scene)**"*
- § 10 ARCHITECT gate: *"Q79 V1–V20 | **RESOLVED** (Matt, 2026-09-15)"*
- `runs/C-5/ledger.json` → `R-C5-0`, **`"class": "matt"`**: *"V2 = 1 match the scene"*

Three places say otherwise, two of them authored the same day by the same hand:

- **`canonical/matt_decision_needed/README.md`, the Q79 row:** *"I accept all rulings other than V1 … V9 … V10 … V17 … V20 · **V2 OPEN — one word owed: match the scene (art step 1, measured …) vs 3**"*
- **`03-architecture.md § 7a` — the charter's own cited design authority** — closes the V2 row: *"**Recommendation: 1 (match the scene)**; E0(e) shows 1 vs 3 in motion so the choice is by eye. **Pending Matt's word.**"* and states the consequence conditionally: *"**If 1:** the § 2.3 scale contract collapses to native = screen … `pixel_scale` is retired …"*
- The Q79 ruling commit's own message (`d6b540c0`): *"**V2 pending** with the scene measured (1:1 linear painting, no pixel step → rec art step 1)"*

**Why it is a BLOCK and not a WARN.** V2 is not one row among twenty. Everything downstream is its *consequence*, exactly as § 7a says: the retirement of `pixel_scale`, the 1 BH = 130 **screen** px identity, V19's 390–780 px envelope, *"no nearest-neighbour step"*, and § 6's standing brief rule — *"Painted extent declared in **screen px (art step 1)**"* — which every asset from P0-a onward is painted under. § 4 then demotes the checkpoint that was supposed to decide it: E0(e) reads *"art-step look, 1 vs 3, in motion (**V2 ruled 1 — confirmation by eye**)"*. A gate whose answer is asserted in its own description is not a gate. The queue's own words are *"V2 is ruled at E0 before any E1 image"*; the charter has pre-ruled it before P0-a.

And the shape is the one I raised last round. BLOCK-6 was *a ruled Matt decision presented as its own alternative*; this is *an unruled Matt decision presented as ruled*, in a ledger entry typed `class: matt`. The ledger is the run's record of what Matt said. Principle 4, Discipline #73.

**Mitigating, and it matters:** the recommendation is well-founded — the scene was actually measured (5376×4096 canvas, 1920×1080 camera, `default_texture_filter = 2`, Keeper 240 px → 130 px at scale 0.5417), and *"there is no pixel step in the scene"* is a fact about the artifact, not a preference. The risk is narrow: P0-a's monster pack is scene dressing in the H1 register at the scene's own 1:1, so almost nothing is spent at risk before E0(e). **Cost of being wrong is low; cost of the record being wrong is not**, because the next reader of `R-C5-0` has no way to know Matt never said it.

**Action.**
- [ ] **Matt:** one word — **V2: 1 or 3.** It is the last open Q79 row and the queue is already holding it.
- [ ] gandalf (if the word has not landed at GO): restate § 2 / § 3 / § 10 as **V2 PROVISIONAL AT 1 — confirmed at E0(e)**, restore § 7a's conditional phrasing, restore E0(e) as the ruling point, and **re-class the `R-C5-0` V2 clause from `matt` to `conductor` with `veto_open: true`**. GO may proceed on the provisional reading; the record may not assert the ruling.

---

### BLOCK-B — The V20 waiver is encoded as `null` in a field the launcher does integer-compares; burst #1 raises `TypeError`

**What I found.** The brief asked whether the waiver is recorded in a way `lane/audit.py` will VOID bursts against. **It is not — `audit.py` never reads the run cap.** It checks only the *per-burst* cap against per-type limits (`lane/audit.py:162-176`, `image_limit = {'GENERATE': 12, 'LABEL': 2}.get(type, 0)`). No VOID exposure. The run cap lives one layer up, and there it is a hard crash:

```python
# lane/run_burst.py:158
if current['images_used'] + task['image_cap'] > current['images_cap']:
    raise ValueError('insufficient run image budget')
```

`runs/C-5/ledger.json` sets `"images_cap": null`. `0 + 12 > None` → **`TypeError: '>' not supported between instances of 'int' and 'NoneType'`** — raised *before* the workdir is created, so the first GENERATE burst of P0-a dies at launch with an exception that says nothing about image budgets. Nothing in § 5's five TOOLING rows touches `run_burst.py`, and `lane/ledger.py:20`'s `empty()` still hard-codes `images_cap=250`, so a rebuilt ledger silently restores the cap V20 waived.

**Rationale.** This is my own BLOCK-4 family one layer down, and the standing law this repo restates in `CLAUDE.md` four times over: *the check running is not the check passing* — here, an instrument that cannot even run against the state the charter mandates. The charter's § 8 and § 9 are correct **as prose**; the encoding of the waiver is what fails. Discipline #75 cl. 6 exactly: *a remedy does not inherit its predecessor's instrument* — V20 changed the rule and left the mechanism pointing at the old one.

**Action.**
- [ ] gandalf: add a **T4f** row (or fold into T4a as the first clause) — guard the run-cap gate for a waived cap (`if current['images_cap'] is not None and …`) and make `ledger.empty()` accept the run's cap rather than hard-coding 250. **Acceptance:** a dry-run GENERATE burst against the C-5 ledger with `images_cap: null` reaches the brief without raising; `images_used` still increments and is reported at every packet. **RED:** any path that silently restores a numeric cap on C-5, or that stops counting.
- [ ] Alternatively and equally acceptable: keep the integer field and set a sentinel with the waiver in `images_cap_note` — **but then § 8's strike-through must say the cap is un-enforced by a sentinel, not waived**, or the next reader believes a number that no longer means anything.

---

## 3. WARN findings

**WARN-1 — `EDIT` is not a burst type; the launcher rejects it.** § 4 budgets *"EDIT ×(2–4)"* (P0-a), *"EDIT ×2+"* (E0-p) and *"GENERATE/EDIT as needed (counted)"* (E1, E2, E3) — five of seven phases. `lane/render_brief.py:6` declares `TYPES = ('TOOLING','GENERATE','CHECK','JUDGE','TRANSCRIBE','LABEL','ANNOTATE','PACK')` and `run_burst.py:246` binds `--type` to `choices=TYPES`; `--type EDIT` fails at argparse. C-3's 350 bursts used no such type (`GENERATE 146 · CHECK 127 · PACK 86 · TRANSCRIBE 63 · TOOLING 23 · JUDGE 4 · ANNOTATE 1`). If EDIT means *a GENERATE burst whose task is an edit*, say so in one line in § 9; if it means a new class, it needs a `BURST_RULES.md` row and an `image_limit` entry **before** P0-a, or `audit.py` will read it as type-unknown and flag `image cap outside type limits` on every image. The charter already flags the **CONSULT** class as owed to me; EDIT is the same gap and is on the critical path where CONSULT is not.

**WARN-2 — FF-08's interval-irregularity trip law is on the run's path and has no instrument in the charter.** 03- § 4 carries it (*"FF-08 interval irregularity (CV ≥ 0.25) on every tick/hop/pulse | event-trace CV | with T3x"*), and 03- § 2.2 states it as a grammar requirement (*"a metronome trips"*). The charter's T4d acceptance clause names *"event-trace comparator for field/aura gates (boundary vs radius; activation/expiry vs events; attachment drift)"* — **no CV** — and § 7's tripwire sentence omits FF-08 entirely. **E2 runs G2 (ground field, fixed tick schedule)**, so the law binds two phases from GO. This is the registry item I ratified on 2026-08-25 (the `OURS_blink` case the law was amended to catch: a fixed period is CV 0.000 exactly). Add CV to T4d's clause and to § 7's tripwire list. One clause each.

**WARN-3 — VO7 and VO9 are dropped without a statement that they are out of scope.** 03- § 4 lists both as **UNBUILT — T3w row**. The charter's § 7 enumerates the BUILT set as *"VO1–VO6/VO8/VO10"* — the omission of 7 and 9 is precise, and I read it as deliberate. But nothing says *"VO7/VO9 are not used in C-5."* VO7 is projectile speed in BH/s and **E1's fixture value is 4 BH at 8 BH/s** (§ 6) — so the achieved speed is an eye-check with no instrument, which § 7's *report-never-verdict* posture permits but which should be stated rather than inferred from an enumeration.

**WARN-4 — The scene the fixture lives in is named by description, not by path.** § 4 P0-a says *"Astra dresses a clearing in **the cliffside**"*; V10's ruling says *"the current scene"*. The repo question is now settled and settled correctly (exporter-generated, Astra-owned, drax assists) — that was the substance of my BLOCK-5 and it is discharged. What remains is that `astra_test_01/burst/runs/` holds **17 `cliffside_v*` trees**, the newest under `runs/C-3/`, and C-5 writes to `runs/C-5/`. Name the source tree and the destination tree in § 9 before P0-a, or the first PACK decides it silently.

**WARN-5 — Q68 G-4 is listed OPEN while V12, which Matt has now ruled, poses the same trade.** § 10 reads *"Q68 G-4 (body-alpha vs occlusion) | **OPEN, Matt's** — not hit before E3."* V12 (*readability of body/footprint first under conflict*) was accepted in the Q79 ruling, and R-25 held that this trade is Matt's alone. Either Matt's V12 acceptance **disposes** G-4 for VFX purposes — in which case say so and close it — or G-4 is a narrower question that survives V12, in which case state the distinction. Two live rows on one trade is the condition that produced the V4 collision I raised last round.

**WARN-6 — The Q79 queue row still points at v2.4 while the design authority is v2.5.** `matt_decision_needed/README.md` names *"**v2.4**"* twice, and its recommendation text still carries superseded positions (*"V4 hybrid oracle DISSOLVED"*, *"V10 drax builds the grey room"*, *"V20 E0-p budget ≤ 4"*) alongside the ruling line that reverses them. The row's ruling summary is correct; its body is pre-ruling. Same stale-reference defect as my WARN-17 last round, one revision later. Restamp the row when V2 lands.

**WARN-7 — The canonical destination is named; the decisions-log entry is not.** § 0 correctly names `canonical/reap-die-rise-game/painted-2d-pipeline/vfx-workflow.md` as the write-up target *"canon on Matt's word"* — that closes the half of WARN-17 that mattered. No decisions-log entry is proposed for the C-5 commitment set (V1 route, V2 register, V9 platform, V16 scope). Route one to me at E1's ruling, not at E3.

**WARN-8 — E1's fixture values remain unprovenanced, and the charter says so.** § 6 labels them **UNPROVENANCED** and gates them on Matt at Packet 85 before either arm is painted — which is the right handling of my WARN-11 and I note it as such. The residual exposure is unchanged: 8 BH/s against the shipped Frozen Orb v3's ≈ 4.9 BH/s is a **1.6×** difference, and **both A and B run at it**, so a wrong value fails both arms together and the experiment measures nothing about painted-vs-painted. Put the shipped figure on the Packet 85 card beside the proposed one, so Matt is approving a comparison rather than a number.

---

## 4. INFO findings

- **INFO-1.** § 8's HALT list is a faithful restatement of `mechanical-process.md § 1.6` — all seven conditions present, wording preserved, the waived one struck rather than deleted and attributed to Matt by ruling number. The three run-specific additions are additive and none narrows an inherited rule. This is the cleanest HALT restatement the lane has produced.
- **INFO-2.** § 8's medium/bar clause carries the H-C3-2 lesson **by name** (*"the conductor may not re-scope a halt rule in-run (H-C3-2 lesson, R-C3-22)"*). A discharged halt that stays legible as a rule is the correct end state for an escalation.
- **INFO-3.** § 7's rejection criterion restores 02d's dropped clause verbatim in substance (*"a candidate meeting bounds only by destructive clipping or unapproved distortion is rejected"*) — my WARN-8a from last round, closed. E3's *"material-glass gate at BWC/PConc; density gate at PConc"* closes WARN-8b. § 6's correspondence + boil tests close WARN-9.
- **INFO-4.** § 7's *"JUDGE bursts carry a known-bad control in every batch; a JUDGE passing its control twice is a HALT"* closes WARN-10 and the #75 cl. 2 action open from `2026-09-13-run-C-3-gate2.md`.
- **INFO-5.** § 10 row *"Renderer parity claims (probe 2 'VERIFIED' = read) | **E0 gates**, not facts"* — WARN-3/WARN-4 from last round, closed by conversion rather than by assertion. Correct move.
- **INFO-6.** Untracked capture debris is still accumulating in the working tree (three `kit_archive.db-shm/-wal` pairs, ~10 untracked C-3 capture PNGs, modified `t0c_*` test outputs). § 10 says *"capture directories untracked"* as a disk strategy; there is still no ignore rule, and § 9's `--only` discipline is what keeps it out of commits. Fine while the discipline holds; worth an ignore rule at the first quiet moment.
- **INFO-7 — credit.** Three things here are better than the lane's precedent: **(a)** § 5's RED clauses, which make tooling falsifiable for the first time in this lane; **(b)** T4c written **report-not-stop** under V17, which correctly refuses to let a feasibility unknown masquerade as a gate; **(c)** § 0's honourable fallback naming *"never a procedural register"* — a stop criterion that cannot be satisfied by quietly changing the medium.

---

## 5. Answers to the six questions as asked

1. **A real charter on its own ledger?** **Yes.** Authority table, forks, phases, RED-capable TOOLING rows, verbatim HALTs with Matt's waiver as his, exit predicate + fallback, own ledger. #80 discharged.
2. **Gates decidable?** **Yes.** One clock (1/60 s, 03- § 2.0); native ≡ screen at art step 1; crop 960×540, peak-frame gate, synchronised case, baseline measured first and printed separately; VO/CO namespaced with a RED clause enforcing it.
3. **Scale contract holds with `pixel_scale` retired?** **In substance yes — in record no.** It now depends on V2, which is **open** (BLOCK-A).
4. **Every § 7 gate names a BUILT or PROVISIONAL instrument?** **Yes**, with two silent drops (VO7/VO9, WARN-3) and one live law without an instrument (FF-08, WARN-2).
5. **Prerequisites a phase, no false £0?** **Yes.** P0-a + P0-b, owners, bursts, RED clauses, Matt checkpoints; 03- states plainly that E0 is £0 in images and not in bursts.
6. **The two reversed rulings handled?** **Yes.** V6 → both presets rendered, Matt rules on sight at E0(a)/Packet 86. V4 → conditional, R-C3-120's precondition restored, ruled at Packet 87, single disposition.

**ARCHITECT gate (§ 10).** The table is well-formed and its OPEN rows are correctly off-path — except that its first row (*"Q79 V1–V20 RESOLVED"*) is the assertion BLOCK-A contests. **The "CLEAN-or-GATED" claim does not hold as written**: V2 is open *and* on the run's path at § 2 and § 6, ahead of its named checkpoint. With V2 ruled — or restated as provisional — the gate is clean.

**Wrapper-audit exposure of the V20 waiver.** `audit.py` will **not** VOID any burst over the run cap; it never reads it. The exposure is `run_burst.py:158` (BLOCK-B).

---

## 6. Action summary

- [ ] **Matt:** rule **V2 (1 or 3)** — the last open Q79 row. *(BLOCK-A)*
- [ ] **gandalf:** if V2 is unruled at GO, restate it PROVISIONAL in § 2 / § 3 / § 10, restore E0(e) as the ruling point, re-class the `R-C5-0` V2 clause to `conductor` / `veto_open: true`. *(BLOCK-A)*
- [ ] **gandalf:** T4f (or T4a clause) guarding the run-cap gate against a waived cap, with `ledger.empty()` no longer hard-coding 250. *(BLOCK-B)*
- [ ] **gandalf:** declare EDIT = GENERATE-in-edit-mode, or mint the `BURST_RULES` row, before P0-a. *(WARN-1)*
- [ ] **gandalf:** add FF-08 CV ≥ 0.25 to T4d's clause and § 7's tripwire list. *(WARN-2)*
- [ ] **gandalf:** state VO7/VO9 out of scope; name the source and destination scene trees; reconcile Q68 G-4 against V12; restamp the Q79 queue row to v2.5; put the shipped 4.9 BH/s beside the proposed 8 BH/s on the Packet 85 card. *(WARN-3…8)*
- [ ] **jack-ryan:** ratify the CONSULT burst-class row (§ 1, § 10) — mine, not blocking, not on the run's path.

**Approval authority (ADR-002).** Every item above is documentation, record-correction or within-lane tooling, which is mine to approve directly. **One escalates to Matt: the V2 word.** Nothing else here needs him before GO.

**Gate-1 verdict: BLOCK — narrow.** Both BLOCKs are record-and-encoding defects with one-line fixes and neither touches the design. On Matt's V2 word (or a provisional restatement) plus the run-cap guard, **this charter is GO**. The five discharged BLOCKs represent a genuinely thorough revision, and § 5 is the first tooling contract in this lane that can fail.

---

## 7. References

**Under review**
- `agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` (v1.0, `d2bc7eb4f0ee`)
- `astra_test_01/burst/runs/C-5/ledger.json`

**Design authority + record**
- `agentic_orchestration/gandalf/notes/2026-09-15-vfx-workflow-architecture/03-architecture.md` (v2.5; § 2.0 units, § 4 instrument table, § 7a rulings)
- `canonical/matt_decision_needed/README.md` (Q79 row — *"V2 OPEN — one word owed"*) · `…/2026-09-15-hybrid-vfx-oracle.md` · `…/2026-08-25-youtube-frame-extraction-sourcing-class.md`
- `astra_test_01/burst/runs/C-3/ledger.json` (H-C3-2 `status: DISCHARGED`; R-C3-90/113/114/115/118/120/123)

**Lane law + instruments inspected**
- `canonical/reap-die-rise-game/painted-2d-pipeline/{mechanical-process,00-system,scene-builder-workflow}.md`
- `astra_test_01/burst/lane/{run_burst,audit,ledger,render_brief}.py` · `astra_test_01/burst/BURST_RULES.md` · `astra_test_01/burst/oracle/vfx_measure.py`
- `agentic_orchestration/gandalf/vfx-feature-registry.md` (FF-08, FF-11, FF-12; I-2, I-7)

**Prior findings this one continues**
- `agentic_orchestration/qa/findings/2026-09-15-vfx-architecture-gate1.md` (the six BLOCKs)
- `agentic_orchestration/qa/findings/2026-09-13-run-C-3-gate2.md` (H-C3-2; #75 cl. 2 and #80 — **both now closed**)

— jack-ryan, Gate-1, 2026-09-15
