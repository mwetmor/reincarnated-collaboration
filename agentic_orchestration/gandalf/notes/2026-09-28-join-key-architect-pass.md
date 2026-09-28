# The join key — ARCHITECT pass: from arena replica to the substrate other kits join

> **STATUS:** CURRENT — ARCHITECT pass (open-questions gate) for the successor to Run KC2-PLAY. **Not a charter; nothing fires from this note.** It sets the course, records one Matt ruling, and gates the rest.
> **Date:** 2026-09-28 · **Author:** gandalf (`ARCHITECT`) · **Authority:** Matt's session ask + ruling **R-J1** (§ 1), recorded in the KC2-PLAY ledger as **KP-82**.
> **Builds on (does not replace):** `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` (one substrate, many masks; three layers; fidelity grades; E-1/E-2 open) · TRUE-SOURCES rulings TSR-2/3/4 (`gandalf/notes/2026-07-23-true-sources-grill-brief.md` § 4) · `gandalf/notes/2026-09-21-the-commission-rule.md` (Failure Mode 2) · KC2-PLAY charter + ledger `gandalf/notes/2026-09-20-kc2-play-run-charter.md` and hand-off `agentic_orchestration/skill_handoff_2026-09-24.md`.

---

## 0 · The ask, in Matt's words

> *"I am interested in picking up on and completing the EOR warlord arena simulation work. … finish making this as a join key to being in other kits from other ARPGs by first testing out its viability as an arena replica and then tweaking the replica until it sits in between our games and contains what is needed to join the other kits in."*

Two steps, in order: **(1) prove the replica, (2) move it to the middle.** The ruling below settles what "the middle" is.

## 1 · R-J1 — the ruling (Matt, 2026-09-28, class `matt`)

> *"Between grim dawn and the other games.. then we leave levers open specifically to be tweaked as we go to reach our own version of fun."*

**What it settles:**
- **The middle sits between Grim Dawn and the other roster games** (corpus-of-record D2 / PoE1 / PoE2; LE parked; annex games at attested grade), **not** between Grim Dawn and our own spec. Our element / resource / stat spec is **not** the target of the tweak. It becomes one later *setting* of the middle, not its shape.
- **Our own fun is reached AFTER, through levers left open on purpose.** The middle does not pre-decide the house game's numbers. It exposes the knobs and leaves them at a known setting until play says otherwise.

**What follows from it (conductor reading, veto-open):**
- The **archive-frame element-courts (k = 5)** qualify as a *candidate* middle, because they were derived from the corpus's `elem_raw` across games rather than authored for our spec. They are tested in B1 like every other candidate, not presumed.
- **Lean on Q86 (below):** "in between" is a property of the **mechanism**, not of the **numbers**. Where a Grim Dawn mechanism cannot express another game's kit (hit chance only as OA/DA, energy as the only resource, GD's damage-type list), the middle **generalises the mechanism** so that GD's rule is one setting of it. The Grim Dawn settings stay the default, because they are the only known-fun, validated setting we hold (Matt's overrule of Failure Mode 1, KP-71). Averaging numbers across games is meaningless before cross-era power normalization (E-1) exists.

## 2 · What is on disk — two systems that have never touched

| System | What it is | Where |
|---|---|---|
| **KC2 referent** | Python oracle (58 modules, ~45k lines, "no free parameters"), baton packs v3.0–v3.3 plus the v3.4 lifted rows (not yet cut into a pack), GDScript runtime (13.3k lines, one runtime with `ORACLE` and `PLAY` configs, 28-row divergence register), and the playable `.app` | `reincarnated-engine/src/reincarnated/simulation/kc2/` · `…/export/kc2_baton_*` · `reincarnated-godot/kc2_runtime/` · `…/desktop/KC2Play/` |
| **Cross-game kit layer** | `corpus.db` (590 kits / 21 games), the GD-SLICE exact-fields schema (107 core + 29 GD-extension; **template lock never landed**), the kit compiler, and the `kits-export/` JSON (includes **`gd-eor-warlord.json`**, APPROX grade) | `agentic_orchestration/research/curated/` · `reincarnated-engine/src/reincarnated/simulation/kit_compiler/` |

**Nothing in the KC2 oracle, pack emitters or runtime references `corpus.db`, a `kit_id`, `kits-export` or `kit_space`.** KC2 reads Grim Dawn records straight from the Edition-III archives. The join key is, concretely, **the connection between these two systems.** That is Failure Mode 2 made physical.

