# Hard-CC generation analysis (Gate-2 C5) — where, why not, what a build costs

**Agent:** rocket (generation seam)
**Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-rocket-hard-cc-generation-analysis.md`
**Mode:** ANALYSIS-ONLY. **No production code touched. No config touched.** Two throwaway read-only
probes under this directory (`2026-07-25-hard-cc-probe.py`, `2026-07-25-hard-cc-probe2.py`).
**Gates:** none pre-registered (no code). Output routes to knight-rider → gandalf elicitation packet.

---

## 0. Headline — three findings, in the order they matter

**(1) THE DESIGN QUESTION IS ALREADY HALF-ANSWERED, BY MATT, ON 2026-06-20 — AND ITS SCOPE IS
NARROWER THAN "NO HARD CC IN KITS."** The hard-control exclusion in the live emitter is not an
oversight. It is a Matt-disposed design fork, implemented exactly as ruled
(`agentic_orchestration/gandalf/notes/2026-06-20-is-control-cut-classification-and-signature-assignment.md`).
But what Matt ruled out was **hard CC riding every chain_A primary attack** — the CC-soup hazard. He
did not rule on whether a **dedicated control skill** may carry hard CC. gandalf's own note says so
explicitly (§5): *"The guardrail is retired **for this cut**, not deleted from the design space."*
**gandalf's elicitation should not re-litigate the 2026-06-20 cut. It should rule on the question the
cut never reached.** Detail in § 0.1.

**(2) THE BIGGER GAP IS NOT HARD CC — IT IS THAT *NO* CONTROL PAYLOAD IS EMITTED AT ALL.** The
endgame kit pipeline emits **133 skills whose effect is literally named `"control"`** across the
66-config census population. That string matches no ailment, no registry entry, and **no branch in
`damage_resolver`'s effect loop** (`damage_resolver.py:829-1200` — verified branch enumeration; there
is no `else` fallback). Every control-role skill in every generated kit carries a placeholder that
the simulation silently skips. **The finding is not "hard CC is missing." It is "the control role is
a label with no mechanism behind it."** Soft CC (chill) reaches the sim only because it rides the
*primary-attack* signature-ailment path, not because any control skill emitted it. Detail in § 2.2.

**(3) FREEZE AND STUN WERE SPEC'D FOR GENERATION-SIDE EMISSION AND THE EMISSION CODE WAS NEVER
BUILT — BY ANYONE.** `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` §251 / §590 / §606
assigns rocket a "gen surface" for freeze + stun. What landed (rocket, 2026-07-16) was the *declaration*
(`SECONDARY_AILMENT_MAP`) and the registry entries. The *consumer* was deferred with the words
**"Emission logic — per-skill secondary-ailment roll probability … GAMORA calibration scope"**
(`src/reincarnated/generation/MIGRATION.md:452`). gamora's slice built only sim-side consumers. The
probability parameter got a home; the mechanism that would read it never did.
**`SECONDARY_AILMENT_MAP` has zero production readers** — verified by full-tree grep: every hit in
`src/` is its own definition, its own docstring, a MIGRATION entry, or a math note. Detail in § 2.3.

### 0.1 The 2026-06-20 ruling, quoted, and what it does and does not settle

Matt disposed an emission-breadth fork to the middle path **`is_control != hard`**. gandalf's
classification note implemented it against the registry's own field:

> **EMIT (non-hard):** bleed, burn, drain, chill, consecrate.
> **EXCLUDE (`is_control == hard`):** root, knockback, shock.
> *"The three excluded ailments are exactly the lock-stacking immobilize/displace trio … the ones
> whose **per-hit re-application** is the CC-soup/stagger-soup hazard."*

The hazard named is **per-hit re-application on primary attacks**. §5 of that note is explicit that
the guardrail retirement is cut-scoped:

> *"if a LATER decision re-adds hard-control signatures … the DR guardrail comes BACK as a
> dependency at that point. The guardrail is retired **for this cut**, not deleted from the design
> space."*

So the live exclusion at `per_skill_emitter.py:817` is a **faithful implementation of a real ruling**,
and hypothesis (b) is the correct classification for root/knockback/shock. But the ruling's subject
was *signature ailments riding chain_A damage skills*. It is silent on a control-role skill slot
whose whole job is control. That silence is the elicitation's actual subject.

**A second thing gandalf should know: the exclusion set silently widened after Matt's ruling.**
On 2026-06-20 the excluded set was `{root, knockback, shock}` — the trio Matt saw. On 2026-07-16 the
ailment layer added `freeze` and `stun` with `is_control: hard`. Because the emitter reads the
registry (`get_hard_control_ailments()`, `ailment_loader.py:413`) rather than a hand-maintained list,
**freeze and stun joined the exclude set at registry-edit time, with no design ruling on them.**
Probe P2 confirms `_HARD_CONTROL_AILMENTS == {freeze, knockback, root, shock, stun}` at HEAD, while
the comment at `per_skill_emitter.py:797` still reads `# frozenset({root, knockback, shock})`.
That stale comment is the visible trace of an unnamed Discipline-#12 semantic shift. The registry-
driven design is correct and I am not proposing to change it — but the widening **inverted the
ailment-layer spec's intent for ice→freeze**, which asked for freeze to be emittable, and instead
made it un-emittable the moment it was registered.

