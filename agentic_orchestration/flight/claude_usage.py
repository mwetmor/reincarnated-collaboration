"""U-11 Claude-lane usage ingester — session transcripts -> flight rows.

RUN U11-BUILD block B-1, star-lord (telemetry seam). Spec: `agentic_orchestration/
workflow-upgrades.md` § U-11. Binding rulings R-1…R-7: `agentic_orchestration/gandalf/
notes/2026-08-25-u11-build-run-ledger.md` § L-1.

THE GAP THIS CLOSES: the U-1 board renders Codex lanes with full token/cache columns
(native `codex exec --json` emission) and Grok with a vendor-reported `cost_usd`, while every
Claude lane renders a declared-null token cell — not because the numbers do not exist, but
because nothing read them. Every Claude Code session transcript at
`~/.claude/projects/**/*.jsonl` carries a per-message `usage` block with the exact four axes
the Codex lane records. This module reads them and folds them onto the tape.

THE LAW (#74), as it lands here — each clause with its mechanism, not its assertion:

  * **Zero write verbs against the substrate.** Every transcript touch in this file is
    `open(path, "r")` or an `os.stat`/`glob`. There is no `open(..., "w")`, no `os.remove`,
    no `shutil`, no rename, anywhere in this module, by construction.
  * **One data path.** Rows reach disk through `tape.append_row` — the same door the Codex
    normalizer and `flight_record` use. This module has no file-append of its own.
  * **Honest nulls.** Anything not mechanically derivable from the transcripts or from a
    named on-disk index is ABSENT from the row (`make_row` drops `None`), never zero-filled
    and never guessed. `workstream`, `seam`, `pin`, `rc` and `tokens_reasoning` are the
    common absences and each is absent for a stated reason (see `build_session_row`).
  * **No LLM in the truth path.** stdlib only; no network; no model call; no heuristic that
    reads prose for meaning. Attribution is exact-token matching against a named ledger.

RULINGS AS IMPLEMENTED:

  R-1  Row grain = ONE ROW PER SESSION, aggregating the main transcript PLUS the session's
       `subagents/` tree — sub-agent tokens are the session's economy, and on this substrate
       they are the MAJORITY share, so omitting them would understate the Claude lane by
       more than it reported. `derived_from` pins the main transcript and the subagents dir.
  R-2  Scope = sessions under a `reincarnated-*` project root whose usage messages fall in
       2026-08; month assignment by the LAST usage timestamp (a session spanning a month
       boundary lands once, in its closing month). `tape.append_row` routes on that `ts`.
  R-3  Workstream/operator mapping ONLY where mechanically derivable — see `custody_index`.
       Honest-null otherwise. No inference, no LLM.
  R-4  Every row `backfill: true` (G-2c-R1: `backfill` is TEMPORAL — the row was assembled
       after the event it records, which is true of every row this module will ever write).
  R-5  Schema v1.1 UNCHANGED. No field added, no enum widened. See TOKEN AXIS MAPPING.
  R-6  Quiescence + idempotence — see `is_quiescent` and `existing_unit_ids`.
  R-7  Zero render work: the report's existing derivations read these rows unmodified.

TOKEN AXIS MAPPING — the one interpretive choice in this build, stated loudly because it is
the only place a reader could disagree with me:

    anthropic `output_tokens`               -> tokens_output          (1:1)
    anthropic `cache_read_input_tokens`     -> tokens_cached_input    (1:1, R-5 names it)
    anthropic `cache_creation_input_tokens` -> tokens_cache_write     (1:1, R-5 names it)
    anthropic `input_tokens`
      + `cache_creation_input_tokens`
      + `cache_read_input_tokens`           -> tokens_input           (the SUM — see below)
    (no anthropic axis)                     -> tokens_reasoning       ABSENT, honest-null

`tokens_input` is NOT `usage.input_tokens` copied across, and the difference is a semantic
one rather than an arithmetic preference. The schema's `tokens_input` axis means TOTAL INPUT
PRESENTED, cached portion INCLUDED. Two independent proofs from the existing corpus:

  1. Codex's stream, which SCHEMA.md § 3 records as mapping 1:1, reports
     `input_tokens: 845782` alongside `cached_input_tokens: 750336` on the same turn — the
     cached figure is a SUBSET of the input figure, not an addend beside it.
  2. Every cache-hit cell on the board is `tokens_cached_input / tokens_input`
     (`bin/flight_report`, twice). That expression is a cache-hit RATE only if the
     denominator is total input. SCHEMA.md § 9 banks the corpus figure as
     "67,431,424 (93.17 % of input)" — a rate, and a rate needs its whole.

Anthropic reports the same whole as three DISJOINT components (fresh / cache-write /
cache-read; disjoint by API definition). Storing their exact sum puts the Claude lane on the
schema's axis; storing `input_tokens` alone would put a fresh-input count under a total-input
name and render a "cache-hit rate" of several thousand percent — a number that is wrong in
the specific way the recorder exists to prevent. The sum is EXACT, not an estimate: every
addend is a vendor-reported integer, nothing is scaled, and the fresh-input component stays
recoverable from the row itself as `tokens_input - tokens_cached_input - tokens_cache_write`.

`tokens_reasoning` is ABSENT rather than 0. Codex emits `reasoning_output_tokens`; the
Anthropic stream on this substrate emits no reasoning axis at all, and a measured zero and an
unmeasured axis are different facts. Declaring 0 would assert Claude did no reasoning.

DOUBLE-COUNT HAZARD and PROGRESSIVE-OUTPUT HAZARD — two defects, one dedupe key, and the
second one shipped. Stated here with its correction rather than quietly replaced, because the
sentence that carried the false premise is the sentence a future reader would trust:

  Claude Code writes ONE transcript line per assistant content block. Summing lines
  double-counts, so aggregation dedupes by `message.id` within the session tree. That much
  was right, and it was verified before the key was relied on: every usage-bearing line
  carries a `message.id`, and zero ids appear in more than one file within a session.

  **The B-1 build then asserted that every line of a multi-block message repeats the SAME
  `usage` object, and kept the FIRST line. That premise is FALSE.** The three INPUT axes do
  repeat identically. `output_tokens` does not — it is written PROGRESSIVELY: the non-terminal
  content-block lines carry a placeholder and the message's complete output count appears only
  on its terminal line. Keeping the first line recorded 1 where a measured message cost 401.

  Measured over the 27-session August population that this module emitted rows for — every
  figure below re-derived from those rows' own `derived_from`, denominators named (G-U11):

      92,185 usage-bearing lines · 49,590 distinct messages · 42,595 repeated lines (46.2 %)
      22,907 of 49,590 messages (46.2 %) carry DIFFERING `output_tokens` across their lines
      `output_tokens` non-decreasing across a message's lines: 22,907 of 22,907 — 0 exceptions
      first-line selector: 19,327,247 output   ·   terminal selector: 50,878,369 output
      the shipped column was short by 31,551,122 — 62.0 % of the true figure

  The three input axes are byte-IDENTICAL under both selectors (fresh 359,469 · cache-write
  204,120,185 · cache-read 8,238,067,996 · `tokens_input` 8,442,547,650), which is why the
  correction touches one axis and only one.

  So `aggregate_session` takes the message's TERMINAL usage payload: the line whose
  `message.stop_reason` is non-null, falling back to the last-seen line for the messages that
  carry none. The selector is SEMANTIC rather than positional on purpose — a positional rule
  ("take the last line") is silent if line order ever changes, whereas `stop_reason` is the
  vendor's own statement that the message finished. Positional-last, semantic, and per-axis
  maximum all agree exactly on this population, so the choice is safe today; the semantic one
  stays safe.

Python 3 stdlib only. No network. No LLM. Ever.
"""

