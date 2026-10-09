# Finding — 2026-10-09 — BV2F full-site 3D BUILD Gate-2 (site_ph3, r332): the M3′ candidate

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** **WARN.** The verdict is **PASS-with-conditions as the M3′ candidate**, with 0 BLOCK. This is **not a parity PASS**: P5 a1, P5(b), P4 snow and P11 carry disclosed FAILs to Matt.
**Target:** the r332 build. The final painting is `fid/pt/ph3/final/painting_ph3_r332_full.png`: file sha `901305202936`, pixels sha `b6ab4dfe8b03`. It equals `fid/pt/site/painting.png`†.
- PT: `e6d561114`, `942d43c04`, `f637928b2`.
- LV: `d26d14c55`, `9263d053d`.
- PH: `7d47a498d`, `a147d61bf`, `c580871cb`, `f7af6f5bc`, `fa84a7fbe`, `65a126d0d`, `75613df7e`.
- Ledger: R-C9-310..338 and M-C9-BV2F-SITE-BUILT.

**Developer:** drax (PT, LV) and galadriel (PH); the conductor is gandalf.
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (control before claim), #4 (charter and ledger as truth), #5 (severity matters).
**Governs:** charter § 6, § 12 W-1, § 15 and § 16; calibration §§ 50–58; my painting Gate-2 (`2026-10-09-bv2f-painting-gate2.md`) and pilot-4 Gate-2 (with its addenda).

**Method.** Every claim below was checked against the primary files, not the ledger. Numbers marked † are my own read-only probes. They are not binding; PH's readings bind. No Godot was run and no image was spent.
- I ran `verify.sh` (exit 0; 25 files) and `build_inputs_check.py` (OK: 223 files, 0 bad).
- `dev24.py` `8447a778c927`, `guided_paint.py` `dedb8d010414` and `guided_stitch.py` `94fa0d7b32b9` are unchanged since my last gate. No Tier-B commit has been made since `f6af5140a`.

---

## 1. Verdict, row by row

| Row | Reading (r332 unless noted) | Bar | Verdict | Checked against |
|---|---|---|---|---|
| P1 | 1.00 | ≤ 1.05 | **PASS** | `site_r332/p1.json` |
| P2 | 102/102 at `c4d4a48b2` | all | **PASS** | `site_r332/p2.json` |
| P3 | sea base-only 4.65; worst class char 13.05; RED 22.97 fails | ≤ 15.5 | **PASS** | `site_r332/p3*.json` |
| P4 snow (Phase 3′) | 3_3 / 4_3 / 4_4 FAIL. 3_0, 4_1, 4_2, 2_3 and 3_4 have insufficient support. | v1 bars; W_min 100 | **FAIL 3/6 judged (disclosed)** | `site_r332/p4.json` |
| P4 rock | all PASS; 4_0 has insufficient support | W_min 3 | **PASS** | same |
| P4 ice (LV `ice`) | 3_1: dE 7.37 | ≤ 9.40 | **PASS** | same |
| P5 a1 | **13/40** (derived § 51 domain plus the W-1 guard)† | 9.569 | **FAIL (disclosed)** | `site_r332/p5.json`, row by row |
| P5 2_2\3_3 corner | 2.223 (substituted; raw 15.449) | 4.809 | **PASS** | same |
| P5(b) | y = 3200 **0.902**; the other 7 seams ≤ 0.596 | ≤ 0.799 | **FAIL (disclosed)** | same |
| P6a | 64 candidates, 8 declared; 56 unmatched (48 open sea + 8 dark structure); 0 invented | 0 invented | **PASS** (record gap, C-3) | `site_r332/p6a*.json*`. My eye on `painting_2_4_c015`: open sea. |
| P8 | min 0.553; the 1 m-shift RED fails | ≥ 0.4476 | **PASS** | `site_r332/p8.json` |
| P9 sway / flow / trail | 5.47 / 8.548 / 1.000; the REDs fail | ≥ 2.064 / ≥ 2.064 / ≥ 0.99 | **PASS** | `site_r332/p9*.json` |
| P9c | v2 **0.267 FAIL-as-read** (§ 53). v3 main **0.030**, L5 0.025 | ≤ 0.25 | **PASS on v3** (§ 2 ratification; condition C-7) | `site_r332/p9c_v3*.json` |
| P10 | not run (T34 quiet window) | — | **OPEN** | — |
| P11 | **27/40**, catch 12/12 (valid), repeats 4/10 consistent | PASS iff ≤ 26/40 | **FAIL by one (valid; disclosed)** | key and answers rescored by me† |

