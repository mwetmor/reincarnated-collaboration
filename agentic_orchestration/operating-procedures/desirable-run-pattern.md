# The Desirable Run Pattern — the shape of the two best autonomous runs

> **STATUS:** DESIRABLE PATTERN (guidance) — explicitly **NOT a protocol, NOT a gate** (Matt ruling 2026-07-21: codify *"a generalized version … as a desirable run pattern — NOT a canonical autonomous-run-charter protocol"*). Deviating from a pattern is a judgment call to be named; violating a protocol is a violation. This is the former kind of document.
> **Born from:** Run A (Atlas derivation → Edition-I freeze, 2026-07-14/15, charter + preregistration) and Run B (VDM-1 corpus verify+dossier+map, 2026-07-18/19, charter R-1..R-9) — Matt 2026-07-21: *"two of our best runs — EVER."* Comparative verdict: gandalf session 2026-07-21 (D1 ruled: `RUN-CONDUCTOR` role-tag added; D4-modified ruled: this doc).
> **Author:** gandalf. **Maintained by:** gandalf (pattern-observations from future runs amend it).
> **Amended 2026-07-23:** §6 added — first failure-lap observations (KIT-FIDELITY, Matt-ruled FAILED at KFL-27; glance prod freeze).
> **Amended 2026-08-08:** §6.5 added — value-set sweep law (KC2-SIM in-run BLOCK harvest; jack-ryan ratified-as-amended, KC2 ledger L-49(d)).

---

## §1 — The generalization (what "concrete corpus" and "concrete target-state" really were)

**"Concrete corpus" generalizes to BOUNDED SUBSTRATE** — a finite, enumerable, inspectable body of ground truth that **exists and is frozen at launch**. Forms it can take: a research corpus, DB tables, a telemetry run-set, datamined game tables, an asset catalogue, a scene inventory, a spec folder, a backlog of queue rows. The test: **you can count it, list it, and diff it.** The run transforms or derives from its substrate; it never invents its own domain mid-run — discoveries beyond the substrate are logged as findings/admissions for the *next* lap, never silent scope growth. (This is the substrate-led discipline wearing run clothes: the substrate votes.)

**"Concrete pipeline/engine data to author towards" generalizes to DECIDABLE TARGET-STATE** — a predicate over named artifacts that **the run itself can evaluate without Matt**: counts reach N; pre-registered gates pass/fail under pinned decision rules; pages serve; schemas hold under assert; a registered prediction resolves. The test: **"done" is a fact the run can check, not a quality feeling.** Where doneness genuinely requires judgment, that judgment was converted *pre-launch* into either (a) a pinned decision rule the run applies, or (b) a named Matt commitment-boundary the run halts at.

**The compressed truth:** a desirable run is a **total function over a finite domain with a decidable codomain.** That is *why* such runs terminate at the desired outcome: the domain is finite and the codomain is checkable. Historically-stuck runs were partial functions over open domains ("improve X until it holds") — their non-termination was structural, not behavioral.

## §2 — The seven elements (generalized from what Runs A + B shared)

| # | Element | Generalized form | Run A instance | Run B instance |
|---|---|---|---|---|
| 1 | **Bounded substrate** | finite, enumerable, frozen at launch; substrate votes | 13-coordinate register + ~500-kit corpus | 574-kit mobile corpus |
| 2 | **Decidable target-state** | artifact predicate checkable in-run | four gates + freeze criterion + fallback | verify/dossier/map counts + hard date |
| 3 | **Elicited charter** | decision-space pre-drained BY the conductor FROM Matt (ELICITOR grill → rulings R-1..R-n) — **intent residency**: the charter's author conducts | charter "elicited through Matt grill-session" | charter v1 ratified, R-1..R-9 |
| 4 | **Pre-registered gates + honorable fallback** | goalposts pinned before results; a gate FAIL is a *processable finding*, not a terminal event | prereg v1.1 (params, seed, decision rule); Gate-B FAIL → Finding F-1 | contradiction ledger (12 CONTRA logged as era-family findings) |
| 5 | **Declared Matt interface** | Matt names his own interrupt surface pre-launch; in-run rulings recorded **veto-open** | taste cuts + freeze reserved to Matt | R-8(b): review book at end, red-flag pings only; push-as-you-go |
| 6 | **Design authority resident in-run** | the conductor legitimately rules at *reasoning-boundaries*; *commitment-boundaries* still HALT to Matt (see §4) | Gate-B diagnosis + proposed reclassification | crosswalk + stale-flag dispositions |
| 7 | **Seam execution** | sub-agents do owned work in their seams; conductor writes no production code; existing machinery (dispatches, Gate-2, decisions-log) reused | elrond pipeline (zero amendments); jack-ryan Gate-2 | elrond schema / legolas crawl / jack-ryan gates |

