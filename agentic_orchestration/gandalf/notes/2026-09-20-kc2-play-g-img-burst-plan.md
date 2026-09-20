# KC2-PLAY · G-IMG packet — the first frame, and the plan for the first burst

> **For Matt.** Gate of record: charter § 6.1 / ledger KP-3 — *"I want to see it and understand the planned burst before the first burst fires."* **No burst has fired. None fires until you say go on this packet.** Conductor: gandalf (RUN-CONDUCTOR), 2026-09-20.
> Files: `~/Desktop/KC2-PLAY Review/001 G-IMG first frame (open this first)/` — `01_…ZOOM-GD` is the default view; `02_…ZOOM-HOUSE` is the same frame at the house zoom (the F4 toggle). Both sent to your phone.

## 1 · What you are looking at

A **mock** — composed by drax from things we already had, without any Astra burst, without Godot, without new art. The art is placeholder; **every distance is real**: the arena ring from your own 21-shot perimeter walk, the six green pools (radii are upper bounds), the Keeper at the ruled 8 % figure, the EoR ring at the pack's 3.0 m radius (454 px across at this zoom), the Banner aura at 8 m, two summons pinned beside you with no health bar, the HUD with your five binds. Everything printed on the frame is derived from the formula in the script, and the script refuses to run if any derived number disagrees with the spec.

Things to notice, because they are what the real scene will do: **the ring is 2.3 screens wide and 4.3 tall at this zoom** — you will not see most of the arena at once, as in GD. The Banner reads **×1.03**, not ×2 (corrected — the +100 % sits on a sheet already at +3036 %). Monster body radii are **declared placeholders**: the pack carries no size key, so tokens are drawn at a chosen radius and say so.

## 2 · Four things I'd like from you on this frame (one word each)

| # | Question | My lean |
|---|---|---|
| **G1** | Does this composition — zoom, ring size, how much arena you see — read as the fight you played? Anything that must change before a burst tries to build it? | It reads. |
| **G2** | **Arena scale.** Nothing we hold can pin it (galadriel tested every route). The frame uses a registered choice, `u = 0.285` (window 0.246–0.324), making the arena ≈ 57 × 77 m. Ratify as the play value until your T24 screenshot (taken while channelling EoR) replaces it? | Ratify. |
| **G3** | **Opening wave.** The reference sim and your footage's timings both start at wave **151** from a checkpoint. Open at 151, with wave 150 available only as a labelled warm-up excluded from every statistic? | 151. |
| **G4** | **Potion key.** In your build the health potion is manual (the reference sim auto-fires it at 23 % health). Which key does your hand expect? | Whatever you used in GD. |

## 3 · The first burst — what it is, in plain language

**Name:** `KP-B1 · scene scaffold probe`. **Labour:** Astra (codex), one TOOLING burst, caps ≤ 40 min / ≤ 60 tool calls, detached, under the shared heavy lock; nothing else runs in the lane meanwhile.

**What it is asked to make.** A new, separate Godot 4.6 project at `astra_test_01/kc2play/` (its own tree — nothing is written under the cliffside's `burst/`, which Run C-7 owns and has frozen). Inside it: drax's headless runtime **vendored by checksum** (the burst verifies every file's sha before copying and refuses on any mismatch); the arena plate drawn from the geometry file at `u = 0.285` under the projection law; the Keeper's existing 8-direction cells; a **canned event stream** (a scripted fake fight — no combat logic yet) that moves one player token and a handful of monster tokens; y-sorting; a Camera2D at the GD zoom with the house zoom on a key. Then it captures one headless frame.

**From which references.** The mock's script and its receipt (the numbers of record) · the geometry file (sha-gated) · the 2D spec §§ 1–3 · the runtime's `MANIFEST.json` · the Keeper cells (copied, never moved). No source-game footage; no third-party art.

**What comes back.** The project tree; a receipt (files written, shas, tool census — the wrapper audits it, the burst cannot self-grade); one 1920×1080 frame; the burst's transcript.

**What is checked, mechanically, before I look.** (1) Every vendored runtime file's sha matches drax's manifest. (2) The frame's ring, pools and EoR ellipse land where the mock's script says they should, within a few pixels — the mock *is* the acceptance geometry. (3) Purity scan: no `CollisionObject2D` under any token; no `Input` in the runtime tree. (4) Nothing written under `burst/`. (5) The wrapper's forbidden-tool census is clean.

**What could go wrong, and what happens then.** *The wrapper cannot run a burst outside `burst/`* → that is the feasibility finding this probe exists to make; the scene seat falls to drax hand-building it (your L3), no halt. *Codex usage limit (it has stopped two runs)* → one retry; a second VOID → drax, per L3. *The frame is off-geometry* → the burst is rejected, re-briefed once with the diff; a second miss → drax. *Anything else* → a finding in the ledger, veto-open to you.

**What happens next if it passes.** Burst 2 adds the HUD and the GD mouse binds; burst 3 the monster tokens' procedural states and the telemetry recorder; meanwhile drax builds the combat runtime against the v3.2 pack (Wave 3) and star-lord cuts that pack (Wave 2). The first thing you can *play* arrives when Wave 3 meets the scene.

## 4 · Where Wave 1 stands (the seal is one step away)

Done: the v3.2 pack rows (791 rows, one honest absence) · the port-fidelity goalposts v1.0 and tolerance widths · your footage's expected-value table (24 rows) · the runtime skeleton (89 loader/rule checks green, purity scan clean) · the macOS build pipeline · this mock. In flight: goalposts v1.1 (carrying the corrections found since v1.0); jack-ryan then pre-reads them before any result exists. **Coverage denominator ruled (KP-9):** the runtime's coverage table counts the census's 89 enumerated row ids, not the note's 72 headline — a gate must count things it can list.

Your word on G1–G4 and on § 3 is what fires burst 1.
