# Entry: Lu Bu — Northern Warlord Crossbow

## Anchor identity
- **Anchor:** Lu Bu
- **Cultural tradition:** east_asian (chinese_three_kingdoms)
- **Tier discipline:** Tier S; Tier 2 soft-attribution
- **Register:** historical

## Cohesion-judge naming-space partitioning
- Pattern family: three-kingdoms / warlord / crossbow / ranged
- This entry: `lu_bu_northern_crossbow` — northern warlord + crossbow (Chinese repeating/heavy crossbow of the period)
- Engine-internal named-bearer: Lu Bu; player-facing: "Northern Siege Crossbow of the Han Warlords"
- Discipline #25 rep-audit: Chinese crossbow (nǔ) was extensively used in Three Kingdoms period; no Mode-C contamination; Han/Northern qualifier is geographic-historical, not contemporary political

## Mechanical profile rationale
- BC-axes cell: `(ranged, low, spiky, STR)` — ranged STR low-tempo spiky; covers GC-1 PCFS-failing archetype
- proxy_range_class: ranged (crossbow is ranged primary)
- proxy_tempo_class: low (heavy crossbow; deliberate aimed shot; slow reload)
- proxy_geometry_class: single (bolt strike; single-target)
- proxy_attribute_class: STR (heavy crossbow requires STR to operate; STR-scaling ranged weapon)
- PCFS-gap coverage: `(ranged, low, STR)` was GC-1 PCFS-failing archetype (76/80 floor); this STR-ranged entry contributes to Sidecar B compound signal per § 4.1
- Sim-viability: STR ranged low-tempo spiky single; within BC envelope; standard heavy-crossbow pattern

## D7 AI-tell compliance
- Templated: [crossbow noun] + [northern warlord vocabulary] + [ranged low-tempo bolt mechanics] + [Chinese Three Kingdoms period]

## gandalf curation pass
- PASS — Chinese crossbow is important Three Kingdoms weapon; STR-ranged covers GC-1 PCFS-gap compound signal; northern-warlord naming within Lu Bu partition; Han qualifier is historical-geographic; Discipline #25 clean
