import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api/bokeh-script': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true
      },
      '/static': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true
      },
      '/basic-plot': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      },
      '/velocity-model': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      },
      '/velan': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      },
      '/bandwidth': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      },
      '/frequency-heatmap': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      },
      '/fk': {
        target: 'http://localhost:5006',
        changeOrigin: true,
        xfwd: true,
        ws: true
      }
    }
  },
  ssr: {
    noExternal: ['@mui/*']
  },
  plugins: [
    tsConfigPaths({
      projects: ['./tsconfig.json']
    }),
    tanstackStart(),
    viteReact()
  ]
})
