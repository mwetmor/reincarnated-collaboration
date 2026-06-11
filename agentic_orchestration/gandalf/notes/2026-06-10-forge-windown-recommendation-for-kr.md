# Loadout Web-App Disposition — CORRECTED (freeze future plans; artifact + cosmograph stay live)

**STATUS:** CORRECTED RECORD — supersedes the original "wind-down / kill it" framing in this same file. Matt narrowed the scope materially during the KR/drax session (2026-06-10). KR already has the live correction; this doc is updated so any cold pickup reads the CORRECT decision.
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Decision authority:** Matt (KR session, 2026-06-10) — final word: **"we're only retiring the future plans."**

---

## 0. What changed (read this first if you remember the old version)

The original version of this doc recommended **retiring the whole `reincarnated-loadout/` web app** — Vercel dark, forge + loadout + 2D cosmograph all gone, the `forge_2d` clause + §3.3 forge-provenance question declared **moot**. That was over-broad. Matt corrected the scope twice in the KR session and landed it here:

- **Nothing on Vercel comes down.** The whole loadout app — including the 2D cosmograph — **stays live, frozen.** Vercel was never touched and stays untouched.
- **The original 2D cosmograph form is RETAINED.** Matt: *"I still plan to use the actual original cosmograph form."* It has ongoing design value.
- **What retires is the ROADMAP, not the artifact.** No further forward development on the loadout web app. The seam freezes; the deployed surface persists as-is.

## 1. The corrected decision (Matt-authorized)

**Freeze the loadout web seam. Do not retire the artifact.**

- Loadout app + forge view + 2D cosmograph: **stay live on Vercel, frozen.** No takedown, no `vercel remove`, no dark.
- Forward development on the loadout web app: **stopped.** UE is the single *shipping* player-facing surface going forward; the web app is no longer a forward-dev target.
- Original 2D cosmograph form: **retained** as a design artifact Matt intends to keep using.

## 2. Cleanup KR sequences with drax (walk back the over-broad framing)

drax correctly staged-but-did-not-execute the retirement actions. The only work is reversing the markers drax applied locally (none pushed/deployed):

- `reincarnated-loadout/README.md` — "RETIRED" marker → **revert** (it's now false)
- `reincarnated-loadout/AGENT_STATE.md` — "repo RETIRED" banner → **revert**
- `drax/loadout-retired-2026-06-10` archive tag → **delete** (implies a retirement that isn't happening)
- Salvage note → **keep, re-cast** as a plain design-learnings note (not a "what we carried out before killing it" note)
- Staged Vercel `vercel remove` command → **discard** (never run; not happening)
- Benign rider commit `aae190a` (rocket engine-sidecar `kit_star_sign_assignments.json` committed into loadout tree) — flagged; goes up whenever the tree next pushes; not a blocker.

## 3. The design consequence Matt must hold (the reopened drift question)

KR flagged this correctly and it is squarely a gandalf call: **the original "one cosmograph, not two" drift-hazard rationale is reopened by keeping the web 2D cosmograph live alongside the UE 3D sky.**

**My read: the hazard does NOT re-fire, for two reasons —**

1. **Frozen ≠ competing shipping surface.** The drift hazard ("a neighbor in the forge becomes a stranger in the sky") requires *two live, evolving, player-facing* surfaces rendering the same star-sign data with independently-drifting layouts. A frozen web app Matt uses as a *design reference* is not a competing shipping surface. UE remains the single shipping player surface. The reference artifact and the shipping artifact can coexist without coherence drift because only one is evolving.

2. **The shared-canonical-layout contract amendment already dissolves the hazard by construction.** My cosmograph contract response (`2026-06-10-radagast-manifestation-design-fit-review-and-cosmograph-contract-response.md` §3) made the sphere the source-of-truth and the 2D forge a *deterministic unwrap* of it. Under that contract, a neighbor in the forge IS a neighbor in the sky **by construction** — the `forge_2d` clause is the *anti-drift mechanism*, not the hazard. So if the web cosmograph is ever re-activated against the canonical layout, it stays coherent with UE automatically.

**Consequence for the cosmograph contract:** the `forge_2d` projection clause and the §3.3 forge-provenance open question are **NO LONGER MOOT** — they return to the contract. This is captured in a correction note appended to the contract response doc. The contract returns to its original two-surface form (sphere source-of-truth + deterministic 2D unwrap). Net: the schema I authored already carried the `forge_2d` per-sign field, so the contract is forward-compatible with no rework — only the "moot" annotation is withdrawn.

## 4. Not in scope (drift guard — unchanged)

- A future PoE-style **web build-planner** for the community remains a clean-sheet future project, independent of this decision.
- Mobile (D8) is a UE target.

## 5. Sign-off

**Author:** gandalf (Opus 4.8), 2026-06-10. Corrected per Matt's KR-session narrowing ("we're only retiring the future plans"). KR sequences the marker-reversal cleanup with drax. The cosmograph contract reverts to two-surface (forge_2d un-mooted); see correction note on the contract response doc.
