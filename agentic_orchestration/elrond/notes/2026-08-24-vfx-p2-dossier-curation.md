# VFX P2 — reference-dossier curation (elrond, 2026-08-24)

**Run:** VFX ARCHETYPE-BINDING RUN, phase **P2 tail** · charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` · ledger **L-14 / L-15 / L-18 / L-19 / L-24**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executed by:** elrond (data steward), named sub-agent
**Migration record:** `../../research/curated/MIGRATION-vfx-p2-dossier-curation-2026-08-24.md` — schema rationale, method, backups, reversibility, downstream queries
**Script:** `../../research/scripts/vfx_p2_dossier_curation_2026_08_24.py`
**DB:** `../../research/curated/corpus.db` (schema stamp `vfx-p2-dossier-curation-2026-08-24/P2`)

---

## 1 · Verdict

**PASS.** 26/26 dossiers curated. **114 candidate rows** (113 parsed + 1 Matt-contributed incumbent),
**26 dossier rows**, **25 finding rows** — 6 WARN / 19 INFO / **0 UNRESOLVED**.

Every dossier met the charter § 4 P2 floor of ≥3 candidates (range 3–6, median 4). Every filename
resolved to a `vfx_archetype` row. Every hard-required field was present on every candidate. Every
dossier candidate's temporal-coverage flags parsed against the chartered grammar. Zero malformed URLs
across 113 primary and 109 secondary URL fields. `integrity_check = ok`, `foreign_key_check = 0`.

**The clean verdict is a measurement, not an assurance.** A negative-control run against a temp copy of
the pre-state DB with nine deliberately injected defects fired all nine detectors and produced 4 FK
violations — versus 0 on the real corpus. Instrumentation confirmed live before the result was
reported (G-S5).

---

## 2 · Per-dossier conformance

`joins` = archetype_id resolves in `vfx_archetype` · `≥3` = charter floor met · `flc` = candidates with
full windup+active+impact coverage · `log` = search-log entries.

| archetype | tier | cands | flc | log | joins | ≥3 | verdict | findings |
|---|---|---:|---:|---:|:-:|:-:|---|---:|
| ground_targeted_circle | T1 | 3 | 3 | 5 | ✓ | ✓ | CONFORMING | 0 |
| melee_strike | T1 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING | 0 |
| self_buff | T1 | 4 | **0** | 5 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| totem | T1 | 3 | 3 | 5 | ✓ | ✓ | CONFORMING | 0 |
| single_target | T1 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING | 0 |
| melee_arc | T1 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| aura | T1 | 5 | **0** | 6 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| multi_projectile | T1 | 5 | 5 | 6 | ✓ | ✓ | CONFORMING | 0 |
| line | T1 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING | 0 |
| ring | T1 | 4 | 3 | 6 | ✓ | ✓ | CONFORMING | 0 |
| circle | T2 | 5 | 4 | 7 | ✓ | ✓ | CONFORMING | 0 |
| whirlwind | T2 | 4 | 2 | 6 | ✓ | ✓ | CONFORMING | 0 |
| dash_attack | T2 | 6 | 6 | 6 | ✓ | ✓ | CONFORMING | 0 |
| ground_slam | T2 | 5 | 5 | 6 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| beam_channel | T2 | 5 | 5 | 5 | ✓ | ✓ | CONFORMING | 0 |
| blink | T3 | 5 | 2 | 5 | ✓ | ✓ | CONFORMING | 0 |
| cone | T3 | 4 | 4 | 5 | ✓ | ✓ | CONFORMING | 0 |
| orbit | T3 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING | 0 |
| chain | T3 | 4 | 3 | 6 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| vortex_pull | T3 | 5 | 5 | 6 | ✓ | ✓ | CONFORMING | 0 |
| placed_lane | T3 | 4 | 4 | 7 | ✓ | ✓ | CONFORMING | 0 |
| ricochet_bounce | T3 | 4 | 4 | 5 | ✓ | ✓ | CONFORMING | 0 |
| leap_strike | T3 | 4 | 4 | 6 | ✓ | ✓ | CONFORMING-WITH-FINDING | 1 |
| teleport | T3 | 4 | 3 | 6 | ✓ | ✓ | CONFORMING | 0 |
| fork | T3 | 5 | 5 | 6 | ✓ | ✓ | CONFORMING | 0 |
| defensive_dash | T4 | 5 | **0** | 6 | ✓ | ✓ | CONFORMING | 0 |
| **`knockback`** | T4 | **—** | — | — | — | — | **NO DOSSIER** — expected, F-3 held (L-14) | INFO |

All six `CONFORMING-WITH-FINDING` verdicts rest on a single INFO-severity finding each (a missing
`secondary_urls`, or a `gif` rather than video). **No dossier carries a structural defect.**

---

## 3 · Coverage statistics (P3 input)

| phase | documented | of 113 |
|---|---:|---:|
| active | 113 | **100.0%** |
| impact | 110 | 97.3% |
| windup | 91 | 80.5% |
| **full lifecycle** | **90** | **79.6%** |

**23 of 26 archetypes carry ≥1 full-lifecycle video candidate.** The three that do not — `aura`,
`self_buff`, `defensive_dash` — are not under-researched. `aura` and `self_buff` are exactly the two
archetypes P1 recorded with `motion_signature_attested = NULL` ("none attested — no path signature"): a
persistent no-path effect has no windup to film in the sense a projectile does. The gap is coherent
with the vote rather than contradicting it. `defensive_dash` is the T4 singleton-tier archetype (4
skills). **P3 should expect this rather than read it as a lane shortfall.**

Windup is the scarce phase corpus-wide — and it is the phase telegraph literacy (charter § 3.6) leans
on hardest.

---

## 4 · Findings

| kind | sev | n | note |
|---|---|---:|---|
| `cross-archetype-primary-reuse` | WARN | 6 | **The material finding — § 5.** |
| `cross-archetype-url-reuse` | INFO | 11 | Shared as *secondary* across two archetypes. |
| `no-secondary-urls` | INFO | 4 | `aura#2`, `chain#4`, `ground_slam#5`, `self_buff#4` — single-source. |
| `non-video-media` | INFO | 2 | `leap_strike#3`, `melee_arc#2` are `gif`. Retained; P3 weighs, curation does not drop. |
| `archetype-uncovered` | INFO | 1 | `knockback` — expected per F-3 / L-14. |
| `incumbent-coverage-unrated` | INFO | 1 | § 6. |

