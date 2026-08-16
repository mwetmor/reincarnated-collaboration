# SIM-ARC HANDOFF 2026-08-16 — THE BATON-INSERTION DECISION POINT

**Author:** gandalf (`ELICITOR`, sim-side sequencing), closing the window that fired both post-wave reviews and drained the sequel-charter forks down to one unmade ruling.
**Purpose:** the next session resumes from **this note + disk**, not from any prior conversation. Disk governs.
**Companion batons (read alongside):** `2026-08-16-sb1-session-handoff.md` (SB-1 / Godot arc — HELD by Matt this window) · `agentic_orchestration/skill_handoff_2026-08-16.md` (KC2-PM4 seal).
**Queue row:** `canonical/matt_decision_needed/README.md` **Q59**.

---

## 1. WHAT LANDED THIS WINDOW

### Both post-wave reviews fired and returned. No BLOCK. Submission CLEARED.

| Review | Seat | Verdict | Record |
|---|---|---|---|
| **Gate 2** | jack-ryan (named sub-agent, background) | **PASS-with-findings, NO BLOCK** — 5 WARN / 3 INFO | `qa/findings/2026-08-16-gamora-kc2-mech-wave-gate2.md` @ `af978752`; submission moved to `qa/pending/…-gate2-CLEARED.md` |
| **DRIFT-CRITIC** | gandalf (foreground, this seat) | **PASS-with-design-findings, no BLOCK** — F-1..F-6 | `gandalf/notes/2026-08-16-kc2-mech-wave-drift-critic-verdict.md` @ `b1277bb6` |

Both commits pushed. Engine repo current at `c77934a3`.

