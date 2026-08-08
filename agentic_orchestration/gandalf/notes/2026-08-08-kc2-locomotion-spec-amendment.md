# KC2-SIM — locomotion spec amendment (F-12) — what changed, and what gamora builds against

**Agent:** named-gandalf sub-agent, **SPEC-AUTHOR**. **Commissioned:** conductor, ledger **L-47**
(fired after the F-13 fold so the § 10 touch lands coherent — L-46(f) sequencing).
**Target artifact:** `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`
(2,764 → 3,177 lines).
**Consumes:** L-43 C-1…C-5 · L-44(d) · L-45(d)/(e) · L-46(a)–(d) ·
`legolas/notes/2026-08-08-kc2-citation-microprobe.md`.
**Commit state:** UNCOMMITTED — rides the conductor's fold.
**Discipline:** charter § 4.2 — every constant DB-/TPL-/SOURCE-/LEVEL-CITED with its record named,
or DECLARED with its empirical bound. **Zero fitted parameters.** No production code touched.

---

## 1 — Edits landed, by anchor

| # | Anchor (line) | Edit | Remit |
|---|---|---|---|
| **E-1** | **§ 2.2** :180 | Heading extended to *"— and the locomotion model of record"*. Struck the *"presentation owns the monster's approach choreography"* clause: under a sweeping-**area** damage predicate the approach is **causal**, so the sim owns actor position over time and presentation owns gait/spacing **within** it. Added the model of record — **`path-to-zone` THEN `pursuit-gate`** — with its three SOURCE/DB citations, the **hypothesis-not-assumption** paragraph (the lap TESTS the shape against r = +0.154; T-1 UNCHANGED), and the discriminability caveat. | (a) |
| **E-2** | **§ 2.3** :232 | Arena-shell bullet annotated with the cited radii + § 10.9a pointer. **New bullet: G-1h under motion** — the reconstruction bar was satisfiable from `{centre, radius, tick}` only because the board was static; hit/no-hit is now a function of two trajectories → **R-LOCO-1**, routed. | (a), + G-1h consequence |
| **E-3** | **§ 10.6** :1168 | **New "Motion hook" block** appended after the landed provenance + bearings paragraphs (landed text untouched): six radii not one; **p01 keyed per tier**; reference frame = `PatrolPoint_Attack` centroid not `playerspawnpoint`; destination is a **node set**; provenance travels with the numbers; per-sitting rule reconciled (**selection** is per-sitting, **positions** are cited). | (c) |
| **E-4** | **§ 10.6** :1198 | **MO-5 re-check block** — the *provisional-on-geometry* flag clears only on re-demonstration under **cited** radii; the two effects (traversal lengthens ~25 %, player-touring term disappears) are reported **separately**; an undershoot is a finding, never a re-pin. | (c) |
| **E-5** | **§ 10.9** :1443 | Struck the additive reading of the cycle decomposition: under motion the terms **overlap**; composition is closer to `max(last_arrival, cumulative_kill) + tail`. Every inherited bound argument — including F-12's own 89/92 — must be **re-derived**. | (e) |
| **E-6** | **§ 10.9a** :1463 | **NEW SUBSECTION — the movement rules.** A model (two limbs, ruled default, divergence condition) · B every term with its citation · C declared-unmodelled lap inputs · D the `v_ref` bracket · E composition law + separability · F calibration procedure · G reporting obligations + R-LOCO-1. | (b),(d),(e),(f) |
| **E-7** | **§ 10.10** :1709 | AC-10.7 amended (floor re-demonstrated under cited radii). **AC-10.8…AC-10.12 added** — board moves + motion is causal (F-12 regression guard) · speed is per-record never global · six cited radii, p01 per tier, **literal 30.0 appears nowhere** (F-12a guard) · ambush excluded from the patrol link · reporting obligations as artifacts. | (b),(d),(f) |
| **E-8** | **§ 12** :2496 | **MO-5 row annotated** (ledgered-ruling consequence, not an edit to a pin): re-check now *specifiable* under cited radii; MO-5 acquires a **second role** as the K-3 **upper** bound on closing speed. | (c) |
| **E-9** | **§ 12** :2503 | **Ordering annotated** — the s2 one-sided inequality runs **INSIDE** the lap as the second-geometry diagnostic (L-45(d)/D2-5); full-ladder stays paused. | (f) |
| **E-10** | **§ 13** :2539 | Declared-not-HALT: *"emitter world positions (DECLARED free parameters)"* **STRUCK** → geometry CITED-per-arena, **selection** declared. `v_ref` annotated **SOLE free scalar**; jitter + controller surface added as declared out-of-model. | (b) |
| **E-11** | **§ 14 F-12** :3051 | **C-3 disposition bullet** annotated: *"monsters path to the player"* struck → path-to-zone THEN pursuit-gate (L-46(a)); the degeneracy clause struck — it **resolved the other way** (m/s NAMED-ABSENT, radius LEVEL-CITED). *Status bullet, F-12a, F-13, F-9/F-10 untouched per fence.* | value-set sweep |
| **E-12** | **§ 11.3 / § 11.4 / § 11.5** :1872, :1998, :2190, :2202, :2240 | Signed-contract surfaces — see **JC-5**. Truth-boundary rows amended (prose); `D-ARENA-DECLARED` struck → `D-ARENA-CITED`; `positions_provenance` / `arena_id` / `closed_by_type` / `arena_pin` annotated **in comments only**, shapes unchanged. | value-set sweep |

