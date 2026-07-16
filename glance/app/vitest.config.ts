/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';

// v1.12 (drax): the atlas port's unit suite (ported from reincarnated-loadout with the
// interactive Build-Horizon package). Kept as a SEPARATE vitest config (not folded into
// vite.config.ts) so the app's build plugin graph and the test runner stay independent —
// the same discipline the loadout seam used. node environment, explicit imports (no
// globals), matching the ported tests' `import { describe, it, expect } from 'vitest'`.
export default defineConfig({
  test: {
    environment: 'node',
    include: ['src/__tests__/**/*.test.ts'],
    globals: false,
  },
});
