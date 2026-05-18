# 2026-05-17 — jack-ryan — D11 Gate-1 twin advisory (gamora math note + gandalf canonical-17 amendment)

**Authority:** Knight-rider per (1) gamora D11 math note completion record handoff "→ jack-ryan (Gate 1)" + (2) gandalf DoE cascade completion record handoff "→ jack-ryan Gate-1 advisory (3 watchpoints)". Both shipped this evening; both gate downstream code execution.
**Type:** Pattern A — Gate-1 dual review; ~30-60 min total. Advisory-only (no BLOCK at this gate per ADR-007 critique-pair pattern).
**Predecessors:**
- gamora D11 math note: `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md` + tag `gamora/v1.6-d11-hybrid-mage-tuning-math-note-1`
- gandalf cascade: `canonical/32-progression-design.md` § 13 + `canonical/17-gear-and-spirit-guide-design.md` heal-cooldown affix subsection

---

## Why this matters

Two distinct downstream code paths are gated on your Gate-1 advisory:

1. **Rocket D11 implementation** (queued; auto-fires on your D11 math note advisory) — implements gamora's element-coverage damage tax + ceiling 4→3 + balance-loop modifier behavior + post-process salvage of 002011-015 hybrid_mage classes. Your D10 pre-flag pattern (3 pre-flags caught field-level mismatches) prevented field-level bugs at code-time; D11 follows the same pattern.

2. **VS2b heal_ability refactor** (deferred; gates eventual gamora + star-lord + rocket execution of STAMINA_POTION_USE → heal_ability) — gandalf's canonical-17 amendment locked the design contract; the engine-side execution executes post-VS2a. Your Gate-1 advisory on canonical-17 catches contract gaps before code fires.

Both reviews are advisory (Gate-1, not Gate-2). Surface pre-flags + watchpoints; do not BLOCK. Downstream code consumers address pre-flags at code-time.

---

## Review 1 — D11 math note (gamora v1.6)

### Read

1. **Gamora D11 math note** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md` (10 sections + § 0 TL;DR)
2. **Gandalf D11 advisory** (the gen-design source) — `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` (especially § 4 tuning lever + § 8.1 8-item gamora-readiness checklist)
3. **Rocket D10 completion record** — for the empirical anchor (37.1% convergence baseline; hybrid_mage 0.63-0.82 WR)
4. **MIGRATION.md v1.10 entry** — `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (3 new ClassBalanceResult fields; cross-seam contract change)

### Review focus

Apply the D10 pre-flag review pattern:

- **Field-level correctness** — does gamora reference any field name that doesn't exist on the class/skill object as actually structured (the D10 `range_profile` per-CLASS-not-per-skill bug; the `generation_seed` vs `seed` bug)? Inspect at least one D10-curated class JSON empirically.
- **Tax formula consistency** — is `tax_multiplier = 1.0 − α × max(0, n_elements − 2)²` with α=0.07 referenced consistently across all sections? Watch for inadvertent magnitude shifts (e.g., section X uses α=0.07 and section Y uses α=0.10).
- **Tax application point** — is the tax applied at generation-time (gen-math) OR balance-loop-time (sim) OR both? gamora's note should be unambiguous about WHICH part of the pipeline consumes the tax.
- **Ceiling enforcement clarity** — ceiling 4→3 is general; 4-element ceremonial deferred to D12+. Does gamora's note flag the ceremonial path explicitly as out-of-scope, or could rocket misread it as in-scope?
- **R11(b) round-trip clause** — gamora claimed clean (§ 8.2). Verify her reasoning; if she added new output paths or contract changes that she missed, surface it.
- **MIGRATION.md v1.10 contract** — 3 new ClassBalanceResult fields. Are they fully specified (name, type, default, populated-by-which-method)? Star-lord follow-on consumes; gaps here propagate.
- **Salvage strategy R11(b)** — § 6 salvage strategy involves post-processing 002011-015. Does it preserve carried_gear (the D10 bug Matt just hit)? Pre-flag if not.
- **Convergence projection grounding** — § 7 should ground projection in v1.5 Class C sample + D10 empirical baseline. Verify the math; flag if α=0.07 is asserted without empirical anchor.

### Output

Append D11 math note review verdict to gamora dispatch (`agentic_orchestration/dispatches/2026-05-17-gamora-d11-hybrid-mage-tuning-math-note-queued.md`) as "Jack-ryan Gate-1 advisory" section. Verdict format:
- `ENDORSE` / `CONDITIONAL ENDORSE` / `REQUEST AMENDMENT BEFORE ROCKET FIRES`
- List of pre-flags (WARN / INFO each)
- Notes for rocket (carry-forward of pre-flags rocket must address at code-time)

Tag your review: `jack-ryan/v1.5-d11-math-note-gate1-review-1` (mirrors D10 pattern).

---

## Review 2 — Gandalf canonical-17 amendment

### Read

