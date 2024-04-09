import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:9090",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // set this to the frontend directory since build tool is in project root
  root: "./frontend",
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