from __future__ import annotations

import datetime
import glob
import json
import os
import re
import time

import schema
import tape

#: Where Claude Code keeps its session transcripts. Read-only, always.
CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")

#: The repo roots whose sessions are in scope (R-2). A project directory is Claude Code's
#: encoding of the session's launch cwd with `/` replaced by `-`, so scope is decidable by
#: string prefix against the encoded root — no decoding required and no guessing about which
#: `-` was a separator. `reincarnated-*` siblings are included even where they currently hold
#: zero transcripts, so a future engine-seam session is captured without a code change.
SCOPE_ROOTS = ("reincarnated-collaboration", "reincarnated-demo", "reincarnated-engine",
               "reincarnated-loadout", "reincarnated-godot")

#: Identity constants for this lane. Each is a mechanical fact about the substrate, not a
#: preference: the transcripts are Anthropic model responses (`provider`), produced by the
#: Claude Code CLI (`harness`, corroborated by the per-line `version` key this module reads
#: into `harness_version`), on the Max subscription that is this host's only Claude credential
#: (`currency`, matching every `claude-agent` row already on the tape).
PROVIDER = "anthropic"
LANE = "claude-agent"
CURRENCY = "anthropic-max"
HARNESS = "claude-code"

#: `unit_id` namespace. One session, one unit, forever (R-6 dedupe key).
UNIT_PREFIX = "claude-session/"
UNIT_KIND = "session"