1. **Gandalf canonical-17 amendment** — `canonical/17-gear-and-spirit-guide-design.md` heal-cooldown affix family subsection (inside the "Updates 2026-05-11/12" zone)
2. **Gandalf canonical-32 § 13 amendment** — `canonical/32-progression-design.md` § 13.1-13.4 (cooldown heal + react-or-auto + portrait note)
3. **DoE feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 7.2 (the WHY)
4. **Existing canonical-17 gear-affix system** — the rest of the doc, pre-amendment, to understand what's being retired vs added

### Review focus

Gandalf's cascade locked engineering values that VS2b code execution must honor. Gate-1 catches contract gaps:

- **Heal mechanic completeness** — 10s CD; 35% max-HP magnitude + 50 HP floor; 0s cast; no resource cost; no default invuln. Is anything missing? (e.g., heal-during-combat-or-only-out-of-combat? heal-while-stunned? heal-while-frozen?)
- **Heal-affix family caps consistency** — 5s effective-CD floor; 60% magnitude ceiling; 2 concurrent secondary-effects. Is "effective-CD floor" defined unambiguously (is it after all reductions stack, or per-affix?)? Is the magnitude ceiling cumulative or per-affix?
- **`heal_secondary_effect` epic+/legendary-tier** — gandalf flagged this as the most opinionated call. Is the tier-restriction enforceable in rocket's existing legendary-mechanical-novelty infrastructure? Pre-flag if rocket needs new infrastructure.
- **Retired affixes list** — gandalf retired potion-interaction affixes. Is the list comprehensive? (e.g., are there spirit-guide-side affixes that interact with potions that were missed?)
- **Cross-seam contract** — VS2b execution will refactor `STAMINA_POTION_USE` → `heal_ability` in combatant.py. Gandalf flagged this in handoffs but didn't author the engine spec. Is the contract well-enough specified that gamora can write a math note for the refactor without ambiguity? Pre-flag if not.
- **Decisions-log entry** — gandalf's cascade locked load-bearing engineering values (heal CD, magnitude, react-or-auto window). Per ADR-001, these warrant a decisions-log entry. You write that entry (jack-ryan owns decisions-log per AGENTS.md § 2); confirm whether you'll author it now or queue for post-Gate-1.

### Output

Append canonical-17 review verdict to gandalf cascade dispatch (`agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`) as "Jack-ryan Gate-1 advisory" section. Verdict format identical to Review 1.

Tag: `jack-ryan/v1.6-doe-cascade-canonical-17-gate1-review-1`.

### Optional: decisions-log entry

If you elect to author the decisions-log entry NOW (recommend YES per ADR-001), title it: "Heal mechanic + heal-affix family canonicalization (DoE feel-target lock 2026-05-17)" with the gandalf-locked values embedded. This sets the contract for VS2b refactor.

---

## Out of scope (DO NOT)

- ❌ DO NOT BLOCK either review — Gate-1 is advisory; surface pre-flags + watchpoints
- ❌ DO NOT modify gamora's math note or gandalf's amendments (consume only; pre-flag in your review)
- ❌ DO NOT pre-empt rocket D11 implementation (your advisory gates it; rocket auto-fires after your verdict)
- ❌ DO NOT pre-empt VS2b heal_ability refactor (out-of-scope this dispatch; you're reviewing the design contract only)
- ❌ DO NOT extend scope to D12+ design questions (canonical-32 ceremonial 4-element path is parked for Matt; not your call)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] D11 math note review verdict appended to gamora dispatch (`ENDORSE` / `CONDITIONAL ENDORSE` / `REQUEST AMENDMENT BEFORE ROCKET FIRES`)
- [ ] D11 math note pre-flag list (WARN / INFO each) authored
- [ ] D11 math note review tagged `jack-ryan/v1.5-d11-math-note-gate1-review-1`
- [ ] Canonical-17 review verdict appended to gandalf cascade dispatch
- [ ] Canonical-17 pre-flag list authored
- [ ] Canonical-17 review tagged `jack-ryan/v1.6-doe-cascade-canonical-17-gate1-review-1`
- [ ] Optional: decisions-log entry for heal-mechanic lock (recommend YES)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE
- [ ] HANDOFF → rocket: D11 implementation may fire; pre-flags carry forward (D10 pattern)
- [ ] HANDOFF → matt: any open questions surfaced by review

---

## Coordination

- **Parallel-safe with**: drax v1.12 loot-pipeline (shipped); drax hotfix v1.12.0 (shipped); rocket hotfix v1.12.1 (shipped); elrond CraftPix curation extension (in flight); legolas-3 (shipped)
- **Triggers downstream**: rocket D11 implementation (auto-fires on your D11 math note verdict, even if CONDITIONAL ENDORSE per D10 pattern; you specify pre-flags rocket must address at code-time)
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **No tag push** without Matt authorization (ADR-006)

---

*Dispatched 2026-05-17 by knight-rider per gamora + gandalf parallel completion handoffs. ~30-60 min combined. Append completion records (two) when done.*