**Why PASS-with-conditions and not PASS.** The build is what it claims to be, and it is pinned:
- painting sha = build painting;
- re-stitch = patch chain (0 px);
- identity proofs pass at every step;
- the build inputs check is green;
- Tier-B is untouched.

Every FAIL is measured and disclosed, and **nothing is masked** (§ 5). Four things stand between this record and an honest M3′ cover. None needs an image.
1. **The P11 cause sentence in the ledger is backwards** (§ 4, C-1).
2. **12 M3′ packet crops are stale** against r332 (C-2).
3. **The 56 P6a triage verdicts exist only as ledger counts** (C-3).
4. **Two items of binding PH evidence are uncommitted** (C-4).

**Why it is not FAIL or BLOCK.** No locked decision is crossed. No bar moved. Each instrument change (§ 2, § 3) was pre-registered before its reading and validated against a null and a RED. Whether the parity FAILs are accepted is **Matt's call at M3′**, as at M2″.

---

## 2. P9c v3: RATIFIED, with one operating-point condition

**Pre-registration integrity, verified.**
- § 56 and `site_p9c_v3.py` were committed at `65a126d0d` (17:08:15).
- The first v3 capture is stamped 17:08:54†. The validation JSON was written 17:19, before the reading JSON at 17:20.
- `site_p9c_v3.py` is byte-unchanged from the pre-registration to HEAD†. The § 56 text was only appended to (no deleted lines)†.
- The bar (≤ 0.25 px) and the statistic (median over samples with motion ≥ 0.25) are unchanged.

**The re-instrument is sound.** It removes the two defects § 55 identified:
- touching floes merged into one label;
- static ice and rock covering floe edges, which the silhouette does not move with.

The § 55 discriminator is the strongest evidence in the stack. The shipped bob and the attached-by-construction rigid null render image-identical (≤ 0.08 % of floe px), with per-floe Δr = 0.000. The validation then passes on both views:
- rigid null: 0.030 / 0.025;
- static: 0.000;
- RED: 0.743 / 0.843, which fail as required.

The v3 bobt rows equal the rigid rows value for value†, as the image identity predicts. **The v2 0.267 stays on record as FAIL-as-read. v3 binds from this ratification on.**

**Condition C-7: the operating point moved, and nothing says so.**
- v3 reads at the § 54 controlled times (t0 = 1.0 + 1.2k). Its counted samples move a median **0.75 px** (main) / 0.85 px (L5)†.
- The § 53 production capture moved a median **1.43 px** / 1.51 px†.
- For a proportional slip, the bar therefore bites at roughly **twice the slip fraction** under v3 (about 33 % vs 17 %).

This does not change today's verdict. The shader is pure translation, and § 55's image identity is amplitude-independent proof of attachment. But the row would be cited as a like-for-like PASS when it is not. **Either:**
- (a) run one v3 read on the production schedule (wall-clock TIME, as § 53), with the validation rule unchanged (0 images, one Godot session); **or**
- (b) the cover states the operating point beside the PASS.

The conductor chooses.

## 3. PH's W-1 add-only guard and the derived § 51 domain: RATIFIED

- **Derived domain.** `site_domain.py` and `s52_domain.json` were committed in the pre-registration commit `7d47a498d`, before any value. They resolve all 18 strips that meet the mask, with 0 unresolved. **This is the #76 forward fix my painting gate asked for.**
  - Its result names 3 vertical joins that § 51's enumerated list missed (0_3|1_3, 1_3|2_3, 2_3|3_3), as well as 3_2/3_3.
  - It shows 2_2|3_2 OFF (3_2-r1 was staged raw).
- **The guard is the correct form of W-1.** The joins new to the domain had raw readings that were ruled before the derivation. The guard binds max(raw, substituted) on those joins only, and the § 51-named joins keep their pre-registered substituted reading. Re-scored by me†:
  - its only effect is **3_2/3_3** (raw 14.934, substituted 4.271), which stays FAIL;
  - 0_3|1_3 fails on both readings, and 1_3|2_3 and 2_3|3_3 pass on both.
