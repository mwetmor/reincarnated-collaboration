// CorpusKit — the full per-kit "single source of truth" detail page (`#/corpus/:id`).
//
// Renders EVERY one of the 10 frozen sections for one kit (spec:
// 2026-07-20-glance-per-kit-join-spec.md): spine · mapping · mints_anchored · dockets ·
// atlas_group · lineage_enrichment · citations · verify_ledger · dossier (6 families) ·
// _row_counts. Static only — the kit JSON is a build-time asset (no DB / no server / no API).
//
// HONEST-GAP RENDERING (a feature, not a bug — this page is also a diagnostic for
// mechanical sparseness): empty mints_anchored → "none"; null atlas_group → "not placed";
// null lineage_enrichment → "not placed in roster_atlas"; abstained dossier rows → "source
// silent"; UNSUPPORTED verdicts → flagged. Quarantined citations + abstained dossier rows
// render VISUALLY FLAGGED (recorded-but-not-authoritative). Never an error, never a crash.

import { useMemo } from 'react';
import { useKitDetail } from '../hooks/useKits';
import { goKit } from './CorpusIndex';
import {
  DOSSIER_FAMILY_LABEL,
  DOSSIER_FAMILY_ORDER,
  displayGame,
  gradeTone,
  verdictTone,
  type Citation,
  type Docket,
  type DossierFamily,
  type DossierRow,
  type KitDetail,
  type KitMapping,
  type KitSpine,
  type MappingJson,
  type MintAnchored,
  type VerifyClaim,
} from '../data/kitTypes';

// ── small shared primitives ────────────────────────────────────────────────────────────

/** A section shell with a title + optional count + an "honest empty" fallback. */
function Section({
  title,
  count,
  emptyLabel,
  children,
  accent = 'slate',
}: {
  title: string;
  count?: number;
  emptyLabel?: string;
  children?: React.ReactNode;
  accent?: 'slate' | 'teal' | 'amber' | 'sky';
}) {
  const isEmpty = count === 0 || children == null;
  const bar =
    accent === 'teal'
      ? 'border-l-teal-700'
      : accent === 'amber'
        ? 'border-l-amber-700'
        : accent === 'sky'
          ? 'border-l-sky-700'
          : 'border-l-slate-700';
  return (
    <section className={`rounded-lg border border-slate-800 border-l-2 ${bar} bg-slate-900/40`}>
      <div className="flex items-baseline justify-between gap-2 border-b border-slate-800 px-3 py-2">
        <h2 className="text-sm font-semibold text-slate-200">{title}</h2>
        {count != null && (
          <span className="font-mono text-[0.65rem] text-slate-500">
            {count} {count === 1 ? 'row' : 'rows'}
          </span>
        )}
      </div>
      <div className="px-3 py-3">
        {isEmpty ? (
          <p className="text-xs italic text-slate-500">{emptyLabel ?? 'none'}</p>
        ) : (
          children
        )}
      </div>
    </section>
  );
}

/** A labeled key/value line (dt/dd style), value omitted when null/empty. */
function KV({ k, v }: { k: string; v: React.ReactNode }) {
  const empty =
    v == null || v === '' || (Array.isArray(v) && v.length === 0);
  return (
    <div className="flex flex-col gap-0.5 sm:flex-row sm:gap-2">
      <span className="shrink-0 text-[0.68rem] uppercase tracking-wide text-slate-500 sm:w-40">
        {k}
      </span>
      <span className="min-w-0 break-words text-xs text-slate-300">
        {empty ? <span className="italic text-slate-600">—</span> : v}
      </span>
    </div>
  );
}

/** External source link (folds long URLs). */
function SourceLink({ url }: { url: string | null }) {
  if (!url) return <span className="italic text-slate-600">no source url</span>;
  let label = url;
  try {
    label = new URL(url).host + new URL(url).pathname;
  } catch {
    /* keep raw */
  }
  return (
    <a
      href={url}
      target="_blank"
      rel="noreferrer"
      className="break-all font-mono text-[0.68rem] text-sky-500 hover:text-sky-300"
    >
      {label}
    </a>
  );
}