Also material:
- **Three grade vocabularies coexist** in KC2 (the oracle's `Cited` grades, the pack's `GRADE_ENUM`, the row-level `precedence`), beside the era-substrate law's MEASURED / DATAMINED / MODEL-VERIFIED / AUTHORED.
- **The unit convention** `kf2-rdr-normalization-convention.md` ("one RDR point = one source-game point, ×1.0") cannot hold in a shared arena where D2 and PoE numbers differ by orders of magnitude. That is E-1.
- **The runtime tests hard-code the v3.3 pack**; nothing references v3.4 yet.

## 3 · The architecture — one substrate, a lever registry, profiles

Four terms, used exactly:

- **Primitive:** a game-neutral mechanism the runtime executes: a resource pool with income / spend / decay / reservation laws; a hit-chance rule; a mitigation stack; a damage packet carrying a type tag; channel, cooldown, charge; summon; aura; proc / trigger.
- **Adapter:** per-game translation from source records into primitives (TSR-2). **Grim Dawn is adapter #1** (TSR-3).
- **Lever:** a named, typed, bounded parameter of a primitive at which the roster's games differ, or which the ablation map shows moves feel. **Levers are DISCOVERED, never authored by hand** (Discipline #41: the substrate votes). There are three sources: the KC2 divergence register (20 `DIV` rows already are levers in all but name), the ablation map (the bridge, § 4), and the B1 schema-pressure census.
- **Profile:** a vector of lever settings. The **GD-REFERENT profile** is REFERENT-v1 exactly. **Era profiles** (era-substrate § 5) are profiles. **The house profile, "our own fun", is a profile.** One mechanism serves all three.

**Lever row (the registry schema, proposed):** `id` · concept · primitive parameterised · **GD-referent value + grade** · per-roster-game value + grade (DATAMINED / MODEL-VERIFIED / attested) · allowed range · **feel sensitivity** (Δ in each feel metric per unit, from ablation) · **load class** (LOAD-BEARING / INCIDENTAL / UNMEASURED) · **status** (**OPEN** by default; SET only by ruling) · authority.

