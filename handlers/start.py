from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.inline import get_main_menu, get_language_keyboard
from database.models import db
from config import config

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    user = message.from_user
    
    # Foydalanuvchini bazaga qo'shish
    await db.add_user(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name
    )
    
    welcome_text = f"""
🍔 <b>Durger King</b> ga xush kelibsiz!

Salom {user.full_name}! 👋

Bizning bot orqali:
🍽 Menyu ko'rish
🛒 Buyurtma berish  
🚚 Yetkazib berish xizmati
💳 Onlayn to'lov

Quyidagi tugmalardan birini tanlang:
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    welcome_text = """
🍔 <b>Durger King</b>

Quyidagi tugmalardan birini tanlang:
    """
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "info")
async def show_info(callback: CallbackQuery):
    info_text = """
ℹ️ <b>Durger King haqida</b>

🕐 Ish vaqti: 24/7
📞 Telefon: +998 90 123 45 67
📍 Manzil: Toshkent sh., Amir Temur ko'chasi
🚚 Yetkazib berish: Bepul (25$ dan yuqori)
💳 To'lov: Naqd, Karta, Click, Payme

<b>Bizning afzalliklarimiz:</b>
✅ Tez yetkazib berish (30 daqiqa)
✅ Yangi mahsulotlar
✅ Sifatli xizmat
✅ Qulay narxlar
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(
        info_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
