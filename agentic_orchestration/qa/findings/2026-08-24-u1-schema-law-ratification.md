# Finding — 2026-08-24 — U-1 flight-recorder schema v1 + THE LAW (Gate G-1, RUN U1-BUILD Block B-2)

**Reviewer:** jack-ryan (DESIGN-MODE → gatekeeper)
**Severity:** **RATIFY-WITH-FINDINGS** — 6 BLOCKING (binding amendments) · 6 WARN · 8 INFO
**Target:** `gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md` § 2, § 3, § 9, § 11.2, § 12.2 (doc-level; no code existed at G-1 close — see INFO-8)
**Author of record:** gandalf (SPEC-AUTHOR) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Parallel builder:** star-lord (B-1)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #3 (cross-seam impact), #4 (decisions-log/law as truth), #5 (severity matters) · ADR-002 (tiered approval) · ADR-004 (cross-seam handoff)
**Disciplines cited:** #9 · #60 · #63 · #64 · #68 · #70 · #73 · R-L47-2 (derived-summary) · WARN-5 (derive-don't-hand-list)

---

## Verdict

**RATIFY-WITH-FINDINGS**, on the **RATIFIED-WITH-AMENDMENTS** pattern I set at `workflow-upgrades.md` § U-4 earlier today: the six BLOCKING findings are **binding amendments that ship AS PART OF schema v1**. Custody transfers to star-lord **with them attached**. The tape does not accumulate founding rows at scale until B-1…B-6 are in the writer and the validator.

**Why not a flat BLOCK.** Not one of the six findings challenges the event grain, the eight fork rulings, or the constitution. I certify all three. Every blocking finding is a **fidelity or enforcement gap between the spec's own rules and the spec's own sample rows** — six mechanical items, each a field or a validator clause. A flat BLOCK would stop a build whose design I am certifying, which is the wrong kind of blocking.

**(a) Schema v1** — event grain SOUND · eight fork rulings 8/8 faithfully embodied (three with named gaps) · founding-corpus fit VERIFIED mechanically, no coercion · honest-null and derived-not-stored **currently aspirational, not structural** — B-4 and B-5 convert them.

**(b) THE LAW** — **RATIFY as standing discipline**, with two tightenings written INTO the discipline text rather than left as recommendations: the `in v1` time-leak (WARN-2) and the unstated outbound direction (WARN-3). Landed as **Discipline #74** in `reincarnated-engine/design/working-agreement/engineering-disciplines.md`.

**Custody:** on this ratification, schema custody transfers to **star-lord** per `operating-procedures/software-factory.md` § 8 (*one schema, one custodian, many readers*). Spec § 3 + amendments B-1…B-6 = the founding version, versioned forward by him. gandalf's § 3 is thereafter a historical record, not the live schema.

---

## What I found

### Certifications (what I am affirmatively ratifying)

**Event grain is SOUND.** `unit_id`-joined event rows folded latest-governs is the *only* grain under which "derivable rather than maintained" holds — a unit-state row would require updating, which contradicts append-only. IN-FLIGHT as "START seen, no terminal event" and staleness as `now − last event` are both pure functions of the tape. `parent_id` makes the record grain-agnostic so F-3 binds only the render, exactly as § 3.1 claims.

**Founding-corpus fit VERIFIED, no coercion (INFO-1).** I re-derived rather than accepted the spec's numbers (WARN-5, derive-don't-hand-list): 30 `.jsonl` streams, **exactly one `turn.completed` each**, 1:1 with 30 `_run-log.tsv` rows, zero orphans either direction, zero duplicate job names, all `rc=0`, TSV uniformly 4 columns. Mechanical sum over the 30 usage blocks reproduces § 1 **exactly**: input **72,375,471** · cached **67,431,424** · cache-write **0** · output **259,471** · reasoning **154,000**. The five Codex usage keys map 1:1 onto the five § 3.4 token primitives with **no residue and no invention**. The schema fits this corpus.

**Fork fidelity — 8/8 embodied:**

| Fork | Ruling | Embodiment | Verdict |
|---|---|---|---|
| F-1 | ONE dashboard (Spec B extended) | § 6.1 Tier-2 cites verbatim; § 12.4 Glance card is a second *window* on the same tape, not a second dashboard | FAITHFUL + rider (see below) |
| F-2 | per-class staleness SLA | § 6.2 lane 2 references it | FAITHFUL in intent, **incomplete in schema** — WARN-1 |
| F-3 | card = verdict-bearing unit | § 3.2 `parent_id`; § 3.1 note | FAITHFUL — but CLOSE sample drops `parent_id` (BLOCKING-3) |
| F-4 | gate Tier-3 | § 6.1 tier table | FAITHFUL on *timing*; **silent on *nature*** — WARN-3 |
| F-5 | both window shapes from one substrate | § 5 SNAPSHOT + `meter_raw` preserved raw | FAITHFUL — raw-preservation is the right call; no premature normalization |
| F-6 | JSONL fleet truth; SQLite derived index only | § 4.1, § 4.2; § 12.4's Glance `state.json` fleet node is consistently a derived index | FAITHFUL |
| F-7 | hooks+snapshots, nulls honest | § 4.3 | FAITHFUL in text; **structurally weak until BLOCKING-5** |
| F-8 | committed monthly JSONL | § 4.1 | FAITHFUL — and it is what makes WARN-6's git check possible |

