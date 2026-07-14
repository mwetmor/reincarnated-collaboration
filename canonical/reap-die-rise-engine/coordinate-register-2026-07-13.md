# Kit-Identity Coordinate Register — the periodic-table cell key

**Author:** gandalf (SPEC-AUTHOR / CANON-STEWARD) · **Date:** 2026-07-13
**Status:** RATIFIED (Matt 2026-07-13) — coordinate membership, the ailment architecture, and the element-naming pools were all ruled this session. Available for jack-ryan Gate-1 review; content is Matt-ruled.
**Consumers:** rocket (emission gate §3.1), gamora (matchup + dedup §6), elrond (corpus→roster migration, cell addressing), the periodic-table render harness (PROMPT 5, S3).
**Supersedes:** the mobile-Claude scaffold `atlas_key_orig` / `lattice_coord` / `mobile_cell_id` — **DEPRECATED.** Those were authored on mobile without engine knowledge, are referenced by zero live code (the render keys off engine fields, never them), and were never the authoritative key. Do not consume them.

---

## 0 — What this doc is
This defines the **kit-identity key**: the coordinates that address a kit to a unique cell in the periodic table. It is the permanent "skeleton" the whole pipeline hangs on — the cell address that survives emission rerolls and *becomes* kit identity at migration (S5). It answers three questions:

1. Which coordinates constitute **mechanical identity** (are in the cell key)?
2. Which are **excluded**, and by which of three membership classes?
3. **When is the key complete enough** to fire dedup + representative-selection (the S4 gate)?

The key is **element-free by construction** and **matures as S4 ratifies mechanics.** It is not "done" today; §5 is the completeness gate.

---

## 1 — The membership law: three coordinate classes
Every candidate coordinate belongs to exactly one class. The class decides whether it enters the key.

| Class | In the key? | Definition | Discriminator | Members |
|---|---|---|---|---|
| **A — Mechanical identity** | **YES** | Measured from combat behavior; source-faithful; the cell address. | "Does it describe how the kit *fights*, invariant under re-skinning?" | the 13 coordinates in §2 |
| **B — Emission overlay** | **NO** | Rolled/rotated at emission; decorrelated from mechanics; colors name / portrait / flavor only. | "Is it rolled at emission and mechanically inert?" | element, race, gender, culture, faction, hybridity, period, flavor |
| **C — Transformation-mapping** | **NO** | The engine re-derives it by internal logic; the value **may differ from the source game's value.** | "Does our engine reassign it such that it can differ from the source?" | **attribute** (first member) |

**Why C is excluded and is not merely "dressing" (Matt, 2026-07-13):** attribute is neither identity (it isn't measured combat behavior) nor emission overlay (it isn't a free roll). It is a *many-games→one-game transformation input* — our engine assigns STR/DEX/INT/WIS by its own logic, which will frequently disagree with the attribute the kit carried in its source game. Putting it in the periodic table would actively mislead a player who knows the source build. It rides in the transformation layer, not the key.

**Why B is excluded — the element case specifically:** `elem_raw` is schema-marked *permanent "descriptor-final"* (never promoted to a keyed coordinate), unlike geo/ctrl/def/econ which promote to `keyed-v1`. Element is randomly rotated at emission and is not unique to a cell — a single mechanical cell contains kits of many elements. Element **names** mechanical functions (§3); it never **is** one.

---

## 2 — The mechanical-identity coordinates (Class A) — the thirteen
Counts are combat-kit snapshots (n = 470) as of 2026-07-13.

