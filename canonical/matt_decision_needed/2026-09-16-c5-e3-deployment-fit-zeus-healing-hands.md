# Q80 — E3 deployment fit: two of the six skills were built as casts that the source games deploy as procs (Zeus, Healing Hands)

> **STATUS:** OPEN — gandalf (ELICITOR, spec lens), 2026-09-16, autonomous stretch of Run C-5. Raised by Matt's question: *"I'm wondering if they are all projectiles or if some of them are instant casts or cast on target or different type of deployment structures. I just want to be sure that what we are building does fit exactly to the intended deployment of the VFX."* Audit source: `agentic_orchestration/research/curated/corpus.db` → `skill_geometry_band` (delivery_class / origin / motion_signature / source_anchor) + `kit_citations`; footage list in `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md` § Sources. Rulings land in `astra_test_01/burst/runs/C-5/ledger.json`; both fixes are spec/parameter re-authoring + one TOOLING burst (no new grammar).

## What fits (no ruling needed)
| skill | source deployment (corpus, fetched text) | built | 
|---|---|---|
| Frozen Orb (D2) | traveling projectile that emits radial bolts along its path, final burst on expiry — footage `b5a-iIras34` @ ≈ 3025 s | G1 projectile + spiral emission + expiry nova ✅ |
| Blackwater Cocktail (GD) | lobbed projectile → burning tar carpet at the ground point | G2 arc → shatter → field → decal ✅ |
| Poisonous Concoction (PoE) | lob a vial in an arc to the targeted point; blast radius at landing | G2 arc → shatter → cloud → decal ✅ |
| Lightning Blast (LE) | fires a bolt that chains to nearby enemies (near-instant) | G3 instant target-tracked bolt + chain hops ✅ (VERIFY: hop count/timing — text-sourced only) |

## Forks — one recommendation each; rule with a letter
- **F1 Zeus chain (Hades).** The corpus has no row for the *player's* boon; the footage we measured (`ijwA_J29j1k` @ 1745.6 s) is *Theseus's* Zeus call — a telegraphed sky strike. The player's Zeus boon is an **on-hit proc**: chain lightning that jumps off your attack/cast from the struck enemy. Built: G3 chain **cast from the caster at a target**.
  **Recommend (a): keep G3, move the origin to the struck target** — the chain begins at the first dummy hit by whatever the player cast, hops from there; no caster-to-target link. Cheapest, and it is the Hades read. *Alt (b):* Theseus sky strike (ring telegraph 0.75 s → bolt from above → ground nova + scorch) — the footage we actually have, and a strong ARPG "call lightning" verb, but not the boon. *Alt (c):* leave as a caster-origin chain (a Diablo II Chain Lightning reading; knowingly off-source).
- **F2 Healing Hands (LE).** Corpus: *procs on melee hits (Cleric's Hammer), healing + fire/holy damage in a small radius **around the melee target**.* Base skill: an instant self-targeted heal with a radius. Neither is a loop. Built: G4 **self-centred aura loop** (seal + 5 orbiting ring segments + petal pulses on a schedule + recast refresh).
  **Recommend (a): re-spec as a single burst-around-target** — seal flash + one petal pulse at the hit point, ~0.4 s, no orbit, no refresh (G4 with pulses=1, loop off, origin at target). Matches the source and reads as *support on contact*. *Alt (b):* instant self burst (base-skill read: seal under the caster, one pulse, ~0.4 s). *Alt (c):* keep the loop as a "consecration" fantasy — knowingly off-source; G4 as a grammar survives either way (it will serve real auras later).

- **F3 Holy seal glyph (register/content).** The painted seal primitive (`VF-prim-holy-seal-01`) carries a **hexagram** (six-pointed star) at its centre — visible under the caster in the v30 look (Packet 93, HH sheets). Diablo II's Paladin auras use abstract geometric seals; a hexagram reads as a specific religious symbol on a mobile storefront.
  **Recommend (a): repaint the seal with a non-denominational sigil** (petal rosette / sunburst in the same four-plane language; 2 images, one GENERATE burst, no exporter change). *Alt (b):* keep it (geometric-occult register, PoE-style). *Alt (c):* eight-pointed star (Diablo's own seal vocabulary) — same cost as (a).

## Consequence of ruling (a)/(a)
One TOOLING burst after T4w: G3 gains an `origin: target` option; G4 gains `pulses: 1, loop: false, origin: target`; the two specs re-authored; kits re-baked; rendered look via the next PACK. Nothing else in the six moves.