*F-1 rider (binding):* the § 12.4 Glance fleet card **must never render IN-FLIGHT or HEALTH**. § 12.4 already binds it to rear-view scope; I am pinning that as a constraint rather than a preference, because a stale live-lane on a push-triggered surface is precisely the desync F-1 was protecting against.

**`model_echo: null` is VERIFIED, not assumed (INFO-2).** Zero occurrences of any `model*`, `version`, `cli_version`, `reasoning_effort`, or `rate_limit*` key across all 30 streams.

---

### BLOCKING findings (binding amendments to schema v1)

**BLOCKING-1 — `row_id` is referenced but never defined.**
§ 2 defines the correction path as `corrects: <row_id>` and § 3.2 lists `corrects` as a common field. **No field named `row_id` exists anywhere in the schema.** The append-only correction path — the constitutional property that makes this a flight recorder rather than a log — is unimplementable as written.
*Amendment:* every row carries `row_id` (content-hash of the canonical-JSON row minus `row_id`, or ULID — custodian rules the form). `corrects` MUST reference an existing `row_id` and MUST carry the same `unit_id` and `event` as its target. Validator enforces both.

**BLOCKING-2 — `verdict` must not be populated from `rc`.**
§ 7 rules that verdicts enter rows **only from named gatekeepers/curators, never from the executing lane's self-assessment**. § 11.2's real-shaped CLOSE row sets `"verdict":"PASS"` on evidence that is `rc=0` alone, and § 11.3 renders **"30 PASS"** for the founding corpus. No gatekeeper judged those 30 jobs at job grain; the one judged verdict in the corpus is galadriel's **run-level** selection gate, which the spec correctly renders as a GATE row. The spec is already internally split on this — the § 11.3 scorecard line honestly reads `100% rc=0` while the SEALED line reads `30 PASS`.
*Machine evidence that rc is not a verdict:* job 01 exited **rc=0** while `01-ground_targeted_circle.err` logged `AuthRequired` transport failure and a models-cache load error. An exit code is a mechanical fact about a process, not a judgment about a work-product.
*Amendment:* `verdict` non-null **REQUIRES** `gatekeeper` non-null (validator-enforced). Mechanical exit codes live in `rc` and nowhere else. Founding rows carry `rc:0, verdict:null`. The board renders `30 rc=0`, never `30 PASS`. **Ledger S2's instruction "verdicts from `_run-log.tsv` rc only" is the defect and is retracted by this amendment** — the honest reading of that line was "nothing else is available", and the correct consequence is a null, not a PASS.

**BLOCKING-3 — the per-event field matrix is not normative, and the spec contradicts itself in both directions.**
§ 3.3 says identity axes appear "on START and CLOSE" — the § 11.2 CLOSE sample carries **none** of them (no `provider`, `lane`, `pin`, `currency`, `operator`, `seam`, `parent_id`). § 5 states *"Every CLOSE row's `currency` + `ts` + token primitives make per-window attribution a join"* — so that sample row structurally breaks payoff query #2 and the entire § 5 attribution story. § 3.2 declares `parent_id` a common field ("every row") yet the CLOSE sample omits it; § 3.4 lists `attempt` as a CLOSE field yet the START sample carries it. **Two implementers reading this build two incompatible tapes**, and § 11.2 is the executable reading a builder will copy.
*Amendment:* schema v1 ships a **REQUIRED / OPTIONAL / FORBIDDEN matrix keyed by event type**, machine-checked, and the § 11.2 samples are corrected to validate against it.
*Lean (custodian may rule otherwise, but must rule explicitly):* **denormalize identity onto CLOSE**. A CLOSE row must be self-describing, because every § 3.6 query is keyed on identity, and a join-back to START silently drops units whose START was never emitted — which § 4.3's partial-coverage design **expects to happen**.

**BLOCKING-4 — the field set must be CLOSED, or derived-not-stored is a promise, not a rule.**
§ 3.4's derived-not-stored rule is prose. Nothing prevents `cache_hit_rate` appearing on a row in six weeks. The lineage the rule cites (R-L47-2; four summary-count defects in one run) is exactly the failure mode that arrives by accretion, one reasonable-seeming field at a time.
*Amendment:* v1's field set is **CLOSED**; the validator **rejects unknown keys**; adding a field is a version bump (`v:2`) with a custodian-signed note. A name test applies at bump time: **no field may be named for a metric** (rate / pct / avg / median / total / count / duration). This converts the rule from an intention into a parse error. Discipline #60 (parse-contract CI-fail-loud).

**BLOCKING-5 — honest-null is enforceable only if a number is required to name its source.**
§ 3.5's per-landing law — *"every number in a row is reproducible from a named artifact"* — has no structural teeth, and **the spec's own sample row violates it**: the § 11.2 START row asserts `pin`, `harness`, `harness_version:"0.147.0"`, `operator`, and `currency` while carrying **no `derived_from` at all**. I verified against all 30 streams: the Codex JSONL contains **no model, version, or rate-limit key of any kind**, so `harness_version` on a backfill row is an unsourced claim about the past.
*Amendment:* (a) any row carrying a non-null cost primitive **MUST** carry non-null `derived_from`, **and the path must exist on disk** (validator check); (b) `derived_from` becomes a **LIST**, so identity claims can name their own source — `workflow-upgrades.md § U-4` is a legitimate named artifact for `pin`; (c) any identity field with no nameable source on a backfill row is **null**. This is what makes *"a null is a fact; an estimated token count is a fabrication"* structural rather than admirable.