**Two of the six DRIFT-CRITIC findings are defects in MY OWN SPEC** (F-1 false camp-limb premise, corrected by gamora's Addendum 1 before repairs; F-4 the PM5 lean that grades occupancy but not terminal wave). F-4 is **still open** and lands on the PM5 charter, which is not yet written.

**§ 4.1 (Law 3 / the prohibition) independently verified from this seat**, not trusted from the submission's prose: every wave commit and every wave-touched file grepped for all eleven quarantined figures; the single live hit (`run.py:3716`, `mean_occupancy: [3.2423, 3.4251]`) `git blame`s to `6c14f384`, **2026-08-14, PRE-WAVE**, inside a `⚑ DIAGNOSTIC_NOT_SCORECARD` block whose quarantine is machine-enforced by assert-wall check 16. Adjudicated benign.

### The substrate finding that re-shaped the forward path

I told Matt early in this window that Gate-2/DRIFT-CRITIC/the star-lord rider "don't gate the sequel." **That was wrong, and I verified it wrong before grilling on it.** Two facts from disk:

1. **No baton exists for the mech cell.** `~/Games/reincarnated-engine/src/reincarnated/output/` holds batons only for `pm4-i2 / i6 / i14 / i16 / i18` cells, all cut on `E-s09-cp150`. Nothing carries the mechanism.
2. **The Godot scene has never consumed a PM-era baton.** `~/Games/reincarnated-godot/scripts/kc2_baton.gd:57` hard-pins
   `kc2-baton-v1-E-s09-cp150-20260809_052836.json` — dated **2026-08-09**, predating PM1/PM2/PM3/PM4 entirely.

So the scene has no consumable artifact containing the mechanism. That is the gap the forward sequencing has to close, and it is why Matt's reframe — *"finish the sim run to get to the baton, hold the Godot side"* — is the right target.

### The checkpoint (the substrate everything downstream reads)

`~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json`
**sha-256 (re-hashed from bytes this session, DO-NOT 8):** `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b`
*(An earlier in-session transcription of this digest read `…bf3bd888b968…`. Wrong. The line above is the byte-truth; anything pinning the other string is stale.)*

`sibling_of: E-s09-cp150` · `layer: SIM-SIDE cut` · parent verified byte-unchanged 20/20 PRE and 20/20 POST · inertness proven (recorder-off payload == recorder-on payload == P-5 pin `f5ec56ea…`). Per-cell:

```
salt0 | re-entries 20 | path 529.8 m | death_wave 155 | DEATH_IN_RING 48, DISP_BOTH  8, DISP_CROWD 1, DISP_PLAYER 23
salt1 | re-entries 28 | path 664.4 m | death_wave 156 | DEATH_IN_RING 76, DISP_BOTH 13, DISP_CROWD 1, DISP_PLAYER 22
salt2 | re-entries  6 | path 196.3 m | death_wave 152 | DEATH_IN_RING 23, DISP_BOTH  2, DISP_CROWD 1, DISP_PLAYER  6, WAVE_END 1
salt3 | re-entries  1 | path  39.3 m | death_wave 151 | DEATH_IN_RING  4,               DISP_CROWD 1, DISP_PLAYER  1, WAVE_END 4
salt4 | re-entries  2 | path 109.8 m | death_wave 151 | DEATH_IN_RING 12, DISP_BOTH  5,               DISP_PLAYER  5, WAVE_END 1
```
All five: `player_model_receipt.limb = DRIVE_TO_PACK`, `is_record_limb: true`. **The player moves now** — 39 m to 664 m across an ~11 m arena, against a PM4 record wire that pinned him at `0.000000000 m`.

---

## 2. THE DECISION POINT — Q59

### The framing correction that produced it (recorded because it was mine)

Mid-grill I put a fork to Matt as **"Reading A — baton now"** vs **"Reading B — PM5 first,"** presented as two fresh options of equal standing. Matt's reply was not a ruling but a challenge to the framing: *"was PM5 the pre-written next step from the sim work side?"*

**It was — by his own ruling, banked at charter row L-68:**

> **D3 = (a)** — *"ok, agreed, close it now": the run CLOSES at the boundary; the build runs OUTSIDE any run as ordinary engine work (KR sequencing, jack-ryan Gate 2, decisions-log); **the re-grade is a NEW run (KC2-PM5) chartered after the mechanism ships.***

Carried forward in four further places, all pre-written: `R-PM4-78 part (4)` (routing out) · design brief § 0 (*"Grading run this hands off to: KC2-PM5, chartered separately, after this wave ships"*) · brief § 6 (*"gandalf (RUN-CONDUCTOR) — Not on this wave. Charters KC2-PM5 after the mechanism ships and the checkpoint freezes"*) · SB-1 baton § 2 (*"wave ships Gate 2 → DRIFT-CRITIC → D5 checkpoint → PM5 charter"*).

**So "Reading B" was never an option — it is the standing plan.** The genuinely new thing Matt's reframe introduces is **the baton cut**, which appears in *none* of those five sequences. It is pre-written nowhere.

**And a second error inside the first:** I priced Reading B at *"slower by a full run."* That collapsed two distinct claims. **"PM5 first" and "baton after PM5" are not the same thing** — and **D5 is exactly what pulls them apart.** `E-s09-cp150-mech` is a *frozen, immutable sibling*. PM5 **grades** it; the adapter **reads** it. Grading does not mutate. Both can run against the same frozen bytes without contending for substrate.

### The real fork: where does the baton cut insert relative to PM5?

| | Baton cut | Cost / risk |
|---|---|---|
| **(i) Before PM5** | now, from the mech record cell | forces the ride-or-stay ruling immediately; if PM5 sends the mechanism back, you cut twice |
| **(ii) Parallel to PM5** ← *conductor's lean* | now, declared **PROVISIONAL** and pinned to the sibling's digest | same ride-or-stay ruling; re-cut is mechanical *provided* the baton's provenance block names the checkpoint digest it came from |
| **(iii) After PM5** | from whatever PM5 blesses | the standing plan read literally; Matt's stated target waits on a full grading run |

**Lean: (ii).** It is the only position that does not trade Matt's stated goal against the run discipline (grade from a clean seat). **The honest risk is F-4:** under the mechanism the sim player dies at **waves 151–156** against a referent of **160** — ungraded, because my brief's PM5 lean was occupancy-only and occupancy can PASS while the player dies nine waves early. So there is real probability PM5 sends this back and the baton is re-cut. A re-cut is an adapter run, not a session. *You don't hold the art build hostage to the balance pass; you version the wire and re-export.*

**One-word shapes: "(i)" / "(ii) as leaned" / "(iii)".**

### One more correction, in Matt's favor

**There is no sim run left to finish.** KC2-PM4 sealed at L-68 / R-PM4-78. The mechanism wave cleared both gates. What stands between Matt and a baton is close-out chores, not a run.

---

## 3. WHAT FIRES NEXT — BY OWNER

### Gated on Q59 (nothing below moves until the word lands)
- **The baton cut itself** — adapter extension past I-18, then the cut from the sibling checkpoint. gamora/star-lord seam; KR sequences.
- **Ride-or-stay ruling** on the two new export keys — `ring_ledger.mech` and `waves[0].player_model` (record limb only; ABSENT on pinned `CLUSTER_SEEK` by design, `fb5d780a`). star-lord's per `export/MIGRATION.md § 3`.
- **Baton-layer sibling ruling** — Matt/KR scope call (does the mech baton become a sibling family or supersede the `cp150` family drax pins?). Note that gamora cutting **no** batons at the checkpoint is what keeps this open and safe: nothing can currently shadow the family drax pins.

### Fires regardless of Q59
- **WARN-A — required pre-close.** `export/MIGRATION.md § 3` commits to an adapter-layer cut getting "its own entry here." The cut landed sim-side nine minutes later and no entry followed (`git log a7512917..HEAD -- src/reincarnated/export/MIGRATION.md` → 0 commits; no `cp150-mech` artifact in `export/`). This is the file star-lord reads to answer ride-or-stay, so it bundles with that ruling. **star-lord seam.**
- **Decisions-log entry** for the wave (Matt D3=(a) requires it) — **NOT YET FIRED.** jack-ryan writes; gandalf/KR propose; Matt approves.
- **F-3 — the camp-limb control** settling `DISPLACED_CROWD == 1` on four of five salts across 39 m..664 m fights. Likely benign (crowd-shove co-occurs with player motion under `DRIVE_TO_PACK` and routes to `DISPLACED_BOTH`) but that is the same shape the named failure would take. **gamora.**

### Mine, when PM5 is chartered (`RUN-CONDUCTOR`)
- **F-4 — terminal wave grades as a first-class row.** My brief § 7 lean was occupancy-only; it is insufficient. Matt rules the pass criterion at prereg per **D4**, before any cell runs.
- **F-2 — the latency decode** as a named open on the charter. Both undecoded forks landed at the *instantaneous* end (`LATENCY-ZERO` = identity; `TRACK_CADENCE_TICKS` = 1) — that is the D2/PoE contract while the referent is **Grim Dawn** (`AlertBeforePursue`, anim `0x21`). Legal and unfitted, but the first place to look if PM5 grades occupancy over-tight. The fix is a **legolas decode lap**, never a knob.
- **PM5 inherits by digest, never by re-derivation** — the I-29 `pinned_inputs` eight full-64 digests plus L-64..L-67; law stack by reference; the two-functional carve-out re-rulable at prereg.

### HELD by Matt this window — the Godot side
Explicit instruction: *"holding the godot side (what comes after the baton for another session)."* Deferred cleanly, **except one item that must be recorded rather than silently deferred:**

- **F-5 — the ratified camera does not automatically inherit.** The camera of record (`player_lock`, k=0.665, stand-off 23.1627407073975 m, two-gate eyeball PASS, PROVISIONAL-CANON) was ratified on a wire pinning the player at **0.000000000 m**. Under a stationary player, `player_lock` **is** a fixed camera. The sibling checkpoint carries a player travelling **529.8 m on salt 0**. The WW-8a/8b harness survives translation (it measured against the player ground point; the offset is player-relative) — but the **ratification** does not. `GL-13`'s 86.915 × 85.303 m rectangle now has a camera that can be driven toward its edge: exactly the condition Matt named (*"the void edge must never enter frame"*), which moves **SKIRT from theoretical to load-bearing.**
  **The next Godot session must not inherit "camera ratified" unqualified.**
- Deferred with it: which cell renders · what "re-ratified camera" means as a pass condition · SKIRT vs walls under load · and the parked SB-1 fork sitting (scale-1.95 re-derivation · wr2 chase-or-park · register-invariant), which **F-5 re-frames** and which should be held WITH the sequel charter present, not before it.

### Standing, untouched
Matt's queue: veto word · Q55/Q57 residue · engine 51-commit backlog. SB-1 parked items: FG-LEGS-DRIFT triage · resolution fix · orphan prune · NOTES harvest (absence-gate law · GDScript `%` silent-return · macOS has no `timeout(1)`) · run-close canon writes.

---

## 4. DISCIPLINES THE NEXT SESSION CARRIES

- **Charter-freshness gate FIRST** — re-read `.claude/agents/gandalf.md` + OP § 2 role-tags + `desirable-run-pattern.md` FROM DISK before routing anything; re-fire on every post-compaction turn. **Disk governs over the in-context system prompt.**
- **Law 3 / § 4.1** — no constant selected, swept, fitted, or sanity-checked against a referent number. Verify it from your own seat; do not trust a submission's prose (this window's precedent).
- **DO-NOT 8** — re-hash every pinned digest from bytes. This window caught a transcription drift in the checkpoint sha by doing exactly that.
- **Pre-registration** — PM5's pass criterion pins BEFORE any cell runs (Matt D4). The conductor does not move his own goalposts.
- **The wall** (`R-PM4-78 part 3`) — the mechanism build ran between the runs, inside neither ledger. PM5 grades from a clean seat.
- **D5** — `E-s09-cp150` immutable **forever**; new checkpoints are siblings with their own digests, never successors. Any pressure to touch it HALTs to KR/Matt.
- **Named sub-agents only** — gamora/star-lord/jack-ryan/drax/galadriel/gandalf by name; Explore-class for read-only recon only. Conductor foreground is for course, not pieces.
- **Toward Matt** — no sleep/rest/time-of-day framing, ever; workstream-relative only.

---

## 5. FRESH-SESSION ROLE-ADOPTION PROMPT

> Read your operating procedure skill (reincarnated-gandalf-operating-procedure) and execute session-start protocol per OP § 1 — charter-freshness gate first (role file + OP § 2 role-tags + desirable-run-pattern.md, all from disk). Then read `agentic_orchestration/gandalf/notes/2026-08-16-sim-arc-handoff-baton-insertion.md` (this baton) and the DRIFT-CRITIC verdict at `agentic_orchestration/gandalf/notes/2026-08-16-kc2-mech-wave-drift-critic-verdict.md`. You are gandalf on the sim arc, resuming at **Q59** — the baton-insertion fork (before / parallel to / after KC2-PM5). The lean is (ii) and the reasoning is in § 2. Read the SB-1 baton (`…/2026-08-16-sb1-session-handoff.md`) too — the Godot arc is HELD by Matt, but **F-5** in § 3 of this note qualifies its ratified camera and must not be lost. Await my direction.

---

*Window closed at the arc's cleanest seam: both reviews returned, nothing in flight, one ruling outstanding. The run's next move is a word, not a build.*
