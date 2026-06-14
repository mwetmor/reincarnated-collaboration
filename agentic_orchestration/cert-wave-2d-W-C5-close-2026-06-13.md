# W-C.5 Close-Acknowledgment — Coverage Audit Settled; Arity = 8; W-D Scope Bound

**Type:** wave-orchestration close-acknowledgment (knight-rider)
**Date:** 2026-06-13
**Author:** knight-rider
**Authorized by:** Matt 2026-06-13 (cert-wave sequence approval + two sharpenings)
**Wave:** 2D combat-sim certification wave (`canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` § 5, phase W-C.5)
**Purpose:** formally close W-C.5 (it landed across prior sessions — it is NOT new dispatchable work) and bind both halves of its output into the downstream wave.

---

## 1. W-C.5 is COMPLETE — both halves landed

W-C.5 (coverage-audit + Bucket-B ruling — settle the axis-surface arity) does not need to be dispatched. Its
deliverables landed 2026-06-13 and are confirmed on disk:

| W-C.5 deliverable | Artifact | State |
|---|---|---|
| Gen-surface inventory (levers→axes; Bucket A build-state + Bucket B) | `reincarnated-engine/src/reincarnated/generation/notes/bc-measurement-coverage-audit-2026-06-13.md` (engine `230366e`) | DONE (rocket) |
| Sim-side measurement-wiring inventory | `reincarnated-engine/src/reincarnated/simulation/math/bc-measurement-coverage-audit-sim-side-2026-06-13.md` (engine `547d54e`) | DONE (gamora) |
| Structural read of the 6 unmeasured axes (predicted-vs-measured discriminator) | `agentic_orchestration/gandalf/notes/2026-06-13-bc-predicted-vs-measured-structural-read.md` | DONE (gandalf) |
| **Bucket-B ruling** (the design call the audit routed to gandalf) | `agentic_orchestration/gandalf/notes/2026-06-13-bc-bucket-b-unaxised-rulings.md` (+ Matt-flagged premise correction, commit `36cd75a`) | DONE (gandalf) |

## 2. Half one — ARITY = 8, RATIFIED (not presumed)

The Bucket-B ruling resolved all 5 post-lock unaxised features to **ZERO new axes** (4 captured by the lock's
cross-axis hybrid-capture machinery; COMPANION split — proxy→Axis 2A, meta-identity→outside/Earth-meta). The
oracle v1.1's open "8 or 8+N" arity question therefore resolves to **8**, and it is now *ratified by the audit*
rather than presumed by the May-20 lock.

**Consequences locked:**
- **W-D wires/measures an 8-tuple** (no growth).
- **Oracle § 5 reference-kit set stays at 6 — NO 7th kit.** The oracle's contingency ("the reference-kit set
  grows a 7th kit if Bucket-B promotes an axis") is **moot** — nothing was promoted.

## 3. Half two — THE SECOND AUDIT FINDING, bound into W-D scope (Matt directive 2026-06-13)

The audit's other half (the one the wave table did not foreground): the sim's measurement pipeline
`bc_measurement.py` computes a bin for **only Axis 4 + Axis 3B (2 of 8)**. The other six coordinates
(Axis 1 / 2 / 2A / 2B / 3A / 5) are binned on generation-stamped **predicted** labels — MAP-Elites currently
culls on predicted coordinates for 6 of 8 axes. Verified by gandalf's structural-read note (independent grep:
exactly two `assign_axis*` functions in `src/`; no `assign_axis{1,2,2A,2B,3A,5}` anywhere).

**Matt's binding directive (verbatim intent):** *"W-D is 'build measurement for six axes,' not 'wire the tuple.'
Otherwise the MEASURE cert (oracle § 6.2 cond. 4) can't pass."* — **ACCEPTED.** W-D is a measurement-BUILD
phase, not a plumbing/wiring pass.

**Precision (from the ratified structural read — prevents the inverse over-scope error):** of the six unmeasured
axes, the discriminator splits them — do NOT build measurement for all six uniformly:

| Subset | Axes | Mechanism | W-D treatment |
|---|---|---|---|
| **Composition-determined (SAFE — predicted ≡ measured)** | **Geometry (2)** fully; **range-half of Engagement (1)** | A (mechanic selection — closed loop) | **Confirm** from spatial telemetry (cheap read-back; wired, not default-valued). No measurement-reduction build needed. |
| **Behaviorally-realized (AT-RISK — predicted is a proxy that diverges)** | **Proxy (2A)**, **Resource (5)**, **mobility-half of Engagement (1)**, **Tempo (3A)**, **Control (2B)** [lower confidence] | B/C (stat objective / fight-dynamics realization) | **BUILD** genuine measurement-reduction from spatial telemetry — the Axis-4-bridge pattern, applied to each. This is the heavy work. |

Three of the at-risk axes (proxy 2A, charge-stack 5, mobility 1) are the **confirmed ORPHAN-measure bugs** the
coverage audit already found — same phenomenon, the bugs are the confirmed instances of the general shape.

**Net W-D scope statement (for the W-D dispatch, authored post-spike):** W-D computes the full 8-tuple from
*spatial* telemetry — confirming the 2 composition-determined axes (Geometry 2, range-half of Engagement 1) and
**building measurement-reduction for the ~4.5 behaviorally-realized axes (2A, 5, mobility-half of 1, 3A, 2B)** —
so that every axis is **wired, not default-valued** (the Bucket-A check, on the spatial seam) and the identity
authority can mint a `CommitGradeVerdict`. The structural-read note is W-D's scoping authority; it is
priority-ordered by build identity there (Axis 2A priority-1, Axis 5 priority-2).

## 4. Parked design fork (does NOT gate the cert wave)

The Bucket-B ruling surfaced one open fork: **is PHASE_MOMENTUM's "phase" intended to confer untargetability?**
(rocket/gamora build-intent question). If yes, it gains an Axis-4 avoidance identity that lands on the lock's
deferred iframe/stealth path — the next avoidance sub-mechanism after the (now-shipped) evasion bridge. **Parked;
not on the cert-wave critical path.** Likewise GEOMETRY_PROPAGATION's corpse-cascade identity is a future
gamora spatial-engine + spatial-archive question, OUT of cert-wave scope (cascade unbuilt in both engines).

## 5. W-C.5 wave-table status

**W-C.5 = CLOSED.** Exit gate satisfied: axis-surface arity LOCKED at 8; oracle § 5 reference-kit set
unchanged (6, no 7th); the six-axis measurement gap bound into W-D scope per § 3. W-D is unblocked on the
arity/coverage axis (it remains blocked on W-C delivering a working spatial engine).

---

**Signed:** knight-rider, 2026-06-13
**For:** closing W-C.5 against the artifacts that already landed, ratifying arity = 8, and binding the second
audit finding (6-of-8 axes binned on predicted labels) into W-D as a measurement-BUILD scope — refined by the
structural read so the build targets the behaviorally-realized axes and confirms-not-rebuilds the
composition-determined ones.