---

## 1. Q1 — the emission-surface map

There are **two** generation pipelines that can attach effects to a skill. Only one of them is
reachable from production. This distinction is load-bearing and I did not find it stated anywhere.

### 1.1 Pipeline A — `per_skill_emitter.py` (THE LIVE PATH; what the census sampled)

Provenance chain, verified end to end:
`clean_boss_numbers_harness_2026_06_19.build_population():62`
→ `season_generation_pipeline.w5r1_generate_kit_candidates():876`
→ `per_skill_emitter.emit_skills_for_kit()` (called at `season_generation_pipeline.py:1191`)
→ `_build_legendary_config():1489` → `_build_real_player_class():1652` (consumes `kit.skills`
verbatim; no effect filtering) → the `player_class.skills[].effects[]` that gamora's census read.

Two effect-attachment sites exist in this file, and only two:

| Site | file:line | What it emits |
|---|---|---|
| **Primary effect** (every skill) | `per_skill_emitter.py:1337-1342` | `AbilityEffect(name = "damage" if role in ("primary_attack","secondary_attack") else role.replace("_","_"))` — i.e. literally `"control"` or `"support"` for those roles |
| **Signature ailment** (chain_A only) | `per_skill_emitter.py:1351-1356` | `_make_signature_ailment_effect(ELEMENT_AILMENT[skill_elem], tier)` |

`_make_signature_ailment_effect` is defined at `:800`; its hard-control exclusion is the bare
`return None` at **`:817`**, gated on `_HARD_CONTROL_AILMENTS` (`:797`).

**Where each effect type WOULD attach, in this pipeline:**

| Effect type | Nearest emission seam | Status |
|---|---|---|
| `root` | `per_skill_emitter.py:817` (exclusion) — *or* `:1339` (control-role primary effect) | Blocked at `:817`; `:1339` emits a placeholder instead |
| `freeze` | same two seams + `element_biases.py:120` `SECONDARY_AILMENT_MAP["ice"]` | Blocked at `:817`; secondary map has no reader |
| `stun` | same + `SECONDARY_AILMENT_MAP["physical"]`, `["lightning"]` | Blocked at `:817`; secondary map has no reader |
| `silence` | **no seam exists in this file at all** | Not in registry → not in `ELEMENT_AILMENT` → `_make_signature_ailment_effect` cannot produce it; `:1339` cannot produce it. There is no site to gate. |

### 1.2 Pipeline B — `ability_grammar.py` (CAN emit hard CC and silence; **not reachable from production**)

`_sample_effects()` at `:556` reads `ailment = ELEMENT_AILMENT[element]` (`:566`) and calls
`_make_ailment()` (`:649`), whose `hard_control` branch (`:712-718`) emits root / knockback / shock
with full param shapes. **Silence has its own dedicated constructor** at `_make_effect():636-638`
(`duration_seconds` uniform 1.5–4.0) and reaches skills by two routes:
`role_constraints.py:120` `utility.secondary_effects=(("silence",0.30),…)`, and the control-role
fallback at `ability_grammar.py:578-579` when the element's signature ailment is not a control effect.

