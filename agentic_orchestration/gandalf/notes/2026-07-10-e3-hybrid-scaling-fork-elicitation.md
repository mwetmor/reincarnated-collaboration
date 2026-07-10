# E3 — Hybrid Scaling Axis: fork elicitation (Q-E3-0 … Q-E3-6)

> **STATUS:** ELICITATION OPEN — decision-shaped forks for Matt; rulings convert this into the E3 design note (same lifecycle as E2/E4: elicitation → rulings → design note → dispatch precondition cleared).
> **Authored:** gandalf, 2026-07-10 (ELICITOR pass; all substrate claims source-verified this session).
> **Ledger row:** `canonical/current-to-end-state/surface-ledger.md` E3. **Roster stakes:** K15 / K20 / K23 + H5 birth.
> **Composition law inherited:** E2 k-conservation · E4 commitment bins + ONE versioned packet contract · Q14 ONE end-of-axis-run band re-anchor (deltas measured + REPORTED only — no per-axis re-anchor).

---

## §0 — What EXISTS (survey-mode; source-verified)

The ledger row says "the dual-scaling pattern vocabulary was stubbed, never designed." The stub is **bigger than the row implied** — and one piece of it just collided with a fresh Matt ruling:

| Substrate | State | Source |
|---|---|---|
| **Three-pattern resolver vocabulary** | EXISTS with real math: `physical_with_element_flavor` (physical path, element flavor via conversion) · `magical_with_martial_weapon` (magical path + ω if cross-attribute) · `sum_paths` (`phys×bf + magic×(1−bf)` + ω) — falls back to magical on None | `damage_resolver.py:922-974`; math note `wave-0-5-per-skill-emission-math-2026-05-27.md` §2.3 |
| **Schema fields** | `damage_scaling_type ∈ {physical, magical, hybrid}` (REQUIRED per Disc #38) + `hybrid_pattern` + `hybrid_balance_factor` — all present, all NULL population-wide | `skill_schema.py:70-83` |
| **Emitter** | `_BC_ATTRIBUTE_TO_SCALING_TYPE`: STR/DEX→physical, INT/WIS→magical; ALL skills inherit the kit's ONE `bc_attribute`; `hybrid_pattern=None` — Q-W05-R4 deferral comment at three sites | `per_skill_emitter.py:196-213, 734, 874` |
| **ω-penalty** | `OMEGA_CROSS_ATTRIBUTE_PENALTY = 0.80` flat; fires on patterns B/C when skill-attr FAMILY ≠ weapon-attr FAMILY (martial STR/DEX vs caster INT/WIS); scope-locked to B/C (gandalf verdict 2026-05-27). **Q10#3 RULED RETIRE-by-construction 2026-07-07** — tripwire: "Track D re-opening cross-attribute wielding re-opens it" | `damage_resolver.py:189-212, 687-703, 949-965`; `matt_decision_needed/` Q10 |
| **Option C census** | Exactly THREE cells carry `allow_cross_attribute=True, option_c_cross_attribute="STR"`: **K15 Red Mage/Spellsword** (melee-INT-high-flat; `__option_c__` STR-melee substrate + INT-flavored) · **K20 Holy Knight/Paladin** (melee-WIS-medium-variable) · **K23 Monk** (melee-WIS-high-variable; quarterstaff) | `bc_target_cell_sampler.py:270-277, 333-345, 375-386` |
| **Chain structure** | `chain_A` = primary, `chain_B` = secondary_attack (pivots to control/support at T3-4 in two templates), `chain_C` = support/control — role maps per template | `per_skill_emitter.py:513-563` |
| **Two-attribute sheet machinery** | `attribute_coupling: Optional[list[str]]` (e.g. `["STR","DEX"]`, populated at Layer 4) + `StatDistributionV2` = fractions over 4 attributes summing to 1.0 — **the dual-attribute funding mechanism already exists** | `bc_target_player_class.py:161-165, 315` |
| **Roster intent** | K15 row: "true dual-scaling version = H5 (E3)"; **H5 True Battlemage** = named hypothesis kit, gates-on E3 | serial tracker PART F :327, :347 |

**Stale-cite correction (this pass):** the ledger E3 row cites "Amendment 7a intends hybrids as builds, not palette swaps." No such amendment exists — the multi-dim doc's Amendment 7 is substrate-availability framing (§8.3.1), unrelated. The REAL intent anchors are: math note §4 hybrid rule ("only for explicit cross-attribute kit designs — Option C substrate cells… require specific per-skill design decision"), `skill_schema.py` doc-47 §2.2 comment, the Q-W05-R4 dispatch deferral, and the H5 roster row. Intent is unchanged and well-grounded; the cite was audit-time compression. Ledger corrected in place with marker (living-doc policy).

## §1 — The failure being fixed (player consequence)

Today K15 "Red Mage/Spellsword" is an INT mage whose range template says melee. Every skill scales INT, every skill is magical; the sword is a costume. K20 "Paladin" is a WIS mage standing close. That is the **palette-swap failure inverted** — worse than a reskin, it's a *mislabel*: the kit name promises the genre's oldest fantasy (weapon in one hand, power in the other — D2 Paladin, FF Red Mage, Grim Dawn Battlemage) and the mechanics deliver a robed caster in melee frame. A player who reads "Spellsword" and inspects the kit finds no sword anywhere in the numbers. That's a D7-adjacent honesty failure at the KIT level, and it's the exact "content-distinct, mechanics-identical" trap the axis run exists to kill.

## §2 — The forks

### Q-E3-0 — What CARRIES hybridity at v1? (scope fork)

| Option | Shape | Cost |
|---|---|---|
| **(a) Cell property** | Hybridity activates on the three Option C cells (+H5 birth). NO new catalog coordinate — **972 stands**; hybridity is pattern texture WITHIN cells, carried by the already-built `option_c_*` sampler plumbing | zero space growth; hybrid population = 4 kits |
| (b) Sampled coordinate | `bc_hybrid` axis; any cell can roll hybrid | space ×N the day after F-3 settled 972; cert bill grows again |
| (c) T4-transform-only | Hybridity enters only via capstone | Paladin isn't a paladin until endgame — identity starved for 40 levels |

**Lean (a).** The sampler has carried `option_c_cross_attribute="STR"` on exactly these three cells since 2026-05 — the generation layer was BUILT for this and never fed. (b) re-opens space bookkeeping we just closed; (c) fights the class fantasy's first-90-seconds readability.

### Q-E3-1 — Pattern vocabulary: portfolio spine or blend spine? (the load-bearing fork)

| Option | Shape |
|---|---|
| (a) Ratify the 3-pattern stub as-is | Per-skill pattern assignment from the existing enum |
| (b) Generalized blend contract | Every hybrid skill scales on weighted attribute pairs |
| **(c) PORTFOLIO hybridity** | **Chain-level attribute routing:** `chain_A` routes to the SUBSTRATE attribute (STR — weapon strikes), `chain_B` routes to the KIT attribute (INT/WIS — spells); each individual skill stays SINGLE-path. `sum_paths` reserved for 1–2 **signature** skills per hybrid kit (H5's flagship; optional T4). Patterns A/B retire as degenerate (A = physical + element flavor, already expressible; B = what every caster-in-melee is by default) |

**Lean (c).** The genre's beloved hybrids are **toolkit** hybrids, not blend hybrids: D2 Paladin = Zeal (physical) + Foh (magical); Grim Dawn Battlemage = Cadence + Devastation; D2 Monk-likes = staff strikes + mantras. Three wins:
1. **Per-skill readability** — each skill IS one thing; tooltips stay honest (D7 law); the blend continuum of (b) makes every tooltip a fraction and the fairness cert a continuum.
2. **Zero-resolver spine** — the sim already resolves per-skill `scaling_attribute` TODAY; chain-level routing is an EMITTER change. `sum_paths` (which already has resolver math) activates only for signatures. E3's build is dramatically lighter than E4's.
3. **Maps 1:1 onto existing structure** — `chain_B` is already the secondary-attack chain; it becomes the second HAND. Composes with E4's weapon-manifestation-class animation enum (sword-hand chain vs god-hand chain read differently in Godot for free).

### Q-E3-2 — The hybrid price identity: fairness-flat or breadth-priced? (the identity fork)

| Option | Shape | Genre verdict |
|---|---|---|
| (a) Zero tax | Hybrids band WITH pure kits on peak; breadth is free | Free breadth = strictly-better kits; pure kits become the trap picks |
| **(b) BREADTH-PRICED** | Hybrids trade single-target peak (magnitude **math-note-derived**, ballpark 10–15% — NOT assumed) for two-path coverage. The **counter-breadth instrument** (~24×24 matrix, Matt law 2026-07-07) VERIFIES the breadth is real: a hybrid whose measured counter-coverage is NOT wider than pure kits is mis-designed and fails cert | Grim Dawn prices dual-mastery ~15% peak for coverage — works for a decade |
| (c) Taxed-uncompensated | Split stat budget, no design compensation | D2-classic: hybrids were meme-tier for 20 years until 2.4 buffed them out of it. Named to REJECT |

**Lean (b).** Mixed-path damage means mono-resist walls can't brick you — that is REAL player value and must be priced, or hybrids dominate. And we uniquely OWN the instrument that keeps the trade honest: the counter-breadth matrix already exists as law with two customers; hybrid certification becomes its third. Same instrument-honesty philosophy as E4's measured premiums — **the price is real only if the benefit is measured, and the benefit is measurable only if the instrument can see it** (→ Q-E3-6). Funding mechanics (how `attribute_coupling` + `StatDistributionV2` fund two attributes without (c)'s starvation) = math-note scope, Disc #1.

### Q-E3-3 — ω-penalty tripwire: does E3 re-open it?

E3 makes `is_cross_attribute_wielding` LIVE from the **kit side**: a STR-chain skill on a caster-weapon kit trips the check mechanically. Q10#3's retire-by-construction assumed no cross-attribute wielding exists; E3 CREATES kit-native cross-attribute.

| Option | Shape |
|---|---|
| **(a) ω stays RETIRED for kit-native hybridity** | Option C kits' designed cross-attribute is exempt; emitter sets weapon-requirement family coherently per kit (quarterstaff is the genre's dual-family weapon for a reason). Tripwire RE-SCOPED verbatim to what Q10 meant: **gear-driven** cross-wielding (Track D re-opening) |
| (b) Tripwire fires; ω re-activates per the 2026-05-27 scope lock | Hybrids pay 0.80 on their STR chains |
| (c) ω re-derives as a measured coefficient in the E3 math note | A priced penalty instead of a flat one |

**Lean (a).** Double-pricing guard — the same anti-double-charge logic that kept damage-interrupt off wind-up at v1: Q-E3-2(b) already prices hybridity at the portfolio level; stacking a flat 0.80 on top double-taxes the same identity. And 0.80-flat is exactly the unmeasured-constant class the E4 pricing philosophy retired — if a wielding penalty is ever wanted (Track D), it gets DERIVED there, not inherited.

### Q-E3-4 — Kit slate at v1

| Option | Slate |
|---|---|
| **(a) K15 + K20 + K23 re-emit as portfolio hybrids; H5 births as the `sum_paths` flagship** | 4 kits touched |
| (b) H5 only | zero re-cert on the existing three; "Spellsword" stays a mislabel |
| (c) (a) + hybrid opens to future cell sampling | scope creep beyond the roster of record |

**Lean (a).** The post-E3/E4 population re-certifies ANYWAY (Q14's ONE re-anchor absorbs it) — this window is the zero-marginal-cost moment to make the three labels true. Coordinates don't move (Q-E3-0a: no new coordinate); K19 Channeling Cleric untouched (option_beta, WIS-pure — its E4 channel pin is its identity, not hybridity).

### Q-E3-5 — T4 path-transform: v1 or named reserve?

E4's capstone law declares `(commitment_bin, amplitude_delta)`. E3's natural analog: **`path_delta ∈ {none, convert_to_secondary}`** — a T4 that converts one chain's damage path (D2 Vengeance/Berserk; PoE Avatar of Fire — the genre's conversion crowns).

| Option | Shape |
|---|---|
| (a) IN at v1 | First conversion capstones certify now (expressed-coordinate machinery exists from E4) |
| **(b) DECLARE-now, POPULATE-later** | `path_delta` enters the packet contract v1 (schema-cheap; no contract re-version later), emits `none` everywhere at v1; first conversion capstone = named H5 follow-on |
| (c) Not in the vocabulary | Conversion re-opens the contract when it comes |

**Lean (b).** Conversion crowns are endgame chase content, not demo-critical — but the contract should never need re-versioning for a field we can already name. Same declare-then-populate shape as E4's v1.1 stagger re-entry.

### Q-E3-6 — Cert regime honesty (the E4 three-axes analog)

The breadth premium (Q-E3-2b) is measurable only if the cert matrix contains resist-textured opposition.

| Option | Shape |
|---|---|
| **(a) HARD requirement** | Hybrid cert matrix must contain ≥1 **mono-resist** regime (the D2 immunity-wall shape — where pure kits brick and hybrids shine) + ≥1 **mixed-defense** regime (where breadth buys nothing — the premium's control group) |
| (b) Reported-only at v1 | Premium calibrates against whatever regimes exist |

**Lean (a).** An instrument that can't see breadth can't price breadth — verbatim the E4 law with "risk" swapped for "coverage." Without the mono-resist regime, hybrids sim as strictly-dominated (their peak is lower, their breadth invisible) and get mis-banded — the channel-kit failure mode, re-worn. The mob-affix/bestiary resist textures are the substrate; regime presence = acceptance criterion, verified not assumed.

## §2-bis — Matt's element-layer challenge (mid-elicitation exchange, 2026-07-10)

Matt (verbatim core): *"why not house it within the elemental randomization piece of the pipeline? Simply list a low probability for two elements to appear, and decide the logic with which they appear (maybe one element per chain, or depending on T4, or hybrid kits can have multiple T4s?)… I don't think element is within BC coordinates, is it?"*

**Verified:** element is NOT a BC coordinate (BcTargetCell = range/tempo/amplitude/attribute/proxy_density + commitment) — Matt correct. **But the elemental hybridity slot ALREADY EXISTS and is the empty thing:** `secondary_element: str | None` = "chain_2 element for hybrid kits; None for mono kits" (`class_schema.py:45-56`, `season_generation_pipeline.py:410-416`; consumers: Phase-5 A/B, Phase-7 cohesion judge, LLM prompt) + `dual_element_factor = 1.0  # TODO: read from T4 DUAL_ELEMENT_ADDITION context` (`damage_resolver.py:877`). Element picks WHICH RESIST + the look; it does not pick armor-vs-resist layer, sheet stat, or gear feed — "content-distinct, mechanics-identical," the §1 emptiness verbatim. Housing E3 there re-ships the flagged failure. **The two hybridities are orthogonal layers that compose:** element = coat + resist matchup (D2 Meteorb — coverage story, one path); path = build identity (FoH/Zeal Paladin, GD Battlemage — two paths). A path-hybrid may be mono- or dual-element on top.

**Matt's MECHANISM adopted at the path layer — three lean amendments:**

1. **Q-E3-0 lean AMENDED:** carrier = `hybrid_path_probability` **sampler field** (Matt's "low probability" shape), v1 pinned **1.0 on K15/K20/K23 + H5, 0.0 elsewhere** — degenerate values, end-state shape; the wild-roll dial exists from birth, turnable later without schema change. Still NO new coordinate; 972 stands.
2. **Q-E3-1(c) independently re-derived by Matt:** "one element per chain" IS the portfolio logic with attribute in the element slot — chain_A weapon-hand / chain_B caster-hand. Convergent derivation from the element side; lean strengthened.
3. **Q-E3-5 lean AMENDED — per-HAND T4 crowns:** kits already emit tiers 1–4 PER CHAIN (`per_skill_emitter.py:513-563`), so "hybrid kits have multiple T4s" is already structurally true; the amendment is that each chain's T4 crown be **path-native** (STR-hand physical crown / caster-hand magical crown), and `path_delta` (5b) + the elemental `DUAL_ELEMENT_ADDITION` T4 stub are siblings in one T4-transform vocabulary.

## §3 — Composition constraints (inherited, not forks)

1. **E2 k-conservation:** k scales `(per_hit, cooldown, cost)` per-skill. Under the portfolio spine each skill is single-path — k composes UNCHANGED. For `sum_paths` signatures: whether k applies per-path-pre-blend or post-blend is a **math-note item** (conservation must hold either way; flag, not fork).
2. **E4 commitment:** path and commitment are ORTHOGONAL coordinates at v1 — no new coupling rows (a STR-chain skill may be any commitment bin the existing table allows). Chain-level flavor pairings (smites lean wind-up, prayers lean channel) are EMERGENT sampler texture, not law.
3. **Q14:** E3 deltas measured + REPORTED only; the ONE end-of-axis-run re-anchor absorbs (same §3.12 law as E4).
4. **Space:** under Q-E3-0(a), catalog stays **972 / 25–31 live** — E3 adds NO coordinate. Composes with the F-3 ADOPT+DEFER settlement.
5. **Packet contract:** per-skill `scaling_attribute` + `damage_scaling_type` + `hybrid_pattern` + `hybrid_balance_factor` (+ `path_delta` under Q-E3-5b) ride the SAME versioned contract — sim, Godot, loadout read identical fields (tooltip says physical because the resolver ran physical — the one-contract law verbatim).

## §4 — Build-shape forecast (for KR sequencing; not a fork)

Under leans (0a · 1c · 2b · 3a · 4a · 5b · 6a): E3's build is **rocket-heavy, gamora-light** — chain-level attribute routing + `attribute_coupling` population + pattern/signature emission are emitter-side; resolver needs only signature-path audit + the ω exemption disposition + cert-regime composition. Likely a LIGHTER dispatch than the E4 pair, on the same two seams. Sequencing vs the in-flight E4 pair = KR's call (the gamora-seam serialization rule applies identically).

## §5 — After rulings

Rulings → E3 design note (same-session) → ledger E3 flips ✓ ruled (build queued) → KR drafts the dispatch → H5 births at build-landing → bench-promotion elicitation UNBLOCKS (it queues post-E3-*design*).

---

**Sign-off:** gandalf, 2026-07-10. Anchors: `damage_resolver.py` §hybrid + ω · `per_skill_emitter.py` scaling tables · `bc_target_cell_sampler.py` Option C census · `bc_target_player_class.py` Layer-4 coupling · math note 2026-05-27 §2.3/§4 · Q10#3 + counter-breadth rulings 2026-07-07 · E2/E4 design notes + addendum. *A Spellsword whose sword is a costume is a promise the numbers break — the forks above decide what the promise costs instead.*
