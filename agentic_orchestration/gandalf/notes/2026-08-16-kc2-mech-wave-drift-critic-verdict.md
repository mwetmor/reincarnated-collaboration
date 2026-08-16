# KC2 MECHANISM WAVE — DRIFT-CRITIC VERDICT

**Author:** gandalf (`DRIFT-CRITIC`) · **Date:** 2026-08-16
**Reviewing:** gamora's KC2 mechanism wave (engine `d242dd46`..`c77934a3`) against the design brief
**Spec under review:** `agentic_orchestration/gandalf/notes/2026-08-16-kc2-mechanism-wave-design-brief.md`
(sha `b3761247dc723008ab7d970aec2252288f895c0418d9e080b2d32bb065151076`) — **authored by me**, per brief § 6
**Conflict declared:** `⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC` — the framing-audit points at my own spec first
**Independent of and non-substitutable for:** jack-ryan Gate 2 (`qa/pending/2026-08-16-gamora-kc2-mech-wave-gate2.md`)

---

## 0 — Verdict

**PASS-with-design-findings.** The wave built the contract, not the number. § 4.1 held under
independent grep; decode-before-declare held in form; the § 4.3 failure list is clean on all seven
shapes; and on two points the build is *more* disciplined than the brief demanded.

**Two of the six findings below are defects in MY SPEC, not in gamora's build.** One of them
(F-1) was caught by gamora and corrected against me at his own cost, ALONE, before his repairs.
The other (F-4) is still open and lands on the PM5 charter, which I have not yet written.

**Nothing here is a BLOCK.** F-5 and F-6 are sequel-charter inputs and must not be absorbed
silently into the scene run.

---

## 1 — § 4.1 THE PROHIBITION — **HELD**

Independently verified, not read off the submission:

- **Wave commit messages** (`d0297ace..HEAD`) grepped for every quarantined figure — `3.24` /
  `3.4251` / `0.8478` / `0.19` / `0.49` / `2.83` / `14.83` / `11.5` / `rung-A` / `rung-C`.
  **Zero hits.** (The occupancy strings that appear in a wider log window are all pre-wave I-28/I-29
  commits.)
- **Every file the wave touched** grepped for the same set. Three hits, all adjudicated:
  - `simulation/kc2/run.py:3716` `"mean_occupancy": [3.2423, 3.4251]` — **PRE-EXISTING**
    (`git blame` → `6c14f384`, 2026-08-14, the I-18 limb), sitting inside a block explicitly
    stamped `⚑ referent_yardsticks` / `⚑ DIAGNOSTIC_NOT_SCORECARD`, with **assert-wall check 16**
    asserting those symbols appear in no branch condition anywhere in the simulation package.
    Quarantine by machine, not by promise.
  - `simulation/AGENT_STATE.md`, `export/MIGRATION.md` — record/lineage prose and a SQLite version
    string. Benign.
  - `scripts/…i26_spawn_structure_fold…py` — pre-wave, figures held in a named `REFERENT_NUMERALS`
    quarantine tuple.
- `law_3.moved == {}` in the findings of record, and the wave introduced **two** constants total,
  one of which is the identity (below).

**No constant in this wave was selected, swept, fitted, or sanity-checked against a referent
number.** The record PM4 earned across twenty-nine iterations is intact at the finish line.

---

## 2 — Decode-before-declare — **HELD IN FORM, with a design consequence (F-2)**

The § 3 design law offered three paths and forbade the third. Gamora took the honest path twice:

