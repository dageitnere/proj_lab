import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      "/auth": "http://localhost:8000",
      "/menu": "http://localhost:8000",
      "/products": "http://localhost:8000",
      "/userProducts": "http://localhost:8000",
      "/profile": "http://localhost:8000",
      "/recipes": "http://localhost:8000",
      "/statistics": "http://localhost:8000",
      "/consumedProducts": "http://localhost:8000",
    },
  },
});