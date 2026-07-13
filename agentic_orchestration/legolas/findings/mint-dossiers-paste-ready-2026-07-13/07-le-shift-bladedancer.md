# Mint Kit Dossier — le-shift-bladedancer

**corpus_kit_id:** `le-shift-bladedancer`
**folk_name:** Shift Bladedancer
**game:** le (Last Epoch)
**status:** positive
**era_year:** 2024
**stabilization_patch:** v1.0 (Last Epoch full release, February 21, 2024)
**for_roster_kits:** B6
**mint_priority:** MED
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

Shift is the Bladedancer's primary movement skill in Last Epoch. The Bladedancer is a mastery of the Rogue class, and Shift is the core mobility-attack tool that defines the Bladedancer's play pattern: dash through enemies, deal damage on transit, generate Shadows (illusory copies of the player), and trigger blade-trail DoT zones along the dash path. Shift appears in 82.5% of documented Bladedancer builds (source: Last Epoch Tools build database, confirmed in search 2026-07-13).

Genre lineage:
- **Direct ancestor:** D3 Dashing Strike Monk (dash-through lane clear pattern; LE Shift Bladedancer is the most faithful descendant)
- **Parallel contemporaneous:** D3 Demon Hunter Vault (repositioning-focused dash; less lane-clear identity); PoE1 Blink Arrow / Frostblink (instant repositioning without direct lane-clear damage)
- **The blade-trail DoT innovation:** Shift adds a persistent zone of damage along the dash path (blade trails) — a distinction from D3 Dashing Strike which deals immediate contact damage but leaves no field effect. The trail makes Shift a HYBRID movement-attack-field kit, combining the movement-verb identity with persistent-zone delivery for enemies that walk into the residual blades.
- **Shadow generation:** Shift (with appropriate skill nodes) creates "Shadows" — illusory copies of the Bladedancer that execute skills independently. Shadow generation via Shift transitions the kit from pure-solo toward a proxy-light layer (shadows = very light proxy, executing skill copies without player input). This is a notable design extension beyond the D3 ancestor.

LE's Bladedancer is built around the thesis that movement IS the primary damage action — a stronger expression of the D3 Monk movement-verb philosophy because LE explicitly rewards Shift integration into the damage loop (via Shadow generation and blade trail stacking) rather than making it a utility-plus-contact skill.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| 2019–2021 | LE Early Access (0.7–0.8) | Rogue class and Bladedancer mastery exist; Shift available; early builds documented in community but not widely stable |
| 2022 | LE v0.9 | Bladedancer builds documented on Maxroll.gg; Shift identified as primary movement skill; Shadow generation mechanics stabilized |
| **February 21, 2024** | **LE v1.0** | **Stabilization** — Last Epoch full release; Bladedancer and Shift documented as core identity; 80+ builds catalogued on Last Epoch Tools across all seasons; 82.5% Shift adoption rate |
| July 2024 | LE v1.1 | Guide updates on Maxroll (Shadow Daggers Bladedancer, Dancing Strikes Bladedancer, etc.); Shift remains the universal Bladedancer mobility foundation |
| August 2025 | LE v1.1 continued | Maxroll Shadow Daggers guide last updated August 20, 2025 (confirmed in fetch 2026-07-13); Shift confirmed active in live meta |

## Mechanical Identity

The Shift Bladedancer dashes through enemies (self-origin, lane delivery — same geometry as D3 Dashing Strike), dealing contact damage along the dash path and leaving persistent blade trail zones behind. With the "Lasting Presence" and "Dancing Shadows" skill nodes, each Shift cast generates a Shadow that independently casts Shadow Cascade at the dash origin and destination points. With the "Shadowslip" node, Shift grants brief invulnerability frames during execution.

The play loop: Shift through a pack → blade trails persist in the lane → Shadows independently cast additional skills → Shift again → repeat. The Bladedancer is moving essentially continuously; all primary damage comes from the movement-chain rather than stationary casting. This is the most complete "movement IS the primary game action" identity in LE's current kit library.

