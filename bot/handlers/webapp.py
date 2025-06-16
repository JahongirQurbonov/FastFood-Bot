from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config
import json

router = Router()

@router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    """Web App'dan kelgan ma'lumotlarni qayta ishlash"""
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        
        if action == "initiate_payment":
            await handle_payment_request(message, data)
        elif action == "add_to_cart":
            await handle_add_to_cart(message, data)
            
    except Exception as e:
        await message.answer("Xatolik yuz berdi!")
        print(f"WebApp data error: {e}")

async def handle_payment_request(message: Message, data):
    """To'lov so'rovini qayta ishlash"""
    order = data.get('order', {})
    items = order.get('items', [])
    total = order.get('total', 0)
    order_number = order.get('orderNumber', 'N/A')
    
    # So'mni tiyin'ga aylantirish (1 so'm = 1 tiyin Telegram'da UZS uchun)
    total_tiyin = int(total)
    
    # Telegram Invoice yaratish
    prices = [LabeledPrice(label="Buyurtma", amount=total_tiyin)]
    
    # Agar yetkazib berish haqi bo'lsa
    delivery = order.get('delivery', 0)
    if delivery > 0:
        prices.append(LabeledPrice(label="Yetkazib berish", amount=int(delivery)))
    
    # Mahsulotlar ro'yxatini yaratish
    items_text = "\n".join([
        f"{item['emoji']} {item['name_uz']} x{item['quantity']} - {format_uzs(item['price'] * item['quantity'])}"
        for item in items
    ])
    
    description = f"Buyurtma #{order_number}\n\n{items_text}"
    
    try:
        await message.answer_invoice(
            title="🍔 Durger King - Buyurtma",
            description=description,
            payload=f"order_{order_number}",
            provider_token=config.PAYMENT_PROVIDER_TOKEN,
            currency="UZS",  # So'm valyutasi
            prices=prices,
            start_parameter="fastfood_payment",
            photo_url="https://i.imgur.com/burger.jpg",
            photo_width=512,
            photo_height=512,
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            is_flexible=False
        )
    except Exception as e:
        # Agar to'lov provider sozlanmagan bo'lsa
        await message.answer(
            f"""
✅ <b>Buyurtma qabul qilindi!</b>

📦 Buyurtma: #{order_number}
💰 Jami: {format_uzs(total)}

{items_text}

📞 Kuryer tez orada aloqaga chiqadi.
💵 To'lov: Naqd (kuryer kelganda)

<b>Rahmat! 🙏</b>
            """,
            parse_mode="HTML"
        )

def format_uzs(amount):
    """So'mni formatlash"""
    return f"{amount:,}".replace(",", " ") + " so'm"

async def handle_add_to_cart(message: Message, data):
    """Savatga qo'shish"""
    item_id = data.get('item_id')
    cart = data.get('cart', {})
    
    await message.answer("✅ Mahsulot savatga qo'shildi!")

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

💳 To'lov miqdori: {format_uzs(payment.total_amount)}
📦 Buyurtma: {payment.invoice_payload}
🧾 To'lov ID: {payment.telegram_payment_charge_id}

🕐 Tayyorlanish vaqti: 25-35 daqiqa
🚚 Kuryer tez orada aloqaga chiqadi

<b>Buyurtmangiz uchun rahmat! 🙏</b>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="back_to_main")],
        [InlineKeyboardButton(text="📋 Buyurtmalarim", callback_data="my_orders")]
    ])
    
    await message.answer(
        success_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
