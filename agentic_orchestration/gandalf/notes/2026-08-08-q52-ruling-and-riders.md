# Q52 RULED — reading (i) + riders 1–3 + red-tree — ruling record and main-session execution checklist

**Ruled by:** Matt, 2026-08-08, gandalf side-session (the T15 depot-sitting session, continued into the KC2 steelman dialogue).
**Verbatim word:** *"Q52 = reading (i); riders 1–3 approved; red tree does not gate emit."*
**Boundary class:** commitment-boundary DISCHARGED (desirable-run-pattern § 4 — the gate interprets Matt's own R-KC2-8 sentence; only Matt adjudicates its meaning).
**Disk-first per the charter-freshness discipline:** this note + the queue strike (`canonical/matt_decision_needed/README.md` Q52 row) are the channel of record between the side-session and the run's main session. The main session executes from THIS note, not from any transcript.
**Ledger row + R-number:** assigned by the run's conductor session at its next fold (two sessions never write one ledger — collision rule). This note is the source the row cites.

---

## § 1 — The ruling: reading (i) governs G-STATS

**Reading (i) — Matt's R-KC2-8 words** (*"I definitely do not want to ship the data packet (baton) without the actual monster stat tables"*): MEASURED stat tables ship ON the baton → the gate is satisfied by the stat fold's measured tables riding the roster rows.

**G-STATS therefore passes today by measurement:** eHP 967/968 · swing damage 953/968 · BOTH 953 = 98.45% (968 = 896 rostered + 72 summon, hop-1 fixpoint). Residual pricing reaches Matt carrying the Gate-2-corrected level bracket **3.3056%** (F-2 corrigendum, NOT the stale 4.736%). Named residuals carry on the baton as priced declarations, not blockers: scavenger 1/968 INFERRED · 14 MEASURED-ZERO-SWING-INCOMPLETE · emission channel EXCLUDED-BY-NAME · band B NOT MEASURED.

**Reading (ii) is RETIRED** — the spec § 11 sentence *"folded into the sim's kill term"* was conductor decidability-narrowing of Matt's sentence, and demanding a sim-side incoming-damage model (three uncharted free parameters in a no-fitting run) is rubric-law intent leak in the OVER-demanding direction (desirable-run-pattern § 6 obs. 3, inverted).

### § 1.1 — The second leg (playtest-endpoint rationale, from the ruling dialogue)

Matt named the endpoint: after baton → Godot render, the next step (parallel to fitting other kits into the sim) is **hands-on playtest**. At that moment the sim's player model is discarded — Matt IS the player. What survives contact with his hands is the monster side, resolved LIVE by Godot against his actual position. Reading (ii)'s deliverable — a pre-computed incoming-damage timeline — is exactly the artifact the endpoint throws away. Reading (i)'s deliverable — the measured tables on the baton — is exactly the artifact the endpoint consumes. **(i) is both the faithful reading of Matt's sentence AND the correct architecture for where the work is going.**

Method context ruled in the same dialogue (reference-as-control-arm): GD Crucible is the project's **feel reference** — measure the reference, reproduce faithfully in Godot, playtest the reproduction to calibrate the *pipeline* first, then perturb one variable at a time (RDR kits into a reference-held arena), with a **divergence ledger** so departures from the measured reference are named (keystone-driven / platform-driven / taste), never silent. The sim stays a **kit-throughput instrument**; it never becomes a threat simulator. Discipline #13 (implicit-pillar drift) is the hazard the ledger guards.

---

## § 2 — Rider 1 (APPROVED): G-E exit-artifact declaration — "what this baton does NOT underwrite"

Scoped as an **exit-artifact amendment, not a mid-run gate rewrite** (preregistration holds: the run does not move its own goalposts; Matt moved the artifact, not the gates).

At Phase E, the **G-E handoff note for the Godot session AND the baton's provenance block** gain an explicit declaration:

> This baton underwrites scene geometry, wave composition, roster (with measured eHP + swing damage), player path, circle sweep, and wave/engage timing. It does NOT underwrite live threat resolution: monster attack-TIMING grammar (wind-up, recovery, telegraph, cadence, root-lock) is NAMED-ABSENT-DECLARED, arriving via the threat-grammar companion lap (Rider 2). Playtest-readiness is a downstream Godot-side milestone gate, judged at Matt's eye (desirable-run-pattern § 6 obs. 2 — the owner's eye as instrument of record), NOT this run's emit gate.

KC2-SIM's pre-registered gate set is otherwise untouched.

---

## § 3 — Rider 2 (APPROVED): threat-grammar companion lap — separate parallel commission, NEVER KC2 scope

Blocks the **playtest milestone**, not the emit. Fires from the **main session** (lifecycle durability — background agents die with their spawning session). Two named briefs:

