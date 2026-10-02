# p05 emergence frames: waves 151, 152, 153 and 157

**Question (KP-216 / ambush-semantics gap G-1):** at wave onset +3.5 to +9 s, do bodies emerge at the p05 point near the arena centre? Do they show a nameplate or health bar while emerging? (Matt says they do not.)

**Labels:** FOOTAGE = read from the referent recording. DATAMINED = from GD's shipped data (prior laps). INFERRED = my reasoning.

## Method

- **Onsets (FOOTAGE).** The wave badge's first changed frame at 60 fps (crop 60×40 at x 1575, y 130, frame difference): w151 **682.10 s** (equal to the "New Mutators Active" banner onset at 682.12 s), w152 **698.42 s**, w153 **714.68 s**, w157 **780.32 s**. The badge animation may lag the engine's wave flip by about one frame to 0.1 s, so the true +4.000 s release can sit up to about 0.1 s *earlier* on this clock.
- **Frames.** 30 fps over onset +3.0 to +9.5 s, all four waves (195 frames each, half resolution, in the scratchpad; not committed). Full-resolution exact-seek frames at the p05 plate positions, tiled in `evidence/`.
- **Plates.** The same 30 fps windows went through the census (`tools/census.py`): every in-world `(cur/max)` readout, OCR'd with galadriel's eye-verified glyph atlas, and allegiance read from the bar colour under it. A p05 body is identified by its max-HP fingerprint (Lap D eHP, DATAMINED).

## Results

| wave | p05 body (fingerprint) | first in-world plate, s after badge flip | HP at first plate | screen position at first plate | what the frames show |
|---|---|---|---|---|---|
| 151 | Carnivorous Plant L104 (278,543) | **+3.93** | full | (1640, 833), lower right | A dust and smoke burst at +3.93. A thorny plant tendril is visible at +4.10, and the spiky pod grows through +4.4 and +4.8. The plate is up throughout. |
| 151 | Carnivorous Plant L103 (272,948) | +4.33 | full | (1344, 952) | Second plant. Its plate is at the frame edge by +3.93 in the full-resolution crop. |
| 152 | aetherialcorruption hero class (443,554) | **+4.27** (partly in frame from +3.90) | full | right edge (1739, 410) | Two green crystalline hero bodies are already standing with full plates at +4.27. By +4.6 both are upright and moving. The p05 point is at the screen edge, so the start of the clip is not visible. |
| 153 | Ugdenbog Golem L104 ×2 (417,957) and L105 (427,128) | **+3.90** | full | (265, 746), (240, 890), (27, 759) | Nothing at +3.85. At +3.95 there are three plates, a blue spawn flash at one, and ground debris through +4.2. **The 417,957 golem's HP reads 407,378 at +4.60**, which is inside its 3.567 s appearance clip. |
| 153 | Carnivorous Plant L103 (273,975) | +4.87 | full | left edge (161, 883) | Off the left edge until +4.5. |
| 157 | imp hero class: Phigillius Stormbile, aetherialimp_h01 (457,975) | **+3.83** | full | top edge (459, 18) | A teal aetherial burst plays on the **central dais** (the raised square with the skull pile) at +3.95 and +4.30. At +5.0, three hero plates (457,975 ×2 and 447,590) and Blugrug sit on the dais. |

**Plate first-appearance times:** +3.83, +3.90, +3.93 and +4.27 s, with the +4.27 one at the screen edge. Against the DATAMINED release of +4.000 s and the badge-lag allowance, the in-world plate appears **at the spawn instant**. It does not appear at release + spawn-clip length, which would be golem +7.57 s, plant +5.5 s and imp hero +5.53 s.

## Answers

1. **Bodies emerge at p05 near the centre: CONFIRMED (FOOTAGE)** on w151, w153 and w157.
   - w151: a dust burst and a growing plant.
   - w153: a flash and debris.
   - w157: a teal burst on the central dais, then the three imp heroes stand there.
   - w152: the point is at the screen edge, so the hero bodies are already formed when they come into view.
2. **Nameplate or health bar while emerging: Matt's recollection is NOT supported for the in-world plate.**
   - On every wave checked, the red health bar and its `(cur/max)` text appear on the first frame of the spawn, at full HP. They stay up through the whole emergence animation.
   - **Damage lands during emergence:** the w153 golem lost 10,579 HP 0.7 s into its 3.567 s clip. This is consistent with the DATAMINED decode: hittable, killable, and immune to CC actions while in `SpawnAction`.
   - **What this does NOT test.** The top-centre hovered-monster plate (name, level, family) and cursor selection belong to a separate UI layer. No hover landed on an emerging body in these four windows. The earliest hover in each wave is a ring body: Ancient Wraith at w151 +3.7 s, and nothing on a p05 body before +7 s. So "cannot be hovered or selected while emerging" is **UNTESTED**, not contradicted.
3. **Consequence for the pack (INFERRED):** `v3p8_rows.am6_emergence_presentation` (the port-side "no plate, no bar, not selectable while emerging" rule) contradicts the footage for the in-world bar. The simulation rows (AM-2/AM-3: inert but hittable for the clip length) are untouched and are corroborated by the golem taking damage.

## Evidence

- `evidence/p05_w151_plant_onset+3.80-5.30.png`
- `evidence/p05_w152_heroes_onset+3.90-6.00.png`
- `evidence/p05_w153_golems_onset+3.85-7.80.png`
- `evidence/p05_w157_dais_onset+3.70-6.00.png`
- 30 fps first-seen tables: reproducible with `tools/p05run.py` → `tools/census.py`. The census JSON stayed in the scratchpad.
