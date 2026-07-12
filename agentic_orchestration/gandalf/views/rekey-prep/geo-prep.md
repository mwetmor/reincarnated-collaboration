# Re-key prep — GEO slot (design session #1)

**Date:** 2026-07-12 · gandalf (mechanical prep; **elicits, does not rule**) · Spec: `corpus-rekey-spec-v1.md` §2 — geo RETIRES as key-slot → raw descriptor; engine target = **16-type geometry palette** (2026-05-08, Option C).

## 1. Corpus code frequency (v3 CSV canon positives, n=478)

| code | meaning | count | % |
|---|---|---|---|
| S | small / melee-radius | 161 | 34% |
| L | large / zone | 111 | 23% |
| N | single | 94 | 20% |
| M | multi | 65 | 14% |
| C | chain | 34 | 7% |
| _ | unspec | 13 | 3% |

**5 live codes.** (decoded via generator `code_geo`/`norm_geo`.)

## 2. Engine vocabulary of record — 16-type geometry palette

Source: `canonical/sidecars/emit_substrate_registry.py::_build_geometry_palette_primitives` (→ `atomic_substrate_registry_v1.json`; canon lineage `09-geometry-palette-discussion.md`). CORE 14 + CORE-MARGINAL 2:

`scatter · line · arc · cone · sweep · circle · aura · beam_channel · persistent_zone · ground_targeted_circle · melee_arc · totem · ground_slam · projectile` + **marginal:** `multi_projectile · chain_lightning`.

## 3. PROPOSED mapping (corpus → engine) + residue

| corpus | → engine 16-type | confidence | note |
|---|---|---|---|
| N single | `projectile` | HIGH | 1:1 clean |
| C chain | `chain_lightning` | HIGH | 1:1 (marginal type) |
| M multi | `scatter` / `multi_projectile` | MED | 1:2 — corpus can't split spread-vs-multi |
| S small | `melee_arc` / `arc` / `sweep` / `ground_slam` / `aura` | LOW | **1:5 collapse** |
| L large | `circle` / `cone` / `persistent_zone` / `ground_targeted_circle` | LOW | **1:4 collapse** |

**Residue — engine types with NO corpus code:** `line`, `beam_channel` (partly lives on the commitment=channel axis, not geo), `totem` (corpus buckets totems under econ=summon, not geo), and the internal splits inside S (5-way) and L (4-way). **The corpus geo axis is 5-way; the engine is 16-way — every corpus S/L/M row is under-resolved for engine keying.**

## 4. Open forks (UNRESOLVED — Matt rules)

- **Fork G1 — refine-at-generation vs re-probe.** (a) Keep corpus S/L/M as a coarse pre-bin; let the engine's archetype templates refine to 16-type at generation time (corpus geo becomes a *hint*, not a coordinate). Cheap, honest about corpus resolution. — vs — (b) commission a legolas Mode-A probe to re-characterize the ~340 S/L/M corpus kits at 16-type granularity. Expensive; buys true geo-coordinate joins. **Genre precedent:** PoE's skill taxonomy distinguishes all 16+ (AoE-slam vs cone vs ring vs beam are separate gems); D2 conflated them (nova/blizzard both "large"). The corpus inherited D2-era coarseness. **Lean:** (a) for now — geo is refined engine-side at generation; probe only the cells where geo drives a whitespace claim (K3 polearm `sweep`-vs-`melee_arc`, K19 `beam_channel`).
- **Fork G2 — is `line` genre-real or engine-only?** No corpus code produces `line`. Either the corpus buries lines inside N/M, or line-geometry (Lightning Strike bolt, Freezing Pulse) is genuinely a projectile subtype. Genre precedent says lines exist (PoE Spark/Arc). **Lean:** line hides inside corpus N — flag for the G1 probe if it fires.
