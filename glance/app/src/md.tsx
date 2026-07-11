import React from 'react';

// Minimal, deterministic inline-markdown renderer. NO html injection; we build
// React nodes by tokenizing. Handles: **bold**, `code`, ~~strike~~, *em*,
// [text](url), and bare urls. Good enough for cell prose + delta bodies.
// (Full CommonMark is out of scope — Glance renders canon prose faithfully but
//  it is not a markdown IDE.)

type Tok = { t: 'text' | 'bold' | 'code' | 'strike' | 'em' | 'link'; v: string; href?: string };

function tokenizeInline(src: string): Tok[] {
  const toks: Tok[] = [];
  let i = 0;
  const push = (t: Tok['t'], v: string, href?: string) => toks.push({ t, v, href });
  while (i < src.length) {
    // links [text](url)
    const link = /^\[([^\]]+)\]\(([^)]+)\)/.exec(src.slice(i));
    if (link) {
      push('link', link[1], link[2]);
      i += link[0].length;
      continue;
    }
    if (src.startsWith('**', i)) {
      const end = src.indexOf('**', i + 2);
      if (end !== -1) { push('bold', src.slice(i + 2, end)); i = end + 2; continue; }
    }
    if (src.startsWith('~~', i)) {
      const end = src.indexOf('~~', i + 2);
      if (end !== -1) { push('strike', src.slice(i + 2, end)); i = end + 2; continue; }
    }
    if (src[i] === '`') {
      const end = src.indexOf('`', i + 1);
      if (end !== -1) { push('code', src.slice(i + 1, end)); i = end + 1; continue; }
    }
    if (src[i] === '*') {
      const end = src.indexOf('*', i + 1);
      if (end !== -1 && end !== i + 1) { push('em', src.slice(i + 1, end)); i = end + 1; continue; }
    }
    // bare url
    const url = /^https?:\/\/[^\s)]+/.exec(src.slice(i));
    if (url) { push('link', url[0], url[0]); i += url[0].length; continue; }
    // plain char run until the next special
    let j = i + 1;
    while (j < src.length && !'*`~['.includes(src[j]) && !src.startsWith('http', j)) j++;
    push('text', src.slice(i, j));
    i = j;
  }
  return toks;
}

export function InlineMd({ src }: { src: string }): React.ReactElement {
  const toks = tokenizeInline(src);
  return (
    <>
      {toks.map((tk, idx) => {
        switch (tk.t) {
          case 'bold':
            return <strong key={idx} className="font-semibold text-slate-100">{tk.v}</strong>;
          case 'code':
            return <code key={idx} className="rounded bg-slate-800 px-1 py-0.5 font-mono text-[0.85em] text-sky-300">{tk.v}</code>;
          case 'strike':
            return <del key={idx} className="text-slate-500">{tk.v}</del>;
          case 'em':
            return <em key={idx} className="italic text-slate-300">{tk.v}</em>;
          case 'link':
            return (
              <a key={idx} href={tk.href} target="_blank" rel="noreferrer"
                 className="text-sky-400 underline decoration-sky-700 underline-offset-2 hover:text-sky-300">
                {tk.v}
              </a>
            );
          default:
            return <React.Fragment key={idx}>{tk.v}</React.Fragment>;
        }
      })}
    </>
  );
}

// Block-level: split delta bodies into paragraphs + simple bullet lists.
export function BlockMd({ src }: { src: string }): React.ReactElement {
  const lines = src.split('\n');
  const blocks: React.ReactElement[] = [];
  let para: string[] = [];
  let bullets: string[] = [];
  const flushPara = () => {
    if (para.length) {
      blocks.push(
        <p key={`p${blocks.length}`} className="mb-2 leading-relaxed">
          <InlineMd src={para.join(' ')} />
        </p>
      );
      para = [];
    }
  };
  const flushBullets = () => {
    if (bullets.length) {
      blocks.push(
        <ul key={`u${blocks.length}`} className="mb-2 ml-4 list-disc space-y-1">
          {bullets.map((b, i) => (
            <li key={i} className="leading-relaxed"><InlineMd src={b} /></li>
          ))}
        </ul>
      );
      bullets = [];
    }
  };
  for (const raw of lines) {
    const l = raw.trim();
    if (l === '') { flushPara(); flushBullets(); continue; }
    const bm = l.match(/^[-*]\s+(.*)$/);
    if (bm) { flushPara(); bullets.push(bm[1]); continue; }
    flushBullets();
    para.push(l);
  }
  flushPara();
  flushBullets();
  return <div>{blocks}</div>;
}

