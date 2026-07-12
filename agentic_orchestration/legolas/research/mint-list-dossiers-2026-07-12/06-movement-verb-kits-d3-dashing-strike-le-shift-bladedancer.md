# Dossier — Movement-Verb Kits: d3 Dashing Strike Monk + le Shift Bladedancer

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** B6 (movement-verb under-harvested family; mobile-crawl utility-vs-identity bias produced no standalone movement-verb records for these two builds)
**Priority:** MED
**Corpus gap confirmed:** D3 corpus has no Dashing Strike record; LE corpus has no Shift Bladedancer record
**Crawl date:** 2026-07-12
**Mint packaging note:** Two builds; one mint entry per V4-r2. Both share the GX-01 movement-verb-as-identity family. Separate sub-sections below. Elrond decides on one combined record vs two distinct rows.

---

## Sub-dossier A: d3 Dashing Strike Monk (Raiment of a Thousand Storms)

### Identity

**Game:** d3 (Diablo 3)
**Patch/era span:** Patch 2.4 (2016) — brief viability window; KILLED BY NERF in same patch cycle's balance pass; present as a playable gimmick/nostalgia build through Season 39 but not meta-viable after 2.4
**Canon tier:** shallow — one-era viability window; killed before it could achieve deep canon status
**Folk names:** "Dashing Strike Monk," "Raiment DS Monk," "Teleporting Monk"
**Shipped / negative-canon status:** SHIPPED but NERF-KILLED — a "killed-by-nerf" record per §9.6 v2.2 FOLD. Valuable as a design data point: it demonstrated movement-verb-as-primary was achievable in D3 before being gated back. Retained in corpus as nerf-contrast record and GX-01 evidence.

### Build identity (2–4 sentences)

The Raiment of a Thousand Storms 6-piece set empowered Dashing Strike — normally the Monk's mobility utility skill — into the primary damage delivery system: the first enemy hit after a dash takes 12,500% increased damage from the next Spirit Generator attack. The core loop is Dash → Fists of Thunder (generator hit) → Dash again, creating a movement-verb-is-damage-verb pattern where the player never stops moving. The build's tempo is the highest in the D3 Monk catalog because EVERY combat interaction is initiated by a dash; standing still is a damage loss. The nerf removed the 12,500% multiplier's effectiveness, returning Dashing Strike to utility-only status.

### Engine-prefix claims (d3 Dashing Strike Monk)

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | DEX | HIGH | Monk = DEX archetype in D3 (primary stat: Dexterity) |
| range | MELEE | HIGH | Dashing Strike closes to melee range; Fists of Thunder is melee; all combat at close range |
| tempo | HIGH | HIGH | Constant dashing = highest movement cadence in the Monk kit; no idle time |
| amp | SPIKY | HIGH | 12,500% damage multiplier on the first hit after a dash = extreme per-strike spike; between dashes the damage is negligible — textbook SPIKY |
| proxy | SOLO | HIGH | Pure solo damage; no proxy entity |
| commitment | INSTANT | HIGH | Dashing Strike is an instant movement skill; Fists of Thunder is an instant generator hit; no wind-up |

### Raw descriptors (d3 Dashing Strike)

**geo:** Melee point-to-point dash (single target engagement per dash); Fists of Thunder has very short range (arm's length). No AoE; single-target focus per dash.

**ctrl:** Reposition via dash provides defacto "avoid" control; no CC applied to enemies.

**mob:** Dashing Strike IS the mobility verb — player is always in motion; never stationary; highest mobility floor of any D3 Monk build.

**def:** Fragile (glass cannon typical of movement-verb builds); relies on constant repositioning to avoid damage rather than building defensive stats.

**econ:** Spirit-based (Fists of Thunder generates Spirit; Dashing Strike costs Spirit with variant rune); self-sustaining Spirit loop within the dash cycle.

**elem:** Physical/Holy (Monk class primary damage types; Fists of Thunder deals lightning in some runes).

**Status note:** NERF-KILLED post-Patch 2.4. Corpus flag: `negative: false` (was viable) with era note `eras: ["2.4-brief"]` + canonicity note "nerf-killed; killed-by-nerf category per §9.6."

---

## Sub-dossier B: le Shift Bladedancer

### Identity

**Game:** le (Last Epoch)
**Patch/era span:** 0.8 (beta, 2021) — Season 4 (1.2, 2024+); Shift is the Bladedancer's defining skill since sub-class introduction; continuous deep canon.
**Canon tier:** deep (Shift appears in 82.5% of all Bladedancer builds per Last Epoch Tools; the Bladedancer is effectively defined by Shift)
**Folk names:** "Shift Bladedancer," "Shift BD," "Bladedancer" (the class folk name itself implies Shift)
**Shipped / negative-canon status:** SHIPPED — deep canon; the Bladedancer's defining identity is built into the skill system via Shift's tree nodes.

### Build identity (2–4 sentences)

Shift is the Last Epoch Bladedancer's primary engagement verb: a teleporting dash through enemies that deals damage on exit, generates Shadows (the class's mirrored-copy mechanic), applies Smoke Bomb effects, grants dodge rating, and serves as the Mana recovery engine. Where other LE Rogue builds use Shift as utility, the Bladedancer's skill tree turns Shift into the combat loop's axis: nodes cause Shift to trigger Shadow Cascade, recall Umbral Blades, generate dodge stacks, and proc defensive invisibility frames. The 82.5% build-prevalence data point (Last Epoch Tools, Season 4) means Shift is effectively the Bladedancer's class identity, not a skill choice. This is the deepest example of movement-verb-as-identity in LE.

