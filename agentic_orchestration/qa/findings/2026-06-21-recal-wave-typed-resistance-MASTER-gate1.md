# Finding — 2026-06-21 — recal-wave-typed-resistance-MASTER (Gate-1 DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict ENDORSE)
**Target:** `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md` (MASTER v2, typed-resistance re-draft)
**Developer:** knight-rider (dispatch author)
**Mode:** Gate-1 DESIGN-MODE (pre-publish gate; releases the re-draft to Matt for publish-go)
**Principles applied:** Review #1 (math-before-code), #2 (smoke/scope-gate), #3 (cross-seam round-trip), #4 (decisions-log/ruling as truth); Discipline #11 (empirical inspection — re-derived the four load-bearing engine facts from source, not from the dispatch's framing).

## What I found

I re-derived the four load-bearing engine facts first-hand (Discipline #11) rather than trusting the re-draft's transcription, because a silent numeric or function-name drift here would corrupt every downstream build. All four confirm exactly: (1) the live flat constants are `PLAYER_ARMOR_FACTOR_VS_BOSS = 0.95` / `MOB_DAMAGE_SCALE = 0.40` (`spatial_engine.py:159/228`), which is precisely the live knob-set the dispatch's G-D names as the one to NOT carry; (2) the death channel is `dmg = raw_dmg * (1.0 - self.player.armor_factor)` (`:1951`) exactly as cited; (3) `resolve_spatial_hit` exists and is the live offense route (`:1391`) — the correct swap target — and the mob carries `resolver_skills=[]` (`:2508`); (4) neither `PartitionModifier` nor `RolledPartitionModifier` carries any element field (`partition_schema.py:505-546`) — identity is `modifier_id`+`category` only, confirming 0b-c3 as the MEDIUM add. The geometry whitelist `{circle,cone,line,point}` with all else falling to no-hit `[]` (`:716-742`) is also source-accurate. The re-draft routes the corrected resolver spine faithfully and re-opens NO ruled design question. Verdict: **ENDORSE.**

## The seven verification points (all PASS)

1. **Spine fidelity — PASS.** Death channel routed through `resolve_spatial_hit` (mob attacker, player real defender); the two 0a engine touches named explicitly (emit non-empty mob `resolver_skills`; swap `:1951` flat→resolver) at gamora line (a) and G-D. `PLAYER_ARMOR_FACTOR_*` explicitly retired/inert on the death channel (gamora line (a)). The flat anchor is genuinely DROPPED: G-D forbids carrying BOTH `4.0/0.76` AND the live `0.40/0.95` as a knob-set, and the SUPERSEDED list (line 66) drops both explicitly. No live knob-set survives anywhere as a calibration seed.

2. **Three 0b concerns folded — PASS, with teeth.** (a) Anti-tax is a first-class JOINT gate on BOTH seam lines: G-A states it as the headline's load-bearing gate with a fail condition; rocket line (a) bullet 4 and gamora line (e) both carry it as a named acceptance criterion explicitly flagged "first-class acceptance gate, not a footnote." Genuinely bilateral with a reject clause. (b) §4 gear prerequisite sized as the MEDIUM add — rocket line (a) SIZING bullet says "element SELECTION must be ADDED to the roll — NOT merely preserved," with the downstream bound (no schema/aggregation/sim change) intact. Source-confirmed accurate. (c) Flat-anchor numeric-drift note present at 0a-c2 fold (line 35): "the held MASTER's `0.76/4.0` were calibration-grid SEARCH TARGETS, not live state (live: `0.95/0.40`)" — no one will mistake it for engine state.

3. **0a spike caveats folded — PASS.** Mob substrate defaultable, called out as optional richness NOT a route requirement (0a-c1 fold line 34; rocket line (a) final bullet). Two engine touches named (0a-c3 fold line 36). Magnitude re-derive-from-scratch carried (G-D; gamora line (b)).

4. **Salvage vs supersede — PASS.** SURVIVES correctly keeps threat SHAPE, geometry HARD constraint, trash<boss, emission-held, two-axis joint re-rate, full-pop validation. SUPERSEDED correctly drops the flat spine, both flat anchors, the typeless ruling (threat-spec §5b reversed), and the old guard-collision argument (which was measured on the false flat-mitigation scenario — matches my 0b Claim 4). Clean partition.

5. **Dependency spine — PASS.** rocket-first is a HARD block for BOTH stated reasons (line 99): gamora cannot calibrate a channel the mob doesn't emit (`resolver_skills=[]`), and the typed payoff is inert against undifferentiated kits. Both reasons are real and source-grounded.

6. **Principle-6 round-trip clauses — PASS, all three seam lines.** rocket (two contract surfaces + MIGRATION.md + round-trip smoke, line 125); gamora (new fight_log survive/death-cause fields + MIGRATION coordination + round-trip smoke, line 145); star-lord (additive telemetry + MIGRATION + round-trip smoke, line 154). The dedicated Principle-6 gate section (line 165) enumerates all three. "No seam tags without its round-trip smoke" stated.

7. **No ruled design question re-opened — PASS.** Typed direction, signature-element + reward-for-matching, the resolver spine, the gear DoD, the guard re-founding, and swarm shallow-typing are all carried as RULED and listed in the wave-level out-of-scope non-goals (line 180). The build lane (sequence + size + validate) is respected; no design adjudication is smuggled in.

## Rationale

ENDORSE (not ENDORSE-WITH-CONCERNS) because all three carried 0b concerns are folded correctly AND with the teeth I asked for — the anti-tax gate is genuinely bilateral and reject-clause-backed, not headline-decorated; the §4 sizing names the larger branch at source; the numeric-drift note is present and explicit. The four engine facts re-derive to source. Per Review #1 the re-draft front-loads math-before-code on both the rocket (magnitude SHAPE envelope before wiring) and gamora (mitigation curves before sweep) lines. Per Review #4 the design rulings are treated as truth and the SUPERSEDED partition cleanly retires the invalid flat spine. This is a build-sequencing artifact that faithfully routes a ruled design — exactly its lane.

## One INFO note (does NOT gate; for the per-seam split)

- **[INFO] Bareword file-path shorthand.** The dispatch cites `spatial_engine.py:1951` etc. as barewords; the file actually lives at `simulation/spatial_gauntlet/spatial_engine.py`. Line numbers are correct. When knight-rider splits into per-seam pickup files, consider expanding to the full path so rocket/gamora land on the file directly. Cosmetic; line-cites all verified accurate.

## Action

- [ ] knight-rider: none required to ENDORSE. On Matt publish-go, split into per-seam pickup files; optionally expand bareword paths to full `spatial_gauntlet/` paths (INFO).
- [ ] Matt: publish-go decision — this Gate-1 ENDORSE releases the re-draft. The design is ruled; this artifact sequences the build faithfully without re-opening it.

## References

- Reviewed dispatch: `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`
- Upstream Gate-1 (three carried concerns): `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md`
- Engine facts re-derived: live constants `spatial_gauntlet/spatial_engine.py:159/228`; flat death channel `:1951`; resolver hit route `:1391`; mob `resolver_skills=[]` `:2508`; geometry whitelist `:716-742`; no element field `generation/partition_schema.py:505-546`; resolver `damage_resolver.py:293`
