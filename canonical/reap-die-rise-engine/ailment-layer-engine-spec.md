# Ailment-Layer Engine Spec — damage-amp + freeze + stun + poison-dot (+ taunt annex)

**STATUS:** CURRENT — Gate-1 PASS-WITH-AMENDMENTS (jack-ryan 2026-07-16). 8 text-level amendments applied inline (see §2.6, §3.6, §5.7, §5.9, §6.3, §6.5.1, §7, §11). Specialists may build; five §10 escalation rulings stand veto-open pending Matt read.
**Date:** 2026-07-16
**Author:** gandalf (SPEC-AUTHOR work unit, autonomous run)
**Authority:** pause-2 convening 2026-07-12 item 4 (ailment-layer design session commissioned; damage-amp + freeze + stun + poison-dot as the first tranche, taunt rides Wave A, GX-15 folded) · autonomous-run delegation Matt 2026-07-16 (sub-agents iterate engine toward 100% atlas mechanical parity). **Six delegated rulings this doc records are gandalf-prime rulings under Matt's autonomous-run authority — veto-open, Matt may overturn on read.**
**Companion docs:**
- `../../agentic_orchestration/gandalf/design-inputs/ailment-layer-evidence-v1.md` — the evidence dossier (kit census · implementation-pattern tables · genre precedents)
- `../../agentic_orchestration/gandalf/views/v3-mechanics-leverage-v1.md` — pause-2 rulings block (GX-15 fold-in · DL-03 stream law · Wave-A summoner ratifications)
- `../../agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` — form model for §0/§1 and the taunt-annex proxy-layer parent
- `/Users/admin/Games/reincarnated-engine/config/ailments.yaml` — the config surface this spec extends (READ-ONLY reference)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` — `_try_apply_ailment` / `_add_or_refresh` / `_DOT_AILMENT_NAMES` (extension points)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py` — `tick_effects` (DoT tick loop; registry-driven)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/foundation/ailment_loader.py` — `VALID_CATEGORY_VALUES` (already reserves `debuff`)

---

## §0 — TL;DR

Four new ailments + one annex extension. Baseline registry today is 8 (burn, chill, root, knockback, bleed, shock, consecrate, drain — `config/ailments.yaml`). This spec adds **sunder** (working name; damage-amp; 3-candidate shortlist §2.7 → gandalf-prime picks at verify), **freeze**, **stun**, **poison** (name of the poison-DoT; `poison-dot` is the gap-code) — and a **taunt** annex parameter riding Wave A's proxy layer (already built: rocket v2.8 + gamora v1.7, `_DEFERRED_PROXY_BINS` lift LANDED via commits 4a70547 / 7aeb2a6 / 4fdd314 / 43fa149).

The four ailments answer four evidence-anchored gaps: damage-amp = **97 kits / ~21% of the 463 combat corpus** — the genre's #1 missing mechanic; freeze = 42 kits (completes the cold pair with existing chill); stun = 36 (physical hard-CC + lightning-escalation counterpart to existing shock); poison = 36 (chaos/nature DoT — the third pillar of a burn/bleed/poison triad). Taunt annex = 11 kits, all proxy-adjacent, rides Wave A.

**Design laws bound in:** GX-15 multi-element cap collisions FOLD IN under sunder as a synergy multiplier riding the Hades Privileged-Status precedent; DL-03 stream law (streams never tax movement) binds any poison-cloud or chill-freeze-escalation authoring; **engine `shock` is UNCHANGED — it is an RDR-original control-class ailment, NOT rebranded** (delegated ruling 1).

**Route:** rocket = ailments.yaml extension + emission surfaces in `generation/element_biases.py` + `geometry_derivation.py` + `substrate_templates.py`; gamora = sim resolution in `damage_resolver._try_apply_ailment` / `effect_resolver.tick_effects` / hard-control enforcement + calibration bands.

**Escalations this doc raises (5 items, count-check §10):** (a) new resource category `amplifier` for sunder (or reuse `debuff` — architectural choice); (b) shatter-hook resolution site (damage_resolver vs effect_resolver expiry); (c) stun boss-diminishing-returns model shape (timer-immunity vs stack-tracker); (d) poison stack-cap semantics (per-attacker, global, or windowed); (e) taunt aggro-priority model (target-override vs threat-generation). These are ARCHITECTURAL, not tuning — Matt/KR ruling owed before build.

---

## §1 — What already EXISTS (do not rebuild)

Per current engine survey (2026-07-16 pass on `damage_resolver.py`, `effect_resolver.py`, `ailment_loader.py`, `element_biases.py`, `geometry_derivation.py`):

| Component | File | State — for ailment-layer purposes |
|---|---|---|
| Ailment registry loader | `foundation/ailment_loader.py` | 8 canonical names FROZEN; `VALID_CATEGORY_VALUES` already includes `debuff` (RESERVED, unused) — sunder can slot in |
| Ailment YAML | `config/ailments.yaml` | 8 entries; params keyed by `min/max/default`; DoT tick_damage set at emission (dynamic) |
| Apply hook | `damage_resolver._try_apply_ailment` (:996) | RNG gate on `BASE_AILMENT_CHANCE=0.35 × (1 − status_resist)`; `_add_or_refresh` for stacking/refresh |
| Refresh law (DoT) | `damage_resolver._add_or_refresh` (:1056) | Keeps STRONGER tick_damage on refresh (F3 fix 2026-06-20); duration = max(existing, incoming) |
| DoT tick loop | `effect_resolver.tick_effects` | Registry-driven via `_DOT_AILMENT_NAMES = get_dot_ailments(_ailments)`; NEW dot ailments auto-tick |
| Soft-control enforcement | `combatant.py:375` | `slow_percent` on active_effects multiplies movement factor; chill mechanic |
| Element→ailment map | `generation/element_biases.py:66-73` | 8 elements → 8 ailments; new ailments need new emission surfaces |
| Geometry derivation | `generation/geometry_derivation.py:167-238` | Ailment-in-effects rules select delivery shapes; `_control_effects` set (:238) drives control-vs-damage classification |
| Substrate templates | `generation/substrate_templates.py:610-618` | Tag-based ailment expression (`tags=["burn"]`, `["chill","slow"]`) |
| Proxy taunt substrate | commits 4a70547/7aeb2a6/4fdd314/43fa149 (rocket v2.8, gamora v1.7) | **BUILT.** Proxy emission gate LIFTED; positioned-ally + AI branches operational — taunt rides this layer as a parameter, NOT a new subsystem |
| Attribution spine (E3) | `damage_resolver.py:1044` stamps `source_element` on DoT ActiveEffect | Byte-pure; carries into telemetry — new DoTs inherit this stamp automatically |

**Existing extension points these ailments plug into (no new subsystems required for 3 of 4):**
- Freeze = new `hard_control` entry (parallel to root/knockback/shock) + a new shatter-payoff hook (ESCALATION b)
- Stun = new `hard_control` entry + new diminishing-returns model (ESCALATION c)
- Poison = new `dot` entry — `_DOT_AILMENT_NAMES` refresh at load auto-includes it; tick loop already handles it; refresh-max-tick law applies
- Sunder = new architectural class (`amplifier` category OR `debuff` reuse — ESCALATION a) — needs new sim-side consumer at damage-multiplier point

---

## §2 — Ailment: `sunder` (damage-amp; genre's #1 missing mechanic)

### 2.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

- **Engine `shock` is UNCHANGED** — RDR-original paralysis-on-arc control-class ailment. Genre's %-increased-damage-taken mechanic enters as a NEW ailment.
- **Name working: `sunder`** (final pick from §2.7 shortlist reserved for gandalf-prime at verify gate).
- **"marked" is EXCLUDED** — Wave C ships mark-and-consume mechanics per pause-2 §3; the collision is reserved.

### 2.2 Mechanic definition

Sunder is a **timed % increased damage taken debuff** on a target. Unlike DoTs (which deal damage themselves), sunder amplifies damage from ALL other sources delivered to the target during its window. Not a stat-shred (which is permanent-while-in-range) but a per-target timed multiplier — the D4 Vulnerable / PoE1 shock-magnitude / GD RR-window archetype fused into one canonical primitive.

**Genre precedent** (evidence dossier §1b/1c):
- **D4 Vulnerable** — flat 20% increased damage taken, 2–4s window, no stacking. Simplest form.
- **PoE1 shock** — % increased damage taken scaling with the lightning-damage hit that applied it; capped 50%; ~2–4s. Scaling form.
- **PoE2 armor-break** (poe2-titan-hotg) — prerequisite gate: without break, hammer does less damage. Mark-and-consume form (Wave C territory; sunder overlaps only in that armor-break IS a sunder shape).
- **GD Resistance Reduction** — stacked to a resist floor; effectively persistent while in radius. Persistence-form; RDR sunder is TIMED not persistent (persistence lives at gear-affix / aura layer, not ailment layer).
- **Hades Privileged Status** — the multi-status-cap multiplier: 2+ status effects → damage-amp multiplier. **THIS binds under GX-15 fold-in** (§2.10 below).

### 2.3 Category classification (ARCHITECTURAL ESCALATION a)

**Options:**
- **(a) Reuse `debuff` category** — already `RESERVED` in `VALID_CATEGORY_VALUES` (`ailment_loader.py`). Fits: sunder is not control, not DoT, not amplification-zone (consecrate). Sim consumer wires into damage_resolver output.
- **(b) New category `amplifier` distinct from `amplification`** — semantic clarity (amplification is zonal/valenced-per-side per consecrate; amplifier is per-target-timed-multiplier). Requires ailment_loader schema extension.
- **gandalf lean: (a) `debuff`.** The reserved slot exists for exactly this class; a new category duplicates concept space. Semantic distinction: `amplification` = zonal-valenced (consecrate's ally-heal + enemy-DoT split); `debuff` = per-target stat/multiplier modification (sunder's damage-taken increase). Clean split.

**ESCALATION a — Matt/KR ruling owed:** ratify (a) or (b) before rocket writes the YAML entry. Impact: one-line category choice + whether sim consumer branches on `category=="debuff"` (a) or `category=="amplifier"` (b).

### 2.4 Params + defaults + ranges (ailments.yaml-shaped)

Assuming ruling (a) `debuff`. If (b), same shape, category field differs.

```yaml
- name: sunder
  description: >
    Timed % increased damage taken. Sunder does not deal damage itself — it
    amplifies damage from all sources delivered to the target during its window.
    The genre's canonical damage-amp primitive (D4 Vulnerable / PoE1 shock-magnitude
    lineage / GD RR-window archetype). Composes multiplicatively with source-side
    damage multipliers; caps at max_amp to prevent runaway stacking.
  is_control: none
  category: debuff  # (or "amplifier" pending ESCALATION a)
  param_ranges:
    damage_taken_percent:
      min: 0.10      # floor: low-tier lightning proc, single stack
      max: 0.50      # ceiling: PoE1 shock cap analog; hard runaway guard
      default: 0.20  # D4 Vulnerable analog
    duration_seconds:
      min: 2.0       # D4 Vulnerable low
      max: 5.0       # PoE1 shock high with duration investment
      default: 3.0   # genre median
    max_amp_cap:
      min: 0.50
      max: 0.50
      default: 0.50  # HARD ceiling on stacked sunder — see §2.6 stacking law
  ai_priority: 2     # AI applies before DoT for multiplier composition (bulk hits benefit)