Probe P5 confirms this empirically (300 samples per element×role at HEAD):

```
earth/control     -> ['damage', 'root']          wind/control  -> ['damage', 'knockback']
lightning/control -> ['damage', 'shock']         ice/control   -> ['chill', 'damage']
fire|holy|physical|shadow /control -> ['damage', 'silence']     (the :578 fallback)
*/utility         -> ['buff_damage', 'buff_mana_regen', 'silence']
```

**But this pipeline has no production caller.** Full-tree grep (excluding `tests/` and a stale
worktree): `MonsterGenerator` and `TrialGenerator` are instantiated only in `scripts/` diagnostic
harnesses and tests. `season_orchestrator.py` — the module that used to construct both — no longer
exists in `src/reincarnated/generation/`; it survives only in
`.claude/worktrees/agent-ad557ae39574ea548/`. `weapon_envelope_composer.py` (the third
`AbilityGrammar` consumer) has zero callers anywhere. `balance_loop.py:875` constructs a grammar
lazily inside `_ensure_generation_tools()`, which is a class-regeneration path, not a season-emission
path.

**So: the only code in the engine that knows how to build a `root`, `knockback`, `shock` or
`silence` effect is orphaned.** That is a real and separate finding — the emission machinery for
three of the four hard-CC types plus silence already EXISTS and is unit-shaped; it just sits on a
pipeline nothing calls.

### 1.3 Adjacent surfaces that reference hard CC but emit nothing

| Surface | file:line | State |
|---|---|---|
| `SECONDARY_AILMENT_MAP` | `element_biases.py:120-129` | Declared; ice→freeze, physical/lightning→stun. **Zero readers in `src/`** (probe P6). |
| `geometry_derivation._control_effects` | `geometry_derivation.py:262` | `{root, silence, chill, knockback, shock, drain}` — **freeze/stun absent.** Named as a deferral in `generation/MIGRATION.md:449`. |
| `ZoneControlStrategy.zone_control_effect` | `mechanic_alteration.py:1235` | `"element_signature"` — declared, **zero consumers anywhere**. A second inert control declaration. |
| Spec'd substrate templates | `substrate_templates.py` | `ice_freeze_field`, `frost_nova_shatter`, `deep_freeze_bolt`, `heavy_smash_stun`, `thunder_clap_stun`, `concussion_grenade` — **none exist.** Named as deferrals in `generation/MIGRATION.md:450`. |
| `d10_kit_constraints._element_specific_effects` | `d10_kit_constraints.py:364` | `{burn, chill, root, shock, drain, heal, heal_over_time}` — **freeze/stun/silence/knockback absent.** A curation-path drop risk if hard CC is ever emitted (see § 3.4). |
| `typed_monster_skills.py` (mob offense) | whole module | Probe P7: boss/elite/swarm all emit `['damage']` only. **Mobs carry no ailments of any kind.** |

---

## 2. Q2 — why they are not emitted, discriminated per type

