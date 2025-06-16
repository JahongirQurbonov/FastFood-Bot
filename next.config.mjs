/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static export uchun
  output: 'export',
  
  // GitHub Pages uchun trailing slash
  trailingSlash: true,
  
  // Build vaqtida xatolarni e'tiborsiz qoldirish
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  
  // Rasmlarni optimizatsiya qilmaslik (GitHub Pages uchun)
  images: {
    unoptimized: true,
  },
  
  // Production uchun asset prefix va base path
  assetPrefix: process.env.NODE_ENV === 'production' ? '/FastFood-Bot' : '',
  basePath: process.env.NODE_ENV === 'production' ? '/FastFood-Bot' : '',
}

export default nextConfig