**Two invariants make it safe to tweak:**
1. **Golden master.** The GD-REFERENT profile, run through the GD adapter and the primitives, must replay REFERENT-v1 on every EXACT row, forever (the forward-architecture contract's golden-master law). A lever change that breaks that replay is a regression, not a design choice.
2. **Levers open, not tuned.** R-J1 says so directly. No lever leaves `OPEN` without a ruling, and no LOAD-BEARING lever moves without Matt's word.

## 4 · The plan

### Phase A — REFERENT-v1: prove it is the fight, then seal it (finishes KC2-PLAY)

1. **Unblock:** Q85 (graded-run cap reset) · T30 (mount the `reincarnated` volume) · gamora's prereg **v1.6** re-derivation (hand-off § 4.1) · **cut v3.4 into a pack** and move the runtime onto it.
2. **Close the feel defects:** per-cast energy costs (C-2's 43.2 / 27.9 / 106.2 / 59.4; the pack charges zero) · `OPEN-UNKILLABLE` (C-6) · enemies stuck in the spawn zone · the nine campaign-attack records (hand-off § 4.2).
3. **Three tiers:** **T-A** port ≡ oracle · **T-B** Matt's telemetry vs his footage · **T-C** Matt's eye, "does it feel like my video" (HITL; no instrument decides it).
4. **Seal REFERENT-v1:** pack digest + runtime digest + register hash + T-A grade + T-B statistics + Matt's T-C word. This is the golden master of § 3.

### Bridge — the ablation map: why it is fun

The commission-rule residue: *"a referent tells you THAT it was fun, not WHY."* The one-runtime-two-configs machinery answers it. Switch off one mechanism at a time (leech, energy drain, OA/DA, devotion procs, summons, pools, hazard aprons…) under the scripted pilot, and measure the feel metrics already instrumented: HP occupancy, energy excursion depth and ceiling duty, wave durations, frac-moving, terminal wave. The output is **every mechanism classed LOAD-BEARING or INCIDENTAL, with a number.** It is also the **Grim Dawn signature-feel checklist (E-2) obtained by measurement** rather than by assertion.

### Phase B — move it to the middle

- **B0 · Self-join.** Compile `kits-export/gd-eor-warlord.json` through the kit compiler into the arena and compare it against REFERENT-v1: **same kit, same fight, known answer.** Whatever the corpus path loses is exactly what the shared schema lacks, measured against ground truth. This is the cheapest test of Failure Mode 2 we will ever get.
- **B1 · Schema-pressure census (paper, zero code).** Express one kit per corpus-of-record game, plus one structurally alien annex kit, in the primitives. Every concept with no home is a primitive to generalise; every value that differs is a lever. The kit slate is Q88.
- **B2 · Adapter refactor.** Grim Dawn moves behind adapter #1; the runtime reads primitives; the golden-master gate runs on every commit.
- **B3 · Lever registry v0.** Seed it from the register, the ablation map and the B1 census. **All levers OPEN at their GD-referent setting.**
- **B4 · Power normalization (E-1).** Required before any foreign kit can be graded in the arena.
- **B5 · The proof.** Join kit #2 for real, then a structurally different kit #3, each graded at its own lane's fidelity grade. **The join key is demonstrated when two foreign kits land inside their home bands.**

### Phase C — our own fun (out of scope here, named so it is not forgotten)

The house profile: levers moved by playtest, each move a ruling priced by its feel-sensitivity row. Per R-J1 this happens **as we go**, after the middle exists, never as a precondition of it.

## 5 · Open-questions gate

| # | Decision | State | Lean (one) |
|---|---|---|---|
| R-J1 | Where the middle sits; levers open | **RESOLVED** (Matt, § 1) | — |
| **Q85** | Graded-run cap resets at the v3.4 re-base? | **OPEN — Matt** (already queued) | **YES** |
| **Q86** | "In between" = generalise the MECHANISM, GD settings as default (the GD profile still replays exactly)? | **OPEN — Matt** | **YES**: mechanism, not numbers (§ 1) |
| **Q87** | REFERENT-v1 "viable" = feel-load-bearing EXACT rows green + T-B inside the pre-registered bands + Matt's T-C yes (not all 89 rows perfect) | **OPEN — Matt** | **YES** |
| **Q88** | B1 slate and kit #2 | **OPEN — Matt** | Paper-join D2 WW Barb · PoE1 Cyclone · PoE2 Bonestorm · one cooldown-only annex kit; **real join #2 = D2 WW Barb** (primary `.txt` data, whirlwind-vs-whirlwind, leech-dependent sustain stresses the likeliest LOAD-BEARING lever) |
| **Q89** | Close KC2-PLAY at the REFERENT-v1 seal; charter successor run **JOIN-1** for the bridge + Phase B | **OPEN — Matt** | **YES**: keeps KC2's goalposts clean; JOIN-1 is a new substrate, so a new charter |
| E-1 | Cross-era power normalization | **GATED+TRACKED** — criterion: REFERENT-v1 sealed + B1 census landed | Lean: **matched margin**. Every kit joins at its own progression frontier, scaled until TTK/TTD against KC2's 466 fully offense-lifted reference monsters sit where its home game's frontier does. (The referent is itself an edge-of-capability fight: death on wave 160 after 29.0 s.) |
| E-2 | Per-era signature-feel checklist | **GATED+TRACKED** — criterion: the ablation map | GD's checklist falls out of the bridge by measurement |
| GV | Unify the three KC2 grade vocabularies with the era-substrate fidelity law | **GATED+TRACKED** — criterion: B2 opens | jack-ryan's seam (vocabulary is a discipline surface) |
| TL | GD-SLICE template lock | **GATED+TRACKED** — criterion: B0 + B1 results | The self-join is the evidence the lock never had |

## 6 · What must not happen

- **Tuning a lever before it is measured.** An UNMEASURED lever moved for feel is a fitted constant with extra steps (Law 3).
- **Letting the adapter drift from the golden master.** Every commit on the join path runs the replay.
- **Choosing the lever set by hand.** Levers come from the register, the ablation and the census, never from a list someone found reasonable.
- **Grading a foreign kit above its lane's fidelity grade** (era-substrate § 4: PoE cannot be MEASURED, only MODEL-VERIFIED).
- **Carrying the ×1.0 unit law into a shared arena.** It holds within a lane and fails across lanes; E-1 replaces it at the join.

## 7 · Seats (when chartered)

gamora: oracle, prereg v1.6, ablation runs, E-1 math · star-lord: the v3.4 cut, pack schema generalisation · drax: runtime primitives, adapter refactor, golden-master gate · elrond: `corpus.db` ↔ primitives join, GD-SLICE lock · legolas: commissions under the Commission Rule, foreign-lane anchors · galadriel: T-B footage instrument · jack-ryan: Gate-1 on the JOIN-1 charter, Gate-2 at the REFERENT-v1 seal, grade-vocabulary unification.

---

**Signed:** gandalf (`ARCHITECT`), 2026-09-28. The replica earns the right to be moved by being proved first; the middle earns the right to be tuned by being measured first.
