# Unit 2 — PoE2 Crossbow Post-Cutoff Check (K8 Crossbow Sniper)

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster context:** K8 Crossbow Sniper — engine coordinate `DRLS__` = DEX / ranged / LOW tempo / spiky amp / solo proxy / commitment unknown
**Task:** Verify whether PoE2 crossbow skills (post-training-cutoff patches 0.1–0.5) attest this cell; provide per-slot claims for best 1–2 exemplars
**Crawl date:** 2026-07-12

---

## Post-cutoff context

PoE2 has been in active development through 2025–2026. The following patch strata are relevant, with decreasing confidence as patches go further post-cutoff:
- **0.1 Early Access** (December 2024): Mercenary class with crossbow introduced — HIGH confidence (partially in training)
- **0.2** (February 2025): Crossbow balance changes including specific Mercenary skills — MED confidence
- **0.3–0.4** (2025): Further balance passes; "0.4 CoC-automation meta" referenced in corpus spec — LOW confidence for specifics
- **0.5** (October 2025): Major expansion (Wall of Shields added, broad skill rework) — LOW-VERY LOW confidence
- **Dawn of the Hunt** (2026): Referenced in search results — VERY LOW confidence

Sources used: Mobalytics, Maxroll, and PCGamesN crossbow build guides (live sources, July 2026).

---

## Exemplar 1: High Velocity Rounds Mercenary / Witchhunter ("Sniper King")

**Source:** mobalytics.gg/poe-2/builds/schwingy-sniperking (accessed July 2026)

### Build identity
High Velocity Rounds loads the crossbow with armor-piercing bolts that pierce enemies and deal significantly amplified damage against fully armor-broken targets. The playstyle is deliberate and sequential: apply armor break (via Fragmentation Rounds or Gas Grenade), then fire High Velocity Rounds for massive per-shot damage. The Mercenary's "Power Shot" firing mode makes HVR fire slower with higher per-shot damage — explicitly the "sniper rifle" mode in GGG's own class description.

### Engine-prefix claims for HVR Mercenary

| Slot | K8 engine coord | PoE2 attested value | Confidence | Evidence |
|---|---|---|---|---|
| attr | D (DEX) | STR/DEX | MED | Mercenary starts at STR/DEX; passive tree for sniper builds slides toward DEX (evasion, projectile speed). NOT pure DEX — the class is hybrid. K8's DEX claim is partially attested; full DEX would require a DEX-only build spec. |
| range | R (ranged) | ranged | HIGH | Crossbow is a ranged weapon by definition; all Mercenary builds fight at distance. |
| tempo | L (low) | LOW | HIGH | Power Shot = explicitly "slower firing, higher per-shot damage" per class guides. HVR builds use deliberate single shots, not rapid fire. Low action cadence confirmed. |
| amp | S (spiky) | SPIKY | HIGH | "When armor is fully broken, the Witchhunter's Exsanguinate can detonate enemies instantly"; HVR on broken-armor targets deals dramatically higher burst damage. Spiky amp confirmed — the damage spike when the armor-break condition fires is extreme. |
| proxy | S (solo) | solo | HIGH | All Mercenary crossbow builds are solo damage; no proxy entities involved in the sniper archetype. |
| commitment | __ (unknown) | WIND-UP | MED | The rotation is: apply armor-break setup → fire HVR for spike. This is a WIND-UP pattern. The setup (armor break) must precede the spike shot. If evaluating just the HVR shot itself, it's INSTANT. The KIT commitment = WIND-UP (the setup is load-bearing). |

**Cell attestation for K8 DRLS__:**
- D (DEX): PARTIAL — Mercenary is STR/DEX hybrid; sniper tree investment toward DEX provides partial attestation. Pure DEX unconstrained.
- R (ranged): CONFIRMED
- L (low): CONFIRMED
- S (spiky): CONFIRMED
- S (solo): CONFIRMED
- __ (commitment): WIND-UP (MED confidence from rotation evidence)

**Overall K8 attestation: 4/5 confirmed slots (ranged/low/spiky/solo), 1 partial (attr = STR/DEX vs pure DEX), 1 filled (commitment = wind-up). Strong attestation of the cell.**

---

## Exemplar 2: Galvanic Shards Witchhunter

**Source:** maxroll.gg/poe2/build-guides/galvanic-shards-witchhunter-build-guide (accessed July 2026)

