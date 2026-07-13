# Skill handoff — 2026-07-13

Continuity doc for the next knight-rider session. What shipped, what's queued, what's blocked, what's flagged for Matt.

---

## ⭐⭐ WAVE-A BUILT + GATE-2 PASSED — awaiting ONLY Matt's push (4 unpushed commits, engine `main`)

KR orchestrated all 4 slices directly via sub-agents (no launch-commands handed to Matt — Matt directive "sub-agent orchestration is your seam"). Serialized on the shared engine working tree; gate lifted LAST.

**The stack (4 commits, tagged, NONE pushed):**
1. `4a70547` rocket Slice-1 — economy config A1/A2/A4 + C2a dual-address + CoG emission · `rocket/v2.8-wave-a-summon-economy-config-1`
2. `7aeb2a6` gamora Slice-1 — B1 re-summon loop + GX-19 clock + proxy-AI + C1a/C1b calibration; emitted CALIBRATION-READY; calibrated CoG floor share → gap 0.86 · `gamora/v1.7-wave-a-summon-simulation-1`
3. `4fdd314` gamora Slice-2 — ranged-proxy nav fix Q26 (a) boss-focus inheritance ONLY (+ load-bearing ranged HOLD-branch heading re-face, Discipline #12 framed); ranged C1b cert D3/D2 PASS; 38.9m park defect gone · `gamora/v1.7-wave-a-summon-simulation-2`
4. `43fa149` rocket Slice-2 + FINAL — A3 reservation build-true (`regen_cap -= reservation_per_proxy × active_count`) + CoG re-pin 0.86 + `ranged_proxy→ranged_kite` map + **`_DEFERRED_PROXY_BINS = frozenset()` gate LIFT (Wave A ON)** · `rocket/v2.8-wave-a-summon-economy-config-2`

**Gate-2 (jack-ryan DEV-MODE): PASS-with-notes, NO BLOCK, push-ready.** Both gamora-flagged items independently verified at code/grep/smoke: (1) #12 heading re-face confined to ranged hold-branches, melee/turret/emitter byte-identical (8/8 deterministic re-run); (2) E4 spine un-entangled — exactly ONE `_boss_focus_entity` write (setup :1980), nav addition is pure guarded read. Q26 (a)-only (no b/c leak), Q27 A3 build-true (not collapsed into A2), CoG 0.86 traced to gamora's `0.40·0.70+0.25·1.0+0.20·0.9+0.15·1.0=0.86`, gate lift genuinely last + post-cert, round-trip not-applicable-with-reason (C2a contract byte-unchanged; MIGRATION.md Slice-2 entry present). Tags are correct seam-prefix intermediate — no ADR-003 milestone approval triggered.

**→ AWAITING MATT: authorize the Wave-A push** (ADR-006 Matt-owned). Nothing else gates it.

### 🔭 FORWARD-QUEUE ITEM (Gate-2 raised — KR must not lose): A3 sim-reader
A3 ships as **emittable config but NOT yet sim-enforced** (`proxy_vocabulary_bridge.py:288` `economy="reserved"` not-emittable; no live A3 kit; `simulation/` does not consume `reservation_per_proxy`). Safe TODAY (doubly inert). **Risk:** if an A3 kit is authored AND enters S6 cert BEFORE gamora's fight-loop reader lands, the reservation tax is silently ignored → a kit that should be regen-cap-leashed passes D2-dominance unpenalized (Discipline #40 scaffold-to-production). **Action owed:** dispatch gamora's fight-loop reader (`regen_cap -= reservation_per_proxy × active_count` enforcement) BEFORE any A3 kit is authored. Tracked here as named forward-queue item, not just a MIGRATION.md line.

---

## ⭐ TOP — Wave-A (summon/proxy) handoff CLOSED: 3 dispatches authored + Gate-1 cleared + 2 Matt escalations filed

gandalf (SPEC-AUTHOR) handed off the Wave-A engine spec to KR for sequencing + dispatch authoring (`gandalf/design-inputs/wave-a-KR-handoff-2026-07-13.md`; full spec `wave-a-engine-spec-2026-07-13.md`; rulings + evidence alongside). Wave A makes the summon/proxy family shippable in the dev-log catalogue (Matt PAUSE-2 / Q25: **ship all 4 economies**; GX-19 ratified as the Wave-A nucleus; DL-03 streams-never-tax-movement adopted as design law). KR ran the brief to close.

### The load-bearing sequencing call: MELEE-FIRST, two slices
- **Slice 1 (fully authorized, dispatched now):** melee economies A1/A2/A4 + GX-19 absorption clock + C1a/C1b calibration → gate lift → S6 cert at the C1b endgame coordinate (D3-evaporate / D2-dominance as pass/fail rails).
- **Slice 2 (HELD behind 2 Matt escalations):** ranged-summon (behind the nav fix) + the A3 reservation economy (behind the build-true-vs-approximate ruling).
- **Do NOT block all of Wave A on the escalations** — Slice 1 is independent and authorized.

### Dispatches authored (all auto-committed, NOT pushed; Matt owns Wave-A push after Gate-2)
1. **rocket** — `dispatches/2026-07-13-rocket-wave-a-summon-economy-config.md`: economy config A1/A2/A4 + C2a dual-address + CoG emission (§5), then HOLD; A3 (Slice 2, held); `_DEFERRED_PROXY_BINS` lift is the LAST action of the whole wave (only after gamora's calibration token). Cross-seam contract (C2a emission → atlas render + S6) → round-trip clause + MIGRATION mandatory.
2. **gamora** — `dispatches/2026-07-13-gamora-wave-a-summon-simulation.md`: B1 re-summon fight-loop (§3) + GX-19 proxy commitment clock (§4) + proxy-AI behavior-branch map + proximity trigger (§7, melee + volatile_emitter; ranged excluded) + C1a/C1b calibration (§6). Ranged-proxy nav fix (§8) is Slice 2 — gamora SCOPES the fix-shape into the escalation file, does NOT build.
3. **elrond** — `dispatches/2026-07-13-elrond-wave-a-returns-data-corrections.md`: 4 corpus-DB corrections (poe1→le-ring-of-shields re-key; CotA/IK-HotA distinct no-dedup; d2-sacrifice negative=1 KEEP; 9 mint dossiers era_year/patch/URL backfill). **⛔ SUPERSEDED — EXECUTED-VIA-GANDALF-PROMPT.** Matt already launched elrond under gandalf's running prompt, a SUPERSET (Fold 1 = these 4 corrections + Fold 2 = key the 9 mint dossiers into `canon_engine_key` for atlas plotting). **Do NOT launch a second elrond** = would be a double-writer on corpus.db. Dispatch retained for lineage only; elrond is already live.

### Gate-1 (jack-ryan, DESIGN-MODE) — both engine dispatches PASS-with-notes; all 4 punch-list items folded
- Principle-6 dispositions confirmed right (rocket mandatory round-trip; gamora conditional).
- Seam-ownership (`PROXY_TYPE_TARGETING`→`PROXY_TYPE_BEHAVIOR`, gen-decl vs sim-exec): symmetric MIGRATION+escalate note confirmed CORRECT (do NOT pin now — the opposite of the 2026-07-11 double-writer, which failed on *silent* co-writes; here coordination is explicit).
- **Folded edits:** (1) tightened rocket's round-trip escape hatch — atlas is a hard consumer, Wave A doesn't close without the export round-trip proven somewhere; (2) named the gate go-signal a **literal token** `CALIBRATION-READY: _DEFERRED_PROXY_BINS lift authorized` (both dispatches) to close a lift-race; (3) added Discipline #12 semantic-shift citation on the `PROXY_TYPE_BEHAVIOR` widening (both); (4) A4 accumulator cross-fight-vs-within-fight reset made explicit.

### 2 Matt escalations — ✓ BOTH RULED 2026-07-13 → Slice 2 build-authorized (queue rows Q26 + Q27 struck)
- **Q26 — ranged-proxy nav fix-shape → RULED (a) boss-focus inheritance.** Ranged ally adopts the player's boss-focus target rather than chasing nearest-add. gamora builds (a) ONLY; not (b)/(c). Unblocks ranged-summon (Slice 2).
- **Q27 — A3 reservation → RULED build-true.** Permanent regen-cap reservation (`regen_cap -= reservation_per_proxy × active_count`), not spend approximation. Preserves the 4th distinct economy + abandonment-tax inversion. rocket builds spec §2 (a). Unblocks the A3 economy (Slice 2).
- Both engine dispatches updated: Slice-2 sections flipped HELD→build-authorized; escalation file RULING RECORD + queue rows struck to RESOLVED.

---

## Next-session actions (KR-owned)
1. **Relay the launch commands to Matt** for **rocket + gamora ONLY** (elrond is ALREADY LIVE under gandalf's prompt — do NOT launch a second): `cd ~/Games/reincarnated-engine && claude --agent rocket` (or gamora). rocket + gamora serialize on the calibration→lift handoff.
2. **Broker the gate handoff live:** when gamora's completion record carries the exact token `CALIBRATION-READY: _DEFERRED_PROXY_BINS lift authorized`, confirm to rocket that the §9 lift is authorized. This is the one live sequencing point KR must be in the loop for.
3. **Slice 2 is build-authorized** (Q26/Q27 ruled) — sequences behind Slice 1 per melee-first; no longer waits on Matt. rocket: A3 build-true. gamora: ranged nav fix (a) boss-focus inheritance + `ranged_proxy` behavior branch.
4. **Gate-2 (jack-ryan) + Wave-A push** after the slices land (Matt owns the push).

## Carried-forward from 2026-07-12 (still open — not Wave-A)
- **Unit 2 `snap` → `instant` commitment rename** — unblocked (E4 ratified); no dispatch authored yet. Read-compat normalizer mandatory (persisted population carries `bc_commitment: "snap"`).
- **`rime` re-promotion** (D1 vocab pool) — Matt one-word call, gandalf recommends RE-PROMOTE. Not blocking.
- **Q18_FLAVOR_POOL cold/frost re-pass** — drop liquid-only water-register words; follow-on, not a blocker.
- **drax presentation-layer relabel** (`water`→`ice`, `chain_lightning`→`chain` VFX/HUD) — post-engine-landing follow-on.
- **Open story cluster:** Q2/Q3/Q4 (run-persistence contract, companion, keystone) + Q10's one band-time item + rolling Q12.

## Pre-existing dirty working tree (NOT introduced this session)
- Modified: `dispatches/2026-07-12-gamora-water-to-ice-simulation.md`, `…-rocket-water-to-ice-element-LEAD.md` (completion records), `gandalf/views/v1-plane/plane_view_v1_2_stratified.svg`. Untracked: galadriel glance-atlas captures/pipeline, claude-mobile-session-docs, glance/app/public/atlas, matt_notes_handoff_docs prompt file. Left as found — not this session's to commit.
