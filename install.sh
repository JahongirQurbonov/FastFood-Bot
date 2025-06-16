#!/bin/bash

echo "🚀 FastFood Bot o'rnatish boshlandi..."

# Virtual environment yaratish
echo "📦 Virtual environment yaratilmoqda..."
python3 -m venv venv

# Virtual environment faollashtirish
echo "🔧 Virtual environment faollashtirilmoqda..."
source venv/bin/activate

# Dependencies o'rnatish
echo "📚 Dependencies o'rnatilmoqda..."
pip install -r requirements.txt

# Database yaratish
echo "🗄️ Database yaratilmoqda..."
python3 -c "from database.db import create_tables; create_tables()"

echo "✅ O'rnatish tugallandi!"
echo "🔑 .env faylini yarating va kerakli tokenlarni kiriting:"
echo "BOT_TOKEN=your_bot_token_here"
echo "WEBAPP_URL=https://jahongirqurbonov.github.io/FastFood-Bot/"
echo "PAYMENT_TOKEN=your_payment_token_here"
echo "ADMIN_ID=your_admin_id_here"
echo ""
echo "🚀 Botni ishga tushirish uchun: python3 main.py"