```

**Calibration ranges (gamora tunes within rails):** `damage_taken_percent` default may shift 0.15–0.25 depending on the S6 gauntlet response; `max_amp_cap` LOCKED at 0.50 (runaway-guard invariant — do not tune).

### 2.5 Application sources (which skill verbs/geometries apply it)

- **Lightning-element skills** — sunder rides lightning as a primary rider (analogous to how shock/lightning is bound in `element_biases.py:71`). This routes the 67-of-100 lightning-heavy gap-citation weight (evidence §1d convergence) into the natural element home.
- **Physical-heavy skills with armor-break tag** — a sub-family: heavy physical hits (mace, hammer, sunder-verb-adjacent) roll sunder as an armor-shred narrative. Rocket routes via a new `armor_break` tag in `substrate_templates.py`.
- **Curse/hex delivery pattern** — rocket-authored curse-shape skills (single-target debuff, area debuff cloud) roll sunder as the payload; distinct from DoT curses.
- **Shadow flavor (bounded)** — a shadow sub-family (necrotic-weakness / vitality RR / life-reduction narrative per LE precedent evidence §1b Pattern F) may roll sunder at reduced magnitude. Not the primary home; keeps shadow's drain identity dominant.
- **NOT holy** (consecrate owns the amplification-zone niche; sunder is timed-per-target and would collide narratively).
- **NOT wind / ice / earth / fire / physical-DoT-native** — these have their own signature ailments already dominant.

Rocket authorship touchpoint: `element_biases.py` gets a NEW element-ailment map entry (or extend the existing map to allow sunder as a secondary map keyed off a `role` or `signature` slot; RECOMMEND: keep primary map as-is, add a `SECONDARY_AILMENT_MAP` that stamps sunder-eligible skills).

### 2.6 Stacking / refresh law

- **Single-instance-per-target** — sunder is NOT stack-additive (unlike poison §5.5). Only ONE sunder `ActiveEffect` ever coexists on a defender. Re-application refreshes duration to `max(existing, incoming)` and takes the **max damage_taken_percent** (mirrors `_add_or_refresh`'s F3 DoT-refresh law at `damage_resolver.py:1075-1087` — the LATER application does not weaken the LIVE stronger amp; consistent with the max-tick preservation for DoTs).
- **Cap invariant** — because sunder is single-instance-per-target, the per-target effective amp is `min(max_amp_cap, current_amp)`. Since `damage_taken_percent.max = 0.50` and `max_amp_cap = 0.50`, the cap is a defense-in-depth invariant against parameter drift; it does NOT compose across multiple simultaneous sunder ActiveEffects (there is only ever one). Multi-caster / multi-skill scenarios follow the max-magnitude refresh rule above — the stronger amp wins for the union of durations.
- **Duration composition** — `attacker.ability_modifiers["control_duration_bonus"]` (already applied at `damage_resolver.py:1039`) applies to sunder duration.
- **Amendment note (jack-ryan Gate-1 2026-07-16):** original wording proposed a `min(cap, sum_of_active_amps)` cross-source sum-cap that CONTRADICTED single-instance-per-target. Resolved to (option 2) single-instance + max-magnitude refresh + cap-as-invariant. §7 "sunder × sunder | REFRESHES + summed cap" amended to reflect this.

### 2.7 Name shortlist (delegated ruling 2 — gandalf-prime picks at verify)

Three launder-clean candidates. **RULED at verify-gate (gandalf-prime, 2026-07-16, veto-open): `sunder`.** Grounds beyond the lean below: the broader action-RPG-adjacent lineage ("Sunder Armor"-class stacking take-more-damage debuffs) makes "sunder = you take more damage now" instantly legible to veterans while **no ARPG in our corpus owns it as ailment identity**; the PoE1 skill named Sunder is a slam attack — a skill-name-layer collision, not an ailment-vocabulary one (RDR skill names are per-kit LLM-generated; ailment vocabulary is engine-internal). It also bridges the lightning primary home to the physical armor-break secondary home (§2.5) in one word. `expose` carries real PoE-Exposure adjacency (a named late-PoE1 mechanic — more laundering risk than first rated); `weaken` actively misleads D2 veterans via the invert-flip. Other two archive.

| Candidate | Lineage note (proves launder-clean) |
|---|---|
| **`sunder`** | Genre-generic English verb; no single ARPG owns it as its signature damage-amp identity. Sundering Charm exists in PoE (a currency, not an ailment); GD/D3 use "sunder" in item names / passives incidentally. Evokes armor-break + heavy-physical narrative naturally — bridges the lightning primary home to the physical secondary home (§2.5). **gandalf lean.** |
| **`expose`** / `exposed` | LE uses "Exposed" for armor-RR (evidence §1b Pattern F — le-dive-bomb-falconer). Not iconic; LE's ailment ecosystem is broad and Exposed is one of many. D2 uses "expose" in passive language (Expose Weakness curse variant). Genre-generic vocabulary. Slight LE-flavor risk. |
| **`weaken`** | D2 Necromancer curse (Weaken — reduces enemy damage OUT; RDR would flip to damage IN). PoE1 curse Enfeeble/Weakness. Widely-distributed genre-generic English. Slight D2-flavor risk (D2 semantic is enemy-damage-reduction, RDR is target-damage-taken — invert-flip may confuse veterans). |

**Excluded by ruling:** `marked` (Wave C collision), `vulnerable` (D4-signature-owned), `frailty` (D2 Necromancer curse — signature-owned even if obscure).

### 2.8 Sim-side resolution point (which damage_resolver path consumes it)

**Consumer site:** `damage_resolver.resolve_skill` — the final damage-multiplier composition point (where `damage_modifier`, `buff_damage`, `bonus_damage_percent` compose). Sunder reads the defender's `active_effects` for `name=="sunder"`, computes `min(max_amp_cap, sum_of_active_percents)`, and applies `raw_damage *= (1 + sunder_amp)` at the composition step.

**Placement:** AFTER attacker-side buff composition, BEFORE defender-side mitigation. Sunder amplifies the damage the mitigation formula operates on (mirrors how the genre models it — Vulnerable/shock are pre-mitigation multipliers).

**gamora scope:** add sunder-amp lookup + apply at `resolve_skill` composition; wire into damage-tick path in `effect_resolver.tick_effects` (DoTs on a sundered target ALSO benefit — genre-canonical; evidence §1b Pattern G wither+poison pairing).

**Attribution:** sunder-amp contribution to total damage is telemetrable via existing E3 attribution spine (`source_element` stamp) IF sunder is stamped with the applier's element. Extend E3 pass: stamp `source_element` on sunder ActiveEffect same as DoTs.

### 2.9 Gen-side emission surface (how kits roll it)

- **`element_biases.py`** — add a `SECONDARY_AILMENT_BIAS` map; lightning-primary skills roll sunder as secondary rider at rocket-tuned rate (LEAN: 0.25 probability at emission; gamora may re-tune).
- **`geometry_derivation.py:_control_effects`** — sunder does NOT go here (it is not a control ailment — is_control=none). Sunder DOES enter `_damage_effects` OR a new `_amplifier_effects` set — impacts geometry routing rules. RECOMMEND: new `_amplifier_effects = {"sunder", "consecrate"}` to keep the concept-space clean.
- **`substrate_templates.py`** — new templates: `lightning_sunder_bolt`, `curse_of_sundering` (single-target sunder verb), `armor_shatter_smash` (physical-secondary sunder-carrier).

Rocket authorship: emission surface + config entry + tag routing. Gamora authorship: sim consumer + calibration.

### 2.10 GX-15 fold-in — the sunder-synergy multiplier (Privileged Status precedent)

**Ruling from pause-2 §5:** GX-15 multi-element cap collisions FOLDED into ailment-layer damage-amp design as an ailment-synergy question. This is where it lands mechanically.

**Design:** when a target carries **2 or more distinct ailments simultaneously** (any combo of the 12-total post-Wave-A registry, excluding sunder itself), sunder's `damage_taken_percent` receives a `synergy_bonus` multiplier at consumer read-time. Threshold gate is BINARY (Hades authored the cap at exactly 2 — the corpus's clean binary gate) OR INCREMENTAL (PoE Discharge scales with count — the two divergent poles per evidence §1e).

**gandalf lean: BINARY at threshold=2, additive bonus.** Reads clean; matches Hades precedent verbatim; avoids runaway stacking (already guarded by `max_amp_cap`); binary threshold is easier to communicate to the player (2+ ailments = amped).

```yaml
    synergy_threshold_count:
      min: 2
      max: 2
      default: 2
    synergy_bonus_percent:
      min: 0.05
      max: 0.15
      default: 0.10   # +10 pp when target carries 2+ non-sunder ailments