**Zero UNRESOLVED.** No missing field, unparseable flag, malformed URL, duplicate rank, join failure or
manifest gap anywhere in the corpus. The manifest's 26 requested archetypes and the 26 dossiers on disk
are the same set.

**Source-game distribution (114 rows):** Path of Exile 61 · Grim Dawn 15 · Diablo III 10 · Last Epoch 9
· Diablo II: Resurrected 6 · Diablo IV 4 · Lost Ark 3 · Diablo III: Reaper of Souls 1 · Diablo IV
(Season 14) 1 *(incumbent)* · Hades, Hades II, Path of Exile 2, Torchlight: Infinite 1 each.

**PoE is 53.5% of the corpus** — the chartered hunt order working as designed (PoE's MTX model is why
it is the only ARPG publishing first-party per-effect showcase video systematically), but a
**style-register concentration risk** for P3: the binding spec would otherwise inherit PoE's visual
register by sampling accident rather than by decision. Routed as C-1, not treated as a defect. Game
strings are preserved verbatim — the D3/RoS and D4/S14 distinctions are real provenance, not noise.

---

## 5 · Material finding — independent cross-archetype convergence

The Codex lane ran 26 serialized jobs with **zero cross-job context** (each saw only its own
`researcher_gloss`). Independent convergence on the same source material is therefore signal, not a
copy-paste artifact.

