// useKits — fetch the per-kit "single source of truth" static assets from public/kits/.
//
// SAME CONVENTION AS useAtlasData: static assets fetched at runtime through
// import.meta.env.BASE_URL (never bundled), no DB / no server / no API. The index is small
// (one thin row per kit); per-kit files are lazy-loaded only when a detail route mounts.
//
//   public/kits/index.json           → the browse/filter list
//   public/kits/<kit_id>.json        → the full per-kit object (10 sections)
//   public/kits/kits-provenance.json → the git-derived source stamp (footer)

import { useCallback, useEffect, useState } from 'react';
import type { KitDetail, KitIndexRow, KitsProvenance } from '../data/kitTypes';

export type LoadStatus = 'idle' | 'loading' | 'success' | 'error';

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`);
  return res.json() as Promise<T>;
}

export interface UseKitIndexResult {
  index: KitIndexRow[] | null;
  provenance: KitsProvenance | null;
  status: LoadStatus;
  error: string | null;
  refresh: () => void;
}

/** Load the thin index + provenance stamp. Provenance failure is non-fatal (index still
 *  renders); the index is the required payload. */
export function useKitIndex(): UseKitIndexResult {
  const [index, setIndex] = useState<KitIndexRow[] | null>(null);
  const [provenance, setProvenance] = useState<KitsProvenance | null>(null);
  const [status, setStatus] = useState<LoadStatus>('idle');
  const [error, setError] = useState<string | null>(null);
  const [rev, setRev] = useState(0);

  const refresh = useCallback(() => setRev((r) => r + 1), []);

  useEffect(() => {
    let cancelled = false;
    setStatus('loading');
    setError(null);
    const base = import.meta.env.BASE_URL;
    // provenance is best-effort — resolve() its rejection so a missing stamp never fails
    // the whole page.
    const provP = fetchJson<KitsProvenance>(`${base}kits/kits-provenance.json`).catch(
      () => null,
    );
    Promise.all([fetchJson<KitIndexRow[]>(`${base}kits/index.json`), provP])
      .then(([idx, prov]) => {
        if (cancelled) return;
        setIndex(idx);
        setProvenance(prov);
        setStatus('success');
      })
      .catch((e: unknown) => {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : String(e));
        setStatus('error');
      });
    return () => {
      cancelled = true;
    };
  }, [rev]);

  return { index, provenance, status, error, refresh };
}

export interface UseKitDetailResult {
  kit: KitDetail | null;
  status: LoadStatus;
  error: string | null;
}

/** Lazy-load ONE kit's full object by id (only when a detail route mounts). `id` null =
 *  idle (no fetch). A 404 surfaces as an error the page renders as "kit not found". */
export function useKitDetail(id: string | null): UseKitDetailResult {
  const [kit, setKit] = useState<KitDetail | null>(null);
  const [status, setStatus] = useState<LoadStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setKit(null);
      setStatus('idle');
      setError(null);
      return;
    }
    let cancelled = false;
    setStatus('loading');
    setError(null);
    setKit(null);
    const base = import.meta.env.BASE_URL;
    // encode the id for the URL but keep the underlying id untouched (render-faithful).
    fetchJson<KitDetail>(`${base}kits/${encodeURIComponent(id)}.json`)
      .then((k) => {
        if (cancelled) return;
        setKit(k);
        setStatus('success');
      })
      .catch((e: unknown) => {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : String(e));
        setStatus('error');
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  return { kit, status, error };
}
