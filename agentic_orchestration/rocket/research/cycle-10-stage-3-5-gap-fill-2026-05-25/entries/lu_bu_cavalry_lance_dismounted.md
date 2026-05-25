# Entry: Lu Bu — Cavalry Lance (Dismounted)

## Anchor identity
- **Anchor:** Lu Bu
- **Cultural tradition:** east_asian (chinese_three_kingdoms)
- **Tier discipline:** Tier S; Tier 2 soft-attribution
- **Register:** historical

## Cohesion-judge naming-space partitioning
- Pattern family: cavalry / halberd / three-kingdoms / lance
- This entry: `lu_bu_cavalry_lance_dismounted` — cavalry-lance wielded on foot (dismounted per D1c constraint)
- Engine-internal named-bearer: Lu Bu; player-facing: "Dismounted Charge-Lance of the Vanguard"
- Note: "cavalry" in name refers to the weapon's origin/design not mounted use — D1c compliant (no mounted mechanics in BC-axes; weapon is wielded on foot)
- Discipline #25 rep-audit: Chinese cavalry lances (shuò/zhǐ) used dismounted in formation fighting; no Mode-C contamination

## Mechanical profile rationale
- BC-axes cell: `(mid, medium, spiky, STR)` — Cell 3 Polearm Brawler; medium-tempo lance thrust
- proxy_range_class: mid (lance reach extends to mid-range)
- proxy_tempo_class: medium (lance thrusts are faster than heavy mace; not high-tempo like DEX but not as slow as heavy halberd)
- proxy_geometry_class: single (lance thrust; single-point penetrating strike)
- proxy_attribute_class: STR
- Medium-tempo variant: covers the medium-tempo STR polearm facet; distinct from low-tempo heavy mace/halberd
- Spiky amplitude: lance thrust concentrates force into single penetrating spike
- Sim-viability: STR mid-range medium-tempo single; within BC envelope

## D7 AI-tell compliance
- Templated: [lance noun] + [dismounted vanguard vocabulary] + [mid-range thrust mechanics] + [Chinese Three Kingdoms period]

## gandalf curation pass
- PASS — dismounted lance correctly handles D1c; medium-tempo STR mid covers important Cell 3 variant; cavalry in name is weapon-origin reference not mounted mechanic; Discipline #25 clean