| pair | shared primaries | distinct shared sources |
|---|---:|---:|
| **`blink` ↔ `teleport`** | **2** | **4** |
| **`circle` ↔ `ring`** | 1 | **3** |
| `cone` ↔ `ground_slam` | 1 | 2 |
| `aura` ↔ `circle` | 1 | 2 |
| `line` ↔ `vortex_pull` | 1 | 1 |
| `line` ↔ `single_target` | 0 | 2 |

`circle` ↔ `ring` is **the pair P1 pre-registered**: L-10 banked falsifier **F-a** as PENDING-P3 with
"`circle`/`ring` likeliest". An independent lane reaching for the same material for both is a datum
for F-a arriving from a direction the vote did not construct.

`blink` ↔ `teleport` was **not** pre-registered and is the stronger signal — twice the primary overlap,
four distinct shared sources (incl. Shadow Strike and the Lightning Warp effect). Filed as candidate
falsifier **F-e** for P3's register.

**Held as hypothesis, with its falsifier named.** Shared reference ≠ archetypes must merge; Shadow
Strike and Lightning Warp arguably instantiate both mechanics, so the convergence may say "these are
boundary-case skills" rather than "these are one archetype." **Falsifier:** if P3 lands *different*
canonical references for `blink` and `teleport` on readability/parameterizability grounds without
strain, the convergence was researcher sampling. If P3 cannot distinguish them without inventing a
criterion, F-a/F-e fire. Curation records that the question is now empirical; it does not answer it.

---

## 6 · The Matt-contributed incumbent (L-18 / L-19)

Curated as `whirlwind` / `candidate_rank = 0` / `provenance = 'matt-incumbent'` /
`validation_status = 'VALIDATED-INCUMBENT'` / `dossier_path = NULL`, source attributed to Matt's live
word 2026-08-23 with conductor oEmbed verification. Rank 0 means *contributed out-of-band* — no
position in any dossier's ordering. `validation_status` is a column distinct from `provenance` so that
"who contributed this" and "has this been validated in the field" are never conflated.

Matt's two confounds carried **verbatim** into `readability_notes`: (i) added cyclones/tornadoes are
Dust-Devil-era BUILD modifications, not base-skill VFX; (ii) cosmetic wings occlude VFX readability.

**Coverage flags left NULL — a deliberate refusal, filed as a finding.** The reference was contributed
as a working referent, not phase-rated by the lane. Curation does not invent flags to make a row look
complete. P3 rates it or knowingly leaves it unrated.

**L-19's companion-clip question is answered: YES.** `whirlwind#1` is Diablo IV Whirlwind via official
Blizzard VFX material, `windup=Y; active=Y; impact=Y`, readability notes recording restrained dust and
blade highlights preserving the rotating silhouette. It carries **neither** confound — no Dust-Devil
build modification, no cosmetic wing occlusion — while remaining the same game and the same base skill.
Incumbent (owner-validated, confounded) + `whirlwind#1` (clean baseline, full lifecycle) **compose
exactly as L-19 anticipated.**

---

## 7 · Boundaries honoured

No schema change to any P0-a/P1 table (additive DDL only, three new tables). Dossiers read **read-only
and byte-unmodified** — `vfx_reference_dossier.dossier_md5` pins the exact input text read, so any
later edit is detectable rather than silent. **Nothing was fixed:** a malformed dossier would have been
curated-with-finding, never repaired; none required it, and the discipline is what makes § 1's verdict
a measurement. No engine store read or written; ADR-004 unaffected.

**Routed onward (C-1..C-5 in MIGRATION § 6):** PoE style-register concentration (P3/P4) · windup
scarcity + the three coherent zero-full-lifecycle archetypes (P3) · `blink`↔`teleport` candidate
falsifier F-e (P3 register) · incumbent unrated coverage (P3) · `knockback` zero-corpus, standing with
F-3.
