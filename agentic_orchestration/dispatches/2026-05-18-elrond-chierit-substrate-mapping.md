# 2026-05-18 — elrond — Chierit substrate mapping (Lightning Ronin + Light Valkyrie)

**Authority:** Matt L3 acquisition 2026-05-18 — both chierit packs purchased + staged; closes #138 monster acquisition gaps (lightning + holy substrates).
**Type:** Pattern A — scout + manifest mapping + drax handoff brief; ~30-45 min.
**Predecessor:** Matt confirmed packs on disk; elrond v1.9 WSP curation complete (you're free).
**Status:** 🟢 **ACTIVE — fire immediately.**

---

## Why this matters

Drax v1.14 monster expansion closed water + wind substrate gaps but **lightning + holy non-boss tiers stayed RED**. Matt acquired chierit Elementals series (CC-BY 4.0 chierit attribution) to close them: **Lightning Ronin → lightning substrate enemy slot**; **Light Valkyrie → holy substrate enemy slot**. Both packs staged at `/Users/admin/Games/reincarnated-demo/public/assets/chierit/lightning_ronin/` + `chierit/light_valkyrie/` (also mirrored under `characters/`).

This is a clean substrate-gap close + closes #138. Your mapping → drax wiring dispatch (queued; lower priority than mobile chain).

Cross-reference flag: drax v1.16.2 holy VFX investigation noted **Light Valkyrie `atk.png` GPU upload timing** as the next investigation target if holy black-rect persists. Note in your handoff brief so drax can investigate during wiring if relevant.

---

## Required reading

1. **Drax v1.14 monster expansion completion** — `agentic_orchestration/dispatches/2026-05-17-drax-v1-14-monster-expansion-wiring-queued.md` § completion (established monster-sprite wiring pattern; 6 monsters wired; pattern for new additions)
2. **Your prior monster-subset manifest** — `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` (existing structure; you'll extend with 2 new rows)
3. **Monster coverage matrix** — `agentic_orchestration/research/curated/monster-coverage-matrix-vs2a-2026-05-17.md` (gap analysis; identifies which tier these fill)
4. **Chierit packs on disk** — `/Users/admin/Games/reincarnated-demo/public/assets/chierit/lightning_ronin/` + `chierit/light_valkyrie/` (verify contents + animation states)
5. **Existing chierit-wired monsters** — Metal Bladekeeper + Leaf Ranger (wiring pattern reference per drax v1.16.2 note)
6. **Drax v1.16.2 holy VFX note** — `agentic_orchestration/dispatches/2026-05-18-drax-v1-16-2-audio-still-broken-plus-holy-vfx-black-rect.md` § completion (Light Valkyrie atk.png GPU upload timing flag)

---

## Scope — three deliverables

### Deliverable 1 — Pack content audit

For each pack, inventory:
- All animation files present (per chierit naming: idle, run, jump, roll, dash, 1_atk, 2_atk, 3_atk, sp_atk, air_atk, defend, take_hit, death)
- Frame dimensions (PIL-measured if needed; don't trust naming)
- Elemental Mode variants present (e_idle, e_run, e_atk*, transform, back2human) — Matt acquired Full tier ($7.50 Lightning Ronin + $12 Light Valkyrie) so these should be present
- Any missing/extra animations vs chierit standard
- License attribution string: "chierit" (CC-BY 4.0 mandatory)

### Deliverable 2 — Monster manifest mapping

Extend `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` with 2 new rows:
- **Lightning Ronin** → lightning substrate; tier recommendation (elite vs mini-boss; you decide based on coverage matrix gap); priority rating
- **Light Valkyrie** → holy substrate; tier recommendation (likely elite or mini-boss given Light Valkyrie's 25-animation set + flight implication); priority rating

For each row include: pack_path, animation_states_present, frame_dimensions, canonical_substrate_mapping, threat_tier_recommendation, scale_estimate, attribution_credit, notes

### Deliverable 3 — Drax wire-in handoff brief

Brief block at the end of your manifest or as separate file capturing:
- Where in `monsterSprites.ts` to add (existing chierit wiring pattern reference)
- Per-monster atlas-load + animation-state-map snippets
- Substrate routing entry (which tier slot each fills)
- Elemental Mode transform handling — note if Matt wants this wired now (Phase-2 polish) or skipped for VS2a
- Light Valkyrie atk.png GPU upload investigation — drax v1.16.2 flagged as next holy VFX investigation target; embed reference + recommend drax verify atk.png file path + check for texture preload opportunity
- Attribution credit addition to `credits.txt`: "chierit (Lightning Ronin + Light Valkyrie) — CC-BY 4.0"
- Test plan: spawn an encounter that should include these monsters; verify render + animation cycle

---

## Acceptance criteria

- [ ] Pack content audit complete (both packs)
- [ ] Manifest extended with 2 new rows
- [ ] Tier recommendation justified (which gap each fills in coverage matrix)
- [ ] Drax wire-in handoff brief authored
- [ ] Elemental Mode handling recommendation included (wire now vs Phase-2)
- [ ] Light Valkyrie atk.png cross-reference for drax v1.16.2 holy VFX flagged
- [ ] Attribution credit string ready for credits.txt
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `elrond/v1.10-chierit-substrate-mapping-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT wire the monsters yourself (drax seam; separate v1.20 dispatch)
- ❌ DO NOT preprocess sprite files (drax does PIL alpha if needed)
- ❌ DO NOT pre-empt drax v1.18 WSP wire-in or mobile audit
- ❌ DO NOT touch other monster manifest rows
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** drax v1.18 WSP wire-in (in flight; different repo)
- **Triggers downstream:** drax v1.20 chierit monster wiring (queued post-this; lower priority than mobile chain)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 chierit acquisition + #138 closure. ~30-45 min. Append completion record + manifest path when done.*

---

## Completion record — elrond/v1.10-chierit-substrate-mapping-1

**Completed:** 2026-05-18 by elrond. Tag `elrond/v1.10-chierit-substrate-mapping-1` (local; no push per ADR-006).

**Acceptance criteria — all met:**
- [x] Pack content audit complete (both packs, PIL-measured)
- [x] Manifest extended with 2 new rows
- [x] Tier recommendation justified (mini-boss for both; rationale in manifest `_tier_justification` field + handoff brief § 1)
- [x] Drax wire-in handoff brief authored (`chierit-monster-wire-in-handoff-brief-2026-05-18.md` — 9 sections)
- [x] Elemental Mode handling recommendation included (DEFER to Phase-2 — handoff brief § 4)
- [x] Light Valkyrie atk.png cross-reference for drax v1.16.2 holy VFX flagged (handoff brief § 5)
- [x] Attribution credit string ready (existing creditsOverlay.ts CREDITS[0] umbrella; supplemental Monster-tier credit recommended — handoff brief § 6)
- [x] PRE-SIGNAL § 14.1.1 before hive-log append (git fetch + tip verified at b40fc78 + status checked)
- [x] AGENT_STATE STATE entry (research/curated/AGENT_STATE.md)
- [x] Tag `elrond/v1.10-chierit-substrate-mapping-1`

**Deliverables:**
1. `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` (EXTENDED — addendum-meta + 2 monster rows appended)
2. `agentic_orchestration/research/curated/chierit-monster-wire-in-handoff-brief-2026-05-18.md` (NEW — drax v1.20 consumption-ready)

**Coverage matrix impact:**
- lightning: YELLOW (palette-shifted mini-boss only) → GREEN (native mini-boss + 2-deep coexistence)
- holy: YELLOW (boss only) → GREEN (mini-boss + boss tier-progressive ladder)
- #138 closed

**Hive log:** STATE entry appended at `agentic_orchestration/hive-mind/phase-1-p1-log.md` ([2026-05-18] STATE — elrond — chierit substrate mapping COMPLETE), preceded by PRE-SIGNAL § 14.1.1.

**Handoff → knight-rider:** ready for drax v1.20 chierit-monster-wiring dispatch when mobile chain clears. elrond ready for Tier 5.1/5.2 final curation pass per knight-rider PRE-SIGNAL.