| fork | landed as | provenance |
|---|---|---|
| re-engagement latency (§ 3.1) | `LATENCY-ZERO` **= the identity — no constant exists** · `LATENCY-ALERT(latency_s)` runnable with **no default** | D-PURSUIT-TIME pattern; `UNREACHED-AA-3` / animation `0x21` named as the decode candidate |
| monster re-target cadence (§ 3.3) | `TRACK_CADENCE_TICKS = 1`, `Cited`, DECLARED-with-bound (integer ≥ 1, enforced by `MechFold`) | behavioural incumbency (the sim's finest clock quantum) + **decode absence, stated** |
| pack coherence (§ 3.3) | individual convergence; **no formation layer invented**; `distressCall` kept as a NAMED OPEN | brief's lean adopted without closing it |

Declaring latency as *the identity* is stronger than the brief asked for: a fork that introduces no
constant cannot have a constant fitted to it. Credit where it is due.

**But see F-2** — the form is honest and the *content* has a direction.

---

## 3 — § 4.3 failure-shape checklist — **CLEAN, 7/7**

| shape | disposition |
|---|---|
| occupancy in any criterion / sweep / commit message | **absent** (§ 1 above) |
| a constant justified by an outcome | **absent** — one constant, provenance = incumbency + decode absence |
| a guard that cannot fire | **handled better than specified.** `MechStateUnclassifiable` fires in 3 negative controls and is silent on every leg. And the three *structurally* unreachable states (`12 HALTED_AT_RING`, `17 HALTED_ALERT_HOLD`, `18 HALTED_AT_NODE`) are each **declared unreachable with the reason inline** rather than left quietly green. That is the correct answer to `D-I27-2`, and it is not what four prior laps did |
| crowd-shove channel silently ignored | **present and live** — `DISPLACED_CROWD` and `DISPLACED_BOTH` are both named partition rows, `DISPLACED_BOTH` deliberately NOT folded into either parent (see F-3 for the population question) |
| the orbiting vacuum, monster side | **absent** — no fixed-radius milling term exists; movers re-path at their own `characterRunSpeed` |
| an invented rule where substrate could be decoded | **absent** — acquisition left decode-resolved and un-relitigated; the undecoded items are named as decode candidates, not guessed |
| a superseded limb deleted | **absent** — `CAMP`, `CAMP_THEN_COLLECT`, `CLUSTER_SEEK` all runnable; `S-CAMP-LADDER` retained reported-never-scored |

Terminal conditions are named and enumerable exactly as § 3.1 required: `HALTED_GATE_VIEW` /
`HALTED_GATE_LEASH` / `HALTED_GATE_PURSUIT_TIME` read off the gate's **own** clause, never
re-derived. "The body stopped coming back" has a name in every case.

---

## 4 — Findings

### F-1 — **MY SPEC ASSERTED A FALSE PREMISE. The build caught it and corrected against me.** *(defect: gandalf)*

Brief § 1 row 3 and § 3.2 both asserted that the PM4 record cells ran a **camp limb** and that the
replication's player was a **pivot**. Addendum 1 (`8510e6cf`, committed ALONE, before its repairs)
refuted this empirically: the record cells have run `CLUSTER_SEEK` and been **fighters since I-16**,
pinned salt-0 travel **38.064863033 m**.

**Where my error came from:** brief § 1 imported `GL-12 / R-CPB-4` — *"the wire pins the player at
0.000000000 m across all 3,732 ticks"* — and read a claim about the **exported baton** as a claim
about the **sim record cell**. Those are different surfaces. The baton is pinned at zero; the cell
it was cut from has not been pinned at zero since I-16.

**Does the design intent survive? Yes — and it strengthens.** The true delta is
**arrives-and-dwells → drive-through**. `CLUSTER_SEEK` seeks the density centroid, *arrives, and
dwells* — a declared departure from `R-PM1-2`. That is, the record limb was running something
adjacent to the **orbiting-vacuum shape my own brief § 2.2 named as the thing to avoid**, from the
player side. Promoting `DRIVE_TO_PACK` is better justified under the brief's design law than the
brief understood. The conclusion was right for a reason I got wrong.

**Disposition:** the brief is a dated artifact and stays as written; this verdict is its
corrigendum. The correction is gamora's, not mine, and it cost him a re-execution he published
unedited. That is the behaviour the wave was supposed to demonstrate, demonstrated against the
person holding the spec.

### F-2 — **The wave built the D2/PoE contract. The referent is Grim Dawn.** *(design finding — PM5 + legolas)*

Both undecoded forks landed at the **instantaneous** end:

- re-engagement latency = **zero** (D2 Whirlwind / PoE Cyclone reading — tightest possible swarm)
- re-target cadence = **1 tick**, continuous (same reading)

Each is individually defensible and neither is fitted. But taken together the sim now runs the
*tightest re-engagement in the genre*, while the fight being replicated is **Grim Dawn**, which
ships `AlertBeforePursue` (animation `0x21`) — a reorientation beat before commit. The brief called
this a decode-first question (§ 3.1) and the decode did not happen; it was declared instead, legally.

**Player consequence, named:** zero-latency + continuous-retarget re-engagement is what a player
reads as **rubber-banding** — bodies that pivot on your heel with no tell. Grim Dawn's beat is not
latency-for-its-own-sake; it is the *readability* window that lets a melee player commit to a drive.
A pack with no tell is a pack you cannot play against, only through.

**This is the first place to look if PM5 grades occupancy *over*-tight**, and the honest fix is the
decode lap, never a knob. **Recommendation:** commission the legolas decode (`AlertBeforePursue`
length + controller re-path rate) as a **named open on the PM5 charter**, and pre-register that if
occupancy overshoots, the decode is the response.

### F-3 — **`DISPLACED_CROWD == 1` on five of five independent salts.** *(hunt — hand to gamora/jack-ryan)*

| salt | DEATH_IN_RING | DISPLACED_PLAYER_MOTION | DISPLACED_BOTH | **DISPLACED_CROWD** | WAVE_END |
|---|---|---|---|---|---|
| 0 | 48 | 23 | 8 | **1** | — |
| 1 | 76 | 22 | 13 | **1** | — |
| 2 | 23 | 6 | 2 | **1** | 1 |
| 3 | 4 | 1 | 0 | **1** | 4 |
| 4 | 12 | 5 | 5 | **0** | 1 |

Exactly 1, four salts running, across wildly different fight lengths (path 39 m → 664 m). The most
likely benign explanation is structural: under `DRIVE_TO_PACK` the player is moving on nearly every
tick, so a crowd-shove almost always co-occurs with player motion and routes to `DISPLACED_BOTH` —
leaving `DISPLACED_CROWD` a near-empty residual **by construction of the record limb**. If that is
the explanation it should be *stated*, because the brief specifically named crowd-shove-ignored as a
failure shape and a near-empty bucket is the shape that failure would also take. The distinction is
cheap to settle: run the classifier on a camp limb, where the player-motion signal is absent, and
show the crowd population opens up.

**Not a BLOCK.** The channel exists, is named, and `DISPLACED_BOTH` proves crowd-shove is being
detected. But "1, 1, 1, 1" is a number that should have a sentence attached to it.

### F-4 — **MY BRIEF'S PM5 LEAN IS INSUFFICIENT: the mechanism moved the death wave and occupancy alone will not see it.** *(defect: gandalf — and it is still open)*

The record cell's terminal, under the promoted limb:

| salt | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **death wave** | 155 | 156 | 152 | **151** | **151** |
| player path (m) | 529.8 | 664.4 | 196.3 | 39.3 | 109.8 |

**The referent died at wave 160.** PM4 replicated 151–160 faithfully in structure. Under the
mechanism bundle the sim player now dies four to nine waves earlier.

This is not a defect in the build — it is the brief's own thesis firing. § 2.1: *"Bodies in the disc
are simultaneously the threat and the health bar."* The wave restored the threat half. Whether the
**sustain** half scales with it is exactly what nobody has measured. If bodies come back and ADCtH
leech does not keep pace, the sim has traded one wrong fight (shooting gallery, no pressure) for a
different wrong fight (pressure without sustain) — and the referent's fight is *neither*: Matt
survived to 160 **with** the swarm.

**The spec gap is mine.** Brief § 7 recorded my PM5 lean as *per-wave movers-only occupancy inside
[rung-A, rung-C]*. That criterion can **PASS while the player dies at 151**. A run that reproduces
the ring but not the fight would grade green.

**Recommendation (mine to execute; the PM5 charter is not yet written):** PM5 pre-registers
**terminal wave as a first-class graded row alongside occupancy**, and the charter states plainly
that occupancy-in-band with terminal-wave-out-of-band is a **FINDING, not a pass**. Matt rules the
final criterion at prereg per D4; this is the conductor's amended lean, recorded as a lean.

### F-5 — **THE RATIFIED CAMERA WAS RATIFIED AGAINST A PLAYER WHO NEVER MOVED.** *(sequel-charter input — highest value, and outside Gate 2's reach entirely)*

The SB-1 camera of record is **`player_lock`**, offset `0.665 ×` base, stand-off `23.1627 m`,
PROVISIONAL-CANON, **two-gate eyeball PASS** (Matt verbatim: *"everything looks good"*).

It was ratified on a wire that pins the player at **0.000000000 m across all 3,732 ticks**.

Under a stationary player, `player_lock` **is a fixed camera.** Every frame Matt has ever ruled on
in this run is a static frame.

The sibling checkpoint `E-s09-cp150-mech` carries a player who travels **529.8 m on salt 0** —
inside a Crucible arena roughly eleven metres across. `player_lock` now means the camera translates
continuously and the entire world sweeps beneath it. **The successor scene run will be the first
frame this project has ever rendered with player translation in it.**

What this does and does not touch:

- **The harness survives.** WW-8a/WW-8b proved the pinhole model against the *player ground point*,
  and the offset is player-relative — so fov / offset / stand-off / anchor keep meaning what their
  labels say under translation. The `ARENA HARNESS CLEAN` verdict at +0.5% is not endangered.
- **The ratification does not survive automatically.** "Everything looks good" was ruled about a
  composition that no longer exists. Pitch 52.95° down at 23.16 m stand-off on a *driving* player is
  a different read: lateral world-sweep, occlusion churn, and a horizon that now moves.
- **The SKIRT/WALL fork acquires real load.** `GL-13`'s clip surface is pinned to the measured
  **86.915 × 85.303 m** rectangle, and I led SKIRT on the argument that the far-plane ground
  intersection is testable per frame. That test was validated on a camera that never moved. A player
  driving hundreds of metres can carry the camera toward the rectangle edge, which is precisely the
  condition Matt named — *"the void edge must never enter frame."* The guard goes from theoretical
  to load-bearing.

**Recommendation:** the sequel charter pre-registers a **camera re-ratification gate under
translation** — it does not inherit the gate-2 PASS by assumption. And the SKIRT enforcement test
re-fires against a driving player before any cell renders.

### F-6 — **The two open fork-sitting rulings now have new evidence under them.** *(sequel-charter input)*

Matt's parked fork sitting (baton § 2) holds scale-1.95 re-derivation and the wr2 mislabel
chase-or-park. Both were framed under a static camera. Under F-5 the scale question changes
character: world-scale on a *driving* camera couples to how much floor enters frame per second,
which is the same quantity the SKIRT guard watches. These should be ruled **with** the sequel
charter in front of him, not before it. Matt's own framing — *the werewolves should stand at an
honest height before you watch them re-engage* — is right, and F-5 adds: *and the camera should be
re-ratified before it drives.*

---

## 5 — What I am NOT finding

For the record, so the PASS is not read as broad:

- I did not audit the P-2 re-bind's legitimacy — that is a **process** question at the prereg/rescue
  boundary and it is jack-ryan's call, correctly flagged by gamora against himself.
- I did not verify parent immutability from bytes; jack-ryan is doing that independently.
- I did not grade any magnitude. Nothing in this verdict compares a sim number to a referent number,
  and the § 4.1 wall binds this verdict as much as it binds the build.

---

## 6 — Disposition

| # | finding | owner | rides |
|---|---|---|---|
| F-1 | brief premise false; corrected by Addendum 1 | gandalf (closed by this corrigendum) | — |
| F-2 | both latency forks landed at the instant end, undecoded | legolas decode lap | PM5 charter, as a named open |
| F-3 | `DISPLACED_CROWD == 1` × 4 salts wants a sentence | gamora | jack-ryan Gate 2 / a camp-limb control |
| F-4 | PM5 lean insufficient — terminal wave must grade | gandalf (`RUN-CONDUCTOR`) | PM5 charter; Matt rules at prereg per D4 |
| F-5 | camera of record ratified on a stationary player | gandalf (`SCENEWRIGHT`) + drax | **sequel charter — gating** |
| F-6 | fork-sitting rulings re-framed by F-5 | Matt | the sitting, held with the sequel charter present |

**Design verdict: PASS-with-design-findings.** The build honoured the brief, and where the brief was
wrong the build said so ALONE, before its repairs, at its own cost. That is the standard the wave
inherited and it kept it.

---

*Authored by gandalf (`DRIFT-CRITIC`), 2026-08-16, per design brief § 6. Independent of jack-ryan's
Gate-2 process pass; neither substitutes for the other.*
