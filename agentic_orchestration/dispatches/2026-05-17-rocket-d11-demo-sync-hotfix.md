# 2026-05-17 — rocket — D11 demo-sync hotfix (engine output → demo public/seasons)

**Authority:** Knight-rider per rocket persistence diagnostic verdict (`D11-persistence-diagnostic-2026-05-17.md`) which surfaced: demo public/seasons NEVER SYNCED post-D11. Demo serves `damage_multiplier = 1.000` (pre-D11) on hybrid_mage classes while engine output has `damage_multiplier = 0.93` (post-D11). Matt may be playtesting OVERPOWERED hybrid_mage classes — they feel un-taxed in actual play.
**Type:** Pattern A — ~5-10 min file copy + smoke verification; no code changes.
**Predecessors:** rocket v1.13 D11 implementation (`c0a622a`?) ; rocket v1.13.1 monster geometry backfill (`001994e`) ; rocket persistence diagnostic.

---

## Why this matters

Diagnostic confirmed engine D11 output is correct (dm=0.93 in monolithic season_002012/classes.json). Diagnostic ALSO confirmed demo public/seasons is STALE (dm=1.000; mtime 18:10 vs engine 18:41). The sync handoff implied in rocket v1.13 ("HANDOFF → drax-demo: in-place refresh sufficient") was never executed — likely because v1.13.1 monster geometry backfill ran AFTER v1.13 and copied a subset of files but not classes.json.

Net effect: Matt's playtest has been seeing D10-era hybrid_mage with NO tax applied. Combined with the D11 sprint outcome being already-projected-MISS by gamora, this means the playtest feel of hybrid_mage right now is even MORE overpowered than engine-curated state — bad for empirical balance feel.

This hotfix is surgical: copy 5 season classes.json files from engine output to demo public/seasons.

---

## Required reading

1. **Diagnostic report** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-persistence-diagnostic-2026-05-17.md` (especially § Check 6 demo sync)
2. **Engine D11 output** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/...015/classes.json` (your sync source; mtime 18:41)
3. **Demo target** — `reincarnated-demo/public/seasons/season_002011/...015/classes.json` (your sync target; mtime 18:10)
4. **drax v1.12.1 carried_gear backfill** — pattern for the engine→demo copy (you ran this earlier; same path discipline)

---

## Scope — three steps

### Step 1 — Copy 5 monolithic classes.json files

For each season (002011-015):
- Source: `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_NNNNNN/classes.json`
- Target: `reincarnated-demo/public/seasons/season_NNNNNN/classes.json`
- Verify pre-copy: source has post_process_d11=True and at least one hybrid_mage class with element_coverage_tax.tax_applied=true; target has dm=1.000 (stale)
- Post-copy verify: target now shows dm=0.93 on hybrid_mage damage-bearing skills; demo public/seasons mtime updated

### Step 2 — Decide on per-class files

Per diagnostic § Implication item (A): per-class `classes/<id>/class_XXXX.json` files are static D10 snapshots; not read by D11 salvage; not consumed by demo (verified in diagnostic).

Options:
- (a) Leave as-is (D10 snapshots; deprecate flag in directory README; document non-authoritative status)
- (b) Backfill per-class files from monolithic to keep parity (more work; only matters if downstream consumer needs them)
- (c) Delete per-class files (per archive discipline)

Recommend (a) for this hotfix — add a `_DEPRECATED.md` or README note in each season's `classes/` subdirectory flagging "these per-class files are D10-era snapshots; authoritative D11 data lives in ../classes.json monolithic". Pursue (b) or (c) as a separate cleanup later if needed.

### Step 3 — Smoke + tag

