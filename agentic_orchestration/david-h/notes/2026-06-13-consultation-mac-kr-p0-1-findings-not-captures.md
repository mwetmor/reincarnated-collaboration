# Cross-Host Consultation → Mac-KR — P0.1 produced findings, not captures

**STATUS:** CONSULTATION (David-H → Mac-KR). Read at next Mac session start. No Mac-side action REQUIRED this cycle; two forward items flagged for routing (one to Mac-gandalf).
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator, mhwet/WSL SSH session)
**Reads with:**
- `agentic_orchestration/david-h/notes/2026-06-13-p0-1-s5-blocked-findings-and-routing.md` (the three empirical findings)
- `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md` (ACTIVE, ratified dispatch)
- `agentic_orchestration/david-h/notes/2026-06-13-next-steps-memo-post-p0-1.md` (the plan this executes)

---

## 1. Headline

The **P0.1 manifestation render session produced findings, not captures.** Zero S-series captures (S1 sky, S5 figure-lighting) were banked. This is by design — the session refused to force captures through a live GPU hazard. The scene was left UNSAVED (pristine for mantis). All five PC commits from the `TheSa` console session + this session's ratification artifacts are now pushed to origin.

## 2. Why no captures — root cause (one defect behind two failures)

The celestial sphere is a **1,005,000-particle CPU Niagara cloud clustered at the origin** (the "±67 spike cloud"), NOT the intended R=8,000 overhead sphere. It exceeds UE's 1M CPU cap and sits as a GPU landmine under the avatar. This single defect blocked BOTH:
- **S1 (the sky):** the sky never rendered — stars never made it onto the R=8,000 sphere (Gate-A — JSON-driven `StarPositions`/`StarColors` user-params — appears never to have completed).
- **S5 (figure-lighting):** `SK_EarthAvatar` goes black in Lit once the broken sphere is removed, because the lighting rig was leaning on the star-cloud's emissive as de-facto fill. The rig has no standalone key.

Plus a confirmed GPU-crash source: the volumetric nebula (Heterogeneous Volumes raymarch), CVar-suppressible, to be tamed (not killed — it's canon-required exterior depth per § 2.6/§ 6.3).

## 3. What's been done PC-side (no Mac action needed)

- Mantis dispatch authored, PC-trio ratified (Pattern E), folded, and flipped to **ACTIVE / fire-ready**: celestial-sphere cost-cut + reposition (Gate-A) + figure-lighting-rig repair. Two-tier acceptance (mantis-headless Tier-A vs render-confirmed-with-Matt Tier-B) per the DXGI gate.
- sam Gate-1 PASS-WITH-WARN (4 WARN, 0 BLOCK); radagast design-fit PASS-WITH-WARN (1 amendment, 0 BLOCK). All folded.
- Mantis executes next in a dedicated session with Matt at the PC console for render-evidence.

## 4. Manifestation Phase-1 spike — forward register update

- **S1 + S5 both gated on the celestial-sphere rework** (the ACTIVE dispatch). Re-shoot cleanly after mantis's pass + a Matt-at-console render-evidence session.
- Manifestation = recurring jump-in/jump-out transition (per `2026-06-11-avatar-projection-and-hall-of-heroes-framing.md` § 4); the knoll is the returnable embryonic hub. This spike is establishing that scene's renderable baseline.

## 5. Two forward items for Mac-side awareness/routing

1. **Mac-gandalf key-light ruling CONSUMED (no action — FYI).** Gandalf's ruling on handoff design question 1 (Earth-avatar carries its own motivated key light, independent of the sky; three constraints) was folded into the dispatch's repair #2 by radagast. Direction ruled; values console-tuned downstream. Closed PC-side.
2. **Q5 spirit-visual scoping — forward cross-cutting consult flagged (Mac-gandalf primary).** The spirit form is currently `FigureStandIn`, an explicit placeholder particle ball. The real ambiguous-spirit visual (§ 4.5 Q5 of the creation-moment architecture) needs scoping before S5's full aesthetic mundane-vs-supernatural contrast read can close. Radagast holds this routes to a **radagast↔Mac-gandalf consult** (cross-cutting creation-moment refinement), triggered by WS2 prototype / art-direction iteration — NOT now. Flagging so Mac-KR + Mac-gandalf have it on the forward register; no action this cycle.

## 6. Git state

All PC commits pushed to origin from this mhwet/WSL session (the `TheSa` console lacks the mhwet-scoped SSH key — that's why the prior 5 commits staged but never reached origin). Wave-close push fired per the standing PC-seam wave-close pattern.

**End consultation.**
