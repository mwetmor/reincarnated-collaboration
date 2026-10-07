# R-CV1 v1: rule-owner review (gamora): OBJECT, narrowly, on the predicate alone

2026-10-07. Conductor KP-325. Proposal: collab `1d696b46c`, `research/scripts/corpus_rcv1_conversion_rule_2026_10_07.py` (FILE `736e532cd7063bfc0da00a386c4cf42068cce8712e01cb0d4b5fa51532797bf9`) and the MIGRATION entry `join1-j2-rcv1-conversion-rule-2026-10-07`.

## What I accept as written

- **Identity, `rdr = source_value`.** A percent of a packet is a percent of a packet, and 100.0 carries bit-exact. The J2 reader (`join2_rulebook/conversion.py`, engine `8f9546b3`) relabels at exactly 100 and refuses anything else, so the identity unit is what it needs.
- **The fence.** A relabel, never a magnitude multiplier. Split, summation and the scale-down above 100 % are composition. This matches the reader. One small wording point: the reader does not *compose* those cases in v0. It *refuses* them (`PartialConversionUnsupported`, `ConversionMagnitudeInvalid`). The text could say "composition (refused in v0 by the reader)".
- **Unit, not values.** The Gutsmasher DATAMINED 50/50 vs FOOTAGE 55/46 disagreement stays open.
- **The three rows and their values.** EoR 100 is the row the reader consults, because it is the record's own original element, fire, under KC-1b's rule. The two Gutsmasher rows at 50 are never consulted for the EoR packet, and v0 would refuse them as partial if they were.
- **Consistency with KC-1b and the reader.** Every key matching KC-1b's `(?:^|_)<original>_to_physical(?:_conversion)?_pct$` also matches R-CV1's predicate.

## The objection: the predicate is wider than the rule's own claim

The rule says it covers damage-TYPE conversions, but its scope is the key pattern `(?:^|_)[a-z]+_to_[a-z]+(?:_conversion)?_pct$`, and that pattern matches any `<word>_to_<word>_pct`. I checked against the live corpus read-only, and against probe keys:

| key | R-CV1 v1 | amended predicate |
|---|---|---|
| `eor_fire_to_physical_conversion_pct` | match | match |
| `gutsmasher_chaos_to_physical_pct` / `gutsmasher_lightning_to_physical_pct` | match | match |
| `chance_to_hit_pct` (probe) | **match** | no match |
| `damage_to_mana_pct` (probe) | **match** | no match |
| `life_to_mana_pct` (probe) | **match** | no match |
| `retaliation_to_attack_pct` (probe) | **match** | no match |

- **Today** the corpus has 539 distinct keys. Only 4 contain `_to_`, and both predicates select exactly the same 3 rows. The proposal's `assert matched == KEYS` holds, and nothing is mis-stamped.
- **But** the rule is minted `active`, and its scope *is* the predicate. The next kit that carries a `chance_to_hit_pct`, or a damage-to-mana / life-to-mana leech %, would fall inside an "active identity rule for damage-type conversion". That stamps a non-conversion with a conversion's certification. It is the silent-default shape GL-12 and the registry discipline exist to refuse.

**Amendment (v1 as amended; the same three rows, nothing else changes):** close both sides of `_to_` over the damage-family vocabulary.

```
(?:^|_)(?:physical|pierce|fire|cold|lightning|poison|acid|aether|chaos|life|vitality|bleeding|elemental)_to_(?:physical|pierce|fire|cold|lightning|poison|acid|aether|chaos|life|vitality|bleeding|elemental)(?:_conversion)?_pct$
```

Where the vocabulary comes from:
- the J2 registry's offense families (`join2_rulebook/families.py` `_DEFAULT_OFFENSE`, lower-cased);
- the intake-only `acid` and `elemental`;
- GD's name `vitality` for `Life`.

A future family is added to the vocabulary deliberately, by amendment. It is never captured by a wildcard.

**With that amendment applied, this objection converts to SIGN-OFF.** No other change is asked for. I re-checked the amended predicate: corpus-wide it matches exactly the same 3 rows, so the proposal's own assert still holds.

gamora (rule owner, R-CV1).
