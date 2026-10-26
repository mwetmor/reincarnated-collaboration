# Join sequencing, kit balancing, and the calibration gap in J4b — design dialogue record

> **STATUS:** CURRENT — **recognition record; architectural commitments deferred** (OP § 3.4). Nothing fires from this note. Every recommendation below is OPEN until Matt rules; the forks are queued as **Q106** in `canonical/matt_decision_needed/README.md`.
> **Date of dialogue:** 2026-10-17 (Pattern B, terminal, Matt ↔ gandalf `ARCHITECT` / `RUN-CONDUCTOR`). **Recorded:** 2026-10-25.
> **Ledger:** KC2-PLAY **KP-508** (`agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`).
> **Builds on:** JOIN-1 charter v0.8.1 (`2026-09-29-join-1-run-charter.md`) · join-key ARCHITECT pass (`2026-09-28-join-key-architect-pass.md`, § 8 governs) · era-substrate canon (`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md`) · doc 50 (`canonical/reap-die-rise-engine/50-bounded-viability-with-specialization-design-directive-2026-05-28.md`) · `canonical/current-to-end-state/pipeline-battle-sim.md` + `pipeline-serial-content-emission.md` · legolas C-13 (`agentic_orchestration/legolas/research/2026-10-14-join1-c13-enemy-anchor/README.md`) · the J4b close-out page `https://claude.ai/artifact/Etw4Hdhjsjn9uqvgks7Lzd` (corrected 2026-10-25).

---

## 0 · Matt's two questions, verbatim

1. *"Maybe it's time to ultra think which systems should be joined in each "join(1,2,3,etc)" and how we will to balance each kit. What are our options? Does it make sense to include portions of our serial content pipeline at this point (I.e. battle sim, iterative balancing mechanisms)?"*
2. *"But what I'm struggling with is how to certify and move beyond the D2 Sorceress when she is over-powered in comparison to the EOR Warlord against its own arena and its own enemies.. I mean I guess that it could be the case that some kits are stronger than others in certain game modes… but does this mean that we should bring over one game mode per game that we join? Would that be a better system? Or should we have brought over more GD kits before joining? I worry that we're making an error with consequences by certifying here without enough thought."*

## 1 · The reframe both answers rest on

- **Nothing past JOIN-1 is defined.** J-L2 (KP-110) folded the Sorceress into JOIN-1; no JOIN-2 charter or slate exists.
- **A join so far is a measurement project, not balancing.** It certifies that a foreign kit's mechanisms run correctly under one boundary rulebook, and records her strength at the enemy-anchored scale (KP-420). J-L3 made every margin **record-only**. The anchored scale normalizes the comparison; it balances nothing.
- **Shipped kits come from the serial pipeline** (engine tracker, Matt: *"They need to be balanced and pipeline emitted… we can pick from a seasonal emission of the serial content pipeline of battle-sim passed kits"*). Foreign kits therefore do two jobs: **they force the rulebook to grow**, and **they are known-fun reference points.** (Era-substrate canon keeps a cross-era homage product possible; that does not change the two jobs.)

## 2 · Which systems go in each join (Q1)

| Cut | What it means | For | Against |
|---|---|---|---|
| By source game | one adapter per join: D2, then PoE1, then PoE2 | clean adapter reuse | our own kits wait behind every foreign game |
| By missing mechanism | next kit = the one that exercises the most still-untouched rulebook rows (energy shield, PoE ailment thresholds, …) | grows the rulebook fastest | a new adapter almost every join |
| By product need | bring our own pipeline kits into the arena | the only join that pays the shipped game; starts the bridge between the two sims | the house kit schema is still moving (E4 cast-time, rotational kernel, band re-anchor) — pin a fixture set |

**gandalf recommendation (OPEN):** JOIN-1 ends with the Barbarian (the D2 pressure the Sorceress did not supply: melee hit chance, physical damage, leech sustain, movement-while-attacking). **JOIN-2 = house join** (3–5 pinned batch-1 pipeline kits through a house adapter, judged against the anchors). **JOIN-3 = PoE**, choosing the kit that exercises the most untouched rows. **Summoners = their own later join** (player allies are out of arena scope today, dockets 2/12).

## 3 · How to balance each kit (Q1)

**Separate power from feel — three dials, three owners:**

| Dial | Controls | Scope | Set by |
|---|---|---|---|
| Rulebook levers | feel | global, never per kit | Matt's playtest (Phase C house profile) |
| Two per-kit scalars (offense, defense) on top of the enemy-anchored scale | power | per kit; mechanisms untouched; distance from 1.0 printed as **fidelity cost** | the sim, tuned to a band |
| Kit-internal numbers | both | **pipeline kits only** (recompose-first loop); never foreign kits | the pipeline |

