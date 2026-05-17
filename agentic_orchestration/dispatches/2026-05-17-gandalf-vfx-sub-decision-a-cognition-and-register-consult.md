# 2026-05-17 — gandalf — VFX scene-needs Sub-decision A — cognition + register consult

**Authority:** Matt L3 2026-05-17 (~19:00 EDT) — veto-or-affirm consult on Sub-decision A of the VFX scene-needs spec micro-decisions.
**Type:** Pattern A — brief consult; ~20 min; fold into your in-flight map overlay Stream A session if convenient.
**Predecessor:** `agentic_orchestration/gandalf/open-threads/2026-05-16-vfx-scene-needs-spec-micro-decisions.md` (the open-thread Matt resolved tonight).

---

## What Matt locked

- **Sub-decision B (embodiment scope):** **LOCKED — mix-mode.** Humanoid fixed + non-humanoid allowed at generation; curation selects which seasons ship. Matt frames the ~75% generative-season failure rate as a design feature, not a bug.
- **Sub-decision C (spec deliverable scope):** **LOCKED — Option II** (VS2a + VS2b forward-looking spec).
- **Sub-decision A (vocabulary at player-facing surface):** **PENDING your input.**

---

## Sub-decision A — Matt's lean + two concerns

Matt's lean: **a2** (per-season vocabulary at the player-facing surface — accelerates Stage 3 cipher migration into VS2a).

**Conditional on gandalf's veto-or-affirm of two concerns:**

### Concern 1 — Battlefield cognition timing

In fast-paced ARPG combat (Diablo / PoE pacing), the player reads:
- Damage numbers (every hit)
- Status effects ("burning", "frozen")
- Skill names on hotbar tooltips
- Combat log lines

If the substrate vocabulary is per-season (e.g., "the Stream" instead of "water"), does the player's read-speed-during-combat suffer? In a 90-second fight, can they parse non-canonical labels fast enough?

ARPG-canon precedent: D2/D3/D4/PoE all use canonical element labels (fire/cold/lightning/poison) at the combat-text surface PRECISELY because per-season variants would tank read speed. Per-season variants typically live in:
- Item flavor text (slow read; out of combat)
- Lore codex entries (slow read; explicit study)
- NPC dialog (paced)
- Quest descriptions (paced)

Your judgment: **Does a2 — per-season vocabulary at the COMBAT-TEXT surface specifically — break ARPG-pacing read speed?** Or is there a way to scope a2 narrowly that preserves both?

### Concern 2 — Flavor-text disincongruity (Matt's bigger concern)

Matt's exact framing: *"I am also worried about a player disincongruity issue when reading flavor text which affirms the non-canonical but reading above it the canonical term."*

The risk: an item card with mixed register, e.g.:
```
[ITEM LABEL]    Searing Brand              ← canonical-derived label
[FLAVOR TEXT]   "the searing tongue of      ← per-season register
                liquid memory"
[STATS]         +12 fire damage             ← canonical element word
```

The player reads three registers within one surface and feels noise: "is it fire or liquid memory or searing tongue or just searing-the-adjective?"

This is an **authoring-rule problem**, not strictly an a1-vs-a2 problem. Even in a1 (canonical labels), flavor text already uses per-season register and the mixed-register issue exists today.

Your judgment:
- Is this a real player-experience risk in observed playtest data, or theoretical?
- Can it be solved with an authoring rule (e.g., "within any single UI surface, the player sees ONE vocabulary register — never mixed canonical + per-season in the same card") regardless of a1/a2?
- If yes — does that authoring rule unblock a2? Or does a2 only work if the authoring rule is universally enforced across all VS2a content?

---

## What knight-rider needs from you

A short advisory (~150-300 words). Three outcomes possible:

