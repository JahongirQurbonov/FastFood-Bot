from typing import Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from database.models import User as DBUser
from database.db import SessionLocal

class LocalizationMiddleware(BaseMiddleware):
    def __init__(self):
        self.translations = {
            "uz": {
                "welcome": "Xush kelibsiz! 🍔\n\nTilni tanlang:",
                "choose_language": "Tilni tanlang:",
                "language_set": "Til o'zbekcha qilib o'rnatildi ✅",
                "share_location": "📍 Iltimos, joylashuvingizni yuboring yoki manzilni kiriting:",
                "location_saved": "📍 Joylashuv saqlandi!",
                "main_menu": "🍔 Asosiy menyu",
                "order_food": "🛒 Ovqat buyurtma qilish",
                "my_orders": "📋 Mening buyurtmalarim",
                "settings": "⚙️ Sozlamalar",
                "contact": "📞 Aloqa",
                "order_success": "✅ Buyurtma muvaffaqiyatli yaratildi!\n\nBuyurtma raqami: #{order_id}",
                "payment_success": "✅ To'lov muvaffaqiyatli amalga oshirildi!",
                "subscribe_channels": "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                "check_subscription": "✅ Obunani tekshirish",
                "not_subscribed": "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!"
            },
            "ru": {
                "welcome": "Добро пожаловать! 🍔\n\nВыберите язык:",
                "choose_language": "Выберите язык:",
                "language_set": "Язык установлен на русский ✅",
                "share_location": "📍 Пожалуйста, отправьте ваше местоположение или введите адрес:",
                "location_saved": "📍 Местоположение сохранено!",
                "main_menu": "🍔 Главное меню",
                "order_food": "🛒 Заказать еду",
                "my_orders": "📋 Мои заказы",
                "settings": "⚙️ Настройки",
                "contact": "📞 Контакты",
                "order_success": "✅ Заказ успешно создан!\n\nНомер заказа: #{order_id}",
                "payment_success": "✅ Оплата прошла успешно!",
                "subscribe_channels": "Для использования бота подпишитесь на следующие каналы:",
                "check_subscription": "✅ Проверить подписку",
                "not_subscribed": "❌ Вы еще не подписались на все каналы!"
            },
            "en": {
                "welcome": "Welcome! 🍔\n\nChoose language:",
                "choose_language": "Choose language:",
                "language_set": "Language set to English ✅",
                "share_location": "📍 Please share your location or enter address:",
                "location_saved": "📍 Location saved!",
                "main_menu": "🍔 Main Menu",
                "order_food": "🛒 Order Food",
                "my_orders": "📋 My Orders",
                "settings": "⚙️ Settings",
                "contact": "📞 Contact",
                "order_success": "✅ Order created successfully!\n\nOrder ID: #{order_id}",
                "payment_success": "✅ Payment completed successfully!",
                "subscribe_channels": "To use the bot, subscribe to the following channels:",
                "check_subscription": "✅ Check Subscription",
                "not_subscribed": "❌ You haven't subscribed to all channels yet!"
            }
        }

    async def __call__(self, handler, event: TelegramObject, data: Dict[str, Any]):
        user: User = data.get("event_from_user")
        if user:
            db = SessionLocal()
            try:
                db_user = db.query(DBUser).filter(DBUser.telegram_id == user.id).first()
                if db_user:
                    data["lang"] = db_user.language
                    data["_"] = lambda key, **kwargs: self.translations.get(db_user.language, self.translations["uz"]).get(key, key).format(**kwargs)
                else:
                    data["lang"] = "uz"
                    data["_"] = lambda key, **kwargs: self.translations["uz"].get(key, key).format(**kwargs)
            finally:
                db.close()
        
        return await handler(event, data)
