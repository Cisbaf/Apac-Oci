import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: [
  'http://192.168.1.79:3000',
  'http://192.168.1.10:3000',
  // ... outros IPs da rede local se necessário
]
};

export default nextConfig;
