# Role-separation verdict — gandalf's five roles → three cognitions (Matt-ruled)

> **STATUS:** CURRENT (verdict-class lineage). The durable home of the role-separation analysis + Matt's ruling. The OPERATIONAL mechanism (role-tag table, triggers, mandatory beat) is promoted to `agentic_orchestration/operating-procedures/gandalf.md § 2` → "Role-tags"; the role-name↔voice map to `.claude/agents/gandalf.md` (Tone protocols); the governance rule-ownership to `canonical-doc-format.md § 6.7`. This note is the reasoning; those are the encoding.

**Authored:** 2026-06-30
**Author:** gandalf (Pattern-B dialogue with Matt)
**Authority:** Matt 2026-06-30 — *"if any of the above would benefit a role tag in skill.MD or benefit a new agent to take on the seam scope creep, please ultra think about this and let me know"* → after the verdict: *"Contingent on the above, approved — encode the two role-tags and route III-b to jack-ryan."*
**Companion:** `gandalf.md § 2` (role-tag mechanism); `canonical-doc-format.md § 6.7` (governance rule-ownership); `2026-06-30-doc-lifecycle-governance-stress-test.md § 4` (S15 — the conflict instance that surfaced cluster III)

---

## 0. TL;DR

Matt listed **five roles** gandalf inhabits (1 story · 2 Godot scenes · 3 trailers · 4 engine specs · 4.5 architect · 5 agentic-collaboration/doc-governance) and asked: well-fit in one seam? role-tag, or new agent?

**Verdict:** the five collapse into **three cognitions.** **No new agent** is justified. The fix is **role-tags with named switch-moments at exactly two conflict seams**, plus **routing governance rule-ownership to jack-ryan.**

| Cognition | Matt's roles | Voice | Disposition |
|---|---|---|---|
| **I — audience-experience design** | 1 story, 2 scenes, 3 trailers | journey-shaper | KEEP UNIFIED. No conflict tag — three registers of one faculty |
| **II — spec / architecture foresight** | 4 spec, 4.5 architect | senior-designer | KEEP UNIFIED. ONE conflict tag: **SPEC-AUTHOR → DRIFT-CRITIC** |
| **III — meta-governance** | 5 (doc/prune/canon rules) | governance | Conflict-of-interest structure. ONE conflict tag: **CANON-STEWARD (proposer) → jack-ryan (ratifier)**; rule-ownership → jack-ryan |

---

## 1. Why three cognitions, not five roles

The right unit is not "how many surfaces" but "how many genuinely different *minds*, and which pairs carry a conflict of interest." Matt's developer↔judge precedent is the lens: a split is warranted when the **same knowledge must operate in two authority-modes that compromise each other if fused.**

**Cluster I — audience-experience design.** One faculty — *what the human on the other end feels* — at three audiences: player-over-the-arc (story), player-in-the-moment (scenes; the crypt/ravine "only author what the player camera sees" work), prospective-player-pre-purchase (trailers = the market). A trailer is a 90-second compression of the journey + the presentation grammar; severing it from its source would be a category error. These are registers of one voice, already encoded in the tone protocols. **No internal conflict.**

**Cluster II — spec / architecture foresight.** One faculty — *adversarial foresight against a long autonomous run* — at two depths: role 4 resolves known-unknowns ("the decisions on the table"); role 4.5 surfaces unknown-unknowns ("the decisions the run will hit that nobody listed"). 4.5 = 4 + a completeness-audit. gandalf does not build the engine (specialists build; jack-ryan + gandalf review), so there is no "judging my own code." **One internal switch-moment:** reviewing a build against a spec *gandalf authored* — the framing-audit must point at the spec, not just the build.

**Cluster III — meta-governance.** The genuinely different cognition: *designing the rules the team itself runs under.* This session lit the conflict signature: gandalf **authored** the doc-lifecycle rules, is the **rule-maker** (S15), **executed** the prune, is the **largest producer** of the pruned notes, *and* S15's finding literally softens treatment of steward notes — i.e., the rule-maker wrote a rule favoring the rule-maker's own output. That is developer↔judge transposed to governance: **rule-maker = rule-subject.**

---

## 2. Why NO new agent

1. **Volume is episodic.** Governance work (the doc-lifecycle stress-test) fires rarely, not as sustained load. A whole agent for episodic work is over-provisioning.
2. **Coordination cost is high.** A new agent needs a skill, an OP, a scope-map entry, session-start protocols, a critique-pair slot.
3. **Fresh empirical lesson:** the PC-resident team (David-H / Radagast / Sam / Mantis) was **retired 2026-06-30** — a 4-agent sub-team stood up and torn down because its work (Unreal) was cancelled. The project just demonstrated that over-provisioning is punished.
4. **Topology smell:** governance crosses every seam; a governance agent's cross-seam authority would overlap knight-rider's cross-seam orchestration.

