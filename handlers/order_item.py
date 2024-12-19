import logging

from aiogram import F, Router
from aiogram.types import Message

from utils.translation import translate as _
from utils.ppginator import Paginator
import database.requests as rq
import markups as btn
import database.sync_to_async as sn

order_item_router = Router()

paginator = None

@order_item_router.message(F.text.in_({'🛒 Korzinka','🛒 Корзина','🛒 Basket'}))
async def all_product(message:Message):
    user = await rq.get_user(message.from_user.id)
    basket_items = await rq.get_all_basket_items_with_products(user_id=message.from_user.id)
    if 'message' in basket_items or basket_items['items'] == []:
        await message.answer(_("Uzr jigar korzinkada hech nima yo'q",user['lang']))
        return 

    for text, image, keyboard in await sn.get_basket_inline_btn(basket_items,user['lang']):
        await message.answer_photo(photo=image, caption=text,reply_markup=keyboard)







