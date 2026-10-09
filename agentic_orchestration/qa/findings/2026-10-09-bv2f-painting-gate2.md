# Finding — 2026-10-09 — BV2F full-site PAINTING Gate-2 (input to the Phase 3′ build)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** **WARN.** The verdict is **PASS-with-conditions as the build input**, with 0 BLOCK. This is **not a parity PASS**: P5 a1 and P4 snow carry disclosed FAILs to M3′.
**Target:** PT `c0fe9ee52`; final painting `fid/pt/ph3/final/painting_ph3_full.png` sha `8e169e6331bb` (6656 × 4096); conductor `9de27c5bd` (M-C9-BV2F-PAINTING-COMPLETE); ledger R-C9-268..309
**Developer:** drax (PT, LV), galadriel (PH); conductor gandalf
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (control before claim), #4 (charter + ledger as truth), #5 (severity matters)
**Governs:**
- charter § 6, § 12 W-1 / W-3, § 15, § 16;
- calibration § 44, § 48 (a)–(e), § 50, § 51;
- my pilot-4 Gate-2 (`2026-10-08-bv2f-pilot4-gate2.md`, incl. addenda A and B);
- my P5 pre-ruling `309c4c41b` (M-1..M-4).

**Method.** Every claim below was checked against the primary files, not the ledger. Numbers marked † are my own read-only probes. They are **not binding**, and PH's readings bind. No Godot was run and no image was spent.
- My snow-spectrum probe reproduces PT's per-wave P4 values exactly (4_0 0.095, 3_1 0.035, 3_2 0.061, old 3_3 0.069, 3_3-r1 0.115, 4_3 0.151, 4_4 0.177), so it is the same instrument.
- `verify.sh` was run by me and exits 0 (25 files).

---

## 1. Verdict: PASS-with-conditions as the build input

**What was verified clean.**

| Check | Evidence | State |
|---|---|---|
| Canvas set | `canvases.json`: all 25 resolve through the stitch's own `src()` order (src_suffixes → -r1 → plain) to the listed dir, and every sha256 matches† | ✓ |
| Pilot identity zone | x < 3840, y < 2304 of `8e169e6331bb` vs the reviewed layer-4 pilot `1b48c75bc16c`: **0 px differ**† | ✓ |
| Layer 5 | Changes 177,840 px, bbox x 1316–1750 × y 3107–3546†, entirely outside the pilot. Exactly 1 image. | ✓ |
| Geometry ⊆ repaint | Every guide pixel (215,261) and class pixel (71,489) that LV `023686e3c` changed inside the pilot lies **100 % under the DEV-24 layer-4 support mask**†. No pilot pixel shows old geometry over new geometry. | ✓ |
| Guide of record | Every Phase 3′ tile LV changed at R-C9-294 (`tiles_294.json`) was painted after the `023686e3c` pins. Unchanged tiles (3_0, 4_0, 3_1, 4_1, 4_2, 4_3) match. | ✓ |
| Tier-B | `verify.sh` exit 0†. `dev24.py` `8447a778c927`, `guided_paint.py` `dedb8d010414` and `guided_stitch.py` `94fa0d7b32b9` match SHA256SUMS. | ✓ |
| Positive control | v1 `barrow_full_painted.png` sha `eecb42661af4…`†, unchanged | ✓ |
| Images | Ledger `image_calls`: BV2F-PH3 **43**, BV2F-LR4 **23**, BV2F total **188** (under the ~250 guard). Caps were raised by conductor ruling (R-C9-296, R-C9-303) inside § 6 authority. | ✓ |