- **13/40 reproduced**†: 3 pilot-internal + 10 Phase 3′, the same membership as my painting gate. The DEV-29 real-mask self-test passes on all 7 substituted older canvases.
- **Disclose beside it (INFO).** Plain raw a1 is **15/40**. The two § 51-named joins 0_2/0_3 (raw 21.457) and 2_2/2_3 (raw 29.288) pass only through the § 51 substitution. That substitution was pre-registered before they were read, so it is legitimate. Matt should still see both numbers.

## 4. P11 27/40 (valid, FAIL by one) and no rebuild for r332: RULED, with one record correction

**The score stands.**
- I re-scored the committed key against the answers: scored 27/40, catch 12/12, snow 24/34, heather 3/6†.
- Under chance, P(≥ 27/40) = 0.019†, so this is real discrimination, one trial over the bar. No bar move.
- **Disclose:** repeat consistency was **4/10**, against 8/10 on both calibration sets (§ 39). That is diagnostic only, but the judge was unusually unstable on this set.

**The decision not to rebuild P11 for r332 is upheld, on two independent grounds.**
1. Pre-registration. The r332 change is 57,220 px, all class tide_ice (my diff: 57,220 px, bbox (3535, 3117)–(3826, 3450), 0 px in the pilot)†. § 52 (b) maps tide_ice to EXCLUDED.
2. Footprint. I mapped every site crop in the key (62 trials × A/B/X) to plate px through `stills_views.json` (the still is 1:1 with the plate per § 50 (a)). **0 crops intersect the r332 patch**†.

The stills were captured on r328 at 16:05 and are phase-accepted 24/24 (`p11_phase.json`).

**C-1 [WARN]: R-C9-334's cause sentence is inverted (#87).**
- The ledger says the judge's cue ("crisp warm peach with outlined lavender cells vs softer, cooler cells") **"matches PH's snow forensic (soft draws propagated…)"**. The answers say the opposite.
- Every confident call names the **site** as the *crisp, warm, outlined* build and **v1** as the *soft, cooler, mottled* one. For example:
  - trials 08/16/22/23/27/31/36/38/47/52 (X = site): "matching the crisp build";
  - trials 01/04/19/32/33/50/57/59/61 (X = v1): "matching the soft build".
- The cue holds on the clean `pc_stills` v1 crops too, not only the window-capture v1ref ones†.
- The forensic finds the painted snow in 3_3-r1 / 4_3 / 4_4 **softer** than v1 (a fine-grain deficit). **The direction does not match.**
- **Correct the ledger before the cover. State the cue as read, and leave the cause OPEN.** It is not the soft-draw chain. Candidates: site-wide cell-outline crispness or warmth, painting-side vs render-side. The locate-the-cue forensic I asked for at pilot 4 (same plate px in the painting and in the still) is the 0-image discriminator, and it is optional before M3′.
- This is the second time in this run that a conductor cause sentence has been written ahead of its data (cf. R-C9-310 (e)).

## 5. The DEV stack since my last gate: masking and re-verification

