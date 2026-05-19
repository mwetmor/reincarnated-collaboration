# Dispatch — 2026-05-19 — gandalf — Stage A2 A6 design watch-items framework

**From:** knight-rider
**To:** gandalf (design-steward — single framework covering three visual/UX axes)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires at Stage A2 kickoff
**Estimated effort:** ~1 day gandalf
**Acceptance:** Per § Acceptance. Tag fires: `stage-a2/v0.6-design-watch-items-framework`.
**Hive context:** Stage A2 closeout hive — A6 gates the visual/UX axes of A2 (B12) + A3 (B13 telegraphs) + A5 (B16 loot visual). Fires alongside A1 + A4 at Stage A2 kickoff.

---

## TL;DR

Per `canonical/16-project-roadmap.md` § "Stage A2 forward-audit (gandalf) watch-items" + `canonical/story/p6-forward-audit-2026-05-16.md`:

> - B12 full audit visual/UX axes (boots/gloves/belt UI; +% MS VFX; cap UX)
> - B13 telegraph-art convention decision
> - B16 loot visual presentation layer (drop animation; loot beams; rarity colors; tooltips; auto-pickup feedback) — **Drift-12 candidate**

A6 authors a single framework covering all three axes — pre-loads design decisions for A2 + A3 + A5 dispatches so drax can execute the visual/UX work without re-engaging gandalf mid-implementation.

---

## Context

Three visual/UX axes converge in Stage A2 closeout, each implicit-deferred until now per p6-forward-audit pattern:

- **B12 visual/UX** — boots/gloves/belt slot UI conventions; +% MS modifier VFX; hard-cap visual cue
- **B13 telegraph-art** — primitive-rendered (circle/cone/line; locked color/opacity in HD-2D-pixel register) vs vendor-sourced. Roadmap recommendation: primitive-rendered with PoE precedent
- **B16 loot visual** — drop animation; loot beams; rarity colors; tooltips; auto-pickup feedback. New Drift-12 candidate filing in drift-audit

A6 closes all three with one gandalf authoring pass.

---

## Required reading

