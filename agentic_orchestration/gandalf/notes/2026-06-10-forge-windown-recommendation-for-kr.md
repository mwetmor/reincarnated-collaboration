# Forge / Loadout Web-App Wind-Down — Recommendation for Knight-Rider (pick up cold; no live KR session)

**STATUS:** RECOMMENDATION — Matt-authorized decision captured for KR next-session pickup (KR had no open session at decision time)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Decision authority:** Matt (this session) — "It was always scaffolding — kill it."

---

## 1. The decision (Matt-authorized)

The web `/forge` + loadout app (`reincarnated-loadout/`, drax's seam, deployed to Vercel) is to be **wound down.** Matt confirmed it was **always scaffolding** toward the real UE surface — never intended to ship as a player-facing companion. UE is now the single player-facing surface.

This is a **recommend-and-escalate** captured durably because it crosses drax's whole seam and KR sequences seam-level work. Matt has authorized the wind-down direction; KR sequences the *how*.

## 2. Why (design-steward rationale — so KR has the reasoning, not just the order)

1. **Drift-hazard removal (the load-bearing reason).** Two cosmograph implementations (web 2D forge + UE 3D sky) are exactly the cross-surface coherence hazard flagged in `agentic_orchestration/gandalf/notes/2026-06-10-radagast-manifestation-design-fit-review-and-cosmograph-contract-response.md` § 3.2 — a star-sign that's a neighbor in the forge becoming a stranger in the sky, breaking the player's spatial memory across surfaces. **One surface = the hazard dissolves.**
2. **Contract simplification.** Killing the forge removes the `forge_2d` projection clause from the cosmograph spatial-layout contract (§ 3.6 of the review). The contract becomes "sphere positions only," and the §3.3 forge-provenance open question (routed to drax) is **moot — drop it.**
3. **Prototyping value spent.** The forge made sense as a fast-iteration surface *before* UE was proven. UE is now empirically proven (mantis spike GREEN; 15K stars @ ~92 FPS). The scaffolding has done its job.

## 3. What KR sequences with drax (the open how-questions)

- **Archive vs delete:** what in `reincarnated-loadout/` gets archived (git history preserved; likely tag + README pointer) vs actively removed.
- **Migrate-forward salvage:** any design learnings / layout heuristics / data-shape work in the forge worth carrying into UE-side tooling rather than discarding. (The 2D web layout itself does NOT migrate — UE computes the sphere from the embedding per the cosmograph contract.)
- **Vercel deployment disposition:** does the deployed app go **dark** (taken down) or **frozen** (left up, no further work)? Lean: dark, to avoid a stale player-facing artifact drifting from canon.
- **drax mandate after wind-down:** drax owns `reincarnated-demo/` (Pixi.js) + `reincarnated-loadout/`. With loadout retired, confirm drax's remaining scope (demo1 status; whether drax redeploys toward UE-adjacent player-surface work or the seam goes dormant).

## 4. One thing to preserve (design note for the sequencing)

**Iteration speed.** Web iterated faster than UE (no compile/DDC). As the forge retires, ensure UE-side has *some* fast design-iteration path — even an internal-only tool — so design exploration doesn't get strangled by the UE compile/editor loop. This is a discipline note, not a blocker.

## 5. Not in scope (drift guard)

- A future PoE-style **web build-planner** for the community is a clean-sheet future project, NOT a reason to keep this codebase. Explicitly out of this wind-down.
- Mobile (D8) is a UE target, not a reason to keep the web app.

## 6. Sign-off

**Author:** gandalf (Opus 4.8), 2026-06-10. Matt-authorized direction; KR sequences execution with drax. Composes with the cosmograph-contract review (same session) — wind-down simplifies that contract.
