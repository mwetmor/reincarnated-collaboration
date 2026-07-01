# Encounter-model firm-up — disposition (the soft-median watch-item, developed)

**Author:** gandalf (design seam). **Status:** ✓ RATIFIED 2026-06-30 (shape locked + floor-co-viability fork ruled PARK — see top stamp). Was design-of-record for the watch-item gandalf was handed at the typed-resistance wave-close (decisions-log `ea39ecc`; anchor ruling `2026-06-21-typed-resistance-boss-anchor-ruling.md` §30). **Mode:** Pattern-B development, verification-first.

**Reads first-hand:** `spatial_engine.py` (`_mint_telegraph_spec` :744, telegraph buffer :1523, byte-identical-when-off :1519); `cycle14_unified_bundle_emitters.py` (:363-373 monster bundle fields); `weapon_envelope_composer.py` (:152-180 guaranteed i-frame dodge); `telegraph-combat-model-2026-06-16.md` (gamora, dispatch 3 spec); `telegraph-dodge-temporal-decoupling-2026-06-15.md` (gandalf, parent ruling); `reincarnated-godot/` scripts inventory + AGENT_STATE.

---

## ✓ RATIFIED — Matt 2026-06-30

Matt ruled the fork (§ "floor co-viability"): **(i) PARK.** Both halves of the disposition are locked:

1. **Shape RATIFIED** — the unified encounter model is **build-floor (resist / tank / out-range) + dodge-skill ceiling (telegraphed signature slam)**. One model answers both the solo §3.4 firm-up and the proxy §4 grading (§ "Proxy convergence"). Design-of-record for the fire boss and its proxy analog.
2. **Floor-co-viability fork ruled PARK** — accept the 0.926 soft build-floor as measured correctly. **No dm=6.0 firm-up** (structurally the wrong lever — it taxes the under-geared tail before firming the median, re-introducing the tail-tax the anchor ruling rejected). **No gamora boss-TTK sweep commissioned.** The **dodge-skill ceiling carries the "wrong form should hurt" texture** when the Godot combat layer lands.

**Nothing fires now.** PARK closes the soft-median watch-item as a *disposition* and unsticks the proxy §4 encounter-model question (design-only). It authorizes **no sweep, no proxy build, no `_DEFERRED_PROXY_BINS` lift, no push.** The build gate stays deferred behind Godot reaching combat.

**Empirical criterion that gates re-engagement (NOT time-passage):** a **Godot combat-loop spike** (player HP + one enemy attack + hit/avoid resolution) that consumes ONE serialized telegraph and proves the dodge window is human-timable against the minted wind-up geometry (t_react 0.3s + escape/v_ref). Named build gate: **dispatch 4** (star-lord serialize TelegraphSpec + i_frame_window) **+ dispatch 5** (Godot combat loop). gandalf owns the dodge-ceiling design contract when Godot combat lands.

