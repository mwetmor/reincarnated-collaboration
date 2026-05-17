# 2026-05-17 — gandalf — Asymmetric perceived AOE radius design briefing

**Authority:** Matt L3 disposition 2026-05-17 (pre-sign-off design surface; "I believe Gandalf once told me Diablo/PoE converged on this pattern").
**Type:** Pattern B (long task) — ~0.5-1 day. Design briefing; no code work.
**Trigger:** Matt sign-off message 2026-05-17 with explicit recall of a gandalf-surfaced design pattern from prior session.

---

## Why this matters

Matt's recall, verbatim:
> *"I believe that Gandalf once told me that Diablo/PoE converged across the years on the concept that the enemy combatant AOE radius would appear larger than it truly was and that the player combatant AOE radius would appear smaller than it truly was. This would give the player the feeling that they are slightly better than the enemies at avoiding the 'adjusted ground radius' of the enemies, and they could visibly see that the enemies were worse at avoiding their player radiuses. This should be a feature of the engine sim and also a feature of the demo."*

**Decoded:**
- **Enemy AOE:** apparent_radius > true_radius (visually larger than damage-effective radius). Player perceives "got out just in time" when actually had buffer; or perceives "barely escaped" when was actually safe.
- **Player AOE:** apparent_radius < true_radius (visually smaller than damage-effective radius). Monsters seem to "barely escape" the visual but still take damage; player's AOE feels more effective than its visual suggests.
- **Net effect:** Player feels slightly more skilled at evasion AND slightly more effective at offense. **Player-favoring asymmetric fudge.**
- This is reportedly canonical ARPG genre wisdom (Diablo/PoE convergence per Matt's recall of your prior conversation).

**Cosmological + pragmatic argument**: The asymmetry is a perception-engineering pattern that doesn't lie about damage outcomes — damage resolution remains deterministic at true_radius — but it gives the player a feel-good asymmetry without compromising mechanical integrity. This is the kind of design wisdom that ARPGs accumulated over decades and that we should incorporate intentionally rather than discover by accident.

**Cross-impact**: Engine simulation gauntlet AI uses apparent_radius for monster decisions (so monster reactive escape behavior in gamora narrow-slice operates on apparent_radius); damage resolves at true_radius. Demo renderer uses apparent_radius for indicator visuals; damage was already engine-driven. Both sides converge on the same player-favoring effect. **Discipline #15 satisfied** (demo as renderer + engine as simulator; both honor the same asymmetry).

---

## Required reading (in order)

1. Matt's verbatim quote above; your own genre-canon memory (Diablo/PoE/D3/D4/Last Epoch/Grim Dawn historical convergence on this pattern)
2. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` (your prior briefing; AOE telegraph system context)
3. `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` (your AOE tuning briefing; § 3 AOE-radius vs spacing coupling — this asymmetry interacts with that math)
4. `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate identity schema; potential location for asymmetry fields
5. Rocket v1.7 + v1.8 schema fields (windup_duration_seconds, indicator_color_hex, dodge_iframes_seconds) — pattern for new fields

---

## Scope (single-track design briefing)

### Surface 1 — Source-validation against genre canon

Your white-wizard memory: was this Diablo/PoE convergence pattern real (Matt's recall accurate)? If yes, document specific examples:
- Which Diablo iteration introduced it? Which PoE expansion locked it as norm?
- What were the magnitudes used? (E.g., enemy_radius_apparent = enemy_radius_true × 1.20? Player = × 0.85?)
- Were there cross-class variations or substrate-coupled variations historically?
- What were the documented failure modes when this pattern was tuned wrong? (Too asymmetric → player feels game is fake / too symmetric → player feels "tagged" by enemy AOEs unfairly)
- Did any ARPGs explicitly reject this pattern? (E.g., did Last Epoch / Grim Dawn deliberately not apply it for a hardcore reason?)

If the pattern is real, propose magnitudes for Phase-1 P1.
If the pattern is over-stated by Matt's recall, propose what the actual ARPG convergence was and adapt.

### Surface 2 — Design specification for Phase-1 P1

Per-substrate or substrate-agnostic? Surface dimensions:

- **Substrate-agnostic option (simplest):** single asymmetry factor (e.g., 0.85 / 1.15 = ±15%) applied uniformly. Damage resolves at true_radius; rendering at apparent_radius. AI uses apparent_radius for decisions.
- **Substrate-coupled option (richer):** different asymmetry per substrate. E.g., fire (escalation) has larger asymmetry because the "feel" of fire requires visual oversell; earth (positional refusal) has minimal asymmetry because earth is honest. Cosmologically motivated. More complex to implement.
- **Recommendation**: which is right for Phase-1 P1? Substrate-agnostic for v1.0, substrate-coupled in Phase-2? Or do it once cleanly with substrate coupling?

Propose magnitudes. Propose schema location (root engine config? substrate identity declarations? class metadata?).

### Surface 3 — Implementation contract

Detail what each seam owns:

- **Rocket** (foundation/schema): adds the asymmetry field(s) to substrate identity declarations OR engine config; fail-loud validation rules
- **Gamora** (simulation): 
  - Fight engine: damage resolution uses true_radius (unchanged from current default)
  - AI logic (`ai_strategies.py`): monster reactive escape uses apparent_radius (visible-to-AI radius is larger for enemy AOEs the monster is dodging; smaller for ally AOEs the monster is fleeing from)
  - Telemetry: emits both true_radius_hit_count AND apparent_radius_hit_count per AOE cast for D14 calibration
- **Drax-demo** (renderer): ground indicator rendered at apparent_radius (smaller for player AOEs; larger for enemy AOEs); damage resolution comes from engine via existing channels
- **Drax-loadout** (no impact): static surface; not relevant
- **Star-lord** (output): export schema may need to carry the asymmetry factor if it's per-class or per-substrate

### Surface 4 — Validation hook for KPM gauntlet test

Matt's KPM-gauntlet-vs-demo-playtest test will measure this asymmetry's effect:
- Engine gauntlet AI uses apparent_radius → monsters escape at apparent_radius boundary → some get caught at apparent_to_true buffer → "spillover kill" rate measurable
- Demo player perceives same → feel-good fudge
- Both sides converge on KPM that includes the spillover effect

Propose: should the gauntlet sim emit `spillover_hit_count` telemetry as a separate field so D14 can calibrate on it? Or fold into total `aoe_hit_count`?

---

## Output deliverable

A single Matt-facing design briefing:
`canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md`

Suggested structure:
- § 0 — TL;DR (specific numerical asymmetry magnitudes + implementation summary in 5-10 lines)
- § 1 — Why this matters (cosmological + pragmatic; Matt's recall + your source validation)
- § 2 — Surface 1: Genre-canon source validation
- § 3 — Surface 2: Phase-1 P1 design specification
- § 4 — Surface 3: Per-seam implementation contract
- § 5 — Surface 4: KPM gauntlet validation hook
- § 6 — Cross-impact map (D10, D14, D27, post-D10 regen, narrow-slice, your prior AOE tuning briefing)
- § 7 — Specific implementation parameters (numerical table; consumable directly by rocket/gamora/drax)
- § 8 — Recommendation: substrate-agnostic v1.0 vs substrate-coupled (your binding decision per Matt's "trust gandalf" pillar)

---

## Out of scope (DO NOT)

- ❌ DO NOT write engine code, simulation code, or demo code
- ❌ DO NOT modify D8 / D9 trait pools
- ❌ DO NOT modify substrate-identity declarations beyond schema-location proposal (your § 4 work)
- ❌ DO NOT extend scope to other player-favoring fudges (e.g., monster damage scaling fudge, hit-detection forgiveness, etc.) — surface as OBSERVATION

---

## Acceptance criteria

- [ ] Briefing authored at `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md`
- [ ] Genre-canon source validation per § 2 (confirm or correct Matt's recall)
- [ ] Implementation contract per § 4 with explicit per-seam obligations
- [ ] § 7 contains direct-implementable numerical parameters (consumable by rocket schema dispatch + gamora sim dispatch + drax renderer dispatch)
- [ ] § 8 binding recommendation per "trust gandalf" pillar
- [ ] Cross-impact map present (§ 6)
- [ ] Tag `gandalf/v1.5-asymmetric-perceived-aoe-radius-briefing-1`
- [ ] Hive-log STATE + HANDOFFs (rocket / gamora / drax / star-lord as applicable)

---

## Knight-rider auto-execution after your briefing lands

Per Matt's "don't wait on decisions; trust gandalf + the hive" pillar, knight-rider auto-spawns rocket schema dispatch + gamora sim dispatch + drax renderer dispatch immediately on your briefing's § 4 contract. No Matt-wait gate.

---

## Math-before-code requirements

N/A — design briefing.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 you authored). Apply broader pull-rebase discipline before engine-repo commits if needed.

---

## Continuous-availability ramp

After this briefing ships, stay LIVE for:
- Matt L3 follow-up Q&A on any of your 5 briefings now stacked (~20+ open questions total parked)
- Implementation seam Q&A as rocket/gamora/drax consume your § 4 contract

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 sign-off pillar. Estimated 0.5-1 day. Append completion record when done.*

---

## Completion record

**Status:** COMPLETE 2026-05-17.
**Briefing:** `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` (615 lines).
**Tag intent:** `gandalf/v1.5-asymmetric-perceived-aoe-radius-briefing-1`.

All acceptance criteria satisfied:
- [x] Briefing authored at the specified path
- [x] § 2 genre-canon source validation — Matt's recall confirmed accurate; D3-RoS 2014 onward; magnitudes converge at enemy 1.10-1.15× / player 0.85-0.92×; Grim Dawn principled-rejection documented
- [x] § 4 implementation contract with explicit per-seam obligations (rocket / gamora / drax-demo / star-lord / jack-ryan / knight-rider)
- [x] § 7 direct-implementable parameter table (15 rows; numerical; consumable by rocket / gamora / drax-demo dispatches)
- [x] § 8 BINDING recommendation: substrate-agnostic at enemy 1.12× / player 0.90× for v1.0; pivot path to substrate-coupled Phase-2 documented (~2.5-3 days when wanted)
- [x] § 6 cross-impact map present (D10 / D14 / D27 / post-D10 regen / narrow-slice / prior AOE briefing / substrate identity declarations / telegraphed AOE windup / roadmap / MIGRATION.md)
- [x] § 9 + § 10 — 7 new open questions surfaced for Matt; ~23 total stacked across all gandalf briefings
- [x] Hive-log PRE-SIGNAL + STATE + HANDOFFs (rocket / gamora / drax-demo / star-lord / knight-rider) appended per § 14.1.1 discipline
- [x] Tag cut

**Cascade unblocked.** Knight-rider auto-executes rocket → gamora → drax per Matt's "trust gandalf + the hive" pillar. Total cascade duration ~2 days end-to-end with overlap.

**Continuous-availability ramp:** gandalf stays LIVE for follow-up Q&A on all 5 briefings now stacked (~23 open questions parked for Matt). Implementation-seam Q&A as rocket / gamora / drax consume § 4 contract.

— gandalf

