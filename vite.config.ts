import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // FastAPI backend
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/spellcheck': {
        target: 'http://localhost:8000', // FastAPI backend with MCP integration
        changeOrigin: true,
      },
      '/quality-checks': {
        target: 'http://localhost:8000', // FastAPI backend with comprehensive quality checks
        changeOrigin: true,
      },
      '/pipeline': {
        target: 'http://localhost:8001', // Pipeline backend with LangGraph
        changeOrigin: true,
      },
      '/manager': {
        target: 'http://localhost:8001', // Manager endpoints
        changeOrigin: true,
      },
    },
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  optimizeDeps: {
    include: ['pdfjs-dist'],
  },
  build: {
    rollupOptions: {
      external: [],
    },
  },
}));
