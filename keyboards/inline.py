from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import config

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Menyu", web_app=WebAppInfo(url=config.WEBAPP_URL))],
        [InlineKeyboardButton(text="🛒 Savat", callback_data="cart")],
        [InlineKeyboardButton(text="📋 Buyurtmalarim", callback_data="my_orders")],
        [InlineKeyboardButton(text="ℹ️ Ma'lumot", callback_data="info")]
    ])
    return keyboard

def get_menu_keyboard(items):
    keyboard = []
    row = []
    
    for i, item in enumerate(items):
        item_id, name, name_uz, price, emoji, category, description = item
        
        button_text = f"{emoji} {name_uz} - ${price}"
        callback_data = f"item_{item_id}"
        
        row.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))
        
        # 2 ta button har qatorda
        if len(row) == 2 or i == len(items) - 1:
            keyboard.append(row)
            row = []
    
    # Orqaga qaytish tugmasi
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_item_keyboard(item_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"add_to_cart_{item_id}"),
            InlineKeyboardButton(text="💰 Sotib olish", callback_data=f"buy_now_{item_id}")
        ],
        [InlineKeyboardButton(text="🔙 Menyu", callback_data="menu")]
    ])
    return keyboard

def get_cart_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="checkout")],
        [InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="clear_cart")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
    ])
    return keyboard

def get_checkout_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 To'lash", callback_data="payment")],
        [InlineKeyboardButton(text="🔙 Savatga qaytish", callback_data="cart")]
    ])
    return keyboard

def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
        ],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")]
    ])
    return keyboard
