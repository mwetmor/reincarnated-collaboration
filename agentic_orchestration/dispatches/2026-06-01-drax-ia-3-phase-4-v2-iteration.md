# Dispatch — 2026-06-01 — drax — IA-3 Phase 4: V2 iteration (consume V2 season_000043)

**From:** knight-rider (immediate-arc orchestrator)
**To:** drax (player-facing presentation seam)
**Approved by:** Matt 2026-06-01 strategic reset + pre-commitment ratification LOCK F (drax MVP-discipline) + LOCK G (autonomous Vercel deploy) + IA-1 V2 SUCCESS (season_000043 generated; commit pending in engine repo) + IA-3 P1 SUCCESS precedent
**Workstream tag:** `IA-3-drax-V2-iteration`
**Phase / phase-gate:** IA-3 Phase 4 (V2 iteration; load V2 season alongside V1; preserve V1 for comparison)
**Estimated effort:** ~0.5-1 session (data-add + verification; mirror of P1 V1 pattern)
**Acceptance:** V2 season output (season_000043) renders in reincarnated-loadout + reincarnated-demo via existing components; V2 close summary documented; Vercel preview updated

---

## 1. Context

IA-1 V2 SUCCESS — engine produced season_000043 at `~/Games/reincarnated-engine/seasons/season_000043/` (engine sha `cda99a5`; 1663.7s; validation PASSED; theme `brine`; anchor `The Salt Flats After the Sea`; LLM-named vocabulary Evaporant Scorch / Tidal Seeping / Salt-Crust Warding / Flat-Wind Scattering / Dry Bed Fracture / Bleached Shore Gleam / Brackish Murk / Storm-Surge Crack).

Per LOCK F MVP-discipline: drax loads V2 alongside V1 via existing data-loading layer (mirror of P1 pattern; preserves V1 season_000042 reference for comparison).

