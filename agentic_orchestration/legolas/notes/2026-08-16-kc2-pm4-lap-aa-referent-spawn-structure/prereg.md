# KC2-PM4 · LAP AA — PRE-REGISTRATION · THE REFERENT'S SPAWN STRUCTURE

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-67 part 7` (RUN KC2-PM4 charter,
`agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`)
**Written and hashed:** 2026-08-16, **before any instrument of this lap ran.**
**Commit discipline:** this file is committed **ALONE**, strictly before the instrument and the
findings (`L-46` carry; the git order is the attestation, not my word).

---

## § 0 — RECONNAISSANCE DECLARED BEFORE THE HASH

Honesty requires that I declare what I had already looked at when I wrote this file, because it
shapes the predictions below and a prediction made after the answer is not a prediction.

**Read before this hash (Lap-Y-lesson re-query of ALREADY-PINNED artifacts, `R-PM4-64 part 3`):**

1. `…/lap-z-ring-operand/pm4z_findings.md` §§ 5 (DO-NOT block), 10.2 (pinned-artifact inventory) —
   as the commission directs.
2. `…/lap-s-arena-advance/pm4s_findings.md` §§ 0, 1, 2.1–2.4, 4, 6 and `pm4s_wave_advance.md`
   in full.
3. `…/lap-t-arrival-decode/pm4t_findings.md` §§ 2, 4 (the `D-T-3` reader repair and the corrected
   spawn-point census).
4. `…/lap-u-ramp-decode/pm4u_findings.md` § 2 (the pursue-trigger decode, `ViewDistance`,
   `UNREACHED-U3`).
5. `…/lap-v2-proxyambush-decode/pm4v2_findings.md` §§ 0, 1, 4, 5, 6 (the `ProxyAmbush` release law).
6. The three shipped Lua sources already banked under
   `…/lap-s-arena-advance/evidence/` — `tier16waves.lua` (read in full),
   `survivalevent.lua` (L1–L120, L500–L620), `eventcontrol.lua` (grep only).
7. **Live recon, this lap, declared:** the ARC name tables of the four `Maps.arc` and three
   `Text_EN.arc`; the `Text_EN` tag payloads; **one** tier-16 proxy record
   (`records/proxies/tier16waves/proxy_w01_p01a.dbr`, whole-record field dump); the `Proxy`-matching
   export names of `vendor/grim-dawn/Game.dll` (names only — **no instruction byte was disassembled**).

**Not read before this hash:** any instruction stream of `Proxy::Load` / `RunProxy` /
`SelectPoolLocations` / `PlaceObjects` / `PoolComplete` / `UpdateSelf` / `DelayedRun`; any
`ShouldPlayRallyOrAlert` or `AlertBeforePursue` body; any `proxy.tpl`; any pool record; any `.map`
byte of this lap; any I-25 artifact; **any sim outcome, scorecard, or occupancy number** (the
outcome firewall — see § 6).

---

## § 1 — THE QUESTION, SPLIT INTO FORKS

The commission asks how a Crucible wave's monster population **enters the board**, for waves
150–160, as a **fight-recipe INPUT** (same class as the player's HP and gear; `R-PM4-67 part 7`).

| fork | question |
|---|---|
| **(a) WHERE** | The spawn-point positions/geometry relative to the combat floor: how many spawn points, where placed, whether all are used per wave, **and the within-point placement law** — how a pack's bodies are distributed about their spawn point. |
| **(b) WHEN** | Per-wave batch composition and release timing. Does a wave release **simultaneously** across points, **staggered** per point, or in **sequential batches**? What inter-batch / per-spawn delays does the shipped data attest? |
| **(c) BETWEEN** | Spawn-time state: is a body aggroed on spawn? Is there a spawn animation or a pre-march delay? How is the initial target acquired? |
| **(d) ARENA IDENTITY** | **Which arena and which difficulty tier did Matt's fight use?** The `D-Z-1` lesson binds: a decoy set is **ENUMERATED, not avoided.** If arena identity is not attested by the run's pinned referent artifacts, that is an **UNREACHED that bounds every fork-(a) claim**, and it will be stated as such at the top of the findings, not buried. |

**Fork (d) is adjudicated FIRST in the findings and its verdict is carried as a qualifier on every
(a) number**, because a spawn-geometry claim is only as identified as its arena.

---

## § 2 — EVIDENCE HIERARCHY (declared in advance; grade travels with every claim)

Ranked. A lower tier may **corroborate** a higher one; it may never **override** it, and a claim
resting on tier 3 alone is never graded above CORROBORATION.

| tier | class | what counts |
|---|---|---|
| **1** | **Shipped instruction stream** | `vendor/grim-dawn/Game.dll` / `Engine.dll` (PE32, unprotected), disassembled at a named RVA. The strongest evidence available for behaviour. |
| **1** | **Shipped record payload** | `.arz` field bytes for a named record path, whole-record replacement resolved across the mod stack. Strongest evidence for **values**. |
| **1** | **Shipped source text** | The Crucible's Lua, which ships as plain UTF-8 (not bytecode). Cited by file + line number. Strongest evidence for **orchestration**. |
| **2** | **Shipped world assets** | `.map` placements (`survivalworld_*`), via Lap T's repaired strict reader. |
| **2** | **Shipped template declarations** | `templates.arc` `.tpl` field declarations + `defaultValue`s. Declares what a field *is*; does not attest that anything consumes it (the `characterRunSpeedJitter` lesson, Lap S finding 5). |
| **3** | **Referent video** | The pinned fight capture and prior laps' derived plate/camera artifacts. Right-censored by the frustum (Lap S § 3.1) — can falsify, rarely confirm. |
| **4** | **Community / modding documentation** | **CORROBORATION grade only, never load-bearing** (commission text, explicit). |

**`D-V2-1` binds:** every claim cites an exact artifact + record path + field, or an exact module +
RVA. **No claim from memory, from archetype knowledge of ARPGs, or from what "Crucible" usually
means.** No vtable reconstruction; a virtual call that I cannot resolve statically is UNREACHED,
not guessed.

**Import-by-identity (`R-PM4-67 part 2`, the `D-CON-6` law):** every number carried from a prior lap
is read from that lap's **pinned artifact** at instrument time and its digest recorded. The
commission's own orientation numbers are **not** authoritative and are not used as inputs. Where I
restate a prior lap's number in prose, the artifact it came from is named on the same line.

---

## § 3 — VERDICT CLASSES, AND WHAT EACH REQUIRES

Fixed here so that no verdict can be chosen after the evidence is in.

| class | requirement |
|---|---|
| **DECODED** | The claim is read directly out of shipped bytes with **no inference step**: an instruction sequence at a cited RVA whose operands I print, a record field whose payload I print, or a line of shipped source I quote verbatim. If a step in the chain requires "and therefore presumably", it is **not** DECODED. |
| **DECLARED** | The shipped data or template **declares** a value or structure, but the **consumer was not traced** to a behaviour. A `.dbr` field whose loader I did not disassemble, or a `.tpl` `defaultValue` with no located reader, is DECLARED. Explicitly weaker than DECODED and never merged with it in a table. |
| **CORROBORATION** | Independent agreement from a lower-tier source (video, community documentation, a second internal instrument). **Never load-bearing alone**; recorded so that the declared evidence class is visibly discharged rather than silently dropped (`Lap Z DO-NOT 7`). |
| **UNREACHED** | Looked for, not found, or blocked (DRM, virtual dispatch, absent attestation). **Named with what was tried and what would reach it. Never estimated, never interpolated, never softened into an "approximately".** |

**INFERRED-WITH-EVIDENCE** is retired for this lap: a claim is either DECODED, DECLARED,
CORROBORATION, or UNREACHED. If something sits between DECLARED and DECODED it is published as
DECLARED with the missing link named.

---

## § 4 — PRE-REGISTERED PREDICTIONS

**Graded at the end, wording unchanged, whether they hold or fail.** A failed prediction is never
rewritten; a prediction that turns out to be unanswerable is graded UNREACHED, not quietly dropped.
Predictions are bets about **mechanism**, not about which answer helps the run.

| id | prediction |
|---|---|
| **P-AA-1** | Across all **54** tier-16 wave-proxy records, the **only** release-shaping fields present are `delayedRun`, `chanceToRun`, `placementExtents` (plus the eight `ProxyAmbush` fields on the seven ambushes). **No base-`Proxy` record in the band carries any spawn delay, spawn interval, batch size, or release-rate field.** |
| **P-AA-2** | `Proxy::PlaceObjects` places its entire id vector inside **one call** — a loop over the vector, not one object per tick. A base-`Proxy` spawn point therefore puts its whole pack on the board **at a single instant**. |
| **P-AA-3** | All active spawn points of a wave release with **no authored stagger between them**: the Lua dispenses them in one `for` loop in one call, and the base-`Proxy` path introduces no per-point delay. Any residual inter-point separation is at most one update tick and is **not** a designed schedule. |
| **P-AA-4** | `Proxy::SelectPoolLocations` distributes bodies about the spawn point by an **independent random offset per body** bounded by `placementExtents`, **not** by a formation, grid, or ring. **Sub-bet, registered blind: the offset region is a SQUARE/BOX (per-axis independent draw), not a disc.** |
| **P-AA-5** | `delayedRun = True` defers the run by **at most one update tick** and carries **no authored duration** on the base `Proxy` — i.e. it is a "run on the next update" latch, not a timer. |
| **P-AA-6** | The **only** spawn-side timer in the 151–160 band is the `ProxyAmbush` `Uniform[4000, 4000] ms` on spawn point 5 (Lap V-2 `F-5`, imported by identity). No second spawn-side delay mechanism exists for the 47 base proxies. |
| **P-AA-7** | **Pessimistic, registered as such: ARENA IDENTITY lands UNREACHED.** The shipped artifacts and the run's pinned referent artifacts will not attest which of `survivalworld_a…j` Matt's session used, nor which difficulty tier, and I will say so rather than pick the modal arena. |
| **P-AA-8** | **Pessimistic: `UNREACHED-U3` (`ShouldPlayRallyOrAlert` → `AlertBeforePursue`) will NOT close.** I expect to read the function body but **not** to resolve whether it fires on the Crucible path, because its driver is behind the same virtual dispatch that made `UNREACHED-U1` unreachable. |
| **P-AA-9** | Per-wave batch composition is **stochastic, not fixed**: each active spawn point draws its pack from a pool with a count distribution (Lap V's count model, imported by identity), so "the wave's composition" is a distribution and not a roster. **No spawn point in the band dispenses in more than one batch.** |
| **P-AA-10** | **The load-bearing bet.** After (a)+(b)+(c), the referent's **arrival ORDER at the player is generated by march geometry and body speed, not by a spawn schedule** — the shipped structure releases packs essentially simultaneously and the ordering is imposed downstream. |
| **P-AA-11** | **Wave 150 is NOT dispensed by `tier16waves.lua`.** `rewardTier = floor(150/10) = 15` routes the *tier-16 event start* at counter 150, but the counter increments **inside** `SpawnNext` (Lap S `A-5`), so the bodies fought on the board labelled 150 were dispensed by the previous tier's table. The commission's "150–160" therefore spans **two authored tables**, and I will say so. |
| **P-AA-12** | The engine reads a **per-body placement radius/extent** at placement time that is **not** the same quantity as the arrival ring — i.e. `placementExtents` will decode as a *scatter bound*, in metres, on the same world scale as Lap F's `actorRadius`. |

---

## § 5 — INSTRUMENT PLAN, AND THE GUARDS ON IT

**One instrument**, `agentic_orchestration/research/scripts/pm4aa_spawn_structure_2026_08_16.py`,
writing only into this lap's notes directory. It re-implements nothing: the project's existing
`gd_arz_adapter_2026_07_24.py`, `gd_arc_reader_2026_07_26.py`, `pm4s_pe_2026_08_14.PE32` and Lap T's
repaired strict `.map` reader are imported unchanged (NOTE-9).

**Legs:**

1. **PINS.** Re-hash every pinned input before any read. **HALT on any mismatch.**
2. **ROUTING.** Decode the wave→table routing for 150–160 from `eventcontrol.lua` +
   `survivalevent.lua` verbatim, including whether `SurvivalEvent_Start` dispenses immediately.
3. **RECORDS.** Whole-record replacement across the mod stack for all 54 tier-16 wave proxies and
   every pool they reference; emit the complete field set of each, so that P-AA-1's negative is a
   **census**, not an impression.
4. **TEMPLATES.** Resolve `proxy.tpl` (and the pool template) from `templates.arc`: the full
   declared field set with `defaultValue`s, so that a field **absent** from a record is still
   accounted for.
5. **BINARY.** Disassemble, at named RVAs, and print the operands: `Proxy::Load`, `Proxy::DelayedRun`,
   `Proxy::RunProxy`, `Proxy::SelectPoolLocations`, `Proxy::PlaceObjects`, `Proxy::PoolComplete`,
   `Proxy::UpdateSelf`, `Proxy::InitialUpdate`; and for fork (c) the alert/rally path.
6. **GEOMETRY.** Re-query, **not re-derive**, the corrected spawn/patrol geometry from Lap T/U's
   pinned artifacts; add only what the new question needs (per-arena spawn-point layout relative to
   the attack ring, and the enumeration for fork (d)).
7. **ARENA (d).** Enumerate the full decoy set: every `survivalworld_*` map in every mod archive,
   with the mod-layering resolution stated, and every discriminator I tried against the referent
   artifacts, **including the ones that returned nothing.**

**Guards, each armed before the run:**

- **`D-Z-1` guard (decoy enumeration).** Every record lookup is by **exact path**, never substring;
  and where a substring match would have had more than one hit, the **full hit set is published**
  in the emitted artifact so the guard lives in the artifact rather than in my attention.
- **`D-Z-2` guard (silent header off-by-one).** Every structural parse asserts an internal
  consistency condition and **HALTs** rather than resyncing. Lap S's `D-T-3` is the precedent: a
  reader that resyncs reports a quality ratio that measures nothing.
- **`D-Z-3` guard (linear-sweep desync).** Any x86 decode whose start is a manual byte anchor is
  decoded from **three independent starts** and the instruction of interest asserted identical in
  all three; disagreement HALTs.
- **`D-T-3` guard.** The `.map` reader used is Lap T's **strict, non-resyncing** one, imported
  unchanged; the two maps that HALT honestly in Lap T are expected to HALT here too and will be
  reported as such rather than back-filled.
- **Determinism ×2.** The instrument runs end to end **twice**; all emitted artifacts must be
  **byte-identical**. Any difference HALTs the lap.

---

## § 6 — THE OUTCOME FIREWALL, AND WHAT THIS LAP WILL NOT DO

- **Law 3 (no tuning).** This lap **prescribes nothing**. It decodes the referent. Referent numbers
  are **GRADES for the sim, never inputs**, and no number here is chosen, framed, or graded by which
  sim outcome it would produce.
- **`R-PM4-27 part 3` (no designation by grade).** Where a fork has limbs, the limb is decided by the
  bytes and **published with its alternatives named**. I will not look at a sim scorecard, an
  occupancy number, an I-25 artifact, or any I-24 result while this lap runs, and I will state at
  the end that I did not.
- **`R-PM4-56 part 4` (new mechanisms: NAME, don't decode).** Anything this lap trips over that is
  outside forks (a)–(d) is **NAMED in a collateral table and left undecoded.** Decoding it is a
  separate commissioned lap.
- **No simulation. No fold. No prescription.** No file outside
  `agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure/` and
  `agentic_orchestration/research/scripts/pm4aa_spawn_structure_2026_08_16.py` is written.
  **Read-only on every external source. No push.**
- **All standing DO-NOT blocks are carried unchanged:** Lap V § 7.2, Lap V-2 § 11.2, Lap W § 7.2,
  Lap X § 12.2, Lap Y § 11.6, **Lap Z § 5 (all seven items)**. In particular Lap Z DO-NOT 4 —
  `NAMED-Z-1` (box-vs-sphere) is **not** propagated as decoded sim behaviour by this lap either.

---

## § 7 — WHAT THE FINDINGS FILE WILL CONTAIN, REGARDLESS OF RESULT

Committed here so that a disappointing result cannot quietly reshape the deliverable.

1. Headline table, one row per fork, **with fork (d)'s verdict first** and stated as a bound on (a).
2. Per-fork findings with grade and exact citation on every claim.
3. **Defect table — self-caught, published BEFORE any claim rests on the repaired instrument.**
4. **Collateral NAMED not decoded** (`R-PM4-56 part 4`).
5. **DO-NOT block binding on downstream folds.**
6. **UNREACHED census, honest, per fork** — with what was tried and what would reach it.
7. **Predictions from § 4 graded, wording unchanged.**
8. **Full 64-hex sha256 of every artifact consulted and every artifact emitted.**

---

*Pre-registered by legolas (UNKNOWN-RESEARCHER), 2026-08-16, RUN KC2-PM4 Lap AA.
Committed alone, before the instrument. If a prediction above fails, it stays as written.*
