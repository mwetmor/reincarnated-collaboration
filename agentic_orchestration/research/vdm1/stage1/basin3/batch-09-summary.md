# VDM-1 basin-3 batch-09 summary — d3 kits 97–108

**Batch:** 09 | **Wave:** CW3 | **Date:** 2026-07-18

## Per-kit one-liners

| kit_id | identity | mechanics | era | negative_canon | notes |
|---|---|---|---|---|---|
| d3-tal-meteor | C | C | set-era C · late-sets C | n/a | Season 3/6 set-era attestation confirmed; set reworked S27 |
| d3-trag-nova | C | C | late-sets C | n/a | Necromancer debut 2017 confirmed; Essence resource confirmed |
| d3-typhon-hydra | C | C | late-sets C | n/a | Typhon's Veil introduced Season 20 |
| d3-ue-multishot | C | C | set-era C · late-sets C | n/a | Hatred+Discipline resource confirmed |
| d3-uliana-ep | C | C | set-era C · late-sets C | n/a | Set released Season 4; reworked Season 22; Spirit resource confirmed |
| d3-vyr-archon | C | C | set-era C · late-sets C | n/a | Vyr rework Season 4; Chantodo stacking confirmed |
| d3-wave-of-force | C | C | (no era rows — negative kit) | **CONTRADICTED** | negative_canon claim "no set multiplier path" contradicted by Delsere's 12,500% WoF multiplier |
| d3-wizard-black-hole | C | C | NULL-era kit — no rows | n/a | Attested eras: none stamped in guide sources; skill is support-role utility only |
| d3-ww-wastes | C | C | **vanilla CONTRADICTED** · set-era C · late-sets C | n/a | D-2a: Wrath of the Wastes set added patch 2.2.0 — kit identity post-vanilla |
| d3-zbarb | C | C | set-era C · late-sets C | n/a | zBarb confirmed since Season 4; Threatening Shout Falter confirmed |
| d3-zero-dogs | C | C | vanilla C | n/a | 2013 vanilla-era guide confirms build pre-RoS; honest single-source |
| d3-znec | C | C | late-sets C | n/a | Necromancer debut 2017 confirmed; Decrepify + Frailty + LotD confirmed |

## Advisory verdict histogram (file truth governs — steward recounts)

- CONFIRMED: ~40
- CONTRADICTED: ~2 (d3-ww-wastes vanilla era D-2a; d3-wave-of-force negative_canon)
- UNSUPPORTED: 0
- SOURCE_NOT_FOUND: 0

## Contradictions (one line each)

1. **d3-ww-wastes / era / vanilla** — CONTRADICTED (D-2a floor-too-early). Wrath of the Wastes set introduced patch 2.2.0 (Season 2, RoS era). Build identity is set-defined; vanilla floor predates the set's existence. Anchor: "Wrath of the Wastes set was added in patch 2.2.0. It was not available in vanilla Diablo 3 — it was introduced in the Reaper of Souls expansion."

2. **d3-wave-of-force / negative_canon** — CONTRADICTED. Claim states "no set multiplier path across any era." Fetched text shows Delsere's Magnum Opus provides +12,500% to Wave of Force vs Slow Time-affected enemies (patch 2.4.1 documented build). The claim is falsified — a set multiplier path existed in set-era. Note: Wave of Force remains non-meta/non-viable as a primary build, but the specific "no set multiplier" language in negative_canon_target is directly contradicted by fetched source. Report to erratum queue.

## SNF kits

None. All 12 kits sourced successfully.

## NULL-era kit: d3-wizard-black-hole

Attested eras from fetched text: Black Hole functions as a utility skill embedded in multiple Wizard builds (DMO Frozen Orb, Typhon Hydra, Vyr-Chantodo). No standalone Black Hole build guide exists on maxroll.gg or icy-veins. Skill introduced at D3 launch as a Wizard active ability. No era stamp as a primary BUILD documented in any current or archived guide. Steward backfill recommendation: if era field is to be populated, `set-era` and `late-sets` are plausible (skill used in those eras as utility); but a dedicated "Wizard — Black Hole" build never reached guide-level documentation as a primary archetype.