// ---------------------------------------------------------------------------
// SectionMd (§7.7 v1.9) — VERBATIM payload renderer for the reference-trio `## §N`
// sections. This is DISPLAY FIDELITY, not semantic parsing: it renders the raw
// markdown a Matt-facing doc already writes (tables, fenced blocks, blockquotes,
// bullets, prose) faithfully, so the lattice tables / resolver walkers / projection
// table appear as real tables — NOT flattened to prose (BlockMd's limit), and NOT
// interpreted into the state model (the parser never touches them). Deterministic;
// no LLM, no HTML injection — React nodes only.
//
// The payload is handed through untouched: a fenced block renders in a <pre>, a
// markdown table renders as an HTML <table>, everything else is BlockMd-class prose.
// ---------------------------------------------------------------------------
function isTableSep(line: string): boolean {
  const s = line.trim();
  if (!s.startsWith('|')) return false;
  const inner = s.replace(/^\|/, '').replace(/\|$/, '');
  return inner.split('|').every((c) => /^:?-{2,}:?$/.test(c.trim().replace(/\s/g, '')));
}
function splitRow(line: string): string[] {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
}

export function SectionMd({ src }: { src: string }): React.ReactElement {
  const lines = src.split('\n');
  const blocks: React.ReactElement[] = [];
  let para: string[] = [];
  let bullets: string[] = [];
  let quote: string[] = [];

  const flushPara = () => {
    if (para.length) {
      blocks.push(
        <p key={`p${blocks.length}`} className="mb-2 leading-relaxed text-slate-300">
          <InlineMd src={para.join(' ')} />
        </p>
      );
      para = [];
    }
  };
  const flushBullets = () => {
    if (bullets.length) {
      blocks.push(
        <ul key={`u${blocks.length}`} className="mb-3 ml-4 list-disc space-y-1 text-slate-300">
          {bullets.map((b, i) => (
            <li key={i} className="leading-relaxed"><InlineMd src={b} /></li>
          ))}
        </ul>
      );
      bullets = [];
    }
  };
  const flushQuote = () => {
    if (quote.length) {
      blocks.push(
        <blockquote key={`q${blocks.length}`} className="mb-3 border-l-2 border-slate-700 pl-3 text-sm italic text-slate-400">
          <InlineMd src={quote.join(' ')} />
        </blockquote>
      );
      quote = [];
    }
  };
  const flushAll = () => { flushPara(); flushBullets(); flushQuote(); };

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const l = raw.trim();

    // fenced code block — VERBATIM in a <pre> (the ASCII/fence payload).
    if (/^```/.test(l)) {
      flushAll();
      const body: string[] = [];
      let j = i + 1;
      for (; j < lines.length; j++) {
        if (/^```/.test(lines[j].trim())) break;
        body.push(lines[j]);
      }
      blocks.push(
        <pre key={`f${blocks.length}`} className="mb-3 overflow-x-auto rounded-lg border border-slate-800 bg-slate-950/70 p-3 text-[0.62rem] leading-tight text-slate-300 sm:text-[0.72rem]">
          {body.join('\n')}
        </pre>
      );
      i = j; // skip past the closing fence
      continue;
    }

    // markdown table — a `| … |` header row immediately followed by a separator row.
    if (l.startsWith('|') && i + 1 < lines.length && isTableSep(lines[i + 1])) {
      flushAll();
      const header = splitRow(l);
      const rows: string[][] = [];
      let j = i + 2;
      for (; j < lines.length; j++) {
        const rl = lines[j].trim();
        if (!rl.startsWith('|')) break;
        if (isTableSep(lines[j])) continue;
        rows.push(splitRow(rl));
      }
      blocks.push(
        <div key={`t${blocks.length}`} className="mb-3 overflow-x-auto">
          <table className="w-full border-collapse text-left text-xs">
            <thead>
              <tr className="border-b border-slate-700 text-[0.7rem] uppercase tracking-wide text-slate-500">
                {header.map((h, k) => (
                  <th key={k} className="py-1 pr-3 align-bottom font-semibold"><InlineMd src={h} /></th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={ri} className="border-b border-slate-800/60 align-top">
                  {r.map((c, ci) => (
                    <td key={ci} className="py-1.5 pr-3 text-slate-300"><InlineMd src={c} /></td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      i = j - 1;
      continue;
    }

    if (l === '') { flushAll(); continue; }

    // blockquote line
    const qm = l.match(/^>\s?(.*)$/);
    if (qm) { flushPara(); flushBullets(); quote.push(qm[1]); continue; }
    flushQuote();

    // bullet line
    const bm = l.match(/^[-*]\s+(.*)$/);
    if (bm) { flushPara(); bullets.push(bm[1]); continue; }
    flushBullets();

    para.push(l);
  }
  flushAll();
  return <div>{blocks}</div>;
}