### Engine-prefix claims (le Shift Bladedancer)

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | DEX | HIGH | Rogue class = DEX archetype in LE (Dexterity primary; dodge-scaling; crit scaling) |
| range | MELEE | HIGH | Shift dashes THROUGH enemies (melee-range contact); Shadows attack at melee; all Bladedancer combat is close-range |
| tempo | HIGH | HIGH | 82.5% of builds use Shift as the primary action; constant shifting = highest tempo in the LE Rogue kit |
| amp | VARIABLE | MED | Shift damage is enhanced by skill tree nodes that can make individual Shifts deal high damage; Shadow proc damage varies; VARIABLE overall |
| proxy | LIGHT | MED | The Shadows generated by Shift are meaningful DPS contributors (Shadow Cascade, Sync Strike combos) but the player's own attacks are still significant; LIGHT proxy. Builds with max Shadow investment approach HEAVY but that's a specific spec, not the general identity. |
| commitment | INSTANT | HIGH | Shift is an instant teleport dash; no wind-up, no channel |

### Raw descriptors (le Shift Bladedancer)

**geo:** Point-to-point dash through enemy position; contact AoE on exit; Shadow attack positions distributed at contact points along the shift path.

**ctrl:** Smoke Bomb blind effect on Shift (secondary CC); invulnerability frames during Shift provide pseudo-CC by making the player temporarily invincible. Primarily damage-plus-evasion, not hard CC.

**mob:** Shift IS the mobility verb — highest-mobility identity in LE Rogue; provides both offense and defense through the same movement action. Shift is both the engagement and the escape.

**def:** Dodge-stacking + Smoke Bomb blind + Shift invincibility frames. Defense is built INTO the movement skill — a unified offense/defense kit.

**econ:** Mana recovery triggered by Shift (skill tree nodes); Shadow generation (managing mirror copies as resource); Bladedancer has unique dual-economy: mana managed through Shift, Shadows managed through engagement pattern.

**elem:** Physical or Cold primary (Shadow Cascade cold node path; Umbral Blades physical by default; player choice).

### Sources

- Last Epoch Maxroll Bladedancer Leveling Guide: https://maxroll.gg/last-epoch/build-guides/bladedancer-leveling-guide (Shift role confirmed)
- Last Epoch Maxroll Shadow Cascade Guide: https://maxroll.gg/last-epoch/build-guides/shadow-cascade-bladedancer-guide
- "Last Epoch Bladedancer Build Guide" (games.gg) — Shift described as "primary mobility tool and appears in 82.5% of Bladedancer builds"
- Knowledge base (kb) — LE Bladedancer mechanics from training data
- V4-r2 §F4 mint-list (gandalf, 2026-07-12)

### Knowledge gaps

- Shadow DPS vs. player DPS split not measured (determines LIGHT vs HEAVY proxy call)
- Season 4 (1.2) specific changes to Shift not verified via live patch notes
- The "Synchronized Strike Bladedancer" and "Dancing Strikes Bladedancer" builds may each have different Shift roles that affect the VARIABLE/SPIKY distinction

---

## Cross-family note (both kits)

Both builds share GX-01 (movement verbs load-bearing) as their primary cross-game signal. Together with D2 Teleport Sorceress, they form a three-game exhibit for movement-verb-as-kit-identity. The NEGATIVE TWINS in the family (Charged Dash, PoE1 — confirmed corpus entry via GX-01) are already attested. This completes the GX-01 exhibit to four positive exemplars across D2/D3/LE/PoE1.
