// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/auth": "http://localhost:8000",
      "/menu": "http://localhost:8000",
      "/products": "http://localhost:8000",
      "/userProducts": "http://localhost:8000",
      "/profile": "http://localhost:8000",
    },
  },
});
