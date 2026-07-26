# Gemini doc triage — what survives into the program, what doesn't

**Source:** `matt_notes_handoff_docs/GD-OBS-ideas-from-gemini` (Matt-supplied external doc, triaged 2026-07-26).
**Author of triage:** gandalf (DRIFT-CRITIC). **Disposition:** three items WOVEN IN (below); the rest
is either already-canonized-at-higher-rigor or rejected with reasons.

---

## 1. Convergence finding (no action)

The doc's core architecture — GD as deterministic baseline, other ARPG behaviors as
configuration-layer modifications over it — is an independent reinvention of the **era-substrate
ruling** (`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md`). Mild external
validation of the canonized shape. Its *reason* is weaker than ours and must not back-propagate:
it selects GD for parseability; canon selects GD for the **live oracle** (LAW §4 — parseability
without behavioral validation is an AUTHORED claim wearing MEASURED clothes).

## 2. WOVEN IN — three items

### 2.1 `game.Speed <float>` — engine time dilation (UNVERIFIED command candidate)

Claimed GD console command slowing the whole engine (e.g. `game.Speed 0.5`). **Not in the probed
command table** (`research/knowledge/gd/2026-07-25-gd-console-command-table.md`). If real, it is a
first-class instrument for the **L1 telegraph/animation-window sitting**: dilated game-time means
each captured frame samples a finer slice — wind-up windows and state-transition boundaries at
effectively higher temporal resolution than 60 fps buys at 1×.

- **Probe items before use** (fold into the NEXT bounded sitting, NOT general-play): (a) does the
  command exist / what syntax; (b) does `PlayStats play_time` dilate with engine time or track
  wallclock — the answer decides whether dilated captures can share the fixtures schema or need a
  `time_scale` provenance field; (c) does AI behave identically at 0.5× (no scheduler artifacts).
- **BANNED from the general-play run.** Dilated play is not natural play; the distribution oracle
  measures the latter. Protocol sheet §2.2 "play normally" governs.

### 2.2 Era-profile dial seeds → fork E-2 (banked so they don't evaporate)

E-2 (per-era signature-feel checklists, `era-substrate-architecture` §7) is deferred until the
first era-profile authoring session. These concrete dial candidates from the doc are BANKED for
that session — seed material, NOT ratified dials:

| Era | Candidate dial | Note |
|---|---|---|
| D2 | **Flee-on-pack-member-death + shaman-rally override** | Morale as pack-level state; the rally override is the interesting part — a leader archetype flipping a pack-wide state matches the probed `followtheleader` observation |
| D2 | **Stutter-timer pathing latency** (`stutter_timer_range` ~[0.2, 0.5] s) | The "retro chase feel" as a dial, not a pathfinding rewrite — profile-compatible (parameter, no state-machine fork) |
| D2 | **Desynchronized aggro** — high-variance per-monster detection radii | Complements canon §5's "big dumb relentless packs" |
| PoE1 | **Same-tick pack awakening** (global alert flag) | The inverse dial of D2 desync — one axis, two era poles. Good sign: dials that span eras on one axis are exactly what §5 wants |
| PoE2 | **Animation-commitment lock** (`attack_commitment_pct` = 1.0: rotation + tracking frozen during heavy attacks) | The soulslike accountability dial; pairs with telegraph beats already in canon §5 |
| PoE2 | **Sequential combo arrays** (weighted-random → ordered skill cycle) | ⚠ BORDERLINE: canon §5 says profiles "never fork the state machine." A selection-MODE switch is arguably a fork. E-2 session must rule whether selection-mode is a legal dial or a state-machine change |
| PoE2 | **Melee engagement cap + circling overflow** | The strongest seed in the doc — genre-correct fix for body-block clumps; also a candidate for OUR native game regardless of era profiles |

### 2.3 CFR capture line

Protocol sheet §3.2 gains "CFR (constant framerate — OBS default; do not enable VFR)". Our
extraction is PTS-based and VFR-robust; CFR is free insurance and simplifies frame arithmetic.

## 3. REJECTED, with reasons

- **DBR extraction script** — superseded before arrival: elrond's M2 banked 4,066 records /
  202,120 fields at DATAMINED grade (edition-pinned, sha256) on 2026-07-26. The doc's 4-key map is
  a toy; adopting its "clean JSON templates" framing would LOSE the provenance discipline.
- **Spawn path `records/controllers/monsters/…`** — wrong; probe-confirmed tree is
  `records/creatures/enemies/…`. Do not let this string leak into any sheet.
- **Engine comparison matrix** (D2 "Poor", PoE1 "Poor", PoE2 "Moderate") — conclusions roughly
  rhyme with canon; reasoning is unsupported vibes. Canon's §2 (one-substrate-or-nothing +
  live-oracle seat) remains the citable argument.
- **Frame-count window equation / VLC scrubbing** — subsumed by the galadriel CV pipeline
  (calibrated 2026-07-26; measured error rates, not hand-scrubbing).
- **Godot AnimationPlayer/StateTree mapping** — presentation-seam (drax) material, premature here;
  noted only that the doc's "decoupled state → node mapping" claim is compatible with the existing
  timeline-export direction.

---

**Signed:** gandalf, 2026-07-26. One command candidate parked for the next probe, seven dials
banked for E-2, one line added to the capture spec. The rest was either already ours — built
honester — or wrong in ways worth writing down.