**Value-set sweep run per the L-45(b) standing method** — enumerated spellings of the superseded
claims (`path to the player` · `monsters path` · `APPROACHING` · `never DB-hunted` · `L-10d` ·
`DECLARED free parameter` · `emitter_radius` · `30.0 m` · `static board` · `SPAWN coordinate` ·
`positions_provenance` · `monster approach choreography`), grepped the **whole** artifact, every hit
adjudicated. Operative hits fixed (E-10, E-11, E-12); benign-historical hits left standing with
reasons: F-12's *Mechanism* bullet (a faithful record of the beat-3 diagnosis), F-12a's
"uncited bare float" (already carries the L-46 re-grade), § 0.1's glossary *"spawn + approach +
kill"* (true under both models).

---

## 2 — Which citation carries each constant

| constant | value | grade | carried by |
|---|---|---|---|
| ring radii (p01–p04, p06) | median **37.53 m**, n = 322, 15.52–47.89 | LEVEL-CITED | `Maps.arc` decode → `kc2_crucible_emitter_geometry.csv` sha `ece0c345…` |
| p01, **per tier** | band-A median 38.51 m; spread ≤ 17.36 m | LEVEL-CITED | same |
| p05 ambush radius | median **10.17 m**, n = 10 | LEVEL-CITED | same |
| patrol node set | 173 nodes, median 18.85 m from centroid | LEVEL-CITED | `kc2_crucible_patrolpoints.csv` sha `106facba…` |
| the mechanism | patrol-link on non-ambush spawns, 17/17 tier modules, 200 waves | **SOURCE-CITED** | `sm_mod/game/events/survivalevent.lua:552` |
| length unit = **metre** | — | DB-CITED (Crate annotation) | `travelSpeed` / `tailTravelSpeed` / `particleSpeed` / `textureSpeed` |
| `characterRunSpeed(a)` | n = 895, median **1.000**, range 0.60–2.00 | DB-CITED | `kc2_s1_banda_record_inputs.csv` sha `ac50ef77…` |
| `ViewDistance` / `MaxPursuitDistance` / `PursuitTime` | **80.0 m** / **125.0 m** / **10 000 ms** (868/895) | DB-CITED | `ControllerMonster` DBRs, 126 distinct |
| `d_engage` | **2.4**…**4.0 m** | DB-CITED | `gameengine.dbr` (`meleeTargetDistance`, `meleeAutoTargetDistance`) |
| player run speed | **135 %** = `playerRunSpeedCapMax` | DB-CITED + ceremony § D | `gameengine.dbr` |
| `disableMovement` | ABSENT 895/895 | DB-CITED | probe § 2.5 |
| scatter | `placementExtents = 8.0`, 925 proxies | DB-CITED | P-E6 § 2.3 |
| **`v_ref`** | **the SOLE free scalar** | **DECLARED**, bracketed K-1…K-3 | HALT-2 CLOSED-BY-TYPE (census-complete NAMED-ABSENT) |
| arena selection | which of 10 | **DECLARED** over a cited enumeration | § 10.6 layer 2 |

---

## 3 — What the gamora lap must BUILD

1. **Per-actor motion** — `x_a(t+dt) = x_a(t) + characterRunSpeed(a)·v_ref·dt·unit(target − x_a)`,
   planar, open-plane. The disc hit-tests against **current** positions, never spawn positions.
2. **Six cited radii per selected arena**, p01 resolved **per content tier**; `Arena.emitter_radius_m`
   deleted, not re-valued.
3. **The gate** — `ViewDistance` / `MaxPursuitDistance` / `PursuitTime` per record, with the
   **p05 ambush exclusion** (no patrol leg).
