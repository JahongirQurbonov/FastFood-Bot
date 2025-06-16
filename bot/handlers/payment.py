from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config
import json

router = Router()

@router.callback_query(F.data.startswith("webapp_payment_"))
async def handle_webapp_payment(callback: CallbackQuery):
    """Web App'dan kelgan to'lov so'rovini qayta ishlash"""
    try:
        # Web App'dan kelgan ma'lumotlarni parse qilish
        data = json.loads(callback.data.split("webapp_payment_")[1])
        
        order_data = data.get('order', {})
        amount = int(float(data.get('amount', 0)) * 100)  # Telegram tiyin hisobida
        
        # Telegram Invoice yaratish
        prices = [LabeledPrice(label="Buyurtma", amount=amount)]
        
        await callback.message.answer_invoice(
            title="Durger King - Buyurtma",
            description=f"Buyurtma #{order_data.get('orderNumber', 'N/A')}",
            payload=f"order_{order_data.get('orderNumber', 'unknown')}",
            provider_token=config.PAYMENT_PROVIDER_TOKEN,  # Sizning to'lov provider tokeningiz
            currency="USD",
            prices=prices,
            start_parameter="fastfood_payment",
            photo_url="https://example.com/burger.jpg",  # Buyurtma rasmi
            photo_width=512,
            photo_height=512,
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            is_flexible=False
        )
        
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        print(f"Payment error: {e}")

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """To'lovdan oldin tekshirish"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Muvaffaqiyatli to'lov"""
    payment = message.successful_payment
    
    success_text = f"""
✅ <b>To'lov muvaffaqiyatli!</b>

💳 To'lov miqdori: {payment.total_amount // 100} {payment.currency}
📦 Buyurtma: {payment.invoice_payload}
🧾 Telegram to'lov ID: {payment.telegram_payment_charge_id}

Buyurtmangiz tayyorlanmoqda! 👨‍🍳
Tez orada kuryer aloqaga chiqadi.

<b>Rahmat! 🙏</b>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")]
    ])
    
    await message.answer(
        success_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