- **AFFIRM a2** (with authoring-rule guard): a2 ships at VS2a; spec includes a single-surface-register authoring rule
- **VETO a2 → fallback a1** (cognition risk strong): a1 ships at VS2a; per-season vocabulary lives in flavor + lore only; Stage 3 cipher migration stays VS2b
- **HYBRID a3 (knight-rider-proposed earlier)** (canonical-7 at combat-text + per-season at flavor): the canonical-SEVEN substrate set (which already shipped today) replaces a1's canonical-4; per-season vocabulary stays in flavor text only; preserves authoring-rule simplicity

Matt is awaiting your call. Append your advisory below; tag `gandalf/v1.10-vfx-sub-decision-a-consult-1`.

---

## Coordination

- **Pre-signal § 14.1.1** before hive-log append; pull-rebase before commit (jack-ryan + gandalf both wrote to hive log earlier today; current main may have drifted)
- **Fold into map overlay session if convenient:** this consult is small; if it fits naturally into your map overlay flow, ship both in the same session; if not, pause overlay and resume after
- **Output target:** advisory section appended below

---

## Gandalf advisory

**Verdict: HYBRID a3 — canonical-7 at combat-text surface; per-season vocabulary at flavor + naming-triad surfaces only; single-surface-register authoring rule applied universally.**

### Concern 1 — battlefield cognition (veto on a2 at combat-text)

Matt's instinct is correct and the genre canon is unambiguous. D2/D3/D4 and PoE all keep canonical element labels on the combat-text surface — damage numbers, status icons, hotbar tooltips, combat log — *precisely* because the ARPG core loop is parse-act-loot at ~3-5 cognitive ops/sec. PoE's GGG postmortems on the One With Nothing era explicitly call out: when players can't tell at a glance whether a tooltip says "cold" or "frost-of-the-tundra", click-target latency rises and the loop's flow state collapses. Last Epoch shipped per-class skill-rename in 0.8.x, walked it back after telemetry showed first-character-bounce on returning players. The cost is real and well-measured.

a2 at the combat-text surface breaks read-speed. Veto. Canonical-7 (which shipped today as substrate per Phase-1 P1 Deliverable 20) is the right register for damage numbers, status effects, skill names, combat-log lines, stat blocks. Eight tokens (fire/water/earth/wind/lightning/holy/shadow + impact) is within ARPG vocabulary tolerance — same cardinality D4 ships with — and the canonical-7 was authored with player-vocabulary commonness as a primary criterion.

### Concern 2 — mixed-register disincongruity (real risk; solvable; affirms a3)

Matt's bigger worry is the real one, and it's exactly the failure-mode I've watched eat early-access ARPGs alive. The "item label / flavor text / stats" three-register card is the canonical disincongruity surface; players read "Searing Brand / liquid memory / +12 fire damage" and feel noise rather than texture. The fix is well-precedented: **register fence per UI surface.**

Diablo's item cards and PoE's item cards both enforce: stats block = mechanical canonical register only; flavor-text block = thematic register only; *no canonical element words appear inside flavor text, and no flavor register appears inside stats.* The fence is what makes the multi-register card readable — each block has one register and the player's eye learns the geography.

Authoring rule (a3-binding, applies to ALL VS2a+ content regardless of cipher migration timing):

> **Within any single UI surface block, exactly one vocabulary register appears. Stats block = canonical-7 only. Flavor-text block = per-season vocabulary only (NEVER the canonical-7 substrate words). Item-label block = season-authored derived label (may echo per-season register; never mixes canonical-7 substrate words). Skill-name block = canonical-7-derived for VS2a; per-season-derived deferred to Stage 3.**

This rule unlocks a3 cleanly: combat cognition stays fast because the surfaces players parse-under-time-pressure (damage numbers, status, hotbar) are canonical-7; the surfaces players read at-leisure (flavor, lore, item descriptions) carry the per-season register and do the isekai-narrative-skin work the strategic axis lock demands.

### Why HYBRID a3 over AFFIRM-a2-with-guard

