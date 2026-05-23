# Request to knight-rider — Canonical Epoch-Stamping Pass

**From:** gandalf (story-and-design steward)
**To:** knight-rider (orchestrator)
**Date:** 2026-05-23
**Authority:** Matt 2026-05-23 — documentation-cleanup pass approved (this morning's session) + cleanup sequencing confirmed
**Companion artifacts:**
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D1-D10 lock)
- `canonical/00-ground-state.md` (oracle, just authored)

---

## 0. TL;DR

Fire a **sub-agent dispatch** to perform a **mechanical epoch-stamping pass** across `canonical/*.md` and `canonical/story/*.md`. Each doc gets a single STATUS header stamp per the rubric below. Bounded scope, single pass, no recurring engagement, ~1-2 hours wall. Goal: agents reading `canonical/story/` after this pass can immediately tell whether a doc is CURRENT, HISTORICAL-INFORMATIVE, or DEAD — without re-walking the full archive.

**This is documentation hygiene. It is NOT a hive-mind workstream. It does NOT touch substrate, telemetry, engine code, or per-agent working dirs.**

---

## 1. Why fire this now

- Hive-mind is IDLE / CHECKPOINTED post-Cycle 8 — bandwidth fully available
- D1 (accept 89.8% vs Wave-4) is awaiting Matt; bandwidth not yet committed downstream
- `canonical/00-ground-state.md` just landed — it names current/historical/dead categories, and `canonical/story/` docs need stamps that match for the oracle to be useful at read time
- Agent-slowdown problem (diagnosed this morning) won't resolve until the stamps land

## 2. Scope (explicit, do not expand)

**IN SCOPE:**
- `canonical/*.md` (numbered top-level docs: 09, 16, 16a, 16b, 17, 19, 28, 29, 30, 31, 32, 33, 34, 35, 36, both 37s, 38, plus README and 00-ground-state)
- `canonical/story/*.md` (~104 docs as of 2026-05-23)

**OUT OF SCOPE (do NOT stamp):**
- `agentic_orchestration/` (per-agent working dirs — knight-rider, gandalf, jack-ryan, rocket, gamora, star-lord, drax, elrond, galadriel, legolas dirs; dispatches; logs)
- `~/Games/reincarnated-engine/` (engine repo)
- `~/Games/reincarnated-demo/` (demo repo)
- `~/Games/reincarnated-loadout/` (loadout repo)
- `agentic_orchestration/skill_handoff_*.md` (these are temporally indexed; consolidation is a separate later pass)
- `canonical/story/archived/` (already archived; no stamping needed)
- Memory files (`~/.claude/projects/.../memory/*.md`)

## 3. The rubric (apply mechanically)

Each doc gets exactly one stamp. Categories:

### 3.1 CURRENT (load-bearing, top-of-stack)

A doc is CURRENT if **any** of these hold:
- Listed by name in `canonical/00-ground-state.md` Section 1 (Current Truth table)
- Authored or last-revised on 2026-05-22 or 2026-05-23 AND not superseded by another doc on those dates
- Engineering disciplines, decisions log, governance, review process (these are always CURRENT regardless of date)

**Stamp format:**
```markdown
> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`
```

### 3.2 HISTORICAL-INFORMATIVE (consult for lineage only)

A doc is HISTORICAL-INFORMATIVE if **all** of these hold:
- Dated before 2026-05-22 (any 2026-05-08 through 2026-05-21 timestamps)
- NOT on the CURRENT list in `00-ground-state.md`
- NOT building on a DEAD pattern (see 3.3)

This is the **default category** for pre-2026-05-22 docs that aren't dead.

**Stamp format:**
```markdown
> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth
```

### 3.3 DEAD BRANCH (do NOT consult as current truth)

A doc is DEAD if **any** of these hold:
- Primary framing builds on **pure-auto-combat** as the game's execution model
- Primary framing builds on **mobile-first** as platform strategy
- Primary framing builds on **non-humanoid playable forms** as standard
- Primary framing builds on **monthly cadence** as the term (vs "seasonal")
- Primary framing builds on **Pattern 4** (pre-imposed aesthetic-tuple dimensions)
- Primary framing builds on **Pattern 5** (15-entry gear catalogue as the substrate)
- Primary framing builds on **Pattern 6** (pre-imposed canonical axes)
- Primary framing builds on **form-bias-diagnosis as the core engine problem** (superseded by substrate-as-cohesion)
- Primary framing builds on **W0.7-framework ablation cycle** as forward work (closed 2026-05-22)
- Primary framing builds on **single-product engine-equals-game** (Variant A; superseded by Variant C)

If a doc *mentions* a dead pattern but doesn't *build on it as primary framing*, that's HISTORICAL-INFORMATIVE, not DEAD. The test is: does removing this dead pattern collapse the doc's central argument? If yes → DEAD. If no → HISTORICAL-INFORMATIVE.

**Stamp format:**
```markdown
> **STATUS:** DEAD BRANCH (primary framing superseded — [name the superseding commitment, e.g., "Variant C lock 2026-05-22" or "D2 variable-execution lock 2026-05-23"]) — do NOT consult as current truth. See `canonical/00-ground-state.md`
```

## 4. Where to place the stamp

Insert the stamp **immediately after the document's first `# Title` line** and before the existing metadata block (Status / Author / Date). If a doc already has a `> **STATUS:**` line at the top, *replace* it with the new stamp rather than duplicating.

Example before:
```markdown
# 09 — Geometry Palette Discussion

**Status:** Active, captured 2026-05-08
**Author:** ...
```

