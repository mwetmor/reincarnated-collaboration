# Matt — Decision Needed (the human-in-the-loop queue)

**STATUS:** LIVING QUEUE — born 2026-06-30 (Matt: *"another folder … titled 'matt_decision_needed' where I can quickly check before session start/end moments"*).
**Maintained by:** gandalf + knight-rider (any agent may surface a row; gandalf/KR curate). **Ruled by:** Matt.

---

## What this is (and is NOT)

This is the **decision queue** — the short list of things **waiting on Matt specifically.** Glance here at session start/end.

- **This queue = what MATT owes the work** (decisions gated on his ruling).
- **The `current-to-end-state/` trackers = what the WORK owes the spec** (build/story/game deltas). Different ledger.
- **jack-ryan-gated or KR-gated items do NOT belong here** — only decisions that genuinely need *Matt*.

**How it flows:** any agent surfaces a Matt-gated decision as a row (pointer to fuller context — a tracker PART-B row, an ARCHITECT doc, a gap). Matt rules → the row is **struck with date + ruling** and swept to the RESOLVED appendix (never silently deleted). The **ARCHITECT role** (`gandalf.md § 2`) is the primary feeder: its open-questions gate surfaces undecided forks *here* before a long run is authorized.

---

## THE QUEUE (open — waiting on Matt)

| # | Decision needed | Why it's on Matt | Source / context | Surfaced |
|---|---|---|---|---|
| **Q2** | **Story flag B1 — run-persistence contract.** What survives a run vs. resets (Hall accumulation, home-realm progress, cult standing)? The death-faith "die and rise" loop needs its persistence rules. | frame-defining; awaiting Matt per the story tracker | `current-to-end-state-story.md` PART B / B1 | 2026-06-30 |
| **Q3** | **Story flag B2 — molt → run-trigger equivalent.** Path Pure's "first molt returns as your first companion" was built on the retired per-season cadence. What's the run-model trigger that unlocks the past-self companion? | frame-defining; awaiting Matt | `current-to-end-state-story.md` PART B / B2 | 2026-06-30 |
| **Q4** | **Story keystone [OPEN] cluster (B4 + B5).** The demigod warm-then-recede tragedy-phase (deliberate arc, or punctuated-neutral?) + the manufactured-rebellion reveal sequence / what the demigod *wants* / how the player learns the cage is manufactured. | Matt's own keystone [OPEN] tags | `reap-die-rise-story/story-keystone.md § 19.1`; `current-to-end-state-story.md` B4/B5 | 2026-06-30 |

*(Q2–Q4 are the story-session decisions already OPEN in the story tracker — surfaced here so they're visible at a glance, not buried in a tracker PART. They're story-session-shaped, not urgent blockers.)*

---

## RESOLVED (struck, with ruling — kept as lineage)

- ~~**2026-07-01 — Q5 fit-audit slate (7 mechanism verdicts).**~~ ✓ RULED **"Agreed"** — all 7 rows ratified, **with one refinement (load-bearing):** *"the grimoire is only a listing of who you've been, you can't use them like a hall."* → the merged Grimoire is **two-register**: **claimed souls = usable/summonable** (§11 capture-and-summon, §13 temporal summoning stand); **own past selves = LISTING-ONLY** (memorial record — never summonable/deployable). Cascades: A9 companion-sourcing ("Hall-sourced past self") superseded — a companion, if B3 ships one, is **claimed-soul-sourced**; B2's molt-return-as-companion premise dies (the molted form feeds the *listing*, not the party). Captured: story-tracker A11 + SESSION-DELTA 2026-07-01.
- ~~**2026-07-01 — Q6 purge process (b)→(b′).**~~ ✓ RULED **"Agreed"** — default-delete with 3 exemptions (E1 ruling-carrier harvest / E2 live-cited move+re-point / E3 spec-member); move-whole legitimate; distillation pull-based; batch ref-scan replaces per-doc capture-checks; specialist confirmation = silence-is-consent lists. Consultant memo §5/§7 is the governing spec.

*(Born 2026-06-30. Resolved rows land here with date + Matt's ruling; truly-dead rows eventually go to git.)*

- ~~**2026-06-30 — GAME tracker name.**~~ ✓ RULED: `current-to-end-state-game.md` (Matt: *"agreed: current-to-end-state-game"*). Stood up 2026-06-30.
- ~~**2026-06-30 — Q1 Perception-asymmetry F2 hinge (telemetry-only vs model-in-sim).**~~ ✓ RULED **symmetric-sim + control-layer edge** (Matt: *"the battle sim should be tuned where player and enemy combatants have the same AOE radius — neither has an edge. When the player is controlling a combatant in the game, that is when the edge is granted (and AI/enemy controlled combatants conversely have a reduced edge)."*). Decisively the layer-handoff family (branch d). **Implications:** (1) sim resolves AOE symmetrically — no 1.12/0.90 constants in `spatial_engine.py`; (2) the perceptual edge is a **piloted-Godot layer-handoff** (drax future-scope, sibling to `dodge_gated_deferred`), **controller-keyed** (human-piloted vs AI-piloted) not role-keyed — supersedes brief §2/§5; (3) §6 WR-falsifier re-homes to the piloted layer (human-piloted vs AI-piloted gap), NOT the headless gauntlet; (4) F3/F6 moot, run unblocked (no rogue-chain dependency). **F2′ (producer home under symmetric sim):** sim emits `AoeCastEvent` with `apparent = true` (spillover 0 = honest "no edge here"); `apparent ≠ true` telemetry is the piloted-layer handoff. Fire-ready brief handed to KR. Constants stay in `foundation/perception_asymmetry.py` as the spec the piloted layer consumes.

---

---

**Sibling instrument:** `agentic_orchestration/architect-effectiveness-ledger.md` — the ARCHITECT-role **foresight-quality** ledger (jack-ryan scores gandalf's ARCHITECT passes against what runs actually hit; recurring misses → new rules). This queue tracks the *decisions*; that ledger tracks *how well they were foreseen*. Both are session start/end reads.

**Signed:** gandalf, 2026-06-30. The trackers say what the work owes. This says what the work is waiting on *you* for.