### §2.1 — Conductor-economics corollary (Matt directive 2026-07-21; sharpens Element 7)

The conductor's foreground processing (Matt's session-level max-effort config — the launcher owns it; never pinned here) is spent on **course**, never **pieces**:

- **Course (foreground):** charter intent, fork detection, in-run rulings, sequencing, drift judgment, synthesis, small conductor-seam artifacts (ruling ledger, queue rows, notes).
- **Pieces (named sub-agents):** every substantial work-product routes to a NAMED agent in its owning seam — seam expertise + fresh context window + the seam's discipline stack loads with the name. Pieces belonging to the conductor's own seam route to the **named `gandalf` sub-agent** (agent-file model pin governs; no override) — never to an unnamed general-purpose spawn, which has no seam home in the accountability graph.
- **Reconnaissance exception:** mechanical read-only sweeps (file inventory, grep census, existence checks) may use Explore-class; output is evidence for the conductor, never a durable artifact.

Rationale: the conductor's scarcest resource is foreground context — burning it on piece-work degrades late-run judgment (the historical long-session failure), while unnamed spawns leak governance (no role file, no OP, no state, no attribution). Runs A + B did it this way; this corollary names what they did. Full routing table: `operating-procedures/gandalf.md § 4.10`.

## §3 — The fit test (run-fitness router)

Ask four questions of any proposed autonomous run:

- **F1 — Enumerable?** Can you count/list/diff the domain at launch?
- **F2 — Decidable?** Can the run check "done" without Matt?
- **F3 — Pre-drainable?** Can an ELICITOR pass convert the foreseeable forks into rulings/decision-rules up front — and are the residual forks *reasoning*-boundaries rather than *commitment*-boundaries?
- **F4 — Authority-resident?** Does the conductor legitimately hold design authority for the residual reasoning-boundaries?

