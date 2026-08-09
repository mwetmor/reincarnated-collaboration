# KC2 Phase E — THE FINAL EMIT: everything ruled was applied, and the gates refused it

**Date:** 2026-08-09
**Author:** star-lord (export / output / telemetry / LLM seam)
**Commission:** FINAL EMIT (conductor gandalf, `RUN-CONDUCTOR`) — discharges **L-80(f)**, the emit
  checklist I authored at § 7 of `2026-08-08-kc2-f5-adapter.md`.
**Rulings applied:** **R-L80-1** (twelve forks, ledger L-80(b)) · **R-L80-2** → **L-81**
  (F5-E := SIM-KNOTS) · **R-KC2-13** (Matt, Q54) · **L-79(e)** (stale-field rule, still binding)
**Supply consumed:** `simulation/output/kc2-phase-e-actor-paths-E-s09-cp150-R-L80-2-20260809_025245.json`
  (engine `e062d058`, sha256 `303978a0…`)

> **THE BATON OF RECORD WAS NOT WRITTEN.** The gate wall runs **66 gates** and reds **four**.
> `emit()` has no override parameter. Per the commission's own instruction: HALT, report, stop.
>
> **62 / 66 green — VALIDATOR 31/32 · G-STATS 1/1 · G-E 30/33.**

---

## 1 · What I did, in the order the commission set it

① **The R-L80-1 dict, applied verbatim.** It lives in `export/kc2_baton_emit.RULING_OF_RECORD` and
the test file *imports* it, so the resolution the tests exercise and the resolution the emitter
would ship cannot become two objects. All thirteen ends resolve; `resolve_forks` is satisfied.

② **F5-E := SIM-KNOTS, and the OBJ-1 union re-law CLOSED in my seam.**
`EVENT-ROW-UNION` is now `available=False` with a `REJECTED-CLASS` consequence, so
`resolve_forks({… "F5-E-ACTOR-PATH": "EVENT-ROW-UNION"})` **raises**. The ruling is structural, not
documentary — the same treatment L-79(e) got. The re-law is on the wire twice: as the
`OBJ-1-UNION-RELAW` provenance row and as `config.arena.path_coverage`. Its text, for drax's
countersign: *`actors[].path[]` is SIM-RECORDED, VERTEX-COMPLETE; linear interpolation between
knots IS the sim's position function, not an approximation of it.*

③ **`calibration_grade: FULL` at a clean committed tree.** The mechanism is built and it WORKS —
`build_baton` refused `FULL` on my working tree with `AC-11.4e: engine_tree_state == 'dirty'`, which
is the guard doing its job on me. FULL was never claimed, because it was never earned: the emit is
refused upstream of the grade.

④ **`spec_pin` — computed, and reported here rather than emitted.**

| field | value |
|---|---|
| `spec_note` | `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` |
| `spec_sha256` | **`d1a0ad19567ad13a1a72a47b9cac7069404d0c56df5bcbf0851c70d3afe4b2d2`** |
| `charter_commit` | **`a761c357`** (supplied; verified = the Q54 / R-KC2-13 charter amendment) |
| `ledger_commit` | **`e7532a01`** (supplied; verified = the L-81 fold) |
| `pin_state` | **COMMITTED** (tracked, no working-copy modification) |

⚑ The commits are the conductor's, taken **verbatim**, not re-derived from `git log -1 -- <path>`.
A path-derived answer drifts to whatever touched the file last; the pin is a statement about which
commit the baton is pinned to, and that is a conductor fact.

---

## 2 · The knots, consumed as the MIGRATION specifies

**995 knots over 344 actors** (min 2 · median 3 · max 5). The rejected union produced **1,476**
knots carrying strictly *less* information — more points, fewer vertices.

