# Gate 3 — Coherence-Judgment Capture Instrument (crypt-vault node PoC)

**Status:** ACTIVE — prepared while drax authors the node (background). Ready for Matt the moment the orbit render set lands.
**Author:** gandalf (design steward), 2026-06-19
**Scope:** THIS PoC node only. Not a general rubric — a single-node calibration capture. Generalization is a post-pass decision.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-19-crypt-vault-node-poc-brief.md` § 4 Gate 3
**Why this exists (brief § 4):** "Matt's verdict + REASONS are calibration samples for the eventual automated coherence judge — this is the HITL investment that removes HITL later." This instrument is the structured form that capture takes.

---

## 0. The trap this instrument is built to avoid

galadriel's CV register-pass **shipped an incoherent scene** — register (image statistics) is structurally blind to spatial coherence. So Gate 3 is NEVER a single camera angle (a single angle re-passes a broken room exactly the way the register CV did). Matt judges from the **orbit render set + walk-through if feasible** — multiple framings, never one hero shot.

Lineage note: in the descent run-to-green, the structural gate existed but was **manual** (gandalf ruling on audit-camera stills — caught the floating sanctum stair). Gate 1 in this PoC is the *automation* of that manual ruling (engine-truth). Gate 3 is the *human* layer that Gate 1 can't replace yet — "does it read as a place a human built" — and the reasons captured here are what would eventually let an automated judge approximate it.

---

## 1. The four calibrated failure-checks (pre-validated negatives)

Each of these is a **real Matt rejection** of the prior scene. They are already-validated negative samples — if the new node reproduces any of them, that is an automatic FAIL with a known reason. For each: the check, and the engine-truth Gate 1 criterion that *should* have already caught it (so a Gate-3 failure here is also a Gate-1 escape worth logging).

| # | Failure mode (prior rejection) | Gate 3 check (Matt, by eye, multi-angle) | Gate 1 criterion that should pre-catch it |
|---|---|---|---|
| F1 | ~50 identical crypts copy/pasted, overlapping each other + other objects | Are the large architectural pieces **few, deliberately placed, non-overlapping**, and do they read as intentional rather than stamped? | No structure-on-structure AABB overlap; sarcophagi grid-snapped + few |
| F2 | Doors half-hidden by walls | Is every door **fully reachable + unoccluded** — does it read as a real opening a person walks through? | Door = wall-variant cell on shared grid (cannot be half-occluded by construction); A* entrance→exit reachable |
| F3 | Second floors at mid-character height, unpassable, clipping surreally (stairs) | Is the mezzanine reached by a **real stair, at a walkable height, with clearance** — no clipping, no mid-character floors? | Vertical navigability: mezzanine reachable via stair; clearance passable |
| F4 | Overly-tall plain walls with no architectural reason | Does every wall **do a job** — enclose, divide, support, frame — or is it a blank tall plane standing for no reason? | (Partial — Gate 1 checks overlap/passability, NOT "reason." This is the gap Gate 3 covers that Gate 1 cannot. Flag F4 reasons especially — they are the richest training signal.) |

**Note on F4:** wall-reason is the criterion **least reducible to engine-truth** — it is semantic/aesthetic, not geometric. The descent grammar gate approximated it ("is it doing a job?"). Matt's F4 reasons are therefore the *most valuable* calibration samples in this whole instrument, because they're the ones a deterministic gate can't yet capture.

## 2. The positive criterion — "a place a human built"

A node can pass all four failure-checks (nothing *broken*) and still feel lifeless or arbitrary. The positive bar:

- **P1 — Spatial logic reads.** You can infer the room's purpose from its shape. A crypt-vault should read as a place where the dead were laid, not a box with sarcophagi in it.
- **P2 — Dressing supports, doesn't dominate.** Small clutter (rubble, candle-stubs) adds life and is non-repetitive; it does not become the F1 failure at small scale.
- **P3 — The footprint reads as playable.** The room is *for* something — the fight footprint + spawns read as a space combat happens in, not a diorama.
- **P4 — Register holds to the eye.** Cathedral register reads right. (This is Gate 2's quantitative job; Matt notes it here only if it reads *wrong* despite a Gate-2 pass — a register/coherence disagreement is itself a calibration signal.)

## 3. Verdict format

One of three. All three **require reasons** — the reasons are the deliverable, not the verdict letter.

- **PASS** — node reads as a place a human built; no F-checks tripped; positive bar met. → Method validated on one node. *Then* the scale conversation.
- **PASS-WITH-NOTES** — fundamentally coherent; specific refinements wanted before it's the template. → Iterate in-loop on the notes; re-render; re-judge. Does not block method-validation if the notes are polish, not coherence.
- **FAIL-WITH-REASONS** — one or more F-checks tripped, or the positive bar missed badly. → Iterate. If a tripped F-check *passed Gate 1*, log it as a Gate-1 escape (the structural gate needs a new criterion).

## 4. Capture protocol (this is the calibration data)

For every reason Matt gives — pass or fail — record the triple:

> **(criterion, specific element, what he'd want instead)**

Examples of the shape:
- `(F4, the north wall, "give it a reason — buttress it, or open an alcove; don't leave a 6m blank plane")`
- `(P1, sarcophagus layout, "reads as a place dead were laid — keep it")`
- `(F3, mezzanine stair, "lands clean now, but the run is too steep to read as built — shallow it")`

Each triple is one training sample for the eventual automated coherence judge. The corpus of triples across PoC iterations *is* the HITL-removal investment. Capture verbatim where possible — Matt's exact phrasing carries the design intent that paraphrase loses.

## 5. What I bring to Matt at Gate 3 (the consolidated package)

1. **Gate 1 result** — PASS/FAIL on all 5 structural criteria, with engine-truth evidence (AABB report, A* path, vertical-nav check, spawn-parity check). If any FAIL, the node does not reach Gate 3 — it goes back to drax first.
2. **Gate 2 result** — galadriel multi-angle register CV; HFD/LMV/LDR/SAT/HLF vs the cathedral band.
3. **Orbit render set** — multi-framing (reuse the descent `render_*.gd` orbit pattern). **Never a single hero angle.**
4. **First-draft node schema** — the substrate-led schema drax derived from the actual authored node.
5. **This instrument** — for Matt's verdict + reasons.

## 6. The line held

Nothing scales to a second node-type, no multi-node stitching, no canonicalization of the "From JSON to Seasons" architecture or katabasis grammar — until Matt's Gate 3 verdict on THIS node is PASS (or PASS-WITH-NOTES where the notes are polish, not coherence). Recognition → validate → commit: the empirical criterion that gates the architecture commit is *this node passing Matt*, not time elapsed.
