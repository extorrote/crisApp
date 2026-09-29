import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],

    build: {
        outDir: 'crisapp/static/react/dist',
        emptyOutDir: true,

        rollupOptions: {
            input: 'crisapp/static/react/main.jsx',

            output: {
                entryFileNames: 'main.js',
                chunkFileNames: 'chunks/[name].js',
                assetFileNames: 'assets/[name][extname]',
            },
        },
    },
});