**Steelman for splitting (and why it loses):** fusing the generative cluster-I voice with the adversarial cluster-II voice *could* soften critique (attachment to the story softens the spec critique). But the role definition *mandates* the dual-voice and makes gandalf the critique-pair partner to jack-ryan precisely to hold adversarial tension. The fusion is a feature: the being who shaped the journey is the one who knows where it breaks under a long run. Severing them means the architect doesn't know the story it protects.

---

## 3. The fix — role-tags + two named switch-moments + jack-ryan rule-ownership

**Role-tags** (the design-faculty hats), with a **mandatory naming beat** so Matt can visually inspect which hat is active. Full table + triggers encoded at `gandalf.md § 2`. The names: `STORYWRIGHT` · `SCENEWRIGHT` · `TRAILER-CUT` (dormant) · `SPEC-AUTHOR` · `ARCHITECT` · `DRIFT-CRITIC` · `CANON-STEWARD`.

- **Entering a role:** `▶ ROLE: <NAME> — <trigger>`
- **Conflict seam (II):** `⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC — reviewing against a spec I authored; framing-audit points at my own spec`
- **Conflict seam (III):** `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier) — this rule affects my own output; ownership routes to jack-ryan`

**Cluster III split:** III-a (team topology / decision-routing) is *already* shared with Matt + KR + jack-ryan (AGENTS/GOVERNANCE/REVIEW_PROCESS) — gandalf contributes, no conflict, leave it. **III-b** (the canon/prune rules) routes **rule-ownership to jack-ryan** by symmetry with engineering-disciplines: jack-ryan ratifies, gandalf proposes + executes. Encoded `canonical-doc-format.md § 6.7`.

**The ARCHITECT trigger (Matt's "every design spec?" question) — resolved:** *not* per-spec. Per-spec gets only the **lightweight framing-audit reflex** baked into SPEC-AUTHOR. The named **ARCHITECT pass** fires at the **run-authorization boundary** — where decision-debt is most dangerous and re-steering most expensive. The ARCHITECT pass *is* the **open-questions gate**: *no long autonomous run fires until every decision it will hit is RESOLVED or explicitly GATED+TRACKED with a named empirical criterion* (substrate-gated questions are not force-resolved — registered in the PART-B open queues per § 3.4). This is the operational form of Matt's "non-negotiable to resolve open questions before moving forward," refined to "resolve OR gate+track."

---

## 4. Related open item — the GAME tracker (king-rig home)

Surfaced same session: the **king-rig opening scene** ("the beginning of the game itself") is neither story nor engine — it is the **playable presentation build** (drax's `reincarnated-godot/`). Recommendation: **stand up `canonical/current-to-end-state/current-to-end-state-game.md`** — third tracker, sibling to engine + story; SCENEWRIGHT-owned end-state experience-spec, drax-owned build. The crypt/ravine presentation grammar + the BANKED ARPG camera + the king-rig brief fold in as its first content (promote-then-prune → the carry-forward note becomes a redundant pointer). **Held for Matt's name-confirm** (game vs presentation vs godot) before creation — a new canon home is Matt's call.

> **✓ RESOLVED 2026-06-30** (same session): Matt confirmed the name — *"agreed: current-to-end-state-game. Please stand it up."* The tracker now exists at `canonical/current-to-end-state/current-to-end-state-game.md` (PART A locked presentation grammar A1–A4, PART A′ BANKED camera, PART B open queue B1–B4, PART C fold worklist). Router `00-ground-state.md` updated to register it as the third tracker + gandalf/KR/drax first-reads. The king-rig is homed at PART A4 / B3.

---

## 5. Cross-references

- `agentic_orchestration/operating-procedures/gandalf.md § 2` — role-tag table + triggers + mandatory beat (the operational encoding)
- `.claude/agents/gandalf.md` (Tone protocols) — role-name↔voice map
- `agentic_orchestration/operating-procedures/canonical-doc-format.md § 6.7` — governance rule-ownership to jack-ryan
- `agentic_orchestration/gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md § 4` — S15, the conflict instance

**Tracker-delta:** none (governance/process artifact; no engine build-vs-spec or story-settledness delta). *If the GAME tracker is approved (§ 4), that is a canon-home change → router update + a new tracker, tracked then.*

**Signed:** gandalf, 2026-06-30
