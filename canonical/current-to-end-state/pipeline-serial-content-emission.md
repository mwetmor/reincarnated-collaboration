# Serial Content Emission — End-to-End Product Pipeline (desired end state, current-state stamped)

> **STATUS:** MATT-FACING · LIVING — born 2026-07-10 per Matt directive: *"I want to see where/how
> the content emission pipeline starts, where it hands off to the battle sim, where it picks up,
> where it calls the LLM via API."*
>
> **PURGE-EXEMPT:** Matt-consumption surface (*"they keep getting hidden, probably because they're of
> use to me but not the rest of the team"*) — NEVER folded, retired, or purged without Matt's explicit
> ruling. Form-precedent: doc 39 §1 (2026-05-24).
>
> **Maintenance law — SAME-COMMIT (Matt condition 2026-07-10: docs hit the mark "as long as they
> will be updated immediately and always"):** gandalf owns the doc; the commit that lands
> stage-changing work UPDATES that stage's stamp in the SAME commit — the §2.7 FLOW-maintenance rule
> extended (owning agents: rocket E2 · star-lord E3/E6 · gamora E4/E5 boundary · drax E8). A build
> landed without its stamp update is an incomplete commit. State derives from the queues
> (tracker PARTs B–F), not from prose. Glance `/content-emission` page renders this doc (contract v1.6).

**Siblings:** `pipeline-battle-sim.md` (stages E4→E5 below hand off INTO and pick up FROM that
machine) · `pipeline-game.md` · `pipeline-story.md` · `pipeline-arcade.md` (POST-LAUNCH mode
factory). **Roster:** the per-kit state this pipeline advances lives in
`current-to-end-state-serial-content-emission.md` PART F (K1–K25 · H1–H6 · bench B-series), rendered
at Glance `/kits`.

---

## FLOW (end-to-end at a glance — Glance shape, contract § 2.7)

1. **E0 Design substrate** ← E0
2. **E1 Emission driver** ← E1
3. **E2 Kit generation** ← E2
4. **E3 LLM flavor pass** ← E3
5. **E4 Handoff → battle sim** ← E4
6. **E5 Pickup ← cert verdicts** ← E5
7. **E6 Bundle + registry** ← E6
8. **E7 Curation gate** ← E7
9. **E8 Godot consumption** ← E8

## The visual flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ E0 · DESIGN SUBSTRATE (canon — gandalf + Matt rulings)                  │
│  BC coordinate space (25 named CellDefs inside the 204,120-cell space   │
│  of record) · race well (5 races × 4 registers, CLOSED/CURATED) ·       │
│  mob-affix families (8) · motion-frame axes (7) · proxy axes (P0/1/2)   │
│  · Axis-5 cost-TYPE bins (reserved-empty)                               │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E1 · EMISSION DRIVER — WHERE THE PIPELINE STARTS                        │
│  full-run pivot: the main line regenerates PER-AXIS (E1 geometry ✓ →    │
│  E2 economy ✓ → E3 hybrid → E4 cast-time → orbital+proxy dialects →     │
│  ONE band re-anchor) · batch-1 = 700-kit fixture bank · batch-2 = the   │
│  derivation population · pilot = standing per-axis instrument           │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E2 · KIT GENERATION (rocket)                                            │
│  cell sampler (25 CELL_DEFINITIONS) → composer (5 skill slots; slot     │
│  law Q-E4-1b) → per-skill emitters (geometry keys, cooldowns,           │
│  cast_time, damage bands) → T4 capstones w/ transform declarations      │
│  MOB-SIDE TWIN: E10 Leg 3 kit-gen consumes ONLY admitted races          │
│  (verified=true rig bindings)                                           │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E3 · LLM FLAVOR PASS — WHERE THE LLM IS CALLED (star-lord llm/ · API)   │
│  templated structure; LLM fills NARROW BLANKS ONLY (names, flavor       │
│  lines — never mechanics; D7 AI-tell law) · culture seeds from race     │
│  rows drive name morphology · faction labels ride S4 order-noun grammar │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E4 · HANDOFF → BATTLE SIM — WHERE THE SIM TAKES OVER                    │
│  bundle enters sibling pipeline at S0 → gauntlet R1–R5 → band fit →     │
│  kit-grain certification at the EXPRESSED coordinate                    │
│  (see pipeline-battle-sim.md S0–S7)                                     │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E5 · PICKUP ← CERT VERDICTS — WHERE EMISSION PICKS BACK UP              │
│  dispositions land on PART F roster rows: PASS → certified · FAIL →     │
│  re-fire · __null__ → Stage-3.5 gap-fill routing · bench rows PROMOTE   │
│  when their named blocker falls                                         │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E6 · BUNDLE + REGISTRY (star-lord)                                      │
│  export artifacts · emission-run registry → feed-2 snapshot →           │
│  Glance /kits per-kit machine truth (auto-updates on push)              │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E7 · CURATION GATE (Matt — the only human hands in the pipeline)        │
│  Matt curates the demo set from the FULL roster (31 rows + bench        │
│  visibility) · curation ≠ authorship (zero-hand-authored law) ·         │
│  GATE1: surface-ledger all-✓ before emission ships to demo             │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ E8 · GODOT CONSUMPTION (drax — One-Realm MVP, THE DENOMINATOR)          │
│  Q7 retarget contract (BoneMaps → GeneralSkeleton) · race-well rigs ·   │
│  Synty register dressing · W4 realm distribution · Camera B′ 20 m       │
│  certifying view · E10 §7 model-visual telegraph channel                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Stage detail (consumes / does / emits / state)

## E0 · Design substrate — **LIVE, growing by ruling**

The canon the factory draws from. The BC coordinate space (25 named CellDefs — PART F's K-numbers —
inside the wider space of record: 68,040 mechanic cells × 3 commitment bins = **204,120** after
Q-E4-4b); the **race well** (5 races × 4 registers = up to 20 identity cells; CLOSED — LLM never
derives races; Leg-3-ready as of the Q17 ruling); **mob-affix families** (8 functional); the
**motion-frame seven-axis family** (F1–F6 ratified); **proxy-behavior axes** (P0/P1/P2 staging);
**Axis-5 cost-TYPE bins** (reserved-empty — the bench B1–B3 blockers).
**Drill-through:** `../reap-die-rise-engine/mob-affix-system-spec-2026-07-09.md` ·
`../reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md` ·
`../reap-die-rise-engine/motion-frame-substrate-amendment-2026-07-09.md` ·
`../reap-die-rise-engine/agnostic-loot-engine-spec.md`.

## E1 · Emission driver — **PIVOT-RULED; per-axis runs firing**

**Where the pipeline starts.** The full-run pivot (2026-07-08) made emission SERIAL and PER-AXIS: the
main line regenerates one texture axis at a time (E1 geometry ✓ landed · E2 economy ✓ closed · E3
hybrid open · E4 cast-time RULED, design note next · orbital + proxy dialects emit post-E3/E4 ·
then the ONE band re-anchor on the full-texture population). Batch-1 = the 700-kit fixture bank
(7 coordinates ×100, `w3_batch1_bundle.json`); **batch-2 = the derivation population** (samples all
25 cells; whether it samples `bc_commitment` or pins defaults = KR sequencing). The pilot is the
standing per-axis certification instrument (completion-build authorized; instrument authority ≠
content authority).
**Gate law:** GATE1 — no emission ships to the demo until the surface ledger is all-✓ (Matt's rolling
Q12 row).

## E2 · Kit generation — **LIVE (player-side); mob-side Leg 3 ready to fire**

`bc_target_cell_sampler.py` (25 CELL_DEFINITIONS; K9 coordinate-drift reconcile owed at batch-2) →
composer assembles the 5 skill slots under the **slot law** (Q-E4-1b: attack slots carry the kit's
commitment-bin identity · control skills take real cast time but don't define the coordinate ·
support fires instant · T4 declares per-capstone) → per-skill emitters
(`per_skill_emitter.py` — geometry keys, cooldowns, `cast_time_seconds` tier map, damage bands) →
T4 capstones carry `(commitment_bin, amplitude_delta)` transform declarations.
**Mob-side twin:** E10 Leg 3 kit-gen consumes ONLY admitted races with `verified=true` rig bindings +
adjectival/culture-seed fields; mob-only kinds never enter the vessel well.

## E3 · LLM flavor pass — **LIVE precedent; the API boundary**

**Where the LLM is called.** star-lord's `llm/` seam calls the API at emission time under the **D7
AI-tell law**: templated structure with the LLM filling NARROW BLANKS ONLY — names and flavor lines,
never mechanics, never raw dialogue at major moments. Culture seeds from the race rows drive name
morphology (orc hard-consonant guttural · elf liquid long-vowel · dwarf stone-compound kennings ·
goblin short guttural chatter · human register-driven); faction labels ride the S4 order-noun
grammar. **Cost precedent:** glyph-flavor Beat B — 35/35 fills, $0.13, in-session key.
**State:** LIVE (Beat B proved the loop) · kit-name + faction-label passes fire with batch-2.

## E4 · Handoff → battle sim — **the seam**

**Where emission hands off.** The bundle enters the sibling pipeline at its S0 and runs S1–S7:
gauntlet R1–R5 regimes → band fit → **kit-grain certification at the EXPRESSED coordinate** (post-T4
transform honored; declaration verified by measurement). Emission does not certify itself — the sim
is the court.
**Drill-through:** `pipeline-battle-sim.md` (this handoff is that doc's entire scope).

## E5 · Pickup ← cert verdicts — **the return seam**

**Where emission picks back up.** Verdicts land on PART F roster rows: PASS → certified (status
flips; Glance `/kits` auto-updates) · FAIL → re-fire under the axis run · `__null__` → Stage-3.5
gap-fill routing (K14's path) · bench rows (B-series) PROMOTE to K/H numbering when their named
blocker falls. Roster statuses are the pipeline's public state — no verdict lives only in a log.

## E6 · Bundle + registry — **export owed (feed-2)**

star-lord exports run artifacts + the **emission-run registry**; the registry snapshot
(`agentic_orchestration/run-registry/emission-runs-snapshot.json`, contract §7.1 feed-2) is the
machine-truth feed for Glance `/kits` — per-kit cert state auto-updates from actual runs, not from
hand-edited docs.
**State:** registry feed NAMED · snapshot export owed.

## E7 · Curation gate — **Matt's hands, by design**

The only human-in-the-loop stage. Matt curates the demo set from the **full roster** (25 K + 6 H = 31,
bench visible alongside); **curation ≠ authorship** — every shipped kit is one the pipeline made and
the sim passed (zero-hand-authored law). GATE1 (surface-ledger all-✓) gates the ship. W4 realm
distribution constrains mob-side picks for the demo realm (elf-native realm; human crusader-stock
common; goblin war-camps in the ravine; orc/dwarf sparse).
**Drill-through:** `surface-ledger.md` (C4/G1 rows) · `../reap-die-rise-game/one-realm-mvp-scope.md`.

## E8 · Godot consumption — **contract live; consumption fires per curated kit**

drax consumes curated kits into the playable surface: Q7 retarget contract (authored BoneMaps →
GeneralSkeleton; `sidekick_bone_map` / `goblin_bone_map` proven), race-well rig bindings
(`verified=true` — human/goblin/orc/elf/dwarf), Synty register dressing (material/prop, not new
rigs), Camera B′ 20 m as the certifying view, the E10 §7 model-visual telegraph channel for mob
affixes. Scope anchor: One-Realm MVP — THE DENOMINATOR.
**Drill-through:** `current-to-end-state-game.md` · Q7/Q8 rulings (decision queue RESOLVED rows).

---

## Gaps at a glance (stage → owed work → home)

| Stage | Gap | Owner | Home |
|---|---|---|---|
| E1 | batch-2 derivation population (+ bc_commitment sampling question) | rocket + KR sequencing | engine tracker |
| E2 | K9 coordinate-drift reconcile · E10 Leg 3 mob kit-gen | rocket | PART F row K9 · mob-affix spec §11 |
| E3 | kit-name + faction-label LLM passes at batch-2 | star-lord | S4 grammar (ruled) |
| E4/E5 | E4 sim consumer + expressed-coordinate cert (design note next) | gandalf → rocket+gamora | E4 elicitation doc (FULLY RULED) |
| E6 | feed-2 registry snapshot export | star-lord | Glance contract §7.1 |
| E7 | GATE1 open rows (surface ledger 12✓/20) | Matt (rolling Q12) | surface-ledger.md |
| E8 | per-curated-kit scene assembly | drax | game tracker |

**Signed:** gandalf, 2026-07-10. The factory is the product: it starts at canon, calls the LLM only
through the narrow blanks, hands every soul to the court, and ships only what returns certified.