Example after:
```markdown
# 09 — Geometry Palette Discussion

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** Active, captured 2026-05-08
**Author:** ...
```

The original metadata block stays untouched. The stamp is additive.

## 5. Pre-classified seed list (do not re-evaluate these)

To reduce sub-agent decision load and ensure consistency with `00-ground-state.md`, here is the explicit pre-classification for docs already known. Apply these directly without re-evaluating.

### 5.1 CURRENT (apply CURRENT stamp directly)
- `canonical/00-ground-state.md` (already itself; stamp anyway with note "this doc is the oracle")
- `canonical/38-downstream-delivery-strategy-2026-05-23.md`
- `canonical/37-engine-and-game-two-products.md`
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md`
- `canonical/story/gear-heavy-promotion-2026-05-22.md`
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md`
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md`
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md`
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md`
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md`
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`
- `canonical/story/style-register.md`
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md`
- `canonical/story/substrate-design-supplement-2026-05-21.md`
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md`
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md`
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`

### 5.2 HISTORICAL-INFORMATIVE (apply HISTORICAL stamp directly)
- `canonical/29-design-overview.md`
- `canonical/16-project-roadmap.md`
- `canonical/16a-roadmap-shipped-log.md`
- `canonical/16b-roadmap-archive-restructures.md`
- `canonical/28-engine-arpg-rebalance-design.md`
- `canonical/30-engine-explainer-current.md`
- `canonical/31-engine-explainer-future.md`
- `canonical/32-progression-design.md`
- `canonical/33-progression-skeleton.md`
- `canonical/35-stage-a2-cli-prompt.md`
- `canonical/36-b14-5-cli-prompt.md`
- `canonical/09-geometry-palette-discussion.md`
- `canonical/17-gear-and-spirit-guide-design.md`
- `canonical/19-llm-call-map.md`
- `canonical/34-monster-design-phase0-vs-production.md`
- `canonical/README.md`

### 5.3 DEAD BRANCH (apply DEAD stamp directly)
- `canonical/37-form-bias-diagnosis-and-recovery.md` — superseded by substrate-as-cohesion architecture; form-bias framing is no longer the engine's core problem
- `canonical/story/form-bias-cadence-strategy.md` — same superseding commitment

### 5.4 Everything else in `canonical/story/`
Apply the rubric in Section 3. **Default to HISTORICAL-INFORMATIVE** unless the doc clearly meets a DEAD criterion. When in doubt, choose HISTORICAL-INFORMATIVE — false-historical is recoverable; false-dead is not.

## 6. Sub-agent execution protocol

Knight-rider, when firing the sub-agent:

1. **Single sub-agent call.** Do not chain or parallelize across multiple sub-agents — the cross-doc consistency is more important than wall-time.
2. **Read this request doc first.** The sub-agent must read this dispatch verbatim before touching any canonical doc.
3. **Read `canonical/00-ground-state.md` second.** This is the authoritative source for the CURRENT list.
4. **Process docs in order:** numbered `canonical/*.md` first (more important, smaller set), then `canonical/story/*.md` alphabetically.
5. **One commit at the end.** All stamps land in a single commit titled `docs(canonical): epoch-stamping pass per gandalf request 2026-05-23`. Do NOT commit per-doc — too noisy.
6. **Report-back format:** sub-agent returns a single summary with counts (X CURRENT, Y HISTORICAL-INFORMATIVE, Z DEAD) and a list of any docs it couldn't categorize confidently (those default to HISTORICAL-INFORMATIVE but are flagged for gandalf spot-check).

## 7. Acceptance criteria (gandalf-side spot-check)

Once the sub-agent returns:

- All docs in `canonical/*.md` and `canonical/story/*.md` have exactly one STATUS stamp
- Pre-classified seed list (Section 5) is matched correctly
- Counts roughly: ~20 CURRENT, ~80 HISTORICAL-INFORMATIVE, ~5 DEAD (rough ratios; actual numbers may vary)
- No false-DEAD stamps (gandalf will spot-check by reading any flagged-DEAD doc and confirming primary framing collapse)
- No `agentic_orchestration/` or repo-code dirs touched

If spot-check passes, the cleanup pass is done. If spot-check finds errors, gandalf returns the diffs and knight-rider fires a corrective pass.

## 8. What this enables (downstream)

Once stamps land:
- Agents reading any `canonical/story/` doc immediately know its status from the header
- `canonical/00-ground-state.md` becomes load-bearing at read time (cross-references actually disambiguate)
- Onboarding-list shrink (next cleanup step) can proceed with confidence — jack-ryan can prune Phase-1 read lists knowing the underlying docs self-identify
- The agent-slowdown problem starts resolving on the next agent invocation

## 9. What NOT to do

- Do NOT rewrite or refactor any doc content
- Do NOT delete any doc
- Do NOT move docs between directories
- Do NOT touch `agentic_orchestration/`, the engine repo, demo repo, or loadout repo
- Do NOT commit per-doc — single end-of-pass commit only
- Do NOT escalate to Matt during execution unless a categorically ambiguous doc surfaces that the rubric can't resolve (gandalf takes those calls, not Matt)

---

**Signed:** gandalf (story-and-design steward)
**For:** knight-rider's sub-agent dispatch to perform the canonical epoch-stamping pass per the rubric above, bounded to `canonical/*.md` + `canonical/story/*.md`, single-pass, single-commit, with gandalf-side spot-check acceptance.

**Next gandalf action after acceptance:** coordinate with jack-ryan on onboarding-list shrink in agent definitions (working-agreement edit).
