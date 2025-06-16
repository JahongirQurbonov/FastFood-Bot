from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import db
from keyboards.inline import get_cart_keyboard, get_checkout_keyboard

router = Router()

class OrderStates(StatesGroup):
    waiting_for_address = State()
    waiting_for_phone = State()

@router.callback_query(F.data == "cart")
async def show_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    cart_items = await db.get_cart(user_id)
    
    if not cart_items:
        empty_text = """
🛒 <b>Savat bo'sh</b>

Mahsulot qo'shish uchun menyuga o'ting.
        """
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🍽 Menyu", callback_data="menu")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ])
        
        await callback.message.edit_text(
            empty_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    cart_text = "🛒 <b>Sizning savatiz:</b>\n\n"
    total = 0
    
    for name_uz, price, emoji, quantity, item_id in cart_items:
        item_total = price * quantity
        total += item_total
        cart_text += f"{emoji} <b>{name_uz}</b>\n"
        cart_text += f"   💰 ${price} x {quantity} = <b>${item_total:.2f}</b>\n\n"
    
    delivery_fee = 0.00 if total >= 25 else 2.99
    final_total = total + delivery_fee
    
    cart_text += f"🍽 Mahsulotlar: <b>${total:.2f}</b>\n"
    cart_text += f"🚚 Yetkazib berish: <b>${delivery_fee:.2f}</b>\n"
    cart_text += f"━━━━━━━━━━━━━━━━━━━━\n"
    cart_text += f"💵 <b>Jami: ${final_total:.2f}</b>"
    
    await callback.message.edit_text(
        cart_text,
        reply_markup=get_cart_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    await db.clear_cart(user_id)
    
    await callback.answer("🗑 Savat tozalandi!", show_alert=True)
    await show_cart(callback)

@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart_items = await db.get_cart(user_id)
    
    if not cart_items:
        await callback.answer("Savat bo'sh!", show_alert=True)
        return
    
    # Buyurtma ma'lumotlarini hisoblash
    total = sum(price * quantity for _, price, _, quantity, _ in cart_items)
    delivery_fee = 0.00 if total >= 25 else 2.99
    final_total = total + delivery_fee
    
    # Order raqamini yaratish
    import random
    order_number = f"#{random.randint(100000000, 999999999)}"
    
    # Buyurtma ma'lumotlarini state'ga saqlash
    await state.update_data(
        cart_items=cart_items,
        total=total,
        delivery_fee=delivery_fee,
        final_total=final_total,
        order_number=order_number
    )
    
    checkout_text = f"""
📋 <b>Buyurtma tasdiqlanmoqda</b>

🏪 <b>Durger King</b>
📦 Buyurtma: {order_number}

"""
    
    for name_uz, price, emoji, quantity, item_id in cart_items:
        item_total = price * quantity
        checkout_text += f"{emoji} <b>{name_uz}</b> x{quantity} - ${item_total:.2f}\n"
    
    checkout_text += f"""
━━━━━━━━━━━━━━━━━━━━
🍽 Mahsulotlar: ${total:.2f}
🚚 Yetkazib berish: ${delivery_fee:.2f}

💵 <b>Jami: ${final_total:.2f}</b>

📍 Yetkazib berish manzilini yuboring:
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Savatga qaytish", callback_data="cart")]
    ])
    
    await callback.message.edit_text(
        checkout_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await state.set_state(OrderStates.waiting_for_address)
    await callback.answer()

@router.message(OrderStates.waiting_for_address)
async def process_address(message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    
    data = await state.get_data()
    order_number = data['order_number']
    final_total = data['final_total']
    
    phone_text = f"""
📋 <b>Buyurtma: {order_number}</b>

✅ Manzil qabul qilindi:
📍 {address}

📞 Endi telefon raqamingizni yuboring:
(Masalan: +998 90 123 45 67)
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cart")]
    ])
    
    await message.answer(
        phone_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await state.set_state(OrderStates.waiting_for_phone)

@router.message(OrderStates.waiting_for_phone)
async def process_phone(message, state: FSMContext):
    phone = message.text
    data = await state.get_data()
    
    # Buyurtmani bazaga saqlash
    order_data = {
        'items': data['cart_items'],
        'total': data['final_total'],
        'address': data['address'],
        'phone': phone
    }
    
    order_number = await db.create_order(message.from_user.id, order_data)
    
    # Savatni tozalash
    await db.clear_cart(message.from_user.id)
    
    # Buyurtma tasdiqlanishi
    confirmation_text = f"""
✅ <b>Buyurtma qabul qilindi!</b>

🏪 <b>Durger King</b>
📦 Buyurtma: {order_number}
💰 Jami: ${data['final_total']:.2f}

📍 Manzil: {data['address']}
📞 Telefon: {phone}

🕐 Yetkazib berish vaqti: 25-35 daqiqa
🚚 Kuryer tez orada aloqaga chiqadi

<b>Buyurtmangiz uchun rahmat! 🙏</b>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 ${:.2f} TO'LASH".format(data['final_total']), callback_data=f"pay_{order_number}")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")]
    ])
    
    await message.answer(
        confirmation_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await state.clear()

@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    order_number = callback.data.split("_")[1]
    
    payment_text = f"""
💳 <b>To'lov</b>

📦 Buyurtma: {order_number}

To'lov usulini tanlang:
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Click", callback_data=f"payment_click_{order_number}"),
            InlineKeyboardButton(text="💳 Payme", callback_data=f"payment_payme_{order_number}")
        ],
        [InlineKeyboardButton(text="💵 Naqd", callback_data=f"payment_cash_{order_number}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(
        payment_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("payment_"))
async def handle_payment(callback: CallbackQuery):
    payment_type = callback.data.split("_")[1]
    order_number = callback.data.split("_")[2]
    
    if payment_type == "cash":
        success_text = f"""
✅ <b>To'lov usuli tanlandi</b>

📦 Buyurtma: {order_number}
💵 To'lov: Naqd pul

Kuryer kelganda to'lov qilasiz.
Buyurtmangiz tayyorlanmoqda! 👨‍🍳

<b>Rahmat! 🙏</b>
        """
    else:
        success_text = f"""
✅ <b>To'lov muvaffaqiyatli!</b>

📦 Buyurtma: {order_number}
💳 To'lov: {payment_type.title()}

Buyurtmangiz tayyorlanmoqda! 👨‍🍳

<b>Rahmat! 🙏</b>
        """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(
        success_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
