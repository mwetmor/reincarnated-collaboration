# SB-1 — R-CPB-17b EYEBALL PACKET (Matt's two-gate ruling)

**Assembled by gandalf (`RUN-CONDUCTOR`), 2026-08-14.** All paths relative to `~/Games/reincarnated-collaboration/`. Every image byte is class-E (on disk, untracked, sha-bridged from tracked text).

> **⚠ CORRECTED SAME DAY (ledger WW-3) — Matt's pointer overrides §§ 1–4 below.** The ratified reference is **`~/Games/reincarnated-godot/tmp/br2watch/BR2W.mp4`** (the BR-2 watch: seed 74000909, 1600×900, 1211 frames / 40.37 s, sha `ea61b0ee…`; `BR2W_C9.mp4` byte-identical), **NOT exhibit E2.** Its camera is READ from the BR-2 run logs + `m6/pl_audit.json` (four laps identical, anchor error < 0.0009 frac) and it is **THE GD GAME CAMERA** — `player_lock`: **pitch 52.9535° · fov_v 31.7861° (vertical) · yaw 47.0° · cam−player offset (14.7262, 28.3970, 13.7826) m = stand-off 34.831 m · anchor (0.50104, 0.55093) · player-locked** — the GAL-CAM gd-parity operands verbatim. Consequences: **E2 demotes** to camera-adjacent exhibit (its fov-24 lens never matched the reference: 24 vs 31.79, pitch 50 vs 52.95); the **§ 4 candidate-boom table is STRUCK** (boom-scaling under the wrong fov is moot); the fork resolves toward **architecture (A) instantiated at the GD camera**; **gate 1 becomes: arena re-rendered under `player_lock`, judged beside BR2W.** In flight: drax ports `player_lock` into the arena harness (camera the ONLY variable — the scale-1.95 over-read this predicts is exactly § 4(A)'s named body-scale follow-up, surfacing on schedule) · galadriel measures BR2W's own subject register from the sha-gated mp4. Full lineage: ledger row WW-3.

---

## 0. What you are ruling, and in what order (your own gate, R-CPB-17b)

> *"I have never eyeballed this fixed boom ≈ 72.9 m, so we won't want to check it off as canon until I can eyeball the werewolf and EOR warlord to ensure the zoom/angle looks the same."*

**Gate 1 — CAMERA-MATCH:** does the arena clip's zoom/angle read as the same camera language as the werewolf frame you ratified and the EOR warlord?
**Gate 2 — ARTICLE FEEL** (only after gate 1): density feel, palette knee, cadence read, FX draw — the R-CPB-17(d) binding ratifications, judged on the promoted clip.

**No canon stamp until gate 1 passes your eye. Whatever register your eye picks, the fix stays one constant.**

---

## 1. The provenance correction you should read first (ledger WW-1)

The werewolf you ratified was **never rendered at 72.857 m**. It was never in the WR1 level at all (four tier+kit rooms, no occupants — git history confirms nothing was removed). The ratified look lives in `vh_race_rig` at a fixed **34.0 m** — within 0.9 m of Grim Dawn's own measured camera depth (**34.82 m**), which is very plausibly *why* your eye read "matches Grim Dawn."

