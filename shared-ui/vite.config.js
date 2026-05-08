import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    dts({
      include: ['src'],
      insertTypesEntry: true,
    }),
  ],
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'shared-ui',
      formats: ['es', 'cjs'],
      fileName: (format, name) => {
        if (format === 'es')
          return `${name}.js`
        return `${name}.${format}`
      }
    },
    rollupOptions: {
      external: (id) => {
        console.log({ id })
        return id.includes('node_modules') ||
          id.includes('react') ||
          id.includes('_virtual') ||
          id.includes(0)
      },
      output: {
        preserveModules: true,
        preserveModulesRoot: 'src',
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
          '@mui/material': 'MaterialUI',
        },
      },
    },
  },
});
