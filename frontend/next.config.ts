import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
    reactStrictMode: true,
    compress: true,
    poweredByHeader: false,
    productionBrowserSourceMaps: false,
    swcMinify: true,
}

export default nextConfig