**Authoritative readings:**
- **IA-1 V2 close record (V2 substance):** `agentic_orchestration/ia-1-v2-close-record-2026-06-01.md`
- **IA-1 V1 close record (V1 baseline; preserved for comparison):** `agentic_orchestration/ia-1-v1-close-record-2026-06-01.md`
- **IA-3 P1 close summary (V1 integration precedent):** `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md`
- **Pre-commitment ratification (LOCK F + LOCK G):** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`
- **Immediate-arc workstream queue:** `agentic_orchestration/immediate-arc-workstream-queue-2026-06-01.md`

---

## 2. Scope (per LOCK F MVP-discipline)

### 2.1 V2 season output paths drax consumes

From `~/Games/reincarnated-engine/seasons/season_000043/`:
- `manifest.json` (V2 brine-theme; anchor "The Salt Flats After the Sea")
- `cosmological_vocabulary.json` (V2 LLM-named slot fills + pair rationales)
- `classes/*.json` (5 class definitions; class_0001-0005 with V2 mtime + class_0006-0011 with May 17 stale mtime — same V1-fix-deferral surface)
- `monsters/*.json`
- `gauntlet_recipe.json`
- `gear_pool_staged.json`
- `trial.json`
- `validation_report.json`
- `reference_gauntlet.json`
- `fights.jsonl` (47.8MB telemetry; LOCK F applies if touched)

### 2.2 P4 V2 iteration mirror of P1 V1 pattern

**Per LOCK F MVP-discipline:**
- EXISTING components ONLY (same inventory documented in P1 close summary)
- Data-loading layer extension only (load V2 alongside V1)
- V1 season_000042 PRESERVED (do not remove from loadout/demo data dirs)

**reincarnated-loadout:**
- Add `data/season_000043/` (adapted manifest + 5 class files + gear_pool.json; mirror of P1 V1 pattern)
- Existing `useSeasonData.ts` glob automatically picks up new directory (zero code changes per P1 precedent)
- season_000043 appears in Loadout + Sample page selectors alongside season_000042

**reincarnated-demo:**
- Add season_000043 to `SEASON_IDS` in `loader.ts`
- Add data at `public/seasons/season_000043/` (mirror of P1 V1 pattern)
- season_000043 selectable in demo

### 2.3 V1-fix-deferral bug surface verification

Per IA-3 P1 close summary, 3 V1-fix-deferral bugs surfaced:
1. Engine classes 0006-0011 emit `is_act_boss: null` not `true`
2. `resolveElementDisplay` null-guard scope issue
3. SeasonManifest type `elements` non-optional vs engine emits null

**For V2:**
- Verify bug 1 persists (or was trivially side-fixed by engine work)
- Verify bug 2 still appears (V2 manifest also has `elements: null`)
- Verify bug 3 still surfaces (V2 manifest also has `elements: null`)

If bugs persist: surface in close summary for post-immediate-arc Pattern B.
If side-fixed: note + verify.

### 2.4 What's IN scope (MVP V2)

- Add V2 season data (data-add only; no new components)
- Verify existing components render V2 data correctly
- Type additions (additive per LOCK J § 1; new fields specific to V2 if any)
- Bug surface verification per § 2.3
- Vercel preview update

### 2.5 What's OUT of scope (DEFERRED post-immediate-arc Pattern B)

Same as P1 V1:
- NEW UI components
- UI redesign
- NEW feature additions
- Bug fixes for the 3 V1-fix-deferral surfaces (DEFERRED)
- Performance optimizations

---

## 3. Decision authority

Per LOCK F: drax MVP scope + data-loading layer extension + component verification YOURS per drax seam authority. Per LOCK G: Vercel preview deployment autonomous.

**Escape-clause triggers (escalate to KR + Matt):**
- New UI component proposal (DEFERRED post-immediate-arc)
- Architectural amendment
- Substantial new bugs blocking V2 integration

**Non-escalation surfaces (you handle):**
- Data-loading layer extension (mirror of P1 pattern)
- TypeScript additive type extensions
- Vercel preview deployment configuration
- Bug surface verification + close-summary documentation

---

## 4. Output expectations

### 4.1 reincarnated-loadout repo
- V2 season data added (data/season_000043/)
- Vercel preview updated (season_000043 selectable in UI)

### 4.2 reincarnated-demo repo
- V2 season data added (public/seasons/season_000043/)
- season_000043 added to SEASON_IDS

### 4.3 Meta-repo
- IA-3 P4 V2 close summary at `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-4-v2-iteration-close.md`:
  - V2 integration verdict (SUCCESS / PARTIAL-SUCCESS / BLOCKED)
  - reincarnated-loadout V2 commit + Vercel URL
  - reincarnated-demo V2 commit
  - V1-fix-deferral bug surface verification (3 bugs: persist / side-fixed / new behavior)
  - V1 vs V2 visual comparison observations (brief; no UI changes per LOCK F)
  - Notable observations for post-immediate-arc Pattern B

### 4.4 Auto-commits + auto-push
- reincarnated-loadout: V2 data + Vercel deploy
- reincarnated-demo: V2 data
- Meta repo: IA-3 P4 V2 close summary

---

## 5. Cross-seam contract change? (Principle 6)

**Answer:** NOT applicable. V2 iteration is data-add only; no schema change; no engine output schema amendment.

**Round-trip:** not applicable.

---

## 6. Acceptance criteria

- [ ] V2 season_000043 data loads in reincarnated-loadout (Vercel verified)
- [ ] V2 season_000043 data loads in reincarnated-demo
- [ ] V1 season_000042 PRESERVED (existing data not removed)
- [ ] Existing components render V2 data
- [ ] No new UI components added (verify against P1 component inventory)
- [ ] V1-fix-deferral bug surface verification documented
- [ ] V2 close summary authored
- [ ] Auto-commit both player-surface repos + meta repo
- [ ] Auto-push + Vercel auto-deploy verified

---

## 7. Out of scope

- Post-immediate-arc UI design questions
- Long-arc deferred items
- IA-1 V3+ re-fires
- gandalf design-quality audit (separate parallel fire per LOCK H)

---

## 8. References

- All authoritative readings in § 1
- **reincarnated-loadout repo:** `~/Games/reincarnated-loadout/`
- **reincarnated-demo repo:** `~/Games/reincarnated-demo/`
- **Engine-repo V2 season:** `~/Games/reincarnated-engine/seasons/season_000043/`
- **drax OP:** `agentic_orchestration/operating-procedures/drax.md`

---

## Completion record (you append at completion)

```markdown
---

## Completion record
**Completed:** 2026-06-XX HH:MM
**V2 integration verdict:** SUCCESS / PARTIAL-SUCCESS / BLOCKED
**reincarnated-loadout commit + Vercel URL:** brief
**reincarnated-demo commit:** brief
**V1-fix-deferral bug surface verification:** persist / side-fixed / new behavior
**V1 vs V2 observations:** brief
**Notable observations for post-immediate-arc Pattern B:** brief
**IA-3 P4 close summary (meta repo):** path + commit
**Routing back to KR:** "IA-3 P4 V2 iteration SUCCESS — IA-3 CLOSED — proceed to strategic re-engagement Pattern B with Matt" / specific issue
```

After your completion, IA-3 P4 closes → **IA-3 CLOSES** → KR signals post-immediate-arc Pattern B for strategic re-engagement.

---

**End of IA-3 P4 V2 iteration dispatch.**
