# FLAG — Items 7+8: label reachability finding + two HOW-latitude calls

**From:** rocket (content-generation seam)
**To:** gandalf (label taxonomy / design intent) — cc knight-rider, jack-ryan (Gate-2)
**Date:** 2026-06-12
**Context:** dispatch `2026-06-12-rocket-generation-handoff.md` §§ 7, 8 (Session 4 §§ 2, 5).
**Disposition:** rules transcribed VERBATIM; no reordering. Reachability is reported as substrate
evidence per § 2.3 rule-order note + dispatch § 8 non-negotiable. Two HOW-latitude calls recorded.
**Implementation:** `src/reincarnated/generation/vestigial_labels.py`, `investment_profile.py`
**Tests:** `tests/test_vestigial_labels.py` (28) + `tests/test_investment_profile.py` (12) — 40 pass.
**Math note:** `generation/math/session-4-items-7-8-investment-and-vestigial-labels-2026-06-12.md`

---

## Finding 1 — two taxonomy labels are STRUCTURALLY UNREACHABLE (for gandalf)

The § 2.2 taxonomy lists **18 primary labels**. The § 2.3 first-match rule set (16 rules) can emit
only a **16-label subset**. Transcribing the rules verbatim, two labels have NO rule that emits
them:

- **Berserker** (§ 2.2 signature: Axis 1 close + Axis 3B spiky + `energy_type`=rage + front-loaded).
  Rule 10 routes close + rage + front-loaded → **Ravager** first; nothing downstream re-tests for
  spiky to recover Berserker. No rule emits Berserker.
- **Conduit** (§ 2.2 signature: resource_generation focus / Resource Conduit proxy). No rule
  references resource-generation focus. No rule emits Conduit.

A third label is **rare but NOT dead**:
- **Phantom** (rule 9: dodger + single-target + shadow) is reachable ONLY for shadow kits that are
  *damage-pure* — because rule 4 (shadow + {mixed, control-pure}) captures the mixed/control-pure
  shadow kits first. So Phantom fires only on the narrow shadow + damage-pure + dodger + single-
  target intersection. Reachable; expect low corpus count.

Per the § 2.3 rule-order note + dispatch § 8 ("labels that never fire are substrate evidence, not
bugs — report unreachable labels to gandalf; do NOT reorder rules to force reachability"), I did
**not** reorder. `reachability_report()` emits both classes separately:
1. `structurally_unreachable` = {Berserker, Conduit} (no rule);
2. `empirically_unfired` = assignable labels that did not fire over the supplied corpus.

**Requested (design call, gandalf):** if Berserker / Conduit are intended to be reachable, the
RULE SET needs an authored rule (e.g. a Berserker rule BEFORE rule 10 testing close + spiky + rage +
front-loaded; a Conduit rule testing resource-generation focus). That is a WHAT change to § 2.3 —
yours to author, not a HOW call I can make. Until then both remain taxonomy-only labels and the
reachability report will continue to flag them. The empirical per-corpus report runs over the
Season 001010 corpus once a BC-measurement pass exists for it (dispatch § 8 pass/fail).

## Finding 2 — HOW-latitude call: secondary-modifier precedence (Item 8)

§ 2.2 lists 6 modifiers and says "append if applicable"; the three worked examples each show ONE
appended modifier ("Invoker Sovereign", "Warden Resonant", "Ravager Undying"). I append **at most
one**, first-match in precedence **Sovereign → Undying → Resonant → Cascading → Fissured → Twin**.
Rationale: the five T4-strategy modifiers are more identity-specific than the architecture-derived
Twin, so they take precedence — a hybrid RESONANCE_LOOP kit reads "… Resonant" (matches the "Warden
Resonant" example shape). Trivially changed to multi-append, or to a different precedence, if you
prefer — single-line edit to `_MODIFIER_PRECEDENCE`.

## Finding 3 — HOW-latitude call: kit_kind gates FIRST in investment profile (Item 7)

The § 5.2 table lists `Axis 4 = glass → HIGH` (row 1) ABOVE `Monster → LOW` (row 9). Strict table
order assigns a glass-axis monster HIGH — but monsters have no gear slots, so HIGH (a gear-power-
ratio profile) is structurally meaningless for them. The three corpora are DISJOINT (player XOR
npc/mercenary XOR monster), so I gate on `kit_kind` FIRST (monster→low; npc/mercenary→scaling;
player→§ 5.2 rows 1-7 + default). This is faithful to the Monster/NPC rows' intent and removes the
glass-monster contradiction. Flagged as a table-order clarification — if you'd rather the table be
read literally top-to-bottom for monsters too, say so and I'll drop the gate.

---

## Cross-refs
- Dispatch: `2026-06-12-rocket-generation-handoff.md` §§ 7, 8
- Spec: `gandalf/notes/2026-06-12-session-4-kit-identity-generation-spec.md` §§ 2.2, 2.3, 5.1-5.3
- Prior Items-1-6/9/11 flags: same `rocket/notes/` dir (cogload fixture; identity affinity tables)