#: R-6: a transcript untouched for this long is treated as closed. The conductor's own live
#: session is excluded by this rule, which is the intended behaviour, not a gap.
QUIESCENCE_SECONDS = 60 * 60

#: R-3 attribution source, repo-root-relative (it is inside the meta-repo, unlike the
#: transcripts, which are not inside any repo).
CUSTODY_TSV = "agentic_orchestration/lanes/agents/_custody.tsv"

#: `<agent>-session-<id-fragment>` — the custody ledger's holder-session vocabulary.
HOLDER_RE = re.compile(r"^(?P<agent>[a-z0-9][a-z0-9-]*?)-session-(?P<frag>[0-9a-f]{6,})$")

#: A fragment shorter than this is not allowed to identify a session. Eight hex chars is the
#: first dash-delimited group of a UUID; the ledger's live example (`gandalf-session-53631d11`)
#: is exactly that. Shorter fragments (`gandalf-session-85515`) are NOT session ids and must
#: not be coerced into one — they resolve to no session and contribute no attribution.
MIN_FRAGMENT = 8

TS_FRACTIONAL_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.\d+)?Z$")


class IngestError(RuntimeError):
    """Raised when the substrate cannot be read as this module requires."""


# --- substrate discovery (read-only) ----------------------------------------

def in_scope_project_dirs(projects_dir: str = None, games_dir: str = None) -> list:
    """Project directories under a `reincarnated-*` root. Pure listing; nothing is opened."""
    projects_dir = projects_dir or CLAUDE_PROJECTS_DIR
    games_dir = games_dir or os.path.dirname(schema.META_REPO_ROOT)
    keys = [os.path.join(games_dir, r).replace("/", "-") for r in SCOPE_ROOTS]
    out = []
    if not os.path.isdir(projects_dir):
        return out
    for name in sorted(os.listdir(projects_dir)):
        path = os.path.join(projects_dir, name)
        if not os.path.isdir(path):
            continue
        if any(name == k or name.startswith(k + "-") for k in keys):
            out.append(path)
    return out


def discover_sessions(projects_dir: str = None, games_dir: str = None) -> dict:
    """`session_id -> {"files": [...], "main": path|None, "subagents_dir": path|None}`.

    R-1's grain in file terms: a session is its top-level `<sessionId>.jsonl` PLUS every
    `<sessionId>/subagents/*.jsonl` beside it. A session dir with sub-agent tapes but no
    top-level transcript is still a session — it is discovered, not dropped.
    """
    sessions = {}

    def bucket(sid):
        return sessions.setdefault(sid, {"files": [], "main": None, "subagents_dir": None})

    for pdir in in_scope_project_dirs(projects_dir, games_dir):
        for f in sorted(glob.glob(os.path.join(pdir, "*.jsonl"))):
            sid = os.path.basename(f)[:-len(".jsonl")]
            b = bucket(sid)
            b["main"] = f
            b["files"].append(f)
        for f in sorted(glob.glob(os.path.join(pdir, "*", "subagents", "*.jsonl"))):
            sdir = os.path.dirname(f)
            sid = os.path.basename(os.path.dirname(sdir))
            b = bucket(sid)
            b["subagents_dir"] = sdir
            b["files"].append(f)

    for b in sessions.values():
        b["files"] = sorted(set(b["files"]))
    return sessions


# --- usage aggregation (read-only) ------------------------------------------

