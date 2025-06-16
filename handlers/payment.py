from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.exceptions import TelegramBadRequest
from services.order_manager import OrderManager
from database.db import SessionLocal
from database.models import User as DBUser
from config import config
import json

router = Router()

@router.message(F.web_app_data)
async def web_app_data(message: Message):
    """Handle data from WebApp"""
    try:
        data = json.loads(message.web_app_data.data)
        
        db = SessionLocal()
        try:
            user = db.query(DBUser).filter(DBUser.telegram_id == message.from_user.id).first()
            if not user:
                return
            
            # Create order
            order = OrderManager.create_order(
                user_id=user.id,
                items=data['items'],
                delivery_address=data.get('address', user.address),
                phone=data.get('phone', user.phone)
            )
            
            # Create invoice
            prices = [LabeledPrice(label="Jami", amount=int(order.total_amount * 100))]  # Amount in kopecks
            
            await message.answer_invoice(
                title="FastFood buyurtma",
                description=f"Buyurtma #{order.id}",
                payload=f"order_{order.id}",
                provider_token=config.PAYMENT_PROVIDER_TOKEN,
                currency="UZS",
                prices=prices,
                start_parameter=f"order_{order.id}",
                photo_url="https://example.com/food-image.jpg",
                photo_width=512,
                photo_height=512
            )
            
        finally:
            db.close()
            
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Handle pre-checkout query"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    """Handle successful payment"""
    payment = message.successful_payment
    order_id = int(payment.invoice_payload.split("_")[1])
    
    # Update order status
    OrderManager.update_order_status(order_id, "paid", payment.telegram_payment_charge_id)
    
    db = SessionLocal()
    try:
        user = db.query(DBUser).filter(DBUser.telegram_id == message.from_user.id).first()
        
        texts = {
            "uz": f"✅ To'lov muvaffaqiyatli amalga oshirildi!\n\nBuyurtma raqami: #{order_id}\n\nTez orada buyurtmangiz tayyorlanadi!",
            "ru": f"✅ Оплата прошла успешно!\n\nНомер заказа: #{order_id}\n\nВаш заказ скоро будет готов!",
            "en": f"✅ Payment completed successfully!\n\nOrder ID: #{order_id}\n\nYour order will be ready soon!"
        }
        
        await message.answer(texts[user.language])
        
        # Notify admins
        for admin_id in config.ADMIN_IDS:
            try:
                await message.bot.send_message(
                    admin_id,
                    f"🆕 Yangi buyurtma!\n\nBuyurtma #{order_id}\nSumma: {payment.total_amount/100} {payment.currency}\nFoydalanuvchi: {user.first_name} (@{user.username})"
                )
            except:
                pass
                
    finally:
        db.close()