4. **Two limbs** — L-A zone-first (default) and L-B gate-first (sensitivity); the baton records which.
5. **A declared player-movement policy** (camp / kite / tour) — the closure attribution turns on it
   and it must be stated once, in one place.
6. **Instrumented arrival and kill terms, separately** — the composition law is measured output, not
   an assumption.

## 4 — What the lap must TEST and REPORT

- **T-1 UNCHANGED** — the only binding clear-time gate. A second failure is a finding.
- **AC-10.8…AC-10.12** (§ 10.10) — motion is causal · speed is per-record · six cited radii ·
  ambush exclusion · reporting artifacts.
- **`r(clear_time, N)`** against the fixture's **+0.154** — a **DIAGNOSTIC**, never a goalpost.
- **The K-1…K-3 feasible region** with the declared `v_ref`'s position in it; an empty region is a
  finding.
- **MO-5 under cited radii**, with traversal-lengthening and touring-removal reported separately.
- **N-sensitivity** (F-13 residual, § 5 below) and the **L-A vs L-B delta**.
- **w152 / w153 / w157**: simulated, reported, **absent from parameter selection**.
- **s2 one-sided inequality inside the lap** as the second-geometry diagnostic — INFORMATIVE,
  cannot false-trip under a slow bias.

---

## 5 — Conflicts found between the L-46 citations and the standing spec — **conductor adjudicates**

> Every item below is a judgment I made under commission. Each is reversible; each names what I did
> and why, so a veto is cheap.

**JC-1 — the 3.5–6.1 s traversal band was measured at the AMBUSH emitter, and § 10.6's landed
sentence applies it to "the arena's one free timescale."** Its provenance (L-44(d)) is the p05 plant
chain against its DB cadence: spawns 4.0 / 7.0 / 10.0 s, engagements +10.1 / +12.7 / +13.5 s ⇒ lags
6.1 / 5.7 / 3.5 s — at a **10.17 m** median radius. **The ring is 37.53 m: a 3.7× mismatch.** Binding
`v_ref` to that band over a ring radius makes monsters ~3.7× too fast. **What I did:** left the
landed § 10.6 paragraph untouched (fenced) and wrote the correction into § 10.9a D, keyed per
emitter class, supplying the **ring-class analogue from the same L-44(d) row** — the w152/w157 boss
minimap-glyph→readout lag of **3.0–4.3 s** at p04's 38.45 m. **Conductor call:** whether the landed
§ 10.6 sentence now needs a strike of its own.

**JC-2 — L-46(a)'s OUTCOME is adopted; its stated REASON needed refinement.** The ruling adopts
path-to-zone-then-gate as *"the less body-count-coupled shape."* What removes the N-coupling is that
**the monsters travel at all** (any limb) — plus two channels the ruling does not name: **convergence
bunching** under a 3.0 m AoE disc, and the **arrival schedule floor**. And the bunching channel runs
the *other* way: **pure pursuit (L-B) bunches on a point; zone-first (L-A) bunches on an 18.85 m node
cloud**, so L-A is not self-evidently the flatter limb. **What I did:** kept L-A as the ruled default,
added L-B as a declared sensitivity limb, and wrote the three flattening channels as **measured, not
credited** (§ 10.9a E). Veto-open.

**JC-3 — the two limbs may not be discriminable in band A.** `ViewDistance` 80 m exceeds every
measured emitter radius (max 47.89 m) and `MaxPursuitDistance` 125 m exceeds every arena diagonal, so
the pursuit gate is **open from t = 0** for any in-arena player; the priority between the two
behaviours lives in the executable (**NAMED-ABSENT**). For a centrally-camped player the limbs
nearly coincide. **What I did:** stated it in § 2.2 and § 10.9a A rather than letting the ruling read
stronger than the citations support.

