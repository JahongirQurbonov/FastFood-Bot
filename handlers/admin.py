from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from database.db import Database
from config import config
import json

router = Router()
db = Database()

@router.callback_query(F.data == "admin_stats")
async def show_admin_stats(callback: CallbackQuery):
    """Show admin statistics."""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Sizda admin huquqlari yo'q!", show_alert=True)
        return
    
    # Get statistics from database
    total_users = db.execute_query("SELECT COUNT(*) FROM users")
    total_orders = db.execute_query("SELECT COUNT(*) FROM orders")
    pending_orders = db.execute_query("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
    total_revenue = db.execute_query("SELECT SUM(total_amount) FROM orders WHERE payment_status = 'completed'")
    
    stats_text = "📊 <b>Bot Statistikasi:</b>\n\n"
    stats_text += f"👥 Jami foydalanuvchilar: {total_users[0][0] if total_users else 0}\n"
    stats_text += f"📋 Jami buyurtmalar: {total_orders[0][0] if total_orders else 0}\n"
    stats_text += f"⏳ Kutilayotgan buyurtmalar: {pending_orders[0][0] if pending_orders else 0}\n"
    stats_text += f"💰 Jami daromad: {total_revenue[0][0] or 0:,} so'm"
    
    await callback.message.edit_text(stats_text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin_orders")
async def show_admin_orders(callback: CallbackQuery):
    """Show recent orders for admin."""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Sizda admin huquqlari yo'q!", show_alert=True)
        return
    
    # Get recent orders
    orders = db.execute_query("""
        SELECT id, user_name, phone, total_amount, status, created_at 
        FROM orders 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    if not orders:
        await callback.message.edit_text("📋 Hozircha buyurtmalar yo'q.")
        await callback.answer()
        return
    
    orders_text = "📋 <b>So'nggi buyurtmalar:</b>\n\n"
    
    for order in orders:
        order_id, user_name, phone, amount, status, created_at = order
        status_emoji = "⏳" if status == "pending" else "✅" if status == "completed" else "❌"
        orders_text += f"{status_emoji} <b>#{order_id}</b> - {user_name}\n"
        orders_text += f"📱 {phone} | 💰 {amount:,} so'm\n"
        orders_text += f"📅 {created_at}\n\n"
    
    await callback.message.edit_text(orders_text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin_menu")
async def show_admin_menu(callback: CallbackQuery):
    """Show menu management for admin."""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Sizda admin huquqlari yo'q!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Yangi taom qo'shish", callback_data="add_menu_item")],
        [InlineKeyboardButton(text="📝 Taomlarni tahrirlash", callback_data="edit_menu_items")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_admin")]
    ])
    
    await callback.message.edit_text(
        "🍔 <b>Menyu boshqaruvi</b>\n\nKerakli amalni tanlang:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