**All four YES → desirable-pattern autonomous run** (gandalf `RUN-CONDUCTOR` conducts; ARCHITECT gates the launch).
**F1/F2 NO** (open domain or judgment-doneness) **→ bounded interactive session** with Matt present.
**F3 NO because forks are commitment-dense** (taste, naming, keystone story calls) **→ ELICITOR grill / Pattern-B dialogue**, not a run.
**Fork profile technical-not-design** (construction against frozen specs; forks resolve in-seam) **→ spec-frozen build wave** (KR-conducted / bounded; disposition of KR's autonomous lanes = open ruling, see queue).

## §4 — The halt taxonomy (the distinction that separates the two run histories)

- **Commitment-boundary HALT — correct, keep forever:** Matt-reserved territory (taste cuts, freezes, charter amendments, his named halt rules), jack-ryan Gate-2 BLOCK, committed-truth conflict (decisions-log contradiction), external-state danger. Runs A/B halted at every one of these. The 2026-07-09 E2 conservation HALT was *this kind* — discipline succeeding, not a run failing.
- **Reasoning-boundary HALT — the failure this pattern eliminates:** an unanticipated fork that needs *design judgment against canon*, not Matt's reserved authority. In the desirable pattern these are ruled in-run (veto-open, logged), with the run's own gates + jack-ryan as checks. Gate-B (Run A) is the founding exemplar: a pre-registered gate FAILED, was diagnosed, reclassified as a published finding under independent Gate-2 review, and the run continued to its outcome — the event class that formerly killed runs became a *finding*.

## §5 — Standing safeties (what kept proposer-and-judge concentration safe; carried into `RUN-CONDUCTOR`)

1. **Preregistration** — the run cannot move its own goalposts (pinned before results).
2. **Independent Gate-2** — jack-ryan review of in-run reclassifications, byte-for-byte on evidence.
3. **Reserved ratification points** — Matt's commitment-boundaries declared in the charter, never inferred.
4. **Veto-open ruling ledger** — every in-run ruling recorded with Matt's one-word veto open; the existing `⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC` beat applies when the conductor judges work against a spec the conductor authored.

---

## §6 — Pattern-observations from run events (first failure lap: KIT-FIDELITY 2026-07-23 + the glance freeze; first in-run BLOCK harvest: KC2-SIM 2026-08-08)

The header promises that "pattern-observations from future runs amend it." This is that mechanism firing for the first time — and it fires from a **FAILED** run, which is worth saying out loud. Runs A and B (§1–§5) were the two best runs ever; they taught the shape. KIT-FIDELITY was the first run conducted *in* that shape that Matt ruled FAILED (at KFL-27), and a pattern that only learns from its successes is a pattern that certifies its own blind spots. These four observations are what the failure taught. Lineage lives in `agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-wind-down.md` (failure taxonomy §1 + conductor lessons §5) and `agentic_orchestration/gandalf/notes/2026-07-23-glance-restore-run-charter.md`. They are guidance in the same key as §1–§5 — deviations are judgment calls to be named — but they carry the weight of having been paid for.

**1. Coverage-gates before accuracy-gates (fidelity runs).** KIT-FIDELITY gauged byte-exactness on the JOINED fraction while never gating what fraction of the watched surface was source-joined at all. The byte-chain lock was real — corpus Fire Ball 242.5 → compiled EXACT → frame `expected_premit 637.775` to the third decimal → scene renders zero-derivation. And it certified a sliver: the camera showed 40/41 synthetic entities (mob-harvest gap), player HP unjoined, a compiler-default Meteor cost, and a flagship kit that never cast its signature skill. For any fidelity/twin run, the FIRST pre-registered gate is **coverage** of the watched surface (entities, skills, stats, behavior); accuracy on the joined part comes second. Run them in the wrong order — as this run did — and you certify a sliver and call it a twin.

**2. Owner-eye checkpoints are pre-registered mid-run gates for presentation-surface runs.** Both KIT-FIDELITY catches were Matt's, mid-stream, unprompted — the declared Matt interface had put his eyes only at the END (the watch brief). When the run's output is a watched surface, the owner's eye is not a briefing recipient; it is an **instrument of record**. The run's own gates said green twice and his eyes said otherwise both times, and his verdict governed. Schedule the owner's eye as a gate, at named mid-run points, *before* downstream gates build on unviewed state — the same way §2 Element 5 declares the Matt interface, but placed at checkpoints rather than only at the end.

**3. Rubric law.** A VERIFIED claim must name its rubric AND show that rubric is the OWNER'S question, not a narrower proxy. KIT-FIDELITY logged "verified" twice on narrower rubrics — data-honesty at KFL-22, five-facts-green at KFL-26 — while the owner's question was twin-fidelity. Every exit predicate was formally met and the run still failed at the owner's eye, because the predicates measured a narrower thing than the intent. Decidability bought by predicate-narrowing is **intent leak**: it is the failure mode of F2 (§3), where making "done" checkable quietly swaps the owner's question for a checkable proxy. At launch, diff the predicate set against the charter's §0 intent sentence and name what fell out — out loud.

**4. Red-main tripwire.** Any run that pushes to a CI-gated or deploy-gated surface carries a post-push **pipeline-green + deploy-truth** gate in its EXIT predicate. The run is not done at push; it is done at **verified serving truth**. This one was born not inside KIT-FIDELITY but from the glance freeze that the GLANCE-RESTORE charter exists to repair: a push left the glance parse-contract red on main and Vercel prod silently frozen at `e5ea8584` (2026-07-22 15:41 UTC) for ~30 hours, because no run's exit predicate owned the deploy. Green-on-my-machine and pushed is not served. The GLANCE-RESTORE charter's G4 is the first application of this gate — applied, pointedly, to ourselves.

**5. Value-set sweep law (born KC2-SIM 2026-08-08 — from a Gate-2 BLOCK the run survived; ratified-as-amended by jack-ryan, KC2 ledger L-49(d)).** When an in-run ruling changes a value or state-name that other surfaces restate, the landing fold owes a whole-file sweep of every consuming surface: enumerate the old value's spellings case-insensitively INCLUDING prior state-names-as-values; declare `(surface, owner)` pairs and hand back hits you may not edit; discharge by hit table, never assertion; give every benign hit a one-clause reason. Each clause was paid for by a measured miss: the founding BLOCK (D2-1) was four stale sites the landing fold had walked past; the extension clause caught two live-tense sites the value-only patterns missed; the hand-back clause exists because the next residual (R-3) sat in a seam the sweeper could not edit; the hit-table clause exists because the one discharge-by-assertion on record (L-43(f)) was false. The event class matters to the pattern: a Gate-2 BLOCK (safety #2) became a standing method plus three ratified amendments while the run continued to its outcome — the §4 reasoning-boundary machinery processing its own audit findings. Operational form: `operating-procedures/gandalf.md § 4.11`. A fifth recurrence graduates it to an engineering-discipline candidate (Matt surface, via jack-ryan).

---

**Signed:** gandalf, 2026-07-21. The pattern, not the conductor's name, is the exportable asset — the conductor matters because the conductor must hold the charter's intent natively and its design authority legitimately.

*§6 appended 2026-07-23 (gandalf, `RUN-CONDUCTOR`) — first failure-lap observations; jack-ryan ratification queued per `canonical-doc-format.md § 6.7`.*
