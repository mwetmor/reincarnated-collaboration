// useAtlasSvg — fetches the Edition-III hooked SVG markup as TEXT for a given canvas.
//
// The Edition-III SVG is inlined into the page DOM (not rendered as <img>) so the
// page-injected highlight CSS and the selection JS can reach its layer groups
// (<g id="layer-live"> …) and per-mark data-el / data-kit / data-core hooks
// (spec §3, §4). The SVG is a print-grade static artifact and carries NO
// scripts inside it (renderer law §3.4) — inlining it is inert at rest.
//
// One file per SKIN; we look up the skin by resolving canvas->skin upstream, so
// this map is keyed by skin name only as the on-disk filename convention.
//
// v1.12 port (drax): re-homed from reincarnated-loadout into glance/app. Assets are
// resolved through import.meta.env.BASE_URL (glance's convention) and the vendored
// filenames upgraded Edition-II → Edition-III (the Matt-ruled re-home render).

import { useState, useEffect } from 'react';
import type { SkinName } from '../data/atlasTypes';

// Relative (no leading slash) so BASE_URL prefixing yields a well-formed URL.
const SVG_FOR_SKIN: Record<SkinName, string> = {
  archive: 'atlas/atlas-edition3-archive.svg', // DARK canvas — the black-copy lead
  instrument: 'atlas/atlas-edition3-instrument.svg', // LIGHT canvas
};

export type AtlasSvgStatus = 'idle' | 'loading' | 'success' | 'error';

export interface UseAtlasSvgResult {
  markup: string | null;
  status: AtlasSvgStatus;
  error: string | null;
}

// Cache per URL so flipping skins back and forth doesn't refetch 4.3MB each time.
const svgCache = new Map<string, string>();

export function useAtlasSvg(skin: SkinName | null): UseAtlasSvgResult {
  const [markup, setMarkup] = useState<string | null>(null);
  const [status, setStatus] = useState<AtlasSvgStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!skin) return;
    const url = `${import.meta.env.BASE_URL}${SVG_FOR_SKIN[skin]}`;

    const cached = svgCache.get(url);
    if (cached != null) {
      setMarkup(cached);
      setStatus('success');
      setError(null);
      return;
    }

    let cancelled = false;
    setStatus('loading');
    setError(null);
    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`);
        return res.text();
      })
      .then((text) => {
        if (cancelled) return;
        svgCache.set(url, text);
        setMarkup(text);
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
  }, [skin]);

  return { markup, status, error };
}