```

**Sim consumer extension:** at `resolve_skill` sunder composition, count `distinct non-sunder ailments on defender.active_effects`; if >= threshold, add `synergy_bonus_percent` to the summed sunder-amp before cap.

**This binds GX-15 in and satisfies the pause-2 fold-in ruling** — GX-15 does NOT need a standalone spec. It IS sunder's synergy modifier.

### 2.11 Calibration guardrails (gamora tunes)

- **HARD guard: `max_amp_cap=0.50`** — do not exceed; stacking runaway would break S6.
- **SOFT guard: default damage_taken_percent 0.20** — tune band 0.15–0.25 based on S6 response.
- **Sunder+DoT interaction check:** sunder amplifies DoT ticks. Composing sunder with a stacked poison could produce spikes. Gamora smoke-gate: sunder@max × poison@max-stacks vs baseline; if delta > 3× baseline burst, reduce sunder cap OR poison stack cap (poison side per §5.5).
- **Boss encounter check:** sunder on bosses composes with sunder-persistence-across-hits. Verify boss encounters do not become one-shot when player invests in sunder duration + damage_taken_percent.

### 2.12 DL-03 conformance

Not directly applicable to sunder (sunder is a debuff, not a stream/beam). Design law noted for cross-check.

---

## §3 — Ailment: `freeze` (hard end of cold ladder; shatter payoff)

### 3.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**Freeze = the hard end of the cold ladder.** Chill (existing) is entry (soft_control, 20–50% slow); freeze is completion (hard_control, full immobilization) + shatter-payoff hook on freeze-break OR freeze-expiry-under-HP-threshold.

### 3.2 Mechanic definition

Freeze applies **full movement + action immobilization** for a timed window. On duration expiry, if defender is under a shatter-HP-threshold (or dies during freeze), triggers a **shatter damage event** — a burst payoff pattern that closes the two-phase freeze→shatter loop the genre expects (evidence §2b Pattern A cross-game consensus: D2/D4/PoE1/PoE2/LE/Chronicon all model it).

**Genre precedent** (evidence §2b):
- **PoE1/PoE2 freeze** — buildup threshold model (cold accumulates; freeze fires when threshold crossed). RDR simplifies to per-hit RNG gate (matches existing chill/root/shock model).
- **D2 Frozen Orb / D4 Ice Shards** — freeze rider + shatter narrative; auto-targeting of frozen enemies is a D4 pattern (deferred; not this spec).
- **PoE2 Ice Strike Invoker** — freeze=core, shatter=payoff, two-phase loop. Highest-signal exhibit.
- **PoE2 Cast-on-Freeze Comet** — freeze-as-proc-trigger. **DEFERRED** to future proc-grammar work (Wave C territory per pause-2 §3 wave order).
- **Hades2 Hail Storm** — freeze-triggers-lightning cross-element engine. Also DEFERRED (satisfies sunder synergy multi-status precedent, not native freeze mechanic).

### 3.3 Params + defaults + ranges

```yaml
- name: freeze
  description: >
    Full movement + action immobilization. The hard end of the cold ladder —
    chill (soft slow) escalates to freeze (hard lock). On expiry, if defender
    HP is below shatter_threshold_fraction, applies shatter_damage_percent
    of defender max HP as a burst damage event.
    Cold element's hard-control primitive; completes the chill/freeze pair.
  is_control: hard
  category: hard_control
  param_ranges:
    duration_seconds:
      min: 0.5     # short freeze at low investment
      max: 3.0     # long freeze at high investment (genre range top per evidence §2c)
      default: 1.5 # median band; less than root (2.5) — freeze is more punishing so shorter
    shatter_threshold_fraction:
      min: 0.15
      max: 0.35
      default: 0.25  # defender must be under 25% HP at freeze-expiry for shatter to fire
    shatter_damage_percent:
      min: 0.10
      max: 0.30
      default: 0.20  # burst = 20% defender max HP
  ai_priority: 1     # hard-control fires first (mirrors root, shock)
