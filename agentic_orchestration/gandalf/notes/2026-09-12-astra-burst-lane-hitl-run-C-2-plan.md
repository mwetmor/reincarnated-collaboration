# Astra burst lane — HITL Run C-2 plan (intent-first loops under oracle gates)

> **STATUS:** v0.2 READY — gandalf (RUN-CONDUCTOR), 2026-09-12. Phase-1 build lane COMPLETE (T1a-idle/-2, T1a-ann-13L, T1a-walk-3, T1b, T1c); tree re-frozen (MANIFEST 9146d9811620), SYNC 10/10. P1–P2 satisfied; P3–P6 at launch. Supersedes the C-1 plan's K3 section. Governing rulings: R-21 (intent over consistency), R-22 (Muybridge oracle), R-23 (H1 register; ARPG-language screen; 17 %), R-24 (Phase-1 GO, push as you go), R-25/26/27 (instrument method), Q76 (X-video probe evidence). Charter: `2026-09-11-astra-burst-lane-run-charter.md` §§ 1–12.

## 0. Goal (leave the session with)
1. The lane **re-frozen in H1** (register card, bible style card, probe set, MANIFEST + SYNC).
2. **Bands committed** by Matt (idle relaxed/combat, walk) — pre-registered before any C-2 loop is measured against them.
3. An **H1 starter master** (woman) approved; the **H1 advanced master** (man) approved with a motif template.
4. **Idle-S and a 12-frame walk-E** minted against the dope sheet + pose guides, measured by the same instrument that measured the oracles, shown beside the oracle video — and **ruled** (pass / fail-with-numbers). L5 closed either way.
5. The **X-video path ruled**: in-betweener (adopted with rules) · instrument only · dropped.
6. A GO/NO-GO word on the **project-wide register pivot** gate (`00-system.md`: one loop + one plate) — or the named evidence still missing.

## 1. Pre-conditions (conductor, before Matt sits down)
| # | condition | check |
|---|---|---|
| P1 | T1c DELIVERED; suite green except the named standing reds (4 × T0-d3, 1 × walk grid-parity) | `tests/run_t0c.py` counts |
| P2 | MANIFEST re-frozen over the T1 tree; `00-system.md § 7` SYNC re-stamped; `lane/check_sync.py` 10/10 | `shasum -c MANIFEST.sha256` from `astra_test_01/burst` |
| P3 | Checkpoint packet on the Desktop: `12 T1 checkpoint` + walk curves (annotation path) + X-video probe (`13`) | files present |
| P4 | Ruling sheet (§ 3) printed at the top of the session — one recommendation per fork | this doc |
| P5 | Image budget reserved: ≤ 60 images for C-2 (cap 250; 66 used) | ledger |
| P6 | Serial law: no TOOLING burst during C-2 except the re-freeze; GENERATE waves of 4 | R-13 |

## 2. Session steps (Matt present from step 2)
| step | what | burst(s) | Matt |
|---|---|---|---|
| 1 | Conductor: session-start, SYNC verify, ledger open, ruling sheet | — | — |
| 2 | **Rulings** (§ 3), one word each; bands → `committed: true` + sha256 into the bible | — | rules |
| 3 | **Re-freeze in H1**: register card + bible `style` sentence = the H1 sentence (R-23); re-freeze; SYNC | T-freeze (TOOLING, serial) | witnesses |
| 4 | **K1′ starter master in H1**: v5 identity text, H1 register, 3 candidates → CHECK → JUDGE (mirrored control) → PACK | K1′-gen-01, chk, jdg, pack (4 imgs) | picks 1 |
| 5 | **Advanced master motif template**: the ring-with-hour-mark drawn as a template (T0 sigil_template route); man re-minted once with the template as a reference if the glyph drifts | K1′-adv-01 (2 imgs) | approves |
| 6 | **K3′ idle-S (relaxed, 16 f @ 8 fps)**: seed = the H1 master on the 512 canvas; dope sheet `dope_idle_relaxed_16.txt` as prompt text; composite mechanism (T0-e) frame by frame; `idle_intent` + G11/G12 + G6b; comparison view vs the Hades combat curves (relaxed band pending a larger source) | K3′-gen-idle (wave of 4 × 4 f), reg, chk, cmp, pack (16 imgs) | reviews curves + loop |
| 7 | **K3′ walk-E (12 f @ 12 fps)**: pose guides `walk_00..11.png` as the layout reference per frame; `dope_walk_12.txt` phase text; sole-aligned registration; `gait_intent` (W-1…W-6), G6c; comparison view vs Muybridge plate 13 (annotation curves) | K3′-gen-walk (3 waves of 4), reg, chk, cmp, pack (12–24 imgs) | reviews + rules L5 |
| 8 | **X-video comparison** (Q76): from the H1 master still → idle (prompt C amplitude-banded) + walk clip; frames 0–4.3 s only; resample; the SAME gates; side by side with K3′ | conductor (Grok CLI), CHECK bursts | rules the path |
| 9 | **Composite proof + gear layer** (Q75 primitive): re-skin 4 idle frames (skin/hair) with pose locked; G12 ≥ 0.99 | K5′-comp (4 imgs) | sees it |
| 10 | **One plate under T3 motif constraints** + per-scene light grade note (H1, ARPG-language, 17 % anchor) | T3 (TOOLING) + K6′-plate (2 imgs) | approves or names the gap |
| 11 | Close: ledger, milestones, handoff, push; project-pivot gate statement | — | GO/NO-GO word |

