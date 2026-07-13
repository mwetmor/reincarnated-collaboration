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
| **A — Mechanical identity** | **YES** | Measured from combat behavior; source-faithful; the cell address. | "Does it describe how the kit *fights*, invariant under re-skinning?" | the 11 coordinates in §2 |
| **B — Emission overlay** | **NO** | Rolled/rotated at emission; decorrelated from mechanics; colors name / portrait / flavor only. | "Is it rolled at emission and mechanically inert?" | element, race, gender, culture, faction, hybridity, period, flavor |
| **C — Transformation-mapping** | **NO** | The engine re-derives it by internal logic; the value **may differ from the source game's value.** | "Does our engine reassign it such that it can differ from the source?" | **attribute** (first member) |

**Why C is excluded and is not merely "dressing" (Matt, 2026-07-13):** attribute is neither identity (it isn't measured combat behavior) nor emission overlay (it isn't a free roll). It is a *many-games→one-game transformation input* — our engine assigns STR/DEX/INT/WIS by its own logic, which will frequently disagree with the attribute the kit carried in its source game. Putting it in the periodic table would actively mislead a player who knows the source build. It rides in the transformation layer, not the key.

**Why B is excluded — the element case specifically:** `elem_raw` is schema-marked *permanent "descriptor-final"* (never promoted to a keyed coordinate), unlike geo/ctrl/def/econ which promote to `keyed-v1`. Element is randomly rotated at emission and is not unique to a cell — a single mechanical cell contains kits of many elements. Element **names** mechanical functions (§3); it never **is** one.

---

## 2 — The mechanical-identity coordinates (Class A) — the eleven
Counts are combat-kit snapshots (n = 470) as of 2026-07-13.

| # | Coordinate | Source column | Values (cardinality) | Status |
|---|---|---|---|---|
| 1 | **Movement-while-casting** | `mob_policy_while_casting` | FREE-MOVE · WALK · ROOTED (3) | **LOCKED** (Q19) |
| 2 | **Delivery** | `delivery_value` | PROJECTILE · ORBITAL · NOVA · ZONE · BEAM · MELEE · SUMMON (7) | **LOCKED** (Q19) |
| 3 | **Amplitude stratum** | `amp_val` | FLAT · SPIKY · VAR (3) | **LOCKED** (Q19) |
| 4 | **Geometry sub-type** | `geometry_value` / `geo_raw`→keyed-v1 | ~21 raw shapes rolling up into #2 (circle, cone, chain, totem, dash, vortex…) | keyed, refine within #2 |
| 5 | **Control** (treatment + function) | `ctrl_treatment` + control-function tag | treatment: damage · control · hybrid (3); function sub-axis: §3 | **RESOLVED THIS SESSION** (was 205/470 ailment-gap) |
| 6 | **Defense** | `def_bin` | tank · mitigate · evade · absorb · glass (5) | keyed (215→28) |
| 7 | **Economy** | `econ_status` / `econ_meter_type` | native · partial · gap | **OPEN** — 161 pure-gap (34%), ~200 not-fully-native (43%) → S4 Wave B |
| 8 | **Proxy density** | `proxy_val` | solo · light · heavy (3) | keyed; summon-economy **OPEN** — 143 non-solo (78 light + 65 heavy) → S4 Wave A |
| 9 | **Range** | `range_val` | melee · mid · ranged · dual (4) | keyed |
| 10 | **Tempo** | `tempo_val` | low · med · high (3) | keyed |
| 11 | **Commit** | `commit_val` | instant · wind-up · channel (3) | keyed |

**The LOCKED skeleton = coords 1–3** — the Q19 plane, 3 × 7 × 3 = **63 buckets.** This is permanent. Coordinates 4–11 refine *within* each bucket. Attribute is **absent by ruling** (§1, Class C).

---

## 3 — Coordinate #5: the ailment architecture (the session's resolution)
"Ailment" was overloading **two distinct concepts.** Separating them dissolves the doubling problem and keeps element mechanically inert.