**Governance (this ruling's routing):** developed gandalf↔Matt directly — design rulings route through the design seam; KR sequences the resulting dispatch, not the disposition. Since PARK fires no dispatch now, KR's relay is informational: the watch-item is closed, the build gate is named and deferred.

---

## TL;DR — the watch-item is mostly already-designed and HALF-built. Do NOT bolt a sim re-tune onto it.

The soft median (0.926 unmatched survive+kill) is the **build-floor measured correctly** — not a balance defect. The firm-up lever is **completing the dodge-skill ceiling**, which is *already architected and half-built*, NOT tuning the sim floor down. Tuning the floor down is the dm=6.0 mistake my own anchor ruling already rejected, wearing a different hat.

## What I verified — the contract status that reshapes the beat

The "encounter model answerable by dodge OR resist OR tank OR out-range" is **not net-new to invent.** It descends from my own `telegraph-dodge-temporal-decoupling-2026-06-15` ruling, and it is half-built:

| Piece | Status | Evidence |
|---|---|---|
| **Telegraph geometry minted in sim** (wind-up + danger-zone shape) | **LANDED** | `_mint_telegraph_spec`; `wind_up_s = t_react 0.3s + escape/v_ref 4.0`; buffer `self.telegraph_buffer`; byte-identical when off |
| **Player's dodge tool baked into kits** (i-frame window on glass-close-ST) | **LANDED** | `weapon_envelope_composer.py:152-180`; `i_frame_window={start 0.05, dur 0.30}`; inert-in-sim by design |
| **Serialize telegraph + i_frame → Godot JSON** (dispatch 4) | **NOT LANDED** | bundle emits only `telegraph_window_seconds` (an R3 AI scalar), not the TelegraphSpec record |
| **Godot consumes telegraph, drives dodge window** (dispatch 5) | **NOT LANDED + BLOCKED** | `reincarnated-godot/` is a *presentation spike* — scene-building, rigs, VFX renders, a walk-around play-shell. **No combat loop: no player HP, no enemy attack, no damage, no dodge.** "Combat camera"/"combat floor" are camera-framing + staging terms, not gameplay |

**The data half of the contract is done** (the danger zone is minted; the dodge tool is in the kit). **The playable half is unbuilt** — and dispatch 5 is correctly *blocked* on Godot not yet having any combat loop at all.

## The consequence — the boss is build-primary by NECESSITY, not just by philosophy

The dodge answer carries **zero load in any surface that currently plays.** The sim is the only thing that "plays," dodge is inert there by design, and Godot has no combat. So today the three **build answers — resist / tank / out-range — are the only live defensive answers, full stop.** That is not a problem to fix; it is the correct staging of a temporally-decoupled design (sim = floor-skill instrument; Godot = skill ceiling, deferred).

## The ruling — build-primary FLOOR + dodge-skill CEILING (✓ RATIFIED Matt 2026-06-30 — see top stamp)

The fire boss is **answerable on the build-floor** (resist/tank/out-range — a thoughtful player who brought the right form survives even with zero dodge skill) **AND rewarding on the dodge-ceiling** (a skilled player times the i-frame roll against the telegraph). This is the genre-canonical split:

- **Souls/Elden Ring:** purest dodge-ceiling (i-frame roll is THE answer) over a build-floor (Vigor/poise lets you over-level and facetank). 
- **PoE:** facetank with resist+life+leech (floor) **or** dodge the Shaper slam / Sirus die-beam with movement (ceiling). Telegraphed, exactly this tension.
- **D3:** melee 30% intrinsic DR (floor) + still kite Desolator pools (ceiling). Last Epoch: armor/endurance floor + dodge-roll ceiling.

**The two failure modes — and which one 0.926 is:**
- **All-floor → stat-check boss.** This is the **Diablo Immortal "just get more Resonance" feel** — the boss is a gear threshold, no skill expression. **0.926-with-no-ceiling is precisely this risk.**
- **All-ceiling → thin-tail tax / match-or-die.** This is the **dm=6.0 / PoE one-shot-under-cap** the anchor ruling already rejected (cohort cliff 0.50→0.00).

The cure for a soft floor is **NOT to harden the floor** (that re-introduces the dm=6.0 tail-tax). **It is to build the ceiling.** 0.926 is correct *as a floor*; the missing texture is the dodge-skill ceiling, which is architected and half-built.

## The 0.926 median is the build-floor, measured correctly — LEAVE IT SOFT

The sim measures "can this build survive with **zero** dodge skill?" → 92.6% yes. For a build-primary floor with a future dodge ceiling, a soft-but-not-trivial floor is *right*. Tuning it down now would (a) chase a "median must sweat" feel the floor is not supposed to deliver — the sweat is the ceiling's job — and (b) lock a difficulty against a dodge-free world that the future dodge then undercuts, re-creating the exact **double-tax** my 2026-06-15 ruling forbade (don't auto-compensate the sim for a dodge that isn't there yet — in *either* direction).

## The one genuinely-live design question — floor co-viability (✓ RULED PARK, Matt 2026-06-30)

On the build-floor itself, the three live answers are **not yet co-viable: kill-speed (offense) substitutes for the defensive read** (calibration §9.3: dm_mod 0.4→3.0 → survive 0.583→0.958). So today the dominant "answer" is *kill it before the slam matters*; resist/tank are load-bearing only for the under-offense tail. The §3.4 "bring the right form" payoff bites at the tail, not the median — a mechanic only the under-resourced feel.

The lever to make resist/tank co-load-bearing with offense **without taxing the thin tail** is the parked **boss-TTK-up** lever (more signature slams land inside the kill window, so a glass-offense kit eats a slam it should have built for) — gated on a gamora sweep confirming it does not crush the slow tail by attrition (anchor ruling §34). **This is the only actionable-now design decision.** Matt's fork:

- **(i) PARK it.** Accept the soft floor; let the dodge ceiling (when Godot combat lands) carry the texture. *Recompose-first default.*
- **(ii) Commission the gamora boss-TTK sweep now** to firm floor co-viability ahead of the ceiling — only if the floor needs to stand alone for an extended window before Godot combat exists.

**Recommendation: (i) PARK.** The floor is honest; the ceiling is the real texture; manufacturing a sim sweep now is form-bias ("do something") against a number that is correct for what it measures.

## The empirical criterion that gates re-engagement (NOT time-passage)

The dodge-skill ceiling becomes buildable when **Godot has a combat loop** (player HP + an enemy attack + a hit/avoid resolution). That does not exist yet. The first substrate evidence that closes the watch-item: a **Godot combat-loop spike that consumes ONE serialized telegraph and proves the dodge window is human-timable** against the minted wind-up geometry (t_react 0.3s + escape/v_ref). That is the viability playtest my 2026-06-15 ruling deferred behind "the pipeline round-trip gate" — the gate is now precisely identified: **dispatch 4 (serialize) + a Godot combat loop (dispatch 5's prerequisite).**

## Proxy convergence — the encounter model is the SHARED answer

The proxy decision packet §4 raised the *same* question — "what makes the boss a STABLE graded outcome, not a DPS-race step?" — with two options: grade on clear-time, or add a player-death channel. **The typed wave already shipped the player-death channel for solo.** The heavy-slow telegraphed signature slam answers the proxy case too: it evaporates army *and* threatens the caster, who must dodge/resist/tank/reposition. So **one encounter model — build-floor + dodge-ceiling, telegraphed signature slam — is the unified answer to both the solo §3.4 firm-up and the proxy §4 grading.** That is the convergence. It **unsticks the proxy §4 design question without authorizing the proxy build** (still a separate ~4-wave extension, Matt-gated).

## What this unblocks / what stays gated

- **Closes (as a design disposition):** the soft-median watch-item. Disposition = build-floor measured correctly; firm-up = complete the ceiling, not re-tune the floor; floor co-viability PARKED (Matt fork above).
- **Unsticks (design-only):** proxy §4 encounter-model question — same model answers it.
- **Names the build gate:** dispatch 4 (star-lord serialize TelegraphSpec + i_frame_window) + a Godot combat loop (dispatch 5 prerequisite). Both deferred behind Godot reaching combat.
- **Stays Matt-gated (unchanged):** proxy architecture call + ~4-wave build; content emission (`_DEFERRED_PROXY_BINS` lift, 25% proxy); all push (Mac per-cycle ask).
- **gandalf owns** the dodge-ceiling design contract when Godot combat lands (the multi-answer feel-tuning is a presentation-layer validation beat, not a sim re-tune).
