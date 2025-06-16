import json
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from database.db import Database
from config import config

router = Router()
logger = logging.getLogger(__name__)
db = Database()

@router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    """Handle data received from the web app."""
    try:
        # Get the data sent from the web app
        web_app_data = message.web_app_data.data
        logger.info(f"Received WebApp data: {web_app_data}")
        
        # Parse the JSON data
        order_data = json.loads(web_app_data)
        
        # Extract order information
        items = order_data.get('items', [])
        total_amount = order_data.get('totalAmount', 0)
        customer_info = order_data.get('customerInfo', {})
        phone = customer_info.get('phone', '')
        address = customer_info.get('address', '')
        
        if not items or not phone or not address:
            await message.answer("❌ Buyurtma ma'lumotlari to'liq emas!")
            return
        
        # Save order to database
        result = db.execute_query("""
            INSERT INTO orders (user_id, user_name, phone, address, items, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            message.from_user.id,
            message.from_user.first_name or "Unknown",
            phone,
            address,
            json.dumps(items, ensure_ascii=False),
            total_amount
        ))
        
        if result is None:
            await message.answer("❌ Buyurtmani saqlashda xatolik yuz berdi!")
            return
        
        # Get order ID
        order_result = db.execute_query(
            "SELECT id FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (message.from_user.id,)
        )
        order_id = order_result[0][0] if order_result else "N/A"
        
        # Format the order message
        order_message = "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
        order_message += f"📋 <b>Buyurtma raqami:</b> #{order_id}\n"
        order_message += f"👤 <b>Mijoz:</b> {message.from_user.first_name}\n"
        order_message += f"📱 <b>Telefon:</b> {phone}\n"
        order_message += f"📍 <b>Manzil:</b> {address}\n\n"
        order_message += "<b>🛒 Buyurtma tafsilotlari:</b>\n"
        
        for item in items:
            name = item.get('name', '')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            total_item_price = price * quantity
            order_message += f"• {name} x{quantity} - {total_item_price:,} so'm\n"
        
        order_message += f"\n💰 <b>Jami summa:</b> {total_amount:,} so'm"
        order_message += f"\n\n⏰ Buyurtmangiz 30-45 daqiqada tayyor bo'ladi."
        order_message += f"\n📞 Aloqa uchun: +998 90 123 45 67"
        
        # Send confirmation to user
        await message.answer(
            order_message,
            parse_mode=ParseMode.HTML
        )
        
        # Send notification to admin
        await notify_admin_about_order(message.bot, order_data, order_id, message.from_user)
        
        logger.info(f"Order #{order_id} saved for user {message.from_user.id}: {total_amount} som")
        
    except json.JSONDecodeError:
        logger.error("Failed to parse web app data as JSON")
        await message.answer(
            "❌ Buyurtmani qayta ishlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )
    except Exception as e:
        logger.error(f"Error handling web app data: {e}")
        await message.answer(
            "❌ Buyurtmani qayta ishlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )

async def notify_admin_about_order(bot, order_data: dict, order_id: int, user):
    """Send notification to admin about new order."""
    try:
        if config.ADMIN_ID:
            items = order_data.get('items', [])
            customer_info = order_data.get('customerInfo', {})
            
            admin_message = f"🔔 <b>Yangi buyurtma #{order_id}</b>\n\n"
            admin_message += f"👤 <b>Mijoz:</b> {user.first_name} (@{user.username or 'username_yoq'})\n"
            admin_message += f"📱 <b>Telefon:</b> {customer_info.get('phone', 'N/A')}\n"
            admin_message += f"📍 <b>Manzil:</b> {customer_info.get('address', 'N/A')}\n\n"
            admin_message += "<b>🛒 Buyurtma:</b>\n"
            
            for item in items:
                name = item.get('name', '')
                quantity = item.get('quantity', 0)
                admin_message += f"• {name} x{quantity}\n"
            
            admin_message += f"\n💰 <b>Jami:</b> {order_data.get('totalAmount', 0):,} so'm"
            
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text=admin_message,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")
