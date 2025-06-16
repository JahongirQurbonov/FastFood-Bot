from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from config import config
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("pay"))
async def process_payment(message: Message):
    """Process payment for an order."""
    # This is a placeholder for payment processing
    # You would integrate with actual payment providers here
    
    prices = [LabeledPrice(label="Buyurtma", amount=25000 * 100)]  # Amount in kopecks
    
    await message.answer_invoice(
        title="FastFood Buyurtma",
        description="Sizning buyurtmangiz uchun to'lov",
        payload="fastfood_payment",
        provider_token=config.PAYMENT_TOKEN,
        currency="UZS",
        prices=prices,
        start_parameter="payment",
        photo_url="https://example.com/food-image.jpg",
        photo_width=512,
        photo_height=512,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        is_flexible=False
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Process pre-checkout query."""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Process successful payment."""
    payment = message.successful_payment
    
    success_message = (
        "✅ <b>To'lov muvaffaqiyatli amalga oshirildi!</b>\n\n"
        f"💰 <b>Summa:</b> {payment.total_amount // 100} {payment.currency}\n"
        f"🆔 <b>To'lov ID:</b> {payment.provider_payment_charge_id}\n\n"
        "🍔 Buyurtmangiz tez orada tayyorlanadi!\n"
        "📞 Aloqa: +998 90 123 45 67"
    )
    
    await message.answer(success_message, parse_mode="HTML")
    logger.info(f"Payment successful: {payment.provider_payment_charge_id}")