```

**Calibration ranges (gamora):** duration_seconds default may shift 1.0–2.0; shatter_damage_percent tuned against S6 boss-encounter response — do not exceed 0.30 (one-shot risk on bosses).

### 3.4 Application sources

- **Ice-element skills** — freeze rides ice as SECONDARY (chill remains primary per `element_biases.py:67`). Skills with high magnitude OR "hard" role tag roll freeze; skills with low magnitude OR "control" role tag with slow_percent already carry chill (existing).
- **Cold-DoT overkill** — a skill that has already applied chill AND lands a heavy secondary hit may escalate chill→freeze (deferred to a future escalation-mechanism ruling; not this spec).
- **NOT other elements** — freeze is cold-locked (mirrors how burn is fire-locked, bleed is physical-locked at the element-bias layer).

Rocket authorship: extend `element_biases.py` — ice element maps to `[chill (primary), freeze (secondary)]`. Skill-emission logic rolls freeze on ice-magnitude-heavy or ice-hard-control-tagged skills.

### 3.5 Stacking / refresh law

- **Refresh duration only** — freeze is a hard-lock; re-applying refreshes to `max(existing, incoming)` duration. NO magnitude stacking (freeze is boolean: locked or not).
- **Chill+freeze coexist** — a target may carry chill AND freeze simultaneously (freeze does not clear chill). On freeze-break, chill remains and continues to slow. This models the genre pattern (freeze fades → still chilled).
- **Diminishing returns on repeated freeze** — DEFERRED to §4 stun DR ruling. If stun gets DR, freeze may adopt the same model (parallel escalation §11).

### 3.6 Sim-side resolution point

- **Application:** `damage_resolver._try_apply_ailment` — no change; freeze is a standard hard-control add via the existing gate.
- **Immobilization enforcement:** NEW consumer in `combatant.py` — while `active_effects` contains `name=="freeze"`, defender's movement_factor=0 AND action_ready=false. Analogous to how `slow_percent` composes at `combatant.py:375`; freeze is the terminal case (full lock).
- **Shatter hook (ESCALATION b):** where does shatter damage resolve?
  - **(i) `effect_resolver.tick_effects` expiry path** — when freeze's `duration_remaining` hits 0, check `defender.hp / defender.max_hp < shatter_threshold_fraction`; if true, apply `shatter_damage_percent * defender.max_hp` as damage event. **Placement precision (jack-ryan Gate-1 2026-07-16):** the shatter check must fire when freeze's decrement inside the tick loop (`effect_resolver.py:59`) drops `duration_remaining <= 0`, BEFORE the expiry cull at line 95 (`combatant.active_effects = [e for e in ... if e.duration_remaining > 0]`). Otherwise the effect is culled before the check reads it. Concretely: after line 59's decrement, if `effect.name == "freeze"` and `effect.duration_remaining <= 0` and `combatant.hp / combatant.max_hp < shatter_threshold_fraction`, apply shatter damage.
  - **(ii) `damage_resolver` on-hit trigger** — a heavy cold hit on a frozen target consumes the freeze and triggers shatter immediately (PoE2 Ice Strike model).
  - **gandalf lean: (i)** — cleaner architecturally; keeps shatter as an ailment-lifecycle event (parallels how DoTs tick in effect_resolver). (ii) mixes concerns and creates a two-seam interaction (Discipline #11). But (ii) is more player-satisfying (immediate feedback vs delayed expiry burst).
  - **ESCALATION b — Matt/KR ruling owed:** ratify (i) or (ii) or hybrid before gamora builds. Impact: which module owns shatter; whether shatter is expiry-triggered or hit-triggered.

### 3.7 Gen-side emission surface

- `element_biases.py` — ice element gets `[chill, freeze]` as ordered list; emission logic per-skill selects one or both based on magnitude/role.
- `geometry_derivation.py` — freeze enters `_control_effects` set (line 238) alongside root/knockback/shock. New rules likely: `freeze + role=control → ground_targeted_circle` (mirrors burn+DoT geometry); `freeze + role=burst_damage + element=ice → melee_arc` (shatter narrative).
- `substrate_templates.py` — new templates: `ice_freeze_field` (chill+freeze paired area), `frost_nova_shatter` (radial freeze + immediate shatter attempt), `deep_freeze_bolt` (single-target long-freeze).

### 3.8 Calibration guardrails

- **HARD guard: shatter_damage_percent ≤ 0.30** — boss one-shot invariant.
- **CC-density guard:** freeze + chill dual-active = target locked >50% of engagement window. S6 must verify player agency preserved (not all mobs freeze-locked in perpetuity).
- **PvE-only:** freeze is a hard-lock; multiplayer PvP considerations OUT OF SCOPE per solo-only project premise.

### 3.9 DL-03 conformance

Freeze does NOT tax movement of the CASTER. It taxes movement of the TARGET (that's what it does). DL-03 applies to caster commitment; freeze is well outside its scope. Confirmed non-collision.

---

## §4 — Ailment: `stun` (short hard CC; boss-resistance parameter)

### 4.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**Stun = short hard CC (sub-second to ~1.5s band).** Includes boss-resistance parameter (diminishing returns OR flat resist tier — §4.6 shape ESCALATION c).

### 4.2 Mechanic definition

Stun applies **brief full action-interrupt** — target cannot act (movement + attack + cast) for a very short window. Physical hard-CC counterpart to lightning's shock; also the hard-CC head of the lightning ladder (evidence §3b Pattern B: shock+stun frequently co-emitted on lightning kits).

**Genre precedent** (evidence §3b):
- **PoE1 stun (poe1-heavy-strike-stun)** — HP-% threshold model. Heavy hits exceed target's stun threshold to apply.
- **D2 Smiter / Singer / BvC** — physical heavy-hit stun; per-hit apply, no threshold.
- **Hades stagger (hades1-beowulf-cast)** — vocabulary variant; functionally equivalent. RDR unifies under "stun."
- **HoT stun-density** — 6 kits normalizing stun as common rider. HoT-style universal application would flood the sim; RDR resists that pattern via boss resistance + short duration.
- **PoE1/PoE2 stun immunity timers** — after being stunned, target has brief immunity. This IS the DR shape §4.6.

### 4.3 Params + defaults + ranges

```yaml
- name: stun
  description: >
    Brief full action interrupt (movement + attack + cast). Short-duration hard
    CC; the physical heavy-hit primitive + lightning-ladder hard-CC counterpart
    to shock. Bosses receive stun_resistance_tier reduction — see interaction
    with immunity_after_seconds diminishing-returns law.
  is_control: hard
  category: hard_control
  param_ranges:
    duration_seconds:
      min: 0.3     # brief interrupt / grenade concussion
      max: 1.5     # heavy-hammer full stun
      default: 0.7 # median physical hit
    stun_resistance_tier_boss:
      min: 0.50
      max: 0.90
      default: 0.75  # bosses take 75% of nominal duration (25% resist)
    immunity_after_seconds:
      min: 1.0
      max: 3.0
      default: 2.0   # after stun expiry, target immune to new stun for 2s (DR law)
  ai_priority: 1     # hard-control fires first alongside root/shock/freeze