**BLOCKING-6 — the R-B `curator` field is missing, and U-1 is its named home.**
My U-4 ratification amendment **R-B** (2026-08-24, binding) names this recorder verbatim: *"the field is the natural identity axis for U-1's flight recorder (§ U-1(a)) — capture it once, at the source"*, and *"a job whose curator field is empty is a refusal to fire"*. Schema § 3.3 has **no `curator`**. § 3.5's `gatekeeper` does not discharge it — different field, different event, different moment (GATE at judgment vs ENQUEUE at fire).
*Amendment:* `curator` is a **REQUIRED non-null field on ENQUEUE** for any vendor-lane unit (`lane` ∈ `codex-serial`, `grok-judge`, `cross-vendor-judge`). Backfill rows: null-with-declaration (the founding TSV's 4-column shape predates R-B). This is a build constraint on star-lord's durable-queue task per § U-4 Status, and **it must land in schema v1 or R-B has no home** — the "zero governance leaks" criterion stays unfalsifiable by query, which is the exact defect R-B was written to close.

---

### WARN findings

**WARN-1 — F-2's staleness SLA needs a class key the schema does not define.** *"Amber at 2× / red at 5× its class median duration"* requires a class; the schema has none. Without one, the board invents a class key at render time — **board-side derivation beyond fold-of-events, which § 6.3 forbids**. Second half: a class median needs a minimum n before it means anything; at n=1 the median *is* the unit and the SLA is vacuously green. *Recommend:* declare the class key in schema (candidate: `(lane, unit_kind)`, or an explicit `job_class`), and declare a min-n (suggest n≥5) below which the lane renders `no SLA — n=k` rather than a colour. Disciplines #63 (unmeasured is not zero), #68 (ceiling statistics).

**WARN-2 — THE LAW carries an `in v1` time-leak, and its sibling rule is weaker.** § 11.4 reads *"Zero write verbs in v1"* — a version-scoped clause on a rule meant to be constitutional. Worse, `software-factory.md` § 7 discipline (2) **read-mostly** explicitly *permits* write verbs (*"interface verbs write only through queue/ledger machinery"*). The fleet board's rule is deliberately **stricter — READ-ONLY, not read-mostly** — and unless that delta is stated, the weaker sibling gets cited later to justify the first button. *Discharged in Discipline #74 clause 3;* recommend the spec adopt the same wording.

**WARN-3 — THE LAW is directionally silent on OUTBOUND.** *"Never in the data path"* does not say which direction. This is **the same defect class as my U-4 amendment R-A**, where an override clause that failed to state its direction had a reading that put a door in the governance line. F-4's Tier-3 iOS push is literally a view emitting outbound; the spec gates its **timing** and never rules its **nature**. Once notifications exist, "auto-escalate a HALT older than 7 days" is one step away, and that step is authority. *Ruled in Discipline #74 clause 4:* outbound from a view carries **NOTICE, never INSTRUCTION**; no view output may be an input to any automated action; a push is addressed to a human and triggers nothing.

**WARN-4 — Discipline #73's board constraint is honored by the spec but never stated in it.** Verified: § 6.2 derives lanes from tape rows, the two Matt-queue files, and render-time probes; **zero** occurrences of the dispatch `Status:` field anywhere in § 6 (the doc's single `Status:` hit is its own header). The constraint is satisfied — **by omission**. But the builders read the spec, and U-1's charter half (b) still says *"cards from the dispatch files"*. *Recommend:* an explicit positive line in § 6.3 citing #73 clause 5.
*Sub-note, deliberately recorded to prevent over-correction:* the AWAITING-MATT lane parses authored markdown (`matt_decision_needed/`, `matt_to_do/`). That is **not** the #73 defect class. Those files are Matt's own ruling surface, authored by the party whose state they describe; `Status:` was authored by an agent about work a *different commit* completed. The distinction keeps the product lane alive, and it should be stated so that #73 is not later used to kill lane 1.

**WARN-5 — the board has no coverage declaration, and forward capture starts empty.** IN-FLIGHT is "START seen, no terminal event". Every unit that started before the recorder existed is **structurally invisible — including the six 2026-07-22 engine-seam dispatches that are the exhibit the lane was created for** (§ 6.2). A lane headed `IN-FLIGHT — 2` reads as a complete census. Discipline **#70** is directly on point: a source declares the population it does NOT cover before any row from it is compared. *Recommend:* every rendered lane carries its coverage boundary — e.g. `IN-FLIGHT — 2 (tape coverage begins 2026-08-24; pre-recorder units unrepresented)`. This is the difference between an honest instrument and a reassuring one.

**WARN-6 — append-only has no enforcement beyond intent.** F-8 committing the tape gives a real partial structural property — a rewrite is at least **visible** in git history — and that is worth naming as a genuine benefit of the F-8 ruling. But nothing **rejects** a rewrite. *Recommend:* a pre-commit/CI check — `git diff --numstat` on `flight/records-*.jsonl` must show **0 deleted and 0 modified lines**; nonzero fails the commit. ~5 lines, and it converts append-only from a discipline into a gate. Discipline #60.

---

### INFO findings

**INFO-1 — corpus fit verified mechanically.** See Certifications above. Re-derived, not accepted.

**INFO-2 — `model_echo:null` verified; the pin-drift tripwire has no signal on our only vendor lane.** Zero `model*`/`version`/`rate_limit*` keys across 30 streams. Two consequences worth banking: (a) the spec's declared null is honest and correct — good; (b) **§ 3.6-4's pin-drift tripwire cannot fire on the Codex lane as currently captured.** That is not a schema defect; it is a capture gap, and naming it now is better than discovering it as a permanently silent green. *Candidate future source:* probe `codex --version` at enqueue into `harness_version`.

**INFO-3 — no ENQUEUE evidence exists in the founding corpus, and "enqueue→seal" is mislabeled.** `_run-log.tsv` carries `start`/`end` only. Backfill must therefore emit **START/CLOSE and no ENQUEUE rows**; an ENQUEUE at `ts=start` would be a fabricated event. Consequently `enqueue→seal` (§ 3.6-2) is **not derivable for VFX-AB**, and the § 11.3 mock's `10.6h` cell is first-start→last-end (03:29:39 → 14:03:40 = 10h34m), i.e. a **run duration**, not enqueue→seal. Relabel.

**INFO-4 — mixed denominators inside one mock row.** § 11.3's SEALED line puts `units 30` (jobs) beside `fabrication 22/22` (URL checks) and `WARN 3.3%` (1 of 30 jobs) in a single row. Same family as the KC2-MC INFO-8 summary-count defects that bought the derived-not-stored rule. *Recommend:* every derived cell renders its denominator.

**INFO-5 — `seam` / `repo` is written as one table row.** One field or two is undeterminable from the text. Name it. Discipline #64 (referent-binding declaration).

**INFO-6 — no CANCEL/ABANDON terminal event. Reviewed and ACCEPTED as designed.** A silently-dead unit stays IN-FLIGHT and ages loudly, which is exactly the exhibit lane 2 exists for. Recorded so the absence is a ruling rather than an oversight.

**INFO-7 — the `.err` sidecars are unreferenced by the schema.** Job 01's `.err` carries real error text under `rc=0`. Since `derived_from` becomes a list (BLOCKING-5), include the `.err` for mechanical lanes: it is free evidence and it is what keeps BLOCKING-2's argument auditable years from now.

**INFO-8 — no code existed at G-1 close.** `agentic_orchestration/flight/` contains directories and **zero files** as of this writing (2026-08-24). No spot-check of `schema.py`/`SCHEMA.md` was possible. Per ledger **L-3** this is expected and code-level verdicts belong to G-2. Recorded so the absence is not later read as a pass.

---

## Rationale

REVIEW_PROCESS **#4** (the law of record is truth) drives BLOCKING-6: R-B is a binding ratification amendment that *names this schema as its home*; a schema v1 without `curator` silently orphans it. **#1** (math-before-code) drives the certifications: I re-derived the aggregate rather than accept § 1's table, per the standing **derive-don't-hand-list** instruction (KC2-MC WARN-5). **#5** (severity matters) drives the verdict shape: six mechanical gaps do not warrant stopping a sound design. Disciplines **#63/#68/#70** ground WARN-1 and WARN-5 (absence and saturation must survive the render); **#60** grounds BLOCKING-4 and WARN-6 (a rule with no parse-time consequence is a preference); **#64** grounds INFO-5; **#73** grounds WARN-4 and is my own prior ruling, which the spec satisfies. **ADR-002** places this ratification and the discipline write inside my direct authority (process/doc tier); the six amendments are schema-shaping, so they route to star-lord as custodian, not to Matt — **no ESCALATE is filed by this finding.**

## Action

- [ ] **star-lord (custodian):** land BLOCKING-1…6 as schema v1 amendments before founding rows accumulate at scale; ship the validator (closed field set, event-keyed required/optional/forbidden matrix, `derived_from`-path existence check, `verdict`⇒`gatekeeper` check); rule explicitly on BLOCKING-3's denormalize-identity lean; correct the § 11.2 samples in whatever becomes `SCHEMA.md`.
- [ ] **star-lord:** backfill founding rows with `verdict:null`, `curator:null`-declared, no ENQUEUE rows (BLOCKING-2, -6, INFO-3).
- [ ] **gandalf (spec):** adopt WARN-2/3 wording into § 2 and § 6.1; add WARN-4's positive line to § 6.3; relabel INFO-3's `10.6h`; carry the F-1 rider into § 12.4.
- [ ] **drax (gated):** WARN-1 class key + min-n; WARN-5 per-lane coverage declaration. Both are render obligations; neither unlocks before G-2.
- [ ] **star-lord or KR:** WARN-6 pre-commit append-only check.
- [x] **jack-ryan:** THE LAW landed as **Discipline #74**; schema custody transferred to star-lord per software-factory § 8.
- [ ] **Matt:** nothing required. No BLOCK is outstanding against him; the six amendments are seam-executable.

---

## Pre-registered G-2 criteria (pinned 2026-08-24, BEFORE any U1-BUILD row exists — `flight/` contains 0 files at this writing)

### Ruling on L-2 admissibility (mine, per ledger G-2 ownership)

**ADMISSIBLE, CONDITIONALLY.**

*For:* this run's own `claude-agent` lane differs from the VFX corpus on **every axis the schema claims generality over** — different `provider` (anthropic vs openai), `lane`, `currency` (anthropic-max vs chatgpt-sub), `unit_kind` mix (dispatch/run vs job), and it is the **only** available exercise of the F-7 honest-null token path and of GATE/HALT event density. Two workflows on the *same* lane would satisfy the letter of "no dashboard before receipts" and fail its intent; these two stress the schema where it is actually load-bearing.

*Against:* it is **self-capture** — the run that builds the recorder recording itself, forward-captured by the same session. The live hazard is that a schema defect and its accommodation happen in one motion, which is gate-gaming (software-factory § 6) with our own name on it.

*Ruling:* admitted, and the self-capture hazard is **converted into the sharpest available test** rather than mitigated by argument — see G2-T2. The tempting move (quietly patch the schema so the new rows fit) is exactly what is being measured. **Sequencing consequence, binding:** BLOCKING-1…6 must be discharged and the schema frozen **before** the first `workstream:"U1-BUILD"` row is written, or those amendments themselves count as churn under G2-T2.

### The tests (objective; goalposts predate the results)

| # | Test | Pass condition | Class |
|---|---|---|---|
| **G2-T1** | **Freeze precedes capture** | Committed `SCHEMA.md`/`schema.py` at a named SHA, carrying B-1…B-6, exists **earlier** than the first `workstream:"U1-BUILD"` row. Binary, checked from git. | HARD |
| **G2-T2** | **Zero accommodating churn** | Between freeze SHA and G-2 ruling: **zero** field additions, type changes, or widenings made to admit U1-BUILD rows (`git log -p` on the schema module). **Distinction pinned now:** adding a *value to an existing enum* PASSES — § 3.3 explicitly designs for it (*"U-8 needs a new enum value, not a new schema"*). Adding a *field* or changing a *type* FAILS. | HARD |
| **G2-T3** | **One validator, zero exceptions** | The same validator accepts **100%** of both workflows' rows with no per-workflow branch, no `if workstream ==`, no skip list. Any lane-specific branch in the validator **is** the schema forking. | HARD |
| **G2-T4** | **Four payoff queries run across the join** | § 3.6's four queries execute over the combined tape and return rows for **both** workstreams — honest nulls where coverage is thin (Claude token cells null per F-7), **not** a missing row. Drift tripwire must return a determinate answer, including `no signal — model_echo null on both lanes` (INFO-2). | SOFT |
| **G2-T5** | **Denominator + coverage honesty on every derived cell** | Every derived figure in generated `report.md` names its denominator and coverage boundary. Tests whether BLOCKING-2 / INFO-3 / INFO-4 defects recur **in output** rather than in a mock. | SOFT |
| **G2-T6** | **No stored metric** | Mechanical scan of the tape's key set vs the frozen allow-list: zero unknown keys; zero keys named for a metric (rate/pct/avg/median/total/count/duration). Greppable. | SOFT |
| **G2-T7** | **Orthogonality floor** (my admissibility condition, made falsifiable) | U1-BUILD rows carry a `provider`, `lane`, and `currency` distinct from VFX-AB, **and** contain ≥1 GATE row **and** ≥1 row with null token primitives. If U1-BUILD's rows turn out shaped like VFX rows, **admissibility lapses** and workflow #2 reverts to the codex-queue's first real workload. | HARD |
| **G2-T8** | **I re-derive; I do not accept a handed list** | At G-2 I compute aggregates and counts myself from the tape and compare against whatever the report claims. Any mismatch is a finding. (WARN-5 standing instruction, KC2-MC.) | METHOD |

**Failure disposition, pre-registered:** any HARD test failing → **G-2 FAILS** and the ledger's honorable fallback fires (seal at S1–S4 + Tier-1; both drax renders return to KR sequencing). A fallback seal is a seal. SOFT tests failing → WARN findings and a discharge loop; they do not by themselves fail the gate **unless a discharge attempt changes the schema**, which trips G2-T2.

**What G-2 does NOT test:** board rendering quality (galadriel, G-3), THE LAW compliance at fold (gandalf, G-4), or whether the four owner-questions are answerable (S8, the run's own seal predicate). G-2 is a **schema-stability** ruling and nothing else.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md` (§ 2, 3, 4.3, 5, 6, 7, 9, 11.2, 11.3, 12.2, 12.4)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-u1-build-run-ledger.md` (seal predicate S1–S8; L-2, L-3)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/workflow-upgrades.md` (§ U-1 charter + my 2026-08-24 build constraint; § U-4 amendments R-A…R-D)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/operating-procedures/software-factory.md` (§ 7 tier ladder + three disciplines; § 8 schema custody)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vfx-p2-dossiers/usage/` — 30 `.jsonl` streams + 30 `.err` sidecars + `_run-log.tsv` (founding corpus, re-derived here)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — **#74 written by this finding**; #60, #63, #64, #68, #70, #73 cited
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/flight/` — empty at G-1 close (INFO-8)

**Signed:** jack-ryan, 2026-08-24. The tape earns the right to be believed by refusing to say anything it cannot source.

---
---

# G-2 ruling — 2026-08-24 — schema stability across two workflows (RUN U1-BUILD, Gate G-2)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper, BLOCK authority) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Developer:** star-lord (B-1)
**Target:** freeze `a4f7a569` (2026-08-24T23:37:44Z) → capture `49d717d5` (2026-08-24T23:38:40Z)
**Criteria:** T1–T8 as pinned above, **before `flight/` held a single file**. Applied as written; not re-interpreted to fit results.
**Scope:** schema stability ONLY. Not board quality (G-3, galadriel), not LAW-at-fold (G-4, gandalf), not the run's seal predicate (S8).

## VERDICT: **PASS-WITH-FINDINGS**

**All four HARD tests PASS (T1, T2, T3, T7). Zero BLOCK. 3 WARN + 1 WARN-condition · 4 INFO.**

No finding is discharged by touching the schema — I checked that explicitly, because a discharge that edited `schema.py` would have retroactively failed T2. Every finding lands in the tape or the render.

### Per-criterion

| # | Test | Class | Verdict | Machine evidence I derived myself |
|---|---|---|---|---|
| **T1** | Freeze precedes capture | HARD | **PASS** | At `a4f7a569`: `schema.py`, `tape.py`, `SCHEMA.md`, validator, 61 founding rows — and `grep -c U1-BUILD` on the tape at that SHA = **0**. The six U1-BUILD rows first exist at `49d717d5`, 56s later. Checked from git, as pinned. |
| **T2** | Zero accommodating churn | HARD | **PASS** | `git diff --name-status a4f7a569 49d717d5` = exactly **two** paths: `records-2026-08.jsonl` (M), `report.md` (A). `schema.py` sha256 `71db1f5e3258eef0` and `tape.py` `522e201d650645af` are **byte-identical at freeze, at HEAD, and on disk**. Zero fields added, zero types changed, zero widenings — and zero enum values added either (which would have passed anyway). `git status --porcelain flight/` clean: no uncommitted accommodation hiding outside the commits. |
| **T3** | One validator, zero exceptions | HARD | **PASS** | `tape.audit()` over the live tape with default `check_paths=True`: **0 errors across all 67 rows**, both workflows, one code path. Grep for `workstream ==` / `workstream in` / `VFX-AB` / `U1-BUILD` / lane-conditionals across `schema.py`, `tape.py`, `bin/*`: the sole hit is the docstring asserting the property. `check_paths=False` exists but every production caller takes the default; it appears only in `tests/` for synthetic rows. Not a skip list. |
| **T4** | Four payoff queries across the join | SOFT | **PASS** | Both workstreams return rows in the SEALED table and the per-model scorecard. anthropic's cost cells render `— (null, declared)` / `— null on 1/1 units`: honest null, **not a missing row**. Pin drift returns the determinate `NO SIGNAL — model_echo is null on 33/33 units … a determinate answer, not a clean bill of health` — verbatim the disposition I pre-registered under INFO-2. `enqueue→seal` returns a declared non-derivable for VFX-AB **with its reason named**. |
| **T5** | Denominator + coverage honesty in OUTPUT | SOFT | **PASS-WITH-FINDINGS** | BLOCKING-2 holds at render: `30/30 rc=0` and `0/30 judged (verdict null — no gatekeeper at this grain)`. The string "30 PASS" appears nowhere. INFO-3's `10.6h` is relabeled **RUN DURATION** in-band with the reason. Every derived cell names n (`93.2% of 72.4M`, `6 WARN across 1 curation row(s)`, `100% (30/30 rc=0)`). INFO-4's mixed-denominator defect does **not** recur. WARN-5 coverage renders on the header **and** inside the IN-FLIGHT lane. Deductions: FINDING-2, FINDING-3. |
| **T6** | No stored metric | SOFT | **PASS-WITH-FINDINGS** | Tape key set = **31 distinct keys, 0 unknown** against frozen `ALL_FIELDS`; exactly **one** metric-named key: `warn_count`. Ruled below. |
| **T7** | **Orthogonality floor** (admissibility) | HARD | **PASS — admissibility HOLDS** | All three axes distinct, read off the tape not the claim: `provider` anthropic vs openai · `lane` claude-agent vs codex-serial · `currency` anthropic-max vs chatgpt-sub. **≥1 GATE row:** exactly 1 (`run:U1-BUILD` / `G-1-schema-law-ratification` / gatekeeper `jack-ryan`); VFX-AB has 0. **≥1 null-token row:** the `u1-build/B-1-recorder` CLOSE carries `rc:0`, `attempt:1`, 8 artifacts and **no token field at all** — F-7 honest-null exercised *structurally* (absent, not zero-filled). Beyond what I demanded: U1-BUILD is the only source of ENQUEUE, of a live-lane `unit_kind:"run"`, and of the **B-1 correction path** (`3e40241720e40e39` corrects `27e367fcf8fad631`) — the constitutional append-only mechanism is exercised on the live tape, not only in tests. |
| **T8** | I re-derive; I accept no handed list | METHOD | **PASS — zero mismatches** | Independently recomputed: 67 raw / **66 after corrections** ✓ · **33 units** ✓ · 31 SEALED / 1 IN-FLIGHT ✓ · token sums **72,375,471 / 67,431,424 / 0 / 259,471 / 154,000** — reproducing spec § 1 **and my own G-1 derivation exactly** ✓ · cache 93.1689% → "93.2%" ✓ · 2,412,515.7 tok-in/artifact → "2.4M" ✓ · median openai wall **239s** → "4m" ✓ · VFX span **10:34:01** → "10.6h" ✓ · 22 open decisions ✓ · `warn_count 6` substantiated by elrond's note ("6 WARN / 19 INFO") ✓. **This is the first gate in four sittings where re-derivation found no summary-count defect** (contrast R-L47-2's four in one run). |

**Tests:** `python3 -m unittest discover agentic_orchestration/flight/tests` → **45/45 OK**, run by me. `TestG1Amendments` locks B-1…B-6 individually; `TestTheLaw` locks the import ban, the no-write-verb property, and a whole-tape audit.

### Star-lord's six claims — verified, not accepted

He said his claims were intent; I treated them as such and checked each in code and in data.

1. **`row_id` = content hash** — VERIFIED. I recomputed sha256 over each row minus `row_id` for all 67: **0 mismatches, 0 duplicates**.
2. **Founding rows carry `rc`, no verdict** — VERIFIED. 31 rows carry `rc` (all 0); of the 30 VFX CLOSE rows, **0** carry a verdict. The corpus's one founding verdict sits on the CURATION row, gatekeeper `elrond`, sourced to elrond's own note. Legitimate under B-2.
3. **Per-event matrix normative** — VERIFIED in code (`FIELD_MATRIX` enforces R *and* F) and in data (identity FORBIDDEN on GATE/CURATION → exactly the 2 rows with null `provider`).
4. **Closed field set** — VERIFIED. 0 unknown keys on tape; validator rejects unknown; unit-tested against `cache_hit_rate`.
5. **`derived_from` = disk-checked list, `.err` sidecars** — VERIFIED. 66/67 rows carry it, 0 non-list, whole-tape audit with `check_paths=True` returns 0 errors — so **every named path resolves on disk**. VFX CLOSE rows do carry the `.err` sidecar (INFO-7 honored).
6. **`curator` on ENQUEUE** — VERIFIED in validator + `test_B6`. See FINDING-4: real enforcement, zero live exercise.

**The signature fact of this build:** my six amendments landed **mid-build**, and star-lord retracted his own `rc→verdict` population rather than defend it. That is the gate working as designed, and it is why T2 could pass — the accommodation happened *before* the freeze, where it is legitimate, instead of after it, where it would have been churn.

---

## Ruling on `warn_count` (routed to me by ledger L-6) — **ACCEPT-WITH-CONDITION**

**I accept the exception. I decline the rename. I close the door behind it.**

**Substance (why the field survives).** I inspected the value rather than ruling on the name. `warn_count: 6` is copied verbatim from elrond's curation note — *"26 dossier rows, 25 finding rows — 6 WARN / 19 INFO"*. It is a **curator-reported primitive, transcribed like a token count, never computed from other tape rows**. That is the class B-4 was written to *protect*, not the class it was written to forbid. The confirming evidence is negative and strong: the report **refuses** to derive a per-model WARN rate from it and says why — *"in schema v1 a CURATION row binds to a `unit_id` … the VFX curation binds to the run, not the jobs."* A stored metric would have been used as one. This one is declined at the point of use.

**Why I decline the rename.** Renaming a spec § 3.5 field would break the fork-fidelity mapping I verified mechanically at G-1, trading a real verified mapping for a cosmetic win. Wrong trade.

**The actual defect is the exception mechanism, not the field.** `METRIC_NAME_EXCEPTIONS` is a module-level tuple, and `test_B4` iterates *around* it without pinning its contents. A future custodian can discharge a B-4 failure by appending one identifier and the suite stays green — which converts my parse error back into the preference BLOCKING-4 existed to abolish. That is accretion-by-one-reasonable-field (R-L47-2), relocated from the field list to the exception list.

**CONDITION (= FINDING-C, WARN; does not gate).** `test_B4` must assert `schema.METRIC_NAME_EXCEPTIONS == ("warn_count",)` **exactly**. Adding a second exception then costs the same as adding a field: a red suite, a `v:2` bump, a custodian-signed note. The grandfather stands; the gate behind it closes. Discipline #60.

---

## Findings

**FINDING-1 — WARN — U1-BUILD's six rows are undeclared backfill.**
All six carry event `ts` from 22:59:53Z–23:38:14Z and were written at 23:38:40Z; each derives from an **authored artifact** (request doc, run ledger, dispatch file, this finding file), not from an instrumented stream. That is reconstruction, and `SCHEMA.md` § 8 uses `backfill: true` for exactly this on the 61 founding rows. `flight_record` exposes `--backfill`; it was not passed. So workflow #2 is a **second backfill**, not the forward capture L-2 described. Two consequences, opposite in sign: (a) the board cannot distinguish recorded-live from reconstructed — the Discipline #70 / WARN-5 honesty class, one level in; (b) it *reduces* the self-capture hazard I named at L-2, since no emitter was shaped to fit. So it is not an admissibility problem — but it must be **labeled**. *Action (star-lord):* append correction rows carrying `backfill: true` (the append-only correction path is already exercised on this tape — this is the mechanism working, not a rewrite), or declare the class in `SCHEMA.md` § 8. `backfill` is already OPTIONAL on every event, so **this does not touch the schema and does not trip T2.**

**FINDING-2 — WARN — the report's lanes do not partition its own units.**
33 units on tape; 31 SEALED + 1 IN-FLIGHT = **32 rendered**. `run:VFX-AB` folds to state **OPEN** (CURATION only; never STARTed under the recorder) and appears in **no lane** — and it is the unit carrying the corpus's only judged verdict. `fold()` defines OPEN; the render has no home for it. A reader who adds the lanes gets 32 while the header says 33. Cite: Discipline #70, my own WARN-5. *Action (drax + `flight_report`):* render an OPEN/UNBOUND lane, or state the residual on the header line. Render-side; no schema change.

**FINDING-3 — WARN — IN-FLIGHT mis-attributes the run's operator.**
`run:U1-BUILD` renders `operator = jack-ryan` because the lane takes the operator of the **latest** row — my GATE. The unit's ENQUEUE and START both carry `operator = gandalf`. A gatekeeper who judged one event is rendered as the owner of the run. Cite: Discipline #9 (attribution clarity). *Action (drax + `flight_report`):* take `operator` from the unit's earliest identity-bearing row, or render owner and last-actor as separate columns. Render-side.

**FINDING-C — WARN — pin `METRIC_NAME_EXCEPTIONS` in the test.** See the `warn_count` ruling.

**FINDING-4 — INFO — B-6 `curator` is enforced but unexercised.**
Zero tape rows populate `curator`; the one ENQUEUE is `claude-agent`, a non-vendor lane, so the rule correctly does not bite. Enforcement is real (validator + `test_B6`); live exercise is absent. R-B's *"zero governance leaks"* criterion becomes falsifiable-by-query only when the codex durable queue emits its first vendor ENQUEUE. Recorded so the silence is a known gap and not read as a green.

**FINDING-5 — INFO — `codex login status` is an outbound vendor-CLI invocation from a read-only view. ACCEPTED as designed.**
Discipline #74 clean on substance: zero write verbs onto the tape, zero authority, no LLM, no network module (`test_no_llm_or_network_imports_anywhere` enforces the import ban). `flight_report` writes exactly one path — its `--out` target — and nothing else, ever. But the HEALTH lane does spawn an external vendor binary. It is bounded: status subcommand, 30s timeout, failure rendered **loudly** (`probe failed: …`), `--no-probes` **declared** rather than silent. Recorded so that the first probe which is *not* a status query is visibly a new decision rather than a precedent already set.

**FINDING-6 — INFO — my own G-1 attribution error, corrected by the tape.**
G-1 attributed the corpus's one judged verdict to *galadriel's* run-level selection gate. The tape attributes it to **elrond**, sourced to `elrond/notes/2026-08-24-vfx-p2-dossier-curation.md`, which names elrond as executor and carries the verdict section. **The tape is right; my G-1 sentence was the imprecise one.** Recorded rather than quietly dropped — the standard I hold others to (Discipline #9) is not waived for the gatekeeper.

**FINDING-7 — INFO — Discipline #73 verified clean at code level.**
**Zero** occurrences of `Status:`-header parsing anywhere in `flight/`. Lane state derives from tape rows and from the two Matt-queue files via a mechanical `~~`-strike test that reads no prose. My U-1 build constraint is honored **in code**, not only in prose, and the report states the rule in-band. This is the constraint earning its keep: L-7(b) surfaced the queue-file strike defect *because* the view refused to interpret.

### G-1 WARNs discharged by this build (verified, not claimed)

- **WARN-1** — DISCHARGED in schema: `SLA_CLASS_KEY = ("lane","unit_kind")`, `SLA_MIN_N = 5`, unit-tested.
- **WARN-5** — DISCHARGED in render: COVERAGE clause on the header **and** inside the IN-FLIGHT lane, in the census-honesty wording I asked for.
- **WARN-6** — DISCHARGED: `bin/check_append_only` exists, runs, reports `0 deleted or modified`; `git diff --numstat` freeze→capture on the tape is `6  0`.
- **INFO-3 / INFO-4 / INFO-7** — all honored in output.

---

## THE SENTENCE

> **G-2 PASSES. Both drax renders are hereby OPEN.** The local fleet board and the Glance historical fleet card may both be built against schema v1 **as frozen at `a4f7a569`**, carrying forward as render obligations — none of which gates the start of work — G-1 **WARN-1** (SLA class key `(lane, unit_kind)`, min-n 5, below which a lane renders `no SLA — n=k` rather than a colour), G-1 **WARN-5** (per-lane coverage declaration), the **F-1 rider** (the Glance card must NEVER render IN-FLIGHT or HEALTH — rear-view scope only), and G-2 **FINDING-2** and **FINDING-3** (lane partition; operator attribution).

## Action

- [ ] **star-lord:** FINDING-1 (`backfill:true` corrections or an `SCHEMA.md` § 8 declaration) · FINDING-C (pin `METRIC_NAME_EXCEPTIONS` in `test_B4`). Both are tape/test-level; neither touches `schema.py`.
- [ ] **drax (NOW UNBLOCKED):** both renders. Carry WARN-1, WARN-5, the F-1 rider, FINDING-2, FINDING-3.
- [ ] **gandalf (conductor):** fold this ruling; FINDING-4 rides to the Step-2 queue wave as the first live `curator` exercise.
- [x] **jack-ryan:** G-2 ruled. No ESCALATE filed — every finding is seam-executable within ADR-002.
- [ ] **Matt:** nothing required by this gate.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/flight/` — `schema.py`, `tape.py`, `SCHEMA.md`, `records-2026-08.jsonl`, `report.md`, `bin/flight_record`, `bin/flight_report`, `bin/normalize_vfx_corpus`, `bin/check_append_only`, `tests/test_flight.py`
- Commits `a4f7a569` (freeze) · `49d717d5` (capture)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-u1-build-run-ledger.md` — L-2, L-5, L-6, L-7
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-08-24-vfx-p2-dossier-curation.md` — the `warn_count: 6` source of record
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #9, #60, #70, #73, #74

**Signed:** jack-ryan, 2026-08-24. The goalposts were pinned before the field existed, and they did not move. The schema held.
