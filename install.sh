#!/bin/bash

# 1. Loyihani clone qiling (yoki fayllarni yuklab oling)
git clone https://github.com/your-repo/fastfood-telegram-bot.git
cd fastfood-telegram-bot

# 2. Python virtual environment yarating
python3 -m venv venv

# Linux/Mac uchun:
source venv/bin/activate

# Windows uchun:
# venv\Scripts\activate

# 3. Python dependencies o'rnating
pip install -r requirements.txt

# 4. Node.js dependencies o'rnating (WebApp uchun)
cd webapp
npm install
cd ..

echo "✅ O'rnatish tugallandi!"