One runtime then carries two profiles: **Homage** (scalars 1.0 — today's J4b result) and **House** (scalars tuned). The lever-profile machinery already supports this.

**Target = doc 50** (every kit 30–200 % of cohort median per encounter type; 1–2 designed peaks at 1.5–2×; base-DPS spread ≤ 1.5×). Two problems in the arena:
- **One arena = one encounter type.** Tuning everyone to one number there flattens them, which doc 50 forbids. Cheap fix: split the existing ten waves (151–160) into encounter types (boss, hero pack, swarm). A wave-type census comes first; it will likely yield fewer than doc 50's six.
- **Three kits are not a cohort.** Measure relative to the anchor set until house kits fill one out.

**Prerequisite (J-L3):** no tuning until the thresholds are numbers — one ELICITOR session with Matt to translate doc 50 into arena metrics (late-wave damage, survival, intake; band widths).

## 4 · The serial pipeline — what to take, and when (Q1)

- **Take now:** doc 50's targets as the band definition; the iterative tuning loop's *shape* (search two scalars per kit on few runs, reject misses, confirm on the full 25; a 25-run batch is ~20–30 min, so ~one overnight per kit); the gauntlet's encounter-variety idea in reduced form (wave slicing).
- **Not yet:** running foreign kits in the engine battle sim (it has none of their mechanisms — block, potion belt, chill, leech; porting them makes a second rulebook in a second court that will disagree); the recompose-first loop on foreign kits (it edits internals); E3 LLM flavor, E6 registry, E7 curation (irrelevant here).
- **Later — the convergence:** a **two-tier court.** The engine sim ran 118,350 fights in 903 s (~130/s, engine tracker); the arena manages ~1 run/minute and can never certify a 700-kit season. The arena becomes the **reference standard**: run a sample of pipeline kits in both, fit the mapping, let the fast sim certify at volume. The house join is step one.
- **Flagged, not decided:** era-substrate canon builds monster AI once on the GD-validated substrate, and the engine sim's monsters are not that. Full convergence means the engine sim eventually adopts the arena's rulebook and monsters. A Matt-level architectural fork when it arrives.

**Process cost:** J4b took ~two weeks at full rigor; four of its control checks failed by instrument design, not join defect. Proposed: **full grade** for the first kit on a new adapter; **roster grade** (runs clean, golden master green, margin recorded, only new rows graded in full) for later kits on an existing adapter. The KP-312 sealed-runtime protocol is unchanged by either grade.

## 5 · The calibration gap (Q2) — the substantive finding of this dialogue

**What J4b certified:** her mechanics run correctly under the shared rules; the Warlord's sealed fight did not move (G3 25/25, § 4.7, J-S8, P4b all identical). That holds whatever her numbers turn out to be.

**What it did not certify:** that she is balanced, or that ×1.53 measures her strength fairly. No balance claim exists (J-L3).

**The step that carries consequences is KP-420's anchor**, because every D2 kit inherits it, the Barbarian next. Verified against C-13:
- **Her side:** rule **R1** = every Hell area at alvl 85 (Chaos Sanctum, WSK 1–3, Throne, Pit, Ancient Tunnels, …), **players 1**, LoD 1.13 SP/ladder `L-` columns. For a finished endgame Sorceress this is **comfortable farming content.**
- **His side:** GD waves 151–160, **the edge of what the Warlord survives** (18/25).
- The scale therefore maps her comfort zone onto his limit. A large edge with 25/25 survival is exactly what that mismatch predicts.
- **Her home margin was never measured:** KP-166, C-12b DEFERRED (1.13 gives no frontier point; Uber Tristram infeasible because Uber Diablo is fire-immune). The result cannot yet separate *"a stronger kit"* from *"an anchor point that flatters her."*
- Partial reassurance: C-13's damage ratio is biased high (55/70 R1 types carry monster skill damage not computed), but she survived across the whole r_DMG band (×46.98–×97.06), so that bias alone does not explain the edge.

**Correction to the conductor's own close-out (corrigendum-forward):** the 2026-10-16 page named the potion belt as the one measured cause and range / Frozen Armor as likely. **Anchor position is a candidate cause it omitted.** Page corrected 2026-10-25; ledger KP-508.

**Recommended disposition (OPEN — Q106):** J4b is held as **two certificates: EXECUTION granted; CALIBRATION withheld** until the anchor point is checked.

### Matt's three sub-questions, answered

- **One game mode per game?** Yes — as a **fidelity check, not as the balancing system.** Canon already has the cheap version: **era profiles** (D2 monster statlines, data C-13 already extracted, on the GD enemy AI). A D2-Hell mode enables a **2×2** (both kits × both modes), which measures both home margins and shows whether the scale preserves her margin across the boundary — **the certificate the join key is missing.** Grade: AUTHORED/homage (GD's AI wearing D2's numbers), not measured D2.
- **Some kits stronger in some modes?** Fine, and doc 50 wants it (designed peaks) — but a peak means something only against several modes. With one arena, "strong here" and "overpowered" are indistinguishable. **Balancing modes = encounter types that cut across games; per-game modes = home-fidelity checks.** Two different jobs.
- **More GD kits first?** **Partly yes, and the conductor should have flagged it before J4b.** With one GD kit we don't know where the Warlord sits among GD's endgame builds; if GD's strongest are 1.5–2× him at 151–160, her ×1.53 is ordinary. Two or three more GD kits give the in-game spread any cross-game result needs. GD kits are also the cheapest join (adapter #1 exists) and the only lane checkable against the live game (MEASURED grade).

### Proposed order before the Barbarian (OPEN — Q106)

Nothing rebuilds: the scale is two run-time numbers (runner `setting` carries `anchor`, `r_dmg`, `r_hp`).
1. **Anchor-point sensitivity:** re-run her anchored at **players 8** (D2's hardest standard setting; several-fold monster life). One 25-run batch, ~30 min, a lever re-run touching nothing sealed. If her edge collapses, the anchor point dominates and choosing it is Matt's.
2. **A small GD cohort:** 2–3 more GD endgame kits in the same arena, build files Matt picks.
3. **The D2 home-mode test** if 1–2 leave it unclear.
4. **Then the Barbarian**, on a checked scale.

## 6 · What this note does not do

It does not reopen KP-420 (that is option C on Q106 and Matt's alone); it does not move any lever; it does not touch the sealed runtime (`fb49080f…`, godot `4e93fa7`, tag `kc2/referent-v1-sealed-r2-runtime-j4b2s26`); it does not start J4a.

**Signed:** gandalf (`ARCHITECT` / `RUN-CONDUCTOR`), dialogue 2026-10-17, recorded 2026-10-25.
