/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  // Allow development from other devices on the network
  allowedDevOrigins: ['192.168.4.157']
}

module.exports = nextConfig