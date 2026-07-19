# VDM-1 STAGE-5 — BLIND RE-PROJECTION RIDER (steward → legolas)

**Author:** gandalf (steward) · 2026-07-18 · **For:** legolas (Mode A, analytical) · **Model:** sonnet · **Background**
**Op:** the run's FINAL QA gate. Independently re-judge ~10% of the 574 mapped kits **BLIND** on the three judgment-grade axes (element · ailments · grade), so the steward can measure mapper reliability (inter-rater agreement) and detect any *systematic* bias before THE REVIEW BOOK.

---

## Why this exists (read first)

The 574 VDM-1 mappings were authored by one mapper population. A mapping is only trustworthy if a *second, independent* judgment — that never saw the first — lands in the same place. **Your independence IS the measurement.** If you agree with the hidden original, that kit's judgment is corroborated. If you diverge, you surface a candidate error (in *either* direction). The steward already caught one real miss this way at audit (a silenced element that the dossier plainly attested); this rider is that check, run at scale.

**HARD BLINDNESS RULES — violating any one voids the measurement:**
- Read ONLY your assigned wave input file (`blind-input-wave{A|B|C}.jsonl`) + this spec.
- Do **NOT** read anything under `research/vdm1/stage2/` (the original mappings live there).
- Do **NOT** open `corpus.db` / query `kit_mapping` / grep for prior grades.
- Do **NOT** read the other waves' files.
- You MAY consult `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` (the main crosswalk law) if a rule below is ambiguous — that is the RUBRIC, not the answers.
- Judge each kit **fresh from its dossier + verify anchors.** Do not try to reconstruct what a prior mapper decided.

---

## Input row shape (your wave file)

`{"kit_id","game","folk_name","core_skills","mech_note","dossier":[{"family","payload","anchor"}…],"verify_anchors":[{"claim_family","anchor"}…]}`

The dossier `payload`/`anchor` + `verify_anchors` are your admissible evidence stores. `mech_note`/`folk_name`/`core_skills` give identity context. **There is deliberately no element, no grade, no mapping — that is what you are re-deriving.**

---

## THE LAWS (self-contained — apply exactly)

### L1 — the 7 engine element families
`fire · water · wind · earth · lightning · holy · shadow`. **water** carries cold/ice/frost. Crosswalks: **vitality/life-drain → shadow**; **arcane / dark / bone / necrotic / chaos → shadow**; **holy / sacred / light → holy**; **aether → lightning-or-shadow (judge by prose)**; **earth(poison) is SANCTIONED** — a poison-DAMAGE kit maps to `earth`. **ONLY physical / pierce are no-family** (null element).

### L2 — the D4 NAME-ONLY LAW (the highest-risk axis)
Element is **ATTESTED** only when an admissible store applies an element word **as a damage-type descriptor to a generic effect noun** ("deals *lightning* damage", "a *fire* nova") **OR as an enemy-directed behavior verb** ("*chills* enemies", "*ignites* the target"). Element is **NOT** attested when the element word appears **SOLELY inside a proper skill / rune / gem / item / kit NAME** (e.g. a skill called "Lightning Vortex", a kit id containing "lightning"). **`element` = null (silent) is the DEFAULT.** Descriptor-prose attests; a name alone never does. Do not over-silence (if the dossier prose carries a real damage-type descriptor, ATTEST it even if it "feels" flavor) and do not over-attest (a name/flavor word alone stays silent).

### L3 — the 16-CLOSED ailment registry
`burn · chill · root · knockback · bleed · shock · consecrate · drain · sunder · freeze · stun · poison · blind · curse{amplify,weaken,decrepify,sap} · fear · execute`. Attest an ailment ONLY from explicit status/CC/debuff prose in an admissible store — **never infer an ailment from element presence** (lightning does NOT imply shock; cold does NOT imply freeze unless the text states the status). `shock` = the engine's paralyze/stun-lock status (needs paralysis prose), not "electricity". Map debuff prose by MECHANISM: "-move speed"→`chill`; "-attack power"→`curse:weaken`; damage-taken-amplify→`curse:amplify`; "-armor/-resist"→`curse:sap`/`sunder`.