```

### 4.4 Application sources

- **Physical-element skills with `heavy_hit` tag** — melee weapon skills, mace/hammer archetypes, shield-bash verbs. Rocket authorship: new `heavy_hit` tag on substrate_templates.
- **Lightning-element skills** — stun rides lightning as a secondary control (shock stays primary). Skills with high-magnitude lightning or chain-lightning archetype roll stun as escalation on target-focus hits.
- **Grenade / concussive-explosive geometries** — thrown-explosive substrate templates (per evidence §3b Pattern C gd-canister-saboteur, poe2-witchhunter-grenades) roll stun as concussive rider.
- **NOT DoT-based skills** — stun requires an impact event; DoT-tick sources are ineligible.

Rocket authorship: extend `element_biases.py` — lightning gets `[shock (primary), stun (secondary)]`; physical gets `[bleed (primary), stun (secondary via heavy_hit tag)]`.

### 4.5 Stacking / refresh law

- **Single-instance** — stun is boolean; re-apply refreshes duration.
- **Immunity-after-expiry law** — after stun expires, target carries `stun_immune_until = current_time + immunity_after_seconds`. New stun applications during immunity window are DROPPED (not silenced-and-retried; hard drop).
- **Chill/root/freeze co-existence** — stun coexists with other hard-controls (all can apply simultaneously; target is locked until longest-remaining lifts).

### 4.6 Boss-resistance model (ARCHITECTURAL ESCALATION c)

**Options:**
- **(a) Flat multiplier `stun_resistance_tier_boss`** — bosses receive stun at `duration × tier_multiplier` (already YAML-shaped above). Simple, single parameter. Genre model: PoE1 boss stun-threshold is very high (bosses rarely stun).
- **(b) Stack-tracker diminishing returns** — track `stun_recent_count` on defender; each stun in a window reduces next stun's duration (0.9× → 0.7× → 0.5× → 0). Genre model: DarkSouls/monster-hunter poise mechanics.
- **(c) Hybrid** — bosses get flat multiplier AND all targets get immunity-after-expiry. Cleanest genre-fit.

**gandalf lean: (c) hybrid.** Immunity-after-expiry (§4.5) is a universal law (mirrors PoE stun immunity); boss flat multiplier layers on top. This is (a)+immunity-law — I have already shaped params to support (c).

**ESCALATION c — Matt/KR ruling owed:** ratify hybrid model (c) or downgrade to (a)-only. Impact: whether `immunity_after_seconds` is universal (all targets) or boss-only.

### 4.7 Sim-side resolution point

- **Application:** `_try_apply_ailment` — extend gate to check `defender.stun_immune_until > current_time`; if immune, drop and do not apply.
- **Immobilization enforcement:** same as freeze (NEW consumer in `combatant.py` — full action + movement lock while stun active).
- **Boss-multiplier apply:** at `_try_apply_ailment` duration composition, check `defender.is_boss` (existing? — gamora verifies); if boss, apply `duration *= stun_resistance_tier_boss`.
- **Immunity stamp:** on stun expiry in `effect_resolver.tick_effects`, stamp `defender.stun_immune_until = current_time + immunity_after_seconds`.

### 4.8 Gen-side emission surface

- `element_biases.py` — lightning `[shock, stun]`, physical `[bleed, stun (heavy_hit)]`.
- `geometry_derivation.py` — stun enters `_control_effects` (line 238). New rules: `stun + role=burst_damage + physical → melee_strike`; `stun + role=area_damage + explosive tag → ground_targeted_circle`.
- `substrate_templates.py` — new templates: `heavy_smash_stun` (physical melee), `thunder_clap_stun` (lightning secondary), `concussion_grenade` (thrown-explosive).

### 4.9 Calibration guardrails

- **HARD guard: stun duration ≤ 1.5s** — stun is BRIEF by design; longer becomes freeze territory.
- **HARD guard: immunity_after_seconds ≥ 1.0s** — prevent stun-locking (perma-stun via rapid re-apply).
- **CC-diversity guard:** stun + shock co-exist (both hard-lock lightning); S6 must verify a lightning kit does not become a permanent-CC engine.

### 4.10 DL-03 conformance

Stun taxes target movement, not caster movement. Non-collision.

---

## §5 — Ailment: `poison` (stack-additive DoT distinct from burn)

### 5.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**Poison = stack-additive DoT, mechanically DISTINCT from burn.**

- Burn (existing) = single-instance DoT (registry semantics; refresh keeps stronger tick).
- Poison = per-application additive stacking with independent durations (each hit adds a new poison instance; each instance ticks independently until its own duration expires).

### 5.2 Mechanic definition

Poison is chaos/nature/corrosive DoT. Each hit that applies poison adds a NEW poison instance to the defender; each instance ticks independently at `tick_damage` per `tick_interval` until its `duration_remaining` reaches 0. Multiple poison instances coexist. Stack cap governs runaway (§5.5).

**Genre precedent** (evidence §4b):
- **PoE1 Viper Strike / Caustic Arrow** — per-hit stacking chaos DoT. Genre-canonical model.
- **D2 Poison Javazon / Nova / Rabies** — D2 uses single-tick highest-value model (simpler; not what RDR adopts).
- **D3 Jade Harvester** — DoT-stack-consume (Wave C mark-and-consume territory; NOT this spec).
- **D2/D4 Rabies contagion** — spread-on-death sub-pattern (evidence §4b Pattern C). **DEFERRED** to future contagion-mechanic work; NOT this spec.
- **PoE1 Wither** — chaos RR paired with poison. This is where sunder+poison synergy naturally emerges (§5.10 interaction).

### 5.3 Params + defaults + ranges

```yaml
- name: poison
  description: >
    Chaos / nature / corrosive DoT. Distinct from burn (single-instance fire DoT) —
    poison is STACK-ADDITIVE: each application adds a new independent instance with
    its own tick_damage and duration. Multiple stacks coexist; each ticks
    independently until expiry. Stack cap prevents runaway. The third pillar of
    the DoT triad alongside burn (fire) and bleed (physical).
  is_control: none
  category: dot
  param_ranges:
    tick_damage:
      min: 0.0
      max: 0.0
      default: 0.0
      note: set dynamically from base_mag at generation time (mirrors burn/bleed/drain)
    duration_seconds:
      min: 2.0
      max: 6.0
      default: 4.0     # shorter than burn (5.0) — stacks compensate for tick life
    stack_cap_per_attacker:
      min: 5
      max: 10
      default: 8       # PoE1-inspired cap; runaway-guard
  ai_priority: 4       # AI applies alongside burn/drain
