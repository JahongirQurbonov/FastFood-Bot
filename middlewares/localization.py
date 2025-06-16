from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class LocalizationMiddleware(BaseMiddleware):
    """Middleware for handling localization."""
    
    def __init__(self):
        self.translations = {
            'uz': {
                'welcome': 'Xush kelibsiz!',
                'order_received': 'Buyurtma qabul qilindi!',
                'error': 'Xatolik yuz berdi!'
            },
            'ru': {
                'welcome': 'Добро пожаловать!',
                'order_received': 'Заказ принят!',
                'error': 'Произошла ошибка!'
            },
            'en': {
                'welcome': 'Welcome!',
                'order_received': 'Order received!',
                'error': 'An error occurred!'
            }
        }
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Get user language
        user_lang = event.from_user.language_code or 'uz'
        if user_lang not in self.translations:
            user_lang = 'uz'
        
        # Add translations to data
        data['_'] = self.translations[user_lang]
        data['user_lang'] = user_lang
        
        return await handler(event, data)