### L4 — PHYSICAL RULE
physical / pierce kits carry NO element family (null). They may still carry ailment-substrate (bleed / stun / poison-venom) if the text attests it. A physical kit's element_set is `[]`.

### L5 — §B5 ROGUELITE genre law (games: vs, hades1, hades2, hot, mcd)
- **Vampire Survivors (vs):** flavor-silent — attest element ONLY on an explicit enemy-directed status; the one sanctioned case is enemy **freeze**. Otherwise element_set `[]`.
- **Halls of Torment (hot):** real damage types — MAP them (fire/lightning/water + burn/freeze where prose attests).
- **Hades 1/2 (hades1/hades2):** boons are typed (e.g. Zeus → lightning) so element MAY attest, BUT the loadout/boon-rotation identity has no engine rotation primitive → such kits are usually **GAPPED** on identity even when an element attests.
- **Minecraft Dungeons (mcd):** enchantment-build identity, typically element-silent; capstone/mastery families structurally absent (that is correct, not a failure).

### L6 — GRADE rubric (+ R-M7)
Judge how faithfully the engine substrate could reproduce this kit's load-bearing identity + mechanics:
- **EXACT** — reproduces with no material deviation.
- **CLOSE** — reproduces with a MINOR, documentable deviation; identity intact.
- **APPROX** — reproduces in spirit but a MATERIAL mechanic/identity bends.
- **GAPPED** — a **load-bearing** mechanic has NO engine primitive → docket.
**GAPPED triggers:** summoner / pet-army / minion-core identity (summoner is Phase-5 **DEFERRED** — no summon primitive); a loadout/boon-rotation *as the whole identity* with no castable rotation (Hades); any core mechanic outside the 7-element / 16-ailment / geometry palette. **R-M7 (STRICT biconditional):** `grade==GAPPED  ⟺  terminal_state=="MAPPED_DOCKET"`; all of EXACT/CLOSE/APPROX → `terminal_state=="MAPPED"`.

---

## YOUR TASK — per kit, produce a kit-level BLIND judgment

For every kit in your wave, read the dossier + verify anchors, apply L1–L6, and emit ONE row:

`{"kit_id","element_set":[…],"ailment_set":[…],"grade":"EXACT|CLOSE|APPROX|GAPPED","terminal_state":"MAPPED|MAPPED_DOCKET","rationale":"<=25 words citing the deciding anchor"}`

- **`element_set`** = the set of engine families you attest across the kit's skills (deduped), e.g. `["lightning"]`, `["fire","water"]`, or `[]` for element-silent. Use L1 family names ONLY.
- **`ailment_set`** = the set of 16-closed ailments you attest, e.g. `["freeze"]`, `["bleed","stun"]`, `[]`. Use `curse:amplify` style for curse sub-types.
- **`grade`** + **`terminal_state`** per L6 (respect R-M7).
- **`rationale`** ≤25 words, naming the anchor phrase that decided element/grade. If you attest an element, quote the descriptor. If silent, say why (name-only / physical / roguelite-flavor).

Write your rows to `agentic_orchestration/research/vdm1/stage5/blind-output-wave{A|B|C}.jsonl` (match your input wave letter). **Commit pathspec-only** (your output file only). **Do NOT push.**

---

## RETURN (≤200 words, in your task result — not a file dump)

- kits judged (must equal your wave's input row count);
- your grade histogram (E/C/A/G) + element-attestation count (how many kits got a non-empty element_set) + ailment-attestation count;
- any kit where you were genuinely torn (name it + the fork) — these are the highest-value rows for the steward diff;
- confirm the blindness rules held (no stage2 read, no DB, no other wave).

**Signed:** gandalf (steward) · Stage-5 blind rider · 61 kits / 3 waves · inter-rater reliability gate before THE REVIEW BOOK.