## 3. Ruling sheet — one recommendation per fork
| fork | recommendation | alternatives |
|---|---|---|
| R-a walk target amplitude (k_vert) | **k_vert = 1.25 → target ≈ 4.9 %H** (Legolas target band 2.5–5, ceiling 7; Muybridge floor 3.95) | 2.0 (7.9 %H, above ceiling) · 1.0 (photographic) |
| R-b combat-idle band | **commit the Hades combat row** (breath 6.5 / head 5.5 %H → floor 0.6×, ceiling 1.5×) with region lists from T1b's displacement classification, not the collapsed energy list | wait for a second source |
| R-c relaxed-idle band | **provisional = 0.5 × combat** (breath ~3 %H, period ~2 s) until a larger relaxed source is measured; mark provisional in the bible | use the Grok exaggerated idle as the source (7.8 %H — too hot) |
| R-d I-1 feet lock | **0.25 %H hard** (Legolas) — the K3 registration residual (1.24 %H) becomes a fail, which is correct | relax to 0.5 %H |
| R-e band ceilings | **1.5× target** (memo) | per-gate from Legolas § 5.4 where stated (W-1 7 %) |
| R-f X-video role | **in-betweener candidate with rules** (0–4.3 s only; amplitude prompted to band; our cut closes the loop; identity via G11) — decide at step 8 on numbers | instrument only · drop |
| R-g PD judge anchors | **yes** — Muybridge frames may calibrate the motion transcriber (X0-M) | our frames only |
| R-h relaxed vs combat first | **relaxed first** (hub-facing; 2 s) | combat first |

## 4. Halts (pre-registered) + honorable fallbacks
- **H-3** K1′ master fails the JUDGE control or the H1 sentence does not survive CHECK (O8 brush-grain) → fallback: mint 2 more; if still failing, C-2 continues on master L pixels with the H1 sentence deferred (register decision unchanged).
- **H-4** K3′ walk-E frames cannot hold the pose guides (gait_intent W-2/W-4 fail on ≥ 2 of 3 waves) → fallback: X-video walk frames as the candidate for step 8; L5 stays open with numbers.
- **H-5** any TOOLING needed mid-session beyond T-freeze/T3 → HALT; no code beyond the two named bursts.
- Image cap for C-2: 60; a wave that would exceed it is not launched.

## 5. Exit criteria (decidable)
- **PASS**: idle-S within the relaxed band AND feet LOCK AND G11 ≤ threshold; walk-E W-1 in band, W-2 phases per the table, W-4 = 2, W-6 ≥ 9/12, G6c ≤ 1.25 — both shown beside the oracle and ruled by Matt.
- **FAIL-WITH-NUMBERS**: any gate outside band → the number, the frame, and the fallback taken are in the ledger; that is a complete C-2.

## 6. Restart prompt (paste at C-2 launch)
> Session-start per OP § 1 incl. the charter-freshness gate. Read `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` and verify § 7 SYNC. Execute `agentic_orchestration/gandalf/notes/2026-09-12-astra-burst-lane-hitl-run-C-2-plan.md` from § 1. RUN-CONDUCTOR; Astra does all labour via `lane/run_burst.py`; gandalf writes no code; Matt present from step 2; rulings from § 3 one word each; push as you go (R-24).
