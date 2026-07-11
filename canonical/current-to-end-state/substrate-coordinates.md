# Substrate Coordinates — the full kit-design search space

> **STATUS:** MATT-FACING · LIVING — born 2026-07-11 per Matt directive: *"We need both a full
> substrate coordinate page for kit design search and we also need a full mechanical reality page
> for the build out when exploring each new kit."*
>
> **PURGE-EXEMPT:** Matt-consumption surface — never folded, retired, or purged without Matt's
> explicit ruling (form-precedent: the pipeline docs, 2026-07-10).
>
> **Maintenance law — SAME-COMMIT:** the commit that lands coordinate-changing work (new axis, new
> cell, new pin/mask, archive change) updates this page in the SAME commit (rocket: sampler/catalog ·
> gamora: archive/fingerprints · gandalf: doc owner + ruling stamps).
>
> **PAIR LAW:** this page = **WHERE a kit sits in design space** (search). Its twin
> `mechanical-reality.md` = **WHAT the engine can express** (build-out). Exploring a new kit reads
> BOTH: sample the coordinate here → verify every mechanical surface the kit touches there.
> **Glance:** candidate page (contract amendment — KR sequences; drax builds).

**Siblings:** `pipeline-serial-content-emission.md` (E0 is this page's pipeline stanza) ·
`pipeline-battle-sim.md` · `mechanical-reality.md` (the pair twin). **Roster of record:**
tracker PART F (25 K + 6 H = 31 denominator; F.3 bench outside it), rendered at Glance `/kits`.

---

## §1 — The operational catalog (GENERATION space of record)

**Six coordinates, 972-cell lattice** (4 × 3⁵; was 324 before `bc_commitment` joined per Q-E4-4b):

| Coordinate | Arity | Values / note |
|---|---|---|
| `bc_attribute` | 4 | STR / DEX / INT / WIS — drives element pool (`STAT_ELEMENT_POOLS`: STR → physical; INT 4-pool; WIS 3-pool; DEX 8-pool) + scaling stat (per-chain law incoming, E3) |
| range | 3 | close / mid / long |
| tempo | 3 | kit cadence bin |
| amplitude | 3 | flat / mid / spiky |
| `proxy_density` | 3 | none / light / heavy — mechanical substrate staged P0/P1/P2 |
| `bc_commitment` | 3 | instant / wind-up / channel (E4; attack slots carry the bin per slot law Q-E4-1b; T4 may transform — expressed-coordinate cert) |

**Sampling:** `bc_target_cell_sampler.py` — **25 named CellDefs** (PART F's K-numbers) in the 972
space; couplings cut the live space (flat×wind-up + spiky×channel hard cuts · charge-stack ≠ wind-up
boundary · proxy-channel tether-only · dodger×channel conditional · summon-act fifth scope row).
**Option C cross-attribute tuple: RETIRED** (E3 ruling 2026-07-10 — deletion in the E3 dispatch;
physical-as-element does the Spellsword's job).

## §2 — The QD archive (MEASUREMENT space of record)

**8 axes · 68,040 full / 12,960 live** (`qd-engine-bc-axes-lock-2026-05-20.md`). The archive is the
gauntlet's measurement spec: every certified kit lands as a **behavioral fingerprint** — the vector
of gauntlet-MEASURED behaviors (what the kit actually did under R1–R5), not its declared coordinate.
The QD/MAP-Elites planner searches over fingerprints; the catalog (§1) is what generation SAMPLES;
the archive is what measurement FILES. Catalog ≠ archive is load-bearing (the F-3 lesson).

**NINTH AXIS — commitment-behavior: ⚑ PRIORITIZED (Matt, 2026-07-11)** — *"let's prioritize the
ninth axis as we move towards the content emission."* Supersedes the ADOPT+DEFER sequencing (E4
addendum §D.1/fork F-3, arity stress-test formerly parked): the **arity stress-test moves up** as the
admission gate (rigor unchanged — the test still decides bin count + archive-size math before
commitment joins as axis 9). Sequencing: KR slots it alongside the E3 dispatch window, ahead of the
batch-2 derivation population so the archive measures commitment-behavior from the emission's first
full population. Owner: gamora (measurement) + rocket (archive plumbing); gandalf design-stamps.

## §3 — Per-cell constraint layer (pins · masks · bands)

| Layer | What it does | State |
|---|---|---|
| **Anchor pins** | pin a cell's identity fields (e.g. K1/K7/K19 commitment pins; K15 element pins below) | E4 pins RULED; E3 pins RULED |
| **`hybrid_affinity` masks** | per-cell constraint at SAMPLING, before binding (e.g. carrier ⇒ emission slot present; kit spans ≥2 geometry classes for `geometry_partition`) | E3 dispatch build |
| **Rate bands** | `element_application.rate_band ∈ {splash, co_equal}` — realized-share law, certified by measurement (attribution spine is the instrument) | RULED; spine = v1-BLOCKING build (star-lord) |
| **Global dial** | `HYBRID_RATE` (0.175 today) → governed dial | E3 dispatch build |

**Element pins RULED (2026-07-11, K15/H5 disposition):** **K15** pins `chain_partition` + `co_equal`
+ the scaling-unification T4 at v1 (magical-primary + physical-secondary — the Spellsword) ·
**K20/K23** pin `splash` (physical-primary + holy-secondary) · **H5 re-homes to the blend family**
(`flat_split`) at v2 — "true dual = H5" preserved under new vocabulary. Breadth price =
**SIM-MEASURED** (pinned four + mono control through gauntlet, counter-breadth matrix,
mono-resist/mixed-defense/armor-heavy regimes); 10–15% is a prior, not a ruling.

## §4 — Adjacent substrate wells (E0 canon this search draws on)

| Well | Shape | State |
|---|---|---|
| **Race well** | 5 races × 4 registers = up to 20 identity cells; LLM never derives races | CLOSED/CURATED; Leg-3-ready (Q17) |
| **Mob-affix families** | 8 functional families; model-visual telegraph channel (E10 §7) | RULED |
| **Motion-frame axes** | seven-axis family F1–F6; defining-vs-flavor cell classification | RATIFIED; staged consumers |
| **Axis-5 cost-TYPE bins** | reserved-empty — the bench B1–B3 blockers | RESERVED |
| **Proxy-behavior axes** | archetype/lifecycle/scaling/command/attribution; P0/P1/P2 staging | RULED |

## §5 — Search semantics (how a kit exploration runs)

1. **Pick or derive the coordinate** — a cell in the 972 lattice (named CellDef, H-series hypothesis,
   or bench candidate awaiting its blocker).
2. **Check the constraint layer** (§3) — pins the cell must honor, masks that gate structure
   eligibility, rate band if hybrid.
3. **Flip to `mechanical-reality.md`** — verify every mechanical surface the kit touches is LIVE (or
   accept the build ladder's gate for what isn't).
4. **Emit → certify** — the pipeline samples (E1–E3), the sim certifies at the EXPRESSED coordinate
   (E4–E5), the fingerprint files to the archive (§2).

The search space says what a kit IS; the archive says what it DID; the mechanical page says what the
engine CAN. Design conversations that conflate the three re-litigate the F-3 confusion — cite the
page you mean.

---

**Signed:** gandalf, 2026-07-11. Drill-throughs: `qd-engine-bc-axes-lock-2026-05-20.md` ·
`motion-frame-substrate-amendment-2026-07-09.md` · `bestiary-race-well-design-2026-07-09.md` ·
`mob-affix-system-spec-2026-07-09.md` · E4 design note + runtime addendum · element-application
addendum · the scaffolding audit (gandalf notes, 2026-07-11).