/** Anchor-quote block (the fetched-verbatim evidence). */
function AnchorQuote({ quote }: { quote: string | null }) {
  if (!quote) return null;
  return (
    <blockquote className="mt-1 border-l-2 border-slate-700 pl-2 text-[0.7rem] italic text-slate-400">
      “{quote}”
    </blockquote>
  );
}

/** A generic parsed-payload renderer: strings/numbers inline, objects/arrays as pretty JSON
 *  (never invented; just a faithful view of whatever the emission carried). */
function Payload({ value }: { value: unknown }) {
  if (value == null) return <span className="italic text-slate-600">null</span>;
  if (typeof value === 'string')
    return <span className="whitespace-pre-wrap text-xs text-slate-300">{value}</span>;
  if (typeof value === 'number' || typeof value === 'boolean')
    return <span className="text-xs text-slate-300">{String(value)}</span>;
  return (
    <pre className="max-h-80 overflow-auto rounded bg-slate-950/60 p-2 text-[0.68rem] leading-relaxed text-slate-300">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

// ── section 1 · spine ──────────────────────────────────────────────────────────────────

function ChipList({ items, empty }: { items: string[]; empty: string }) {
  if (!items.length) return <span className="text-xs italic text-slate-600">{empty}</span>;
  return (
    <span className="flex flex-wrap gap-1">
      {items.map((it) => (
        <span key={it} className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.65rem] text-slate-300">
          {it}
        </span>
      ))}
    </span>
  );
}

function SpineSection({ spine }: { spine: KitSpine }) {
  return (
    <Section title="Spine" accent="teal">
      <div className="space-y-1.5">
        <KV k="folk name" v={spine.folk_name} />
        <KV k="game" v={displayGame(spine.game)} />
        <KV k="tier / canon" v={[spine.tier, spine.canon_tier].filter(Boolean).join(' · ') || null} />
        <KV k="eras" v={spine.eras} />
        <KV k="gx" v={spine.gx} />
        <KV k="source" v={[spine.source, spine.provenance_tag].filter(Boolean).join(' · ') || null} />
        <KV k="source date" v={spine.source_date} />
        <KV k="lineage" v={spine.lineage} />
        <KV k="elements attested" v={<ChipList items={spine.elements_attested} empty="none attested" />} />
        <KV k="ailments attested" v={<ChipList items={spine.ailments_attested} empty="none attested" />} />
        <KV
          k="verify tally"
          v={
            <span className="flex flex-wrap gap-1">
              <span className="rounded border border-emerald-800 bg-emerald-950/30 px-1.5 py-0.5 text-[0.65rem] text-emerald-300">
                ✓ {spine.verify_confirmed ?? 0}
              </span>
              <span className="rounded border border-rose-800 bg-rose-950/30 px-1.5 py-0.5 text-[0.65rem] text-rose-300">
                ✗ {spine.verify_contradicted ?? 0}
              </span>
              <span className="rounded border border-amber-800 bg-amber-950/30 px-1.5 py-0.5 text-[0.65rem] text-amber-300">
                ? {spine.verify_unsupported ?? 0}
              </span>
            </span>
          }
        />
        {(spine.negative === 1 || spine.is_system === 1) && (
          <KV
            k="flags"
            v={
              <span className="flex gap-1">
                {spine.negative === 1 && (
                  <span className="rounded bg-rose-950/40 px-1.5 py-0.5 text-[0.65rem] text-rose-300">
                    negative
                  </span>
                )}
                {spine.is_system === 1 && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.65rem] text-slate-300">
                    system
                  </span>
                )}
              </span>
            }
          />
        )}
      </div>
    </Section>
  );
}

// ── section 2 · mapping ────────────────────────────────────────────────────────────────

