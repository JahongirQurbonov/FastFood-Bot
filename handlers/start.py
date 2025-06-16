from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.db import SessionLocal
from database.models import User as DBUser, RequiredChannel
from keyboards.inline import language_keyboard, main_menu_keyboard, subscription_keyboard
from keyboards.reply import location_keyboard
from services.subscription_checker import check_user_subscriptions

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(DBUser).filter(DBUser.telegram_id == message.from_user.id).first()
        
        if not user:
            # Create new user
            user = DBUser(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            db.add(user)
            db.commit()
            
            # Show language selection
            await message.answer(
                "Xush kelibsiz! 🍔\n\nTilni tanlang:\nДобро пожаловать! Выберите язык:\nWelcome! Choose language:",
                reply_markup=language_keyboard()
            )
        else:
            # Check required subscriptions
            required_channels = db.query(RequiredChannel).filter(RequiredChannel.is_active == True).all()
            
            if required_channels:
                subscribed = await check_user_subscriptions(message.bot, message.from_user.id, required_channels)
                if not subscribed:
                    lang = user.language
                    texts = {
                        "uz": "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                        "ru": "Для использования бота подпишитесь на следующие каналы:",
                        "en": "To use the bot, subscribe to the following channels:"
                    }
                    await message.answer(
                        texts[lang],
                        reply_markup=subscription_keyboard(required_channels, lang)
                    )
                    return
            
            # Show main menu
            if not user.latitude or not user.longitude:
                texts = {
                    "uz": "📍 Iltimos, joylashuvingizni yuboring:",
                    "ru": "📍 Пожалуйста, отправьте ваше местоположение:",
                    "en": "📍 Please share your location:"
                }
                await message.answer(
                    texts[user.language],
                    reply_markup=location_keyboard(user.language)
                )
            else:
                texts = {
                    "uz": f"Salom {user.first_name}! 🍔\n\nNima buyurtma qilmoqchisiz?",
                    "ru": f"Привет {user.first_name}! 🍔\n\nЧто хотите заказать?",
                    "en": f"Hello {user.first_name}! 🍔\n\nWhat would you like to order?"
                }
                await message.answer(
                    texts[user.language],
                    reply_markup=main_menu_keyboard(user.language)
                )
    finally:
        db.close()

@router.callback_query(F.data.startswith("lang_"))
async def language_callback(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.telegram_id == callback.from_user.id).first()
        if user:
            user.language = lang
            db.commit()
            
            texts = {
                "uz": "Til o'zbekcha qilib o'rnatildi ✅\n\n📍 Iltimos, joylashuvingizni yuboring:",
                "ru": "Язык установлен на русский ✅\n\n📍 Пожалуйста, отправьте ваше местоположение:",
                "en": "Language set to English ✅\n\n📍 Please share your location:"
            }
            
            await callback.message.edit_text(
                texts[lang],
                reply_markup=None
            )
            await callback.message.answer(
                texts[lang],
                reply_markup=location_keyboard(lang)
            )
    finally:
        db.close()
    
    await callback.answer()

@router.message(F.location)
async def location_handler(message: Message):
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.telegram_id == message.from_user.id).first()
        if user:
            user.latitude = message.location.latitude
            user.longitude = message.location.longitude
            db.commit()
            
            texts = {
                "uz": f"📍 Joylashuv saqlandi!\n\nSalom {user.first_name}! 🍔\n\nNima buyurtma qilmoqchisiz?",
                "ru": f"📍 Местоположение сохранено!\n\nПривет {user.first_name}! 🍔\n\nЧто хотите заказать?",
                "en": f"📍 Location saved!\n\nHello {user.first_name}! 🍔\n\nWhat would you like to order?"
            }
            
            await message.answer(
                texts[user.language],
                reply_markup=main_menu_keyboard(user.language)
            )
    finally:
        db.close()

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.telegram_id == callback.from_user.id).first()
        required_channels = db.query(RequiredChannel).filter(RequiredChannel.is_active == True).all()
        
        subscribed = await check_user_subscriptions(callback.bot, callback.from_user.id, required_channels)
        
        if subscribed:
            texts = {
                "uz": f"✅ Rahmat! Endi botdan foydalanishingiz mumkin.\n\nSalom {user.first_name}! 🍔",
                "ru": f"✅ Спасибо! Теперь вы можете пользоваться ботом.\n\nПривет {user.first_name}! 🍔",
                "en": f"✅ Thank you! Now you can use the bot.\n\nHello {user.first_name}! 🍔"
            }
            
            await callback.message.edit_text(
                texts[user.language],
                reply_markup=main_menu_keyboard(user.language)
            )
        else:
            texts = {
                "uz": "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!",
                "ru": "❌ Вы еще не подписались на все каналы!",
                "en": "❌ You haven't subscribed to all channels yet!"
            }
            await callback.answer(texts[user.language], show_alert=True)
    finally:
        db.close()