**DEV-24 layers 6–24** (sea pass L6–15, r328 round L16–23, ledge grain L24). LR4 images: **43/45**.
- **Scale (state it at M3′):**
  - the layers 6–24 change **6.29 M px = 23.1 % of the site**† (L5–24 union 23.2 %†);
  - with layers 1–4 (≈ 2.8 M layer-sum, pilot) the DEV-24 share is **≤ ≈ 33 % of the shipped painting**;
  - in the pilot identity zone (x < 3840, y < 2304), **594,721 px (6.7 %)** changed after the reviewed `8e169e6331bb`† (PT's layer-sum: 705,828 + 442,378).
- **Tone rings at patch edges: none found.** Probe†: same-class boundary px of the L6–24 region, n = 34,206. Smoothed-luminance gradient, new vs old at the same px:
  - p50 0.96 / 0.96; p90 5.72 / 5.66;
  - excess p90 1.45, shore_ice 0.17, sea 0.33.
  - The only concentrated excess is snow and rock inside the Matt-noted cave zones, where the content itself changed.
  - The R-C9-322 fade-field refinement holds, with no Tier-B change (the shas above).
- **"Land done": verified by the class maps, not by the paste masks.** The identity proofs' "0 px outside the paste mask" is circular as a *land* proof: it shows the paste stayed in its mask, not that the mask avoided land.
  - My check†: **543,774 changed px are land in both** the `023686e3c` and `d26d14c55` class maps.
  - Of those, 141,857 lie outside the pilot allowlist rects, and **all of them lie inside the r328 plan's declared `LAND_ZONES`**: the Matt-noted cave brow, the east wall and the icy ledge (R-C9-325/329/332). **0 px fall outside both.** No undeclared land change.
- **Matt-eye notes (INFO):**
  - the sunlit snow tongue at the ledge lip stays smoother (R-C9-337; 2 images remain);
  - one heather tuft at about plate (3615, 2105) is ghosted or doubled on the cave_brow mask edge (1:1 only; my crop);
  - the cave mouth reads as a clean arch, the stair and the ledge are continuous, and the black rectangle is gone (my 1:1 crop of x 3100–4100, y 2300–3300).
- **Parity coverage (INFO).** Water and ice are excluded from P4 snow/rock and P11 by pre-registration. So the sea pass (about 21 % of the site) is judged by **P3 sea, P6a triage, P9/P9c and Matt's eye only**. Say so on the cover.

**R-C9-324 / R-C9-326 projected-paint rules: correct, and complete for this build.** These are BV2F-PT code in `bv2f_pilot.gd` `_dress_painted`, which is OWN, not Tier-B.
- The logs read `uvless meshes projected: 1` and `procedural posts projected: 49`.
- The new UV-overlap check in `pt_export_meshes.gd` flags **49 of 100 exported models, exactly the 49 palisade posts** (uv_area_sum 1.551). **No other model exceeds 1.0**†, so no other bake carries the posts' defect.
- The proofs are committed: `post_proof_longhall.jpg`, `panel_proof_longhall.jpg` and `post_panel_proof_r330.jpg`.
- These rules change what ships, so they go on Matt's line (§ 6).

**DEV-5 shared material (R-C9-317).**
- The A/B showed 8/12 identical and 4/12 within noise.
- § 55 shows the shipped bob path image-identical to the attached null.
- PT's P9c A/B (0.161 vs 0.207) agrees. No concern.

**Cleanup manifests M22–M24.**
- I intersected every manifest path with the 223 build-input paths: **0 hits**†.
- **Two record defects [WARN]:**
  1. **Authority.** Charter § 6 (disk row) and § 10 still say **"Matt runs deletions."** M22 records a "PROCESS CHANGE (Matt)" with **no verbatim**. A conductor's account of Matt's direction is not on the record as Matt's words, and the charter was not amended. Matt confirms it by name at M3′, the verbatim (or Matt's restatement) goes in the ledger, and § 6/§ 10 are amended. Until then the M23 and M24 executions rest on an unrecorded authorization.
  2. **Evidence of record deleted (#73).** M24 removed `film/_r330_mere_route/…mp4`, which is **the film Matt watched for his R-C9-332 verdict** (sha `670b2b2ffe19`, cited by M-C9-BV2F-SITE-BUILT). The verdict's evidence no longer resolves, and no ledger row records that.
     - Disposition: a one-line ledger note. The r332 film (`4b6a1b65241a`) is now the film of record.
     - Forward rule: a cleanup manifest also excludes any file whose sha a ledger row cites as evidence, unless the deleting note says so.

**Pilot allowlist expansions R-C9-314..330: sound.**
- The `allow_330` byte check covers the full chain 023686e3c → bac035332 → 44d657e24 → d26d14c55. Guide 321,242 / class 104,168 / ids 98,742 changed, **0 outside**. The allowlist is 18.71 % of the pilot.
- Every land exception is Matt-noted except one. The conductor accepted the **waterline rect** (R-C9-321) as "necessary to the Matt-noted sea fix… disclosed to Matt". Disclosed is not ratified (§ 6).
- LV's ice proof passes: zero stacking, self-crossing and ring checks with fail-first, walk 8/8. The bounds spike is removed (`9263d053d`), and the direct wreck-to-circle walk passes.

**Re-verify: nothing further owed for the build itself.** P-4 reproduces as an identity chain at every step: r332 vs r328 changes 57,220 px, with 0 outside the patch mask and 0 pilot px outside the allowlist. The shipped file equals the build's painting.

## 6. What Matt must ratify by name at M3′ (ADR-002 ESCALATE)

1. **DEV-29** (context patch), carried from the painting gate.
2. **The DEV-24 `read_zone` / pinned-correction re-base**, now including the per-patch pinned **fade field** used by the sea pass (R-C9-322).
3. **The DEV-24 extension.** It consists of:
   - the sea-pass tranche of 20 images and the LR4 cap 45 (R-C9-317/327/332);
   - **the conductor's exemption of Matt-noted patches from the DEV-13 seam cap**;
   - the resulting share: **≤ ≈ 33 % of the painting is DEV-24 paint** (23.2 % from L5–24).
4. **The projected-paint rule** (R-C9-324/326): UV-less meshes and procedural posts wear the projected painting. That is 1 + 49 objects.
5. **The changes to the M2″-ratified pilot**:
   - 594,721 identity-zone px;
   - the land exceptions: spar, beach reveal (261 px), waterline, drift, stones and cave_top.
   - The **waterline** rect is the one exception that was not Matt-noted.
6. **The conductor-executed deletions** (M22–M24 process change), plus the charter amendment.
7. **Acceptance of the FAIL rows as stated** (§ 7).

**Not on Matt's line** (QA ratified here): P9c v3; the W-1 guard and the derived domain; the P11 no-rebuild.

## 7. M3′ cover disclosures (counts)

- **P5 a1: 13/40 FAIL (binding)**: 3 pilot-internal + 10 Phase 3′. **Plain raw 15/40.** 3_2/3_3 is held by the W-1 guard.
  - Corner 2_2\3_3 PASS 2.223.
  - Report-only: 7 `\` corners over 4.809, and 4 anti-diagonals above v1's maximum of 6.50.
- **P5(b): 1 of 8 seams FAIL**: y = 3200 at 0.902 against 0.799, a grain band with no line by eye.
- **P4 snow:**
  - Phase 3′: **3/6 judged FAIL** (3_3, 4_3, 4_4), and 5 chunks have insufficient support.
  - Site: **7/15 judged FAIL** (pilot 4/9).
  - Rock PASS (1 insufficient). Ice PASS (1 chunk).
- **P11: 27/40 FAIL by one** (valid: catch 12/12; repeats 4/10). Cue: **site snow reads crisper and warmer than v1. Cause open** (C-1).
- **P9c:** v2 0.267 FAIL-as-read; **v3 0.030 PASS** (L5 0.025), with the operating-point note (C-7).
- **P6a:** 64 candidates = 8 declared + 48 open sea + 8 dark structure; **0 invented**.
- **PASS:** P1, P2, P3, P8, P9. **P10 not run.**
- **DEV-24:**
  - LR4 43/45 images;
  - L5–24 = 23.2 % of the site (≤ ≈ 33 % with L1–4);
  - pilot identity zone: 594,721 px changed;
  - land changed: 543,774 px, all inside declared rects or zones.
- **Images:** BV2F **208** (~250 guard): PH3 43, LR4 43.
- **For Matt's eye:**
  - the smoother snow tongue;
  - the ghosted tuft at (3615, 2105);
  - the sea pass is outside the binding parity rows;
  - the deleted r330 film.

## 8. Before the arena work (R-C9-318) and before a P10 run (T34)

**Arena.** Per R-C9-318, implementation follows Matt's walk at M3′.
- **A-1.** M3′ is ratified (§ 6) **before** any spawn or entrance work starts.
- **A-2.** No arena change touches guide, class or ids. If one must, it goes through the pins, the allowlist, the identity proof and a "land done" ruling, exactly as the sea pass did.
- **A-3.** LV runs a walk check for each of the six spawn approaches before placement:
  - the sea cave's iced ledge → stair, with the 22 icicles clear of the route;
  - the wreck beach, newly connected (`9263d053d`).
- **A-4.** The DV entrance VFX are re-judged over the new paint.
- **A-5.** The pack-anchor mapping goes to the Sim Session. C-9 writes no KC2/JOIN-1 records.

**P10.**
- **P-1.** T34 (host quiescence) is Matt's.
- **P-2.** The § 50 (c) loops were proven on **rp4, not site_ph3**, and the bounds have since changed. PH re-proves the start and sea loops on site_ph3 under the walk-validity rule and **pre-registers them before the window**. The sea loop should now include bobbing floes in frame (39).
- **P-3.** Same interleave and VOID rules as § 34 / § 50 (c). No bar moves.

## 9. DELTA: R-C9-339 (the icy ledge repainted as high-tide ice with kelp)

**Scope of this gate.** R-C9-339 arrived mid-review: Matt's verbatim, *"Only 25% of the snow issue below the sea cave got fixed…"*. Everything above gates **the rest of the build** and stands. The M3′ candidate becomes **the r339 build** once the delta below passes. This ledge goes in as a **delta Gate-2** (jack-ryan), not a new full gate.

**Record note (INFO).** Matt's "only 25 % fixed" is his read of R-C9-337's ledge_grain-1. The conductor had accepted that patch, noting a smoother sunlit tongue "for Matt's eye". The r332 film is therefore not the film of record either. The r339 clip replaces it.

**What PH must re-run.** It is the § 57 pattern: pre-register before any r339 value (§ 59), with every rule unchanged.
- **Whole-site, painting-dependent rows:** P1, P2, P3 (a fresh `ph_p3_sea.gd` capture), P4, P5(b), P6a, P8 and P9 (sway, flow, trail).
- **a1 does not move.** The raw canvases are untouched; prove it with identical values.
- **P9c is not re-run** unless prep rewrites floe data. PT states which.
- **P4:** the ledge is tide_ice, which is **report-only**. Matt's "like the mere ice" does **not** promote it into the binding `ice` domain after the fact (W-1). Its report-only dE will move; report it.
- **P6a: pre-register now that dark kelp clumps on ice are an expected false-positive mode** (dark blobs at T 32). tide_ice is a water class, so every kelp candidate gets a **per-candidate triage row plus a crop**, never auto-passed (and C-3 applies to these rows too).
- **P11:** it stands on the same two grounds as § 4, **only if** PH re-runs the footprint check against the r339 changed-px mask (not the r332 bbox): 0 site crops intersecting, and the changed px all tide_ice. Any intersection is the conductor's call, recorded before any re-judge.

**What I want to see for the delta.** All of it costs 0 additional images beyond R-C9-339's canvas.
1. **The paste mask declared before firing.** It is tide_ice ∩ the ledge rect.
   - **State whether the cave-mouth floor is inside it.** R-C9-339 says the cave-mouth floor "reads the same so the two join". If the floor is outside the mask, the junction is a **same-class paste edge**, which is exactly where a seam would show.
2. **The identity proof r339 vs r332**, which must show all of:
   - re-stitch = chain, 0 px;
   - changed px ⊆ paste mask;
   - **the changed px's class histogram = tide_ice only**, from the pinned `d26d14c55` class map;
   - 0 pilot px;
   - guide, class and ids **sha-identical** to the `d26d14c55` pins (paint-only: no blockout change, so walk 8/8 carries).
3. **A 1:1 before/after of the ledge**, plus the junctions with the cave-mouth floor, the stair foot and the lip icicles. My § 5 boundary-gradient probe re-run on the delta's edge is enough; PT may cite mine.
4. **Images.** LR4 ≤ 48 (cap per R-C9-339); BV2F stays under the ~250 guard.
5. `build_inputs_manifest` refreshed and the check green.
6. A ledge still plus clip for Matt, with its sha recorded in the ledger as the new evidence of record (C-6).

**Sequencing.**
- **C-2's re-crops wait for r339.** Packet crop 18, at (2718, 2993), and any crop near the ledge would otherwise go stale twice.
- The § 7 cover counts (images, DEV-24 share, land px, pilot px) are re-stated on r339.

## Conditions (all 0 images; before the M3′ packet goes to Matt)

- **C-1 (conductor).** Correct R-C9-334's cause sentence (§ 4).
- **C-2 (PT/PH).** Re-crop the packet from r332. Stale against L6–24†:
  - J08 (0.12 changed), J09 (0.11), J10 (0.32), J11 (0.12), J12 (0.32);
  - eye/P6a crops 12 (1.00), 13, 14 (0.72), 15 (0.72), 17 (1.00), 18 and 19 (0.83).
  - PH's `site_r332/p5_crops/` (23, from r332) serve for the joins (#75 cl. 1).
- **C-3 (conductor/PH).** Write the 56 per-candidate triage verdict rows. Both `p6a_triage.jsonl` files still read PENDING, and the reads exist only as R-C9-333 counts. This is my H-2 again.
- **C-4 (PH).** Commit the binding evidence:
  - `p11/answers/abx3_site_v1_vs_site_judge.json` (untracked; the 27/40 rests on it);
  - the `v3` case in `harness/run_site_godot.sh` (uncommitted; it produced every § 58 capture).
- **C-5 (conductor).** **Charter § 16, second fold.** The last fold was at R-C9-310, and nothing since is in it:
  - layers 6–24, the tranche and caps, the DEV-13 exemption;
  - R-C9-324/326 and the UV check;
  - DEV-5 shared material;
  - P9c v3 and the W-1 guard;
  - the cleanup process change;
  - plus the § 6 ratification line.
- **C-6 (conductor).** The ledger note for the deleted film of record, and the forward exclusion rule (§ 5).
- **C-7 (PH/conductor).** The P9c operating point: confirm read **or** cover note (§ 2).
- **C-8 (PT/PH, then jack-ryan).** The R-C9-339 ledge delta (§ 9): the declared mask, the identity proof with its class histogram, the § 59 pre-registration and re-run, kelp triage rows and the P11 footprint check. Then a **delta Gate-2** before the packet.

## Action

- [ ] **Conductor (gandalf):** the ledger row for this finding; C-1, C-3 (verdicts), C-5, C-6; choose C-7 (a) or (b).
- [ ] **PT (drax):** C-2 eye/P6a re-crops from r332.
- [ ] **PH (galadriel):** C-4; C-3 rows; C-7 (a) if chosen; P-2 before any P10 window.
- [ ] **LV (drax):** A-3 before any arena placement.
- [ ] **Matt (ESCALATE, at M3′):** the § 6 ratification line; accept or refuse the § 7 FAIL rows; confirm the deletion process by name; T34.

## References

- **Ledger:** `astra_test_01/burst/runs/C-9/ledger.json`: R-C9-310..338, M-C9-BV2F-SITE-BUILT, N-C9-CLEANUP-M20..M24, `bursts[].image_calls`.
- **Charter:** `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md`, § 6 (disk row), § 10, § 16.
- **Calibration:** `…/barrow_v2/fid/ph/calibration.md` §§ 39, 50–58.
- **PH** (all under `…/barrow_v2/fid/ph/`):
  - `results/site/{s52_domain, p5, p9c, p9c_null, p11_phase, p11_set_shas, snow_forensic}.json`;
  - `results/site_r332/{p1, p2, p3, p3_sea, p4, p5, p6a, p6a_triage, p8, p9, p9c_v3_validation, p9c_v3}.json*`;
  - `harness/{site_domain, site_p5, site_p9c_v3, run_site_godot.sh}`;
  - `p11/keys/abx3_site_v1_vs_site.json` and `p11/answers/abx3_site_v1_vs_site_judge.json`.
- **PT** (all under `…/barrow_v2/fid/pt/`):
  - `ph3/final/{painting_ph3_full, painting_ph3_sea_full, painting_ph3_r328_full, painting_ph3_r332_full, painting_pre_l5}.png` and `build_inputs_manifest.json`;
  - `ph3/sea/{plan, identity_proof}.json` and `ph3/sea_r328/{plan, identity_proof, identity_proof_r332}.json`;
  - `ph3/allow_330.json` and `ph3/class_art_pinned_{023686e3c,d26d14c55}.png`;
  - `site/{stills_views.json, stills/phase_check.json, work/export.log, root/work/meshes/*.json, film/, *proof*.jpg}`;
  - `RESUME_PT.md`.
- **Code:** `…/barrow_full/godot/scripts/bv2f/bv2f_pilot.gd` and `…/godot/tools/bv2f/pt_export_meshes.gd` (`e468e5362`, `b8641876d`).
- **LV:** `…/fid/RESUME_LV.md` (R-C9-314..331) and `lv/art/pilot_allowlist_319.json`.
- **Frozen toolchain:** `fid/v1tools/{verify.sh, SHA256SUMS}`.
- **Cleanup:** `astra_test_01/burst/runs/C-9/cleanup/manifest_bv2f_scratch_{22,23,24}.txt`.
- **Disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #73, #75, #76, #87.
