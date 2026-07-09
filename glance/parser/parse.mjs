#!/usr/bin/env node
/**
 * Glance parser — deterministic canon → state.json.
 *
 * Contract sources (authoritative):
 *   - canonical-doc-format.md § 7 (the five legislated shapes, RATIFIED jack-ryan 2026-07-06)
 *   - engineering-disciplines.md Discipline #60 (CI-fail-loud severity split)
 *   - glance-contract-spec-2026-07-03.md § 3 (state.json output contract)
 *
 * NO LLM. NO network. NO judgment. Pure text → structure.
 *
 * The parser reads ONLY:
 *   canonical/current-to-end-state/current-to-end-state-{engine,story,game,serial-content-emission}.md  (the 4 trackers)
 *   canonical/current-to-end-state/surface-ledger.md  (the 5th Tier-0 card — Glance contract v1.3 §7.2)
 *   canonical/matt_decision_needed/README.md
 *   canonical/matt_to_do/README.md
 * It NEVER touches the engine tree.
 *
 * Severity split (Discipline #60 / § 7.6) — closed, enumerated MALFORMED set (exactly 3):
 *   (a) a queue row whose first cell begins with a row ID but whose table structure is broken;
 *   (b) a SESSION-DELTA heading (### YYYY-MM-DD — …) whose date is unparseable;
 *   (c) a duplicate row ID within one board.
 * MALFORMED → CI build FAILURE with file+line.
 * Dangling gates-on token → warning badge (never a failure).
 * ABSENCE is never an error.
 *
 * Modes:
 *   node parse.mjs            → write state.json; exit 1 if any MALFORMED (unless GLANCE_REPORT_ONLY)
 *   node parse.mjs --report   → list ALL malformed findings in one pass, then exit 1 (report mode)
 *                               (still writes state.json so a preview can render)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
// repo root = two levels up from glance/parser/
const REPO_ROOT = resolve(__dirname, '..', '..');
const CANON = join(REPO_ROOT, 'canonical');

const REPORT_MODE = process.argv.includes('--report');
// The GitHub blob base for deep-links (§6). Overridable via env for forks.
const GH_BLOB_BASE =
  process.env.GLANCE_GH_BLOB_BASE ||
  'https://github.com/mwetmor/reincarnated-collaboration/blob/main';

// ---------------------------------------------------------------------------
// Findings accumulator (the report-mode surface)
// ---------------------------------------------------------------------------
const findings = []; // { severity: 'MALFORMED'|'WARN', kind, path, line, message }
function malformed(kind, relPath, line, message) {
  findings.push({ severity: 'MALFORMED', kind, path: relPath, line, message });
}

// ---------------------------------------------------------------------------
// Status enum — § 7.3 prefix table
// ---------------------------------------------------------------------------
const STATUS_PREFIXES = [
  { token: 'closed', match: '✓' },
  { token: 'blocked', match: '⛔' },
  { token: 'awaiting_ruling', match: '⚖' },
  { token: 'parked', match: 'PARKED' },
  { token: 'in_flight', match: 'IN-FLIGHT' },
];
// OPEN (or no prefix) is the default.

/**
 * § 7.3: "some cell carries a status PREFIX". A prefix leads a cell. So the
 * status is decided by scanning each cell for a LEADING status token; a token
 * buried in free prose (e.g. "night-sky presentation PARKED → game tracker",
 * or a "✓ DONE" reference to a sub-item) is prose, NOT the row's status.
 *
 * Detection order across the row's cells:
 *   1. any cell whose (bold/emphasis-stripped) content BEGINS with a status
 *      token — first such cell wins, in the STATUS_PREFIXES precedence order
 *      the cell itself presents (leftmost leading token in that cell);
 *   2. else default OPEN (§ 7.3: "OPEN (or no prefix)").
 *
 * Passed the FULL set of cells, not a joined string, so "begins-with" is real.
 */
function statusAtCellStart(cellRaw) {
  const t = stripInlineMd(cellRaw);
  for (const { token, match } of STATUS_PREFIXES) {
    if (t.startsWith(match)) {
      return { token, prose: t.slice(match.length).trim() };
    }
  }
  if (t.startsWith('OPEN')) return { token: 'open', prose: t.slice(4).trim() };
  return null;
}
function detectStatusFromCells(cells) {
  for (const c of cells) {
    const s = statusAtCellStart(c);
    if (s) return s;
  }
  return { token: 'open', prose: '' };
}