**Why PASS-with-conditions and not PASS.**
- The record misstates its own FAIL count (§ 2).
- Most of the carried-join evidence was cropped from intermediate previews or superseded canvases, not from the painting that ships (§ 2, #75 cl. 1).
- P6a triage is unrecorded for 21 candidates on kept canvases (§ 3).
- The painting's irreplaceable inputs exist on one disk, untracked (§ 5 R-1).

None of these hides a defect. My own probes found no line, no invented opening and no tone ring. All of them are 0-image fixes.

**Why it is not FAIL or BLOCK.** Every FAIL is measured and disclosed. Nothing is masked (§ 3). The build input is pinned, reproducible from pinned inputs, and verify-green. Whether the parity FAILs are accepted is **Matt's call at M3′**, as it was at M2″ (R-C9-268).

---

## 2. Carried raw a1 FAILs and P4 snow FAILs: ruling

### 2(a) The "8 carried, stitch-corrected" joins: dispositions ACCEPTABLE under M-1, but the count and the evidence are wrong

Under M-1 a raw a1 FAIL **stays a FAIL**. "Carried" is a disclosure of a FAIL whose stitched painting shows no line. Each of the eight has a conductor by-eye no-line read, except 3_3/3_4 (below).

My own 1:1 look at the **final** painting:
- 3_1/3_2: no straight line; the yard grades from snow-patched to darker ash;
- the 3_2/3_3 cave-stair corner: continuous across x 3840 / 4096 and y 2304 / 2560;
- the layer-5 corner: repaired.

That concurs with the conductor. It is not binding.

**Corrections, all 0 images:**
1. **The count is 10 Phase 3′ raw a1 FAILs, not 8.**
   - The kept 1_4-r1 reads **0_4|1_4 11.193** and **1_3/1_4 10.946** (`qa_w15`).
   - DEV-24 layer 5 corrected the *stitched* pixels. Under M-1 that never changes the *raw* verdict.
   - The QA summary files them under "repaired" and the milestone under "carried: 8". **Both undercount.**
   - Site-wide, with the 3 pilot-internal joins, that is **13 of 40 neighbour joins FAIL raw a1** (v1: 0).
2. **3_1/3_2 has no disposition of its own.**
   - R-C9-293 carried 24.562 against the **superseded** 3_2.
   - The kept pair (3_2-r1) reads **29.185** (`qa_w7`), and no ruling line covers it.
   - Packet crops 02/03 are md5-identical to `qa_w5/*`, i.e. the **old 3_2**.
3. **3_3/3_4 9.574** was classified "carried-type" by PT and passed over without the stop R-C9-303 required ("stopping only on a failed check"). The margin is 0.005. It needs one conductor by-eye line.
4. **The evidence is stale, not of the painting that ships (#75 cl. 1).** Traced by md5:
   - 07 (0_3|1_3 seg 8) and 09 (0_3/0_4 seg 11–12) predate 0_4/1_4, and predate layer 5, which repainted x ≥ 1316, y ≥ 3107 across both segments.
   - 08 is raw strips, not a stitched crop.
   - 19 is the superseded 1_4. 21 is the superseded 4_2.
   - DEV-26 re-cuts every unpinned band whenever a chunk is added, so any crop taken before the last chunk is not the shipped join.
   - **Remedy:** re-crop all 13 FAIL joins at 1:1 **from `8e169e6331bb`**; the conductor re-confirms by eye.
5. **INFO.** The diagonal 0_2\1_3 reads **7.42** against v1's corner bar 4.809. It is report-only per § 51, which did not list it, but it must be disclosed beside the FAILs.

### 2(b) The 3 P4 snow-spectrum FAILs (3_3-r1, 4_3, 4_4) and R-C9-305's standing rule: ACCEPTABLE as disclosed FAILs. The stated cause is not supported.

**The rule is legitimate.**
- It changes the wave **cadence**, not a verdict, bar or support rule (W-1 intact).
- It was ruled before 4_4 was read, so it is not post-hoc for 4_4.
- The histogram and guard conditions are sensible co-signals.

**The conductor's hypothesis (v7.1's "rounded cobble cells" wording) is weakened by the data.**
- 3_1-r1 and 3_2-r1 were painted under the same v7.1 and pass at **0.035 / 0.061**.
- The rival hypothesis is named here (#87): **wavefront drift by inheritance.** My probe† splits each chunk's snow windows into paste-strip and interior:

| chunk | spec (bar 0.097) | strip / interior | fine-period dev | coarse-period dev |
|---|---|---|---|---|
| 3_1-r1 | 0.035 | 0.029 / 0.062 | −0.038 | +0.037 |
| 3_2-r1 | 0.061 | 0.025 / 0.089 | −0.063 | +0.019 |
| 4_0 | 0.095 | 0.027 / **0.104** | −0.112 | +0.099 |
| old 3_3 | 0.069 | 0.100 / 0.087 | −0.020 | −0.023 |
| **3_3-r1** | **0.115** | 0.075 / 0.155 | −0.113 | +0.036 |
| **4_3** | **0.151** | 0.112 / 0.163 | −0.148 | +0.091 |
| **4_4** | **0.177** | 0.157 / 0.197 | −0.189 | +0.127 |

- **One signature:** fine-grain deficit plus coarse excess, i.e. **softer snow**.
- It **grows monotonically** along the paste chain 3_3-r1 → 4_3 (left context 3_3-r1) → 4_4 (top context 4_3). The interior is always worse than the strip.
- 4_0, the other far wavefront chunk, has the same sign and sits 0.002 under the bar.
- Old 3_3 had the **same contexts** as 3_3-r1 and passed the spectrum (it failed the guard). So the chain likely **started from a stochastic soft draw on the 3_3 repaint and was inherited downstream.**
- **This is the pilot-4 § 4 mechanism** ("the painter continues the grain it is handed"). The standing rule carried a FAIL canvas that was **paste context for unpainted chunks**, which is exactly where propagation happens.

**Disposition.**
- The three are **FAILs of record at M3′**.
- Together with the pilot's four, the P4 snow row reads **7 FAIL of 15 judged chunks** (pilot 4/9, Phase 3′ 3/6).
- PH runs a 0-image, report-only forensic that discriminates the two hypotheses before M3′. Examples: spectrum vs paste depth over every snow-supported chunk; the same split on old 3_3 vs 3_3-r1.
- **No wording change is adopted on the conductor's hypothesis.**

---

## 3. Tier-B stack: masking and re-verification

- **M-1 held again.** Raw a1 is the only instrument that registered the 3_1/3_2/4_2 ash-yard redraws and the four-chunk corner. Keep it raw.
- **DEV-24 `read_zone` and pinned correction field (R-C9-301/302): no masking found.**
  - The risk was a correction field computed on the 3 × 3 base and then applied over the *blended* full-site strips, which would leave a tone ring at the mask edge.
  - Probe†: the inside-vs-outside step at the layer-4 mask edge in the strips (n = 66) is p50 **1.60** / p90 16.5 / max 36.1 in the final, against **1.49** / 17.3 / 36.1 in the reviewed pilot. In the identity zone the two are identical (by construction).
  - At y = 2560 and y = 2304 the straight-line excess peaks only at floe and lead **content edges** (verified by eye). There is no straight seam.
  - The P-2b re-run (`p2b_l4.json`) shows the control moving 780,978 px, so the proof can fail.
- **DEV-29 (context patch): mechanics correct, domain gap disclosed.**
  - The real-mask substitution check passes on 0_2 / 1_2 / 2_2 (`qa_w18`: 0 px outside the mask, inside = patched).
  - The mask covers **65.6 %** of the pilot's bottom strip and **17.9 %** of its right strip†. That is a large share of what 0_3–3_3 were shown.
  - **Gap (R-C9-304, below):** § 51 named its joins rather than deriving them, so 3_2/3_3 (corner 100 % in the mask†, with 3_2-r1 staged pre-DEV-29) fell outside it.
- **src_suffixes:** plumbing only. Flag-off reproduces `a25fb3`, and the resolution matches the manifest (above).
- **Allowlist pins check: sound, under-recorded.**
  - The verdict of record (215,261 px, all inside the 45 rects) exists only in stdout, the ledger and LV's proof.
  - **`pins_ph3.json` still carries `"r_c9_189": "HALT: pilot tiles changed -> repaint"`.** A build-time reader of the pin file reads a HALT.
  - LV's proof references its reference images in a session scratchpad. I verified their shas equal the 67fc pins (`8cfd9d8e43b9`, `d86fb5f1512b`). Record those shas in the proof.
- **P6a: triage unrecorded on kept canvases.**
  - § 50 addendum says sea-class candidates go to by-eye triage "with its crop … never auto-passed". There are no Phase 3′ `p6a_triage*.jsonl` rows, and no crops for **1_4-r1 (7), 2_4-r2 (11), 3_4 (3)**. Packet 19 is the superseded 1_4.
  - My class check†: all 21 are **100 % class sea**, and my eye on the 2_4/3_4 crop finds open water only.
  - **Record mismatch:** R-C9-295/300 call 4_2's candidates "class char". The kept 4_2-r1's candidate at **(6446, 1789) is class wood**: the longhall wall. My eye: a timber wall behind fallen rafters, no opening.
  - **P6a was never run on the DEV-24 layer-4/5 output.** That is post-stitch service paint, and it is what ships.
- **DEV-24 share (state it at M3′).**
  - Layers 1–5 change ≈ **2.97 M px** (layer-sum; ≤ **10.9 % of the site**). Layers 1–4 change ≤ **28 % of the pilot** (13 % at pilot 4).
  - Seam patches: 3 site-wide out of 25 chunks, inside DEV-13's ≤ 15 %. Images 23/24.
- **Matt ratification [ESCALATE, ADR-002]:**
  - DEV-29 and the `read_zone` / pinned-correction re-base were ruled by the conductor as companions of the Matt-ratified DEV-24, "recorded for his eye". **That is not ratification.**
  - Both change what ships (DEV-29 changes the painter's input for four chunks).
  - They go on the **M3′ ratification line** by name. If Matt refuses DEV-29, those four chunks are repainted.
- **Charter § 16 is stale and GOVERNS.** It lacks:
  - layers 4–5;
  - `read_zone`, with the corr npz shas;
  - the L5 seam patch;
  - src_suffixes;
  - DEV-25c's outcome (**NOT adopted**, R-C9-281);
  - the counts (it still says "8 patches / 16 images").

**Re-verify at the build: P-4 in substance.**
- The build's stitch, re-run from the pinned inputs after the restart, must reproduce **`8e169e6331bb` byte for byte**. The identity zone must read 0 px against `1b48c75bc16c`.
- A difference is a **HALT, never a re-base**.
- PT's QA summary already shows zone identity on the archived painting, and I reproduce it. What the build adds is **determinism after the restart and identity of the file the take actually reads** (#75 cl. 1).

---

## 4. Conductor errors (R-C9-287/298/307) and R-C9-304: discipline notes

Attributable images: **8 of 43**: R-C9-287 = 2; R-C9-298 = 2 + 2 for the consequent 4_2-r1; R-C9-307 = 2. Phase 3′ overran its ~35 plan by **8**. The conductor recorded each error himself, which is the record working as intended.

**These are instances of existing disciplines. No new number (#76 cl. 5 retrieval note).**

| Ruling | What happened | Discipline |
|---|---|---|
| **R-C9-298** | "Repaint 3_2 to carry the eroded columns": the columns lay in the pilot C rects | **#83** (confirm the surface can carry the remedy). Both discharges were 0-image: diff 3_2's strip guide. |
| **R-C9-306/307** | "Repaint 1_4 to remove the corner line": the line sat at the overlap ends x = 1536 / y = 3328, on 0_4's side | **#83**. Discharge: locate the line against the grid. |
| **R-C9-287** | Geo v7 (R-C9-258) dropped the ash-yard clause | **#72** (with #76 cl. 2). The mechanical sweep v7.1 later ran (v6 vs v7 vs every unpainted tile's class list) was owed **at v7's landing**. |
| **R-C9-304** | — | See below |

**R-C9-304.**
- **The refusal was correct.** Extending § 51's substitution to a non-pilot side after reading is a post-hoc instrument change (W-1). The FAIL stands, with the diagnostic 1.19–4.27 non-binding.
- The defect upstream is **#76**: § 51 **enumerated** pilot-side joins instead of **deriving** the domain from mask geometry × staging chronology. `context_vs_allowlist.json` (R-C9-298) held the data to derive it before registration.
- **Forward fix:** PH pre-registers the derived domain before any M3′ a1 reading. 3_2/3_3 stays FAIL-of-record as read.

**One local procedure note.** It is pipeline-specific and belongs in calibration § 48 (e), not the discipline corpus. **"Locate before repaint":**
- Before any repaint for a visible line, tabulate the line's coordinates against overlap ends, band centres, DEV-26 cut paths and DEV-24 patch edges.
- If it coincides with any of them, it is **structural**: use a DEV-24 seam patch, never a chunk repaint.
- Corollary for any future carry rule: a disclosed-FAIL canvas that is **paste context for unpainted chunks** is a propagation risk (§ 2(b)) and stops the wave.

jack-ryan folds the #72/#76/#83 instances into `engineering-disciplines.md` in a separate docs commit (not this one).

---

## 5. Build entry checklist (after the restart)

[R] = before the restart **and before any disk deletion** · [E] = before take/bake/build · [H] = before any M3′ value is read · [M] = Matt

**R-1 [R] (single-disk risk).** Everything the build consumes is **gitignored and on one disk**: `*.png` and `*.npz` under `astra_test_01/.gitignore`. That covers:
- the 25 canvases;
- the 12 DEV-24 patch region / paste / new PNGs;
- the 3 corr npz;
- the context_patch painting and mask;
- the pinned guide / ids / class copies;
- the final painting;
- **23 of the 24 M3′ packet crops.**

The service cache's `regeneratable_until` is not a backup. Disk is at **23 GiB** and deletions are Matt's. So:
- PT writes and **commits** one input manifest (path + sha256, generated from `canvases.json` and the PH3 cfg) and a check script;
- every deletion list excludes these paths;
- copying the set to a second volume is a `matt_to_do`.

**E-1.** Run `pwd` and use `git -C` throughout. `git status --porcelain` is clean on `fid/v1tools/`, the PH3 cfg and `fid/lv/`. LV's uncommitted `walk/walkability.md` is committed or explained.

**E-2.** `verify.sh` exit 0; `cfg_check` OK; the R-1 manifest check exits 0. Positive control per § 6: v1 painting sha `eecb4266…` and `godot/data/painted/` shas recorded before and after; `barrow_full/` shows no BV2F path outside the LV allowlist.

**E-3.** Disk **≥ 25 GiB** (now 23); macOS auto-install off (T34). Otherwise HALT.

**E-4. P-4.** Re-stitch from pins; the sha must equal `8e169e6331bb`; the identity zone is 0 px against `1b48c75bc16c`; the L5 bbox is as recorded. Any difference is a HALT.

**E-5. Pins.**
- Re-run `pilot_pins_check --allow allow_294.json`, **writing a JSON record**, and correct `pins_ph3.json`'s `r_c9_189` field.
- LV regenerates the level at **`023686e3c`**; its guide / ids / class render must sha-match `cbb4496aee5b` / `d49d7e5108bc` / `bbe0eab6715f` before the take.

**E-6. Charter § 16 folded (§ 3 list).** DEV-29 and the re-base are placed on the M3′ ratification line.

**H-1. P5.**
- PH computes the full a1 table on the pinned canvases (§ 44; § 51 with the **derived** domain pre-registered).
- **P5(b) on the final painting.** It has not been computed for any Phase 3′ join.

**H-2. P6a.**
- Run on the **final painting** (covers the DEV-24 L4/L5 regions).
- Triage rows and crops for every unmatched candidate on kept canvases, including 1_4-r1, 2_4-r2 and 3_4.
- Correct the 4_2 class record.

**H-3. P4.**
- Snow and rock per § 50 (b).
- **Ice: declare the domain** (#70) — which of ice / ice_mid / tide_ice / shore_ice / lead it reads — against the frozen Lab, before reading.
- The snow forensic of § 2(b), report-only.

**H-4. P11.**
- **Derive** (#76) the mapping of every full-site class into `ALLOWED` / `EXCLUDED`. Ash, char, shingle, tide_ice, shore_ice, ice_mid, lead, passage_dark and path have no entry in `p11_abx.py` today.
- The ruling is made pre-data. Report the drawable-trial count. **Fewer than 40 = VOID, declared before any judge.**
- B-3: phase-matched stills (§ 50 (a)).

**H-5.**
- **P9c** on the floe field, owed since R-C9-189 W-5; include a view inside L5's repainted floes, whose outlines changed.
- P8.
- **P10** only inside a quiet window (T34; [Bb] 11 still open).

**H-6. Packet.**
- Re-crop all 13 raw-a1-FAIL joins from `8e169e6331bb` (§ 2(a) 4); the conductor re-confirms.
- Add conductor lines for 3_1/3_2 at 29.185 and for 3_3/3_4.
- Track crops as jpg, or record their shas.

**M-1 [M] M3′ cover states plainly:**
- **P5 a1 FAIL on 13/40 joins** (raw; no line by eye) and 0_2\1_3 report-only;
- **P4 snow FAIL on 7/15 judged chunks**, with the drift hypothesis;
- the DEV-24 share;
- **DEV-29 and the re-base for ratification.**

Also on the cover, for Matt's eye:
- the **crack-line net**, which spans the row-4 sea (1_4 / 2_4 / 3_4), not 0_4 only (my 2_4/3_4 crop);
- the 10.11 m² of locked pilot stacking. LV reconciles it with the audit's 3.1 m² first: the two definitions disagree.

## Action

- [ ] **PT (drax):**
  - R-1 manifest, check script and commit;
  - E-4 P-4;
  - E-5 pins record and `pins_ph3.json` fix;
  - H-6 re-crops and packet hygiene;
  - QA summary count corrected to 10 Phase 3′ raw a1 FAILs.
- [ ] **LV (drax):**
  - E-5 regenerate at `023686e3c` and sha-match;
  - `walkability.md`;
  - allowlist-proof reference shas;
  - reconcile 10.11 vs 3.1 m².
- [ ] **PH (galadriel):**
  - H-1 (derived § 51 domain pre-registered; P5(b));
  - H-2 (P6a on the final painting and triage rows);
  - H-3 (ice domain; snow forensic);
  - H-4 (P11 class mapping, pre-data);
  - H-5.
- [ ] **Conductor (gandalf):**
  - ledger row for this finding;
  - dispositions for 3_1/3_2 at 29.185 and 3_3/3_4;
  - § 16 fold (E-6);
  - "locate before repaint" into § 48 (e);
  - corrected milestone count.
- [ ] **jack-ryan:** fold the #72 / #76 / #83 instances (§ 4) in a separate docs commit.
- [ ] **Matt (ESCALATE, at M3′):**
  - ratify or refuse DEV-29 and the DEV-24 `read_zone` / pinned-correction re-base;
  - accept or refuse the P5 a1 and P4 snow FAIL rows as stated;
  - `matt_to_do`: second-volume copy of the R-1 input set before any deletion.

## References

- **Ledger:** `astra_test_01/burst/runs/C-9/ledger.json`: R-C9-268..309, M-C9-BV2F-PAINTING-COMPLETE, and `bursts[].image_calls` (BV2F-PH3, BV2F-LR4).
- **Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` §§ 6, 7, 12, 15, 16.
- **Calibration:** `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/calibration.md` §§ 44, 48–51.
- **PT, final** (all under `…/barrow_v2/fid/pt/`):
  - `ph3/final/{painting_ph3_full.png, painting_pre_l5.png, canvases.json, qa_summary.json, stitch_final.log, corner_l5_before_after_*.png, m3p_packet/index.json}`;
  - `ph3/qa_w1..w18/qa.json`;
  - `ph3/{pins_ph3.json, allow_294.json, context_vs_allowlist.json, class_art_pinned_023686e3c.png, guide_art_pinned_023686e3c.png}`.
- **PT, DEV-24 and pins** (same root):
  - `dev24/{dev24_block_l4.json, l4_support_mask.png, painting_dev24_l4.png, ps4_l4_g*-1_corr.npz, spec_ph3_corner_l5.json}`;
  - `r272/fullsite/{fullsite_proof.json, p2b_l4.json}`;
  - `pilot/cfg_bv2a_ph3.json`;
  - `tools/{ph3_wave_qa.py, ph3_pin.py, pilot_pins_check.py}`.
- **Frozen toolchain:** `fid/v1tools/{verify.sh, SHA256SUMS, ALLOWLIST.md, dev24.py}`.
- **LV:**
  - `fid/RESUME_LV.md` (R-C9-283 / 289-290 / 294 sections);
  - `fid/lv/art/{ice294_proof.json, pilot_allowlist_294.json, ice_audit.json, tiles_294.json}`;
  - `fid/lv/guide_art/guide_manifest.json` (class legend).
- **Harness:** `fid/ph/harness/{p4_texture.py, p11_abx.py, p11_abx3.py}`.
- **Prior findings:**
  - `agentic_orchestration/qa/findings/2026-10-08-bv2f-pilot4-gate2.md` (incl. addenda A and B);
  - `…/2026-10-08-bv2f-p5-dense-texture-preruling.md`.
- **Disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #70, #72, #75, #76, #83, #87.
