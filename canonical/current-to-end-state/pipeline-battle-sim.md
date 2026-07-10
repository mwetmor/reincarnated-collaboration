# Battle Sim — End-to-End Product Pipeline (desired end state, current-state stamped)

> **STATUS:** MATT-FACING · LIVING — born 2026-07-10 per Matt directive: *"What I need are the
> desired-state end-to-end pipelines of the actual products… I want to see what the battle sim
> consumes and what it does every step of the way."*
>
> **PURGE-EXEMPT:** this doc class "keeps getting hidden, probably because they're of use to me but
> not the rest of the team" (Matt, same directive). This doc is a **Matt-consumption surface** — it is
> NEVER folded, retired, or purged without Matt's explicit ruling. Form-precedent:
> `../reap-die-rise-engine/39-qd-engine-end-to-end-workflow-2026-05-24.md` §1 (right form, stale
> content — that doc predates the full-run pivot, E1/E2/E4, and the Godot seam).
>
> **Maintenance law:** gandalf owns the doc. Stage-state stamps (**LIVE / PARTIAL / GAP**) update when
> owning agents land work (gamora: S1–S7 · rocket: S0 inputs · star-lord: S5 telemetry + S8). The
> desired end state is the SPINE; the current state is the STAMP; the gap column links tracker rows —
> state derives from the queues, not from prose. Glance `/engine` page renders this doc (contract v1.6).

**Sibling:** `pipeline-serial-content-emission.md` (the factory that FEEDS this machine and consumes
its verdicts). This doc is the certification machine itself.

---

## FLOW (end-to-end at a glance — Glance shape, contract § 2.7)

1. **S0 Inputs** — kit bundles · encounter specs · mob/race rows
2. **S1 Spawn & arena init** — actors, positions, proxies
3. **S2 Decision loop** — readiness, targeting, AI policy
4. **S3 Cast & motion resolution** — commitment (cast-time), trajectories, motion-frame kernel
5. **S4 Hit & damage resolution** — hit kernels, amplitude k, ailments, resources
6. **S5 Fight termination & telemetry** — outcomes, KPM, floor guard
7. **S6 Gauntlet batch runner** — R1–R5 regime families, regime-mix law
8. **S7 Band fit & certification** — fairness bands, expressed-coordinate cert
9. **S8 Outputs** — cert records → registry → feeds → downstream consumers

## The visual flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ S0 · INPUTS (from the emission pipeline — sibling doc stage E4 handoff) │
│  • kit bundle: per-skill JSON — cooldown_seconds, cast_time_seconds,    │
│    damage bands, geometry keys (20 live), element/attr, T4 capstones    │
│    w/ (commitment_bin, amplitude_delta) declarations                    │
│  • encounter spec: R1–R5 beat-family regime + mob population (§3)       │
│  • mob/race rows: E10 race×register kits + affix profiles               │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S1 · SPAWN & ARENA INIT (gamora)                                        │
│  concrete-positional arena · straight-line nav · actor spawn            │
│  proxy actors: P0 emitters / P1 stationary+HP / P2 mobile minions       │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S2 · DECISION LOOP (per tick, per actor)                                │
│  readiness gate (cooldowns; E4 adds commitment cost) · targeting        │
│  (scalar-distance; P1 adds mob aggro-CHOICE) · AI policy per kit        │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S3 · CAST & MOTION RESOLUTION                                           │
│  snap fires instant · wind-up delays damage to cast COMPLETION against  │
│  positions AT THAT TIME (motion-whiff) · channel = sustained lock       │
│  motion-frame kernel: E1 geometry (20 keys) + rotational family (ω,     │
│  dr/dt, frames) · nova/spin compile-layer migration (audit-gated)       │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S4 · HIT & DAMAGE RESOLUTION                                            │
│  hit kernels (AoE symmetric per Q1 — perception edge is piloted-Godot   │
│  layer, NOT sim) · amplitude k fan-out (E2 — the spiky/flat identity)   │
│  ailments/control · resource costs (Axis-5 cost-TYPE bins reserved)     │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S5 · FIGHT TERMINATION & PER-FIGHT TELEMETRY (star-lord boundary)       │
│  outcomes via HP · per-fight events, KPM · clear-time floor guard       │
│  (de-censors the instrument)                                            │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S6 · GAUNTLET BATCH RUNNER (the certification instrument)               │
│  four-family run-beat regimes R1–R5 · density targets §3 (perf-spike    │
│  PASS) · REGIME-MIX LAW: cert suite MUST sample mobile regimes where    │
│  wind-ups genuinely whiff (else commitment premium = free money)        │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S7 · BAND FIT & CERTIFICATION                                           │
│  encounter-KPM bands at declared baseline (re-fit CERTAIN at each new   │
│  baseline; ONE re-anchor at END of axis run) · fairness ε bands ·       │
│  EXPRESSED-COORDINATE CERT: T4 transform declarations verified by       │
│  measurement (mismatch = cert fail) · accept / reject / __null__       │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ S8 · OUTPUTS                                                            │
│  cert records → emission-run registry → feed-2 snapshot → Glance /kits │
│  band sheets → loot campaign · telemetry DB → design audits            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Stage detail (consumes / does / emits / state)

