# FastFood Telegram Bot

O'zbek fastfood xizmatlari uchun ovqat buyurtma qilish Telegram boti.

## Xususiyatlar

- 🌐 Ko'p tillilik (O'zbek, Rus, Ingliz)
- 🛒 WebApp orqali ovqat buyurtma qilish
- 💳 Telegram Payments orqali to'lov
- 📱 Responsive dizayn
- 👨‍💻 Admin panel
- 📢 Majburiy obuna tizimi
- 📍 Geolokatsiya qo'llab-quvvatlash

## O'rnatish

### Backend (Bot)

1. Repository ni clone qiling:
\`\`\`bash
git clone <repository-url>
cd fastfood-telegram-bot
\`\`\`

2. Virtual environment yarating:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
\`\`\`

3. Dependencies o'rnating:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Environment variables o'rnating:
\`\`\`bash
cp .env.example .env
# .env faylini tahrirlang
\`\`\`

5. Database yarating:
\`\`\`bash
python scripts/seed_database.py
\`\`\`

6. Botni ishga tushiring:
\`\`\`bash
python main.py
\`\`\`

### Frontend (WebApp)

1. WebApp papkasiga o'ting:
\`\`\`bash
cd webapp
\`\`\`

2. Dependencies o'rnating:
\`\`\`bash
npm install
\`\`\`

3. Development server ishga tushiring:
\`\`\`bash
npm start
\`\`\`

4. Production build yarating:
\`\`\`bash
npm run build
\`\`\`

## Deploy qilish

### Backend
- VPS (DigitalOcean, Hetzner)
- Docker orqali deploy qilish mumkin

### Frontend
- Netlify yoki Vercel ga deploy qiling
- Build fayllarini upload qiling

## Konfiguratsiya

### Bot Token
1. @BotFather ga boring
2. Yangi bot yarating
3. Token ni `.env` fayliga qo'shing

### Payment Provider
1. Telegram Payments provider ro'yxatdan o'ting
2. Provider token ni oling
3. `.env` fayliga qo'shing

### Database
PostgreSQL database yarating va connection string ni `.env` ga qo'shing.

## Foydalanish

1. Botni ishga tushiring
2. `/start` buyrug'ini yuboring
3. Tilni tanlang
4. Joylashuvni yuboring
5. "Ovqat buyurtma qilish" tugmasini bosing
6. WebApp ochiladi
7. Ovqatlarni tanlang va buyurtma bering
8. To'lovni amalga oshiring

## Admin Panel

Admin bo'lish uchun `config.py` faylidagi `ADMIN_IDS` ro'yxatiga o'z Telegram ID ingizni qo'shing.

Admin buyruqlari:
- `/admin` - Admin panel

## Texnik ma'lumotlar

- **Backend**: Python 3.11, aiogram 3.x, SQLAlchemy, PostgreSQL
- **Frontend**: React 18, Framer Motion, TailwindCSS
- **Payments**: Telegram Payments API
- **Deployment**: Docker, VPS

## Litsenziya

MIT License
