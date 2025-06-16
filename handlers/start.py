from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from database.db import Database
from config import config

router = Router()
db = Database()

@router.message(CommandStart())
async def start_command(message: Message):
    """Handle /start command."""
    
    # Save user to database
    user = message.from_user
    db.execute_query("""
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, language_code)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, user.username, user.first_name, user.last_name, user.language_code or 'uz'))
    
    # WebApp tugmasi bilan keyboard yaratish
    webapp_button = KeyboardButton(
        text="🍔 Ovqat buyurtma qilish",
        web_app=WebAppInfo(url=config.WEBAPP_URL)
    )
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [webapp_button],
            [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="ℹ️ Ma'lumot")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    welcome_text = (
        f"🍔 <b>Salom, {user.first_name}!</b>\n\n"
        f"<b>FastFood Bot-ga xush kelibsiz!</b>\n\n"
        f"Bizning bot orqali siz:\n"
        f"• 🚀 Tez va oson buyurtma bera olasiz\n"
        f"• 🍕 Turli xil taomlarni tanlashingiz mumkin\n"
        f"• 🏠 Uyingizgacha yetkazib beramiz\n"
        f"• 💳 Online to'lov qilishingiz mumkin\n\n"
        f"Buyurtma berish uchun quyidagi tugmani bosing:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.message(F.text == "📞 Aloqa")
async def contact_info(message: Message):
    """Show contact information."""
    contact_text = (
        "📞 <b>Aloqa ma'lumotlari:</b>\n\n"
        "📱 Telefon: +998 90 123 45 67\n"
        "📧 Email: info@fastfood.uz\n"
        "📍 Manzil: Toshkent sh., Chilonzor t.\n"
        "🕐 Ish vaqti: 24/7\n\n"
        "❓ Savollaringiz bo'lsa, bemalol murojaat qiling!"
    )
    
    await message.answer(contact_text, parse_mode="HTML")

@router.message(F.text == "ℹ️ Ma'lumot")
async def about_info(message: Message):
    """Show information about the service."""
    about_text = (
        "ℹ️ <b>FastFood Bot haqida:</b>\n\n"
        "🍔 Bizning xizmatimiz orqali siz:\n"
        "• Tez va sifatli ovqat buyurtma qilishingiz mumkin\n"
        "• 30-45 daqiqada yetkazib beramiz\n"
        "• Naqd va online to'lov qabul qilamiz\n"
        "• 24/7 xizmat ko'rsatamiz\n\n"
        "🎯 <b>Bizning maqsadimiz:</b>\n"
        "Mijozlarimizga eng yaxshi xizmat ko'rsatish va\n"
        "mazali taomlar bilan ta'minlash!\n\n"
        "🚀 Bot versiyasi: 2.0\n"
        "👨‍💻 Ishlab chiquvchi: @JahongirQurbonov"
    )
    
    await message.answer(about_text, parse_mode="HTML")

@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Show admin panel for authorized users."""
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("❌ Sizda admin huquqlari yo'q!")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="admin_orders")],
        [InlineKeyboardButton(text="🍔 Menyu boshqaruvi", callback_data="admin_menu")],
    ])
    
    await message.answer(
        "🔧 <b>Admin Panel</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
