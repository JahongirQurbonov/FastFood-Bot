#!/bin/bash

# 1. Git repository yaratish
git init
git add .
git commit -m "Initial commit: FastFood Telegram Bot"

# 2. GitHub repository bilan bog'lash
git remote add origin https://github.com/YOUR_USERNAME/fastfood-telegram-bot.git
git branch -M main
git push -u origin main

echo "✅ GitHub ga yuklandi!"