**JC-4 — R-LOCO-1: the amendment BREAKS a standing spec law, and the baton cannot yet express the
fix.** § 2.3's BR-2 **G-1h** law requires that an independent function reconstruct hit/no-hit from
the emitted set alone. That held under a static board because each actor's position *was* its
emitted `spawn_x/spawn_y`, forever. Under motion, hit/no-hit is a function of **two** trajectories
and the baton emits **one**. **What I did:** named it at the moment the amendment created it,
registered it as **R-LOCO-1** (§ 10.9a G), stated the two candidate shapes with their costs
(Option 1 per-actor piecewise-linear waypoints, ~tens of bytes/actor against a measured 17.4 MB
artifact — my lean; Option 2 per-tick position tracks, exact but lands on § 11.6.1's size work), and
**did not decide it.** Routed to conductor → star-lord + drax.

**JC-5 — I edited signed § 11 surfaces, in prose and comments only. This is the item most worth a
veto check.** Three operative-false statements sat inside a *signed cross-seam contract*: (i) the
§ 11.3 truth-boundary row assigning *"monster approach choreography"* wholly to presentation;
(ii) the `D-ARENA-DECLARED` declaration string — *"emitter positions are DECLARED free parameters …
never DB-hunted"* — which L-46 falsified by hunting and finding them; (iii)
`positions_provenance: "DECLARED"` and `arena_id: "s1"|"s2"`, which can no longer express which of
ten cited arenas ran. **What I did:** amended (i) and (ii) with strike-lineage — a **false provenance
claim inside a provenance block** is precisely the defect the baton exists to prevent — and left
(iii)'s *values and shapes* untouched, marking them with `⚠ OPERATIVE-FALSE post-L-46` comments that
point at R-LOCO-1. **Consequence the conductor must route: `AC-11.4b` set-compares against the
declarations register, so `D-ARENA-DECLARED` → `D-ARENA-CITED` requires a star-lord re-sync.**

**JC-6 — I annotated F-12's C-3 disposition bullet.** It still read *"monsters path to the player"* —
the model L-46(a) superseded. It is neither the Status bullet, nor F-12a, nor F-13, nor the F-9/F-10
bullets, so it sat outside the fence; the L-45(b) standing method makes leaving it a sweep failure.
Strike-lineage, cites L-46(a), points to § 10.9a.

**JC-7 — a derived, pre-registered consequence that sits close to the fitting line; I drew the line
explicitly.** K-1 (closing ≥ 8.01 m/s) and K-3 (closing ≤ 33.53/(7.0 − A)) are simultaneously
satisfiable **only if the declared non-traversal latency budget A ≳ 2.81 s**. That is a falsifiable
prediction of the amended model and a genuinely useful one — but **solving the inequality for A and
adopting the result would be fitting**, so § 10.9a D says so in terms: A is declared from evidence or
declared unknown, *then* the check runs; a violation is a finding with four named candidate causes.
If the conductor judges even the stated inequality too close to the line, it strikes cleanly without
touching the rest of D.

**JC-8 — the band-A N residual, which the F-13 exclusions do not reach.** The landed F-12 status
excludes w152/153/157 — all in the s2 band. **Band A (1–93) contains no censused wave**, so its
counts are neither falsified nor corroborated, and they are drawn from the same trash limb F-13
graded **INCOMPLETE**. Excluding band-A waves is impossible (nothing is falsified) and asserting
their soundness is unwarranted. **What I did:** left the landed exclusion set exactly as ruled and
added an **N-sensitivity reporting obligation** instead (§ 10.9a F.4, AC-10.12) — a result
insensitive to N is robust to the residual; a sensitive one inherits it and says so.

---

## 6 — Open residuals handed back

| # | Residual | Owner |
|---|---|---|
| **R-LOCO-1** | Baton cannot express a moving board (G-1h). Option 1 waypoints (lean) vs Option 2 per-tick tracks; plus `arena_ref` over the cited enumeration + the six radii + `positions_provenance` value. | conductor → star-lord + drax |
| **R-LOCO-2** | `AC-11.4b` declarations-register re-sync for `D-ARENA-DECLARED` → `D-ARENA-CITED`. | conductor → star-lord |
| **R-LOCO-3** | `characterRunSpeedJitter` (median 15.0, n = 810) — declared out-of-model this lap; if it disperses run speed, **arrival is a distribution, not a time**. | conductor → gamora (probe § 6 O-1) |
| **R-LOCO-4** | The 126 × 27 `controller` surface — roam, patrol-idle, emote, swing pauses, `walkDistance`, distress calls. Every unmodelled field adds **latency**, a known signed bias toward late arrival. | conductor → gamora (probe § 6 O-2) |
| **R-LOCO-5** | `arena_id` discrimination needs a save-file level id or a footage landmark; the datamine cannot settle it (probe § 4.5). Until then the selection is declared over a cited enumeration. | conductor → galadriel / save lane |
| **R-LOCO-6** | Patrol-node **assignment** rule (nearest / centroid / per-emitter) is in no pin — DECLARED; the baton records which ran. | gamora, declared |
| **R-LOCO-7** | JC-1's ring-vs-ambush provenance correction may warrant a strike on the landed § 10.6 traversal-bounds sentence. | conductor |

---

**Filed:** named-gandalf (SPEC-AUTHOR), 2026-08-08, KC2-SIM Phase D. No production code touched.
No ledger writes. F-13, F-9/F-10 and the F-12 status bullet untouched per fence.