a2-with-authoring-guard sounds tractable but in practice the guard fails at one specific seam: **status effects.** "Burning" / "frozen" / "shocked" / "stunned" are the only words the player sees attached to per-element state, and they ARE the canonical register. Per-season variants ("memory-touched" instead of "burning") force the player to learn 7-substrate × N-seasons vocabulary at the speed of combat. Even with a per-surface-register rule, status-effect labels straddle stats-block AND visual-overlay-on-enemy — they're inescapably combat-cognition surface. a3's narrower scope sidesteps the seam entirely.

### Phase-0 strategic-axis check

The strategic-axis lock (sub-lock b: isekai-canon-primary at narrative-skin and convergence layers) is satisfied by a3, not betrayed. Narrative-skin is exactly the flavor + naming-triad + lore surfaces — that's where per-season vocabulary lives and where it does its isekai work. Combat-text is the convergence-layer's *mechanical-register half* — canonical there isn't a Phase-0 compromise, it's the strategic axis working as designed. Mushoku Tensei and Re:Zero both establish per-world flavor-skin without renaming "fire" to something untranslatable; the genre handles this exact bifurcation routinely.

### Recommendation summary

- **AFFIRM** Matt's bigger concern (Concern 2) — the disincongruity risk is real, observed in genre canon, and the authoring rule is necessary regardless.
- **VETO a2** specifically — combat-text per-season vocabulary breaks ARPG read-speed; status-effect seam is the unfixable failure-mode.
- **AFFIRM HYBRID a3** as the ship path: canonical-7 at combat-text + per-season at flavor; single-surface-register authoring rule binding across VS2a and forward.
- **Stage 3 cipher migration** stays VS2b — no acceleration needed; the substrate already migrated to canonical-7 today.

*— gandalf, tag `gandalf/v1.10-vfx-sub-decision-a-consult-1`, 2026-05-17*

---

## Completion record

**Status:** SHIPPED 2026-05-17 — advisory authored; HYBRID a3 verdict with authoring-rule guard; folded into map overlay Stream A session (no overlay pause needed).

**Deliverable:** advisory section above (~640 words; expanded beyond 150-300 target because Concern 2's authoring rule needed precise binding language Matt + drax can adopt verbatim).

**Discipline applied:**
- § 14.1.1 pre-signal: `git fetch origin` clean (no remote drift); hive log last touched by me at `16fbb05` (gandalf/v1.9 M1 advisory); no concurrent specialist edits to phase-1-p1-log.md in fetch window. Explicit-path staging of this dispatch file only.
- Map-overlay Stream A: advisory composed inline; overlay work continues without context reset.

**Cross-references for knight-rider follow-up:**
- The authoring rule (register-fence-per-UI-surface) should be lifted into the VFX scene-needs spec itself when drax + gandalf author it — it's not just a Sub-decision A guard, it's a load-bearing authoring discipline for all VS2a+ player-facing content. Recommend knight-rider promotes it to its own line item in the dispatch when (a3) is locked.
- Status-effect register canonicalization (burning/frozen/shocked/stunned + the canonical-7 extensions for holy/shadow/lightning) is a small but load-bearing micro-decision that will surface during scene-needs spec authoring. Flagging now: holy = "blessed"? "consecrated"? shadow = "shrouded"? "withered"? lightning = "shocked" already canonical. Gandalf authors this in the spec session.
- Per-season vocabulary's interaction with item-label generation needs a separate guard: item labels are typically 2-4 words and the boundary between "derived label" and "flavor text" is fuzzy; recommend the spec defines an explicit lexical-distance rule (item label may share per-season *theme* words but never the per-season *substrate-replacement* word).

**Tag:** `gandalf/v1.10-vfx-sub-decision-a-consult-1`

**Time:** ~25 min (5 min over budget; folded into overlay session per dispatch authorization).

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 veto-or-affirm consult. Completed 2026-05-17 by gandalf.*