- Verify demo build still loads with synced data (no need to rebuild; vite hot-reloads JSON via browser refresh)
- Note in completion record: any loadout-side consumer of per-class files needs to be aware (per drax v1.11 noted that loadout uses per-class — verify whether loadout's data/ for D11-curated 002011-015 is also stale or already correct)
- PRE-SIGNAL § 14.1.1 before hive-log append
- Tag `rocket/v1.13.2-d11-demo-sync-hotfix-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify any engine code or salvage scripts (sync only)
- ❌ DO NOT alter D11 output values (copy as-is from engine to demo)
- ❌ DO NOT pre-empt D11.1 chain (jack-ryan Gate-1 + rocket D11.1 implementation auto-firing in parallel)
- ❌ DO NOT push tag without Matt authorization (ADR-006)
- ❌ DO NOT execute per-class file backfill / deletion this dispatch — separate decision (Matt-flag in completion record if you have strong opinion)

---

## Acceptance criteria

- [ ] 5 monolithic classes.json files copied engine → demo
- [ ] Demo target verification: dm=0.93 on hybrid_mage damage-bearing skills (sample at least 2 seasons)
- [ ] Per-class files left as-is OR deprecation note added (recommend option a)
- [ ] Loadout per-class files verified — are they D11-aligned or also stale?
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE entry
- [ ] Tag `rocket/v1.13.2-d11-demo-sync-hotfix-1`
- [ ] HANDOFF → matt: hard-refresh demo; hybrid_mage classes now play with proper D11 tax applied (still overpowered per gamora's smoking gun projection, but engine-curated overpowered, not stale-D10 overpowered)
- [ ] Append completion record to this dispatch

---

## Coordination

- **Parallel-safe with**: jack-ryan D11.1 Gate-1 (in flight); rocket D11.1 implementation (queued; auto-fires post-Gate-1); gandalf audio register canon (in flight); legolas-4 audio crawl (shipped)
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No tag push** without Matt authorization (ADR-006)

---

*Dispatched 2026-05-17 by knight-rider per persistence diagnostic critical secondary finding. ~5-10 min. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 late-evening+2 by rocket
**Tag:** `rocket/v1.13.2-d11-demo-sync-hotfix-1` (applied to reincarnated-demo main)
**Commits:** `6537625` (reincarnated-demo) + `004ff45` (reincarnated-engine)
**Duration:** ~10 min

### Acceptance criteria status

- [x] 5 monolithic classes.json files copied engine → demo
- [x] Demo target verification: `post_process_d11=True` + `element_coverage_tax_multiplier=0.93` on all multi-element hybrid_mage; skill-level `dm=0.93` confirmed on damage-bearing skills (sampled seasons 002011 and 002012)
- [x] Per-class files left as-is; `_DEPRECATED.md` added to each `output/season_NNNNNN/classes/` subdirectory (option a)
- [x] Loadout per-class files verified — **STALE (D10-era)**. `reincarnated-loadout/data/season_002011..002015/classes/class_XXXX.json` contain only `post_process_d10=True`; no `element_coverage_tax_multiplier`. Flagged for drax/matt — drax to verify whether loadout reads per-class files or monolithic classes.json before next deploy.
- [x] PRE-SIGNAL § 14.1.1 before hive-log append (git fetch confirmed clean; last remote: gamora/v1.7)
- [x] Hive-log STATE entry appended
- [x] Tag `rocket/v1.13.2-d11-demo-sync-hotfix-1` applied (local; push gated per ADR-006)
- [x] HANDOFF → matt noted below

### Pre-copy verification (confirmed stale)

Demo `season_002012` before copy: 4 hybrid_mage with only `post_process_d10=True`; no D11 fields.
Engine `season_002012` source: 4 hybrid_mage with `post_process_d11=True`, `element_coverage_tax_multiplier=0.93`, skill `dm=0.93`.

### Post-copy verification (confirmed D11)

All 5 seasons in demo now show `post_process_d11=True`. Tax values:
- `{0.93}` — seasons 002012, 002014, 002015 (all hybrid_mage multi-element, all taxed)
- `{0.93, 1.0}` — seasons 002011, 002013 (mix: some hybrid_mage single-element = no tax; correct engine behavior)

### HANDOFF → matt

Hard-refresh demo (Cmd+Shift+R). Hybrid_mage now plays with D11 engine-curated state. Still overpowered per gamora's D11.1 projection, but engine-overpowered not stale-D10-overpowered. D11.1 Gate-1 (jack-ryan) + D11.1 implementation (rocket, queued) unaffected by this hotfix.

**Loadout flag for drax:** Verify whether `reincarnated-loadout` reads per-class JSON directly or from monolithic classes.json. If per-class, loadout is showing D10 stats for hybrid_mage.

— rocket
