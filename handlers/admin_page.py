import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from utils.filters import AdminFilter
import database.requests as rq
import database.sync_to_async as syn

ADMIN_IDS = [5714872865]

admin_router = Router()

admin_router.message.filter(AdminFilter(admin_ids=ADMIN_IDS))


@admin_router.message(Command('start'))
async def run_as_admin(message:Message):
    data = await rq.get_all_orders()
    
    formatted_message = await syn.format_orders_for_message(data)
    await message.answer(formatted_message)
