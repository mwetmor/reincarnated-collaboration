# work-cycle-skeleton — the 6-Slot Cycle Structure (cross-cutting reference)

> **STATUS:** CURRENT (load-bearing as of 2026-06-13) — first-trial. Authored to rebuild work-cycle scaffolding after the 2026-06-13 knight-rider planner-reversion diagnosis. Trial #1 was the BC-measurement keystone cycle (worked example, § 7). The skeleton is adopted ("let's try the 6 slots," Matt 2026-06-13) and will be refined as cycles run against it.

**Authored:** 2026-06-13
**Author:** gandalf (design-of-process), co-designed with Matt in Pattern B dialogue. **Handed to knight-rider for operational adoption + refinement** — KR owns the operational *use* of cycles; this doc captures the *structure* they share.
**Authoritative companions:**
- `agentic_orchestration/dispatches/README.md` — how slot-5 front-work gets issued (dispatch template)
- `agentic_orchestration/operating-procedures/critique-pair-gate-protocol.md` — Gate 1 / Gate 2, which slot 4 routes to
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` — seam-owner decision routing the skeleton assumes
- `agentic_orchestration/cycles/` — per-cycle *scope instances* (this doc is the *template* they follow)

---

## 0. What this IS and IS NOT

**IS:** the reusable six-header skeleton every work cycle follows. A fixed, shallow structure that is coherent enough for knight-rider to parse a cycle prompt and drive it, and loose enough for design/architecture to steer it mid-flight.

**IS NOT:** a per-cycle scope doc (those live in `cycles/` or, by default, embedded in KR's opening prompt — see § 6). NOT a dispatch template (`dispatches/README.md`). NOT the substantive review gates (`critique-pair-gate-protocol.md`). NOT a replacement for seam-owner authority (`hive-mind-protocol.md`) — the skeleton routes work to seam owners, it does not override them.

---

## 1. The problem this solves

**A committed dispatch has no autonomous consumer.** It is an inert document that sits until something launches it. Authoring a dispatch is not the same as the work happening.

Knight-rider has historically been a *driver* — when a cycle doc framed work as drive-to-done, he fired specialists as sub-agents and followed the work through. Without that scaffolding, he reverts to *planner* mode: author the dispatch, stop, await direction. This is not an architecture failure in KR; it is a missing-scaffold failure. The 2026-06-13 diagnosis (Matt's correction of an earlier gandalf over-diagnosis): the gap was the absent cycle structure, not KR's design.

The fix is this skeleton. It makes two things explicit that the missing scaffold left implicit:
1. **"Done" means executed, not authored** (slot 4).
2. **Where design judgment enters mid-cycle is named, not improvised** (slot 6).

---

## 2. The core principle — coherence from a fixed shallow skeleton; flex from open content

The trap is thinking *looseness comes from vagueness.* It does not. A vague cycle is exactly what makes KR revert — no done-signal, so he stops at dispatches. The old wave docs failed the other way: fully specified, coherent for KR, but *rigid* — mid-cycle design insight (a ruling, a scope reclassification) had nowhere to live, so it got lost or forced a stop-and-ask.

**The genre answer (design lineage):** this is the Path of Exile league-cadence problem, and Blizzard's Diablo seasonal model. GGG ships a league on a *fixed, shallow skeleton* (league mechanic + reusable systems + balance pass) and leaves the *content inside the slots open*. Coherence comes from the skeleton being **fixed and shallow** — few required slots, always the same ones — not from it being detailed. Flex comes from the content slots being **open**.

So: **don't make the cycle vague to make it flexible. Make the skeleton fixed-but-shallow, and leave the content open.** Slots 1–5 are KR's coherence (the fixed structure he can always parse). Slot 6 is design's flex (the open judgment slot).

---

## 3. The six slots

| Slot | Owner | What it is |
|---|---|---|
| **1. Objective** | Matt + gandalf | One sentence. The keystone / deliverable this cycle stands up. |
| **2. Critical path** | knight-rider | The dependency chain — what unblocks what. KR keeps it current as the cycle runs. |
| **3. Early wins** | knight-rider | What resolves *without* the long pole. Bank these first — they de-risk and produce signal early. |
| **4. Done = executed** | knight-rider enforces | Done means driven-through-the-early-win + Gate-routed + a live blocker-map. **NOT "dispatches authored."** The load-bearing slot — see § 4. |
| **5. Front vs pole** | knight-rider (escalates to slot 6 on judgment calls) | Which work KR drives to completion as sub-agents *this* cycle (the front); which heavy build he tracks + hands forward (the pole). See § 8 for the escalation rule. |
| **6. Flex points** | gandalf + Matt | **Named** places where design/architecture rules mid-cycle. KR *routes* to design-side here — does not pre-resolve, does not stop-and-wait. See § 5. |

---

## 4. The load-bearing slot — Done = executed, not authored

This is the slot whose absence caused the planner-reversion. State it explicitly in every cycle:

> **Done** for this cycle = the bounded front (slot 5) is **driven to execution as sub-agents**, the early wins (slot 3) are **ruled**, the work is **Gate-routed** (jack-ryan / sam per seam), and a **live blocker-map** is recorded for the heavy pole. Done is **not** "the dispatches are written."

KR enforces this against himself and against the front specialists. A specialist returning "dispatch authored" is at the *start* of the work, not the end. The driving-cycle pattern (KR 2026-06-13): *"a committed dispatch has no autonomous consumer — KR is the driver."*

What "Gate-routed" means: front-work that produces engine changes routes to Gate 2 (jack-ryan, or sam on the PC seam); design-judgment outputs route to the slot-6 owner. The cycle is not done until the gate verdict is in hand, not merely requested.

---

## 5. Slot 6 — flex points, and why the old docs failed without it

Design inputs arrive **asynchronously and mid-cycle**: a Legolas research pull returns, a substrate distribution lands and needs a ruling, a scope assumption proves wrong and needs reclassification. The old wave docs had **no home** for these. So they either got lost (the input never fed back into the cycle) or forced a stop-and-ask (KR halted the whole cycle to surface one judgment call).

Slot 6 fixes this by **naming the flex points up front**. For each, the cycle declares: *this is a design-judgment moment; KR routes it to gandalf/Matt and keeps driving the rest of the front; KR does not pre-resolve it and does not stall on it.*

Examples of what belongs in slot 6:
- An **early-win ruling** that needs design judgment (e.g., a coupling-flip decision read off a generation-time distribution).
- A **scope reclassification** (cost-discovery vs scope-amendment — a Matt call).
- A **substrate-representativeness judgment** ("is this corpus the right one to measure?" — a gandalf call).
- A **methodology-consultation hotspot** (Discipline #18 — fires before a specialist executes math at a named hotspot).

The discipline: a flex point is *routed, not guessed, and not stalled-on.* The rest of the front keeps moving while the judgment resolves in parallel.

---

## 6. Where the skeleton lives vs where the cycle content lives

Resolved in the 2026-06-13 dialogue:

- **The skeleton** (this doc) is the durable form — six headers, reusable, captured once so we stop re-deriving it every cycle.
- **Each cycle's content** is embedded in **knight-rider's opening prompt** (the fresh substance). The 2026-06-13 BC cycle proved the prompt-embed half works: Matt embedded the cycle in KR's prompt and KR drove it to execution.
- **Optional heavier form:** for a large multi-wave cycle, the content may also be captured as a `cycles/cycle-NN-<name>-scope.md` instance doc (matching the existing `cycles/` convention). Default is prompt-embed; the scope doc is for cycles big enough to warrant a durable instance record.

Best of both: durable structure (this doc), fresh substance (the prompt), optional durable instance (cycles/ for heavy cycles).

---

## 7. Worked example — the BC-measurement keystone cycle (2026-06-13, trial #1)

The first cycle run through this skeleton, populated from what actually happened:

| Slot | Content |
|---|---|
| **1. Objective** | Stand up the BC-measurement keystone — produce MEASURED Axis-4 / Axis-3B bins for the kit corpus (rocket generation → gamora simulation → BC measurement → measurement-time items 7/8). |
| **2. Critical path** | gen RUN → [early win: cogload×coupling, no build dep] ; BC build → measure → Items 7/8 → Gate 1 (reachability). Parallel: elrond faction redraw (soft-precedes gen), star-lord consume schema, jack-ryan decisions-log. |
| **3. Early wins** | The cogload×coupling distribution (Q4) — *generation-time* data, resolves without the BC build. Banked: ruled FLIP True. |
| **4. Done = executed** | KR drove elrond + rocket + star-lord to **execution** (faction table populated, 240-kit corpus generated, telemetry schema landed), Q4 **ruled**, Gate-2 **routed** (jack-ryan PASS), live blocker-map recorded. NOT "four dispatches authored" — which was the earlier stop-point that triggered the diagnosis. |
| **5. Front vs pole** | **Front** (driven to completion): elrond faction + rocket corpus + star-lord schema. **Pole** (tracked + handed forward): gamora BC build (~50%, hard unknowns resolved, full run next cycle). |
| **6. Flex points** | (a) gandalf rules Q4 [early-win gate]; (b) Matt reclassifies BC scope as cost-discovery vs scope-amendment; (c) gandalf rules "is the current corpus representative enough to measure?" → HOLD the full-run [the second-cycle sequencing call]. Each was *routed to design-side*, not pre-resolved by KR, not stalled-on. |

The cycle advanced two steps past plan (star-lord schema + a design gate closed) precisely because the early win and the flex points had explicit homes.

---

## 8. Adoption notes for knight-rider

- **Reference this doc from your OP + session-start.** When a cycle prompt arrives, map it onto the six slots; if a slot is missing from the prompt, that is the thing to surface before driving (most often slots 4 and 6).
- **You own slots 2, 3, 5 by default.** Map the critical path, identify early wins, split front vs pole — these are orchestration calls, yours to make.
- **Slot 5 escalates to slot 6 when the split hinges on a design judgment.** The mechanical front/pole split is yours. But when "what to drive next" depends on a design-side judgment — *is this substrate representative? is this the right corpus to spend the run on?* — that is a slot-6 flex point: route it to gandalf/Matt, don't pre-resolve. The 2026-06-13 BC sequencing call was exactly this: you asked the binary (drive full-run or hold?), design-side ruled HOLD on substrate-representativeness grounds.
- **Enforce slot 4 against yourself.** "Dispatch authored" is the start of the work. Drive to executed-and-Gate-routed.
- **Refine this skeleton.** It is trial #1. If a slot proves too thin or too thick across cycles, raise it — the thinness is a deliberate bet (six slots), not a law.

---

**Author:** gandalf, 2026-06-13. Co-designed with Matt (Pattern B). Handed to knight-rider for adoption. Genre lineage: PoE league cadence + Diablo seasonal model (fixed shallow skeleton, open content). Worked example: the BC-measurement keystone cycle, trial #1.
