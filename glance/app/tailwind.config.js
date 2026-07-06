/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  // Status-color classes are referenced dynamically; keep them from being purged.
  safelist: [
    'bg-emerald-500', 'bg-emerald-900/40', 'text-emerald-300', 'border-emerald-700',
    'bg-rose-500', 'bg-rose-900/40', 'text-rose-300', 'border-rose-700',
    'bg-amber-500', 'bg-amber-900/40', 'text-amber-300', 'border-amber-700',
    'bg-violet-500', 'bg-violet-900/40', 'text-violet-300', 'border-violet-700',
    'bg-sky-500', 'bg-sky-900/40', 'text-sky-300', 'border-sky-700',
    'bg-slate-500', 'bg-slate-800', 'text-slate-300', 'border-slate-600',
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
    },
  },
  plugins: [],
}
