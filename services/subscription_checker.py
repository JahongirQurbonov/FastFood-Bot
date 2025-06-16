from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from typing import List
from database.models import RequiredChannel

async def check_user_subscriptions(bot: Bot, user_id: int, channels: List[RequiredChannel]) -> bool:
    """Check if user is subscribed to all required channels"""
    for channel in channels:
        try:
            member = await bot.get_chat_member(channel.channel_id, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except TelegramBadRequest:
            # Channel not found or bot is not admin
            continue
    return True
