import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    watch: {
      usePolling: true
    },
    hmr: {
      host: 'localhost'
    },
    allowedHosts: ['benimotomasyonum.com', 'api.benimotomasyonum.com']
  }
})