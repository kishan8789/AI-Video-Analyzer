/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    compress: true,
    poweredByHeader: false,
    productionBrowserSourceMaps: false,
    swcMinify: true,

    eslint: {
        ignoreDuringBuilds: true,
    },
}

module.exports = nextConfig