| semantic (gamora's MIGRATION) | how I consumed it |
|---|---|
| `tick` is wave-local | I read the artifact's own `run_tick`; I never re-add a base |
| the spawn knot's `tick`/`t_s` split IS the drip | see § 3 — it is neither snapped nor smuggled |
| a 2-knot path is a MEASURED straight walk | 61 of them, and they are exactly the p05 ambush set |
| a dwell is two knots at one place, two times | never deduped on position; 12 bodies dwell 44–70 ticks |
| `kinds` may carry several | carried in the supply; not projected onto the wire (schema has no field) |
| NO heading is derived | F5-D / F5-F stay DECLARED conventions; I derive nothing from consecutive knots |
| summons have no path | **344 actors, 344 paths, zero fabricated.** An absence, per R-L53-2 |

**The supply is pinned by DIGEST, not filename.** `KNOTS_ARTIFACT_SHA256` — a regenerated artifact
is a different measurement, and loading one silently is how a baton starts carrying somebody else's
trajectory. Mismatch raises; tested.

**`path_model` — a schema question NAMED, not taken.** `ConfigArena.path_model` is
`Literal["PIECEWISE-LINEAR"]` on a drax-countersigned surface. The sim's own stronger name is
`"piecewise-linear, VERTEX-COMPLETE"`, and the strengthening is the entire difference between
SIM-KNOTS and the rejected subsample — so it ships in `path_coverage` (free text, required
non-empty by `G-LOCO-PATH`) and in the provenance row. Retyping the Literal is a signed-surface
change; I did not take it.

---

## 3 · Two things I found while wiring, both measurements

### (a) Rulings **J** and **M** INTERLOCK — and the sim's own record is now the source

`F5-M` LAST-STILL-TICK used to be *re-derived* as `ceil(spawn_t_s / period) − 1`, because nothing
recorded it. It is now RECORDED: gamora's recorder writes the spawn vertex at `tick − 1` of the
first tick the run loop actually stepped the body. **§ 11.3 forbids re-deriving a sim-owned
quantity, so the knot is now the SOURCE and the arithmetic is the CHECK** — they must agree or the
adapter raises. They agree **344/344**.

That agreement is not free. `tick_period_s(196) = 0.0816326530612245` is a **different float** from
`1/12.25 = 0.08163265306122448`, and the spec's printed pin `0.0816` is a third. Against `1/12.25`
the ceiling lands one tick late on **20 of 344** bodies — every body whose drip is an exact tick
multiple (`49 × p == 4.0` exactly under the sim's float; `49.000000000000006` under the other).
**R-L80-1 ruled J and M independently, and M is only reproducible because of J.** I found this by
writing the check with the wrong float first, which is the honest version of the story. Pinned by
`test_rulings_J_and_M_INTERLOCK_and_that_is_measured_not_assumed`.

### (b) The drip cannot ride `PathWaypoint.t_s`, and it is not being snapped

The MIGRATION says the spawn knot's sub-tick `t_s` must not be snapped to the grid. It is not — but
it also cannot travel in that field: § 11.4 **pin 4** rules `t_s` DERIVED from `run_tick` and never
a key, and the emitter recomputes every waypoint `t_s` accordingly. The drip survives as the
LAST-STILL-TICK `spawn_tick` and as an explicit **`DECLARED-BOUND-ON-DRIP`** provenance row —
`spawn_t_s` is a *bound on* the drip to within one tick (81.6 ms), which is exactly what R-L80-1(M)
said it would be. **61 spawn knots sit off the grid, by ≤ 1 tick, one-signed**; asserted by test so
the claim is measured rather than repeated.

---

## 4 · THE HALT — four reds, and they are four different things

`export/kc2_baton_emit.py` runs the wall: **32 validator checks + G-STATS + the 33-item G-E stub**.
`emit()` writes only on all-green and takes **no override**, because a flag that let a red gate
through would be the only line anyone ever used.

```
[gates] 62/66 green — VALIDATOR 31/32 · G-STATS 1/1 · G-E 30/33 — RED
[counts] {'actors': 344, 'waves': 20, 'event_rows': 1900, 'path_knots': 995, 'track_samples': 3732}
```

### H-1 · `G-LOCO-ONE-TRAJECTORY` — **NEW**, and new because the guard stopped being VACUOUS

```
events.rows[244] (damage_dealt, target=w154_a004, tick=663): emitted position (0.141, 2.535)
disagrees with the path interpolation (0.1465, 2.6285) beyond 0.002 m
```

**Mechanism, MEASURED.** `Mover.step` clips the final approach step at the engage ring:
`travel = min(v·dt, max(0, dist − d_engage))`. That is a **speed change with NO direction change**.
The knot predicate keys on direction (`1e-9` rad) plus dwell boundaries plus markers — **a speed
change is invisible to all three**, so no knot is recorded, and linear interpolation on `run_tick`
then misplaces the body on the interior tick of that leg.

**Population, enumerated not estimated.** Per-leg implied speed (`Δlength / Δtick·period`) against
each body's own maximum: **12 non-uniform legs on 12 bodies, and every single one is of class
`contact → engage+halt`.** No second class exists. Of those 12, four legs span one tick (no
interior, harmless) and eight carry an event row on the interior tick — **8 violations, max
0.154 m ≈ 77× the 1 mm position quantum**, on the exact ticks where damage was dealt.

**Why nothing else caught it.** The polyline-length check is **parameterisation-blind** — length is
invariant to how time is distributed along it — which is why it reads `max |Δ| = 2.1e-13 m` and is
still telling the truth. The determinism law compares the run to itself, so it cannot see it
either. **Only the one-trajectory guard can, and its docstring predicted this exact case:** *"If a
sim's realized motion is not reproduced by its own emitted knots, this fires — and that is the
ruling being falsified at the emitted-knot density, i.e. more knots are owed. Do not widen the
tolerance to make it pass."*

**⚑ AND THE CORROBORATION.** Under `EVENT-ROW-UNION` this guard **passed vacuously**: the union's
knots *were* the event rows, so the guard compared the event rows against a path built from those
same event rows — a tautology, 32/32, meaningless. SIM-KNOTS is the first path the guard could
actually bite on. **R-L80-2's rejection of the union is independently corroborated by the gate's own
behaviour**, which I did not expect and which I think is the most useful thing in this lap.

#### Options, with the provenance consequence of each

| # | Option | Provenance consequence |
|---|---|---|
| **1** | **CLIP-KNOT (gamora seam).** Extend the knot predicate: record a knot whenever `travel < v·dt` (a clipped step), not only on a direction change. | The only option that makes the emitted `path_interpolation` rule TRUE rather than printed. Cost is **≤ 12 extra knots on this run** (995 → ~1,007, +1.2 %; ~2 B/actor against R-LOCA-1's 357 B headroom). Requires a re-run under the R-L80-2 determinism law. The guard then passes **on evidence**. |
| **2** | **WIDEN THE TOLERANCE** to ≥ 0.16 m. | Explicitly forbidden by the gate's own docstring. The baton would assert a position the sim did not occupy, by up to 77 quanta, **on ticks where damage was dealt** — the picture disagreeing with the damage, which is the failure the whole schema exists to prevent. |
| **3** | **RE-WORD `path_interpolation`** to declare the final approach segment decelerated. | Puts a special-case motion law in a free-text field that the consumer must re-implement correctly to draw the body right. That is § 11.3's re-derivation, relocated into Godot. |
| **4** | **UNION-SUPPLEMENT (my seam).** Insert the missing interior knot from the event row's own emitted `target_x/target_y`. | Every inserted number is sim-emitted — but it repairs **only the 8 legs that carry an event row** and leaves the other 4 wrong *and unwatched*. **The gate would go green because the evidence was removed, not because the defect was.** The vacuous-pass class, one layer down. |
| **5** | **EMIT AT `PARTIAL` with the divergence on the ledger.** | Not reachable: `write_baton` refuses an invalid baton (AC-11.1). And the divergence ledger is for named divergences from the FIXTURE, not a licence for an artifact to disagree with itself. |

**No recommendation is a decision.** My reading is that (1) is the only option that leaves the
artifact honest, and it is small; but it is gamora's predicate and the conductor's call.

### H-2 · `M-7` (G-E **MUST**) — PRE-EXISTING. A **box-vs-disc** shape gap

```
scatter_model=SIM-ROLLED, 272/344 spawns inside placement_extents_m=8.0
```

`run.py` rolls `sx = ex + U(−8, +8)`, `sy = ey + U(−8, +8)` — a **BOX** of half-width
`PLACEMENT_EXTENTS_M`. The consumer stub reads `placement_extents_m` as a **RADIUS**. Measured:
**272/344 inside the disc · 342/344 inside the box**; max radial offset 11.081 m = 1.385× extents
(a square's corner is 1.414×). **The value is correct and the SHAPE is undeclared on the wire.** A
Godot loader drawing spawn markers in an 8 m circle places 72 of 344 bodies wrong.

The remaining **2** are not scatter at all: both are **p01 bodies on tier-17 waves**, displaced by
the p01 tier shift (max per-axis 8.281 m vs the 0.714 m p01 shift). **`DIV-P01-TIER` has a MEASURED
consequence on a MUST item**, not a cosmetic one — worth knowing when F5-H is revisited.

Options: **(a)** declare the shape in `scatter_model` (free-form `str`) and teach the stub the box
test — my seam, but it changes a **MUST** item on a drax-signed list at emit time, so I am
surfacing rather than taking it; **(b)** a first-class `scatter_shape` field — signed-surface schema
change, drax countersign; **(c)** leave red and emit PARTIAL — refused by the wall, and it would
ship an undeclared shape to a loader that has to draw it.

### H-3 · `R-LOCO-1` (G-E AC) — PRE-EXISTING. Five **MEASURED-still** bodies

```
995 waypoints over 344 actors; 339 actually change position, 5 span time without moving
```

The five are `w153_a023 · w156_a012 · w156_a015 · w161_a014 · w167_a017`: p05 ambush bodies that
spawned **already inside `d_engage`**, with `n_steps == 1` and `path_len_m == 0.0`. The motion law
correctly held them. The stub's predicate — "spans more than one tick and ends where it started" —
was written to catch a board **frozen at spawn** (the F-12 defect) and cannot yet tell a frozen body
from one the sim measured as still.

Options: **(a)** strengthen the predicate to discriminate — a still body whose spawn lies within
`d_engage_m` of the player at its spawn tick is *correctly* still, and that is re-derivable from the
wire, which makes the check sharper rather than looser; **(b)** leave red. **(a)** is my seam and I
believe it is right, but changing a gate at emit time is exactly the move that must be visible, so
it is here and not in the code.

### H-4 · `R-LOCO-1-HITTEST` (G-E AC) — PRE-EXISTING, and **IMPROVED 37 → 6** by SIM-KNOTS

```
32083 (actor, tick) pairs re-decided; 6 inside-the-disc-without-a-damage-row, 0 damage-row-outside
```

All six sit at **`path[0]`** — i.e. at LAST-STILL-TICK, one tick **before** the body is on the
board — and they are the six of the 61 drip bodies whose spawn lies inside the 3 m disc. A loader
replaying the path draws them inside the disc one tick early and finds no damage row. **This is a
direct consequence of R-L80-1(M)**, not a defect in the knots.

Options: **(a)** declare it — extend the emitted `path_coverage` to state that the body is not on
the board until `path[0].run_tick + 1` and MUST NOT be hit-tested at `path[0]` (the same shape as
the existing "outside the span the position is UNDEFINED" rule); **(b)** start the path at the first
live tick — collides with `G-LOCO-PATH`'s `path[0].run_tick == spawn_tick` and re-opens F5-M;
**(c)** teach the stub to skip `path[0]`. **(a)** is one sentence and costs nothing, but it is a
consumer-facing semantic on a signed surface.

---

## 5 · ⚑ CORRIGENDUM ON MY OWN RECORD — the stub figure was the fixture's

My F-5 note § 8 and MIGRATION entry `[2026-08-08]` both reported, for the **adapted record**:

> **Validator 32/32 PASS · consumer stub 33/33 PASS**

**The stub figure is STRUCK.** **33/33 is the synthetic fixture's number**, carried onto the
adapted-record line. I re-measured on the same code: the fixture reads 33/33 and the **adapted
record read 30/33 then and reads 30/33 now** — H-2, H-3 and H-4 were red at `84996d29` and nobody
saw them **because the stub was never actually run against the adapted record**. The validator
figure stands (32/32 under EVENT-ROW-UNION), though § 4 H-1 shows what that 32/32 was worth on the
`G-LOCO-ONE-TRAJECTORY` limb.

Nothing downstream consumed the wrong figure — no artifact was ever written — but it rode ledger
row **L-80** into the record, so it is corrected here and in MIGRATION rather than edited away.
**The lesson is mine and it is the discipline-#8 one:** I reported a gate result I had not run on
the object I was reporting about.

---

## 6 · What is green, so the remaining distance is exactly four things

* **Replay** reproduces the committed artifact exactly: waves 151…170, terminal
  `arena_tier_exhausted` @ 171, w151 `t_end_s` 18.449 s / 28 bodies / 6 champions.
* **344 actors · 20 waves · 1,900 event rows · 3,732 track samples · 995 path knots ·
  1,061,978 B = 1.062 MB** serialized `rows-compact` (drax's signed budget ≈ 22 MB). The F-5 note's
  1.11 MB was the union-path build; the vertex-complete path is **smaller** — fewer, better knots.
* **VALIDATOR 31/32** — every check but H-1, including `G-LOCO-PATH`, `G-CD2-POLICY`,
  `G-M24-CRIT`, `G-ARENA-REF`, `G-PRECISION` and the whole AC-11.x set.
* **G-STATS** — DECLARED and cited to its discharge at **L-68** (eHP 967/968 MEASURED, damage
  953/968, BOTH 953 = 98.45 %); this run consumes that fold through `monster_stats.ehp_lookup` and
  `player_damage_per_tick`. It is not recomputed here: recomputing another seam's gate in this one
  is the § 11.3 re-derivation the run refuses.
* **G-E 30/33 · 22/23 MUST** — `M-7` is the only MUST red.
* **Provenance complete:** `DIV-F7-WALL · DIV-F1-BAND-EHP · DIV-LEVEL-COVERAGE (176/344) ·
  DIV-WAVE-SPAN · DIV-P01-TIER · DIV-TICK-PIN · R-KC2-13-TERMINAL`, plus **eleven `DECLARATION`
  rows** — one per DECLARED-* obligation R-L80-1 imposed, including `OBJ-1-UNION-RELAW`.
* **The stale-field rule still holds structurally**: `assert_admissibility_not_artifact_sourced()`
  raises on any mapping carrying `terminal_admissible`; admissibility comes from R-KC2-13.

## 7 · Tests

`tests/test_kc2_run_adapter.py` **13 → 27**. Adapter + baton: **125 passed** (was 111).
Blast radius **enumerated** (Discipline #10): the 5 test files referencing `baton_v1` /
`kc2_run_adapter` / `kc2_baton_emit` run **186/186**.

Five of the new tests are **HALT PINS** — they assert a KNOWN-RED state (12 clipped legs of one
class; 272/342 box-vs-disc; the six hit-test offenders at `path[0]`; the union's unreachability;
the wall naming exactly four reds and 62 greens). **They are meant to break when the halt is
repaired.** A pin that survives a repair is a pin nobody updated.

---

**Refs:** L-78 / R-KC2-13 · L-79(a)(e)(h) · **L-80(b) R-L80-1 · L-80(c) R-L80-2 · L-80(f)** ·
**L-81(a)–(g)** · L-68 (G-STATS) · L-51 / R-LOCA-1 · R-L53-2 · spec § 11.3 / § 11.3.1 / § 11.4
pins 3–5 · AC-10.6 / AC-10.11 / AC-11.1 / AC-11.4e / AC-11.7c · G-LOCO-PATH ·
G-LOCO-ONE-TRAJECTORY · G-M24-CRIT · G-CD2-POLICY · OBJ-1 · Disciplines #1, #2, #8, #10, #12.

**Engine tree:** new module + adapter amendments + tests + MIGRATION + AGENT_STATE.
**The results artifact and the knots artifact were both READ, never rewritten.**
**COMMIT-ONLY, NO PUSH** (R-KC2-10 — the conductor pushes at fold).
