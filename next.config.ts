import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // youtubei.js loads protobuf definitions and the player script at runtime;
  // keep it out of the server bundle so Node resolves it as-is.
  serverExternalPackages: ['youtubei.js'],
};

export default nextConfig;
