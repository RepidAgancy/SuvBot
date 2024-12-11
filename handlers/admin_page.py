from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from utils.filters import AdminFilter
from utils.ppginator import Paginator

import database.requests as rq
import database.sync_to_async as syn

ADMIN_IDS = [5714872865]

admin_router = Router()

admin_router.message.filter(AdminFilter(admin_ids=ADMIN_IDS))

paginator = None

async def pagination_keyboard():
    buttons = []
    if paginator.page > 1:
        buttons.append(InlineKeyboardButton(text = "◀ Prev", callback_data="prev"))
    if paginator.page < paginator.pages:
        buttons.append(InlineKeyboardButton(text = "Next ▶", callback_data="next"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@admin_router.message(Command("start"))
async def run_as_admin(message: Message):
    global paginator

    data = await rq.get_all_orders()
    formatted_messages = await syn.format_orders_for_message(data)

    # Initialize paginator with data
    paginator = Paginator(formatted_messages, per_page=1)

    # Send the first page
    current_page = paginator.get_page()
    await message.answer(
        current_page[0], reply_markup=await pagination_keyboard()
    )


@admin_router.callback_query(F.data.in_({"prev", "next"}))
async def handle_pagination(callback: CallbackQuery):
    global paginator

    if callback.data == "next":
        paginator.get_next()
    elif callback.data == "prev":
        paginator.get_previous()

    current_page = paginator.get_page()
    
    await callback.message.edit_text(
        current_page[0], reply_markup=await pagination_keyboard()
    )
    await callback.answer()