**Proxy layer note:** Shadow generation via Shift creates a lightweight proxy layer (shadows cast skills independently). This gives the Bladedancer a secondary proxy-light dimension; however, the player movement (Shift) remains primary and shadows are riders, not primary damage actors. Proxy = `solo` for the Shift identity itself; the full Bladedancer loop introduces `light` when Shadow generation nodes are specced. The corpus entry should reflect `solo` (Shift's own identity) with a note on the Shadow extension.

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | DEX | HIGH | Rogue = DEX primary class in Last Epoch; all Rogue abilities and damage scaling favor DEX (Agility); Bladedancer mastery is the DEX-forward Rogue path |
| range | melee | HIGH | Shift ends with the Bladedancer at melee-contact range of the dash target; blade trails and damage are delivered at melee distance |
| tempo | high | HIGH | Rapid repeated Shift dashes; the build's identity is continuous movement at high action density; Shift is spammable on a short cooldown/mana basis |
| amp | flat | MED | Per-dash contact damage is consistent; blade trail DoT is continuous; no significant burst/spike differentiation. Some Variable quality in Shadow Cascade triggers (dependent on Shadow generation count) but base Shift output is flat. |
| proxy | solo | HIGH | Shift itself = solo (player body IS the weapon during the dash); Shadow generation is an extension mechanic that introduces light proxy; primary identity = solo |
| commit | instant | HIGH | Shift is an instant dash (no cast animation delay; executes immediately); Shadowslip node adds invulnerability frames but the dash itself is instant |

## Raw Descriptors

**geo:** Self-origin lane dash: Bladedancer dashes from current position to target, striking all enemies in the lane. Blade trails persist as a zone effect along the dash path for several seconds. Shadow generation adds at-origin-and-destination secondary AoE casts from Shadow entities.

**ctrl:** Bleed ailment (blade trails apply bleed to enemies in the zone). Brief stagger on enemies struck by the dash contact (not formalized CC, but contact physics).

**mob:** Maximum mobility; Shift provides invulnerability frames (Shadowslip node) and massive Dodge buff on use. The build is "always moving" — one of the highest-mobility builds in Last Epoch's current meta. The build guide notes: "It's hard to go much faster than this build thanks to its very high movespeed, a short cooldown on Shift and most of our damage coming from skills with the movement tag."

**def:** Dodge-primary (Shift provides a "massive boost of Dodge on use"); invulnerability frames (Shadowslip) for timing-based avoidance; armor secondary. Glass cannon tendency matched by the high dodge and invulnerability frame access.

**econ:** Mana spend per Shift (low cost; enables rapid dash looping); mana regeneration sustains the spam cadence. The resource ceiling is the mana pool and recovery rate — builds typically stack mana regeneration and mana on kill to sustain continuous Shift spam.

**elem:** Physical primary (Shift's direct strike and blade trail = physical damage). Bleed DoT (physical-damage-over-time from blade trail zones). Some Shadow Cascade arms convert to void or elemental damage depending on spec — but the base Shift identity is physical.

## Sources (live URLs)

- [Shadow Daggers Bladedancer Guide — Maxroll (v1.1)](https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide) — primary Shift-integrated Bladedancer documentation; confirms "Shift is your main Movement Skill"; invulnerability frames (Shadowslip); Shadow generation via Dancing Shadows node; 82.5% adoption rate from LE Tools; last updated August 2025 (LIVE — fetched 2026-07-13)
- [Shadow Cascade Bladedancer Guide — Maxroll (Season 4)](https://maxroll.gg/last-epoch/build-guides/shadow-cascade-bladedancer-guide) — alternative Shift+Shadow Cascade integration (LIVE)
- [Dancing Strikes Bladedancer Guide — Maxroll](https://maxroll.gg/last-epoch/build-guides/dancing-strikes-bladedancer-guide) — additional Bladedancer variant with Shift (LIVE)
- [Bladedancer Leveling Guide — Maxroll](https://maxroll.gg/last-epoch/build-guides/bladedancer-leveling-guide) — progression documentation confirming Shift as foundational (LIVE)
- [Best Bladedancer Build — GINX TV](https://www.ginx.tv/en/last-epoch/best-bladedancer-build-skills-stats-passives) — build overview with Shift integration (LIVE)
- [Bladedancer Build — Games.gg](https://games.gg/last-epoch/guides/last-epoch-bladedancer-build-guide/) — build guide confirming movement-identity (LIVE)

## Knowledge Gaps

- Elrond: verify vs existing LE Rogue / Bladedancer corpus records for duplication; this is a DISTINCT record for the Shift skill identity (movement-verb primary), not the full Bladedancer mastery
- Exact LE Early Access patch when Shift was solidified (before v0.9) not pinned; v1.0 is the confirmed stabilization date
- Shadow generation proxy-layer: the megaprobe tagged proxy as `solo` (Shift's own identity, accurate); the Shadow extension adds `light` when fully specced — both should be noted; recommend elrond tag `proxy_primary = solo; proxy_extended = light` or equivalent schema expression
