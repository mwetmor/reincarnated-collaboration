# SHAPESHIFT (GX-02) — Design Docket (ELICITOR-shaped; fork-surfacing)

**STATUS:** GATED DOCKET — forks OPEN for Matt; gandalf-prime DRIFT-CRITIC **PASS-WITH-NOTES** (2026-07-16, same session).
**Date:** 2026-07-16
**Author:** gandalf (sub-agent, ELICITOR role; atlas-parity autonomous run under Matt authorization 2026-07-16)
**Route:** ✓ gandalf-prime DRIFT-CRITIC gate (below) → Matt rulings (docket-3 sitting or earlier at his pleasure) → then a SPEC-AUTHOR docket-to-spec pass.

> **DRIFT-CRITIC GATE STAMP (gandalf-prime, 2026-07-16):**
> 1. **Verdict: PASS-WITH-NOTES.** Fork discipline, evidence triangulation, engine grounding, and DL-03 check all sound. All six leans are **PRIME-CONCURRED** as design priors — A2 (decision-cadence is the honest family boundary; AURA/TOTEM-SENTRY split logic; kit grain = loop identity, and Ferality vs PBA ARE different loops) · B3 · C1+C2 pairing (C4 rides temporal-window as config variant) · **D5-with-D3-Wave-1-slice especially** (the docket's sequencing insight: cooldown-lockout has zero new-economy dependency; gauge-coupled entry waits for GX-19, which outranks shapeshift on the family docket anyway) · E5 compositional (Wave-A side-clock discipline; commit_state stays per-cast) · F2. **Forks remain OPEN — Matt rules.**
> 2. **NAMING RULED (gandalf-prime seam — style register / vocabulary stewardship; veto-open):** §3.4's collision resolves as option 2 — **shapeshift renames; the in-fight state noun is `shape`** (`shape_active`, `shape_gate`, `shape_state_machine.py`, "Bear shape" / "Fox shape" at player surface). **"Form" stays EXCLUSIVELY the ascended-lineage / Court-of-Forms / form-library concept** — that is core meta-layer story vocabulary (Earth-Self form library; spirit-guide-as-future-self) and outranks. Grounds: `shape` is the honest genre word with D2 lineage (the tree is literally "Shape Shifting"); launder-clean in the engine namespace; `stance` is RESERVED for a possible STANCE-DANCE family label (A3/F3 vocabulary orthogonality); `body` collides with seasonal body-swap; `vessel`/`guise` fail common-vocab (the D1 element-name lesson). Renaming Court instead = HIGH churn on story canon that is correct as-is; namespacing both = permanent ambiguity. The class fantasy may still say "shapeshift" freely — the STATE is `shape`.
> 3. **Stale-line correction:** §Fork F's "the E4 refit is currently running" is superseded — E4 COMPLETED + verified this session; it sits at Matt's ratification gate. The substantive point survives: shape families queue for a future edition's admission via the docket-3 review sitting, never E4.
**Authority:** GX-02 form-shift ratified keystone gap, ranked #3 on the family discovery docket (`canonical/current-to-end-state/current-to-end-state-engine.md` §Ranked-docket — after MELEE-STRIKE, GAUGE/BUILDER-SPENDER). Evidence debt just paid — three fresh attestations (LA Wildsoul Ferality + PBA, GD Berserker Wereforms) join the accumulated exhibits (D2 Druid, D4 Druid, LA Shadowhunter Demonize).
**Companion docs:**
- `agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/01-la-ferality-wildsoul.md` — attestation 1 (STRONG, persistent-form)
- `agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/02-la-phantom-beast-awakening-wildsoul.md` — attestation 2 (MEDIUM, temporal-window)
- `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` — sibling engine-spec style + commit_state machinery + proxy layer template
- `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` — sibling layer, just Gate-1-passed (§0/§1 pattern; ESCALATION-block pattern; DL-03 fold-in pattern)
- Engine surfaces read (read-only): `simulation/spatial_gauntlet/commitment_state_machine.py` (bin snap/wind-up/channel; commit_state idle/committing/channeling; move_policy rooted/walk/full_move) · `simulation/spatial_gauntlet/spatial_engine.py:670,787-798,2191-2287,2802-2805` (player commit_state, move_policy consumption) · `generation/kit_architecture.py` (Architecture enum: single/hybrid-2/physical-hybrid — no runtime kit swap) · `foundation/court_persistence.py` (Court-of-Forms is ascended-form persistence, NOT in-fight body-swap — semantic reservation exists)

**ELICITOR discipline:** every fork below carries options + tradeoffs + genre precedent (game+system) + player-consequence + a stated LEAN with grounds. **Matt rules. gandalf does not close.** The lean is a design-informed prior, not a closure.

---

## §0 — TL;DR

Shapeshift is genuinely NEW engine work. The Wave-A proxy layer + ailment layer + commit_state machinery cover ~40% of what shapeshift needs — enough that the seam is engine-legible — but four architectural questions have no incumbent answer in the engine today:

1. **Whether "form" is one atlas family or two** — persistent-form and temporal-window are mechanically distinct enough that they may deserve to sit as separate atlas citizens (parallel to how DoT/AILMENT sits distinct from CHANNELED-BEAM even though both are "damage-over-time-ish").
2. **How form persists** — persistent-loop (Ferality alternation) vs temporal-window super-mode (PBA Z-form, D3 Archon lineage) vs stance-dance (fast in-combat toggle without a super-mode wrap).
3. **What skill slots do under form** — locked subset (only Fox-skills castable in Fox form) vs remapped (skills re-derive their effect per form) vs whole-kit swap (form = whole new loadout).
4. **How form entry couples to economy** — gauge-fill wind-up (fill-to-enter) vs cooldown-lockout (fixed re-entry timer) vs both (two families).

Plus one grammar coordinate:
5. **Where does form sit in commit_state?** — is form entry a new commit_state (`transforming`)? Is form itself a new persistent player state parallel to `commit_state`? Or is form an ailment-adjacent buff with skill-set replacement machinery on top?

**Wave-A comparison for calibration:** Wave-A introduced ONE mechanical primitive (proxy absorption + commit-clock on proxy entity) with four economy variants + one calibration axis (C1a floor / C1b endgame). Shapeshift will need at LEAST two mechanical primitives (form-state + skill-availability re-routing) with 2–3 economies + a commitment-grammar coordinate. **Scope is at minimum equal to Wave A, likely larger** — this is a signal that the fork rulings matter, not that the work is impossible.

**No player-consequence rulings closed here.** The docket exists to surface the forks before spec pretends to close them.

---

## §1 — Evidence synthesis (the attested geometries as a small taxonomy)

Five exhibits with dated attestations; three fresh (2026-07-16 Legolas dossiers + GD 2026-07 patch).

### 1.1 Persistence axis (how long the form lasts)

| Axis value | Exhibit | System name | Signature marker |
|---|---|---|---|
| **PERSISTENT-LOOP** (form-swap as rotation cadence) | LA Wildsoul Ferality [dossier 01] | Ferality engraving; Fox↔Bear alternation on per-skill cadence | Both forms exist in the player's active loop; Phantom Beast Energy spent to swap forms; ordered-pair rotation ("3-2-3 setup") |
| **PERSISTENT-LOOP** | D2 Druid Werewolf/Werebear | Lycanthropy (persistent buff) + Werewolf/Werebear skills (persistent form toggles) | Player enters form and stays until manually swapped or unshifted; skills gated by which form |
| **TEMPORAL-WINDOW** (form is a timed super-mode) | LA Wildsoul PBA [dossier 02] | Phantom Beast Awakening engraving; Z-triggered 30s state after meter-fill | Base state → fill gauge → Z activates 30s form → landing skills accumulates Phantom Beast Spirit stacks → Z again converts stacks to cooldown reduction (self-recycling) |
| **TEMPORAL-WINDOW** | LA Shadowhunter Demonize (accumulated exhibit) | Demonize (identity skill); temporary demon-form | Meter-fill → activate → timed transformation state → auto-expire |
| **TEMPORAL-WINDOW** | D3 Wizard Archon (accumulated exhibit) | Archon (skill); 20s form-swap ultimate | Cooldown-gated entry; entire skill palette replaced; stat re-basing |
| **TEMPORAL-WINDOW** | GD Berserker Wereforms [Fangs of Asterkarn, 2026-07] | Werebear + Wereboar transformations, cooldown-gated | Cooldown-triggered entry; timed active-form window with wereform-specific skills |
| **PERSISTENT-LOOP w/ STANCE-DANCE flavor** | D4 Druid Werewolf/Werebear | Spirit-form on-skill-use (form determined by last skill cast) | Player is in whichever form their last cast implied; skills auto-shift; no gauge, no timer — pure skill-driven state |

**Geometric read:** three sub-shapes are attested in the corpus.
- **PERSISTENT-LOOP** — form is the resting state you cycle within (Ferality, D2 Druid).
- **TEMPORAL-WINDOW** — form is a super-mode you occasionally enter (PBA, Archon, GD Wereforms, Demonize).
- **STANCE-DANCE** — form is skill-implied and shifts in-flight (D4 Druid). Debatably a persistent-loop sub-variant with implicit swap-triggers instead of explicit ones.

> **ANNEX (post-gate, 2026-07-16 legolas econ re-crawl — evidence only, forks untouched):** the re-crawl's `gd-berserker-wereforms` row (grimdawn.com official mastery page) refines the GD exhibit two ways. (1) **Fork-B evidence:** *"Transformations are temporary, and Berserker has means to extend their duration or even to make them permanent"* — the GD exhibit sits on a TEMPORAL-WINDOW→PERSISTENT-LOOP **slider**, not a fixed point; direct corpus support for the B3 lean (support both persistence models). Econ-side it classified `persistent-condition / activation-toggle` (Wave-B PC bin), consistent with ruling 10's SS→this-docket routing (shapeshift owns form-lock econ). (2) **Form-name discrepancy flagged:** this table says "Werebear + Wereboar"; the official mastery page says **werewolf / wereraven** (wereraven = ranged + ice magic). Official-source wording wins pending the docket-to-spec pass; the geometry (cooldown-gated timed window, extendable) is unaffected.

### 1.2 Skill-slot semantics under form (how the loadout reacts)

| Semantics | Exhibit | Mechanic |
|---|---|---|
| **LOCKED SUBSET** (form gates which slots are castable) | Ferality Wildsoul | Fox skills castable ONLY in Fox form; Bear skills ONLY in Bear form; neutrals (Claw) any form; ultimates gated to matching form |
| **LOCKED SUBSET** | D2 Druid | Werewolf skills require werewolf form; Werebear skills require werebear form; caster skills unavailable in shifted form |
| **REMAPPED (whole-kit swap)** | D3 Wizard Archon | Every action bar slot replaced with Archon-specific abilities during 20s window; base skills unavailable |
| **REMAPPED (whole-kit swap)** | GD Berserker Wereforms | Wereform-specific skill palette during transformation window |
| **COLLAPSED-SUBSET** (form removes the partition inside itself) | PBA Wildsoul | Inside PBA state, BOTH Fox and Bear skills castable (Ferality's partition dissolves inside the super-mode) |
| **REMAPPED w/ SKILL-DRIVEN TRIGGER** | D4 Druid | Slot skills tagged as werewolf-cast or werebear-cast; casting a tagged skill implicitly shifts form + resolves effect |
| **AMPLIFIER** (form buffs existing skills; no partition) | LA Shadowhunter Demonize | Demon form empowers existing skills + adds demon-exclusive spells alongside base kit (partial-replacement) |

**Geometric read:** three sub-shapes at the slot-semantics layer, and they are semi-independent of the persistence axis (Ferality = persistent + locked-subset; PBA = temporal + collapsed-subset; Archon = temporal + whole-kit-swap; D4 Druid = persistent-ish + skill-driven-remap). **Two dimensions matter, and they compose.**

### 1.3 Entry economy (how you get INTO the form)

| Economy | Exhibit | Mechanic |
|---|---|---|
| **BUILD-TO-SPEND** (gauge fill → spend to enter) | Ferality Wildsoul | Phantom Beast Energy accumulates; transformation skills spend it |
| **BUILD-TO-TRIGGER** (gauge fill → free trigger to enter) | PBA Wildsoul | Phantom Beast Meter accumulates; Z-press activates PBA state at zero-cost once meter is full |
| **BUILD-TO-TRIGGER** | LA Shadowhunter Demonize | Identity meter fills → activation is meter-consuming trigger |
| **COOLDOWN-LOCKOUT** (fixed-timer re-entry) | D3 Archon, GD Wereforms | Skill cooldown gates re-entry; no ambient fill required |
| **PERSISTENT (no entry cost)** | D2 Druid | Lycanthropy is a passive; form is toggled by skill cast |
| **SKILL-DRIVEN** (form implicit from action selection) | D4 Druid | No entry cost per se; form shifts as skills are cast |
| **DURATION-DRAIN** (form drains a resource while active) | (Archon-adjacent; GD wereforms partial) | Time-in-form consumes a bar that ticks down |

**Geometric read:** the entry-economy axis has 4–5 sub-shapes. **Two dominant families are attested at the atlas-worthy layer:** BUILD-TO-TRIGGER (gauge-coupled) and COOLDOWN-LOCKOUT (cooldown-coupled). Fork D below decides whether these are one atlas family with a config axis or two atlas families with distinct grammar coordinates.

### 1.4 Player-consequence framing (what the player feels differently, per shape)

- **PERSISTENT-LOOP + LOCKED-SUBSET (Ferality):** every cast decision carries a form-cost. The rotation IS the identity. Skill routing is spatially-partitioned: half your loadout is "wrong form" at any moment. Fantasy = **you ARE the beast, alternating faces.**
- **TEMPORAL-WINDOW + WHOLE-KIT-SWAP (Archon, GD Wereforms):** the transformation is a burst window. Downtime = base kit; uptime = burst kit. Fantasy = **you become the beast briefly, then return.**
- **TEMPORAL-WINDOW + COLLAPSED-SUBSET (PBA):** super-mode compresses the base tension. Inside the window, everything is available; outside, you're grinding to open it. Fantasy = **you unlock a temporary apex form.**
- **PERSISTENT + SKILL-DRIVEN-REMAP (D4 Druid):** low-friction; form is decorative-plus-mechanical. Fantasy = **you flow between forms as combat demands.** Least-committed shapeshift shape.
- **STANCE-DANCE (D4 Druid variant / general stance kits):** form is a fast tactical layer; entry costs are low. Fantasy = **your combat toolkit has two channels you tab between.**

**No RDR player-consequence ruling is CLOSED here.** The seam should express whichever fantasy Matt selects; the point is the axes are legibly separable.

---

## §2 — THE FORKS (ELICITOR-shaped; OPEN)

Six forks. Each carries options + tradeoffs + genre precedent + player-consequence + gandalf lean + grounds. **Matt rules; gandalf does not close.**

---

### FORK A — Is form-shift ONE atlas family or TWO?

**The question.** Persistent-form (Ferality, D2 Druid) and temporal-window (PBA, Archon, GD Wereforms) are attested at similar corpus weight. Do they sit as ONE family (SHAPESHIFT) with a persistence-axis config parameter, or TWO families (PERSISTENT-FORM + TEMPORAL-WINDOW-FORM) at the atlas level?

**Precedent for either resolution:**
- **ONE family:** ailment-layer chose ONE family for damage-amp (sunder) even though genre attests multiple shapes (D4 Vulnerable / PoE1 shock-magnitude / GD RR-window / Hades Privileged Status) — the shapes were config parameterizations of one primitive.
- **TWO families:** the E4 atlas splits AURA and TOTEM-SENTRY into distinct citizens even though both are "persistent stationary emitter" adjacents, because the player-consequence layer is different (aura = radial-buff / totem = damage-emitter). GAUGE/BUILDER-SPENDER (GX-19, atlas-ripe) is being handled as a family distinct from RESOURCE-DRAIN even though both are economies.

**Options:**
- **A1 — ONE family (SHAPESHIFT), persistence-axis is a config parameter.** Genre precedent: config-parameterization of one primitive (sunder). Tradeoffs: keeps atlas count manageable; makes cross-form config compose (a Ferality kit and a PBA kit share the same feature-space); risks the atlas losing signal at the plane-address layer (both forms occupy adjacent-but-distinct cells and the coordinate confuses).
- **A2 — TWO families (PERSISTENT-FORM + TEMPORAL-WINDOW-FORM).** Genre precedent: the player-consequence-driven family-split of AURA vs TOTEM-SENTRY. Tradeoffs: reflects the mechanical grammar honestly (rotation-identity vs burst-window are DIFFERENT experiences); enables the atlas to seat each with its own commitment-grammar coordinate; costs one atlas citizen (currently ~6 named families → ~7 named families); risks fragmenting a class-fantasy that reads as unified genre-wide ("the shapeshifter" is a Diablo audience cognitive category regardless of temporal shape).
- **A3 — TWO families with THREE citizens (add STANCE-DANCE).** Same as A2 but split further: PERSISTENT-FORM (Ferality/D2), TEMPORAL-WINDOW-FORM (PBA/Archon/GD), STANCE-DANCE (D4 Druid / general stance kits). Tradeoffs: highest fidelity to attested geometry; risks over-splitting on the strength of one exhibit (D4 Druid stance flavor).

**Player consequence:** if A1, the RDR class-fantasy "shapeshifter" reads unified across forms — a design flexibility Matt has historically valued. If A2, the RDR player picks between "become the beast (persistent)" and "unleash the beast (temporal)" as two distinct build-paths — closer to the corpus's actual player-facing surface.

**gandalf lean: A2 (TWO families).** Grounds: the persistence axis carries the **larger player-consequence delta** in the attested corpus (a Ferality kit and a PBA kit share ~40% of skills but ~0% of decision-cadence — Ferality is per-cast rotation, PBA is meter-fill-then-30s-burst). A1 would collapse this into a config parameter and lose the signal. A2 mirrors AURA/TOTEM-SENTRY family-split logic. A3 is over-fit on one exhibit; D4 Druid's stance-flavor sits within PERSISTENT-FORM as a low-friction sub-shape. **But A2 imports a scope cost: two families = two spec docs = two calibration passes.** Matt rules.

**Strongest evidence:** LA dossier 01 (Ferality) vs LA dossier 02 (PBA) side-by-side — the same class chassis produces two mechanically-distinct atlas rows because the persistence axis IS the identity delta. If Wildsoul's two engravings warrant two atlas rows (which they do — the corpus curated them separately), then RDR's family taxonomy should mirror the distinction.

---

### FORK B — Persistence model (how long does form last?)

**The question.** Given A ruling (whether one family or two), what persistence model(s) does the engine express?

**Options:**
- **B1 — Persistent-loop ONLY.** Form is entered and remains until player unshifts or swaps to another form. Attested: Ferality (loop-alternation), D2 Druid (toggle). Tradeoffs: closest to the Diablo audience's "you ARE the beast" fantasy; simplest state-machine (form ∈ {none, form_A, form_B, ...}); loses temporal-window burst-window design space.
- **B2 — Temporal-window ONLY.** Form is a timed super-mode with an entry trigger and auto-expiry. Attested: PBA (30s), Archon (20s), GD Wereforms (cooldown-gated timer). Tradeoffs: cleaner integration with cooldown/gauge machinery (already engine-legible); "shapeshift as burst-window" reads as a build-diversifier rather than a build-identity; loses persistent-loop identity fantasy.
- **B3 — BOTH (persistent-loop AND temporal-window).** Engine expresses form as `form_active: str | None` (persistent-loop) AND supports a `form_duration_remaining_s: float | None` field for temporal-window kits. Attested: the corpus itself carries both. Tradeoffs: highest fidelity; largest scope; requires the state-machine to compose cleanly with commit_state (Fork E).
- **B4 — Persistent + skill-driven-shift (D4 Druid model).** Form is persistent but shifts implicitly on skill cast, no explicit entry action. Tradeoffs: lowest-friction shape; least commitment-cost per shift; risks feeling not-shapeshifty (form is decorative rather than identity-defining).

**Player consequence:** B1 = "the shapeshifter is a class"; B2 = "shapeshift is a mid-fight verb"; B3 = "there are two shapeshifter classes"; B4 = "shapeshift is a rotational flavor."

**gandalf lean: B3 (BOTH persistent AND temporal), conditional on Fork A ruling A2 or A3.** If A1 (one family), then B3 becomes B1 + B2 configurable at emission — cleaner. If A2 (two families), B3 is definitionally the ruling (each family owns one persistence model). Grounds: the corpus attests both at comparable weight; excluding either would refuse a shipped genre pattern. B4 is a sub-shape of B1 the emission layer can express as a config parameter (skill-shift-implicit vs explicit-shift-required).

**Strongest evidence:** GD Fangs of Asterkarn Wereforms (2026-07) as the third temporal-window attestation stacked on PBA + Archon — the temporal-window shape has cross-decade cross-game persistence. Ferality + D2 Druid give the persistent-loop shape parallel weight.

---

### FORK C — Skill-slot semantics under form

**The question.** When a form is active, what does the player's skill loadout look like?

**Options:**
- **C1 — LOCKED SUBSET (skills tagged; form gates castability).** Skills carry a `form_gate: str | list[str] | None` field; a skill is castable only when its form_gate matches the active form. Attested: Ferality (Fox/Bear/neutral tagging), D2 Druid. Engine work: emit form_gate on skills; sim consults it at cast-check. Tradeoffs: cleanest; extends the existing cast-check flow with one field; introduces "wasted slot" perception (half your bar is grayed out).
- **C2 — REMAPPED (whole-kit swap on form entry).** Form entry replaces the entire action bar with a form-specific kit. Attested: D3 Archon, GD Wereforms. Engine work: significant — a `form_kit_index: dict[str, list[Skill]]` structure on the player + kit-swap machinery in the sim's player-action-selection loop. Tradeoffs: cleanest player-consequence (form = new class briefly); largest engine scope; interacts hard with progression (do form-kits level independently? per-form gear affix routing?).
- **C3 — SKILL-DRIVEN-REMAP (D4 Druid: skill-cast implies form).** Skills carry a `form_implication: str | None` field; casting a skill shifts the player into its implied form + resolves the skill. Attested: D4 Druid. Engine work: modest — one field + a state-transition hook at cast resolution. Tradeoffs: lowest-friction; no wasted-slot perception; risks the form-shift feeling accidental / not identity-defining.
- **C4 — COLLAPSED-SUBSET (form REMOVES a partition, does not add one).** PBA-shape: outside form, kit is partitioned; inside form, partition dissolves and all skills castable. Attested: PBA. Engine work: form_gate field + a "form_disables_gate" bool on the form definition. Tradeoffs: unique player-consequence (form is a *permission* burst, not a *substitution* burst); only sensibly composes with a persistent-loop layer that already partitions.
- **C5 — AMPLIFIER-only (form buffs existing skills, no partition, no substitution).** Attested: LA Shadowhunter Demonize (partial). Tradeoffs: lowest engine work; loses "shapeshift" flavor entirely (becomes a self-buff variant of the ailment layer's `sunder`).

**Player consequence:** C1 = "I have two decks and I toggle"; C2 = "I have a base class and a rage form"; C3 = "my form flows with my casts"; C4 = "my burst window is more expressive"; C5 = "I'm a slightly-transformed spellcaster."

**gandalf lean: C1 + C2 as a config choice per family (persistent-loop → C1; temporal-window → C2).** Grounds: the attested corpus cleanly pairs LOCKED-SUBSET with PERSISTENT-LOOP and REMAPPED with TEMPORAL-WINDOW. C3/C4 are sub-shapes each family can additionally express (C4 is a natural temporal-window variant; C3 is a natural persistent-loop variant). C5 is degenerate — do NOT ship it as the primary; if desired, it lives in the ailment layer, not here. **But the C1+C2 pairing is the ELICITOR-shaped lean, not a ruling — Matt may prefer to ship one and defer the other.**

**Strongest evidence:** Ferality dossier 01 documents LOCKED-SUBSET as the ordered-pair rotation ("Fox skills cannot be cast in Bear form and vice versa") — the persistent-loop family's signature. Archon (accumulated genre knowledge; D3 shipped 2012) documents REMAPPED whole-kit swap — the temporal-window family's signature.

---

### FORK D — Entry economy (build-to-spend vs cooldown-lockout vs duration-drain)

**The question.** How does the player GET INTO the form?

**Options:**
- **D1 — BUILD-TO-SPEND (spend gauge to swap forms).** Ferality-shape. Gauge fills passively + accelerated by non-form skills; transformation skills spend it. Tradeoffs: composes with the GX-19 gauge-economy family already atlas-ripe (rank #2 on the family docket); "shape-swap has a cost you feel" — good tension; requires the gauge economy layer to be built first (or in parallel).
- **D2 — BUILD-TO-TRIGGER (fill gauge → free trigger to enter).** PBA-shape; Demonize-shape. Gauge fills to full → button press enters form at zero incremental cost → form auto-expires. Tradeoffs: cleaner temporal-window pairing; composes with the GX-19 gauge-economy family in a mode-2 variant (build-to-consume-in-full); "the fill IS the wind-up" — reads as a natural burst-window.
- **D3 — COOLDOWN-LOCKOUT (fixed timer for re-entry).** Archon-shape, GD Wereforms-shape. Form entry is a skill on cooldown; no ambient fill required. Tradeoffs: simplest to build (no new economy); loses the "build-toward-burst" tension; makes shapeshift feel like just-another-cooldown-skill.
- **D4 — DURATION-DRAIN (form consumes resource while active).** Archon-flavored (secondary bar). Tradeoffs: pairs with D3 or D1; adds a "you can extend form by managing resource" layer; complicates state-machine.
- **D5 — ALL FOUR AS EMISSION-CONFIGURABLE ECONOMIES.** Mirror Wave-A's Fork-A ruling (ALL-4 economies). Tradeoffs: highest scope; highest fidelity; requires the GX-19 gauge economy to land BEFORE this fork's D1/D2 slices ship (dependency).

**Player consequence:** D1 = "shape is a resource I manage"; D2 = "burst opens when the meter fills"; D3 = "I use my transformation on cooldown"; D4 = "form has an internal timer I extend"; D5 = "each kit picks its economy."

**gandalf lean: D5 with D3 as the Wave-1 shippable slice (config the axis, ship the cooldown variant first, D1/D2 land after GX-19 gauge economy ratifies).** Grounds: Wave-A's D5-analog (ALL-4 economies) has proven the emission-configurable-economy pattern works. Cooldown-lockout is the LOWEST-dependency variant — it requires only existing cooldown machinery (already in-engine). Gauge-coupled variants (D1/D2) DEPEND ON the gauge economy layer whose atlas family (GX-19) is ranked #2 on the docket ABOVE this one. Ship shapeshift-cooldown as a Wave-1 slice, defer gauge-coupled shapeshift to Wave-2 after GX-19 lands. **Matt rules on ordering; the axis-config approach is the lean.**

**Strongest evidence:** GD Berserker Wereforms (Fangs of Asterkarn, 2026-07) is a live, current, cooldown-gated wereform — the third temporal-window attestation and the cleanest D3-only exhibit. Wave-A's ALL-4-economies ruling shows the config-axis pattern is the RDR house style.

---

### FORK E — Commitment-grammar coordinates (which commit_state cells does form occupy?)

**The question.** The engine already has a commit_state machine with three bins (SNAP / WIND-UP / CHANNEL) and player-side states (idle / committing / channeling). Where does FORM sit? Is form-entry a new commit_state bin, a new player-state, or something orthogonal?

**Engine-legibility check (read-only survey):**
- `commit_state` is a per-cast player-side machine — it resolves and returns to `idle` per skill cast.
- Form is (in most attested shapes) a PERSISTENT player state — an active form persists across many skill casts.
- Form does not fit the existing `committing/channeling` semantics: those describe THIS cast, not "I am currently a bear."
- BUT form-ENTRY (the transformation animation itself) IS a cast — it fits WIND-UP semantics naturally (Ferality's ordered-pair transformation "wind-up macro pattern" per dossier 01 §Commitment; Archon and PBA both have visible entry animations).

**Options:**
- **E1 — Form as new PERSISTENT PLAYER STATE, orthogonal to commit_state.** Add `form_active: str | None`, `form_duration_remaining_s: float | None` fields to the player entity. Form-ENTRY is a WIND-UP cast (existing bin); form-EXIT is either a WIND-UP cast (Ferality unshift), an auto-expire (temporal-window), or a WIND-UP swap (Ferality Fox→Bear). Skill castability check consults BOTH form_active AND commit_state. Tradeoffs: cleanest separation — commit_state stays a per-cast machine; form is a persistent flag. Composes with move_policy naturally (form buffs can multiply move_policy). Adds one player-state layer.
- **E2 — Form as a fourth commit_state ("transformed").** Player's commit_state becomes idle / committing / channeling / transformed. Tradeoffs: over-fits the commit_state machine to a use it wasn't designed for. commit_state per its docstring is a PER-CAST resolution state; making it also carry PERSISTENT identity is a semantic overload. **Anti-lean.**
- **E3 — Form as an ActiveEffect on the player (ailment-adjacent).** Model form as a specialized ActiveEffect: `name="form:werebear"`, duration, tags. Tradeoffs: reuses existing ActiveEffect machinery; risks losing the identity-layer signal (form ≠ debuff); ActiveEffects live on `combatant_state.active_effects` which is designed for defender-side debuffs. **Anti-lean** — semantic mismatch.
- **E4 — Form as a new sim subsystem entirely.** A `form_state_machine.py` sibling to `commitment_state_machine.py`. Tradeoffs: highest engine work; cleanest architectural separation; matches Wave-A's `commitment_state_machine.py` pattern.
- **E5 — Form-entry is a WIND-UP cast (existing bin); form-persistence is E1 (new player state); form-swap is another WIND-UP cast; form-exit-on-expire is a state-machine transition on form_state.** Compositional. Tradeoffs: mixes multiple engine seams; requires clean cross-machine coordination; matches how ailment-layer's freeze composes hard-control-enforcement with sim-side apply hooks.

**gandalf lean: E5 (compositional): form entry uses the existing WIND-UP bin (Ferality's ordered-pair rotation IS a wind-up macro; PBA's Z-press is a snap-shape with immediate form-entry; Archon's entry has a small animation cast_time — WIND-UP bin fits all three); form-persistence uses new fields (E1) on the player entity; form-swap is another WIND-UP cast; form-exit auto-fires from a `form_state_machine.py` per-tick check for temporal-window kits (E4 sub-shape).** Grounds: E5 reuses the existing commit_state machinery for the CAST layer (do not rebuild) and adds a minimal new player-state for the PERSISTENCE layer (form_active is genuinely new). **Matt rules on the composition; the axis is the lean.**

**Strongest evidence:** Wave-A engine spec §4 documents the pattern of adding a proxy-side commit-clock without touching the player commit_state — the SAME architectural pattern applies here: add form-side state without polluting commit_state. `spatial_engine.py:2191-2287` is the player commit_state resolution loop; extending it to consult `form_active` at castability-check time is a targeted 3-line addition, not a rewrite.

---

### FORK F — Where does form-shift live in the atlas? (family scope + naming)

**The question.** Given all prior rulings, what does the family (or families) look like at atlas-citizen granularity?

**Options:**
- **F1 — SHAPESHIFT as one family (if A1); config axes: persistence + slot-semantics + economy.** Tradeoffs: matches Ferality+PBA sitting in one Wildsoul class chassis; loses the mechanical-grammar distinction at plane-address.
- **F2 — PERSISTENT-FORM + TEMPORAL-WINDOW as two families (if A2).** Tradeoffs: each family gets its own commit-state coordinate; matches AURA/TOTEM-SENTRY split logic; imports two-spec-doc cost.
- **F3 — PERSISTENT-FORM + TEMPORAL-WINDOW + STANCE-DANCE as three (if A3).** Tradeoffs: highest fidelity to attested; over-splits on one exhibit (D4 Druid).

**Cross-atlas composition check:** the E4 refit is currently running (per current-to-end-state 2026-07-16 §MATT'S PULL PROBE + P-PARAMETERS RULED). Form families will not admit into E4 (post-freeze); they will queue for a future edition's admission per the discovery-docket protocol. Ranked docket has SHAPESHIFT at #3 — so the family or families here become the atlas targets in the docket-3 review sitting (after MELEE-STRIKE + GAUGE/BUILDER-SPENDER complete).

**gandalf lean: F2 (two families), consistent with Fork A lean A2.** Grounds: as above. If Matt rules Fork A → A1, F1 auto-follows; if A2, F2 auto-follows; if A3, F3 auto-follows. This fork is derivative of A, restated to make the atlas-citizen count explicit as a design consequence.

**Strongest evidence:** the discovery docket already writes shapeshift as one row (rank #3) but flags "Wildsoul tri-form + Shadowhunter Demonize + druid lineage" as its exhibit set — three shapes under one label. Whether the docket-3 review sitting ratifies one or two family names is downstream of this fork's ruling.

---

## §3 — Engine-delta sketch (what Wave-A + ailment give us vs what's new)

This is DELIBERATELY not a spec section. It is an inventory sketch to inform the fork rulings by scoping what work each fork adds. All amounts are ROUGH — a proper spec would math them.

### 3.1 What EXISTS (reuse; do not rebuild)

| Engine surface | Reuse for shapeshift |
|---|---|
| `commitment_state_machine.py` — bins snap/wind-up/channel; player states idle/committing/channeling | Form-ENTRY is a WIND-UP cast (existing bin); form-SWAP is another WIND-UP cast. Zero new commit_state work. |
| `move_policy` field (rooted/walk/full_move) on skills | Form buffs may re-multiply move_policy (Fox +20% MS = form-scaled walk_pct); existing hook. |
| `active_effects` list on combatant_state | Form-BUFFS (Fox +20% MS, Bear +10% DR) can ride ActiveEffect; existing hook. |
| Wave-A proxy layer (positioned-ally spawn, proxy commit-clock, absorption ramp) | Companion-summon flavor of PBA can ride this (PBA companion spirits = proxy adjacents). Some overlap with Wave A's summon economies. |
| Ailment layer (`_add_or_refresh`, `_apply_skill_damage`, DoT tick loop, hard-control enforcement) | Form-BUFFS as ActiveEffect ride the SAME refresh law. Form-DEBUFFS (Ferality synergy -12% defense) route through sunder-adjacent damage-amp machinery. |
| GX-19 gauge economy (family docket rank #2, not yet built) | BUILD-TO-SPEND and BUILD-TO-TRIGGER entry economies (Fork D options D1/D2) DEPEND ON this family landing first. |
| `kit_architecture.Architecture` enum (single / hybrid-2 / physical-hybrid) | May need a 4th enum value for `shapeshift-multi-form` OR the enum stays and form is a compositional layer on top. Matt/rocket call. |

### 3.2 What is NEW (genuinely additive engine work)

| New primitive | Fork it depends on | Scope estimate |
|---|---|---|
| `form_active: str | None`, `form_duration_remaining_s: float | None` fields on player entity | Fork E (E1/E5) | SMALL — 2 fields + serialization. |
| `form_gate: str | list[str] | None` field on Skill schema (LOCKED-SUBSET) | Fork C (C1) | SMALL — 1 field + castability-check extension. |
| Whole-kit-swap machinery: `form_kit_index: dict[str, list[Skill]]` on player + kit-swap on form-entry | Fork C (C2) | LARGE — new state layer + interaction with cooldown-carryover semantics. |
| `form_state_machine.py` sibling to commitment_state_machine (temporal-window auto-expire) | Fork E (E4/E5) | MEDIUM — parallel to Wave-A's csm; ~100-200 LOC parity. |
| Form-definition schema (name, persistence type, entry economy, exit trigger, tag list, buff/debuff riders) | ALL forks | MEDIUM — new config surface (`config/forms.yaml`?). |
| Form-entry / form-swap / form-exit as VERB entries in `ability_grammar.py` | Fork F | SMALL — 3-5 new grammar verbs. |
| Emission: form-eligibility at kit-generation (which kits can carry form-shift; which elements bias toward it) | Fork D + F | MEDIUM — new emission surface in `element_biases.py` + `substrate_templates.py`. |
| Sim-side castability-check extension: `skill.form_gate in {None, form_active}` | Fork C | SMALL — 1 clause in the skill-selection loop. |
| Progression composition: does form-shift carry across seasonal descent? (Court-of-Forms is ascended-form persistence, semantic reservation) | Wave-2 | UNRESOLVED — Court-of-Forms uses "form" in a different sense (persistent ascended-lineage). Naming collision. |

### 3.3 Wave-A pattern reuse (the compositional discipline)

Wave-A's pattern was: minimal-new-primitives + maximum-reuse of existing seams. This docket's engine-delta preserves that discipline:
- Wave-A added ONE new state machine (proxy commit-clock) + FOUR economy config axes + ONE calibration axis.
- Shapeshift will add ONE-to-TWO state machines (form persistence + optional form_state_machine for temporal-window auto-expire) + THREE-to-FOUR economy axes + ONE-to-TWO calibration axes (form entry-cost band + form uptime band).

**Scope-comparability read:** shapeshift is Wave-A-comparable-to-larger, NOT genuinely new-order-of-magnitude. The forks are architectural (schema + state), not fundamental (no new physics primitive is needed; form is a persistent flag with skill-availability re-routing).

### 3.4 Naming collision to surface (not a fork, a flag)

`foundation/court_persistence.py` uses the noun "form" to mean an **ascended lineage record** — a persistent Earth-Self identity, NOT an in-fight body-swap state. Shapeshift's engine work will need to disambiguate:
- Either rename Court's "form" concept (Court-persisted-ascension → `AscendedIdentity` / `Vessel` / `Body`) — HIGH churn, semantic clarity gain.
- Or rename shapeshift's in-fight state (form → `stance` / `body` / `shape`) — MEDIUM churn, mechanical clarity gain.
- Or accept the collision and namespace: `form.court.*` vs `form.combat.*` — LOW churn, ongoing readability cost.

**Not a fork the docket closes.** Flagged for gandalf-prime awareness at DRIFT-CRITIC gate; Matt call at spec draft time.

---

## §4 — DL-03 conformance check (docket-level)

Shapeshift touches stream-mechanics only obliquely: form-BUFFS may ride move_policy scaling (Fox +20% MS = form-scaled walk_pct). DL-03 (streams never tax movement) is satisfied by the base engine's move_policy contract — form scaling composes cleanly with the existing rooted/walk/full_move hooks, does NOT introduce a new "movement penalty during form" mechanic.

Ailment layer's spec §2.12 pattern applied.

---

## §5 — The fork-list summary (for gandalf-prime DRIFT-CRITIC scan)

| # | Fork | Options | gandalf lean | Impact if ruled otherwise |
|---|---|---|---|---|
| A | ONE atlas family vs TWO | A1 (one) / A2 (two) / A3 (three) | **A2** | A1 collapses persistence axis to config; A3 over-splits on D4 Druid |
| B | Persistence model | B1 persistent-only / B2 temporal-only / B3 BOTH / B4 skill-driven | **B3** (conditional on A2) | B1 or B2 alone refuses shipped genre pattern |
| C | Slot-semantics | C1 locked-subset / C2 whole-kit-swap / C3 skill-driven-remap / C4 collapsed-subset / C5 amplifier | **C1+C2 pair** (persistent→C1, temporal→C2) | Shipping C1-only forces temporal-window into locked-subset (awkward); C2-only forces persistent-loop into whole-kit-swap (Ferality-style rotation impossible) |
| D | Entry economy | D1 spend / D2 trigger / D3 cooldown / D4 drain / D5 all-4 configurable | **D5, with D3 as Wave-1 slice** (defer D1/D2 behind GX-19) | D1/D2 alone requires GX-19 land first (blocking); D3 alone loses gauge-tension |
| E | commit_state coordinates | E1 new field / E2 new commit_state / E3 ActiveEffect / E4 new subsystem / E5 compositional | **E5** (WIND-UP entry + new player-state + optional form_state_machine) | E2/E3 semantically wrong; E4 alone reinvents patterns Wave-A settled |
| F | Atlas family scope (derivative of A) | F1 one / F2 two / F3 three | **F2** (auto-follows A2) | Auto-follows A ruling |

**Rulings sequence:** A first (family count); B second (persistence model); C third (slot semantics); D fourth (entry economy); E fifth (commit_state coordinates); F auto-follows A.

---

## §6 — What this docket does NOT do

- **Does NOT close any fork.** All six remain OPEN pending Matt rulings.
- **Does NOT specify implementation.** No `_try_apply_form()` function signatures; no `forms.yaml` schema draft. Those live in the spec that follows the rulings.
- **Does NOT pre-empt gandalf-prime DRIFT-CRITIC.** DRIFT-CRITIC checks the docket's fork-shape + evidence citation + engine-grounding + not-closing-forks discipline BEFORE Matt reads.
- **Does NOT touch canon.** No `canonical/` writes; no corpus.db touch; no dispatches fired.
- **Does NOT bind naming.** "SHAPESHIFT" and "PERSISTENT-FORM"/"TEMPORAL-WINDOW-FORM" are working labels for the atlas docket-3 review sitting; final family names are gandalf-prime + Matt call at ratification.

---

## Signed

gandalf sub-agent (ELICITOR role) · 2026-07-16 · atlas-parity autonomous run under Matt authorization 2026-07-16
