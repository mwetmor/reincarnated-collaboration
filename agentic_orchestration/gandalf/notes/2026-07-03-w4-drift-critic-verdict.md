# W4 DRIFT-CRITIC verdict — demo-readiness run, batch-1 bundle

> **STATUS:** VERDICT — CURRENT. **Author:** gandalf (DRIFT-CRITIC). **Date:** 2026-07-03.
> **Leg:** W4 of the DEMO-READINESS UNATTENDED RUN (spec `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` v1.1, §3 W4 + §8).
> **Bundle asserted:** `reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (45MB; registry run `cbeb9471`/`f0bd67e5`; season `w3-batch1-solo-spectrum`; 700 kits @ 38.9% yield, 7 BC cells × 100, 40 monsters, 150 gear, 4 factions).
> **Assertion method:** parsed the bundle programmatically; every claim below is a count off the data, not a read-through (Gate-1 #7).

---

## ▶ ROLE: DRIFT-CRITIC — bundle-vs-spec audit + thematic drift read

## 1. Six-type mechanical assertion — **PASS (5 live + 1 honestly-PARKED)**

The "six-type" per spec §3 W4 = the six CONTENT types. Key-present + non-NULL count per type:

| # | Type | Key present | Non-NULL count | Verdict |
|---|---|---|---|---|
| 1 | kits | ✓ | 700 / 700 | PASS |
| 2 | monsters | ✓ | 40 / 40 | PASS |
| 3 | factions | ✓ | 4 clusters, non-empty | PASS |
| 4 | gear_pool | ✓ | 150 / 150 | PASS |
| 5 | weapons (per-kit `main_weapon`) | ✓ | 700 / 700 `substrate_weapon_id` non-NULL | PASS |
| 6 | flavortext | ✓ (key present) | 0 / 700 kit, 0 / 40 monster | **PARKED — not FAIL** |

**Flavortext ruling:** the key is present and every value is honestly `None` — the LLM pass was never run (dry-run, `spend=$0`). Per spec §7 this is the *resumable* park, and `_assembly_notes.proxies_field_honest_state` documents the same honesty for proxies. This is **not** a hollow-spot faking criterion B; criterion B forbids NULLs *in a bundle claimed complete*, and batch-1 does not claim flavor-complete. **Five content types mechanically hold; the sixth is a declared, resumable gap, not a structural failure.** The assertion PASSES for the batch-1 scope.

**Population-structure sub-assertion (the mechanical archetype spine): PASS.** Exactly 7 BC cells, 100 each, byte-clean:
`melee/low/spiky/STR` · `melee/high/flat/STR` · `melee/medium/variable/STR` · `ranged/low/spiky/STR` · `ranged/high/flat/DEX` · `ranged/low/spiky/DEX` · `mid/high/flat/DEX`.
Range spread 300 melee / 300 ranged / 100 mid; attribute 400 STR / 300 DEX; every kit carries 12 skills, 3 chains, 2 T4-chains, a `bc_target_cell`, a bound `main_weapon`. `proxies: []` on all 700 (correct — solo batch). No CONVERGENCE/DUAL T4 candidates present (correct — those are the summoner/pairing layer, batch 2).

## 2. Thematic / experiential drift read — **CURATION-VIABLE with two named caveats**

**Does 700 kits support curation-from-abundance for the ~7-8 non-summoner seats (G7)? YES — the abundance is real at the axis level, thin at the flavor level.** Two drift flags, neither a blocker:

- **DRIFT FLAG 1 — geometry is cell-locked (mild homogeneity).** Within any single cell all 100 kits share ONE geometry: `low/spiky`→`single_target`, `high/flat`→`large_aoe`, always. Element varies (physical/fire dominate per cell, with a 1–5% sprinkle of the other seven), but the *shape* of the fight does not vary within a cell. This is the substrate behaving correctly — a BC cell IS a shape — but it means the 100-per-cell "abundance" is abundance of *skin*, not of *shape*. Diablo-III-launch lesson: 100 near-identical Whirlwind barbarians re-tinted is not 100 builds. **Consequence for curation:** the real distinctiveness lever is CROSS-cell (pick one seat per cell), not within-cell. Within a cell, curate on element + name/flavor quality, not on mechanical differentiation — there isn't any. This is exactly the III.4 "300-sharp beats 400-with-reskins" launch concern surfacing early, and it's fine for a demo roster of 7-8.

- **DRIFT FLAG 2 — no `mid`-range STR, no `variable`-tempo ranged.** The 7 emitted cells are a diagonal slice, not a grid. There is no mid-range brawler, no ranged variable-tempo skirmisher. For a 7-8 seat demo this is *sufficient* coverage (melee/ranged/mid all present; low/med/high tempo all present; spiky/flat/variable all present), but the roster cannot show a "positioning-flexible mid" fantasy that isn't STR. Name it to Matt as a coverage fact, not a defect.

**No archetype collapse, no degenerate chains.** Every kit is a real 3-chain / 12-skill build with a bound weapon and a T4 offer table; the gauntlet ≥9/18 gate did its job (38.9% survivor yield is a healthy, honest filter — not the suspicious 0.4% of the defective run, which DEFECT 1 correctly explained). Faction narratives (Broad Blade Convergence, Loess Cannon Wardens, etc.) are element-and-geometry-derived and read coherently — the death-faith register isn't *carried* yet (that's flavortext, PARKED), but the structural faction spine is sound.

**One honesty note for Gate-2/curation:** kit `name`, `archetype_tag`, `energy_type`, `role_orientation`, `dominant_element`, `balance_metadata` are all `None` at the top level — the identity lives in the `id` string and `bc_target_cell`. Curation and the §8 table must read structure off `id` + `bc_target_cell`, NOT off the named fields, until the flavor/identity pass populates them. jack-ryan Gate-2 should confirm this is the resumable-park state and not a writer regression.

## 3. §8 curation shortlist — DESIGN-TRACK INPUT (axes prep, not the final shortlist)

Given what actually emitted (solo-only, 7 cells, geometry cell-locked, no summoners), the shortlist axes should be:

1. **PRIMARY axis — BC cell (one seat per cell).** This is the only axis carrying true mechanical distinctiveness. 7 cells → up to 7 mechanically-distinct seats. This maps almost 1:1 onto the ~7-8 non-summoner target — near-ideal. Curate one exemplar per cell first; that alone fills the roster with zero mechanical redundancy.
2. **SECONDARY axis — element identity within the chosen cell.** Since geometry is fixed per cell, element is the within-cell differentiator. Prefer the cell's off-dominant elements (the shadow/holy/lightning/wind sprinkle) where a distinct fantasy is wanted, physical/fire where the cell's "default" read is wanted.
3. **TERTIARY axis — name/flavor quality (the demo's face).** DEFERRED until the LLM flavor pass runs. Cannot be a selection axis on batch-1 as-is; flag to Matt that final seat-locking should wait on flavor for the shortlisted subset (shortlist-first flavor ordering is the cheaper path — see re-interpretation below).
4. **Coverage guardrails (spec §8 mandatory rows):** element spread ✓ achievable (8 elements present across cells); archetype spread ✓ (melee/ranged/mid × spiky/flat/variable); **no ranged summoners** ✓ (none exist — deferral stands trivially); summoner share ≈ G4% — see below.

### Re-interpretations forced by solo-only batch 1:

- **"≥1 CONVERGENCE kit" (§8) — RE-INTERPRET as DEFERRED-TO-BATCH-2, not dropped.** Batch 1 is solo-only by KR disposition; CONVERGENCE kits are structurally impossible in it (no proxy path, no DUAL/CONVERGENCE T4 candidates — asserted: 0 present). The §8 line was written under the assumption pairing rode the run; it didn't. **Recommendation:** the §8 CONVERGENCE row is satisfied by batch 2 (summoner emission), NOT by batch 1. Do not force it into the batch-1 shortlist — that would fabricate a kit that doesn't exist. Carry it forward as a batch-2 shortlist row, gated on Matt's summoner-emission ruling (`canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` — my CONTEST verdict there stands).
- **"both certified melee summoners" + "summoner share ≈ G4%" (§8 mandatory rows) — GATE on Matt's batch-2 ruling.** `demo_bone_acolyte` + `demo_crypt_lieutenant` are certified but NOT in this bundle (they're the batch-2 emission). The summoner-share row (2-3 of 8-10) is *unfulfillable from batch 1 alone*. **Recommendation:** batch-1 shortlist covers the ~7 non-summoner seats from the 7 cells; the 2-3 summoner seats are appended when batch 2 lands. Present the shortlist to Matt as **"7 non-summoner seats ready now; 2-3 summoner seats pending your batch-2 ruling"** — do not fake a full roster off a solo bundle.

**Net:** the curation shortlist is a **two-part deliverable** by structural necessity — the batch-1 slice (ready) and the batch-2 summoner slice (Matt-gated). The abundance is genuinely there for the part that emitted; the missing part is honestly missing, not degraded.

---

**Drift verdict:** **NO ARCHITECTURAL DRIFT. Batch-1 bundle holds the six-type structure for its declared solo scope (5 live + flavortext honestly parked). Curation-from-abundance is viable for the 7 non-summoner seats via the BC-cell primary axis. Two thematic caveats (geometry cell-locked → curate cross-cell; diagonal-slice cell coverage) are demo-sufficient facts, not defects. The summoner seats and the §8 CONVERGENCE row correctly defer to Matt's batch-2 ruling — forcing them into batch-1 would fake content that does not exist.**

**Signed:** gandalf, 2026-07-03 (DRIFT-CRITIC).
