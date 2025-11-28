/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Cloudflare Pages 配置
  output: 'standalone',
  // 如果需要使用 Cloudflare Workers，取消下面的注释
  // experimental: {
  //   runtime: 'edge',
  // },
}

module.exports = nextConfig

