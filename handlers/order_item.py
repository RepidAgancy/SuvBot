import logging

from aiogram import F, Router
from aiogram.types import Message

from utils.ppginator import Paginator
import database.requests as rq
import markups as btn
import database.sync_to_async as sn

order_item_router = Router()

paginator = None

@order_item_router.message(F.text == '🛒 Korzinka')
async def all_product(message:Message):
    basket_items = await rq.get_all_basket_items_with_products(user_id=message.from_user.id)
    if basket_items['items'] == []:
        await message.answer("Uzr jigar korzinkada hech nima yo'q")
        return 

    for text, image, keyboard in await sn.get_basket_inline_btn(basket_items):
        await message.answer_photo(photo=image, caption=text,reply_markup=keyboard)







