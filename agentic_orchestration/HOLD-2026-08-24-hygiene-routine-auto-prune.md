# ⛔ HOLD — hygiene-audit Routine § 6.6 step 3 (auto-prune tier)

**Placed:** 2026-08-24 by knight-rider (orchestration channel; ADR-002 coordination authority)
**Scope:** `canonical-doc-format.md` § 6.6 **step 3 only** — *"auto-prunes the four-predicate-safe tier (git-rm; in-scope auto-commit)"*
**Lifts on:** jack-ryan ratification of gandalf's proposed § 6.3 clauses 4 / 4a / 5 (`⚠ SWITCH: CANON-STEWARD → jack-ryan`, gandalf commit `bdec6e1e`)
**Not a blocker for:** steps 1, 2, 4, 5, 6, 7. The judgment tier, the tracker collapse, and all three tripwires are unaffected and should keep running. **Step 4 in particular becomes MORE valuable while step 3 is held** — route anything step 3 would have auto-pruned into the Matt-ratification list instead.

---

## Why

The Routine's auto-prune tier is gated on `§ 6.3 predicate 4` (cross-repo reference check). gandalf derived, 2026-08-24, that **predicate 4 and the hygiene-Routine step 2 enumerate six surfaces to grep, and executable code is not among them.**

Predicate 1 correctly excludes code as a prune *target*. That exclusion leaked into treating code as a non-prune-*blocker*. Those are opposite roles served by one list.

**This is not hypothetical and it is not one doc.** Tranche 1b (`5fc2890b`) swept 98 already-demoted docs. Of those:

- **81** are still referenced by name
- **24** are still referenced by **executable code / config / data**
- **23 of those 24 are now homeless**

Adjudicated so far: 9 of 23. **Three Class-1 live constraints** found stranded — `substrate-expansion-decision-2026-05-17.md` § 7 (the vocab freeze; restored by gandalf this session), `vs2a-vfx-scene-needs.md` L985, `spatial-data-jsonschema.md` L477. **14 remain unopened**, and a keyword net structurally cannot see a live clause phrased without the keywords.

Two illustrative unfixed cases: `movement-speed-baseline.md` is cited by **10 engine files**. `substrate-identity-declarations-2026-05-17.md` is cited by `config/elements.yaml`, `config/ailments.yaml`, `element_biases.py`, and `resistance_matrix.py`.

## The cost, demonstrated

§ 7 was stranded for ~12 weeks. In that window three agents — rocket, jack-ryan, and knight-rider — each independently reconstructed § 7's content from its citations, **built three different and mutually incompatible versions, and the two most confident were the furthest from the text.** knight-rider relayed one of those inventions to Matt as fact. gandalf's framing, worth preserving:

> *A citation is a claim about where truth lives, and an unresolvable one converts every downstream reader into an author. A dangling pointer in a corpus that reasons does not throw an error — it invites invention.*

A register does not fix this: jack-ryan's own purpose-built `legacy-constraint-audit-2026-05-21/constraint-inventory.md` cites this document three times, inventories §§ 3, 3.1 and 5 as LC-001/012/022, **and walks past § 7.**

## Why a hold rather than a note

Step 3 is the only step that is **destructive, automatic, and recurring**. It fires `git rm` with in-scope auto-commit, unattended, into a gandalf session, on a fixed cadence, gated on the defective predicate. Every additional firing adds stranded live clauses to a backlog that currently stands at 14 unopened. The hold costs one deferred sweep; not holding costs unbounded re-instances of a failure the team has now paid for three times.

Steps 1–2 still *find* candidates — that inventory is useful and should keep accruing. Only the unattended execution is held.

## Lift procedure

1. jack-ryan ratifies, returns, or amends gandalf's clauses **4** (derive the reference check over all tracked files), **4a** (a code citation is never auto-prunable), and **5** (*liveness is per-clause, STATUS is per-document; a demotion must adjudicate the gap*).
2. On ratification, whoever lands the amendment **deletes this file in the same commit** and says so in the message.
3. If jack-ryan returns the clauses rather than ratifying, the hold stays until a replacement safety predicate is ratified. It does not lapse by default.

## Related, not gated by this hold

- **Owed to jack-ryan:** § 7.4 names a decisions-log entry as a consumption channel and § 6 cascade step 2 assigns it to knight-rider. gandalf verified **no decisions-log entry exists** for the substrate expansion or the freeze — while three *other* Matt L3 decisions from 2026-05-17 got entries that week. That single omission is the whole difference between this case and the safe-by-accident ones. Cheapest durable fix available.
- **Owed to gandalf/whoever:** 14 unopened Tranche-1b cases, declared not glossed (#70 / #76 clause 4).
- **Third-order, unowned:** `d3-path-a-archetype-composition-phase-1-p1.md` cites *"§ 5.7 — Path-a recommendation."* **§ 5.7 has never existed in any revision** of the target. A math note anchored on a section that was never written, undetectable for eight weeks because the anchor could not be resolved.

## Discipline citations

**#76** (*derive, don't hand-list*) — the six-surface grep list is instance **five**, in the governance layer, four months after instance four.
**#19.1(b)** (*claims do not inherit their verification*) — the sweep inherited the `HISTORICAL-INFORMATIVE` stamp's claim without verifying it, one layer above where the same failure was found in the citation chain. The stamp was applied on the doc's **date**; nothing the doc specifies has shipped.
**#74** — a mirror is not a remedy: `vfx_coverage_manifest.json`'s `vocab_freeze_note` mirrored § 7, went false 2026-06-01, and stayed false and unread for twelve weeks.