function MappingJsonView({ mj }: { mj: MappingJson | string }) {
  if (typeof mj === 'string') {
    // non-JSON source left raw by the generator — show verbatim.
    return <Payload value={mj} />;
  }
  const skills = mj.skills ?? [];
  const t4 = mj.t4_doors ?? [];
  const lanes = mj.scaffold?.support_lanes ?? null;
  return (
    <div className="space-y-3">
      {mj.motion_frame && (
        <div>
          <div className="mb-1 text-[0.62rem] uppercase tracking-wide text-slate-500">Motion frame</div>
          <p className="whitespace-pre-wrap text-xs text-slate-300">{mj.motion_frame}</p>
        </div>
      )}

      {skills.length > 0 && (
        <div>
          <div className="mb-1 text-[0.62rem] uppercase tracking-wide text-slate-500">
            Skills ({skills.length})
          </div>
          <div className="space-y-2">
            {skills.map((s, i) => (
              <div key={i} className="rounded border border-slate-800 bg-slate-950/40 p-2">
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="text-xs font-semibold text-slate-200">
                    {s.source_skill ?? '(unnamed skill)'}
                  </span>
                  {s.geometry_value && (
                    <span className="rounded bg-teal-900/40 px-1.5 py-0.5 text-[0.6rem] text-teal-300">
                      {s.geometry_value}
                    </span>
                  )}
                  {s.element_primary && (
                    <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-300">
                      {s.element_primary}
                      {s.element_secondary ? `/${s.element_secondary}` : ''}
                    </span>
                  )}
                  {(s.ailments ?? []).map((a) => (
                    <span key={a} className="rounded bg-amber-900/30 px-1.5 py-0.5 text-[0.6rem] text-amber-300">
                      {a}
                    </span>
                  ))}
                </div>
                {s.delivery_notes && (
                  <p className="mt-1 whitespace-pre-wrap text-[0.72rem] leading-relaxed text-slate-400">
                    {s.delivery_notes}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {t4.length > 0 && (
        <div>
          <div className="mb-1 text-[0.62rem] uppercase tracking-wide text-slate-500">T4 doors</div>
          <span className="flex flex-wrap gap-1">
            {t4.map((d) => (
              <span key={d} className="rounded bg-sky-900/40 px-1.5 py-0.5 text-[0.62rem] text-sky-300">
                {d}
              </span>
            ))}
          </span>
        </div>
      )}

      {lanes && Object.keys(lanes).length > 0 && (
        <div>
          <div className="mb-1 text-[0.62rem] uppercase tracking-wide text-slate-500">Support lanes</div>
          <div className="space-y-1">
            {Object.entries(lanes).map(([lane, vals]) => (
              <div key={lane} className="flex flex-col gap-0.5 sm:flex-row sm:gap-2">
                <span className="shrink-0 text-[0.65rem] text-slate-500 sm:w-24">{lane}</span>
                <span className="text-[0.7rem] text-slate-400">{(vals ?? []).join(' · ')}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {mj.fidelity_notes && (
        <details className="text-xs">
          <summary className="cursor-pointer text-[0.7rem] text-slate-500 hover:text-slate-300">
            fidelity notes
          </summary>
          <p className="mt-1 whitespace-pre-wrap text-[0.72rem] leading-relaxed text-slate-400">
            {mj.fidelity_notes}
          </p>
        </details>
      )}
    </div>
  );
}

function MappingSection({ mapping }: { mapping: KitMapping | null }) {
  if (!mapping) {
    return <Section title="Mapping" emptyLabel="no mapping row (kit not mapped)" />;
  }
  return (
    <Section title="Mapping" accent="teal">
      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-1.5">
          {mapping.grade && (
            <span className={`rounded border px-1.5 py-0.5 text-[0.62rem] font-bold uppercase ${gradeTone(mapping.grade)}`}>
              {mapping.grade}
            </span>
          )}
          {mapping.terminal_state && (
            <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.62rem] text-slate-300">
              {mapping.terminal_state}
            </span>
          )}
          {mapping.mapping_provenance && (
            <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.62rem] text-slate-400">
              {mapping.mapping_provenance}
            </span>
          )}
        </div>
        {mapping.deviation_notes && (
          <div>
            <div className="mb-1 text-[0.62rem] uppercase tracking-wide text-slate-500">Deviation notes</div>
            <p className="whitespace-pre-wrap text-[0.72rem] leading-relaxed text-slate-400">
              {mapping.deviation_notes}
            </p>
          </div>
        )}
        {mapping.mapping_json != null && <MappingJsonView mj={mapping.mapping_json} />}
      </div>
    </Section>
  );
}

// ── section 3 · mints_anchored ─────────────────────────────────────────────────────────

function MintsSection({ mints }: { mints: MintAnchored[] }) {
  return (
    <Section
      title="Mints anchored"
      count={mints.length}
      emptyLabel="this kit forced no mints (source silent on new mechanics)"
      accent="amber"
    >
      {mints.length > 0 && (
        <div className="space-y-2">
          {mints.map((m) => (
            <div key={m.mint_id} className="rounded border border-slate-800 bg-slate-950/40 p-2">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="rounded bg-amber-900/40 px-1.5 py-0.5 text-[0.62rem] font-semibold text-amber-300">
                  mint #{m.mint_id}
                </span>
                {m.mint_class && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-300">
                    {m.mint_class}
                  </span>
                )}
                {m.evidence_tier && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-400">
                    {m.evidence_tier}
                  </span>
                )}
                <span
                  className={`rounded px-1.5 py-0.5 text-[0.6rem] ${
                    m.build_authorized === 1
                      ? 'bg-emerald-900/40 text-emerald-300'
                      : 'bg-slate-800 text-slate-500'
                  }`}
                >
                  {m.build_authorized === 1 ? 'build-authorized' : 'not build-authorized'}
                </span>
              </div>
              {m.description && (
                <p className="mt-1 whitespace-pre-wrap text-[0.72rem] leading-relaxed text-slate-400">
                  {m.description}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </Section>
  );
}

// ── section 4 · dockets ────────────────────────────────────────────────────────────────

function DocketsSection({ dockets }: { dockets: Docket[] }) {
  return (
    <Section
      title="Mechanic-gap dockets"
      count={dockets.length}
      emptyLabel="no gap dockets cite this kit"
      accent="amber"
    >
      {dockets.length > 0 && (
        <div className="space-y-2">
          {dockets.map((d) => (
            <div key={String(d.docket_id)} className="rounded border border-slate-800 bg-slate-950/40 p-2">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.62rem] font-semibold text-slate-200">
                  docket {String(d.docket_id)}
                </span>
                {d.mechanism_class && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-300">
                    {d.mechanism_class}
                  </span>
                )}
                {d.docket_family && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-400">
                    {d.docket_family}
                  </span>
                )}
                {d.status && (
                  <span className="rounded bg-sky-900/30 px-1.5 py-0.5 text-[0.6rem] text-sky-300">
                    {d.status}
                  </span>
                )}
              </div>
              {(d.destination || d.disposition) && (
                <p className="mt-1 text-[0.7rem] text-slate-400">
                  {[d.destination, d.disposition].filter(Boolean).join(' → ')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </Section>
  );
}

// ── section 5 · atlas_group ────────────────────────────────────────────────────────────

function AtlasGroupSection({ ag }: { ag: KitDetail['atlas_group'] }) {
  if (!ag) {
    return <Section title="Atlas group" emptyLabel="not placed in a plane group" accent="sky" />;
  }
  return (
    <Section title="Atlas group" accent="sky">
      <div className="space-y-1.5">
        <KV
          k="group"
          v={
            ag.group ? (
              <span className="rounded bg-sky-900/40 px-1.5 py-0.5 text-[0.68rem] font-semibold text-sky-300">
                {ag.group}
              </span>
            ) : null
          }
        />
        <KV k="rationale" v={ag.group_intent_rationale} />
      </div>
    </Section>
  );
}

// ── section 6 · lineage_enrichment ─────────────────────────────────────────────────────

function LineageSection({ lin }: { lin: KitDetail['lineage_enrichment'] }) {
  if (!lin || Object.keys(lin).length === 0) {
    return (
      <Section
        title="Lineage enrichment"
        emptyLabel="not placed in roster_atlas (corpus kit — expected)"
        accent="sky"
      />
    );
  }
  return (
    <Section title="Lineage enrichment" accent="sky">
      <div className="space-y-1.5">
        {Object.entries(lin).map(([k, v]) => (
          <KV key={k} k={k} v={typeof v === 'object' && v !== null ? <Payload value={v} /> : (v as React.ReactNode)} />
        ))}
      </div>
    </Section>
  );
}

// ── section 7 · citations (quarantined flagged) ────────────────────────────────────────

function CitationRow({ c }: { c: Citation }) {
  const q = c.quarantined === 1;
  return (
    <div
      className={`rounded border p-2 ${
        q ? 'border-rose-800/60 bg-rose-950/20' : 'border-slate-800 bg-slate-950/40'
      }`}
    >
      <div className="flex flex-wrap items-center gap-1.5">
        {q && (
          <span className="rounded bg-rose-900/50 px-1.5 py-0.5 text-[0.6rem] font-bold uppercase text-rose-300">
            quarantined
          </span>
        )}
        {c.cite_class && (
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-300">
            {c.cite_class}
          </span>
        )}
        {c.rank_class && (
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-400">
            {c.rank_class}
          </span>
        )}
        {c.site && <span className="text-[0.65rem] text-slate-500">{c.site}</span>}
      </div>
      {c.title && <div className="mt-1 text-xs text-slate-300">{c.title}</div>}
      <div className="mt-0.5 flex flex-wrap items-center gap-2">
        <SourceLink url={c.url} />
        {c.archive_url && (
          <a
            href={c.archive_url}
            target="_blank"
            rel="noreferrer"
            className="text-[0.62rem] text-slate-500 hover:text-slate-300"
          >
            (archive)
          </a>
        )}
        {c.author_handle && <span className="text-[0.62rem] text-slate-500">@{c.author_handle}</span>}
      </div>
    </div>
  );
}

function CitationsSection({ citations }: { citations: Citation[] }) {
  const quarantined = citations.filter((c) => c.quarantined === 1).length;
  return (
    <Section title="Citations" count={citations.length} emptyLabel="no citations recorded">
      {citations.length > 0 && (
        <div className="space-y-2">
          {quarantined > 0 && (
            <p className="text-[0.65rem] text-rose-400/80">
              {quarantined} quarantined (recorded but not authoritative — flagged below)
            </p>
          )}
          {citations.map((c, i) => (
            <CitationRow key={(c.url ?? '') + i} c={c} />
          ))}
        </div>
      )}
    </Section>
  );
}

// ── section 8 · verify_ledger ──────────────────────────────────────────────────────────

function VerifySection({ claims }: { claims: VerifyClaim[] }) {
  return (
    <Section title="Verify ledger" count={claims.length} emptyLabel="no verify claims recorded">
      {claims.length > 0 && (
        <div className="space-y-2">
          {claims.map((v, i) => (
            <div key={i} className="rounded border border-slate-800 bg-slate-950/40 p-2">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className={`rounded border px-1.5 py-0.5 text-[0.6rem] font-bold uppercase ${verdictTone(v.verdict)}`}>
                  {v.verdict}
                </span>
                {v.claim_family && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-300">
                    {v.claim_family}
                  </span>
                )}
                {v.run_tag && <span className="text-[0.6rem] text-slate-500">{v.run_tag}</span>}
              </div>
              {v.claim_text && <p className="mt-1 text-[0.72rem] text-slate-300">{v.claim_text}</p>}
              {/* UNSUPPORTED claims commonly have a null anchor_quote — render honestly. */}
              {v.anchor_quote ? (
                <AnchorQuote quote={v.anchor_quote} />
              ) : (
                <p className="mt-1 text-[0.68rem] italic text-slate-600">no anchor quote</p>
              )}
              {v.source_url && (
                <div className="mt-1">
                  <SourceLink url={v.source_url} />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </Section>
  );
}

// ── section 9 · dossier (6 families; abstained flagged) ─────────────────────────────────

function DossierRowView({ row }: { row: DossierRow }) {
  const abstained = row.abstained === 1;
  if (abstained) {
    return (
      <div className="rounded border border-slate-800 border-dashed bg-slate-950/30 p-2">
        <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] font-semibold uppercase text-slate-400">
          source silent
        </span>
        <span className="ml-2 text-[0.68rem] italic text-slate-600">
          the source abstained on this family
          {row.conf != null ? ` (conf ${row.conf})` : ''}
        </span>
      </div>
    );
  }
  return (
    <div className="rounded border border-slate-800 bg-slate-950/40 p-2">
      <div className="mb-1 flex flex-wrap items-center gap-2">
        {row.conf != null && (
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.6rem] text-slate-400">
            conf {row.conf}
          </span>
        )}
        {row.source_url && <SourceLink url={row.source_url} />}
      </div>
      <Payload value={row.payload} />
      <AnchorQuote quote={row.anchor_quote} />
    </div>
  );
}

function DossierSection({ dossier }: { dossier: KitDetail['dossier'] }) {
  // Render the 6 canonical families in order; then any extra families the emission carries.
  const knownKeys = new Set<string>(DOSSIER_FAMILY_ORDER);
  const extraKeys = Object.keys(dossier).filter((k) => !knownKeys.has(k));
  const totalRows = Object.values(dossier).reduce((n, rows) => n + (rows?.length ?? 0), 0);

  const renderFamily = (family: string, label: string) => {
    const rows = dossier[family];
    return (
      <div key={family}>
        <div className="mb-1 flex items-baseline justify-between">
          <span className="text-[0.68rem] font-semibold uppercase tracking-wide text-slate-400">{label}</span>
          <span className="font-mono text-[0.6rem] text-slate-600">{rows?.length ?? 0}</span>
        </div>
        {rows && rows.length > 0 ? (
          <div className="space-y-1.5">
            {rows.map((r, i) => (
              <DossierRowView key={i} row={r} />
            ))}
          </div>
        ) : (
          <p className="text-[0.68rem] italic text-slate-600">no rows for this family</p>
        )}
      </div>
    );
  };

  return (
    <Section title="Dossier" count={totalRows} emptyLabel="no dossier rows recorded" accent="teal">
      {totalRows > 0 && (
        <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
          {DOSSIER_FAMILY_ORDER.map((f: DossierFamily) => renderFamily(f, DOSSIER_FAMILY_LABEL[f]))}
          {extraKeys.map((k) => renderFamily(k, k))}
        </div>
      )}
    </Section>
  );
}

// ── section 10 · _row_counts (the density header) ──────────────────────────────────────

function DensityHeader({ kit }: { kit: KitDetail }) {
  const rc = kit._row_counts;
  const cells: { label: string; n: number }[] = [
    { label: 'citations', n: rc.citations },
    { label: 'dossier facts', n: rc.dossier_facts },
    { label: 'verify claims', n: rc.verify_claims },
    { label: 'mints', n: rc.mints_anchored },
    { label: 'dockets', n: rc.dockets },
  ];
  return (
    <div className="grid grid-cols-3 gap-1.5 sm:grid-cols-5">
      {cells.map((c) => (
        <div
          key={c.label}
          className={`rounded-lg border p-2 text-center ${
            c.n > 0 ? 'border-slate-700 bg-slate-900/60' : 'border-slate-800 bg-slate-900/20'
          }`}
        >
          <div className={`text-lg font-bold tabular-nums ${c.n > 0 ? 'text-slate-100' : 'text-slate-600'}`}>
            {c.n}
          </div>
          <div className="text-[0.6rem] leading-tight text-slate-500">{c.label}</div>
        </div>
      ))}
    </div>
  );
}

// ── the page ───────────────────────────────────────────────────────────────────────────

export function CorpusKit({ id }: { id: string }) {
  const { kit, status, error } = useKitDetail(id);

  const title = useMemo(() => kit?.spine?.folk_name ?? id, [kit, id]);

  if (status === 'loading' || status === 'idle') {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-sky-500 border-t-transparent" />
          <p className="font-mono text-sm text-slate-500">Loading kit…</p>
        </div>
      </div>
    );
  }

  if (status === 'error' || !kit) {
    return (
      <div className="space-y-4">
        <BackLink />
        <div className="mx-auto max-w-2xl rounded-lg border border-rose-800/50 bg-rose-950/20 p-6 text-sm text-rose-300">
          <p className="font-semibold">Kit “{id}” not found.</p>
          <p className="mt-1 font-mono text-xs text-rose-400/80">{error ?? 'no such per-kit file'}</p>
          <p className="mt-3 text-xs text-slate-500">
            Per-kit files are staged at build time (public/kits/&lt;kit_id&gt;.json). Check the
            id, or return to the corpus index.
          </p>
        </div>
      </div>
    );
  }

  // The generator's honest "couldn't find in kit_master" marker.
  if (kit._error) {
    return (
      <div className="space-y-4">
        <BackLink />
        <div className="mx-auto max-w-2xl rounded-lg border border-amber-800/50 bg-amber-950/20 p-6 text-sm text-amber-300">
          <p className="font-semibold">Kit “{id}” has no spine.</p>
          <p className="mt-1 font-mono text-xs">{kit._error}</p>
        </div>
      </div>
    );
  }

  const spine = kit.spine;

  return (
    <div className="space-y-4">
      <BackLink />

      {/* header — folk name, id, top-line chips */}
      <div className="space-y-2">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h1 className="text-2xl font-bold text-slate-100">{title}</h1>
          <span className="font-mono text-xs text-slate-500">{kit.kit_id}</span>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="rounded bg-slate-800 px-2 py-0.5 text-[0.68rem] text-slate-300">
            {displayGame(spine.game)}
          </span>
          {spine.tier && (
            <span className="rounded bg-slate-800 px-2 py-0.5 text-[0.68rem] text-slate-300">{spine.tier}</span>
          )}
          {spine.grade && (
            <span className={`rounded border px-2 py-0.5 text-[0.68rem] font-bold uppercase ${gradeTone(spine.grade)}`}>
              {spine.grade}
            </span>
          )}
          {spine.terminal_state && (
            <span className="rounded bg-slate-800 px-2 py-0.5 text-[0.68rem] text-slate-300">
              {spine.terminal_state}
            </span>
          )}
        </div>
      </div>

      {/* section 10 (density) leads as the at-a-glance header */}
      <DensityHeader kit={kit} />

      {/* two-column section grid on wide; single column on mobile */}
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        <SpineSection spine={spine} />
        <MappingSection mapping={kit.mapping} />
        <MintsSection mints={kit.mints_anchored} />
        <DocketsSection dockets={kit.dockets} />
        <AtlasGroupSection ag={kit.atlas_group} />
        <LineageSection lin={kit.lineage_enrichment} />
        <CitationsSection citations={kit.citations} />
        <VerifySection claims={kit.verify_ledger} />
      </div>

      {/* dossier spans full width (6 families, dense) */}
      <DossierSection dossier={kit.dossier} />
    </div>
  );
}

function BackLink() {
  return (
    <button
      onClick={() => (window.location.hash = '#/corpus')}
      className="text-xs text-sky-500 hover:text-sky-300"
    >
      ← corpus index
    </button>
  );
}

// re-export goKit so callers importing from the detail module also get it (symmetry).
export { goKit };
