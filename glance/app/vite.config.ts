import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Boring on purpose. Static SPA; state.json is emitted by the parser into
// public/ before build and served as a static asset.
export default defineConfig({
  plugins: [react()],
})
