from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.models import db
from keyboards.inline import get_menu_keyboard, get_item_keyboard, get_main_menu

router = Router()

@router.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    items = await db.get_menu_items()
    
    menu_text = """
🍽 <b>Bizning menyu</b>

Quyidagi mahsulotlardan birini tanlang:
    """
    
    await callback.message.edit_text(
        menu_text,
        reply_markup=get_menu_keyboard(items),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("item_"))
async def show_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    
    # Ma'lumotlar bazasidan mahsulot ma'lumotlarini olish
    items = await db.get_menu_items()
    item = None
    for i in items:
        if i[0] == item_id:
            item = i
            break
    
    if not item:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return
    
    item_id, name, name_uz, price, emoji, category, description = item
    
    item_text = f"""
{emoji} <b>{name_uz}</b>

💰 Narx: ${price}
📝 Tavsif: {description}
🏷 Kategoriya: {category.title()}

Nima qilmoqchisiz?
    """
    
    await callback.message.edit_text(
        item_text,
        reply_markup=get_item_keyboard(item_id),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id
    
    await db.add_to_cart(user_id, item_id)
    
    await callback.answer("✅ Mahsulot savatga qo'shildi!", show_alert=True)

@router.callback_query(F.data.startswith("buy_now_"))
async def buy_now(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    # Savatni tozalash va mahsulotni qo'shish
    await db.clear_cart(user_id)
    await db.add_to_cart(user_id, item_id)
    
    # To'g'ridan-to'g'ri checkout'ga o'tish
    await show_cart(callback, direct_checkout=True)

async def show_cart(callback: CallbackQuery, direct_checkout=False):
    user_id = callback.from_user.id
    cart_items = await db.get_cart(user_id)
    
    if not cart_items:
        await callback.answer("Savat bo'sh!", show_alert=True)
        return
    
    cart_text = "🛒 <b>Sizning savatiz:</b>\n\n"
    total = 0
    
    for name_uz, price, emoji, quantity, item_id in cart_items:
        item_total = price * quantity
        total += item_total
        cart_text += f"{emoji} {name_uz}\n"
        cart_text += f"   💰 ${price} x {quantity} = ${item_total:.2f}\n\n"
    
    cart_text += f"<b>💵 Jami: ${total:.2f}</b>"
    
    if direct_checkout:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="checkout")],
            [InlineKeyboardButton(text="🔙 Menyu", callback_data="menu")]
        ])
    else:
        from keyboards.inline import get_cart_keyboard
        keyboard = get_cart_keyboard()
    
    await callback.message.edit_text(
        cart_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