```

### 5.4 Application sources

- **Physical-element skills with `venom` / `toxin` tag** — assassin dagger, viper strike-adjacent verbs, poison-coating narrative.
- **Shadow-element skills** — poison rides shadow as a secondary DoT (drain remains primary per `element_biases.py:73`). Chaos/necrotic overlap.
- **Nature/beast archetype substrate** (rocket-authored) — druid-adjacent, beast-form kits (rabies-lineage narrative).
- **NOT fire / ice / earth / wind / lightning / holy** — element identity guard.

Rocket authorship: extend `element_biases.py` — physical `[bleed (primary), poison (venom_tag)]`, shadow `[drain (primary), poison (chaos_tag)]`. New `venom` + `chaos` tags in substrate_templates.

### 5.5 Stacking / refresh law (THE key mechanical distinction from burn)

**Poison DOES stack.** This diverges from `_add_or_refresh` semantics for burn/bleed/drain (which refresh single-instance with max-tick preservation).

**Options (ARCHITECTURAL ESCALATION d):**
- **(a) Independent-stack model** — each poison application adds a separate `ActiveEffect` with its own duration + tick. `_add_or_refresh` special-cases poison to APPEND rather than refresh. Stack cap enforced at append time (drop oldest OR drop lowest-tick OR drop new — pick one).
- **(b) Rolling-aggregate model** — single `ActiveEffect` for poison; each new application ADDS its `tick_damage` to the aggregate and extends duration by a share. Simpler tick math; loses PoE1 stack-visualization identity.
- **(c) Per-attacker stack cap, global tick sum** — track poison stacks per attacker (for stack cap enforcement) but sum tick_damages into a single tick number at read-time (single tick per interval, additive magnitude).

**gandalf lean: (a) independent-stack model.** Matches PoE1 the closest (genre-signal strongest); each stack ticks visibly; player can see stacks accumulate. Requires `_add_or_refresh` special-case AND a new `active_effects` entry per stack (memory footprint scales with cap).

**Stack-cap eviction on overflow (LEAN):** drop OLDEST stack (FIFO). PoE1 convention. Rationale: rewards continuous poison application; punishes stopping.

**ESCALATION d — Matt/KR ruling owed:** ratify (a), (b), or (c) before gamora builds. Impact: `_add_or_refresh` change scope; memory footprint; player-visible stack semantics.

**Duration refresh interaction:** each stack has its OWN duration_remaining; a new stack does NOT refresh existing stacks (they age independently). This is the PoE1 model.

### 5.6 Sim-side resolution point

- **Application:** `_try_apply_ailment` — special-case poison to enter through a NEW `_add_poison_stack` path (not `_add_or_refresh`). This path:
  1. Count existing poison stacks by attacker on defender.
  2. If count >= stack_cap_per_attacker, evict oldest (LEAN).
  3. Append new stack.
- **Tick:** `effect_resolver.tick_effects` — no change; each poison stack is a distinct `ActiveEffect`, each ticks per existing DoT logic.
- **Attribution:** E3 `source_element` stamp applies per-stack.

### 5.7 Gen-side emission surface

- `element_biases.py` — new secondary-ailment routing (see §5.4).
- `geometry_derivation.py` — poison enters `_damage_effects` set (line 239) alongside burn/bleed. New rules: `poison + role=damage_over_time + physical tag=venom → melee_strike`; `poison + role=area_damage + shadow → ground_targeted_circle` (poison cloud narrative). **Note (jack-ryan Gate-1 2026-07-16):** the existing `_control_effects` set at line 238 currently contains `drain` (a DoT), inherited from a pre-Wave-A precedent where the set doubles as a "disqualify pure_utility_effects" filter. Rocket authorship: DO NOT add poison to `_control_effects` — poison is a DoT with `is_control: none`, matches burn/bleed treatment. The drain-in-control-set inconsistency is pre-existing and out of scope.
- `substrate_templates.py` — new templates: `venom_strike` (per-hit poison-carrier), `toxic_cloud` (area poison-ground), `corrupting_touch` (shadow poison rider).

### 5.8 Calibration guardrails

- **HARD guard: stack_cap_per_attacker ≤ 10** — memory/perf guard; visualization guard.
- **DPS composition guard (gamora smoke-gate):** poison@max-stacks × sunder@max should not exceed the direct-hit baseline of an equivalent-tier physical kit by more than 2×. If it does, reduce poison stack cap or reduce tick_damage seed.
- **Boss encounter guard:** poison DoT + sunder + long boss fight = risk of over-time nuke. Verify boss DPS-taken bands.

### 5.9 DL-03 conformance

Poison-cloud (`toxic_cloud` template) is a placed ground zone. If authored as a stream/channel (caster holds cloud active), DL-03 binds: stream must not tax movement. **jack-ryan Gate-1 ruling (2026-07-16, per §11 explicit deferral):** `toxic_cloud` MUST be authored place-and-forget — use `tags=["placed"]` following the existing precedent set by `bomb_mine`, `turret`, `totem`, `zone_teleport_shadow`, `sentinel`, `wall`, `wind_cyclone_zone`, `holy_sanctify_zone` in `substrate_templates.py`. Do NOT use `tags=["channel"]` (the `hp_cost_channel_*` family shape) — that would create a caster-held cloud that taxes caster movement, violating DL-03. Rocket authorship binding.

### 5.10 Interaction highlights

- **Poison + sunder (§2)** — sunder amplifies poison ticks (already handled by §2.8: sunder applies at damage composition, ticks included). Genre-canonical (PoE1 wither+poison). No new work.
- **Poison + freeze (§3)** — poison ticks continue while target is frozen (freeze locks movement/action, does not stop DoT). Consistent with genre.
- **Poison + burn** — coexist; different DoTs on same target both tick. NO merger.

---

## §6 — Taunt Annex (proxy-layer parameter riding Wave A)

### 6.1 Wave A is BUILT (as of 2026-07-16)

Confirmed via commits 4a70547 / 7aeb2a6 / 4fdd314 / 43fa149 (rocket v2.8 + gamora v1.7, proxy emission gate LIFTED). The Wave-A summoner/proxy engine spec (`wave-a-engine-spec-2026-07-13.md`) is largely operational: positioned-ally spawn, re-summon fight-loop, proxy commitment clock, proxy-AI behavior branches, `_DEFERRED_PROXY_BINS = {}` (lifted).

Taunt rides this machinery as a **parameter, not a new subsystem.** No new ailment loader entry required IF taunt is modeled as a proxy-AI directive; a full ailment loader entry IS required IF taunt is modeled as a target-side ailment (see §6.4 ESCALATION e).

### 6.2 Mechanic definition

**Taunt = enemy-targeting override.** An enemy under taunt from proxy P will preferentially attack P instead of the player. In solo ARPG context (per project premise) taunt is always **proxy-mediated** (a summoner's pet taunts) or **tank-self-taunt** (a build wants to be attacked; e.g., Thorns-Templar Chronicon exhibit).

**Genre precedent** (evidence §5b):
- **8 of 11 taunt kits are summoner/proxy chassis** — taunt = pet's aggro-generation.
- **1 exception: chr-thorns-templar** — tank-identity taunt where player wants to be attacked for damage-reflection payoff.
- **1 exception: di-druid-bear / tq2-bastion-tank** — melee form / tank-warfare identity.

### 6.3 Params (rides proxy layer, minimal new work)

Two possible representations:

**Representation A — Proxy-AI directive (LEAN):**
Add `taunt_priority: float [0.0, 1.0]` in `proxy_vocabulary_bridge.py`. **Post-Wave-A code shape (verified 2026-07-16 jack-ryan Gate-1):** the existing maps are `PROXY_TYPE_TIER` (int) and `PROXY_TYPE_TARGETING` (string, one of `nearest|player_target|taunt|intercept|positional|proximity|none`). There is NO `PROXY_TYPE_BEHAVIOR` map by that name. `golem_construct` already carries `targeting_behavior="taunt"`. Rocket authorship: add a NEW parallel map `PROXY_TAUNT_PRIORITY: dict[str, float]` keyed by `proxy_type` (default 0.0 for absent entries); do NOT extend `PROXY_TYPE_TARGETING` to a dict-value shape (would break existing string-consumers). Enemy nav-selection consumers in `spatial_engine.py` read `PROXY_TAUNT_PRIORITY.get(proxy_type, 0.0)` to weight target selection: higher = enemy more likely to target this proxy.

**Representation B — Target-side ailment:**
Add `taunt` as a new ailment in `ailments.yaml` (is_control: soft, category: hard_control or debuff — unclear; ARCHITECTURAL ESCALATION e). Enemies with `taunt` ActiveEffect on them are forced to target the taunt-source until expiry.

### 6.4 ARCHITECTURAL ESCALATION e — model choice

**Ruling owed:** Representation A (proxy-AI directive) vs B (target-side ailment).

- **(A) LEAN — cleaner architecturally.** Taunt = pet AI property. No ailment loader entry required; rides proxy layer natively. Fits the "taunt annex" framing (small delta to Wave A). Genre-matched: taunt is fundamentally about pet-aggro, not target-status.
- **(B) — More architecturally symmetric with other control ailments.** Taunt as a debuff registered in ailments.yaml means every control-adjacent mechanic lives in one place. But requires wiring a target-behavior override into the sim that no other ailment does.

**gandalf lean: (A) proxy-AI directive.** The taunt gap kits (evidence §5) are 10/11 proxy-hosted; the 1 exception (Thorns-Templar) is tank-self-taunt which is not the same mechanic (it wants the PLAYER to be attacked — a self-taunt buff, not a target-override).

**ESCALATION e — Matt/KR ruling owed:** ratify (A) or (B) before rocket/gamora build the taunt-annex delta. Impact: whether ailments.yaml grows or `proxy_vocabulary_bridge.py` grows.

### 6.5 Small delta owed to Wave A (assuming ruling A)

1. **rocket:** add NEW map `PROXY_TAUNT_PRIORITY: dict[str, float]` to `proxy_vocabulary_bridge.py` (parallel to existing `PROXY_TYPE_TIER` and `PROXY_TYPE_TARGETING`). Default 0.0 (absent = no taunt). Proxy types with tank-adjacent identity (e.g., `golem_construct` — already has `targeting_behavior="taunt"`; new `melee_tank_pet`, `thorns_barrier_summon`) get `PROXY_TAUNT_PRIORITY[proxy_type] > 0`. Note: keep `PROXY_TYPE_TARGETING` string-valued unchanged.
2. **gamora:** enemy nav-selection consumers in `spatial_engine.py` (`_navigate_entity` and target-selection paths) read taunt_priority to weight target scoring. Higher taunt_priority = enemy prefers that proxy over the player.
3. **Tank-self-taunt exception** — Thorns-Templar-style: player carries `taunt_self_priority` as a build modifier; enemies weight player-targeting up (rather than proxy-targeting). Small extension; SAME nav-selection consumer.

### 6.6 Interaction with other ailments

- **Taunt + freeze/stun on target proxy** — if the proxy is frozen/stunned, its taunt_priority still counts (enemies still preferentially attack it) but proxy cannot fight back. Consistent behavior.
- **Taunt + sunder on target** — enemy targets taunter; sunder applies to whichever enemy is hit (unchanged). No new interaction.

### 6.7 Deferrable

Wave B11 master-hides / zero-aggro taunt (evidence dossier §5b Wave-A note) remains deferrable — an inverse taunt (enemy targets AWAY from source) is beyond this annex's scope.

---

## §7 — Interaction table vs existing registry

The full post-spec registry becomes 12 ailments (8 existing + 4 new + taunt-if-B). Interaction highlights:

| A × B | Interaction |
|---|---|
| burn × sunder | sunder amplifies burn tick at composition. Genre-canonical. |
| bleed × sunder | sunder amplifies bleed tick. Genre-canonical. |
| drain × sunder | sunder amplifies drain tick. Consistent. |
| poison × sunder | sunder amplifies EACH poison stack's tick (multi-tick amp). Watch DPS composition guard §5.8. |
| chill × freeze | chill remains after freeze; freeze does not clear chill. Genre-consistent. |
| freeze × stun | both hard-lock; both refresh; target locked until longest-remaining expires. |
| stun × root | stun full-locks (action + movement); root movement-locks only. Overlap coexists. |
| shock × stun | shock's paralysis-on-arc coexists with stun's brief interrupt. Lightning kits stack both — evidence §3d convergence expected. Watch S6 CC-density §4.9. |
| freeze × shatter | shatter fires at freeze expiry IF HP < threshold. On-hit-shatter (ESCALATION b variant) fires immediately. |
| poison × poison | STACKS (up to cap per attacker; evict oldest on overflow). |
| burn × burn | REFRESHES (single-instance; max-tick preserved). |
| sunder × sunder | REFRESHES (single-instance-per-target). Max-magnitude wins; cap enforced as invariant, not as sum. |
| freeze × sunder | The tentpole combo — freeze locks target, sunder amps every hit during the lock window. This is the pattern §10 ruling (b) rationale names ("unload while locked"). Watch DPS composition guard §2.11 boss check. |
| stun × sunder | Short-window analog of freeze × sunder. Amp fires during the ≤1.5s interrupt. |
| root × sunder | Positional-lock analog. Target rooted, amp fires on incoming hits. |
| shock × sunder | Shock's paralysis-on-arc + sunder amp — lightning-kit natural pairing (both ride lightning per §2.5/§4.4). Watch S6 CC-density §4.9. |
| poison × freeze | Poison ticks continue while target frozen (freeze locks movement/action, not DoT). §5.10. |
| stun × stun-immunity | new stun DROPPED if within immunity_after_seconds window. |
| any 2+ non-sunder ailments × sunder | sunder synergy_bonus_percent applies (GX-15 fold-in §2.10). |
| consecrate × sunder | consecrate is holy amplification zone (zone DoT ticks in `effect_resolver`); sunder is per-target debuff (amp applied in `damage_resolver.resolve_skill`). Coexist. If target is shadow AND sundered AND in consecrate zone: consecrate's shadow-DoT tick is amplified by sunder at tick-time (§2.8 says sunder applies at damage composition AND at DoT tick path). Composition is DOUBLE-multiplicative (consecrate tick × sunder amp), not triple — the shadow-target amp is consecrate's own valenced rule, not a separate multiplier. Verify S6 DPS bands. |
| taunt × any ailment | taunt does not clear or interact with other ailments; changes target-selection only. |
| root × freeze | both movement-lock. Coexist; expiry independent. |
| knockback × freeze | knockback displaces; freeze locks. If freeze applied to knocked-back target mid-flight, freeze fires post-landing (existing knockback resolution behavior; verify with gamora). |

**GX-15 synergy activation summary:** any target carrying 2+ distinct ailments (from any combination of the 11 non-sunder ailments) triggers sunder's synergy_bonus_percent when sunder is present. This is the multi-status incentive the Hades Privileged Status precedent authored. Sundered targets are incentivized to be "primed" with other ailments first.

---

## §8 — Routing & sequencing (→ KR)

### 8.1 Routing (by seam owner)

**rocket (generation / config / emission):**
- `config/ailments.yaml` — add 4 entries: sunder, freeze, stun, poison (per §§2.4, 3.3, 4.3, 5.3).
- `generation/element_biases.py` — extend primary/secondary ailment maps per §§2.5, 3.4, 4.4, 5.4.
- `generation/geometry_derivation.py` — extend `_control_effects` set (freeze, stun) and `_damage_effects` set (poison); add new derivation rules.
- `generation/substrate_templates.py` — add new templates per §§2.9, 3.7, 4.8, 5.7.
- `generation/proxy_vocabulary_bridge.py` — extend `PROXY_TYPE_BEHAVIOR` with `taunt_priority` field (§6.5, if ESCALATION e resolves to A).

**gamora (sim / resolution / calibration):**
- `simulation/damage_resolver._try_apply_ailment` — extend for stun immunity gate (§4.7), poison stack path (§5.6), sunder E3 stamping (§2.8).
- `simulation/damage_resolver.resolve_skill` — add sunder-amp composition step (§2.8).
- `simulation/damage_resolver._add_or_refresh` — special-case poison append semantics (§5.6).
- `simulation/effect_resolver.tick_effects` — extend expiry path for freeze shatter (§3.6, if ESCALATION b resolves to (i)).
- `simulation/combatant.py` — add freeze / stun immobilization consumers (movement + action lock).
- `simulation/spatial_gauntlet/spatial_engine.py` — read taunt_priority in enemy nav-selection (§6.5, if ESCALATION e resolves to A).
- Calibration bands for all 4 ailments — S6 gauntlet pass required post-emission.

### 8.2 Sequencing (LEAN — KR sequences)

1. **First slice — sunder (highest leverage: 97-kit gap, GX-15 fold-in ready)** — rocket config + gen surface; gamora sim consumer at resolve_skill composition; calibrate against S6.
2. **Second slice — freeze + stun (parallel; both hard_control extension)** — rocket config + gen surface; gamora immobilization consumers + stun immunity path + freeze shatter path (per ESCALATION b ruling).
3. **Third slice — poison (stacking model requires ESCALATION d ruling first)** — after (d) ruling: rocket config + gen surface; gamora stack path + tick.
4. **Taunt annex — parallel with any slice** — after ESCALATION e ruling; if (A) small delta to Wave A; if (B) new ailment entry + sim consumer.
5. **S6 gauntlet cert pass** — all four new ailments certify through S6 matchup gate; calibration bands validate; no 3-way runaway (sunder × poison-stack × GX-15 synergy = worst-case composition, must pass).

---

## §9 — Blocking vs deferrable triage

| Item | Status | Reason |
|---|---|---|
| §2 sunder (all sections) | **BLOCKING** on ESCALATION a (category choice) | one-line config decision; blocks YAML entry |
| §3 freeze (all sections) | **BLOCKING** on ESCALATION b (shatter site) | affects gamora's build scope + Discipline #11 two-seam risk |
| §4 stun (all sections) | **BLOCKING** on ESCALATION c (DR model) | affects gamora's `immunity_after_seconds` universal-vs-boss-only enforcement |
| §5 poison stack model | **BLOCKING** on ESCALATION d (stacking arch) | affects `_add_or_refresh` semantics; memory footprint |
| §6 taunt annex | **BLOCKING** on ESCALATION e (repr A/B) | affects whether ailments.yaml or proxy_vocabulary_bridge.py grows |
| Freeze-as-proc-trigger (Cast-on-Freeze) | **DEFERRABLE** | Wave C proc-grammar territory per pause-2 §3 wave order |
| Freeze-buildup-threshold model (PoE-style) | **DEFERRABLE** | current per-hit RNG gate suffices for MVP; buildup a future refinement |
| Chill→freeze escalation mechanism | **DEFERRABLE** | manual per-skill rolls suffice for MVP |
| Rabies contagion (poison spread-on-death) | **DEFERRABLE** | contagion mechanic requires new sim event; separate design |
| DoT-stack-consume (D3 Jade Harvester model) | **DEFERRABLE** | Wave C mark-and-consume territory |
| Poison + wither RR pairing | **RESOLVED via sunder synergy** | sunder is the RR-flavor primitive; poison+sunder composition covers the pairing |
| Hades2 freeze→lightning trigger | **DEFERRABLE** | cross-element proc mechanism separate design |
| Auto-targeting-of-frozen (D4 Ice Shards) | **DEFERRABLE** | targeting rule extension; separate design |
| Stagger (Hades vocabulary) as distinct from stun | **RESOLVED via stun unified** | RDR unifies stagger under stun per genre-convergence signal |
| Damage-amp on prerequisite gate (poe2-titan-hotg armor-break) | **DEFERRABLE** | Wave C mark-and-consume + prerequisite-gate territory |

---

## §10 — ESCALATIONS (5 total — RULED at gandalf verify-gate 2026-07-16; veto-open; Gate-1 stress-tests)

> **RULINGS (gandalf-prime, 2026-07-16 verify-gate, under Matt's autonomous-run delegated authority — all five ratify the drafter's leans, each on named grounds; one word from Matt reverses any):**
> - **a → `debuff`.** The RESERVED slot exists for exactly this class; `amplification` stays zonal-valenced (consecrate), `debuff` = per-target timed multiplier. No new category.
> - **b → (i) expiry-under-threshold.** Decisive DESIGN ground beyond the architectural one: on-hit shatter would make freeze a pseudo-amp-window and **collide with sunder's niche**. Expiry-under-threshold keeps the verbs distinct — sunder = amp window, freeze = **execute-setup** (unload while locked; the burst is earned by pushing the target under threshold during the freeze — the PoE2 Ice Strike Invoker two-phase loop, with death-during-freeze preserving the D2 shatter beat). Player consequence: freeze-then-unload feels authored; freeze-then-idle earns nothing.
> - **c → (c) hybrid.** Universal immunity-after-expiry (anti-stunlock floor) + boss duration multiplier — the solo-ARPG genre shape (D3 elite CC-reduction / LE boss CC resist), not MMO stack-DR.
> - **d → (a) independent-stack.** The PoE1 poison model is the deepest build-craft realization of "stack-additive, distinct from burn" (the delegated ruling's core); cap + evict-oldest guard stands (§7).
> - **e → (A) proxy-AI directive.** 10/11 gap kits are proxy-hosted; taunt is pet-aggro, not target-status. Thorns-class self-taunt = player build-modifier on the SAME nav-selection consumer (§6.5.3). ailments.yaml does not grow a behavior-override no other ailment has.

1. **ESCALATION a (sunder §2.3)** — category choice: `debuff` (reuse reserved) OR `amplifier` (new category). **RULED: `debuff`.**
2. **ESCALATION b (freeze §3.6)** — shatter resolution site: (i) `effect_resolver.tick_effects` expiry path OR (ii) `damage_resolver` on-hit trigger OR hybrid. **RULED: (i).**
3. **ESCALATION c (stun §4.6)** — boss-resistance model: (a) flat multiplier only OR (b) stack-tracker DR OR (c) hybrid (multiplier + universal immunity-after-expiry). **RULED: (c).**
4. **ESCALATION d (poison §5.5)** — stacking architecture: (a) independent-stack (PoE1 model) OR (b) rolling-aggregate OR (c) per-attacker cap + global tick sum. **RULED: (a).**
5. **ESCALATION e (taunt §6.4)** — model choice: (A) proxy-AI directive (small delta to Wave A) OR (B) target-side ailment entry. **RULED: (A).**

Count check: 5, all RULED veto-open. Matches §0 TL;DR.

---

## §11 — DL-03 conformance note (whole spec)

DL-03 (Matt 2026-07-12 design law: streams never tax movement) binds specifically:
- Sunder: N/A (debuff).
- Freeze: taxes TARGET movement; DL-03 addresses CASTER movement. Non-collision.
- Stun: same as freeze.
- Poison: `toxic_cloud` template MAY collide if authored as a caster-held channel — RESOLVED at Gate-1 (§5.9): rocket authors as `tags=["placed"]` per existing zone-template precedent. DL-03 conformance passes.
- Taunt: N/A.

DL-03 explicitly satisfied.

---

## §12 — Cross-references

- Evidence dossier: `agentic_orchestration/gandalf/design-inputs/ailment-layer-evidence-v1.md`
- Pause-2 rulings: `agentic_orchestration/gandalf/views/v3-mechanics-leverage-v1.md`
- Form model: `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md`
- Current registry: `~/Games/reincarnated-engine/config/ailments.yaml`
- Sim consumer sites: `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (`_try_apply_ailment` :996 · `_add_or_refresh` :1056 · `resolve_skill` for sunder composition), `effect_resolver.py` (`tick_effects` :42), `combatant.py` (:375 for slow_percent; new consumers for freeze/stun full lock)
- Gen emission sites: `element_biases.py` :63-73 · `geometry_derivation.py` :115-238 · `substrate_templates.py` :610-618 · `proxy_vocabulary_bridge.py` (taunt if ESCALATION e = A)
- Ailment loader schema: `~/Games/reincarnated-engine/src/reincarnated/foundation/ailment_loader.py` (VALID_CATEGORY_VALUES already includes `debuff`)
- Wave A parent (taunt annex rides): commits 4a70547 / 7aeb2a6 / 4fdd314 / 43fa149 (rocket v2.8 + gamora v1.7)
- GX-15 folded here per pause-2 §5.5; no standalone GX-15 spec required.

Tracker-delta: NEW SPEC `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` — 4 new ailments (sunder / freeze / stun / poison) + taunt annex; draft-for-Gate-1; 5 escalations flagged; gandalf-prime consolidates into engine tracker.
