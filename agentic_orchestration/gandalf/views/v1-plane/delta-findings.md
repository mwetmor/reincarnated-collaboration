# Delta Findings — Plane A vs Plane B

> Findings only — no recommendation. Plane-lock read is gandalf's.
> Delta = where the two planes DISAGREE on how to group corpus kits.
> 'Merge' = Plane B lumps together what Plane A separates; 'Split' = reverse.

## Top structural disagreements (ranked by kit count affected)

Each disagreement = kits that Plane A puts in one family cell, Plane B puts in a different column.

### Disagreement #1 — A-group SPLIT by B (188 kits affected)

**Plane A groups into `large_aoe`; Plane B splits across: `NOVA` (171), `ORBITAL` (17)**

Plane A cell: `large_aoe`
Plane B distribution:
  - `NOVA`: 171 kits
  - `ORBITAL`: 17 kits

Example kits: Arrow Storm Warden, Bee Swarm Warden, Auradin, Nova Sorceress

### Disagreement #2 — B-column MERGES A-families (118 kits affected)

**Plane B `PROJECTILE` column merges: A:`chain` (72), A:`single` (38), A:`small_aoe` (8)**

Plane B column: `PROJECTILE`
Plane A distribution:
  - `chain`: 72 kits
  - `single`: 38 kits
  - `small_aoe`: 8 kits

Example kits: Crown of Innate Probability (proc-lock archetype), High Ranger Bleed Warden, Saw Master Mechanist, Bowazon, Penetrating Shot Rogue

### Disagreement #3 — A-group SPLIT by B (92 kits affected)

**Plane A groups into `single`; Plane B splits across: `MELEE` (54), `PROJECTILE` (38)**

Plane A cell: `single`
Plane B distribution:
  - `MELEE`: 54 kits
  - `PROJECTILE`: 38 kits

Example kits: Bleed Berserker, Fulmination Holy Reckoning Templar, Crown of Innate Probability (proc-lock archetype), High Ranger Bleed Warden

### Disagreement #4 — A-group SPLIT by B (49 kits affected)

**Plane A groups into `small_aoe`; Plane B splits across: `ORBITAL` (27), `ZONE` (11), `PROJECTILE` (8), `BEAM` (3)**

Plane A cell: `small_aoe`
Plane B distribution:
  - `ORBITAL`: 27 kits
  - `ZONE`: 11 kits
  - `PROJECTILE`: 8 kits
  - `BEAM`: 3 kits

Example kits: BvC, Whirlwind Barbarian, Penetrating Shot Rogue, Forcewave Warlord, Multishot Demon Hunter

### Disagreement #5 — B-column MERGES A-families (44 kits affected)

**Plane B `ORBITAL` column merges: A:`small_aoe` (27), A:`large_aoe` (17)**

Plane B column: `ORBITAL`
Plane A distribution:
  - `small_aoe`: 27 kits
  - `large_aoe`: 17 kits

Example kits: Auradin, Nova Sorceress, BvC, Whirlwind Barbarian

---

## Summary: Plane A vs Plane B structural comparison

| Dimension | Plane A (spec) | Plane B (mock) |
|---|---|---|
| Total cells | 15 (3×5) | 24 (3×8) |
| Column axis | 5 dispersion families (Axis 2 canon) | 8 delivery-family columns (visual/gameplay taxonomy) |
| Row axis | 3 commitment classes (spec §2.2) | 3 classes (SNAP/WIND-UP/CHANNEL) — equivalent |
| Column overlaps | None (mutually exclusive) | NOVA∩ZONE (circle types); ORBITAL∩RING (ring type) |
| MELEE separation | Merged into `single` (footprint=1 per hit) | Explicit MELEE column separates contact-range |
| BEAM separation | Merged into `small_aoe` | Explicit BEAM column separates sustained-linear |
| SUMMON/ORBITAL | Both in `multi_spawn` | SUMMON and ORBITAL are separate columns |
| Empty-cell count | See Plane A table above | See Plane B table above |

## Key structural disagreement (single largest)

**Plane A groups into `large_aoe`; Plane B splits across: `NOVA` (171), `ORBITAL` (17)** — 188 kits affected.

This is the biggest separation: Plane B's column taxonomy distinguishes delivery *mechanism* (projectile vs melee vs orbital) while Plane A's Axis 2 measures dispersion *outcome* (how many damage origins, how wide). Kits that Plane A groups by similar footprint are scattered by Plane B based on how they *look* in motion.
