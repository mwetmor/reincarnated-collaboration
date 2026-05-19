# Dispatch — 2026-05-19 — gandalf — VS2b V4 chierit element-reconciliation (small)

**From:** knight-rider
**To:** gandalf (story-and-design steward — chierit slot assignment + physical/hybrid fallback OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires at VS2b kickoff (no upstream V-gate)
**Estimated effort:** ~30 min gandalf
**Acceptance:** Per § Acceptance. Tag fires: `vs2b/v0.4-chierit-element-reconciliation`.
**Hive context:** VS2b hive — V4 unblocks V3 (drax loadout display) by locking the chierit slot assignments. Same call serves both VS2a (chierit per-archetype mapping watch-item) + VS2b (V3 loadout portraits).

---

## Context

Per `canonical/story/embodiment-display-loadout.md` § 15 "For knight-rider" recommendation 4:

> Author chierit element-reconciliation dispatch (small; ~30 min) confirming 10-character slot assignments + physical/hybrid fallback strategy

Per `canonical/16-project-roadmap.md` § VS2a "Design watch-items":

> chierit per-archetype mapping — chierit ships 10 element-mapped characters; Reincarnated has ~14 class archetypes. Need decision: element-only mapping (Fire Knight covers fire_warrior + fire_mage) vs per-archetype with placeholders.

Per `canonical/16-project-roadmap.md` § VS2b "Design watch-items":

> Character roster gap — see VS2a chierit per-archetype mapping decision; same call serves both VS2a + VS2b display surfaces.

V4 is the ONE gandalf decision that closes both VS2a (chierit watch-item) and VS2b (V3 portrait + character-track C3 in-flight). Small surface; high leverage.

---

## Required reading

In order:
1. `canonical/story/embodiment-display-loadout.md` § 13 (chierit portrait crop tooling) + spec § 4 + § 5 (class-header visual + spirit name)
2. `canonical/16-project-roadmap.md` § VS2a + § VS2b "Design watch-items" (chierit reconciliation)
3. C3 character-track ingest dispatch (in-flight per drax AGENT_STATE; sibling consumer of your decision)
4. F3 dispatch + Drift-15 framework (parallel canonical-bias closure work)
5. legolas chierit catalogue scout doc (existing under `agentic_orchestration/research/catalogue/`)
6. `canonical/story/style-register.md` (HD-2D-pixel-art register)
7. `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.4 (V4)
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## What you're producing

### Decision doc

**Path:** `canonical/story/vs2b-chierit-element-reconciliation-2026-05-19.md`

**Content:**

1. **10-character chierit slot assignments per element** — locked mapping table:
   - Which chierit character covers which substrate element (fire / earth / water / wind + L2 grouping-layer elements + non-canonical-four where applicable)
   - Per-archetype-coverage decision: element-only (Fire Knight covers fire_warrior + fire_mage + fire_caster) OR per-archetype with placeholders (separate Fire Knight per archetype)
   - Recommendation (your design read): element-only is the lower-bandwidth path; per-archetype-with-placeholders is the higher-fidelity path; trade-off discussion + commit

2. **Physical/hybrid fallback strategy** — for archetypes where no chierit element maps cleanly:
   - Physical archetypes (`physical_grappler`, `physical_warrior`): which chierit character + how rendered (palette-shift? composite? bespoke placeholder?)
   - Hybrid archetypes (`hybrid_mage`, `hybrid_caster`): which chierit + visual differentiation strategy
   - Experimental archetype: fallback per spec convention

3. **Implications for V3 loadout display** + C3 demo character rendering:
   - V3 portrait crop pipeline (drax tooling per spec § 13) — chierit assignment per class manifest
   - C3 chierit Elementals integration — same slot assignment
   - cross-reference both consumers

4. **VS2a + VS2b watch-item closure:**
   - Update `canonical/16-project-roadmap.md` § VS2a + § VS2b "Design watch-items" — close the chierit per-archetype mapping decision as RESOLVED
   - Cross-reference back to this decision doc

---

## What you are NOT doing

- **NOT executing the portrait crop tooling** (drax V3 § 13)
- **NOT touching character-track ingest pipeline** (drax C3 in-flight)
- **NOT amending substrate-identity declarations** (already-locked per 2026-05-17)
- **NOT escalating to Matt** — V4 is autonomous per protocol § 4.0; small design steward call within your scope

---

## Cross-seam contract change? (Principle 6 gate)

**Decision-only dispatch; no production code change.**

**Round-trip: not applicable — gandalf design decision authoring; no code touched. V3 + C3 dispatches carry their own contract changes downstream.**

---

## Acceptance criteria

- [ ] Decision doc authored at `canonical/story/vs2b-chierit-element-reconciliation-2026-05-19.md`
- [ ] 10-character slot assignments locked with rationale
- [ ] Physical/hybrid fallback strategy documented
- [ ] V3 + C3 consumer implications cross-referenced
- [ ] Roadmap § VS2a + § VS2b watch-items closed (RESOLVED status)
- [ ] Hive log entry: gandalf STATE on decision authored + cross-references to V3 + C3 consumers
- [ ] Tag fire request: `vs2b/v0.4-chierit-element-reconciliation`

---

## Out of scope

- chierit portrait crop tooling implementation (drax V3 § 13)
- Demo-side character rendering integration (drax C3 in-flight)
- New chierit character commissioning (post-VS2b territory; potentially Phase 1)
- Non-chierit character roster expansion (out of scope)
- Style register amendments (already locked)

---

## Open questions for gandalf

- **Element-only vs per-archetype** — your design read. Spec § 15 implies element-only is the spec assumption ("chierit element-only character mapping (per Q3 council answer today)") but document the explicit reconciliation reasoning
- **Physical archetype fallback** — what visual register do physical_grappler / physical_warrior use? Palette-shift on a generic warrior chierit? Separate non-chierit asset? Document choice.
- **Hybrid archetype visual differentiation** — hybrid_mage carries two element substrates; visual rendering shows which? Or generic "hybrid" silhouette?
- **Cross-reference with Drift-15 closure** — V4 + F3 + F5 all converge on canonical-bias-clean player surface. Does V4 surface any Drift-15 follow-on? Surface in hive log.
- **Experimental archetype fallback** — `experimental` archetype has intentional unconventionality; how renders?

---

## References

- `canonical/story/embodiment-display-loadout.md` § 13 + § 4 + § 5
- `canonical/16-project-roadmap.md` § VS2a + § VS2b "Design watch-items"
- C3 character-track ingest dispatch (in-flight)
- F3 dispatch + Drift-14/15 framework
- legolas chierit catalogue scout doc (`agentic_orchestration/research/catalogue/`)
- `canonical/story/style-register.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.4
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** VS2a L1 ships → VS2b kickoff. Can fire alongside V1 + V5 in parallel.

**Post-activation:** gandalf L2-equivalent decision-authoring; no Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. V4 is small but central. One gandalf decision unblocks V3 + C3 + closes two watch-items. The chierit slot map locks; the player gets the form.*