### Build identity
Galvanic Shards fires wide shotgun-style lightning projectiles that shock enemies; then Shockburst Rounds detonates the shock for massive burst damage. This is a shock-first → burst model for bosses, with Galvanic Shards also serving as the primary AoE clear skill.

### Engine-prefix claims for Galvanic Shards Witchhunter

| Slot | K8 engine coord | PoE2 attested value | Confidence | Evidence |
|---|---|---|---|---|
| attr | D (DEX) | STR/DEX | MED | Same Mercenary class; same dual-attribute situation |
| range | R (ranged) | ranged | HIGH | Crossbow; all ranged |
| tempo | L (low) | MED | MED | Galvanic Shards itself fires at "medium attack speed" per Maxroll guide; not the slow deliberate single-shot pattern of HVR; this build leans MED rather than LOW tempo |
| amp | S (spiky) | VARIABLE | MED | Galvanic Shards = consistent AoE spread; Shockburst Rounds = spiky boss burst; combined pattern is VARIABLE (not pure SPIKY like HVR) |
| proxy | S (solo) | solo | HIGH | Same as HVR — solo damage only |
| commitment | __ | WIND-UP | MED | Shock-first → Shockburst detonation = WIND-UP (setup + execute); same rotation pattern as HVR |

**Cell fit for K8:** Galvanic Shards Witchhunter does NOT cleanly fit K8's `DRLS__` cell. The MED tempo and VARIABLE amp diverge from K8's LOW/SPIKY. Galvanic Shards may fit a different roster cell (e.g., DRMS__ = DEX/ranged/MED/spiky/solo or DRMV__ = DEX/ranged/MED/variable/solo).

**Conclusion: Galvanic Shards is NOT the K8 attesting build. It's a separate cell in the same crossbow family.**

---

## Cell attestation summary for K8 (DRLS__)

**Best attesting build: High Velocity Rounds Mercenary/Witchhunter**

| Slot | K8 value | PoE2 attestation | Status |
|---|---|---|---|
| attr | DEX | STR/DEX hybrid | PARTIAL — sniper tree slides DEX; full-DEX not confirmed |
| range | ranged | ranged | CONFIRMED |
| tempo | low | low | CONFIRMED |
| amp | spiky | spiky (on armor-break execution) | CONFIRMED |
| proxy | solo | solo | CONFIRMED |
| commitment | __ | wind-up | PROPOSED FILL — wind-up for the armor-break → HVR execution rotation |

**Attestation verdict: K8's cell is strongly attested by PoE2's HVR Mercenary/Witchhunter build across 4/5 resolved slots + partial on attr. The STR/DEX hybrid attribute is the main deviation from K8's pure DEX claim — PoE2's Mercenary is constitutionally STR/DEX; a "pure DEX crossbow" would require the Ranger class (bow-based, not crossbow) or a highly specific passive tree path for Mercenary.**

**Commitment slot recommendation:** WIND-UP (MED confidence) based on the armor-break setup requirement.

---

## Cross-reference to known corpus

The PoE2 corpus already contains 38 records (from the 0.1–0.2 era research). The HVR Mercenary may already be in the corpus under a different folk name; Elrond should check `canon-corpus-poe2.jsonl` for any existing crossbow/mercenary records before treating this as a mint.

---

## Sources

- Mobalytics "Sniper King" PoE2 Mercenary Build Guide [0.2.0 Buffs]: https://mobalytics.gg/poe-2/builds/schwingy-sniperking
- Maxroll "Galvanic Shards Witchhunter Build Guide": https://maxroll.gg/poe2/build-guides/galvanic-shards-witchhunter-build-guide
- PCGamesN "Best PoE2 Mercenary Build": https://www.pcgamesn.com/path-of-exile-2/mercenary
- Mobalytics "Mercenary Overview": https://mobalytics.gg/poe-2/guides/mercenary-overview
- dving.net "PoE2 Mercenary Guide" (Crossbow mechanics section)
- Note: all PoE2 post-0.2 claims carry ≤0.5 confidence ceiling per post-cutoff law; source-verification mandatory before these claims are treated as confirmed

## Knowledge gaps

- Whether PoE2 has a pure-DEX crossbow ascendancy or class path that would confirm K8's "D" slot without the STR hybrid
- HVR post-0.5 "Dawn of the Hunt" changes unknown; the build may have been reworked significantly
- Whether the HVR build already exists in `canon-corpus-poe2.jsonl` under a different folk name