### S0 · Inputs — **PARTIAL**

**Consumes:** the emission pipeline's certified hand-off (sibling doc E4). Three input classes:
**kit bundles** (per-skill emitted JSON — `cooldown_seconds`, `cast_time_seconds` (tier map
`per_skill_emitter.py:194`), damage bands, geometry keys, element/attribute, T4 capstone declarations);
**encounter specs** (R1–R5 beat family + population densities); **mob/race rows** (E10 mob kits over
the race well).
**State:** kit bundles LIVE (batch-1 fixture bank `w3_batch1_bundle.json`; batch-2 derivation
population owed) · `cast_time_seconds` emitted-but-never-read (E4 GAP — the sim consumer is the E4
build) · mob-affix rows not yet built (E10 Leg 3, race well Leg-3-ready).
**Drill-through:** `../reap-die-rise-engine/mob-affix-system-spec-2026-07-09.md` ·
`../reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md` ·
`agentic_orchestration/gandalf/notes/2026-07-09-e4-casttime-axis-fork-elicitation.md`

### S1 · Spawn & arena init — **PARTIAL**

**Does:** concrete-positional arena; straight-line nav (`spatial_engine.py:1170`); `ChokeZone` is the
only terrain object — the space is obstacle-free (Walls = named future spatial-layer workstream, Q15).
Proxy actors are the staged build: **P0** parametric emitters (ride the motion-frame kernel — the
totem sim-liveness probe G1 is the first P0 certification) · **P1** stationary + targetable (HP, mob
aggro-choice) · **P2** mobile autonomous minions (nav + attribution + command verbs).
**State:** LIVE for player+mob actors · **GAP: zero proxy actors today** (verified — `spatial_engine.py`
has no proxy handling; `ProxySpawn` is generation-side only).
**Drill-through:** `../reap-die-rise-engine/motion-frame-substrate-amendment-2026-07-09.md` (P0/P1/P2
staging, §7 premise record) · Q15 Walls: mob-affix spec §5.1.

### S2 · Decision loop — **LIVE (scope-current)**

**Does:** per-tick readiness gate (`spatial_engine.py:1281`) — cadence derives from
`cooldown_seconds` alone today; targeting by scalar distance (`:1017` — mob targeting knows only THE
PLAYER; P1 adds aggro-choice); AI policy per kit (ai_strategies — the rotational family lands as ONE
kernel here).
**End state adds:** commitment cost in the decision itself — choosing a wind-up is choosing risk
(Q-E4-2b THROUGHPUT-ACTIVE).
**State:** LIVE · E4 consumer GAP · P1 aggro-choice GAP.

### S3 · Cast & motion resolution — **PARTIAL (the E4 build lands here)**

**Today:** damage applies at selection instant (`:2402`); every skill is a snap — the game has no
weight of commitment.
**End state:** three commitment bins (`bc_commitment`: snap / wind-up / channel). Wind-up delays
damage application to cast COMPLETION **against positions at that time** — the sim has real positions,
so wind-ups genuinely whiff against mobile targets (the v1 risk channel: motion-whiff +
fight-truncation + channel-lock; damage-interrupt = named v1.1). Motion-frame kernel resolves
trajectories: E1 geometry (20 keys LIVE, 11–12 geometries/kit) + the rotational seven-axis family
(frame/ω/dr\/dt/count/persistence/collision/emission; nova + spin compile INTO the kernel as
degenerate points, behavior-preserving, conservation-audit gated).
**State:** E1 LIVE ✓ · E2 LIVE ✓ · **E4 GAP** (all six forks RULED; design note next; rocket+gamora
dispatch pair follows) · **rotational GAP** (G2 kernel math note owed).

### S4 · Hit & damage resolution — **LIVE (core), named reserves**

