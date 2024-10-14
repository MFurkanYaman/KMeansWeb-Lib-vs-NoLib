import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// });
export default defineConfig({
  server: {
    host: "0.0.0.0", // Docker içinde dışarıya açılmasını sağlar
    port: 5173, // Port ayarını doğru tanımla
    strictPort: true, // 5173 kullanılamazsa hata versin
  },
});