**Method (Discipline #10).** I re-materialized the exact census population
(`build_population()`, `SEASON_SEED_BASE = 14001`) and dumped the full effect-name histogram, cross-
tabbed by role and element. This is not a re-derivation of gamora's census — it reproduces it as a
control (`cc_effects_per_config == {0: 61, 4: 5}`, identical) and then reports the *rest* of the
distribution, which the CC-filtered census could not see.

```
n_configs 66 · n_kits 54
effect_name_histogram:
  damage 478 · support 181 · control 133 · bleed 56 · consecrate 44 · burn 24 · chill 20 · drain 8 · summon 5

role x effect:                          element x effect (control-role slice):
  control|control            133          earth|control     25   (0 root)
  primary_attack|bleed        56          wind|control      18   (0 knockback)
  primary_attack|consecrate   44          lightning|control 13   (0 shock)
  primary_attack|burn         24          holy|control      21
  primary_attack|chill        20          physical|control  27
  primary_attack|drain         8          fire|control      12 · ice|control 12 · shadow|control 5
  support|support            181
```

The 5 CC-bearing configs are exactly the ice kits: 4 chain_A tiers × `chill` = `cc_effects = 4`.
Every other config's element signature is either a non-control ailment (burn/bleed/drain/consecrate)
or a hard-control ailment that `:817` suppresses. **Both halves of gamora's `Counter({0:61, 4:5})`
are now mechanically explained.**

### 2.1 `root` — **(b) implemented but gated.** Evidence: decisive.

`ELEMENT_AILMENT["earth"] == "root"` (`element_biases.py:76`), so earth kits *do* reach
`_make_signature_ailment_effect("root", tier)`. Probe P3 returns `None` — the `:817` exclusion.
Probe P4 confirms `earth → PSE_emits: null`. The gate is **not a probability, not a flag, not a
constraint that could be satisfied by a different pool draw** — it is an unconditional `return None`
keyed on a registry field. No config change can reach past it. Same discrimination applies verbatim
to `knockback` (wind) and `shock` (lightning), which are not in this dispatch's scope but are the
same mechanism.

**Not (c).** I want to be explicit here because the dispatch asked me to say so plainly if the answer
were (c): **it is not.** There is no weight, allow-list, or bias to nudge. Every earth kit in the
population reaches the gate and every one is refused.

**Not (d).** `_build_real_player_class` consumes `kit.skills` without filtering, and the census read
the same objects. Nothing downstream drops anything, because nothing upstream produced anything.

### 2.2 The control-role placeholder — **(a) never implemented.** This is the load-bearing one.

`per_skill_emitter.py:1339` builds the primary effect as
`name = "damage" if role in ("primary_attack","secondary_attack") else role.replace("_","_")`.
For `role == "control"` that expression evaluates to the string `"control"` — `str.replace("_","_")`
is a no-op, so the name IS the role. 133 such effects exist in the census population. They carry
damage-shaped params (`base_spell_damage_l50`, `economy_k`, commitment fields).

`damage_resolver.resolve_skill`'s effect loop (`:829`) branches on
`damage / heal / shield / heal_over_time / buff_* / AILMENT_NAMES / silence / lifesteal`, with **no
`else`**. `"control"` matches nothing. `spatial_engine` reads `effect_category` only for AOE-radius
defaults (`:1420`) and a geometry fallback (`:990`). **A control-role skill is inert in the live
loop on both axes at once: it deals no damage and applies no control.**

That is (a) — never implemented — and it is a strictly larger hole than the hard-CC question. It also
means the **BC `control density` axis is measuring role-share in the emitted kit, not any realized
mechanic** — which is a stronger statement than the one already in
`simulation/MIGRATION.md` (that the axis measured *emitted property, not realized effect*). For
control-role skills there is not even an emitted property to measure: there is a string.

*(Flagged, not fixed, per dispatch § 3: whether control skills should also deal damage is a
consumer-side question I am not ruling on. I report it because it is the same emission site.)*

### 2.3 `freeze` / `stun` — **(a) never implemented, on top of (b).** Both, in that order.

Two independent blocks, either of which alone would produce a hard zero:

- **(a):** `SECONDARY_AILMENT_MAP` (`element_biases.py:120`) is the map that would let ice roll
  freeze and physical/lightning roll stun. It has **zero readers in `src/`** (probe P6 — all 24 hits
  are the definition, its docstrings, MIGRATION entries, math notes, AGENT_STATE, and one `.pyc`).
  The spec-lean emission probability (0.25) has no consumer to parameterise. This is a
  seam-boundary drop: rocket's MIGRATION deferred it as *"GAMORA calibration scope"*
  (`generation/MIGRATION.md:452`), gamora's slice built only sim-side consumers, and the emission
  code — which is generation-side — was built by neither.
- **(b):** even with a reader, both are `is_control: hard`, so any route through
  `_make_signature_ailment_effect` returns `None` at `:817` (probe P3: `freeze → null`,
  `stun → null`). Note this gate was inherited automatically at registry-edit time, not ruled — § 0.1.

**Both blocks would have to be lifted.** Neither is a config change.

### 2.4 `silence` — **(a) never implemented in the live pipeline**, and its cause is structurally different.

Silence is not in `config/ailments.yaml` (`effect_categorization.py:35-38`), so it is absent from
`ELEMENT_AILMENT`, absent from `SECONDARY_AILMENT_MAP`, and cannot be constructed by
`_make_signature_ailment_effect` (which resolves param shapes off the registry). `per_skill_emitter.py`
contains no silence code at all — **there is no gate to lift, because there is no site.**

The asymmetry the dispatch anticipated is real and cuts the *opposite* way from the other three:

| | root / freeze / stun | silence |
|---|---|---|
| Registry entry | yes | **no** |
| Param shape source | registry `param_ranges` | hardcoded at `ability_grammar.py:636-638` |
| Live sim consumer | yes (F8, 2026-07-25) | **yes, and older** — `damage_resolver.py:1182-1188` |
| Live emission path | gated | **none** |
| Orphaned emission path | `ability_grammar._make_ailment` | `ability_grammar._make_effect` + `role_constraints.py:120` |
| Governing spec text | ailment-layer spec §§3.4/4.4 | **none anywhere** (jack-ryan, Gate-2) |

So silence is the one type where the *engine* is more ready than the *design*: it has had a working
producer and consumer for longer than the registry ailments have, and no spec has ever said what it
is for. Its only semantic declaration is `combatant.py:461`.

### 2.5 What I could NOT discriminate, and why

**I cannot rule out that the control-role placeholder at `:1339` was a deliberate scaffold rather
than an omission.** The expression `role.replace("_", "_")` is a no-op — it reads like it was meant
to be a mapping (`role.replace("_", "-")`? a dict lookup?) and was left as an identity. I found no
math note, MIGRATION entry, or design note that names the control-role primary effect at all. The
`generation/math/` notes for the W5R1 emitter cover roles, geometry ladders, economy and commitment
axes, but not the effect payload for non-attack roles. **Absence of a record is not evidence of
intent either way, and I am not going to guess.** What I can say with evidence: the string is inert
in the resolver, 133 instances of it exist, and nothing anywhere claims it should be otherwise.

---

## 3. Q3 — what a build would cost. **Conditional on the § 6 ruling; framed as "if yes, here is the price."**

### 3.0 The plain answer to the dispatch's own framing

The dispatch asked me to say so plainly if the answer were "flip a config weight." **It is not.**
There is no weight, no allow-list, no bias, no tier gate. Both blocking mechanisms are unconditional
code: a `return None` and a missing consumer. The smallest honest build is a **new emission path**,
not a re-parameterisation. I am telling you this rather than manufacturing a cheaper-sounding option.

### 3.1 Three build shapes, distinguished by which design question they answer

**Option A — control-role payload (recommended shape if the ruling is yes).**
Give `role == "control"` skills a real payload at `per_skill_emitter.py:1337-1342` instead of the
placeholder. The control skill is *already* a dedicated, cooldown-gated, non-primary slot (8-20 s
cooldowns in the grammar analogue; the W5R1 ladder gives control its own geometry ladder at `:290`
and its own economy cadence at `:332`). **This is the shape that does NOT re-open Matt's 2026-06-20
hazard**, because the payload rides a control slot, not every primary hit. It also fixes finding (2)
— the inert control role — as a by-product rather than leaving it.
*Rough size:* one emission function (~60-100 lines, mirroring `_make_signature_ailment_effect`'s
category dispatch), one element→hard-CC resolution map (reads existing `ELEMENT_AILMENT` hard entries
+ `SECONDARY_AILMENT_MAP`, no new hand-maintained data), the `:1339` call-site change, and the
`d10_kit_constraints` / `geometry_derivation` widenings in § 3.4.

**Option B — secondary-ailment roll (the ailment-layer spec's original §2.9 shape).**
Build the `SECONDARY_AILMENT_MAP` consumer at the spec's LEAN 0.25 emission probability, riding
attack skills. This is closer to what the 2026-07-16 spec asked for — and it is **exactly the
per-hit re-application shape Matt's 2026-06-20 cut was designed to prevent.** If the ruling wants
this, the DR guardrail returns as a hard dependency (gandalf 2026-06-20 §5). I flag the conflict
rather than resolving it; the two rulings are 26 days apart and were never reconciled.

**Option C — silence.** Needs a design home *first*. There is no spec sentence anywhere that says
what silence is for. Building emission before that is building to no requirement. If the ruling
wants silence, the cheapest path is not new code at all — it is deciding whether silence belongs in
the ailment registry, after which it flows through whichever of A/B is chosen.

**Options A and B are not mutually exclusive but should not ship together.** A alone is the smaller
blast radius and the one whose measurement story is clean.

### 3.2 Math owed BEFORE code (Discipline #1) — three notes, and one of them is not mine

1. **CC uptime budget.** N control skills per kit × duration × (1/cooldown) → expected lockout
   fraction per mob per fight, with the stun DR immunity window and boss resist tier composed in.
   Needs a target lockout ceiling *chosen* before durations can be picked. Registry ranges are wide
   (root 1.5-4.0 s, freeze 0.5-3.0 s, stun 0.3-1.5 s) and the control ladder gives 1-2 control slots
   per kit at T1-T2 plus chain_B pivots at T3-T4 under `control_leaning` (`per_skill_emitter.py:732`).
   This is mine.
2. **DR guardrail re-derivation.** gandalf's 2026-06-20 §5 caveat fires: hard-control emission
   re-arms it as a paired dependency. Partially pre-paid — gamora built `immunity_after_seconds` and
   the boss resist tier for stun. Root, knockback, shock, freeze have no DR story. This is
   gandalf-design + gamora-sim, not mine; I flag it as a blocker on the build dispatch, not on this
   analysis.
3. **Control-density BC axis — YES, IT RE-OPENS.** `simulation/MIGRATION.md` already says any BC
   coordinate derived from control density pre-2026-07-25 measured an emitted property, not a
   realized effect. § 2.2 sharpens that: for control-*role* skills there was not even a property —
   the axis binned a role budget whose payload was a placeholder string. If hard CC becomes
   emittable, the axis changes meaning **a second time**, and this time in the direction that makes
   it real. The re-derivation owed is: control-density bin boundaries against realized lockout
   fraction (from note 1), plus a re-measure of substrate-lattice coordinates for every kit whose
   `control_density` bin is not `damage-pure`. **Flagged, not attempted here**, per dispatch § 5.

### 3.3 Smoke gate (Discipline #2), including the novel-path watch

5 kits × 30 fights, ~2-3 min. The 5 must be **element-selected, not random**: one earth (root), one
ice (freeze), one lightning (shock/stun), one physical (stun), one wind (knockback) — otherwise the
sample can miss every hard-CC element, which is precisely how this gap survived.

Assertions:
- `select_action_locked > 0` **and** `nav_move_locked > 0`. These have been hard zeros in every
  production frame the engine has ever run. **First non-zero is the novel-path event jack-ryan asked
  to be watched, not treated as routine telemetry** — the smoke report must call it out by name.
- Per-type attempt/landed counters non-zero for each emitted type (the `bump()` create-on-first-
  increment idiom makes key-absence a hard zero — reuse gamora's harness pattern verbatim).
- Realized lockout fraction inside the § 3.2-note-1 ceiling.
- Zero-CC control arm byte-identical (the inert corner must stay inert).
- Effect names round-trip through the export boundary unchanged.

### 3.4 Seams touched, and the ones that will silently eat a hard-CC effect if not widened

| Seam | file:line | Why it must move |
|---|---|---|
| `per_skill_emitter` primary effect | `:1337-1342` | The build site (Option A) |
| `per_skill_emitter` hard-control gate | `:797, :817` + stale comment | Gate must become scope-aware (control-slot yes / chain_A signature still no), and the comment must stop lying |
| `element_biases` | `:120` | `SECONDARY_AILMENT_MAP` gains its first reader (Option B) or is cited by the control-slot resolver (Option A) |
| `geometry_derivation._control_effects` | `:262` | **freeze/stun absent** — control geometry would misclassify. Already a named deferral (`generation/MIGRATION.md:449`) |
| `d10_kit_constraints._element_specific_effects` | `:364` | **freeze/stun/silence/knockback absent** — the D10 curation path would treat a hard-CC skill as element-remappable and silently move e.g. a freeze onto a fire kit |
| `substrate_templates` | — | 6 spec'd hard-CC templates never authored (`generation/MIGRATION.md:450`); optional for A, expected for B |
| `d10_kit_constraints.DAMAGE_CONTRIBUTING_EFFECTS` | `:490+` | **No change** — hard CC correctly excluded from the damage tax already |

**Cross-seam / ADR-004 (dispatch § 7):**
- **No `loadout` dict key moves.** No key added or removed.
- **No export packet shape change.** `effects` is a passthrough field
  (`export/cycle14_wave5_emitter.py:364` `_SKILL_PASSTHROUGH_FIELDS`), serialized generically.
- **BUT the value domain of `effects[].name` widens** — same class as gamora's F8 entry
  (*"no schema change, value-level shift"*). **A `MIGRATION.md` IS owed**, because three downstream
  readers key off that domain: star-lord's LLM prompt ailment vocabulary, drax's loadout ailment
  labels, and the player-facing ailment table at `export/season_exporter.py:255-266`.
- **That exporter table is already stale, worse than the dispatch's ledger item says.** It documents
  6 ailments (registry has 16), calls `root` *"(demo2)"*, and labels `silence` **"Fire-element
  signature"** — silence has no element and is not in the registry. The dispatch ledger flagged one
  sentence of it for star-lord; the whole table needs the pass. **star-lord's item, not mine — I am
  reporting scope, not patching.**

### 3.5 Honest cost

| Phase | Estimate | Notes |
|---|---|---|
| Math notes 1 + 3 (mine) | 3-5 h | Note 1 needs a lockout ceiling *chosen* first — that is a design input, not a derivation |
| Math note 2 (DR guardrail) | **not mine** | gandalf + gamora; a blocker on the build dispatch |
| Option A implementation | 4-6 h | 1 new function, 1 call-site, 2 set widenings |
| Smoke iteration | 2-4 h | Element-selected 5-kit frame; expect 2-3 rounds on durations |
| MIGRATION + downstream notify | 1-2 h | rocket MIGRATION entry + explicit routes to star-lord and drax |
| **Option A total** | **10-17 h**, ~2-3 sessions | Excluding the DR guardrail dependency |
| Option B increment | +6-10 h | Plus the DR guardrail, which is the real cost and is not mine to size |
| Option C (silence) | design-blocked | No spec requirement exists to build against |

**LLM cost: ~$0.** Neither option calls the LLM. Kit emission is deterministic; naming is a
separate Phase-5 pass that is unaffected by effect payloads.

---

## 4. The corpse-ordering question, applied to hard CC (dispatch ledger, one paragraph as asked)

`_try_apply_ailment` is called from `resolve_skill` **after** damage with no defender-liveness gate,
so an overkilling hit stamps the effect onto a corpse — re-measured at Gate-2 C2 as **91.8% of chill
landings** (4,696 / 5,116, post arm). **The same ordering would apply verbatim to hard CC, and the
consequence is worse in kind, not just in degree.** A chill on a corpse is merely wasted; a stun or
freeze on a corpse is wasted *and* silently inflates every control-density and CC-uptime measurement
the build would be calibrated against — a lockout budget computed from `landed:` counters would be
~12× the realized one at the current corpse ratio. **If the ruling is yes, the liveness-gate question
should be resolved before the calibration run, not after**, or the § 3.2 note-1 uptime budget is
being fitted to a number that is 91.8% fiction. (Routed design item, gandalf/Matt — I am naming the
dependency, not the fix. Note it may partly self-correct: hard CC applied by a *control* skill fires
on a cooldown-gated non-killing cast, so its corpse ratio should be structurally lower than
chill's, which rides primary attacks. That is a hypothesis, not a measurement.)

---

## 5. Reproduction

Both probes are read-only, touch no engine file, and write nothing.

```
python3 agentic_orchestration/rocket/notes/2026-07-25-hard-cc-probe.py    # P1-P7 surface probes
python3 agentic_orchestration/rocket/notes/2026-07-25-hard-cc-probe2.py   # census population effect histogram (~3 min)
```

Probe 2 reproduces gamora's `Counter({0: 61, 4: 5})` exactly as a control before reporting the rest
of the distribution. It is a reproduction, not a re-derivation — the census stands as cleared.

**Discipline #25 (semantic-layer rep-audit):** not applicable. Nothing in this analysis inherits
cluster identity from substrate work as design substrate; every claim is a code read or a probe.

---

**Signed:** rocket, 2026-07-25. Analysis only. No production code, no config, no tag. The ruling
gates the build.
