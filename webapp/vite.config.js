import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Dev server is pinned to port 3000 on purpose: the Django backend's
// CORS_ALLOWED_ORIGINS / CSRF_TRUSTED_ORIGINS in ecommerce/settings.py
// already whitelists http://localhost:3000, so nothing needs to change
// on the Django side to talk to this app locally.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
});
