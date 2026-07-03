# Skill Handoff — 2026-07-02 — One Realm MVP: Godot spine CLOSED + two-lane wave FIRING

**Author:** knight-rider · Matt-facing (per OP §3.1)

---

## Pending Matt-decisions queue

| # | Decision | Gating criterion | Where it surfaces |
|---|---|---|---|
| 1 | **Ranged-proxy nav fork** — fix nav (Lane B) vs. EXCLUDE ranged summoners from v2 curation | gandalf lean: EXCLUDE (melee certifies clean; nav fix post-demo). Does NOT gate B4 (run emits; B5 curation chooses). | B5 report (after B4 lands) |
| 2 | **Run-registry schema** — the minimal runs-table write shape | star-lord proposes with B4 → jack-ryan Gate-1 → Matt ratifies | B4 (HELD until B1 lands) |
| 3 | **Push authorization** — engine repo is 8 commits ahead of origin; meta-repo carries this session's relay + fold + wave commits unpushed | Matt-explicit per ADR-006 (relay §1 confirmed the prior chain is on remote; forward = commits auto-fire, push at wave boundaries Matt-authorized) | Now — awaiting go |

## Active workstreams + status (in flight NOW)

- **Lane A (Godot, drax) — FIRING:** D5 (verb realization incl. summon, §20d heart) · D6 (three-beat floors, camera ratifies floor-1 EARLY) · D8 (grimoire + scouting UI). One drax session, sequenced, against bundle-v1 bridge (`08e6f24`). Gate-1 cleared (jack-ryan + gandalf); folds applied. Multi-day — expect progress + the §20d cost datapoint, not all-three-complete in one run.
- **Lane B (engine) — FIRING lead:** B1 Phase 1 (rocket — proxy-T4 suite architecture + η + dormant-five revival) against gandalf's canonical spec (`proxy-t4-suite-spec-2026-07-02.md`). Gamora Phase 2 (numbers) fires AFTER rocket (same-repo serial).
- **Lane B queued (authored, sequenced within lane):** B2 gear-pass (star-lord; feeds D8) · B3 six-type flavor completion (star-lord + gandalf curation) · B4 summoner un-gate + demo emission run (**GATED on B1**) · B5 v2 roster curation (**GATED on B4**).

## Awaiting-Matt blockers

- **Push** (queue #3) — the only hard blocker; everything else is in-flight or seam-owned.
- B4/B5 are gate-HELD on B1/B4 respectively (not Matt-blocked).

## Recent Matt-decisions (this session, where they landed)

- **Two-lane fire order** (relay §4) — EXECUTED: Lane A folded to FIRES; Lane B B1-B5 authored; MASTER §8 board added.
- **Q5 60 FPS min-spec floor** (relay §3.1) — RATIFIED → filed to decisions-log (`787da67`, engine repo).
- **§6.7 serial-content-emission split** — jack-ryan RATIFIED (total-content-supersession-with-pointer-stub); the fourth ledger is canon.
- **Four rulings (relay §2)** — all-six-types demo bundle / zero hand-authored shipped content / proxy-T4 demo-critical / split ratified — carried into the Lane B dispatch scopes.

## Next-session pickup (concrete first action)

1. **Process drax + rocket completion notifications** (do NOT poll). On rocket B1 Phase-1 land → fire gamora B1 Phase 2 (sim-eval + magnitudes; engine repo, after rocket vacates). Check rocket's Phase-1 exit-gate answer (new emitted field? → star-lord MIGRATION flag).
2. **On drax Lane A returns:** verify artifacts empirically (Disc #11); capture the §20d cost datapoint (the headline validation — surface to Matt if 10 kits collapse to <10 distinct verbs).
3. **Sequence B2 (star-lord)** into the engine window when B1 frees rocket/engine tree (or schedule against Lane B serial order).
4. **Carry Matt-plate items** (queue #1/#2) to the B4/B5 reports.

## Gate/commit ledger (this session, meta-repo — UNPUSHED)

- `cc0c523` two-lane relay execution (Lane A folds + Lane B B1-B5 authored + MASTER §8)
- `251c03c` Gate-1 folds applied (D5-a/b, D6-1, B1-1/2, B2-1)
- Engine repo: `787da67` Q5-60fps decisions-log entry (jack-ryan)

**Signed:** knight-rider, 2026-07-02 — relay executed end-to-end: authored → Gate-1 → folded → FIRING. Both lanes running; monitor-not-poll.