In order:
1. `canonical/16-project-roadmap.md` § "Stage A2 forward-audit (gandalf) watch-items"
2. `canonical/story/p6-forward-audit-2026-05-16.md` (P6 pattern + implicit-deferred axis)
3. `canonical/28-engine-arpg-rebalance-design.md` B12 + B13 + B16 (engine-side specs)
4. `canonical/story/style-register.md` (HD-2D-pixel-art register; score-don't-filter)
5. `canonical/story/drift-audit.md` (Drift-12 forward-flag location)
6. `canonical/story/arena-room-hallway-system.md` (drax room/hallway topology + PIXELS_PER_METER=48)
7. F3 + F4 dispatches (sibling design surfaces — VS2a B6 skill-tree UI + Drift-14/15 framework precedent)
8. `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.6 (A6) + § 1.2/§ 1.3/§ 1.5 (consumer dispatches)
9. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## What you're producing

### Framework doc

**Path:** `canonical/story/stage-a2-design-watch-items-framework-2026-05-19.md`

**Content (three axes; single doc):**

### § A — B12 visual/UX framework

1. **Boots/gloves/belt slot UI conventions** — slot grid layout per existing gear-slot conventions; cross-reference loadout app surface (drax consumes in A2 UI work). Visual register: HD-2D-pixel-art per style-register.
2. **+% MS modifier VFX** — visual cue when player MS modifier is active. Particle trail? Foot-glow? Speed-lines? Pick one or specify per intensity-tier.
3. **Cap UX** — visual cue when MS modifier hits hard-cap (e.g., +50% MS is the cap). Show as "MAX" indicator? Greyed-out slot? Tooltip warning?
4. Cross-references for drax A2 consumption

### § B — B13 telegraph-art convention decision

1. **Decision: primitive-rendered vs vendor-sourced.** Roadmap recommendation: primitive-rendered with PoE precedent (`canonical/16-project-roadmap.md` § "Design watch-items (gandalf)").
2. **Per-shape convention** — circle / cone / line / point (geometry from F1 schema). Per-shape color (per element + telegraph-type) + opacity (per windup phase) locks.
3. **HD-2D-pixel register coherence** — telegraphs must read as integral to the demo's visual language, not as overlay artifacts.
4. **Per-tier convention** — trash mob telegraphs vs elite vs boss; intensity / size / windup-duration calibration
5. Cross-references for drax A3 consumption (telegraph UI for B13 escape AI + AOE indicators)

### § C — B16 loot visual presentation layer framework

1. **Drop animation** — loot drops with arc + landing-bounce; mobile-first responsive
2. **Loot beams** — per-rarity color beams (common/magic/rare/elite/legendary); HD-2D-pixel register
3. **Rarity colors** — locked palette (canonical ARPG palette; D3/D4-style; document hex values)
4. **Tooltips** — gear name + rarity + key affixes on hover/tap; mobile + desktop UX
5. **Auto-pickup feedback** — particle + sound on auto-pickup (audio deferred to Phase 1+ per audio-strategy; visual only for now)
6. Cross-references for drax A5 consumption

### § D — Drift-12 candidate filing in drift-audit

Add Drift-12 entry to `canonical/story/drift-audit.md` per existing pattern:
- **Drift-12 — Loot visual presentation layer implicit-deferred without being named as a deferred axis** (P6 instance similar to Drift-11A/B + Drift-14 + Drift-15)
- Prevention prescription: when scoping visual catalogue work, enumerate ALL load-bearing visual axes (VFX + characters + environment + UI + loot visual + telegraph art) at scoping time

---

## What you are NOT doing

- **NOT executing the visual work itself** (drax owns A2/A3/A5 UI implementation)
- **NOT amending B12/B13/B16 engine-side specs** (rocket + gamora own those; A6 is design-side only)
- **NOT escalating to Matt** — A6 is autonomous design-steward authoring per protocol § 4.0
- **NOT specifying audio cues** (audio deferred per audio-strategy-phase0; visual only)

---

## Cross-seam contract change? (Principle 6 gate)

**Design framework authoring; no production code change.**

**Round-trip: not applicable — framework only. Consumer dispatches (A2 + A3 + A5) carry round-trip smoke requirements where applicable.**

---

## Acceptance criteria

- [ ] Framework doc authored at `canonical/story/stage-a2-design-watch-items-framework-2026-05-19.md` covering all three axes (§ A B12 + § B B13 + § C B16)
- [ ] Drift-12 entry filed in `canonical/story/drift-audit.md`
- [ ] Cross-references reciprocal: A2 / A3 / A5 consumer dispatches cite this framework
- [ ] Hive log entry: gandalf STATE on framework authored + readiness signal for A2 + A3 + A5
- [ ] Tag fire request: `stage-a2/v0.6-design-watch-items-framework`

---

## Out of scope

- Engine-side B12/B13/B16 implementation (A2/A3/A5)
- Audio convention (Phase 1+)
- Localization (post-Phase-0)
- Per-class loot drop tuning (rocket A5 scope)
- Telegraph-art VFX integration with Pimen catalogue (drax A3; per A6 framework)

---

## Open questions for gandalf

- **B13 primitive-rendered details** — opacity per windup phase (0.3 → 0.9 ramp?); color per element (red/blue/green/yellow?); document conventions
- **B16 rarity palette** — D3-style (common-white / magic-blue / rare-yellow / legendary-orange / set-green) vs D4-style (slight palette variants) vs Reincarnated-specific. L1 gandalf
- **+% MS cap value** — typically 50% per ARPG canon; confirm with B12 spec
- **Drift-12 forward-prevention prescription** — extend to which future stages? Stage A4 (sets) and Stage A7 (progression) have visual layers; cross-reference

---

## References

- `canonical/16-project-roadmap.md` § Stage A2 forward-audit watch-items
- `canonical/story/p6-forward-audit-2026-05-16.md`
- `canonical/28-engine-arpg-rebalance-design.md` B12 + B13 + B16
- `canonical/story/style-register.md`
- `canonical/story/drift-audit.md`
- F3 dispatch (Drift-14 + Drift-15 framework precedent)
- F4 dispatch (B6 skill-tree UI precedent — sibling visual surface)
- `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md` § 1.6
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** Stage A2 kickoff (VS2b V6 ships). Fires alongside A1 + A4 (engine-only) at first-fire batch.

**Post-activation:** gandalf L2-equivalent decision-authoring; no Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. A6 closes three implicit-deferred visual axes with one framework; A2 + A3 + A5 inherit design decisions; Drift-12 fills the audit's last forward-flag.*