**Does:** hit kernels (`:779-839`, occluder-blind — Walls dependency); AoE resolves SYMMETRICALLY
(Q1 ruling: no perception constants in sim; the player's perceptual edge is a piloted-Godot
layer-handoff, controller-keyed); amplitude k fan-out (E2 ✓ — encounter-layer fan-out ruled AS the
spiky/flat identity reaching the encounter layer, Q14); ailments/control; resource costs.
**Named reserves (bench blockers live here):** Axis-5 cost-TYPE bins — HP-spend (blood magic),
damage-taken-converts (thorns), charge-state (builder-spender) are resolver plumbing, reserved-empty
with F5 re-entry (bench rows B1–B3).
**State:** LIVE · reserves named-not-built by design.

### S5 · Fight termination & telemetry — **LIVE**

**Does:** outcomes resolve via HP (draws ≈0.06%); per-fight event stream + KPM to telemetry
(star-lord seam); clear-time floor guard de-censors the KPM instrument (Q14 remedy, Gate-2 PASS).
**Known telemetry debts:** `engine_version`, `termination_reason` (sidecar-analysis findings).
**State:** LIVE + guard landed.

### S6 · Gauntlet batch runner — **RATIFIED SPEC, build in lane**

**Does:** the four-family run-beat instrument (R1–R5) drives batch certification; density targets §3
(drax perf spike PASS — re-open trigger not tripped); **regime-mix law** (Q-E4-5 guard 2): the cert
suite MUST sample mobile regimes where wind-ups genuinely whiff — commitment premiums are priced from
measured completion/whiff rates, so a stationary-only gauntlet would make the premium dishonest.
**Drill-through:** `../reap-die-rise-engine/gauntlet-run-beat-families-spec.md` (RATIFIED R1–R5).
**State:** spec RATIFIED · gamora build in lane · regime-mix law enters with E4.

### S7 · Band fit & certification — **LIVE bands; two new laws entering**

**Does:** encounter-KPM band fit at the declared baseline (arm-G; bands STAND per C3; **re-fit is
CERTAIN at every declared baseline** — full-run pivot rule 4; **ONE band re-anchor at the END of the
axis run**, post-E3/E4 + orbital/proxy dialects, on the de-censored instrument — Q14 iii); fairness ε
bands; kit-grain certification (GRAIN mode).
**Two laws entering with E4:** (1) **expressed-coordinate cert** — every T4 capstone declares
`(commitment_bin, amplitude_delta ∈ {none, flatten, invert})`; a rhythm-inverting channel capstone
flips the kit's EXPRESSED post-T4 coordinate spiky→flat and cert fires at the expressed coordinate;
the measured band must CONFIRM the declaration (mismatch = cert fail; the substrate votes; the
generation cell / roster K-number stays stable — precedent: the K13→K12 artillery fold). (2) **priced
premium** — wind-up/channel throughput premium derived from measured whiff/completion rates; expected
band center stays in tolerance; VARIANCE carries the fantasy (D3-Inferno unpriced wind-ups = dead
skills; PoE priced slams = real archetype).
**State:** bands LIVE (current instrument) · expressed-coordinate + priced-premium laws enter with the
E4 design note.

### S8 · Outputs — **feed named, export owed**

**Emits:** cert records → star-lord **emission-run registry** → **feed-2 snapshot**
(`agentic_orchestration/run-registry/emission-runs-snapshot.json`) → Glance `/kits` per-kit machine
truth (auto-updates on push); band sheets (the loot campaign inherits them; Q10's resist/mitigation
caps ride the band-sheet); telemetry DB → design audits (the ~24×24 grouping matrix doubles as the
counter-breadth/matchup-topology measurement).
**State:** registry feed NAMED (contract §7.1 feed-2) · star-lord export owed · Glance consumer wired.

---

## Gaps at a glance (stage → owed work → tracker home)

| Stage | Gap | Owner | Tracker home |
|---|---|---|---|
| S0/S3 | E4 sim consumer (`cast_time_seconds` read + motion-whiff + channel-lock) | gamora (+rocket emitter side) | engine tracker — E4 row; design note next |
| S1 | proxy actors P0→P1→P2 | gamora | engine tracker — proxy family (E6-adjacent) |
| S1/S4 | Walls / blocking geometry (obstacle nav + occlusion) | named future workstream | mob-affix spec §5.1 (Q15) |
| S2 | P1 mob aggro-choice | gamora | proxy staging |
| S3 | rotational kernel (G2 math note → build) | gamora+rocket | motion-frame amendment gates |
| S6 | gauntlet build + regime-mix law | gamora | gauntlet spec §11 |
| S7 | expressed-coordinate cert + priced premium | gamora | E4 design note (gandalf, next) |
| S8 | registry snapshot export (feed-2) | star-lord | Glance contract §7.1 |

**Signed:** gandalf, 2026-07-10. The sim is the court: every kit that ships was tried here, and the
verdict is measured, not asserted.
