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
