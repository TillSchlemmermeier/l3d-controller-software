import { defineConfig } from 'vite'
import path from 'node:path'
import electron from 'vite-plugin-electron/simple'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    electron({
      main: {
        entry: 'electron/main.ts',
        vite: {
          build: {
            rollupOptions: {
              external: ['bufferutil', 'utf-8-validate'],
            },
          },
        }
      },
      preload: {
        input: path.join(__dirname, 'electron/preload.ts'),
      },
      // Ployfill the Electron and Node.js API for Renderer process.
      // If you want use Node.js in Renderer process, the `nodeIntegration` needs to be enabled in the Main process.
      // See 👉 https://github.com/electron-vite/vite-plugin-electron-renderer
      renderer: process.env.NODE_ENV === 'test'
        // https://github.com/electron-vite/vite-plugin-electron-renderer/issues/78#issuecomment-2053600808
        ? undefined
        : {},
    }),
  ],
  server: {
    watch: {
      ignored: [
        '**/assets/previews/**',  // Ignore preview GIFs
        '**/*.db',  // ignore database files
        '**/*.pkl',  // ignore pickle files
        '**/*.log',  // ignore log files
        '**/*.py',  // ignore python files
        '**/*.txt',  // ignore text files
        '**/core/**',  // ignore core files
        path.resolve(__dirname, 'mobile') + '/**',  // ignore mobile files
      ]
    },
    // hmr: false,  // Disable HMR completely
  },
})
