# Next-Steps Memo — post P0.1 resumed render session

**STATUS:** HANDOFF. Read by (a) **next-david-h** picking up in the SSH/TMUX `mhwet` orchestration session, (b) **gandalf** (cross-cutting design questions surfaced), (c) **Matt**.
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator, `TheSa` console session)
**Reads with:** `2026-06-13-p0-1-s5-blocked-findings-and-routing.md` (the findings) + the dispatch DRAFT `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md`.

---

## Where we are in one paragraph

P0.1 manifestation render session resumed on `TheSa`. **Outcome: findings, not captures.** The session was meant to bank S5 (figure-lighting Rig A/B readability) safely while S1 (the sky) stayed deferred. Live diagnosis blocked S5 on the same root cause as S1 — the celestial sphere is broken. Nothing was saved; the scene reverts to pristine for mantis. Two artifacts are committed locally on `TheSa` (`19c09f8` findings, `79ed954` dispatch DRAFT) and need pushing from `mhwet`.

## The three findings (detail in the findings note)

1. **Volumetric nebula crashes the GPU** (Heterogeneous Volumes raymarch) — confirmed; CVar-suppressible; mantis will tame it so it's cheap-enough-to-leave-ON.
2. **Celestial sphere = 1,005,000 CPU Niagara particles clustered at the origin** (the "±67 spike cloud"), not on the R=8,000 sphere. Exceeds UE's 1M CPU cap; sits as a GPU landmine under the figure. One root cause behind BOTH S1 and S5 failures.
3. **`SK_EarthAvatar` is a black silhouette in Lit** (great in Unlit) even with `RigA_Moonlight` ON, Channel 0, 10× intensity. The rig leaned on the deleted star-cloud for fill. Mantis rig repair.

## Planned next steps — for next-david-h in the SSH/TMUX session (in order)

1. **PUSH FIRST.** This session is the `mhwet`/WSL context where the GitHub SSH key works. Run `git pull --rebase origin main` then `git push origin main` to publish `19c09f8` + `79ed954` + this memo. (They were committed on `TheSa`; `C:\dev\` is shared on disk so they're already in the working tree.)
2. **Run PC-trio ratification (Pattern E) on the dispatch DRAFT** — fire **sam** (Gate-1: scope, acceptance testability, math-before-code sufficiency, R48.4) and **radagast** (design-fit, see questions below) in parallel as Pattern A subagents. Fold verdicts into the dispatch.
3. **Flip dispatch STATUS DRAFT → ACTIVE** if both PASS (address any WARN inline; resolve any BLOCK before firing).
4. **Author the cross-host note to Mac-KR** — `david-h/notes/<date>-consultation-mac-kr-p0-1-findings-not-captures.md`: P0.1 produced findings not captures; S5 + S1 both gated on the celestial-sphere rework; manifestation Phase-1 spike forward register updated.
5. **Push again at wave-close.**
6. **Then a dedicated mantis session** can execute the fired dispatch (`claude --agent mantis` from `C:\dev\reincarnated-unreal\Reincarnated`).

## Design questions — for gandalf + radagast + Matt

- **Figure-lighting independence (the load-bearing one):** the Earth avatar's lighting currently *depends on the celestial sphere* for fill — that's why it went black when the sphere was removed. Should the figure carry its **own key light independent of the sky**? This touches the creation-moment scene composition (Earth avatar on the knoll under the celestial sphere), so it may be cross-cutting, not purely PC-seam — gandalf's read welcome. Radagast holds the PC-seam design-fit call; gandalf consulted if cross-cutting.
- **Spirit visual scoping:** the spirit form is currently `FigureStandIn` — an explicit **placeholder particle ball**, not an intended ambiguous-spirit mesh. When does the real ambiguous-spirit visual get scoped (Meshy + Control Rig pipeline per canon)? Design call for radagast/gandalf.
- **Gate-A confirmation:** the 1M-CPU-cloud-at-origin state strongly implies Gate-A (expose `StarPositions`/`StarColors` + `BP_CelestialSphere` loading the R=8,000 JSON) was never completed — the stars never made it onto the sphere. Confirm Gate-A is the correct unblock (the dispatch assumes it is).

## Git / push note (load-bearing)

- `TheSa` cannot push (GitHub SSH key is `mhwet`-scoped; pull/push fail with publickey-denied; `core.sshCommand` points at a WSL path — do NOT mutate it, WSL depends on it).
- The SSH/TMUX `mhwet` WSL session IS the push context. Step 1 above.
- Commit prefix discipline: `david-h: ...`.

## Sign-off

Session closed on `TheSa` with the scene unsaved (pristine for mantis). Dispatch is a ratified-pending DRAFT. Forward path is push → PC-trio ratify → fire → mantis. Matt invokes the SSH/TMUX orchestration session to carry this forward.
