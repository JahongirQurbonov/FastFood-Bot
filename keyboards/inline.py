from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config

def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
    )
    return builder.as_markup()

def main_menu_keyboard(lang: str = "uz"):
    texts = {
        "uz": {
            "order": "🛒 Ovqat buyurtma qilish",
            "orders": "📋 Buyurtmalarim",
            "settings": "⚙️ Sozlamalar",
            "contact": "📞 Aloqa"
        },
        "ru": {
            "order": "🛒 Заказать еду",
            "orders": "📋 Мои заказы", 
            "settings": "⚙️ Настройки",
            "contact": "📞 Контакты"
        },
        "en": {
            "order": "🛒 Order Food",
            "orders": "📋 My Orders",
            "settings": "⚙️ Settings", 
            "contact": "📞 Contact"
        }
    }
    
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=texts[lang]["order"],
            web_app=WebAppInfo(url=f"{config.WEBAPP_URL}?lang={lang}")
        )
    )
    builder.row(
        InlineKeyboardButton(text=texts[lang]["orders"], callback_data="my_orders"),
        InlineKeyboardButton(text=texts[lang]["settings"], callback_data="settings")
    )
    builder.row(
        InlineKeyboardButton(text=texts[lang]["contact"], callback_data="contact")
    )
    return builder.as_markup()

def subscription_keyboard(channels, lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    
    for channel in channels:
        builder.row(
            InlineKeyboardButton(
                text=f"📢 {channel.channel_name}",
                url=f"https://t.me/{channel.channel_id.replace('@', '')}"
            )
        )
    
    check_text = {
        "uz": "✅ Obunani tekshirish",
        "ru": "✅ Проверить подписку", 
        "en": "✅ Check Subscription"
    }
    
    builder.row(
        InlineKeyboardButton(text=check_text[lang], callback_data="check_subscription")
    )
    
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
        InlineKeyboardButton(text="🍔 Mahsulotlar", callback_data="admin_products")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Kanallar", callback_data="admin_channels"),
        InlineKeyboardButton(text="💳 To'lov", callback_data="admin_payments")
    )
    return builder.as_markup()