## Dossier coverage

12 kits × 6 families = 72 possible rows.
- Abstained rows: d3-wave-of-force/author_credit (no byline on consulted community page); d3-wizard-black-hole/item_alterations, capstone_alterations, author_credit, variants (no standalone build guide — skill is support-only utility).
- Total abstained: 5
- Non-abstained: 67 / 72 = **93.1%**

## Author credits by kit

| kit_id | handle | site |
|---|---|---|
| d3-tal-meteor | Chewingnom | maxroll.gg |
| d3-trag-nova | wudijo | maxroll.gg |
| d3-typhon-hydra | wudijo | maxroll.gg |
| d3-ue-multishot | Northwar / wudijo | maxroll.gg |
| d3-uliana-ep | Northwar / Raxxanterax | maxroll.gg |
| d3-vyr-archon | Chewingnom | maxroll.gg |
| d3-wave-of-force | (none recoverable) | community pages only |
| d3-wizard-black-hole | (none — no standalone guide) | — |
| d3-ww-wastes | Chewingnom / Rob | maxroll.gg |
| d3-zbarb | Chewingnom / Rob | maxroll.gg |
| d3-zero-dogs | Thander | slashnblast.wordpress.com |
| d3-znec | Northwar / wudijo | maxroll.gg |

## Red flags for steward erratum queue

1. **d3-ww-wastes vanilla D-2a — HIGH.** Wrath of the Wastes set = patch 2.2.0 (RoS, Season 2). Vanilla WW Barb existed but the KIT IDENTITY as "WW Wastes" is post-vanilla. Era floor should be `ros-early` or `set-era` at earliest. Mirrors ik-hota precedent exactly. Flag for INGEST-13 correction.

2. **d3-wave-of-force negative_canon CONTRADICTED — HIGH.** The spec's `negative_canon_target` claims "no set multiplier path across any era." This is falsified: Delsere's Magnum Opus grants +12,500% to Wave of Force (documented in patch 2.4.1 community build guides). The negative kit rationale needs revision: WoF is non-meta because it has no dedicated set (Delsere's bonus is shared across many spells, not WoF-specific), not because zero multiplier path exists. Erratum: revise negative_canon_target framing.

3. **d3-uliana-ep probe fact: `meter_type: "focus"` — PROBE FABRICATION.** Probe facts for d3-uliana-ep record `meter_type: "focus"` as the Monk resource. Monk's resource is Spirit. Fetched text confirms Spirit explicitly. This is the same fabrication pattern as basin-2 spirit/focus artifact. Flag for erratum queue; probe fact should read `meter_type: "spirit"`.

4. **d3-trag-nova probe fact: `resource_verbatim: "life+mana"` — PROBE FABRICATION.** Necromancer resource is Essence, not mana. Fetched text confirms Essence. The probe fact "life+mana" confuses life-spending mechanic with the resource meter name. Flag for erratum queue.

5. **d3-wizard-black-hole NULL-era — BACKFILL NEEDED.** No guide-level documentation exists for a standalone "Black Hole Wizard" build. Black Hole is a utility skill used across many Wizard builds. Steward should decide: (a) populate era field with `set-era;late-sets` as utility-presence attestation, or (b) retain NULL with a note that no standalone build archetype exists. Either way, a kit-level note is warranted.

6. **d3-zero-dogs single-source provenance — AMBER.** Only one era-attesting source found (Thander, slashnblast, Oct 2013). Build is vanilla-era and guide-sparse as expected per the brief. Attestation is credible (pre-RoS, byline present, mechanics match). No CDogs-era guide sourced for post-vanilla continuity — if post-vanilla era tokens are ever added to this kit, a separate source will be needed.

7. **d3-typhon-hydra: Typhon's Veil introduced Season 20 (attested).** Kit era is `late-sets` only — consistent with Season 20 introduction. Era floor appears correct.

8. **Advisory-drift disclosure.** Returned histogram is advisory. Steward recounts from committed files. Series 15-for-15 drift; expect this batch to drift.