| # | Coordinate | Source column | Values (cardinality) | Status |
|---|---|---|---|---|
| 1 | **Movement-while-casting** | `mob_policy_while_casting` | FREE-MOVE · WALK · ROOTED (3) | **LOCKED** (Q19) |
| 2 | **Delivery** | `delivery_value` | PROJECTILE · ORBITAL · NOVA · ZONE · BEAM · MELEE · SUMMON (7) | **LOCKED** (Q19) |
| 3 | **Amplitude stratum** | `amp_val` | FLAT · SPIKY · VAR (3) | **LOCKED** (Q19) |
| 4 | **Geometry sub-type** | `geometry_value` / `geo_raw`→keyed-v1 | ~21 raw shapes rolling up into #2 (circle, cone, chain, totem, dash, vortex…) | keyed, refine within #2 |
| 5 | **Control** (treatment + function) | `ctrl_treatment` + control-function tag | treatment: damage · control · hybrid (3); function sub-axis: §3 | **RESOLVED THIS SESSION** (was 205/470 ailment-gap) |
| 6 | **Defense** | `def_bin` | tank · mitigate · evade · absorb · glass (5) | keyed (215→28) |
| 7 | **Economy model** | `economy.model` · resource-name via `resource_verbatim` | spend · cooldown · generator-spender · reserve · self-cost · finite · free (7) | **RESOLVED THIS SESSION** (Wave B; §3B — model = Class A; resource-name = 1:1 preserved, out of key) |
| 8 | **Proxy density** | `proxy_val` | solo · light · heavy (3) | keyed; **summon-economy RESOLVED** (Wave A) — derived read = #7 model ∩ delivery=SUMMON (#2) ∩ proxy density, not a separate axis (§3B) |
| 9 | **Range** | `range_val` | melee · mid · ranged · dual (4) | keyed |
| 10 | **Tempo** | `tempo_val` | low · med · high (3) | keyed |
| 11 | **Commit** | `commit_val` | instant · wind-up · channel (3) | keyed |
| 12 | **Activation model** | `activation_val` *(new)* | active · triggered (2) | **RESOLVED THIS SESSION** (Wave C; intrinsic-trigger only — §3A.1) |
| 13 | **Dependency structure** | `dependency_val` *(new)* | one-shot · build→spend · apply→detonate (3) | **RESOLVED THIS SESSION** (Wave C) |

**The LOCKED skeleton = coords 1–3** — the Q19 plane, 3 × 7 × 3 = **63 buckets.** This is permanent. Coordinates 4–13 refine *within* each bucket. Attribute is **absent by ruling** (§1, Class C).

---

## 3 — Coordinate #5: the ailment architecture (the session's resolution)
"Ailment" was overloading **two distinct concepts.** Separating them dissolves the doubling problem and keeps element mechanically inert.

- **CONTROL** — crowd-control, kit-*designed*, **element-neutral**: hard-stop · stun · taunt · fear · blind · knockback · expose (damage-amp) · hex/curse · silence. → **Class A, coordinate #5's function sub-axis.**
- **ELEMENTAL AILMENT** — damage-type debuff / DoT, **element-inherent** flavor: ignite · chill · shock · poison · bleed. → **Class B emission.**

**The load-bearing insight: element NAMES a control function; it does not ADD a second effect.** A hard-stop is the same mechanical stop whether it surfaces as *freeze* (ice) or *petrify* (earth). No second effect is stapled on, so the population never doubles and element stays inert.

**Three layers:**
- **Layer 1 — CONTROL** (Class A key; element-neutral; element-*names*-it). The mechanical function lives here.
- **Layer 2 — ELEMENTAL AILMENT** (Class B emission; weak, always-on, flavor-tier; supplies element↔ailment continuity). When a same-family Layer-1 control is present, Layer 2 is *absorbed* into the Layer-1 naming rather than double-counted.
- **Layer 3 — GEAR AMPLIFICATION** (**DEFERRED** to a gear-axis follow-on): **soul-bound gear** (`agnostic-loot-engine-spec.md`) — kit-agnostic, mechanic-*adjusting* operators, **never** per-kit stat-rolls — amplifies a latent/signature ailment. **The gear law (§3A.1) — amplify your own · path texture to anyone · import no one's core · invent nothing.** The kit-agnostic operator model is the only itemization that scales across ~500 kits from ~15 incompatible source games (a universal amplify operator serves all of them; a legacy per-kit roll serves one). Build-crafting + loot relevance + the isekai "gear awakens power" beat. Scoped later; the seam is reserved. (The same law governs coord #12 — see §3A.1.)

