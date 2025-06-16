from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def location_keyboard(lang: str = "uz"):
    texts = {
        "uz": "📍 Joylashuvni yuborish",
        "ru": "📍 Отправить местоположение",
        "en": "📍 Send Location"
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=texts[lang], request_location=True)
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def contact_keyboard(lang: str = "uz"):
    texts = {
        "uz": "📞 Telefon raqamni yuborish",
        "ru": "📞 Отправить номер телефона", 
        "en": "📞 Send Phone Number"
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=texts[lang], request_contact=True)
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
