# Radagast (Fable-5) — Manifestation-Moment UE Feasibility + Architecture Consult

**STATUS:** COMMISSION — paste-ready opener for a fresh Fable-5 Radagast session (Goal-1, step 1: UE feasibility consult for the character-creation "grassy-knoll" manifestation moment)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8, Mac side)
**Why Fable-5:** first real PC-seam design-generation run at the higher model tier; gradable single-agent output (NOT a handoff eval — no air-gap concern).

**Launch notes (do NOT paste into the Radagast session):**
- PC-resident agent → use the tmux-wrapped WSL launch (the new default per CLAUDE.md). Step-by-step:
  ```
  ssh -t mhwet@192.168.1.133
  wsl -d Ubuntu
  tmux new-session -A -s pc-work
  cd /mnt/c/dev/reincarnated-collaboration
  claude --agent radagast
  ```
- **Model tier:** Radagast's agent frontmatter was migrated to `claude-opus-4-8` (commit 823fe51). After a session-start `git pull origin main`, `claude --agent radagast` runs at Fable-5 automatically. To force it regardless of pull state, add `--model claude-opus-4-8`. (Avoid the `[1m]` suffix — it glob-errors in some shells.)
- **Verify tier in-session:** if unsure, ask the session to confirm its model before the work; if it reports Opus 4.7, the frontmatter didn't pull — re-pull and relaunch.

---

## PASTE-READY OPENER (everything below the line)

---

You are radagast, the PC-side design steward (UE / Niagara / Mutable / asset-pipeline / rendering / animation domain). Read your operating procedure skill (`reincarnated-radagast-operating-procedure`) and execute the session-start protocol per your OP — **including `git pull origin main` FIRST** (PC pull discipline; Mac-side commits don't reach the PC until you pull). Then take on the commission below.

**Mission: a UE 5.7 feasibility assessment + recommended technical architecture + implementation plan for the character-creation MANIFESTATION MOMENT — the "grassy-knoll" scene.**

This is the moment the player's reincarnated character *manifests* in the new world. It is the single most thematically loaded scene in a game literally titled *Reincarnated* — the threshold where the Earth-self crosses into a new-world form, under the cosmograph night-sky, and is bound to a star-sign. **It is NOT a character-creator menu.** It is a narrative-experiential set-piece whose job is awe, identity-crystallization, and the weight of a new beginning. Design for that feeling, not for a stats-selection UI.

### Required discipline (declare at the top of your deliverable)
1. **Canonical-source-consultation declaration.** Before assessing feasibility, read the authoritative scene + world definition in full (NOT ground-state one-liners). Find the current sources via `canonical/00-ground-state.md` and the `canonical/story/` creation-moment / cosmograph lineage. At minimum consult: the cosmograph-pivot doc, the creation-moment / kit↔star-sign binding architecture, the federated-PC-team architecture commit, any prior Radagast notes touching character/VFX/Mutable, and any Mantis spike-findings relevant to character manifestation, Niagara, or the sequencer/asset pipeline (a Mantis WS3.1 sequencer-asset close just landed — read it; it's directly relevant). **Declare every doc you read in full.** If the canonical scene definition differs from the thematic framing above, the CANON wins — flag the delta and note it for Mac-gandalf.
2. **Substrate-led.** Respect what the canon and the existing UE project already establish; don't pre-impose UE patterns the project hasn't chosen.
3. **Recognition-validate-commit.** Flag every value/assumption you scaffold or placeholder explicitly (Discipline #40). Do not present a guess as a locked recommendation.
4. **D7 AI-tell line (HARD here).** This is a MAJOR moment. No raw LLM dialogue/generation at the manifestation beat — any text/voice is human-authored or templated-with-narrow-blanks. If your architecture touches runtime content generation for this scene, it must honor D7.

### Scope guard (read carefully)
**THIS SCENE and its immediate near-neighbors ONLY.** Assess: the manifestation beat itself, the cosmograph night-sky it happens under, the player-form/avatar that manifests, and the transition in/out. Do **NOT** design the whole game's UE layer, the full combat system, the loadout flow, or the broader Earth-self meta-loop. If the work pulls you toward "design everything," stop and stay bounded — an unbounded UE design doc has a huge silent-assumption surface and isn't gradable. Bounded scope, gradable output.

### Required deliverable contents
1. **Scene understanding** — restate, in your words, what the manifestation moment IS (design intent + target player experience), so Mac-gandalf can confirm shared understanding before any build. Flag any delta from the canon you found.
2. **UE 5.7 feasibility assessment, by subsystem** — what is achievable, with honest difficulty ratings:
   - the manifesting player-form / avatar (is this a Mutable use-case? skeletal-mesh morph? what's realistic?)
   - the cosmograph night-sky (rendering approach — skybox? volumetric? the star-signs as visible constellations?)
   - the manifestation VFX (Niagara — the act of a form coalescing/manifesting)
   - lighting / atmosphere / the "grassy-knoll" threshold environment
   - animation + sequencer orchestration of the beat (leverage the WS3.1 sequencer-asset work where relevant)
3. **Recommended technical architecture** — the UE approach you'd choose per subsystem, with the *why* (and the alternative you rejected).
4. **Implementation plan / sequencing** — phased, with dependencies. What's first, what blocks what.
5. **Risks, unknowns, and spike candidates** — explicit list of what you are NOT confident is feasible without a **Mantis spike** to de-risk it. Name each spike, what it would prove, and roughly how cheap/expensive it is. This is high-value output — be rigorous about what's unproven.
6. **Cross-cutting data contracts (IMPORTANT)** — what does this scene need to be FED by the engine? At minimum: the player's manifested form/avatar data, the kit/star-sign assignment (the engine emits a `kit_star_sign_assignments.json` sidecar — schema v1.1), and any cosmograph data. Name the contracts the scene depends on; flag any that don't exist yet. (This feeds a parallel Mac-side forward-architecture effort on the generation↔sim↔UE-emit contracts — your contract list is a load-bearing input there.)
7. **Scaffold register** — every placeholder/assumed value, listed, so it's auditable.

### Authority + cross-host
- This is PC-seam feasibility — your domain. Push back hard if you see design drift or a UE pattern that fights the scene's thematic intent.
- For cross-cutting architecture questions (engine emit contracts, anything spanning Mac seams), file a cross-host consultation note to Mac-gandalf rather than deciding unilaterally.
- Run Sam (Gate-1 peer) on the deliverable if your local trio process calls for it; otherwise this is a design-generation artifact for Matt + Mac-gandalf review.

### Output
Write the deliverable to `agentic_orchestration/radagast/notes/2026-06-10-manifestation-moment-ue-feasibility-consult.md`, STATUS-stamped. Auto-commit authorized (PC wave-close push pattern). When done, report: the deliverable path, a one-paragraph summary of your top-line feasibility verdict (is the scene buildable as envisioned in UE 5.7, and what's the single biggest risk), and your shortlist of Mantis spike candidates.
