# Dispatch — jack-ryan: Engineering Discipline #20 — Respect robots.txt + explicit Claude-agent directives

**Date:** 2026-05-22 (overnight)
**Author:** knight-rider (overnight cascade per Matt 2026-05-22 evening authorization)
**Recipient:** jack-ryan (process steward; engineering-disciplines author)
**Authority:** Matt 2026-05-22 explicit overnight-fire-cascade approval for Track D
**Priority:** HIGH — load-bearing for the weapon-library-import workstream NOT making the same mistake the Meshy probe surfaced
**Estimated effort:** 1-2 hours (single discipline entry; mirror the Discipline #19 ratification pattern)
**Status:** PROPOSED — Discipline #19 used the same pattern (jack-ryan drafts; Matt ratifies); mark this entry PROPOSED on first commit; await Matt ratification

---

## 0. TL;DR

Author a new entry in `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — **Discipline #20: Respect robots.txt + explicit Claude-agent directives**.

The pattern is grounded in two empirical instances during the weapon-library-import workstream tonight (2026-05-22 evening):

1. **First instance (gandalf 2026-05-22 evening — Meshy discover-page probe):** legolas commissioned to probe Meshy `/discover` page crawl feasibility. The probe executed multiple HTTP fetches across robots.txt, ToS, AUP, sitemap, and individual model pages. AFTER the probe completed, the probe writeup surfaced that `robots.txt` contains `User-agent: ClaudeBot / Disallow: /` and `User-agent: anthropic-ai / Disallow: /`. The probe HAD ALREADY VIOLATED the directive by the time the directive was discovered. The lesson: robots.txt verification was scheduled as a finding to surface, not as a P0 gate before the first fetch. See `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/meshy-discover-page-probe.md`.

2. **Second instance (knight-rider 2026-05-22 overnight — per-source robots verification):** when knight-rider opened the weapon-library-import workstream, the FIRST action was per-source robots.txt verification across ~25 candidate sources. Result: ~40% of candidate sources had explicit ClaudeBot Disallow directives (poewiki.net, OSRS wiki, warcraft.wiki.gg, Smithsonian si.edu, Met Museum, IMFDB, monsterhunter.wiki.gg). The discipline of probing FIRST surfaced these as blocked before any dispatch fired. Without this discipline, the same pattern would have repeated at scale — a 30K-entry crawl across ~25 sources would have hit explicit-block sources before discovering the block.

The compound risk: at scale, the cost of not respecting these directives is not just ethical/policy — it is **operationally catastrophic** because (a) crawled output from a blocked source may itself be invalid for downstream use; (b) the block signals a publisher's explicit non-consent for AI consumption, which has reputational and potentially legal implications for the project; (c) repeated violations could result in IP-level blocking from Anthropic's infrastructure or upstream provider escalations.

This dispatch frames the discipline; jack-ryan authors the canonical entry. **Mark as PROPOSED on first commit, pending Matt ratification — mirror the Discipline #19 pattern exactly.**

---

## 1. The discipline (proposed draft)

> **Discipline #20 — Respect robots.txt + explicit Claude-agent directives.**
>
> **Statement:** For every external source touched by automated work — research crawls, library imports, asset enumeration, content scraping, ANY automated HTTP traffic — perform a robots.txt probe as a **P0 step BEFORE the first content fetch**. If `User-agent: ClaudeBot` or `User-agent: anthropic-ai` is `Disallow`-listed (full-site or path-specific), the source routes to non-Claude implementation OR is skipped entirely. The explicit machine-readable directive is binding regardless of whether the technical access is possible. Discovery of the directive AFTER fetches have executed is a discipline violation, not just a documentation update.
>
> **Practical rules:**
>
> 1. **P0 probe is the FIRST action.** Before any content fetch from a new source domain, fetch the source's `robots.txt`. Verify the User-agent stanzas for `ClaudeBot`, `anthropic-ai`, `Claude-SearchBot`. Also check the default `User-agent: *` stanza for the specific paths the work intends to touch.
>
> 2. **Disposition rubric:**
>    - `User-agent: ClaudeBot / Disallow: /` (site-wide) → **RED**. Drop the source from Claude-agent scope. Route to non-Claude implementation only if Matt explicitly authorizes; otherwise skip.
>    - `User-agent: ClaudeBot / Disallow: <specific-path>` → **AMBER**. Restrict scope to allowed paths only; do not touch disallowed paths.
>    - `User-agent: ClaudeBot` absent + `User-agent: *` permits target paths → **GREEN**. Proceed with research-appropriate User-Agent string + crawl-delay honored.
>    - `User-agent: anthropic-ai` Disallow (even if ClaudeBot is absent) → **RED** (treat as equivalent to ClaudeBot per the spirit of the directive).
>    - Content-Signal headers indicating `ai-train=no` or similar → **AMBER**. Read-only research-research consumption may be acceptable per the source's terms; do not treat as training data; honor per-source nuance.
>
> 3. **No fetch before disposition.** The robots.txt probe is itself a content fetch — but it is the ONE allowed pre-disposition fetch (analogous to how a TCP handshake precedes data exchange). All other content fetches MUST be gated on a verified GREEN or AMBER-with-scope disposition.
>
> 4. **Record disposition in a probe log.** Per-source robots.txt verification results MUST be captured in a probe-log artifact (e.g., `agentic_orchestration/logs/<date>-<workstream>-robots-verification.md`). The log is the cross-session continuity artifact — future workstreams touching the same source consult the log before re-probing.
>
> 5. **Re-verify periodically.** robots.txt is mutable. For long-lived workstreams or recurring crawls, re-verify the probe at meaningful intervals (typically: at the start of each new dispatch firing against a source previously verified more than 7 days ago).
>
> 6. **Honor Crawl-delay.** Where `Crawl-delay: N` is specified in the matched User-Agent stanza, honor it precisely. This is a separate constraint from the Allow/Disallow check.
>
> 7. **Respect ToS + AUP alongside robots.txt.** robots.txt is the machine-readable signal; ToS and AUP are the human-readable signals. Both bind. Per-source ToS review is required for any commercial-product use case; flag to Matt if ambiguous.
>
> 8. **Self-policing reflex.** Before any HTTP fetch beyond robots.txt itself, the orchestrator checks: has the robots.txt been probed for this source in the current workstream? If no, probe first.
>
> **What this discipline does NOT regulate:**
>
> - Authenticated API access where the API publisher explicitly documents agent compatibility (e.g., Wikidata SPARQL endpoint, Sketchfab Data API v3, Smithsonian Open Access via api.data.gov). These are scoped by their own API documentation and ToS, not by robots.txt; the discipline applies to the robots.txt of the API documentation domain itself but not to the API endpoint's request flow.
> - Static-resource downloads from a publisher who explicitly distributes that resource for the use case (e.g., Wikimedia dumps from `dumps.wikimedia.org`, Kenney CC0 ZIP packs). These are not "crawl" traffic in the robots.txt sense.
> - Single-page fetches by Matt-the-human or Matt-the-developer-using-a-browser; the discipline applies to automated agent-driven fetches, not interactive human browsing.

---

## 2. Why this is load-bearing for the weapon-library-import workstream specifically

The weapon-library-import workstream is the largest single-workstream HTTP traffic generator in the project's history. Without Discipline #20:

- ~25 candidate sources would each be probed-by-default-then-cease-on-block — but the cease-on-block decision would only fire AFTER fetches had executed against the blocked source
- ~40% of candidate sources turned out to be RED tonight — that's ~10 of 25 sources where uncontrolled fetching would have generated Claude-agent traffic against an explicit opt-out
- The Meshy probe tonight is empirical proof: the probe writeup surfaced the block AFTER the fetches; same pattern would have repeated 10× at scale

The pattern is also generalizable beyond this workstream — any future research scout or external-source dispatch (legolas crawls; rocket pulling reference docs; galadriel pulling visual references from external archives) operates under the same risk surface.

---

## 3. Empirical anchors (jack-ryan references these in the canonical entry)

| Reference | What it shows |
|---|---|
| `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/meshy-discover-page-probe.md` | First empirical instance: robots.txt block surfaced AFTER fetches executed |
| `agentic_orchestration/logs/2026-05-22-evening-robots-verification.md` | Second empirical instance: P0-probe-first discipline applied across 25 sources; ~40% RED disposition |
| `agentic_orchestration/skill_handoff_2026-05-22-evening.md` § 1.5 + gandalf's pattern-6 amendment commentary | Gandalf's recognition of the systematic vestigial-pattern that this discipline complements at the empirical-access layer |
| Discipline #19 (RATIFIED 2026-05-22) | Mirror pattern: PROPOSED → Matt ratifies → header marker removed |
| Discipline #2 (smoke-test vs full-regen) | Cross-reference: "right tool for the question" — robots.txt probe IS the smoke test for new-source viability |
| Discipline #11 (empirical inspection over assumption) | Cross-reference: do not assume a source is accessible based on legolas's prior research; probe directly |

---

## 4. Mark as PROPOSED — Discipline #19 ratification pattern

Per the established pattern that produced Discipline #19:

1. **First commit:** jack-ryan authors the discipline entry with a header marker `**[PROPOSED — pending Matt ratification]**` at the top of the entry
2. **Matt review:** at session-return, Matt reads, may amend, ratifies via decisions-log entry
3. **Second commit:** jack-ryan removes the PROPOSED header; references the decisions-log ratification entry in the cross-references list

DO NOT remove the PROPOSED marker on the first authoring commit. Matt's ratification is the trigger for that.

---

## 5. Acceptance criteria

| # | Criterion |
|---|---|
| 1 | New entry `### 20. Respect robots.txt + explicit Claude-agent directives` added in numerical sequence after Discipline #19 |
| 2 | Statement paragraph captures the canonical rule (per § 1 above; jack-ryan may tighten the wording) |
| 3 | Practical rules section (1-8) per § 1 above; jack-ryan may rearrange but must preserve semantic content |
| 4 | "What this discipline does NOT regulate" section preserves the carve-outs |
| 5 | Empirical anchors (§ 3 references) cited in a "Cross-references" closing section |
| 6 | **Header marker `**[PROPOSED — pending Matt ratification]**` present** at top of entry |
| 7 | Cross-references include Disciplines #2, #11, #19 + the Meshy probe + the robots verification log |
| 8 | Move the "Discipline #20 candidates" stub in Discipline #19's closing list to a new "Discipline #21 candidates" stub (the original three candidates in that stub are about JSON summary artifacts + log verbosity + wall-time estimates; those are LEGITIMATELY still queued for future discipline-numbering — do NOT delete them; just renumber the candidate stub heading) |

---

## 6. Out of scope (do NOT do these)

- Authoring Discipline #21 itself (just rename the candidate stub)
- Authoring decisions-log entry for Discipline #20 ratification (Matt does that at ratification time)
- Removing the PROPOSED marker (Matt removes that at ratification time)
- Modifying any of the existing 19 disciplines

---

## 7. Tag intent

On completion: `jack-ryan/v0.1-discipline-20-proposed`

---

**Signed:** knight-rider (overnight cascade; this is a Pattern-A dispatch — knight-rider invokes jack-ryan as sub-agent immediately after writing this file)