def iter_usage(path: str):
    """Yield `(message_id, usage_dict, envelope)` for every usage-bearing line in one file.

    Opened read-only. A line that is not JSON, or carries no usage, is skipped silently —
    transcripts contain many non-message line kinds and their presence is not a defect.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"usage"' not in line:
                continue
            try:
                env = json.loads(line)
            except ValueError:
                continue
            msg = env.get("message")
            if not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            if not isinstance(usage, dict) or usage.get("input_tokens") is None:
                continue
            yield msg.get("id"), usage, env


def _norm_ts(raw: str):
    """`2026-08-24T20:28:21.904Z` -> `2026-08-24T20:28:21Z`, or None if unparseable.

    Truncation, never rounding: rounding a timestamp up could move a session across a month
    boundary and therefore across tapes.
    """
    m = TS_FRACTIONAL_RE.match(raw or "")
    return (m.group(1) + "Z") if m else None


def terminal_rank(env: dict) -> int:
    """How authoritative this line's `usage` is for its message. Higher wins.

    2 = the vendor said the message FINISHED here (`message.stop_reason` non-null).
    1 = a non-terminal content-block line, whose `output_tokens` is a placeholder.

    This is the whole of the semantic selector, isolated so a test can address it directly
    and so the rule is greppable rather than buried in an aggregation loop.
    """
    msg = env.get("message")
    if isinstance(msg, dict) and msg.get("stop_reason") is not None:
        return 2
    return 1


def aggregate_session(files: list) -> dict:
    """Sum one session's economy across its transcript tree. Nothing is written.

    Returns a dict of exact vendor-reported sums plus the identity axes observed.

    TWO passes over one iteration, because a message's lines answer two different questions:

      * WHICH MESSAGES exist, and WHEN / on what model they were recorded — answered by the
        message's FIRST-SEEN line, deduped by `message.id`. `lines` and `calls` are both
        returned so the discarded repeats stay visible rather than silently vanishing.
      * WHAT THE MESSAGE COST — answered by its TERMINAL usage payload (see the module
        docstring's PROGRESSIVE-OUTPUT note). Every line of the message is offered to the
        selector, including the repeats the dedupe discards for counting purposes, because
        the repeat IS where the true output count lives.

    The token sums are therefore taken AFTER the scan, from one usage payload per message —
    never accumulated line-by-line, which is what made the first-line selector look correct.
    """
    seen = set()
    usage_by_message = {}     # message.id -> (rank, usage) — the terminal payload
    progressive = set()       # message.ids whose lines disagree about `output_tokens`
    agg = {"input": 0, "cache_write": 0, "cache_read": 0, "output": 0,
           "calls": 0, "lines": 0, "repeated_lines": 0, "unidentified_lines": 0,
           "progressive_messages": 0,
           "first_ts": None, "last_ts": None, "models": set(), "versions": set(),
           "session_ids": set(), "bad_ts": 0}
    for path in files:
        for mid, usage, env in iter_usage(path):
            agg["lines"] += 1
            if not mid:
                # No id means no dedupe key. Counted and skipped rather than summed on a
                # guess: an over-count is a wrong number, and a named omission is not.
                agg["unidentified_lines"] += 1
                continue
            if mid in seen:
                agg["repeated_lines"] += 1
            else:
                seen.add(mid)
                agg["calls"] += 1
                ts = _norm_ts(env.get("timestamp"))
                if ts is None:
                    agg["bad_ts"] += 1
                else:
                    if agg["first_ts"] is None or ts < agg["first_ts"]:
                        agg["first_ts"] = ts
                    if agg["last_ts"] is None or ts > agg["last_ts"]:
                        agg["last_ts"] = ts
                model = (env.get("message") or {}).get("model")
                if model:
                    agg["models"].add(model)
                if env.get("version"):
                    agg["versions"].add(env["version"])
                if env.get("sessionId"):
                    agg["session_ids"].add(env["sessionId"])

            # --- the terminal-usage selector, offered EVERY line of the message ---------
            rank = terminal_rank(env)
            held = usage_by_message.get(mid)
            if held is None:
                usage_by_message[mid] = (rank, usage)
            else:
                if (held[1].get("output_tokens") or 0) != (usage.get("output_tokens") or 0):
                    # Counted, not assumed: the population where the two selectors DIVERGE
                    # is the population BLOCK-1 was about, and a coverage figure for it is
                    # cheaper than trusting the docstring again.
                    progressive.add(mid)
                if rank >= held[0]:
                    # `>=` so that, at equal rank, the LAST line seen wins — the positional
                    # fallback for the messages that carry no `stop_reason` at all.
                    usage_by_message[mid] = (rank, usage)

    for _rank, usage in usage_by_message.values():
        agg["input"] += usage.get("input_tokens") or 0
        agg["cache_write"] += usage.get("cache_creation_input_tokens") or 0
        agg["cache_read"] += usage.get("cache_read_input_tokens") or 0
        agg["output"] += usage.get("output_tokens") or 0
    agg["progressive_messages"] = len(progressive)
    return agg


def tokens_total_input(agg: dict) -> int:
    """The schema's `tokens_input` axis: total input presented, cached portion included.

    See the module docstring's TOKEN AXIS MAPPING for why this is a sum rather than a copy.
    """
    return agg["input"] + agg["cache_write"] + agg["cache_read"]


def mtime_max(files: list) -> float:
    return max((os.path.getmtime(f) for f in files), default=0.0)


def is_quiescent(files: list, now_epoch: float = None,
                 quiescence_seconds: int = QUIESCENCE_SECONDS) -> bool:
    """R-6: no transcript in the tree touched for >= the quiescence window.

    Asked of the whole tree, not the main transcript alone — a session whose sub-agent is
    still writing is still spending.
    """
    now_epoch = time.time() if now_epoch is None else now_epoch
    return (now_epoch - mtime_max(files)) >= quiescence_seconds


# --- R-3 attribution (mechanical only) --------------------------------------

def known_workstreams(records_dir: str) -> set:
    """The workstream vocabulary the TAPE already uses — derived, never hand-listed.

    Attribution matches against this set so the emitter can only ever assign a workstream the
    recorder already knows; it cannot mint one out of prose. Deriving the vocabulary from the
    tape rather than pinning a literal is the R-L47-2 discipline applied to the emitter's own
    inputs: the list grows when the tape grows, with no edit here.
    """
    rows, _ = tape.load(records_dir)
    return {r["workstream"] for r in rows if r.get("workstream")}


def custody_index(custody_path: str, session_ids, vocabulary) -> dict:
    """`session_id -> {"operator": str|None, "workstreams": set}` from the custody ledger.

    R-3, and the whole rule is exact-token matching — there is no parsing of meaning here:

      * column 3 holds a holder token `<agent>-session-<fragment>`. A session is identified
        when `<fragment>` (>= 8 hex chars) is a PREFIX of exactly one discovered session id.
        The agent name in the token is then that session's `operator` — a direct identity
        mapping recorded by the team itself, not an inference about who was typing.
      * the row's own free-text columns are scanned for EXACT occurrences of workstream names
        the tape already carries (`vocabulary`). Prose is never read for meaning; a token
        either appears verbatim or it does not.

    A session whose custody rows name MORE THAN ONE workstream gets no workstream: the row
    grain is one session and one workstream field, so an ambiguous session is honest-null
    rather than arbitrarily assigned its first or last claim. Ambiguity is reported by the
    caller as coverage, not resolved by preference.
    """
    out = {}
    if not os.path.exists(custody_path):
        return out
    session_ids = list(session_ids)
    with open(custody_path, "r", encoding="utf-8") as fh:
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 3:
                continue
            m = HOLDER_RE.match(cols[2].strip())
            if not m or len(m.group("frag")) < MIN_FRAGMENT:
                continue
            frag = m.group("frag")
            matches = [s for s in session_ids if s.startswith(frag)]
            if len(matches) != 1:
                continue                      # 0 = not a session id; >1 = ambiguous
            sid = matches[0]
            ent = out.setdefault(sid, {"operator": None, "operators": set(),
                                       "workstreams": set()})
            ent["operators"].add(m.group("agent"))
            text = "\t".join(cols[3:])
            for ws in vocabulary:
                if re.search(r"(?<![A-Za-z0-9-])%s(?![A-Za-z0-9-])" % re.escape(ws), text):
                    ent["workstreams"].add(ws)
    for ent in out.values():
        ent["operator"] = (sorted(ent["operators"])[0] if len(ent["operators"]) == 1 else None)
    return out


# --- row construction --------------------------------------------------------

def unit_id_for(session_id: str) -> str:
    return UNIT_PREFIX + session_id


def existing_unit_ids(records_dir: str) -> set:
    """R-6 idempotence key: a session gets exactly one row, ever.

    Dedupe is by `unit_id`, deliberately NOT by `row_id`. A row_id is a content address, so a
    re-run over a session that gained one more message would mint a DIFFERENT row_id and the
    content-address dedupe in `tape.append_row` would wave it through as a second row for the
    same session. Asking "does this session already have a row" is the question R-6 actually
    poses, and it is the only question whose answer is stable under a growing substrate.
    """
    rows = schema.read_tape(tape.tape_files(records_dir))
    return {r["unit_id"] for r in rows if r.get("unit_id")}


def build_session_row(session_id: str, session: dict, agg: dict, attribution: dict,
                      repo: str, repo_root: str = None) -> dict:
    """One CLOSE row for one session. Every absence below is a stated absence.

    CLOSE (not START+CLOSE) because R-1 says one row per session and because a CLOSE is the
    only event the schema lets carry cost fields (`FIELD_MATRIX`). The report's span cell will
    say "no START row" for these units, which is true: this emitter reads a finished
    transcript and never witnessed a start.

    ABSENT, each for a reason:
      `pin`             the transcript echoes the RESOLVED model, which is `model_echo`.
                        What was requested is not in the substrate, so no pin is claimed.
      `tokens_reasoning` no anthropic axis reports it (see module docstring).
      `rc` / `attempt`  a session is not a process; it has no exit code and no retry count.
      `artifacts`       a session's outputs are commits and files across four repos, not a
                        harness-declared artifact list. Nothing mechanical to name.
      `verdict`/`gatekeeper`  no one judged a session. B-2 forbids inventing one.
      `seam`            not derivable — an agent's seam is a role fact, and the transcript
                        records a cwd, not a seam.
      `workstream`      honest-null wherever the custody ledger does not name exactly one.
    """
    derived = []
    if session.get("main"):
        derived.append(session["main"])
    if session.get("subagents_dir"):
        derived.append(session["subagents_dir"])
    if not derived:
        raise IngestError("session %s has no transcript to name" % session_id)
    if attribution.get("operator") or attribution.get("workstream"):
        derived.append(CUSTODY_TSV)

    models = sorted(agg["models"])
    versions = sorted(agg["versions"])

    return schema.make_row(
        "CLOSE",
        ts=agg["last_ts"],
        unit_id=unit_id_for(session_id),
        unit_kind=UNIT_KIND,
        workstream=attribution.get("workstream"),
        operator=attribution.get("operator"),
        repo=repo,
        backfill=True,                                   # R-4
        derived_from=derived,
        provider=PROVIDER,
        lane=LANE,
        # The vendor's own echoed model id(s), verbatim. A session that spanned more than one
        # resolved model names all of them rather than picking one: the set is what the stream
        # said, and picking a representative would be a summary of it.
        model_echo=", ".join(models) or None,
        harness=HARNESS,
        # Single-valued or absent. A session that spanned two CLI versions has no single
        # harness version, and joining them would put a non-version string in a version field.
        harness_version=versions[0] if len(versions) == 1 else None,
        currency=CURRENCY,
        tokens_input=tokens_total_input(agg),
        tokens_cached_input=agg["cache_read"],
        tokens_cache_write=agg["cache_write"],
        tokens_output=agg["output"],
        repo_root=repo_root,
    )


# --- the ingest ---------------------------------------------------------------

def repo_for_session(session: dict, games_dir: str = None) -> str:
    """Which repo root this session's project dir encodes. Mechanical, from the dir name."""
    games_dir = games_dir or os.path.dirname(schema.META_REPO_ROOT)
    pdir = os.path.basename(os.path.dirname(
        session["main"] or os.path.dirname(session["subagents_dir"])))
    best = None
    for r in SCOPE_ROOTS:
        key = os.path.join(games_dir, r).replace("/", "-")
        if (pdir == key or pdir.startswith(key + "-")) and (best is None or len(r) > len(best)):
            best = r
    return best


def ingest(records_dir: str, projects_dir: str = None, games_dir: str = None,
           months=("2026-08",), now_epoch: float = None,
           quiescence_seconds: int = QUIESCENCE_SECONDS,
           dry_run: bool = False, repo_root: str = None) -> dict:
    """Fold every eligible session onto the tape. Returns a report dict; writes nothing else.

    Skips are CLASSIFIED and returned, never dropped — a session the emitter passed over is a
    fact about coverage, and a coverage figure whose denominator is invisible is the
    mixed-denominator defect the board already refuses elsewhere.
    """
    repo_root = repo_root or schema.META_REPO_ROOT
    now_epoch = time.time() if now_epoch is None else now_epoch
    sessions = discover_sessions(projects_dir, games_dir)

    vocabulary = known_workstreams(records_dir)
    attribution = custody_index(os.path.join(repo_root, CUSTODY_TSV),
                                sessions.keys(), vocabulary)
    already = existing_unit_ids(records_dir)

    report = {"scanned": len(sessions), "appended": [], "rows": [],
              "skipped": {"no-usage": [], "out-of-month": [], "not-quiescent": [],
                          "already-emitted": []},
              "attribution": {"operator": [], "workstream": [], "workstream-ambiguous": []},
              "aggregates": {}, "generated_at": now_epoch}

    for sid in sorted(sessions):
        session = sessions[sid]
        if unit_id_for(sid) in already:
            report["skipped"]["already-emitted"].append(sid)
            continue
        agg = aggregate_session(session["files"])
        if not agg["calls"] or agg["last_ts"] is None:
            report["skipped"]["no-usage"].append(sid)
            continue
        if schema.month_of(agg["last_ts"]) not in months:
            report["skipped"]["out-of-month"].append((sid, agg["last_ts"]))
            continue
        if not is_quiescent(session["files"], now_epoch, quiescence_seconds):
            report["skipped"]["not-quiescent"].append(
                (sid, round((now_epoch - mtime_max(session["files"])) / 60.0, 1)))
            continue

        ent = attribution.get(sid) or {}
        wss = sorted(ent.get("workstreams") or ())
        attr = {"operator": ent.get("operator"),
                "workstream": wss[0] if len(wss) == 1 else None}
        if attr["operator"]:
            report["attribution"]["operator"].append(sid)
        if attr["workstream"]:
            report["attribution"]["workstream"].append((sid, attr["workstream"]))
        elif len(wss) > 1:
            report["attribution"]["workstream-ambiguous"].append((sid, wss))

        row = build_session_row(sid, session, agg, attr, repo_for_session(session, games_dir),
                                repo_root=repo_root)
        path, status = tape.append_row(row, records_dir, dry_run=dry_run, repo_root=repo_root)
        report["rows"].append(row)
        report["appended"].append((sid, row["row_id"], status))
        report["aggregates"][sid] = {k: v for k, v in agg.items()
                                     if not isinstance(v, set)}
    return report


def summarize(report: dict) -> dict:
    """Derived headline figures over the rows THIS run produced. Nothing stored."""
    rows = report["rows"]
    tin = sum(r.get("tokens_input") or 0 for r in rows)
    tcr = sum(r.get("tokens_cached_input") or 0 for r in rows)
    return {
        "rows": len(rows),
        "tokens_input": tin,
        "tokens_cached_input": tcr,
        "tokens_cache_write": sum(r.get("tokens_cache_write") or 0 for r in rows),
        "tokens_output": sum(r.get("tokens_output") or 0 for r in rows),
        "cache_hit_pct": (100.0 * tcr / tin) if tin else None,
        "calls": sum(a["calls"] for a in report["aggregates"].values()),
        "repeated_lines_discarded": sum(a["repeated_lines"]
                                        for a in report["aggregates"].values()),
        "unidentified_lines": sum(a["unidentified_lines"]
                                  for a in report["aggregates"].values()),
        "progressive_messages": sum(a.get("progressive_messages", 0)
                                    for a in report["aggregates"].values()),
    }


# --- the correction pass (G-U11 BLOCK-1 discharge) ----------------------------
#
# The tape is APPEND-ONLY and nothing on it may be edited, so a row that recorded a wrong
# number is repaired by appending a `corrects:` row beside it — the schema's only amendment
# path. This pass re-derives every U-11 row from ITS OWN `derived_from` and appends a
# correction wherever a measured axis disagrees with what was shipped.
#
# It re-derives from the ROW rather than re-running discovery on purpose: the substrate grows,
# and a correction must be a statement about the sources the original row named, not about
# whatever those sessions have become since.

#: The gate that measured the defect. Named on every correction row so the amendment carries
#: its own provenance and a reader can find out WHY the number moved without a git log.
GATE_FINDINGS = "agentic_orchestration/qa/findings/2026-08-25-u11-gate.md"

#: The axes a correction may restate. Identity, timestamps and attribution are NOT re-derived:
#: this pass repairs a measurement, and silently moving a row's `ts` under cover of a token
#: correction would be a second, undeclared amendment.
CORRECTABLE_AXES = ("tokens_input", "tokens_cached_input", "tokens_cache_write",
                    "tokens_output")


def u11_rows(rows) -> list:
    """Every row this module authored, identified by its own `unit_id` namespace."""
    return [r for r in rows
            if str(r.get("unit_id") or "").startswith(UNIT_PREFIX) and r.get("event") == "CLOSE"]


def superseded_ids(rows) -> set:
    """row_ids already named by a `corrects` edge — do not correct a correction's target."""
    return {r["corrects"] for r in rows if r.get("corrects")}


def files_for_row(row: dict) -> list:
    """Re-expand a row's `derived_from` into the transcript files it names.

    A `derived_from` entry is either the session's main transcript or its `subagents` DIR
    (R-1). A directory is expanded to the tapes inside it; a path that no longer exists is
    NOT silently dropped — `IngestError` fires, because a correction derived from a partial
    read would be a worse number than the one it replaces.
    """
    out = []
    for p in row.get("derived_from") or ():
        if p == CUSTODY_TSV or not p.endswith((".jsonl", "subagents")):
            continue
        if os.path.isdir(p):
            out.extend(glob.glob(os.path.join(p, "*.jsonl")))
        elif os.path.isfile(p):
            out.append(p)
        else:
            raise IngestError("row %s names a source that is gone: %s"
                              % (row.get("row_id"), p))
    if not out:
        raise IngestError("row %s names no readable transcript" % row.get("row_id"))
    return sorted(set(out))


def measured_axes(row: dict) -> dict:
    """Re-derive the four token axes for one row, from the sources the row itself names."""
    agg = aggregate_session(files_for_row(row))
    return {"tokens_input": tokens_total_input(agg),
            "tokens_cached_input": agg["cache_read"],
            "tokens_cache_write": agg["cache_write"],
            "tokens_output": agg["output"]}


def build_correction_row(original: dict, measured: dict, repo_root: str = None,
                         findings: str = GATE_FINDINGS) -> dict:
    """One `corrects:` row restating the measured axes. Every other field is carried across.

    `backfill` is True for the same reason every U-11 row's is (R-4 / G-2c-R1): the row is
    assembled after the event it records. A correction is, by construction, retrospective.
    """
    fields = {k: v for k, v in original.items()
              if k not in ("v", "row_id", "event", "ts", "corrects")}
    fields.update({k: measured[k] for k in CORRECTABLE_AXES if k in measured})
    fields["corrects"] = original["row_id"]
    fields["backfill"] = True
    df = list(original.get("derived_from") or [])
    if findings and findings not in df:
        df.append(findings)
    fields["derived_from"] = df
    return schema.make_row("CLOSE", ts=original["ts"], repo_root=repo_root, **fields)


def correct(records_dir: str, repo_root: str = None, dry_run: bool = False,
            findings: str = GATE_FINDINGS, emit_unchanged: bool = False) -> dict:
    """Append a correction for every U-11 row whose measured axes have moved.

    Idempotent by construction and in two independent ways: a row already named by a
    `corrects` edge is skipped, and a row whose re-derivation AGREES with what is on the tape
    produces no correction at all. Running this twice appends nothing the second time.

    `emit_unchanged=True` corrects EVERY row, delta or not. It exists because G-U11's
    discharge condition reads "emit `corrects:` correction rows for all 27 rows", and the
    measured population is smaller than 27 — see the note below. It is OFF by default and the
    default is the deliberate call, not an oversight:

      The gate's own per-row claim ("under-reported on 27/27 rows") is a LANE-grain finding
      stated at ROW grain. Re-derived per row from each row's own `derived_from`, the two
      selectors disagree on SOME of the rows and agree byte-for-byte on the rest — the
      agreeing ones are the sessions with no multi-block message (the four synthetic-probe
      zero rows among them). Appending a `corrects:` row that restates identical values would
      put an amendment on an append-only tape asserting a change that did not happen, and a
      later reader counting corrections would over-count the defect's blast radius. The
      recorder refuses to manufacture a measurement; it should equally refuse to manufacture
      an AMENDMENT. Both populations are reported, so the ruling is re-derivable either way
      and costs one flag.
    """
    repo_root = repo_root or schema.META_REPO_ROOT
    rows = schema.read_tape(tape.tape_files(records_dir))
    already = superseded_ids(rows)
    report = {"examined": 0, "unchanged": [], "already_corrected": [], "corrected": [],
              "deltas": {}, "rows": []}
    for row in sorted(u11_rows(rows), key=lambda r: (r.get("unit_id"), r.get("ts"))):
        if row["row_id"] in already:
            report["already_corrected"].append(row["row_id"])
            continue
        report["examined"] += 1
        measured = measured_axes(row)
        delta = {k: (row.get(k), measured[k]) for k in CORRECTABLE_AXES
                 if row.get(k) != measured[k]}
        if not delta:
            report["unchanged"].append(row["row_id"])
            if not emit_unchanged:
                continue
        corr = build_correction_row(row, measured, repo_root=repo_root, findings=findings)
        tape.append_row(corr, records_dir, dry_run=dry_run, repo_root=repo_root)
        report["corrected"].append((row["unit_id"], row["row_id"], corr["row_id"]))
        report["deltas"][row["row_id"]] = delta
        report["rows"].append(corr)
    return report


def utc(epoch: float) -> str:
    return datetime.datetime.utcfromtimestamp(epoch).strftime("%Y-%m-%dT%H:%M:%SZ")