// ---------------------------------------------------------------------------
// Row-ID grammar — § 7.3
//   D.1#8, D.1 #8, B1, W0.3, III.8, Q2, or a plain ordinal (1, 2, ...)
// The first cell "begins with" a row ID. We also strip markdown bold/emphasis.
// ---------------------------------------------------------------------------
function stripInlineMd(s) {
  return s.replace(/\*\*/g, '').replace(/`/g, '').replace(/~~/g, '').trim();
}

// A row ID is: an alnum/dot/hash token at the start. We accept the documented
// families plus plain ordinals. Deliberately permissive on the token body but
// anchored at cell start so free-prose rows (no leading ID) are NOT modeled.
// ORDER MATTERS: the longest/most-specific alternative first (Roman-numeral
// dotted IDs like III.1 must win over the bare-alpha III branch).
const ROW_ID_RE =
  /^([IVX]+\.[0-9]+|[A-Z]\.[0-9]+(?:\s*#\s*[0-9]+)?|[A-Z]{1,4}[0-9]+(?:\.[0-9]+)*|[A-Z]{1,4}[0-9]*(?:\s*#\s*[0-9]+)|[0-9]+)(?=$|[\s—:.)|])/;

function extractRowId(firstCellRaw) {
  const cell = stripInlineMd(firstCellRaw);
  const m = cell.match(ROW_ID_RE);
  if (!m) return null;
  // normalize whitespace inside the id (D.1 #8 -> D.1#8)
  return m[1].replace(/\s+/g, '');
}

// ---------------------------------------------------------------------------
// gates-on: grammar — § 7.4
//   gates-on: <token>[ (<qualifier>) ] [· <token>[ (<qualifier>) ]]*
// ---------------------------------------------------------------------------
function extractGatesOn(rowText) {
  const gates = [];
  const re = /gates-on:\s*([^\n|]+)/gi;
  let m;
  while ((m = re.exec(rowText)) !== null) {
    const clause = m[1].trim();
    // split on the middot separator
    for (const part of clause.split('·')) {
      const p = part.trim();
      if (!p) continue;
      // token (optional (qualifier))
      const tm = p.match(/^([A-Za-z0-9.#_-]+)\s*(?:\(([^)]*)\))?/);
      if (!tm) continue;
      gates.push({
        token: tm[1].replace(/\s+/g, ''),
        qualifier: tm[2] ? tm[2].trim() : null,
        resolved: false, // filled in the resolution pass
      });
    }
  }
  return gates;
}

// ---------------------------------------------------------------------------
// Known agent names for best-effort owner extraction (§3)
// ---------------------------------------------------------------------------
const AGENTS = [
  'gandalf', 'knight-rider', 'jack-ryan', 'rocket', 'gamora', 'star-lord',
  'galadriel', 'elrond', 'legolas', 'drax', 'matt',
];
function extractOwner(cells) {
  const joined = cells.join(' ').toLowerCase();
  for (const a of AGENTS) {
    if (joined.includes(a)) return a;
  }
  return null;
}

// ---------------------------------------------------------------------------
// Line helpers
// ---------------------------------------------------------------------------
function splitTableRow(line) {
  // a markdown table row: | a | b | c |
  let s = line.trim();
  if (!s.startsWith('|')) return null;
  s = s.replace(/^\|/, '').replace(/\|$/, '');
  return s.split('|').map((c) => c.trim());
}
function isSeparatorRow(cells) {
  return cells.every((c) => /^:?-{3,}:?$/.test(c.replace(/\s/g, '')));
}

// ---------------------------------------------------------------------------
// Shape 1 — STATUS banner (§ 7.1)
// First blockquote line containing the literal **STATUS:** marker.
// ---------------------------------------------------------------------------
const STAMP_WORDS = [
  'PARTIALLY SUPERSEDED', 'SUPERSEDED', 'SPEC-CURRENT', 'CANONICAL',
  'LIVING', 'CURRENT', 'ROUTER', 'HISTORICAL', 'DEAD',
];
function parseStatusBanner(lines, relPath) {
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    if (/\*\*STATUS:\*\*/.test(raw)) {
      // stamp: first matching stamp word after the marker
      const after = raw.split(/\*\*STATUS:\*\*/)[1] || '';
      let stamp = null;
      for (const w of STAMP_WORDS) {
        if (after.toUpperCase().includes(w)) { stamp = w; break; }
      }
      const dateMatch = raw.match(/(\d{4}-\d{2}-\d{2})/);
      return {
        stamp: stamp || null,
        date: dateMatch ? dateMatch[1] : null,
        raw: raw.trim(),
        line: i + 1,
      };
    }
  }
  return null; // absence is legal
}

// ---------------------------------------------------------------------------
// Shape 2 — SESSION-DELTA LOG (§ 7.2)
// ## SESSION-DELTA LOG   then   ### YYYY-MM-DD — headline (newest first).
// ---------------------------------------------------------------------------
function isValidDate(s) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return false;
  const [y, m, d] = s.split('-').map(Number);
  if (m < 1 || m > 12) return false;
  if (d < 1 || d > 31) return false;
  const dt = new Date(Date.UTC(y, m - 1, d));
  return dt.getUTCFullYear() === y && dt.getUTCMonth() === m - 1 && dt.getUTCDate() === d;
}

function parseDeltaLog(lines, relPath) {
  const deltas = [];
  // find the SESSION-DELTA LOG section start
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (/^##\s+SESSION-DELTA LOG/i.test(lines[i])) { start = i; break; }
  }
  if (start === -1) return deltas; // absence is legal

  // collect ### entries until the next ## (not ###)
  let i = start + 1;
  const entryStarts = [];
  for (; i < lines.length; i++) {
    const l = lines[i];
    if (/^##\s/.test(l) && !/^###/.test(l)) break; // next top section ends the log
    if (/^###\s/.test(l)) entryStarts.push(i);
  }
  const logEnd = i;

  for (let e = 0; e < entryStarts.length; e++) {
    const startLine = entryStarts[e];
    const endLine = e + 1 < entryStarts.length ? entryStarts[e + 1] : logEnd;
    const heading = lines[startLine];
    // grammar: ### YYYY-MM-DD [ (qualifier) ] — <headline>
    const hm = heading.match(/^###\s+(.+)$/);
    const rest = hm ? hm[1] : '';
    // the date is the FIRST YYYY-MM-DD-shaped token in the heading
    const dateTok = rest.match(/(\d{4}-\d{2}-\d{2})/);
    // A delta heading that carries a date-SHAPED token that is unparseable = MALFORMED (b).
    // Distinguish "delta heading" from an arbitrary ### by requiring a leading
    // date-shaped token (with optional parenthetical) then an em-dash headline,
    // OR a bare date. Headings with no date-shape at all are NOT delta entries
    // (absence, legal) — but inside SESSION-DELTA LOG every ### is expected to be one.
    const looksLikeDated = /^\d{4}-\d{2}-\d{2}/.test(rest.trim());
    if (looksLikeDated) {
      const cand = rest.trim().slice(0, 10);
      if (!isValidDate(cand)) {
        malformed(
          'delta-date',
          relPath,
          startLine + 1,
          `SESSION-DELTA heading has an unparseable date "${cand}": ${heading.trim()}`
        );
        continue;
      }
    } else if (dateTok && !isValidDate(dateTok[1])) {
      malformed(
        'delta-date',
        relPath,
        startLine + 1,
        `SESSION-DELTA heading date "${dateTok[1]}" is unparseable: ${heading.trim()}`
      );
      continue;
    } else if (!dateTok) {
      // a ### inside the log with no date at all — treat as prose sub-heading, skip (absence-legal)
      continue;
    }
    const date = dateTok ? dateTok[1] : rest.trim().slice(0, 10);
    // headline = everything after the first em-dash (— or --); else the rest post-date
    let headline;
    const dashIdx = rest.indexOf('—');
    if (dashIdx !== -1) headline = rest.slice(dashIdx + 1).trim();
    else headline = rest.replace(/^\d{4}-\d{2}-\d{2}/, '').trim();
    const bodyLines = lines.slice(startLine + 1, endLine);
    deltas.push({
      date,
      headline,
      body_md: bodyLines.join('\n').trim(),
      line: startLine + 1,
    });
  }
  return deltas;
}

// ---------------------------------------------------------------------------
// Shape 3 — Queue rows (§ 7.3), tables + modeled bullets.
// A "board" = one queue (one table, or one bullet-list group). Duplicate row
// IDs within one board = MALFORMED (c).
// ---------------------------------------------------------------------------
function currentHeading(lines, upto) {
  for (let i = upto; i >= 0; i--) {
    const m = lines[i].match(/^#{2,4}\s+(.*)$/);
    if (m) return { title: m[1].trim(), line: i + 1 };
  }
  return { title: '(untitled)', line: 1 };
}

function parseQueues(lines, relPath) {
  const queues = [];

  // -- Table queues --
  let i = 0;
  while (i < lines.length) {
    const cells = splitTableRow(lines[i]);
    // a table starts: header row, then a separator row
    if (cells && i + 1 < lines.length) {
      const sep = splitTableRow(lines[i + 1]);
      if (sep && isSeparatorRow(sep)) {
        const headerLine = i;
        const colCount = cells.length;
        // collect data rows
        const dataRows = [];
        let j = i + 2;
        for (; j < lines.length; j++) {
          const dcRaw = lines[j];
          if (!dcRaw.trim().startsWith('|')) break; // table ended
          const dc = splitTableRow(dcRaw);
          if (!dc) break;
          dataRows.push({ cells: dc, line: j + 1, raw: dcRaw });
        }
        // Does this table carry any ID-bearing rows? If not, it's not a queue → prose (absence-legal).
        const idRows = dataRows.filter((r) => extractRowId(r.cells[0]) !== null);
        if (idRows.length > 0) {
          const head = currentHeading(lines, headerLine - 1);
          const rows = [];
          const seenIds = new Map(); // id -> first line, for dup detection
          for (const r of dataRows) {
            const id = extractRowId(r.cells[0]);
            if (id === null) continue; // free-prose row inside a modeled table — skip (absence-legal)
            // MALFORMED (a): ID-bearing row whose column count != header column count
            if (r.cells.length !== colCount) {
              malformed(
                'row-structure',
                relPath,
                r.line,
                `Queue row "${id}" has ${r.cells.length} cells but its table header has ${colCount}: ${r.raw.trim().slice(0, 120)}`
              );
              continue;
            }
            // MALFORMED (c): duplicate row ID within this board
            if (seenIds.has(id)) {
              malformed(
                'duplicate-id',
                relPath,
                r.line,
                `Duplicate row ID "${id}" within one board (first seen at line ${seenIds.get(id)}): ${head.title}`
              );
              continue;
            }
            seenIds.set(id, r.line);
            const rowText = r.cells.join(' | ');
            const status = detectStatusFromCells(r.cells);
            rows.push({
              id,
              cells_md: r.cells,
              owner: extractOwner(r.cells),
              status,
              gates_on: extractGatesOn(rowText),
              line: r.line,
            });
          }
          if (rows.length > 0) {
            queues.push({ title: head.title, line: head.line, kind: 'table', rows });
          }
        }
        i = j;
        continue;
      }
    }
    i++;
  }

  // -- Bullet queues (§ 7.3: modeled iff bullet begins with a row ID followed by — or :) --
  // Group consecutive modeled bullets under their nearest heading into one board.
  let bIdx = 0;
  while (bIdx < lines.length) {
    const bm = lines[bIdx].match(/^\s*[-*]\s+(.*)$/);
    if (bm) {
      const content = stripInlineMd(bm[1]);
      const id = extractRowId(content);
      const afterId = id ? content.slice(content.indexOf(id.replace(/\s/, '')) ) : '';
      // require a — or : right after the id (per § 7.3)
      const modeled = id && /^[^—:]*[—:]/.test(afterId) === false
        ? // fallback: check the raw content right after id token
          new RegExp(`^${id.replace(/[.#]/g, '\\$&')}\\s*[—:]`).test(content.replace(/\s*#\s*/, '#'))
        : false;
      // simpler robust check:
      const modeled2 = id && new RegExp(`^\\**\\s*${id.replace(/[.#\\]/g, '\\$&')}\\s*[—:]`).test(content);
      if (id && modeled2) {
        // start a bullet board; consume consecutive modeled bullets
        const head = currentHeading(lines, bIdx - 1);
        const rows = [];
        const seenIds = new Map();
        let k = bIdx;
        for (; k < lines.length; k++) {
          const kb = lines[k].match(/^\s*[-*]\s+(.*)$/);
          if (!kb) {
            // allow blank lines within a bullet group? No — a blank breaks the group.
            if (lines[k].trim() === '') { continue; }
            break;
          }
          const kc = stripInlineMd(kb[1]);
          const kid = extractRowId(kc);
          const kmodeled = kid && new RegExp(`^\\**\\s*${kid.replace(/[.#\\]/g, '\\$&')}\\s*[—:]`).test(kc);
          if (!kid || !kmodeled) break;
          if (seenIds.has(kid)) {
            malformed('duplicate-id', relPath, k + 1,
              `Duplicate row ID "${kid}" within one bullet board: ${head.title}`);
            continue;
          }
          seenIds.set(kid, k + 1);
          // strip the leading "ID —" / "ID:" so a status token right after the
          // id is treated as cell-leading (bullets pack id+status in one cell).
          const afterKid = kc.replace(
            new RegExp(`^${kid.replace(/[.#\\]/g, '\\$&')}\\s*[—:]\\s*`), '');
          const status = detectStatusFromCells([afterKid]);
          rows.push({
            id: kid,
            cells_md: [kc],
            owner: extractOwner([kc]),
            status,
            gates_on: extractGatesOn(kb[1]),
            line: k + 1,
          });
        }
        if (rows.length > 0) {
          queues.push({ title: head.title, line: head.line, kind: 'bullet', rows });
        }
        bIdx = k;
        continue;
      }
    }
    bIdx++;
  }

  return queues;
}

// ---------------------------------------------------------------------------
// Counters (§3)
// ---------------------------------------------------------------------------
function tallyCounters(queues) {
  const c = { open: 0, in_flight: 0, blocked: 0, awaiting_ruling: 0, parked: 0, closed: 0 };
  for (const q of queues) {
    for (const r of q.rows) {
      const t = r.status.token;
      if (t in c) c[t] += 1;
    }
  }
  return c;
}

// ---------------------------------------------------------------------------
// Tracker parse
// ---------------------------------------------------------------------------
const TRACKERS = [
  { id: 'engine', file: 'current-to-end-state-engine.md' },
  { id: 'story', file: 'current-to-end-state-story.md' },
  { id: 'game', file: 'current-to-end-state-game.md' },
  { id: 'serial-content-emission', file: 'current-to-end-state-serial-content-emission.md' },
  // v1.3 §7.2 — the surface-ledger joins the modeled set as the FIFTH Tier-0 card.
  // "Not a fifth tracker" editorially, but structurally it IS one more entry in the
  // tracker glob (the parser doesn't care about the editorial distinction).
  { id: 'surface-ledger', file: 'surface-ledger.md', ledger: true },
];

function parseTracker(t) {
  const relPath = `canonical/current-to-end-state/${t.file}`;
  const abs = join(CANON, 'current-to-end-state', t.file);
  if (!existsSync(abs)) {
    malformed('missing-tracker', relPath, 0, `Tracker file not found: ${relPath}`);
    return null;
  }
  const lines = readFileSync(abs, 'utf8').split('\n');
  const status_banner = parseStatusBanner(lines, relPath);
  const deltas = parseDeltaLog(lines, relPath);
  // §7.2: the ledger reuses the STATUS + SESSION-DELTA shapes identically, but its
  // queue tables carry two ledger-specific properties that the generic §2.3 parser
  // would mis-read (see parseLedgerQueues). Everything else is shared.
  const queues = t.ledger ? parseLedgerQueues(lines, relPath) : parseQueues(lines, relPath);
  const counters = tallyCounters(queues);
  const tracker = {
    id: t.id,
    path: relPath,
    status_banner,
    deltas,
    queues,
    counters,
  };
  if (t.ledger) tracker.surfaces_agreed = surfacesAgreed(queues);
  return tracker;
}

// ---------------------------------------------------------------------------
// §7.2 — surface-ledger queue parse.
//
// The ledger writes the SAME legislated shapes (§2.1 STATUS, §2.2 SESSION-DELTA,
// §2.3 status-prefixed rows, §2.4 gates-on, §2.7 FLOW), but its queue tables have
// two properties the generic §2.3 table parser does NOT handle correctly:
//
//  (1) THE STATUS LIVES IN THE LAST CELL (the "Matt gate" column), NOT the first
//      matching cell. §7.2 row-semantics: the prefix encodes Matt-agreement state
//      (✓ agreed · IN-FLIGHT executing · OPEN · ⚖ · ⛔ gate-bound). The ledger's
//      lifecycle rule is explicit: a ruled-FLIP row's Classification cell reads
//      "✓ RULED …" while its Matt-gate cell still reads IN-FLIGHT/OPEN — "status
//      tracks EXECUTION, ruling lives in the classification cell; Glance counters
//      must never claim queued work as executing." The generic left-to-right scan
//      would wrongly count row E10 (Classification "✓ RULED path (iii)", Matt gate
//      IN-FLIGHT) as closed. So: status = the LAST cell (Matt gate) only.
//
//  (2) A stray blank line inside the ENGINE table (after E1) splits it into two
//      markdown tables; the second has no header row of its own, so the generic
//      parser drops E2–E10 entirely. The ledger is a flat surface list under
//      section headings, so we collect EVERY row-ID-bearing table data row under
//      each section heading, tolerant of blank-line table splits — the ledger's
//      row IDs are its board grain, not its markdown table boundaries.
//
// This is ledger-scoped: the four trackers keep parseQueues() unchanged.
// ---------------------------------------------------------------------------
function statusFromGateCell(cellRaw) {
  const t = stripInlineMd(cellRaw);
  for (const { token, match } of STATUS_PREFIXES) {
    if (t.startsWith(match)) return { token, prose: t.slice(match.length).trim() };
  }
  if (t.startsWith('OPEN')) return { token: 'open', prose: t.slice(4).trim() };
  return { token: 'open', prose: '' }; // §2.3: no prefix = OPEN
}

function parseLedgerQueues(lines, relPath) {
  const queues = [];
  let current = null; // { title, line, rows, seenIds }

  const flushIf = () => {
    if (current && current.rows.length > 0) {
      queues.push({ title: current.title, line: current.line, kind: 'table', rows: current.rows });
    }
    current = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // A section heading opens a new board (## ENGINE surfaces, ## THE GATE, …).
    const h = line.match(/^#{2,4}\s+(.*)$/);
    if (h) {
      flushIf();
      // Only sections that will contain surface rows become boards; empty ones
      // are dropped by flushIf (rows.length === 0). Prime a candidate board.
      current = { title: h[1].trim(), line: i + 1, rows: [], seenIds: new Map() };
      continue;
    }
    if (!current) continue;

    const cells = splitTableRow(line);
    if (!cells || isSeparatorRow(cells)) continue; // header / separator / prose
    const id = extractRowId(cells[0]);
    if (id === null) continue; // header row or free-prose table row (absence-legal)

    // MALFORMED (c): duplicate row ID within one board (§2.6 rule 3).
    if (current.seenIds.has(id)) {
      malformed('duplicate-id', relPath, i + 1,
        `Duplicate row ID "${id}" within one ledger board (first seen at line ${current.seenIds.get(id)}): ${current.title}`);
      continue;
    }
    current.seenIds.set(id, i + 1);

    const rowText = cells.join(' | ');
    // §7.2 property (1): status = the Matt-gate column = the LAST cell.
    const status = statusFromGateCell(cells[cells.length - 1]);
    current.rows.push({
      id,
      cells_md: cells,
      owner: extractOwner(cells),
      status,
      gates_on: extractGatesOn(rowText),
      line: i + 1,
    });
  }
  flushIf();
  return queues;
}

// §5 header strip counter: "surfaces agreed ✓N / M" (the demo-gate number;
// GATE1 closes at N === M). Derived from the ledger's parsed rows — never
// hard-coded. The GATE1 row is the gate SINK, not a surface, so it is excluded
// from BOTH the numerator and the denominator (§7.2: GATE1 "closes when every
// row above reads ✓").
function surfacesAgreed(queues) {
  let agreed = 0;
  let total = 0;
  for (const q of queues) {
    for (const r of q.rows) {
      if (r.id === 'GATE1') continue;
      total += 1;
      if (r.status.token === 'closed') agreed += 1;
    }
  }
  return { agreed, total };
}

// ---------------------------------------------------------------------------
// Shape 5 — Matt queues (§ 7.5). README index; item = heading or table row
// carrying a Q-style ID; resolved = ~~strikethrough~~ or in a resolved section.
// ---------------------------------------------------------------------------
function parseMattQueue(dir) {
  const relPath = `canonical/${dir}/README.md`;
  const abs = join(CANON, dir, 'README.md');
  if (!existsSync(abs)) return []; // absence legal
  const lines = readFileSync(abs, 'utf8').split('\n');
  const items = [];
  const seen = new Set();

  // Track whether we're in a RESOLVED / DONE / appendix section.
  let resolvedSection = false;
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const sec = line.match(/^#{2,4}\s+(.*)$/);
    if (sec) {
      resolvedSection = /RESOLVED|DONE|APPENDIX|LINEAGE/i.test(sec[1]);
    }
    // table rows with a Q-style / T-style / ordinal ID in the first cell
    const cells = splitTableRow(line);
    if (cells && cells.length >= 2 && !isSeparatorRow(cells)) {
      const id = extractRowId(cells[0]);
      if (id && /^(Q|T)[0-9]+$/.test(id)) {
        const struck = /~~/.test(line);
        const title = stripInlineMd(cells[1]).slice(0, 200);
        if (!seen.has(id)) {
          seen.add(id);
          items.push({
            id,
            title,
            resolved: resolvedSection || struck,
            path: relPath,
            line: i + 1,
          });
        }
      }
    }
    // heading-carried or bullet-carried Q/T items (e.g. "- ~~**2026… Q5 …**~~")
    const struckBullet = line.match(/^\s*[-*]\s+~~(.*)~~/);
    if (struckBullet) {
      const qm = struckBullet[1].match(/\b(Q|T)([0-9]+)\b/);
      if (qm) {
        const id = qm[1] + qm[2];
        if (!seen.has(id)) {
          seen.add(id);
          items.push({
            id,
            title: stripInlineMd(struckBullet[1]).slice(0, 200),
            resolved: true,
            path: relPath,
            line: i + 1,
          });
        }
      }
    }
    i++;
  }
  return items;
}

// ---------------------------------------------------------------------------
// gates-on resolution + dangling collection (§ 7.4 / §3)
// A token "closes" when the row it resolves to reaches ✓ (closed). A token that
// resolves to NO row across all trackers = dangling (warning badge).
// ---------------------------------------------------------------------------
function resolveGates(trackers) {
  // build the id -> status map across all boards
  const idStatus = new Map();
  for (const tr of trackers) {
    for (const q of tr.queues) {
      for (const r of q.rows) {
        // last-writer-wins is fine; ids are meant to be board-unique
        if (!idStatus.has(r.id)) idStatus.set(r.id, r.status.token);
      }
    }
  }
  const dangling = [];
  for (const tr of trackers) {
    for (const q of tr.queues) {
      for (const r of q.rows) {
        for (const g of r.gates_on) {
          if (idStatus.has(g.token)) {
            g.resolved = idStatus.get(g.token) === 'closed';
          } else {
            g.resolved = false;
            g.dangling = true;
            dangling.push({
              token: g.token,
              row: r.id,
              path: tr.path,
              line: r.line,
            });
          }
        }
      }
    }
  }
  return dangling;
}

// ---------------------------------------------------------------------------
// last commit (§3) — commit provenance for the Tier-0 freshness signal.
//
// PRECEDENCE (deterministic, no LLM, no network):
//   1. Vercel build → read the injected build env vars as the PRIMARY source.
//      Vercel does NOT expose full .git history in the build working dir
//      (shallow/absent .git), so the git shell-out below returns nothing there.
//      When VERCEL_GIT_COMMIT_SHA is set we are in a Vercel build → use env vars.
//   2. Local / CLI build → full .git present → read via `git log`.
//
// Date subtlety: Vercel injects NO commit-DATE env var. "Age" is the whole point
// of the freshness signal, so last_commit.date must still populate. On a Vercel
// build we first try a git committer-date read (works if any git data exists);
// if that yields nothing we fall back to generated_at as an EXPLICIT build-time
// proxy, LABELED via date_is_build_time_proxy so the UI never silently claims a
// commit timestamp it does not have.
// ---------------------------------------------------------------------------
function gitCommitDateISO() {
  // committer date (ISO-8601) of HEAD, or null if git has no data.
  try {
    const out = execSync('git log -1 --format=%cI', {
      cwd: REPO_ROOT,
      encoding: 'utf8',
    }).trim();
    return out || null;
  } catch {
    return null;
  }
}

const COMMIT_FIELD_SEP = String.fromCharCode(0);

function lastCommitFromGit() {
  try {
    // NUL-delimited (%x00) so subjects containing spaces never break the split.
    const out = execSync('git log -1 --format=%H%x00%an%x00%aI%x00%s', {
      cwd: REPO_ROOT,
      encoding: 'utf8',
    }).trim();
    if (!out) return null;
    const [sha, author, date, subject] = out.split(COMMIT_FIELD_SEP);
    if (!sha) return null;
    return {
      sha,
      author: author || null,
      date: date || null,
      subject: subject || null,
      date_is_build_time_proxy: false,
    };
  } catch {
    return null;
  }
}

function lastCommitFromVercelEnv(generatedAtISO) {
  const sha = process.env.VERCEL_GIT_COMMIT_SHA;
  if (!sha) return null; // not a Vercel build
  const rawMsg = process.env.VERCEL_GIT_COMMIT_MESSAGE || '';
  const subject = rawMsg.split('\n')[0].trim() || null; // first line only
  const author =
    process.env.VERCEL_GIT_COMMIT_AUTHOR_NAME ||
    process.env.VERCEL_GIT_COMMIT_AUTHOR_LOGIN ||
    null;
  // Prefer a true commit timestamp if git happens to have it; else build-time proxy.
  const gitDate = gitCommitDateISO();
  return {
    sha,
    author,
    date: gitDate || generatedAtISO,
    subject,
    date_is_build_time_proxy: gitDate === null,
  };
}

function lastCommit(generatedAtISO) {
  // Precedence: Vercel env (when present) → git.
  return (
    lastCommitFromVercelEnv(generatedAtISO) ||
    lastCommitFromGit() || {
      sha: null,
      author: null,
      date: null,
      subject: null,
      date_is_build_time_proxy: false,
    }
  );
}

function repoSha() {
  // Same commit-provenance precedence: Vercel env SHA → git rev-parse.
  if (process.env.VERCEL_GIT_COMMIT_SHA) return process.env.VERCEL_GIT_COMMIT_SHA;
  try {
    return execSync('git rev-parse HEAD', { cwd: REPO_ROOT, encoding: 'utf8' }).trim() || null;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const trackers = [];
  for (const t of TRACKERS) {
    const parsed = parseTracker(t);
    if (parsed) trackers.push(parsed);
  }
  const dangling = resolveGates(trackers);
  const matt_decision_needed = parseMattQueue('matt_decision_needed');
  const matt_to_do = parseMattQueue('matt_to_do');

  const generatedAt = new Date().toISOString();
  // §5 header strip: surfaces-agreed counter (the demo-gate number) is derived
  // from the surface-ledger card. Absent if the ledger doesn't parse (absence-legal).
  const ledgerTracker = trackers.find((t) => t.id === 'surface-ledger');
  const surfaces_agreed = ledgerTracker?.surfaces_agreed ?? null;
  const state = {
    generated_at: generatedAt,
    repo_sha: repoSha(),
    gh_blob_base: GH_BLOB_BASE,
    last_commit: lastCommit(generatedAt),
    trackers,
    surfaces_agreed,
    matt_decision_needed,
    matt_to_do,
    dangling_gates: dangling,
  };

  // write state.json into the app's public dir so vite bundles it.
  // public/ may not exist on a fresh checkout (it holds only the gitignored
  // state.json, so git doesn't track the empty dir) — create it.
  const outDir = join(__dirname, '..', 'app', 'public');
  if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, 'state.json');
  writeFileSync(outPath, JSON.stringify(state, null, 2));

  const malformedFindings = findings.filter((f) => f.severity === 'MALFORMED');

  // Report banner
  console.log('── Glance parse ──────────────────────────────────────');
  console.log(`  trackers modeled : ${trackers.length}`);
  const rowCount = trackers.reduce(
    (n, tr) => n + tr.queues.reduce((m, q) => m + q.rows.length, 0), 0);
  console.log(`  queue rows       : ${rowCount}`);
  console.log(`  matt_decision    : ${matt_decision_needed.length} (open ${matt_decision_needed.filter((x) => !x.resolved).length})`);
  console.log(`  matt_to_do       : ${matt_to_do.length} (open ${matt_to_do.filter((x) => !x.resolved).length})`);
  console.log(`  surfaces agreed  : ${surfaces_agreed ? `✓${surfaces_agreed.agreed} / ${surfaces_agreed.total}` : '—'}`);
  console.log(`  dangling gates   : ${dangling.length}  (warnings, not failures)`);
  console.log(`  MALFORMED        : ${malformedFindings.length}`);
  console.log(`  state.json       : ${outPath}`);
  console.log('──────────────────────────────────────────────────────');

  if (dangling.length > 0) {
    console.log('\nDANGLING gates-on tokens (WARNING badges — not build failures):');
    for (const d of dangling) {
      console.log(`  ⚠  ${d.path}:${d.line}  row ${d.row}  gates-on: ${d.token}`);
    }
  }

  if (malformedFindings.length > 0) {
    console.log('\nMALFORMED findings (CI BUILD FAILURE — Discipline #60):');
    for (const f of malformedFindings) {
      console.log(`  ✗  ${f.path}:${f.line}  [${f.kind}]  ${f.message}`);
    }
    if (REPORT_MODE) {
      console.log('\n(report mode: full list above; exiting non-zero so CI is red)');
    }
    process.exit(1);
  }

  console.log('\n✓ parse GREEN — no malformed legislated shapes.');
  process.exit(0);
}

main();
