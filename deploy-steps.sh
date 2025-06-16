#!/bin/bash

echo "🚀 FastFood Bot deploy qilish..."

# Git repository yangilash
echo "📦 Git repository yangilanmoqda..."
git add .
git commit -m "Update FastFood Bot"
git push origin main

# WebApp deploy qilish
echo "🌐 WebApp deploy qilinmoqda..."
cd webapp
npm run build
git add .
git commit -m "Deploy WebApp"
git push -f origin gh-pages

echo "✅ Deploy tugallandi!"
echo "🔗 WebApp URL: https://jahongirqurbonov.github.io/FastFood-Bot/"
