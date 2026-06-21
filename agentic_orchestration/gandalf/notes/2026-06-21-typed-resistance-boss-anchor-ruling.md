# Typed-resistance boss anchor ruling — design-side disposition (G-C input)

**Author:** gandalf (design seam). **Status:** Matt-agreed 2026-06-21. **Gates:** resolves gamora's reserved open question (the unmatched-difficulty anchor, §9.7 of the calibration note); is the G-C input KR was holding before firing the finalized joint re-rate.

**Reads first-hand:** `simulation/math/typed-resistance-resolver-spine-and-calibration-2026-06-21.md` §9.2 / §9.4 / §9.5 / §9.7 (gamora tag `0c6ba9d`, Gate-2 PASS-WITH-CONCERNS).

---

## The ruling

**Lock boss `damage_multiplier` = 5.0 @ cadence 4.5s. Do NOT push to 6.0.** Swarm `damage_multiplier` = 0.20 (the re-derived trash<boss value) holds.

## Why not 6.0 — it is the PoE tax wearing a difficulty knob

- §9.2: cohort fixtures cliff from **0.50–0.625 unmatched at dm=5.0 → 0.00 at dm=6.0** — one knob-step takes the lower-offense kits from "tense coin-flip" to "dead."
- §9.5: the population's weakest *real* kits already sit at **0.438** unmatched at dm=5.0. Push dm and that tail follows the cohort to the floor.
- That is the exact failure the wave forbade: **unmatched = match-or-die.** D2 made resist a threshold you potion-chugged under; PoE made under-cap a one-shot. dm=6.0 is the PoE version.
- **Structural reason dm is the wrong lever:** dm moves the *whole distribution.* The thin tail is already at the right risk (0.44 is a genuinely tense thin-kit fight — keep it). Any dm increase taxes the tail *before* it firms the median. You cannot dial the median down with dm without crushing the floor.

## Why dm=5.0 is the safe lock

All four guards passed there: no one-shot (analytic ceiling ~13.4), matched comfortable (1.0), anti-tax holds on the **production** roller (max total resist 1.60 < 2.0, §9.4), trash strictly below boss (§9.5). It is the tax-free foundation.

## The named cost — a WATCH-ITEM, not a blocker

Population unmatched mean = **0.924** (§9.5). Read as player feel: the median build brings the *wrong form to the fire boss and wins 92% of the time without noticing the fire.* The §3.4 "bring the right form" payoff currently bites at the **tail** (under-geared/thin kits), not the median — a mechanic only the under-resourced feel never teaches itself to the broad player.

**Do not read 0.924 as failure.** The spine is the win: before this wave the kit's defense was a globally-inert constant; now it is live and typed, and the §3.4 mechanism *exists.* 0.924 is "tuned soft," not "broken." Lock the foundation; the softness is firmable on top of a now-correct base.

## The firm-up is a SEPARATE design beat — do not bolt it onto this close

To make the defensive read a *median* experience, the lever is **not** a damage knob — it is the **encounter model:** a heavy-slow telegraphed slam answerable by **dodge OR resist regardless of DPS.** Fast kits dodge it, matched kits tank it, unmatched-loose kits eat it — everyone reckons with the boss's element. This is the **same §4 encounter-model question the proxy decision packet raised** ("DPS-race step vs graded outcome"). Both threads now point at one design beat. **gandalf owns that follow-on.** It does NOT block this joint close.

*(Within-wave partial lever, parked unless Matt calls for it before emission: boss HP/TTK up — more slams land on fast kits, firming the median without raising per-hit damage / one-shot risk — but it needs a gamora sweep to confirm it does not crush the slow tail by attrition. The clean structural fix remains the encounter model, not a knob.)*

## What this unblocks / what stays Matt-gated

- **Unblocks:** gamora's finalized two-axis joint re-rate (G-C / §6h) against the dm=5.0 / swarm dm=0.20 bands. Telemetry already live (star-lord `player_death_element`).
- **Stays Matt-gated (unchanged):** band finalization + content emission (G-C close); the three additive DB-apply auths (`_V2_17`/`_V2_18`/`_V2_19`, ADR-006); push (whole wave held).
