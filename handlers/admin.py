from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import SessionLocal
from database.models import Product, Category, Order, RequiredChannel
from keyboards.inline import admin_keyboard
from config import config
from sqlalchemy import func
from datetime import datetime, timedelta

router = Router()

class AdminStates(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_product_price = State()
    waiting_for_channel_id = State()
    waiting_for_channel_name = State()

@router.message(Command("admin"))
async def admin_command(message: Message):
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    await message.answer(
        "🔧 Admin Panel\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=admin_keyboard()
    )

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    db = SessionLocal()
    try:
        # Get statistics
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        total_orders = db.query(Order).count()
        today_orders = db.query(Order).filter(func.date(Order.created_at) == today).count()
        week_orders = db.query(Order).filter(func.date(Order.created_at) >= week_ago).count()
        month_orders = db.query(Order).filter(func.date(Order.created_at) >= month_ago).count()
        
        total_revenue = db.query(func.sum(Order.total_amount)).filter(Order.status == "paid").scalar() or 0
        today_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.status == "paid",
            func.date(Order.created_at) == today
        ).scalar() or 0
        
        stats_text = f"""📊 Statistika
        
🔢 Jami buyurtmalar: {total_orders}
📅 Bugungi buyurtmalar: {today_orders}
📅 Haftalik buyurtmalar: {week_orders}
📅 Oylik buyurtmalar: {month_orders}

💰 Jami daromad: {total_revenue:,.0f} so'm
💰 Bugungi daromad: {today_revenue:,.0f} so'm"""
        
        await callback.message.edit_text(stats_text, reply_markup=admin_keyboard())
    finally:
        db.close()
    
    await callback.answer()

@router.callback_query(F.data == "admin_products")
async def admin_products(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.is_active == True).all()
        
        products_text = "🍔 Mahsulotlar ro'yxati:\n\n"
        for product in products[:10]:  # Show first 10 products
            products_text += f"{product.emoji} {product.name_uz} - {product.price:,.0f} so'm\n"
        
        if len(products) > 10:
            products_text += f"\n... va yana {len(products) - 10} ta mahsulot"
        
        await callback.message.edit_text(products_text, reply_markup=admin_keyboard())
    finally:
        db.close()
    
    await callback.answer()

@router.callback_query(F.data == "admin_channels")
async def admin_channels(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    db = SessionLocal()
    try:
        channels = db.query(RequiredChannel).filter(RequiredChannel.is_active == True).all()
        
        channels_text = "📢 Majburiy kanallar:\n\n"
        if channels:
            for channel in channels:
                channels_text += f"• {channel.channel_name} ({channel.channel_id})\n"
        else:
            channels_text += "Hech qanday majburiy kanal yo'q"
        
        await callback.message.edit_text(channels_text, reply_markup=admin_keyboard())
    finally:
        db.close()
    
    await callback.answer()
