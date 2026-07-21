# The Desirable Run Pattern — the shape of the two best autonomous runs

> **STATUS:** DESIRABLE PATTERN (guidance) — explicitly **NOT a protocol, NOT a gate** (Matt ruling 2026-07-21: codify *"a generalized version … as a desirable run pattern — NOT a canonical autonomous-run-charter protocol"*). Deviating from a pattern is a judgment call to be named; violating a protocol is a violation. This is the former kind of document.
> **Born from:** Run A (Atlas derivation → Edition-I freeze, 2026-07-14/15, charter + preregistration) and Run B (VDM-1 corpus verify+dossier+map, 2026-07-18/19, charter R-1..R-9) — Matt 2026-07-21: *"two of our best runs — EVER."* Comparative verdict: gandalf session 2026-07-21 (D1 ruled: `RUN-CONDUCTOR` role-tag added; D4-modified ruled: this doc).
> **Author:** gandalf. **Maintained by:** gandalf (pattern-observations from future runs amend it).

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

**Signed:** gandalf, 2026-07-21. The pattern, not the conductor's name, is the exportable asset — the conductor matters because the conductor must hold the charter's intent natively and its design authority legitimately.