### 3.1 — The element-naming compatibility rule (the "gacha" resolution)
**The problem is semantic, not lexical.** Element is a Class-B free roll, but some control functions cannot be coherently *named* by every element — "fire hard-stop" fails because fire does not immobilise, and no clever word fixes that. You cannot name your way out of a semantic gap; you must prevent the incoherent pairing at the roll.

**The rule (Matt-ratified 2026-07-13) — SCOPED constraint:**
- **Universal control functions roll element free** (all 8): stun, blind, expose/damage-amp, knockback, taunt, silence.
- **Three element-constrained functions carry an allow-list.** Emission rolls element from **`kit-eligibility ∩ function-allow-list`.**

**Canonical 8 elements** (source: `kit_space_schema.py` / `bc_target_player_class.py`): `physical · fire · ice · earth · wind · lightning · holy · shadow`.

| Constrained function | Allow-list (of the 8) | Naming | Excluded |
|---|---|---|---|
| **hard-stop** | ice · earth · lightning · shadow · physical | freeze / petrify / paralyze / shadow-bind / shackle | **fire, wind** |
| **hex/curse** | shadow · holy | curse / condemn (holy = divine condemnation) | the other 6 |
| **fear** | shadow · fire | terror / primal-panic | the other 6 |

- **Intersection-empty** = a **healthy generation-time flag** (the kit's identity is over-constrained), never silent garbage.
- For a constrained-function kit, the allow-list sets the eligible set of the **primary element slot**; flex slots follow normal rules.

**Why this does NOT contradict the gender-decorrelation principle.** Gender rolls upstream specifically to *destroy* the archetype↔gender correlation, because that correlation is a **stereotype** (archer→female). Element↔control-naming is the opposite: it is a **genre affordance players enjoy** — cold = control/freeze is bedrock ARPG (D2 Blizzard sorceress; PoE's cold-ailment freeze/brittle line vs fire's ignite as pure damage; Grim Dawn petrify). **Decorrelate stereotypes; honor affordances.** Same mechanism (constrain a roll by a prior-fixed coordinate), opposite intent — no contradiction.

---

## 3A — Coordinates #12–#13: activation & dependency (Wave-C resolution)
The placeholder "trigger / mark-consume axis" was **one label smuggling two orthogonal Class-A axes.** Separating them fixes the schema and closes Wave C.

- **#12 — Activation model** `activation_val` ∈ {**active**, **triggered**}. *Who pulls the trigger* — the player each cast (active), or a game-state condition the kit wired up (triggered: on-crit, on-hit, on-a-timer).
- **#13 — Dependency structure** `dependency_val` ∈ {**one-shot**, **build→spend**, **apply→detonate**}. *How the kit's payload is staged* — fire-and-resolve, accumulate-then-release, or plant-then-pop.

**Orthogonality proof (both axes vary independently — populated pairings):**
| | one-shot | build→spend | apply→detonate |
|---|---|---|---|
| **active** | Fireball | Blade Flurry (charge-stack) | Detonate Dead |
| **triggered** | CoC Ice Nova | Poet's Pen (spell-on-attack ramp) | Explosive-Trap Falconer |

Four corners populated ⇒ the two axes are genuinely independent, not one axis mislabelled.

**Two things ruled OUT of these axes (not new coordinates):**
- **Retaliation** (thorns, reflect, block-counter) is a **defense-rider**, not an activation mode — it keys as a flag on **coord #6 (defense)**, because it is *how the kit survives*, not *how it delivers*.
- **Deployed-pulse** (totems/traps ticking on a timer) is already fully addressed by **delivery = SUMMON/ZONE (#2) × activation = triggered (#12)**; it needs no separate coordinate.

### 3A.1 — The intrinsic-vs-gear discriminator (the soul-bound-gear law)
`#12 = triggered` enters the key **only when the trigger is the kit's intrinsic core delivery** — Cast-on-Crit builds, Autobomber, Poet's Pen. These *are* trigger-shaped at their mechanical core; strip the trigger and the kit ceases to exist.

**Source builds whose trigger came from a bespoke unique item key as `active`, not `triggered`.** Andariel's-Visage ignite-proc, a helm that *is* the build — that reactivity was granted by a **kit-specific loot artifact we do not reproduce.** Our **soul-bound gear** (`agnostic-loot-engine-spec.md`) grants **no kit-specific mechanics**: it is kit-agnostic, mechanic-*adjusting* operators over universal axes (value / structural / transform) — the only itemization that scales across ~500 kits from ~15 incompatible source games. Soul-bound gear can add reactivity, but **only as a universal structural operator any kit may equip** — a *build choice*, never a cell-identity coordinate.

**This is the same law that governs ailment Layer-3 (§3) — THE GEAR LAW, in four clauses:**
- **Amplify your own** — gear scales a mechanic the kit *already owns* (an owner's control-effectiveness, an owner's minion count/quality). This is the specialist's reward for specializing.
- **Path texture to anyone** — gear may grant *texture* coordinates (movement #1, geometry #4, tempo #10, activation-trigger #12, cost-reduction #7…) to any kit as a build choice; texture is not cell-defining, so pathing it dilutes nothing.
- **Import no one's core** — gear never grants another cell's *core competency* (#5 control-specialization, #8 proxy/summon, #2 delivery-type) at specialist grade. Core may appear on a non-owner ONLY as **capped-garnish** — hard-capped, low-potency — never at the specialist's scaling tier.
- **Invent nothing** — every operator moves along an *existing* Class-A coordinate (§2); gear never mints a mechanic absent from the register.

The earlier "amplifier, never creator" was too tight — it forbade the legitimate *path-texture* clause. The four-clause law is the precise statement. So the discriminator is clean: **intrinsic trigger → keys `triggered`; gear-granted reactivity → keys `active`** (the base kit) **+ an equippable operator** (the build layer). The tell for elrond (§8): a `mech_note` reading "Cast-on-Crit **gem**" is intrinsic → `triggered`; "the **helm** IS the build" is gear → `active`.

---

## 3B — Coordinate #7: economy model-structure (Wave-B resolution)
"Economy" was overloading **two separable things** — the *mechanical structure* of how a kit pays for its power, and the *name* that structure wears in the source game. Separating them closes Wave B and de-risks the fantasy Matt flagged: *"a warrior with mana, or a sorceress spending rage, would immediately kill the fantasy."*

**The carve.**
- **Economy MODEL** — the mechanical cost-structure. **Class A, in the key.** Seven values (corpus `economy.model`, n = 478):

  | Model | What it is | n |
  |---|---|---|
  | **spend** | pay-per-cast pool (mana/energy/focus); regen-rate is a parameter | 183 |
  | **cooldown** | time-gated, no pool | 61 |
  | **generator-spender** | build via generators, spend via spenders (Fury/Hatred/Rage/Combo/Wrath); carries a `{continuous · combo · stack}` sub-structure | ~44 |
  | **reserve** | ongoing upkeep — auras, sustained minions, channel-sustain | ~47 |
  | **self-cost** | life/HP *is* the resource (blood magic) | 15 |
  | **finite** | consumable inputs — ammo · charges · recipe · corpses | ~37 |
  | **free** | no economy; paced by cooldown or trigger (folds `proc`) | residual |

  De-conflicts: `proc` → coord #12 (activation = triggered, economy = free); `channel` → coord #11 (commit = channel, economy = reserve). The `generator-spender` sub-structure `{continuous · combo · stack}` is a **strong hypothesis, split resolved at keying** (Matt 2026-07-13) — it does not fork the coordinate now.
- **Resource NAME** — the label the model wears (mana, fury, hatred, essence, combo points…). **NOT in the key.** It is a **1:1 preserved lineage attribute**, like `display_name`: read verbatim from source (`resource_verbatim`), never rolled, never re-derived.

**Why the name is preserved, not rolled — the principle: *roll the overlays that add experiential variety; preserve the overlays that are pure recognition.*** Element is a Class-B *roll* because changing it moves the kit through the 7×7 matchup matrix — real, felt variety. Resource-name, once the model is fixed, adds **zero** mechanical variety — Fury vs Rage is the same generator-spender; the name is a pure recognition anchor. Rolling it would only ever *break* recognition (the warrior-with-mana failure) for no variety gain. So it is preserved verbatim — a preserved overlay, not a rolled one.

**Empirical warrant for 1:1** (Matt's question — *"can a build map to more than one resource?"*): the corpus answers **no.** `resource_verbatim` is populated for 461/478 kits (96%), **strictly one economy fact per kit** — zero kits carry a resource *choice*. A WW Barb is Fury; it is not "Fury-or-Rage." 1:1 source-preservation is therefore strictly better than an allow-list — an allow-list would manufacture a choice the genre never offered. **The allow-list is demoted to a fallback:** for the 17 unknowns and any net-new (non-source) kit, where a model-appropriate name must be chosen because none was inherited.

**The "exact fit" gate is SATISFIED by construction.** Matt: *"fold it in after we are certain how we skin the resource for an exact fit."* 1:1 verbatim preservation **is** the exact fit — there is no skinning step to get wrong. The warrior keeps Fury because Fury is on its record; mana is impossible for it by construction.

**KWYK — this closes coordinate #8's summon-economy too.** "Summon economy" is not a separate axis; it is a **derived read**: `#7 economy-model ∩ delivery = SUMMON (#2) ∩ proxy density (#8)`. A heavy-proxy SUMMON kit on a **reserve** model is an upkeep-summoner; on **cooldown**, a cooldown-summoner. Closing #7 closes #8 — no separate fill.

**F5 dependency — engine-native MECHANIC fidelity is a BUILD gap, not a KEY gap.** The key is complete: every kit keys to one of the 7 models. But the *engine* today natively simulates only the mana-substrate + live martial economies (`econ_status`: 264 native, 174 `gap`). The 174 `gap` kits key correctly, yet their model (reserve / self-cost / generator-spender) is not yet natively costed in sim — this is the **F5 cost-type-bin** build (`agnostic-loot-engine-spec.md` §2 RESERVED / §8 R1: three structural cost-TYPE bins open at the F5 re-derivation event). Flagged as the economy-fidelity build dependency; it does **not** hold the key open.

---

## 4 — Explicitly EXCLUDED coordinates (and the reason)
| Coordinate | Class | Reason excluded |
|---|---|---|
| **element** | B | Schema-permanent `descriptor-final`; randomly rotated; not unique to a cell. Names functions (§3), never is one. |
| race · gender · culture · faction · hybridity · period · flavor | B | Emission overlays; mechanically inert; rolled at emission. |
| **attribute** | C | Engine re-derives it; will differ from the source value; would mislead players who know the source build. Matt-ruled OUT 2026-07-13. |

---

## 5 — The completeness gate (when the key is "done")
**The key matures as S4 ratifies mechanics.** Full-key operations — dedup, freeze, representative-selection (S5 / S8) — fire **only when the gap-map below closes.** Until then, S2/S3 (census views + periodic table) run *in front* of S4 as **steering instruments**, not portraits.

**S4 gap-map:**
| Coord | Gap | Population | S4 wave | State |
|---|---|---|---|---|
| #5 control / ailment | function sub-axis + naming | 205/470 (44%) ailment-gap | (this session) | **CLOSED** |
| #12 activation + #13 dependency | carved from the old "trigger / mark-consume" placeholder into two orthogonal axes (§3A); intrinsic-vs-gear discriminator ruled (§3A.1) | ~60 intrinsic-trigger; ~70 setup-payoff | Wave C | **CLOSED** |
| #7 economy model | 7 model-structure values ratified; resource-name 1:1-preserved out of key; engine cost-fidelity (174 econ-`gap`) deferred to F5 cost-type bins (§3B) | 7 values / 478 kits | Wave B | **CLOSED** |
| #8 summon-economy | derived read (#7 model ∩ SUMMON ∩ proxy) — closes with #7, not a separate axis (§3B) | 143 non-solo | Wave A | **CLOSED** |

**⊳ GATE STATE (2026-07-13): all four S4 waves CLOSED — no OPEN coordinate remains. The completeness gate is OPEN.** Full-key operations — dedup, representative-selection, freeze (§6) — are unblocked. Engine-native cost-fidelity for the 174 econ-`gap` kits is an F5 *build* dependency, not a *key* gap; the key is complete (§3B).

**Gate rule (standing):** do not force fine granularity or dedup while any OPEN item stands. Merging on an incomplete key forces a re-key later; splitting a cell as the key sharpens is cheap (§6). Split-late beats merge-wrong. (No item is currently OPEN — see gate state above; the rule governs any future re-open.)

---

## 6 — Dedup (grain + tiebreak) and the isotope model
Dedup has two independent parts, and the hard dependency is on **key-completeness (§5)**, not on tiebreak complexity.

- **Grain** — *who shares a cell* — is the **cell key**: a projection of the matured 13-tuple (§2) onto the coords that define "same build." **RATIFIED (Matt 2026-07-13): strict-13-tuple first, then coarsen with the data — see §6.1.** Grain-completeness = the S4 gate (now OPEN, §5).
- **Tiebreak** — *who is the primary representative* — is **simple and grain-independent:** longevity of lineage across games → recency → primary. Losers are **never deleted** — they are retained as mouseover **"isotopes."** Breadth is the pitch ("every build the genre ever made"); deletion would throw away the pitch.

**Isotope model.** A hexagon is one mechanical "element"; kits sharing a fully-resolved cell are its **isotopes** (true variants). As S4 sharpens the key, some cells **split** — an isotope resolves into its own element (the early-chemistry pattern). This is exactly why dedup waits on §5: a later split is cheap; a wrong early merge is a re-key.

### 6.1 — The ratified cell key (Matt 2026-07-13): strict-13 first, coarsen with the data

**Class A ≠ cell-defining.** The 13-tuple is the *identity* key; the *cell* key is a **projection** of it. Two isotopes differ on some Class-A coord — that difference is *what makes them isotopes* rather than identical rows. So the cell key = the subset of the 13 whose equality means "same build." That subset is decided in two stages:

**Stage 1 — the STRICT key = the full 13-tuple, exact-match.** Two kits share a cell iff identical on all 13 (with #5 contributing **both** treatment AND function; unknown / blank = its own literal value → conservative, never merges on absence). This is the *maximally-split* start: it **never wrong-merges.** Dedup v1 is a `GROUP BY` on the serialized `cell_key` — zero further grain guesswork. gamora runs it the moment the columns materialize (§8).

**Stage 2 — coarsen with the data (the grain-review pass).** Review the Stage-1 clusters: where two cells are the same build archetype differing only on one *texture* coord, demote that coord from cell-defining to isotope-distinguishing (collapsing the cells). This is a **reviewed merge with evidence** — the safe direction (split-late beats merge-wrong; Discipline #11 empirical-over-assumption, applied to the key itself). **The result of Stage 1 IS the evidence that drives Stage 2** — the grain is measured, never guessed a priori.

**Coarsening guardrails (gandalf lean — the demotable set is RULED at Stage 2 with the cluster data, NOT now):**
- **Never-demote core** (build identity — stays in the cell key regardless): **#2 delivery · #5 control (treatment + function) · #8 proxy · #1 movement · #12 activation · #13 dependency.**
- **Demotable-with-evidence** (in the strict v1 key; candidates for isotope-demotion if clusters show over-split): **#3 amp · #4 geometry · #6 defense · #7 economy-model · #9 range · #10 tempo · #11 commit.** (#7 is the contentious one — generator-spender is build-defining; mana-vs-cooldown often is not. The data rules.)

**Why strict-first, not a designed-coarse key up front:** a coarse key bakes in merges you cannot cheaply undo (re-key); strict-first bakes in nothing and *measures* the real collapse structure. Genre precedent: Mendeleev left gaps and split later — he never merged speculatively; poe.ninja clusters builds by a coarse projection (skill + support gems), but that projection was tuned against observed build data, not guessed. We tune ours against Stage-1 output.

**The gate to gamora:** the strict key is not runnable until elrond materializes the 4 non-column coords (#5-function, #7-model, #12, #13) and serializes `cell_key` (§8). Then: gamora strict-dedup → cluster review → Stage-2 coarsen. Representative-selection rides on top unchanged (the tiebreak above is grain-independent).

---

## 7 — Presentation contract (periodic table, S3)
- **One representative kit per cell** (hexagon / square); the rest sit **behind it** as a mouseover isotope list.
- The render keys off **Class-A coordinates only** — already true: `render_v1_2_stratified.py` keys off `geometry_value` + `mob_policy_while_casting` and builds `public_label` from engine fields; it never touches the deprecated `atlas_key_orig`.
- Pre-S4, the harness renders the **current-maturity** key as a steering view; the occupied-cell count it reports is **provisional** and will shift as coords #5/#7/#8 sharpen. (A prior element-excluded snapshot collapsed the ~470 combat kits toward ~396 occupied cells with shallow isotope depth — treat as illustrative scale only; the harness is the live source of truth.)

---

## 8 — Sequencing hooks
- **rocket** — implement §3.1: after the Class-A control function is fixed, roll the primary element from `eligibility ∩ function-allow-list`; universal functions roll free; emit the intersection-empty flag.
- **elrond** — **materialize the cell key (§6.1).** Promote to keyed columns the 4 coords that are not columns yet: **#5 control-function** sub-axis (from `canon_probe_facts` control family / `mech_note`, §3), **#7 economy-model** (the 7 values, from `canon_probe_facts` economy family, §3B — distinct from the existing `econ_status`), **#12 `activation_val`** + **#13 `dependency_val`** (per §3A, applying the §3A.1 discriminator — tell: `mech_note` "Cast-on-Crit **gem**" = intrinsic → `triggered`; "the **helm** IS the build" = gear → `active`). Also surface **`resource_verbatim`** as a column (1:1-preserved lineage; out of the cell key, needed for display, §3B). Then **serialize `cell_key`** = the canonical ordered 13-tuple (#5 contributes treatment+function; unknown/blank = literal value) — note this **spans two tables**: `canon_engine_key` (#1/#2/#4/#5/#6 + new #7-model/#12/#13) ⋈ `canon_corpus` (#3/#8/#9/#10/#11) on `kit_id`. The other 9 coords are already columns.
- **gamora** — dedup consumes `cell_key` **after elrond materializes it** (§5 is now OPEN). Dedup v1 = strict exact-match `GROUP BY cell_key` (§6.1 Stage 1); the cluster review then feeds Stage-2 coarsening. Matchup consumes the key likewise.
- **S3 harness** — renders the current key now; **S5** migration turns cell addresses into kit identity and fires dedup (§6); **S8** selects demo kits from representatives.

---

*This register is the canonical home for the kit-identity key. As S4 waves close the §5 gap-map, update the coordinate-status column (§2) and the gap-map (§5) here rather than forking a new doc.*
