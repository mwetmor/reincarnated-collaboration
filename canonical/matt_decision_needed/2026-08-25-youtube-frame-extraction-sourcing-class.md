# matt_decision_needed — Is frame extraction from published YouTube videos an authorized sourcing class?

**Filed:** 2026-08-25 (gandalf, RUN-CONDUCTOR — VFX-DEPTH run, charter R-17f; raised by galadriel at W-E1 landing as "routing 11," explicitly NOT taken on agent authority).
**Class:** sourcing-policy commitment boundary. **Blocking:** NO — the run proceeds on the already-authorized classes.

## Context

W-E1 repaired the run's substrate arithmetic: measurable twin videos went **2/24 → 23/24**, but almost entirely via the **2012 Blizzard CDN tree** (publisher's own Akamai origin, T-A spec § 6.6-authorized) plus one first-party forum MP4. **~15 rows still have YouTube URLs as their CANONICAL reference**, from which the lane has only ever taken published thumbnails — five of them title cards with no gameplay. For those rows, the donor/CDN structure is the measurement ceiling unless frames may be cut from the YouTube masters themselves.

Usage would be: internal measurement only (frame forensics, blind-extraction input, judge-panel input). Nothing republished, nothing shipped.

## Options

- **(a) YES, broadly** — any published gameplay video is frame-extractable for internal measurement. Upgrades ~15 rows from donor-inference to canonical measurement. Widest evidence base; loosest sourcing posture.
- **(b) YES, narrow** — only videos on **publisher-official channels** (the YouTube mirror of the same class § 6.6 already authorizes on the CDN). Upgrades most of the 15; excludes third-party uploads.
- **(c) NO** — donor/CDN structure is the ceiling; the T-A spec records that ceiling **knowingly** (a named limit, not a silent one).

## Conductor's lean

**(b).** It is the same authorization § 6.6 already granted, transported to the publisher's other distribution channel — no new principle, just a new pipe. (a) adds third-party-upload provenance questions the run doesn't need; (c) leaves ~15 rows judged against donors when the canonical is one click away. Your call — this is sourcing posture, not design.

## Disposition

One word suffices: **a / b / c**. R-17f holds all YouTube-dependent evidence-tier upgrades gated until this resolves; CDN-class upgrades (`cone`, `dash_attack`) proceed regardless.

## Disposition — WORKING (2026-09-12, gandalf, RUN-CONDUCTOR Run C-1; pending Matt's explicit a/b/c)

Matt (2026-09-12, animation-oracle work): *"gather representative sample videos (walk, 2 idle types) from an ARPG type painted 2D style game and break those apart into frames … Hades may be a good fit."* That is a class-E use — frames cut from a shipped game's published video — for **internal measurement and Matt's private comparison only**: tuning the gait gates and the cycle prompt guidance against Muybridge; never a burst input (`lane/ref_provenance.py` refuses it), never redistributed. It maps onto **(b)**: legolas R10c is scouting **publisher-official** Supergiant material first (trailers, dev diaries, Steam store videos); third-party captures only where no official clip shows the cycle cleanly, flagged as such. Recorded as the working posture; **Matt confirms a / b / c** to close this row. Cross-ref: ledger R-19 (judge-anchor vs generation-reference are distinct before policy — CraftPix forbids AI testing/validation; CC0/CC-BY/PD are anchor-safe), Q73(e).

---
## 2026-09-12 — R10c returned: the licence reading TIGHTENS the disposition (gandalf, HALT to Matt)
Legolas § 9 (`agentic_orchestration/legolas/research/2026-09-12-r10-walk-idle-cycle-oracle/findings.md`, `b2a2987f`): Supergiant Website ToU § 3.5 forbids "download, copy or use" of Supergiant content (only grant: noncommercial fansite reproduction; no research/measurement carve-out); YouTube ToS and Steam SSA forbid downloading; the E1/E2 (official vs third-party) split does NOT track the download restriction. The restricted act is the download itself, so working disposition (b) still performs it. Hades II is 3D-rendered (not painted-2D); no Hades cycle maps to 12 frames — Muybridge supplies structure, clips only amplitude; the amplitude rule is first-party (Williams "increase the ups and downs"; Hades animator Thinh Ngo: push timing "almost like hand-key").
**Top clips (view-only):** `youtube.com/watch?v=GlV6omZqbJo` @ 6:44–8:15 (Zagreus, Eternal Spear, fixed camera, smears 7:05–7:15 · class E2) · Bastion Steam trailer @ 0:18–0:33 (app 107100, movie 80996; Kid ~250 px, facing N · E1) · `youtube.com/watch?v=GRSI7iAT4Tg` @ 19:10–19:35 (official dev stream, House walk, low amplitude · E1).
**Gandalf recommendation (one): option (c′) — NO download; Matt frame-steps in the YouTube player (`,` / `.` while paused) at the timestamps to compare against Muybridge plates 2/13; spec amplitude from published ratios (Williams; Legolas § 5.4 ranges), floor from Muybridge. Alternative (b) as previously recorded, with the ToS breach on record.** `clip_to_oracle.sh` NOT run. Status: OPEN — Matt rules.

**RULED 2026-09-12 — Matt: "download" (option b).** Private extraction for measurement + Matt's comparison only; frames outside the repo (Desktop class-E folder, SOURCE_and_CLASS sidecar); never redistributed; never a burst input (`lane/ref_provenance.py` refuses class-E paths). ToS breach recorded as knowing, private, non-commercial. Status: RULED.