The 72.857 m canon boom = the WR1 room-law output (34.0 × 37.5/17.5) — **derived from the same-angular-size law you struck**, mis-attributed by the conductor via a label collision (`run_wr1.sh` is the vh rig's harness; "the wr1 werewolf frame" never meant the wr1 level rig). **What survives clean:** the lens — yaw 47 / pitch −50 / fov 24 are byte-identical across both rigs; your "zoom/angle" ratification of the *lens* carries. The **distance** is the open variable, exactly what this packet puts in front of your eye.

---

## 2. The exhibits

| # | What | Path | Integrity |
|---|---|---|---|
| E1 | **THE WATCH** — arena clip @ 72.857 m boom (320 A-stationary · 18 dip · 320 B-undulating, 21.9 s) | `agentic_orchestration/galadriel/captures/2026-08-13-sb1-a2gr-lookdist/a2gr-lookdist-cadence-ab.mp4` | sha256 `017aebf4bb92cfff…d1ec16` · manifest + fg10-digests tracked in same dir |
| E2 | **Ratified werewolf frame** — vh rig @ 34.0 m, fresh render, bit-identical ×2 | `agentic_orchestration/galadriel/captures/2026-08-14-sb1-werewolf-recap/frames/wwrecap-vhaura-p1.png` | sha256 `35fd577a…8b11cc` · receipt tracked in same dir |
| E3 | **Arena still** (frame n=160, A-phase) for direct side-by-side with E2 | `agentic_orchestration/galadriel/captures/2026-08-14-sb1-register-measure/arena-n160.png` | sha256 `115fd99a…4b0f51` |
| E4 | **GD ground truth** — your own 1 h 54 m playtest corpus: plates, gd/ vs ours/ | `agentic_orchestration/galadriel/captures/2026-07-31-gd-parity/` (`plates/PLATE_gd_parity_player.png` first) | `gd-parity-numbers.json` tracked |
| E5 | **EOR warlord stills** — the felt weight reference | `agentic_orchestration/galadriel/captures/2026-08-07-eor-sittings/` + `2026-08-08-eor-followup/evidence/` | per-dir receipts |
| E6 | **A2g diagnostic** — the struck-law frame @ 168.863 m (what "ludicrous" looked like) | `agentic_orchestration/galadriel/captures/2026-08-13-sb1-a2g-canon/` | per-dir manifest |
| E7 | **Register measurement of record** — one method, all subjects | `agentic_orchestration/galadriel/captures/2026-08-14-sb1-register-measure/register-numbers.json` + `receipt.txt` | tracked |

**Suggested viewing:** E2 beside E3 (the camera-match core) → E4 plate (GD anchor) → E1 full clip → E5/E6 as calibration extremes.

---

## 3. The measured register table (ONE method — galadriel seg-bracket, gd-parity convention)

| Subject | Camera | h_frac (tight) | vs GD werewolf | Position human→werewolf |
|---|---|---|---|---|
| GD human form | GD's own (34.82 m depth) | **7.04 %** (n=1, MEDIUM conf) | 0.48× | 0 % |
| **Ratified werewolf (E2)** | vh rig @ **34.0 m** | **9.44 %** (generous 11.67 % w/ aura plume) | 0.64× | 31 % |
| **Arena fighter (E1/E3)** | canon pin @ **72.857 m** | **12.96 %** (generous 21.67 % w/ upper element) | 0.88× | 77 % |
| GD werewolf form | GD's own | **14.77 %** (median, n=4) | 1.00× | 100 % |
| GD boss tier | GD's own | **21.57 %** (COARSE — do not tune to it) | 1.46× | — |
| Arena @ struck law (E6) | 168.863 m | 5.59 % (harness diagnostic) | 0.38× | — |

Arena number is **double-sourced**: harness geometry 12.990 % vs galadriel independent bracket 12.963 % — agreement within 0.3 px, box not tuned.

**THE CONFOUND, stated plainly (galadriel's words carry):** h_frac conflates camera framing with body size, and these are different bodies (werewolf 1.8 m; arena fighter world-scale 1.95 — a much taller mass). The 1.37× gap between E2 and E3 does **not** by itself prove the cameras differ. The table informs; your eye rules.

---

## 4. The register question, properly decomposed

Grim Dawn's own law — measured from your corpus — is **FIXED CAMERA, BODIES VARY**: one camera, and human/werewolf/boss read 7 / 15 / 22 %. Size is threat language. Diablo (2/3/4 alike) runs the same law. Two coherent architectures for our canon:

**(A) Camera-constant (the GD/D3 law).** Pin ONE boom for all content; presence differences carry meaning. The frame you already ratified (E2) *is* this law at GD's own depth (34.0 ≈ 34.82 m). Consequence to know before choosing: at ~34 m the arena's scale-1.95 subject would read far above 12.96 % — boss-class presence. The 1.95 inflation plausibly originated as compensation for the old too-far struck law (168.863 m); under a near camera the compensation over-corrects. **Choosing (A) opens a body-scale follow-up in drax's seam — two knobs were layered; un-layer them.**

**(B) Presence-constant.** Tune the boom per content to hold subject presence at a chosen register (the current 72.857 pin holds *this* subject at 12.96 %). Flattens the size language the genre anchors use deliberately: the boss that fills the frame stops being a beat.

Same-subject distance scalings from the measured arena register (legitimate lens geometry for the SAME body; any chosen value gets a verification render before pinning — no number is canon from a desk):

| If the arena subject should read… | Boom ≈ |
|---|---|
| 12.96 % (current) | **72.857 m** (pinned, live-rig-confirmed) |
| 9.44 % (= your ratified werewolf frame's register) | **≈ 100.0 m** |
| 7.04 % (= GD human register) | **≈ 134 m** |
| 14.77 % (= GD werewolf register) | **≈ 64 m** |

**Conductor lean, veto-open:** architecture **(A)** — fixed camera at/near the ratified 34 m register with honest body scales. It is the law both genre anchors run; it is the frame your eye already ratified once; and in the isekai power-fantasy grammar, the moment a demigod-class body *fills the frame* is a beat presence-normalization can never buy back. But (A) couples to the scale-1.95 strike, which is exactly why this is your gate and not my pin.

---

## 5. Gate-2 caveats, named so they cannot ambush

1. **The floor is a placeholder.** Tiled diamond floor dominates at telephoto. Judge zoom/angle at gate 1, not the linoleum.
2. **The whirlwind reads rotor-like at register.** Galadriel (declared, not adjudicated): the arena subject at n160 "reads as a large wheel/rim + radial-spoke mass," not an unambiguous humanoid; a second instance sits top-right. In D3, whirlwind keeps the barbarian's silhouette with the blur additive; if our body dissolves into its FX at canon distance, that is a readability finding for drax's seam — flag it if your eye agrees, but it does not gate the camera call.
3. **The 18-frame dip is designed black** (seam max-luma 16.0 vs picture 102.27) — it is the A/B splice, not a defect.
4. **Determinism honesty:** the clip ships with no fix claimed — the 2026-08-13 red was never reproduced in 31 instrumented draws; 100 % of observed variance is confined to discarded preroll (deepest 23/60), watched by a standing diagnostic. The manifest carries the full ancestry.

---

*Packet complete. Ledger rows CLK-2-3 · WW-1 · WW-2 carry the full lineage. Ruling interface: your gate-1 verdict + (if gate 1 passes at some register) gate-2 ratifications land as R-CPB-18 in the run ledger, veto-open as always.*