**galadriel — frame-level threat-grammar extraction (WR3-shaped, pointed at KC2's own roster):**
- Substrate: s1 footage (41.6 min + 142 screenshots) + s2 (1,034 s 1920×1080@60), `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-1/` + `eor-test-2/`.
- Per monster family in the encoded run's roster (prioritize the specified run's waves once Matt's top-3 pick lands): attack wind-up duration, recovery duration, telegraph shape + duration, attack cadence (attacks/s in contact), root-lock fraction while attacking, approach speed at contact.
- Output vocabulary = WR3's (2026-07-30 referent-extraction precedent: Primordian 0.489 s wind-up / 0.879 s recovery, 0.80 s nova telegraph, root 79.6%). Provenance per measurement: MEASURED-FRAME / ESTIMATED / NOT-OBSERVED (a family that never landed a visible attack on camera is NOT-OBSERVED, declared, never interpolated).
- Attempts labeled; frame timestamps cited; the fixture's ONE death (s1) gets a dedicated forensic pass — the highest-information threat event in the substrate.

**legolas — Edition-III `.arz` attack-timing field join:**
- Corpus: `~/Games/vendor/grim-dawn-edition-III-20260808/` (the cut this session landed; pins 8/8 verified). Note KC2-SIM's sim tables are Edition-III-measured already (stat fold) — same edition, no cross-edition hazard.
- Question: which timing parameters are DB-resident at all (attack speed, animation refs, cooldowns, projectile speed) vs animation-baked (`.anm`, likely needing the frame lap)? Map the boundary explicitly — the boundary IS a finding.
- Join target: the same 968-record roster basis as `t22_band_a_monster_stats.csv` (SHA `0d6992e8`), so the threat-grammar table extends the existing board rather than minting a parallel one (#67 name-is-a-pin; namespace guard).

**Fold target:** a per-family threat-grammar table consumable by drax's Godot runtime alongside the baton — the companion artifact Rider 1's declaration points to.

---

## § 4 — Rider 3 (APPROVED): G-STATS offense clause + declared absence

Spec § 11 G-STATS amendment (conductor-owned spec; main-session SPEC-AUTHOR beat, `⚠ SWITCH` beat applies):

1. **Restate the gate in reading-(i) terms** — the *"folded into the sim's kill term"* sentence is superseded by: *"emit BLOCKS unless every encoded wave's roster (incl. summon bodies) carries MEASURED combat stats — eHP AND swing damage — shipped ON the baton roster rows."* (The kill-term fold remains true and cited, but is no longer the gate's predicate.)
2. **Offense clause:** the gate checks measured swing-damage fields ride the roster rows. **Passes today by measurement** (953/968; residuals priced per § 1).
3. **Declared absence:** attack-timing grammar ships `NAMED-ABSENT-DECLARED` on the provenance block with the Rider-2 pointer. Block on what the frozen substrate measures; declare what it cannot. Incoming-damage remains OUT of model, declared (`player_hp` FLAT; `monster_attack_model: abstract-schedule` — unchanged).

---

## § 5 — Red-full-tree: ruled, does not gate emit

Matt's word: *"red tree does not gate emit."* The 63 failed / 21 error full-tree results (HB-8 substrate fact, L-71(i)) do not gate the baton emit: they appear in no pre-registered gate (adding one post-hoc = goalpost-moving in reverse), the emit path's own suite is green (smoke 244/0; export 1,124/24 modules), and A/B control proved the run caused none of them. The HB-8 **naming enumeration proceeds regardless** inside gamora's repair bundle — ruled non-gating, not non-work.

---

## § 6 — Main-session execution checklist (the beats this ruling commissions)

1. **Verify the queue strike read** (`canonical/matt_decision_needed/README.md`, Q52 row struck 2026-08-08).
2. **Ledger fold:** record this ruling with the next R-KC2 number, citing this note; fold the § 1.1 rationale so the run inherits the reasoning, not just the verdict.
3. **Spec § 11 amendment** per § 4 above (SPEC-AUTHOR beat).
4. **Queue the § 2 declaration text** for Phase-E G-E execution (handoff note + provenance block).
5. **Fire the § 3 commissions** (galadriel + legolas, named, background) — parallel track reporting into the Godot playtest milestone, NOT into KC2 gates.
6. **Proceed on the ruled sequencing (R-L68-3, now fully unblocked):** gamora repair-bundle fold → Phase-E seeded batch (FULL-capable, post-fold clear-times, SHEET-limb declaration riding) → top-3 → **Matt's pick (R-KC2-5/6, his last touch)** → emit under G-STATS-as-amended + G-ARENA-REF + star-lord pre-emit.

**Push:** this note + the queue strike ride one meta commit; push per R-KC2-10.