- **CONTROL** — crowd-control, kit-*designed*, **element-neutral**: hard-stop · stun · taunt · fear · blind · knockback · expose (damage-amp) · hex/curse · silence. → **Class A, coordinate #5's function sub-axis.**
- **ELEMENTAL AILMENT** — damage-type debuff / DoT, **element-inherent** flavor: ignite · chill · shock · poison · bleed. → **Class B emission.**

**The load-bearing insight: element NAMES a control function; it does not ADD a second effect.** A hard-stop is the same mechanical stop whether it surfaces as *freeze* (ice) or *petrify* (earth). No second effect is stapled on, so the population never doubles and element stays inert.

**Three layers:**
- **Layer 1 — CONTROL** (Class A key; element-neutral; element-*names*-it). The mechanical function lives here.
- **Layer 2 — ELEMENTAL AILMENT** (Class B emission; weak, always-on, flavor-tier; supplies element↔ailment continuity). When a same-family Layer-1 control is present, Layer 2 is *absorbed* into the Layer-1 naming rather than double-counted.
- **Layer 3 — GEAR AMPLIFICATION** (**DEFERRED** to a gear-axis follow-on): soulbound gear amplifies a latent/signature ailment. Amplifier, never creator — build-crafting + loot relevance + the isekai "gear awakens power" beat. Scoped later; noted here so the seam is reserved.

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
| #7 economy | reservation / aura / meter | 161 pure-gap (34%); ~200 (43%) not-fully-native | Wave B | **OPEN** |
| #8 proxy | summon / companion economy | 143 non-solo | Wave A | **OPEN** |
| — trigger / mark-consume | a **new axis, currently unschema'd** | TBD | Wave C | **OPEN** |

**Gate rule:** do not force fine granularity or dedup while any OPEN item stands. Merging on an incomplete key forces a re-key later; splitting a cell as the key sharpens is cheap (§6). Split-late beats merge-wrong.

---

## 6 — Dedup (grain + tiebreak) and the isotope model
Dedup has two independent parts, and the hard dependency is on **key-completeness (§5)**, not on tiebreak complexity.

- **Grain** — *who shares a cell* — is set entirely by the matured key (§2). Grain-completeness = the S4 gate.
- **Tiebreak** — *who is the primary representative* — is **simple and grain-independent:** longevity of lineage across games → recency → primary. Losers are **never deleted** — they are retained as mouseover **"isotopes."** Breadth is the pitch ("every build the genre ever made"); deletion would throw away the pitch.

**Isotope model.** A hexagon is one mechanical "element"; kits sharing a fully-resolved cell are its **isotopes** (true variants). As S4 sharpens the key, some cells **split** — an isotope resolves into its own element (the early-chemistry pattern). This is exactly why dedup waits on §5: a later split is cheap; a wrong early merge is a re-key.

---

## 7 — Presentation contract (periodic table, S3)
- **One representative kit per cell** (hexagon / square); the rest sit **behind it** as a mouseover isotope list.
- The render keys off **Class-A coordinates only** — already true: `render_v1_2_stratified.py` keys off `geometry_value` + `mob_policy_while_casting` and builds `public_label` from engine fields; it never touches the deprecated `atlas_key_orig`.
- Pre-S4, the harness renders the **current-maturity** key as a steering view; the occupied-cell count it reports is **provisional** and will shift as coords #5/#7/#8 sharpen. (A prior element-excluded snapshot collapsed the ~470 combat kits toward ~396 occupied cells with shallow isotope depth — treat as illustrative scale only; the harness is the live source of truth.)

---

## 8 — Sequencing hooks
- **rocket** — implement §3.1: after the Class-A control function is fixed, roll the primary element from `eligibility ∩ function-allow-list`; universal functions roll free; emit the intersection-empty flag.
- **elrond** — promote the control-function sub-axis (§3) to a keyed column; author the economy (#7) and summon-economy (#8) gap-fill columns as their S4 waves land.
- **gamora** — dedup + matchup consume the key **only after** §5 closes.
- **S3 harness** — renders the current key now; **S5** migration turns cell addresses into kit identity and fires dedup (§6); **S8** selects demo kits from representatives.

---

*This register is the canonical home for the kit-identity key. As S4 waves close the §5 gap-map, update the coordinate-status column (§2) and the gap-map (§5) here rather than forking a new doc.*
