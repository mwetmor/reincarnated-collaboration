# Camera B′ — Re-ratification (dist-only revision of Camera B) — Matt sign-off record

**STATUS:** ACTIVE (binding for the v2 Godot demo — the camera every floor inherits).
**Date:** 2026-07-07
**Author:** jack-ryan (recording a made decision — NOT re-litigating it).
**Authority:** Matt live-review ruling 2026-07-07 (walltop play-shell). Verbatim ruling below (§4).
**Supersedes (dist axis only):** the Q8 Camera-B ratification — `reincarnated-godot/data/camera_floor1_ratification.md` (drax, 2026-07-02) — on the **distance** parameter (34 m → 20 m). FOV / pitch / yaw were NOT re-opened and carry forward from Q8 unchanged.
**Composes with:**
- `reincarnated-godot/data/camera_floor1_ratification.md` — the original Q8 Camera-B ratification artifact (FOV 40 / pitch −55° / yaw 47° / dist 34m). This record is its dist-axis successor; the two are read together.
- Decisions-log entry `2026-07-07 — Camera B′ RULED (dist-only revision …)` (`~/Games/reincarnated-engine/design/decisions/decisions-log.md`).
- Decisions-log entry `2026-07-07 — Q7 RULED (Option A) …` — its "FIXED Camera B (… dist 34m)" references are reconciled by the B′ entry (dist-axis note added, not deleted).
- Q7 decision doc `agentic_orchestration/matt_decision_needed/2026-07-07-Q7-bonemap-vs-generalskeleton.md` and dispatch `…/dispatches/2026-07-07-drax-q7-optionA-rig-gated-D6-D5-D8.md` (D5/D6/D8 render+capture were gated under Camera B dist 34; that hold LIFTS under B′ — see §6).

---

## 1. The question Matt ratifies

The **character register** of the v2 Godot demo camera — how large the hero reads on screen — under the already-ratified Camera B basis (FOV 40 / pitch −55° / yaw 47° fixed). This is the axis Q8 never measured: Q8 ratified Camera B on **room-band legibility** (does the 20–30 m combat room fit the frame — measured floor ~40.6 m near-edge / ~48.9 m legible band). Matt's live play of the walltop play-shell (`reincarnated-godot`, `scenes/walltop_playshell.tscn`) surfaced the missing axis: *"Diablo 3 is definitely zoomed in further (character size is larger vs the camera)."*

## 2. The finding — hero screen-register empirical ladder (drax, 2026-07-07)

Evidence: `~/Games/reincarnated-godot/harness_logs/playshell_2026-07-07-zoomladder-d{34,24,20,17.5}/` (silhouette + composite captures per distance).

**Height correction (load-bearing — it is what broke Matt's first ruling apart):** the King world-space height was **measured** at **h = 2.123 m** feet→crown, NOT the 1.8 m that had been assumed. The crown adds ~0.27 m over the 1.8 m assumption. Every fraction below is against the measured 2.123 m.

Hero screen-fraction at FOV 40 / pitch −55, feet→crown geometric, and the pixscan figure (includes the up-held blade + bloom):

| Camera distance | Hero screen-fraction (geometric, feet→crown) | Pixscan (incl. up-held blade + bloom) |
|---|---|---|
| 34 m (Camera B / Q8) | 4.80% | 5.74% |
| 24 m | 6.73% | 10.56% |
| **20 m (Camera B′ / RULED)** | **8.02%** | **12.69%** |
| 17.5 m | 9.10% | 14.63% |

## 3. Genre anchor — MED confidence, conflict RECORDED not resolved (flagged honestly)

The D3 hero-fraction target is community-inferred and **the two reads conflict**:

- **≈8–9%** (gandalf read) — the band the 20 m ruling lands in geometrically (8.02%).
- **~10–15%** (drax cite).

**Both are community-inferred, MED confidence.** The conflict is recorded, not adjudicated. The named **HIGH-confidence** resolution path, if it ever matters: **galadriel pixel-benchmark of our capture vs real D3 screenshots.** Not invoked here — the ruling did not require it.

## 4. The ruling sequence (recorded faithfully)

1. **Matt's first ruling: "7%–7.5% and 20 m."** Internally consistent under the OLD 1.8 m height assumption (where 20 m produced ~7%). The **measured 2.123 m broke the target and the distance apart**: at the true height, 20 m yields **8.02%**, above the 7–7.5% band. The two constraints could no longer both hold.

2. **The reconciliation fork (gandalf presented):**
   - **22 m → 7.29%** — lands in the stated band; a D4 / Last Epoch character register.
   - **20 m → 8.02%** — above the band; a D3 character register.

3. **Matt ruled the fork: *"On the camera, let's try 20m."*** — i.e., he chose the **D3 register** (larger character, 8.02%) over the band-consistent 22 m. The distance is the binding axis; the 7–7.5% band was the pre-height-correction proxy for it and is superseded by the direct dist ruling.

**RESULT — Camera B′:** FOV 40 / pitch −55° / yaw 47° / **dist 20 m**, hero fraction **8.02% geometric**. This is a **dist-only** revision of Camera B. **FOV, pitch, and yaw were NOT re-opened and stay closed** (carry forward from Q8 unchanged).

## 5. Implementation (verified read-only by jack-ryan)

- `reincarnated-godot` commit **`67e128e`** — `scripts/playshell.gd` ONLY; `CAM_DIST 34.0 → 20.0`; comment block rewritten to the Camera B′ lineage (records B as the Q8-ratified basis, B′ as the dist-only revision). `CAM_FOV`/`CAM_PITCH`/`CAM_YAW` unchanged. Confirmed via `git show 67e128e -- scripts/playshell.gd`.
- Prior lineage: **`6b41967`** (walltop room → F1-scale, `FLOOR_TILES 14`, 17.5 m edge — the review room for the zoom ladder) and **`46cb19f`** (Camera B swap into the play-shell — FOV 20→40 / pitch −50→−55 / yaw 47 unchanged / dist 16.5→34, superseding the rejected harness portrait cam).
- Smoke: **6/6 SHOOT frames err=0** at the new distance — `reincarnated-godot/harness_logs/playshell_2026-07-07-camBprime-smoke/` (compass, occlude_control, occlude_top50, playshell_regression, sword_idle, sword_walk). Confirmed present read-only.

## 6. Consequence — the D5 / D6 / D8 render+capture HOLD LIFTS

All D5 / D6 / D8 captures now fire under **Camera B′ (dist 20)**. This **supersedes the "dist 34" language** in the 2026-07-07 Q7 decision doc and anywhere else Camera B's distance is quoted for a capture config (e.g., the Q7 decisions-log entry's "FIXED Camera B … dist 34m" references — reconciled, not deleted, by the B′ decisions-log entry). Room-band legibility is unaffected (a dist-only pull-in tightens the hero read; the room still frames — B′ keeps the Camera B basis).

## 7. Harness finding (recorded — drax caught it)

SHOOT-mode frame grabs require `--rendering-driver metal` **WITHOUT** `--headless`. `--headless` forces the Dummy rasterizer → the SubViewport has no framebuffer → `get_texture()` returns null → every `save_png` errors. **Dispatch templates must never pair `--headless` with SHOOT captures.** (This is orthogonal to the min-spec probe, which is legitimately `--headless` because it measures the CPU sim-loop slice only and never grabs frames.)

---

**Signed:** jack-ryan, 2026-07-07. *Recording a made decision. Camera B′ is Camera B pulled to 20 m for a D3 character register; the basis is unchanged, the hold lifts, the captures fire.*
