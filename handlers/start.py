from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
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
    
    # Inline keyboard yaratish
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🍔 Order Food",
                web_app=WebAppInfo(url=config.WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton(text="📞 Aloqa", callback_data="contact"),
            InlineKeyboardButton(text="ℹ️ Ma'lumot", callback_data="about")
        ]
    ])
    
    welcome_text = (
        f"Let's get started 🍟\n\n"
        f"Please tap the button below to order your perfect lunch!"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "contact")
async def contact_info(callback):
    """Show contact information."""
    contact_text = (
        "📞 <b>Aloqa ma'lumotlari:</b>\n\n"
        "📱 Telefon: +998 90 123 45 67\n"
        "📧 Email: info@fastfood.uz\n"
        "📍 Manzil: Toshkent sh., Chilonzor t.\n"
        "🕐 Ish vaqti: 24/7\n\n"
        "❓ Savollaringiz bo'lsa, bemalol murojaat qiling!"
    )
    
    await callback.message.edit_text(contact_text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "about")
async def about_info(callback):
    """Show information about the service."""
    about_text = (
        "ℹ️ <b>FastFood Bot haqida:</b>\n\n"
        "🍔 Bizning xizmatimiz orqali siz:\n"
        "• Tez va sifatli ovqat buyurtma qilishingiz mumkin\n"
        "• 30-45 daqiqada yetkazib beramiz\n"
        "• Naqd va online to'lov qabul qilamiz\n"
        "• 24/7 xizmat ko'rsatamiz\n\n"
        "🎯 <b>Bizning maqsadimiz:</b>\n"
        "Mijozlarimizga eng yaxshi xizmat ko'rsatish!"
    )
    
    await callback.message.edit_text(about_text, parse_mode="HTML")
    await callback.answer()